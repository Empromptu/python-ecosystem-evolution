import matplotlib.pyplot as plt
import re
from collections import Counter
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_top_metrics(df_metrics, metric_column, title_name, top_n=10):
    """
    Generates a horizontal bar chart for the top N nodes of a specific metric,
    following the visual style of the reference image.
    """

    topk = df_metrics.sort_values(metric_column, ascending=False).head(top_n)
    
    plt.figure(figsize=(6, 4))
    
    ax = topk.set_index("node")[metric_column].plot(kind="barh")
    ax.set_xlabel(metric_column + " (Log Scale)")
    ax.set_ylabel('') 
    ax.set_xscale("log")
    ax.tick_params(axis='y', labelsize=14)
    
    plt.tight_layout()
    output_dir = "output/images"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    save_filename = f"top_{top_n}_{metric_column}.png"
    savepath = os.path.join(output_dir, save_filename)
    
    plt.savefig(savepath)
    print(f"Graph saved in: {savepath}")
    
    plt.show()
    
def plot_wordcloud_and_rank(nodes, title, i, pagerank_dict, df_descriptions, save=False, save_path=None):
    """Generates a combined WordCloud and PageRank bar chart for a community."""
    
    # Filter descriptions for nodes in this community
    descriptions = df_descriptions[df_descriptions['name'].isin(nodes)]['summary']
    
    all_words = []
    for d in descriptions:
        if d is None or pd.isna(d): 
            continue
        words = re.split(r"[ ,.-:(){\n}]+", str(d).lower())
        all_words += list(filter(None, words))

    counts = Counter(all_words)
    stop_words = {
        'for', 'a', 'library', 'and', 'the', 'package', 'python', 'in', 'to', 
        'with', 'of', 'as', 'is', 'it', 'on', 'an', 'that', '-', 'your', 
        'which', 'you', 'by', 'into', 'or', 'from', 'module', 'this', 'simple', 'fast'
    }

    count_filtered = {k: v for k, v in counts.items() if k not in stop_words}
    
    # Get top 10 nodes by PageRank for the side bar chart
    top_nodes = sorted(nodes, key=lambda n: pagerank_dict.get(n, 0), reverse=True)[:10]
    top_values = [pagerank_dict.get(n, 0) for n in top_nodes]

    # Create WordCloud
    wordcloud = WordCloud(
        width=800, height=800,
        background_color='white',
        random_state=42
    ).generate_from_frequencies(count_filtered)

    # Plotting
    fig, ax = plt.subplots(1, 2, figsize=(16, 9), gridspec_kw={'width_ratios': [2, 1]})
    
    ax[0].imshow(wordcloud, interpolation='bilinear')
    ax[0].axis('off')
    
    ax[1].barh(top_nodes[::-1], top_values[::-1], color='teal', alpha=0.6)
    ax[1].tick_params(axis='both', labelsize=12)
    for spine in ax[1].spines.values(): 
        spine.set_visible(False)
    ax[1].get_xaxis().set_ticks([])
    
    fig.suptitle(title, size=20)
    fig.tight_layout()
    
    if save and save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"  ✓ Saved: {save_path}")
    else:
        plt.show()