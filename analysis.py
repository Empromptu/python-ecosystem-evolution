import pandas as pd
import networkx as nx
import os
from src import (
    standardize_and_clean, 
    get_basic_metrics,
    get_connected_components,
    calculate_all_centralities, 
    compute_communities,
    create_subgraph_by_metric,
    create_subgraph_by_in_degree,
    create_subgraph_by_degree,
    create_top_communities_subgraph,
    plot_top_metrics, 
    plot_wordcloud_and_rank,
    export_to_gephi
)

# ============================================================
# CONFIGURATION & SETUP
# ============================================================

# Create output directories
os.makedirs("output", exist_ok=True)
os.makedirs("output/images", exist_ok=True)
os.makedirs("output/gephi", exist_ok=True)
os.makedirs("output/csv", exist_ok=True)

# Load descriptions once (shared for both years)
try:
    df_desc = pd.read_parquet("data/raw.parquet")
    df_desc['name_clean'] = df_desc['name'].str.lower().str.strip()
except FileNotFoundError:
    print("⚠ Warning: raw.parquet not found. WordClouds will be skipped.")
    df_desc = None

# Define the years and paths to analyze
datasets = [
    {"year": "2016", "path": "data/clean_data_2016.csv"},
    {"year": "2025", "path": "data/clean_data_2025.csv"}
]

# Dictionary to store results for final comparison
comparison_results = {}

# ============================================================
# MAIN ANALYSIS LOOP
# ============================================================

for item in datasets:
    year = item["year"]
    print(f"\n{'='*60}")
    print(f" ANALYZING YEAR: {year} ")
    print(f"{'='*60}")

    # A. Clean and Standardize
    df_clean = standardize_and_clean(item["path"], year)
    print(f"✓ Cleaned data: {len(df_clean)} edges")

    # B. Build Graphs
    G = nx.from_pandas_edgelist(
        df_clean, 
        source='package_name', 
        target='requirement', 
        create_using=nx.DiGraph()
    )
    G_undirected = G.to_undirected()
    print(f"✓ Directed graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    # C. Calculate Basic Metrics
    print("\n--- BASIC METRICS ---")
    stats = get_basic_metrics(G)
    print(f"Nodes: {stats['nodes']:,}")
    print(f"Edges: {stats['edges']:,}")
    print(f"Avg degree: {stats['degree_avg']:.2f}")
    if 'in_degree_avg' in stats:
        print(f"Avg in-degree: {stats['in_degree_avg']:.2f}")
        print(f"Avg out-degree: {stats['out_degree_avg']:.2f}")

    # D. Connected Components Analysis
    print("\n--- CONNECTED COMPONENTS ---")
    comp_stats = get_connected_components(G)
    for key, value in comp_stats.items():
        print(f"{key}: {value}")

    # E. Calculate Centralities
    print("\n--- CALCULATING CENTRALITIES (this may take a moment) ---")
    df_metrics = calculate_all_centralities(G)
    print(f"✓ Calculated 4 centrality metrics")

    # F. Visualize Top Metrics
    print("\n--- VISUALIZING TOP METRICS ---")
    metrics_to_plot = [
        ("degree_centrality", f"Degree Centrality ({year})"),
        ("pagerank", f"Page Rank ({year})"),
        ("betweenness_centrality", f"Betweenness Centrality ({year})")
    ]
    for col, title in metrics_to_plot:
        plot_top_metrics(df_metrics, col, title, top_n=10)

    # G. Community Detection
    print("\n--- COMMUNITY DETECTION ---")
    G_und, partition, modularity, community_sizes = compute_communities(G.to_undirected())
    print(f"✓ Communities found: {len(set(partition.values()))}")
    print(f"✓ Modularity: {modularity:.4f}")
    print(f"✓ Largest community: {community_sizes.max()} nodes")
    print(f"✓ Density: {nx.density(G_und):.4f}")

    # H. Create Subgraphs
    print("\n--- CREATING SUBGRAPHS ---")
    pr_dict = dict(zip(df_metrics['node'], df_metrics['pagerank']))
    bet_dict = dict(zip(df_metrics['node'], df_metrics['betweenness_centrality']))

    # H1. Subgraph by in_degree (directed)
    try:
        sub_in_deg, nodes_in_deg = create_subgraph_by_in_degree(G, threshold=500)
        print(f"✓ Subgraph (in_degree > 500): {sub_in_deg.number_of_nodes()} nodes, {sub_in_deg.number_of_edges()} edges")
        export_to_gephi(sub_in_deg, f"output/gephi/subgrafo_in_degree_500_{year}.gexf")
    except Exception as e:
        print(f"✗ Error in in_degree subgraph: {e}")

    # H2. Subgraph by degree (undirected)
    try:
        sub_deg, nodes_deg = create_subgraph_by_degree(G_und, min_degree=45)
        print(f"✓ Subgraph (degree >= 45): {sub_deg.number_of_nodes()} nodes, {sub_deg.number_of_edges()} edges")
        export_to_gephi(sub_deg, f"output/gephi/subgrafo_degree_45_{year}.gexf")
    except Exception as e:
        print(f"✗ Error in degree subgraph: {e}")

    # H3. Subgraph by PageRank (top 5%)
    try:
        pr_series = pd.Series(pr_dict)
        umbral = pr_series.quantile(0.95)
        top_pr_nodes = [n for n, v in pr_dict.items() if v >= umbral]
        sub_pr = G.subgraph(top_pr_nodes).copy()
        print(f"✓ Subgraph (top 5% PageRank): {sub_pr.number_of_nodes()} nodes, {sub_pr.number_of_edges()} edges")
        export_to_gephi(sub_pr, f"output/gephi/subgrafo_pagerank_top5_{year}.gexf")
    except Exception as e:
        print(f"✗ Error in PageRank subgraph: {e}")

    # H4. Subgraph by Betweenness (top 300)
    try:
        sub_bet, nodes_bet = create_subgraph_by_metric(G, bet_dict, top_n=300)
        print(f"✓ Subgraph (top 300 Betweenness): {sub_bet.number_of_nodes()} nodes, {sub_bet.number_of_edges()} edges")
        export_to_gephi(sub_bet, f"output/gephi/subgrafo_betweenness_300_{year}.gexf")
    except Exception as e:
        print(f"✗ Error in Betweenness subgraph: {e}")

    # H5. Subgraph from top 3 communities
    try:
        sub_top3, top3_comm = create_top_communities_subgraph(G_und, partition, top_n=3)
        print(f"✓ Subgraph (top 3 communities): {sub_top3.number_of_nodes()} nodes, {sub_top3.number_of_edges()} edges")
        export_to_gephi(sub_top3, f"output/gephi/subgrafo_top3_comunidades_{year}.gexf")
    except Exception as e:
        print(f"✗ Error in top 3 communities subgraph: {e}")

    # I. Export Complete Graph with Community Attributes
    print("\n--- EXPORTING GRAPHS ---")
    try:
        degrees = dict(G_und.degree())
        pagerank_und = nx.pagerank(G_und, max_iter=50)
        
        nx.set_node_attributes(G_und, partition, 'community')
        nx.set_node_attributes(G_und, degrees, 'degree')
        nx.set_node_attributes(G_und, pagerank_und, 'pagerank')
        
        export_to_gephi(G_und, f"output/gephi/grafo_completo_{year}.gexf")
        print(f"✓ Exported complete graph")
    except Exception as e:
        print(f"✗ Error exporting complete graph: {e}")

    # J. Export Summary Statistics to CSV
    print("\n--- EXPORTING CSV FILES ---")
    try:
        # Centralities summary
        df_metrics.to_csv(f"output/csv/centralities_{year}.csv", index=False)
        print(f"✓ Exported centralities to CSV")
        
        # Community sizes
        community_df = pd.DataFrame({
            'community_id': community_sizes.index,
            'size': community_sizes.values,
            'percentage': 100 * community_sizes.values / len(partition)
        })
        community_df.to_csv(f"output/csv/communities_{year}.csv", index=False)
        print(f"✓ Exported communities to CSV")
        
        # Summary stats
        summary_df = pd.DataFrame({
            'Metric': list(stats.keys()) + list(comp_stats.keys()),
            'Value': list(stats.values()) + list(comp_stats.values())
        })
        summary_df.to_csv(f"output/csv/summary_{year}.csv", index=False)
        print(f"✓ Exported summary to CSV")
    except Exception as e:
        print(f"✗ Error exporting CSV: {e}")

    # K. WordClouds for Top Communities
    if df_desc is not None:
        print("\n--- GENERATING WORDCLOUDS ---")
        try:
            top_3_comms = community_sizes.head(3).index.tolist()
            for i, comm_id in enumerate(top_3_comms, 1):
                nodes_comm = [n for n, c in partition.items() if c == comm_id]
                plot_wordcloud_and_rank(
                    nodes_comm, 
                    f"Year {year} - Community {comm_id}", 
                    f"{year}_{i}", 
                    pr_dict, 
                    df_desc,
                    save=True,
                    save_path=f"output/images/wordcloud_community_{year}_{i}.png"
                )
            print(f"✓ WordClouds generated")
        except Exception as e:
            print(f"✗ Error generating wordclouds: {e}")

    # L. Store for later comparison
    comparison_results[year] = stats

# ============================================================
# FINAL COMPARISON
# ============================================================

print("\n" + "="*60)
print(" FINAL COMPARISON TABLE ")
print("="*60)
comparison_df = pd.DataFrame(comparison_results).T
print(comparison_df)
comparison_df.to_csv("output/csv/final_comparison.csv")
print("\n✓ All analysis complete! Check 'output/' folder for results.")