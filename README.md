# Structural Evolution of the Python Package Ecosystem (2016–2025)

![Texto alternativo](imagen.png)

## 🎯 Research Overview
[cite_start]This study presents a comparative topological analysis of the **Python Package Index (PyPI) Dependency Network** across two temporal snapshots: 2016 and 2025[cite: 22]. [cite_start]By modeling the ecosystem as directed graphs ($G$ and $H$), we analyze how the architecture of the network reflects a global transition from web-infrastructure dominance to a data-science and automated testing paradigm[cite: 22, 229, 231].

## 👥 Authors (FCEN-UBA)
* [cite_start]**Carlos Sarraute** [cite: 5]
* [cite_start]**Martina Rosario Pérez** [cite: 5]
* [cite_start]**Juan Ignacio Catania** [cite: 5]
* [cite_start]**Mateo Guerrero Schmidt** [cite: 5]
* [cite_start]**Sofia Gutierrez** [cite: 5]

[cite_start]*Department of Computing, Facultad de Ciencias Exactas y Naturales - Universidad de Buenos Aires* [cite: 3, 4]

## 📈 Comparative Network Metrics
[cite_start]Our analysis reveals a massive structural expansion and densification of the ecosystem over a nine-year period[cite: 225]:

| Metric | 2016 Dataset ($G$) | 2025 Dataset ($H$) |
| :--- | :--- | :--- |
| **Total Nodes** | [cite_start]26,234 [cite: 43] | [cite_start]295,898 [cite: 152] |
| **Total Edges** | [cite_start]72,252 [cite: 43] | [cite_start]1,606,337 [cite: 152] |
| **Average Degree** | [cite_start]5.51 [cite: 44] | [cite_start]10.86 [cite: 153] |
| **Giant Weakly Connected Component** | [cite_start]25,169 nodes [cite: 51] | [cite_start]291,204 nodes [cite: 161] |
| **Modularity (Louvain)** | [cite_start]0.538 [cite: 125] | [cite_start]0.426 [cite: 211] |

## 🔍 Key Findings & Industry Evolution

### 1. The Pivot to Data Science and AI
[cite_start]The comparison of both networks demonstrates a fundamental shift in the ecosystem's "Industry Anchors"[cite: 25, 208]:
* [cite_start]**2016 Era:** Dominated by web development and compatibility tools such as `Django`, `Six`, `Sphinx`, and `Distribute`[cite: 120, 144].
* [cite_start]**2025 Era:** Transition toward **Data Science**, **AI**, and **Scientific Computing**, led by `NumPy`, `Pandas`, `SciPy`, and `Torch`[cite: 220, 221, 229].

### 2. Professionalization of Software Work
* [cite_start]**Automated Testing:** The emergence of `Pytest` as a top-centrality node in 2025 reflects the universal integration of automated testing and quality assurance into the standard developer workflow[cite: 197, 198, 204].
* [cite_start]**Complexity and Density:** The increase in average degree from 5.51 to 10.86 indicates that modern software packages now depend on a significantly larger number of libraries, reflecting higher architectural complexity[cite: 225, 231].

### 3. Structural Dynamics
* [cite_start]**Connectivity:** While both eras feature a massive Weakly Connected Component [cite: 52, 161][cite_start], the 2025 network exhibits more "diffuse" community boundaries due to increased interconnection, as evidenced by the drop in modularity[cite: 211, 213].
* [cite_start]**Structural Bridges:** Libraries such as `Requests` maintain an influential role across both eras, serving as a primary node for global visibility and communication[cite: 95, 169, 227].

## 🛠️ Methodology
* [cite_start]**Graph Construction:** Directed graphs analyzed using `NetworkX`[cite: 23, 43, 152].
* [cite_start]**Centrality Metrics:** Evaluation of Degree, Closeness, PageRank, and sampled Betweenness Centrality[cite: 23, 56, 164, 166].
* [cite_start]**Community Detection:** Implementation of the **Louvain Algorithm** to detect functional clusters[cite: 23, 122, 210].
* [cite_start]**Textual Analysis:** Generation of WordClouds from package descriptions to identify community-specific themes[cite: 140, 143, 219].

## 📚 Bibliography
* [1] Gullikson, Kevin. (2016). [cite_start]*Python Dependency Analysis*. [cite: 232]
* [2] Chugh, V. (2025). *Tutorial de pandas en Python: La guía definitiva para principiantes*. [cite_start]Datacamp. [cite: 233]


