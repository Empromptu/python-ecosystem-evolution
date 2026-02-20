# Structural Evolution of the Python Package Ecosystem (2016–2025)

![Texto alternativo](imagen.png)

## 🎯 Research Overview
This study presents a comparative topological analysis of the **Python Package Index (PyPI) Dependency Network** across two temporal snapshots: 2016 and 2025. By modeling the ecosystem as directed graphs, we analyze how the architecture of the network reflects a global transition from web-infrastructure dominance to a data-science and automated testing paradigm.

## 👥 Authors (FCEN-UBA)
* **Carlos Sarraute**
* **Martina Rosario Pérez**
* **Juan Ignacio Catania**
* **Mateo Guerrero Schmidt**
* **Sofía Gutierrez**

*Department of Computing, Facultad de Ciencias Exactas y Naturales - Universidad de Buenos Aires*

## 📈 Comparative Network Metrics
Our analysis reveals a massive structural expansion and densification of the ecosystem over a nine-year period. Note the significant leap in the total number of nodes and the doubling of the average degree:

| Metric | 2016 Dataset | 2025 Dataset |
| :--- | :--- | :--- |
| **Total Nodes** | 25,819 | 405,872 |
| **Total Edges** | 72,189 | 2,076,516 |
| **Average Degree** | 5.59 | 10.23 |
| **Giant Weakly Connected Component** | 24,823 nodes | 399,758 nodes |
| **Modularity (Louvain)** | 0.615 | 0.489 |

## 🔍 Key Findings & Industry Evolution

### 1. The Pivot to Data Science and AI
The comparison of both networks demonstrates a fundamental shift in the ecosystem's "Industry Anchors":
* **2016 Era:** Dominated by web development and compatibility tools such as `Django`, `Six`, `Sphinx`, and `Distribute`.
* **2025 Era:** Transition toward **Data Science**, **AI**, and **Scientific Computing**, led by `NumPy`, `Pandas`, `SciPy`, and `Torch`.

### 2. Professionalization of Software Work
* **Automated Testing:** The emergence of `Pytest` as a top-centrality node in 2025 reflects the universal integration of automated testing and quality assurance into the standard developer workflow.
* **Complexity and Density:** The increase in average degree from **5.59** to **10.23** indicates that modern software packages now depend on a significantly larger number of libraries, reflecting higher architectural complexity.

### 3. Structural Dynamics
* **Connectivity:** The 2025 network exhibits a massive Weakly Connected Component of nearly **400,000 nodes**, showing that almost the entire ecosystem is reachable through dependency paths.
* **Community Boundaries:** The drop in modularity from **0.615** to **0.489** suggests that community boundaries have become more "diffuse." This is likely due to the rise of "ubiquitous" libraries that are imported across diverse functional clusters, tying previously isolated niches together.

## 🛠️ Methodology
* **Graph Construction:** Directed graphs analyzed using `NetworkX`.
* **Centrality Metrics:** Evaluation of Degree, Closeness, PageRank, and sampled Betweenness Centrality ($k=500$).
* **Community Detection:** Implementation of the **Louvain Algorithm** to detect functional clusters.
* **Textual Analysis:** Generation of WordClouds from package descriptions to identify community-specific themes.

## 📚 Bibliography
* [1] Gullikson, Kevin. (2016). *Python Dependency Analysis*.
* [2] Chugh, V. (2025). *Tutorial de pandas en Python: La guía definitiva para principiantes*. Datacamp.