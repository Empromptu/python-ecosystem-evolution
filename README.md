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
Our analysis reveals a massive structural expansion and densification of the ecosystem over a nine-year period:

| Metric | 2016 Dataset | 2025 Dataset |
| :--- | :--- | :--- |
| **Total Nodes** | 26,234 | 295,898 |
| **Total Edges** | 72,252 | 1,606,337 |
| **Average Degree** | 5.51 | 10.86 |
| **Giant Weakly Connected Component** | 25,169 nodes | 291,204 nodes |
| **Modularity (Louvain)** | 0.538 | 0.426 |

## 🔍 Key Findings & Industry Evolution

### 1. The Pivot to Data Science and AI
The comparison of both networks demonstrates a fundamental shift in the ecosystem's "Industry Anchors":
* **2016 Era:** Dominated by web development and compatibility tools such as `Django`, `Six`, `Sphinx`, and `Distribute`.
* **2025 Era:** Transition toward **Data Science**, **AI**, and **Scientific Computing**, led by `NumPy`, `Pandas`, `SciPy`, and `Torch`.

### 2. Professionalization of Software Work
* **Automated Testing:** The emergence of `Pytest` as a top-centrality node in 2025 reflects the universal integration of automated testing and quality assurance into the standard developer workflow.
* **Complexity and Density:** The increase in average degree from 5.51 to 10.86 indicates that modern software packages now depend on a significantly larger number of libraries, reflecting higher architectural complexity.

### 3. Structural Dynamics
* **Connectivity:** While both eras feature a massive Weakly Connected Component, the 2025 network exhibits more "diffuse" community boundaries due to increased interconnection, as evidenced by the drop in modularity.
* **Structural Bridges:** Libraries such as `Requests` maintain an influential role across both eras, serving as a primary node for global visibility and communication.

## 🛠️ Methodology
* **Graph Construction:** Directed graphs analyzed using `NetworkX`.
* **Centrality Metrics:** Evaluation of Degree, Closeness, PageRank, and sampled Betweenness Centrality.
* **Community Detection:** Implementation of the **Louvain Algorithm** to detect functional clusters.
* **Textual Analysis:** Generation of WordClouds from package descriptions to identify community-specific themes.

## 📚 Bibliography
* [1] Gullikson, Kevin. (2016). *Python Dependency Analysis*.
* [2] Chugh, V. (2025). *Tutorial de pandas en Python: La guía definitiva para principiantes*. Datacamp.
