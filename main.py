import pandas as pd
import networkx as nx
import os
from pathlib import Path

from src import (
    clean_dataframe,
    clean,
    get_basic_metrics,
    get_connected_components,
    calculate_all_centralities, 
    compute_communities,
    create_subgraph_by_metric,
    create_subgraph_by_in_degree,
    create_subgraph_by_degree,
    plot_top_metrics, 
    plot_wordcloud_and_rank,
    plot_communities_distribution,
    export_to_gephi
)

# ============================================================
# CONFIGURATION
# ============================================================

CONFIG = {
    "full_run" : False, # if set to true, runs everything from scratch
    "input_dirs": {
        "descriptions" : "../../python-ecosystem-evolution/data/raw.parquet"
        },
    "output_dirs": ["output", "output/images", "output/gephi", "output/csv"],
    "load_params": {
        "load_centralities" : True,
        "load_communities" : True,
    },
    "compute" : {
        "Subgraphs" : False,
        "Top Metrics": False,
        "Wordclouds" : True,
        "save_stats" : False,
        },
    "subgraph_params": {
        "in_degree_threshold": 500,
        "degree_min": 45,
        "pagerank_percentile": 0,
        "betweenness_top_n": 300,
        "communities_top_n": 10
    },
    "visualization_params": {
        "top_n_metrics": 15,
        "pagerank_max_iter": 50
    }
}

def setup_directories():
    """Create output directories."""
    for directory in CONFIG["output_dirs"]:
        os.makedirs(directory, exist_ok=True)

def load_and_clean_data(file_path, year):
    """Load and clean data from CSV or Parquet."""
    file_path = Path(file_path)
    print(f"\n📂 Loading {file_path.name} for year {year}...")
    
    try:
        if file_path.suffix == ".parquet":
            df = clean_dataframe(str(file_path))
        elif file_path.suffix == ".csv":
            df = pd.read_csv(file_path)
        else:
            raise ValueError(f"Unsupported format: {file_path.suffix}")
        
        # Ensure correct columns exist
        if 'package_name' not in df.columns or 'requirement' not in df.columns:
            print(f"⚠ CSV columns: {df.columns.tolist()}")
            print("⚠ Expected: package_name, requirement")
            raise ValueError("Missing required columns")
        
        # Keep only necessary columns
        df = df[['package_name', 'requirement']]
        
        # Remove NaNs
        df = df.dropna()
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Save clean data
        if file_path.suffix == ".parquet":
            os.makedirs("data", exist_ok=True) # Ensure dir exists
            out_path = f"data/clean_data_{year}.csv"
            df.to_csv(out_path, index=False)
            print(f"✓ Saved clean dataframe to {out_path}")
        
        print(f"✓ Loaded: {len(df):,} clean rows ({df['package_name'].nunique():,} packages)")
        return df
    except Exception as e:
        print(f"✗ Error loading {file_path}: {e}")
        return None


def load_descriptions():
    print("""Loading package summaries""")
    try:
        df = pd.read_parquet(CONFIG["input_dirs"]["descriptions"])
    except Exception as e:
        print(f"⚠ Error loading descriptions: {e}")
        return None
    
    df['name'] = df["name"].apply(clean)
    df = df[["name","summary"]].drop_duplicates()

    return df


def analyze_centralities(year, G):
    if CONFIG["load_params"]["load_centralities"]:
        print("\n--- LOADING CENTRALITIES ---")
        file_path = f"./output/csv/centralities_{year}.csv"
        try:
            df_metrics = pd.read_csv(file_path)
            print("✓ Loaded")
        except Exception as e:
            print(f"✗ Error loading {file_path}: {e}")
            print("\n--- CALCULATING CENTRALITIES ---")
            df_metrics = calculate_all_centralities(G)
            print("✓ Calculated")
    else:
        print("\n--- CALCULATING CENTRALITIES ---")
        df_metrics = calculate_all_centralities(G)
        print("✓ Calculated")
    
    return df_metrics


def create_subgraphs(year, G, G_und, df_metrics):
    print("\n--- SUBGRAPHS ---")
    pr_dict = dict(zip(df_metrics['node'], df_metrics['pagerank']))
    bet_dict = dict(zip(df_metrics['node'], df_metrics['betweenness_centrality']))
    
    try:
        sub_deg, _ = create_subgraph_by_in_degree(G, threshold=CONFIG["subgraph_params"]["in_degree_threshold"])
        print(f"✓ In-degree: {sub_deg.number_of_nodes()} nodes")
        export_to_gephi(sub_deg, f"output/gephi/subgrafo_in_degree_{year}.gexf")
    except Exception as e:
        print(f"⚠ In-degree error: {e}")
    
    try:
        sub_deg, _ = create_subgraph_by_degree(G_und, min_degree=CONFIG["subgraph_params"]["degree_min"])
        print(f"✓ Degree: {sub_deg.number_of_nodes()} nodes")
        export_to_gephi(sub_deg, f"output/gephi/subgrafo_degree_{year}.gexf")
    except Exception as e:
        print(f"⚠ Degree error: {e}")

    try:
        pr_series = pd.Series(pr_dict)
        threshold = pr_series.quantile(CONFIG["subgraph_params"]["pagerank_percentile"])
        nodes = [n for n, v in pr_dict.items() if v >= threshold]
        sub_pr = G_und.subgraph(nodes).copy()
        nx.set_node_attributes(sub_pr, pr_dict, "pagerank")
        nx.set_node_attributes(sub_pr, bet_dict, "betweenness")
        print(f"✓ PageRank: {sub_pr.number_of_nodes()} nodes")
        export_to_gephi(sub_pr, f"output/gephi/subgrafo_pagerank_{year}_{CONFIG["subgraph_params"]["pagerank_percentile"]}.gexf")
    except Exception as e:
        print(f"⚠ PageRank error: {e}")
    
    try:
        top_n = CONFIG["subgraph_params"]["betweenness_top_n"]
        sub_bet, _ = create_subgraph_by_metric(G, bet_dict, top_n=top_n)
        print(f"✓ Betweenness (top {top_n}): {sub_bet.number_of_nodes()} nodes")
        export_to_gephi(sub_bet, f"output/gephi/subgrafo_betweenness_{year}.gexf")
    except Exception as e:
        print(f"⚠ Betweenness error: {e}")


def compute_wordclouds(year, G, df_metrics, comm_sizes, partition):
    print("\n--- WORDCLOUDS ---")

    df_descriptions = load_descriptions()
    pr_dict = dict(zip(df_metrics['node'], df_metrics['pagerank']))
    communities = {}
    for i, comm_id in enumerate(comm_sizes.head(CONFIG["subgraph_params"]["communities_top_n"]).index, 1):
        communities[comm_id] = [n for n, c in partition.items() if c == comm_id]
    
    try:
        for i, comm_id in enumerate(comm_sizes.head(CONFIG["subgraph_params"]["communities_top_n"]).index, 1):
            plot_wordcloud_and_rank(
                communities[comm_id], f"Year {year} - Community Top {i}", f"{year}_{i}",
                pr_dict, df_descriptions,
                save=True, save_path=f"output/images/wordcloud_{year}_{i}.png"
            )

        print("✓ Generated")
    except Exception as e:
        print(f"⚠ Error: {e}")


def analyze_single_dataset(year, df_clean):
    """Analyze a single year dataset."""
    print(f"\n{'='*60}\n ANALYZING YEAR: {year}\n{'='*60}")
    
    # Build graph
    G = nx.from_pandas_edgelist(
        df_clean, source='package_name', target='requirement', create_using=nx.DiGraph()
    )
    G_und = G.to_undirected()
    print(f"✓ Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    

    # Metrics
    print("\n--- BASIC METRICS ---")
    stats = get_basic_metrics(G)
    for k, v in stats.items():
        print(f"{k}: {v:,.2f}" if isinstance(v, float) else f"{k}: {v:,}")
    
    
    # Components
    print("\n--- CONNECTED COMPONENTS ---")
    comp_stats = get_connected_components(G)
    for k, v in comp_stats.items():
        print(f"{k}: {v}")
    
    
    # Centralities
    df_metrics = analyze_centralities(year, G)

    
    # Visualize Metrics
    if CONFIG["compute"]["Top Metrics"]:
        print("\n--- VISUALIZING METRICS ---")
        for col in [
            "degree_centrality", "pagerank", "betweenness_centrality", "closeness_centrality"
            ]:
            plot_top_metrics(df_metrics, col, year, top_n=CONFIG["visualization_params"]["top_n_metrics"])


    # Communities
    if CONFIG["load_params"]["load_communities"]:
        print("\n--- LOADING COMMUNITIES ---")
        try:
            partition  = pd.read_csv(f"output/csv/community_partition_{year}.csv",
                                     index_col=0, header=0).iloc[:,0].to_dict()
            print("✓ Partition loaded")
        except Exception as e:
            print(f"✗ Error loading output/csv/community_partition_{year}.csv: {e}")
        try:
            comm_sizes = pd.read_csv(f"output/csv/community_sizes_{year}.csv",
                                     index_col=0, header=0).iloc[:,0]
            print("✓ Communities sizes loaded")
        except Exception as e:
            print(f"✗ Error loading output/csv/community_sizes_{year}.csv: {e}")

    else:
        print("\n--- CALCULATING COMMUNITIES ---")
        G_und, partition, modularity, comm_sizes = compute_communities(G_und)
        pd.Series(partition,name="comm_id").to_csv(f"output/csv/community_partition_{year}.csv")
        comm_sizes.to_csv(f"output/csv/community_sizes_{year}.csv")

        print(f"✓ Found {len(set(partition.values()))} communities")
        print(f"✓ Modularity: {modularity:.4f}")    

    # Community distribution
    print("\n--- VISUALIZING COMMUNITY DISTRIBUTION ---")    
    plot_communities_distribution(comm_sizes, year, 15)
    
    # Subgraphs
    if CONFIG["compute"]["Subgraphs"]:
        create_subgraphs(year, G, G_und, df_metrics)

    
    # Wordclouds
    compute_wordclouds(year, G, df_metrics, comm_sizes, partition)

    # Export
    print("\n--- EXPORTING CSV ---")
    df_metrics.to_csv(f"output/csv/centralities_{year}.csv", index=False)
    pd.DataFrame({
        'community_id': comm_sizes.index,
        'size': comm_sizes.values,
        'percentage': 100 * comm_sizes.values / len(partition)
    }).to_csv(f"output/csv/communities_{year}.csv", index=False)
    pd.DataFrame({
        'Metric': list(stats.keys()) + list(comp_stats.keys()),
        'Value': list(stats.values()) + list(comp_stats.values())
    }).to_csv(f"output/csv/summary_{year}.csv", index=False)
    print("✓ Exported")
    


# ============================================================
# MAIN: ANALYZE DATASETS
# ============================================================

def analyze_datasets(**datasets):
    """
    Analyze one or multiple datasets.
    Pass datasets as keyword arguments: year_key=file_path
    
    Example:
        analyze_datasets(Y2016="data/clean_data_2016.csv")
        analyze_datasets(Y2016="data/raw_2016.parquet", Y2025="data/clean_data_2025.csv")
        analyze_datasets(Y2025="data/raw.parquet")
    """
    if not datasets:
        print("❌ No datasets provided!")
        return
    
    setup_directories()

    
    results = {}
    
    # Process datasets
    for year_key, file_path in datasets.items():
        year = year_key.replace("Y", "")
        df = load_and_clean_data(file_path, year)
        if df is not None:
            stats = analyze_single_dataset(year, df)
            results[year] = stats
    
    # Compare if multiple datasets
    if len(results) > 1:
        print("\n" + "="*60)
        print(" COMPARISON TABLE")
        print("="*60)
        comparison_df = pd.DataFrame(results).T
        print(comparison_df)
        comparison_df.to_csv("output/csv/comparison.csv")
    
    print("\n✓ Complete!")

if __name__ == "__main__":
    if CONFIG["full_run"]:
        for k in CONFIG["load_params"].keys():
            CONFIG["load_params"][k] = False
        for k in CONFIG["compute"].keys():
            CONFIG["compute"][k] = True


    # Example usage - uncomment and modify as needed:
    analyze_datasets(
        Y2016="../../python-ecosystem-evolution/data/clean_data_2016.csv",
        # Y2025="data/clean_data_2025.csv",
        # Y2025="../../python-ecosystem-evolution/data/raw.parquet"
    )
    
    # Or single dataset:
    # analyze_datasets(Y2025="data/raw.parquet")
    
    # Or mix CSV and parquet:
    # analyze_datasets(Y2016="data/raw_2016.parquet", Y2025="data/clean_data_2025.csv")
