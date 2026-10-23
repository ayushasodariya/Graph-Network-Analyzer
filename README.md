# Graph Network Analyzer

An interactive web application for exploring fundamental graph algorithms and understanding how they solve network problems. Built with Python and Streamlit, with graph/network processing and interactive visualizations.

<p align="center">
  <a href="https://graph-network-analyzer.onrender.com/"><strong>🚀 Try the Live App</strong></a>
</p>

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Algorithms Explained](#algorithms-explained)
  - [Dijkstra's Shortest Path](#1-dijkstras-shortest-path)
  - [Floyd–Warshall All-Pairs Shortest Paths](#2-floydwarshall-all-pairs-shortest-paths)
  - [Kruskal's Minimum Spanning Tree](#3-kruskals-minimum-spanning-tree)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Run Locally](#run-locally)
- [Deploy on Render](#deploy-on-render)
- [How to Use the App](#how-to-use-the-app)
- [Limitations and Notes](#limitations-and-notes)
- [Contributing](#contributing)
- [License](#license)

## Overview

Graph Network Analyzer is an educational tool for learning and experimenting with graph theory and network analysis. It brings common graph algorithms into an interactive web interface so users can explore paths, compare routes, and understand how a network can be connected efficiently.

A **graph** consists of vertices (also called nodes) and edges (connections between nodes). Edges may have weights, such as distance, cost, or time. Graph algorithms analyze these relationships to answer questions such as:

- What is the shortest route between two nodes?
- What are the shortest distances between every pair of nodes?
- What is the lowest-cost set of edges that connects all nodes?

## Features

- Interactive Streamlit web interface.
- Graph/network visualization.
- Dijkstra's algorithm for a shortest path between a source and destination.
- Floyd–Warshall algorithm for shortest paths between all pairs of vertices.
- Kruskal's algorithm for a minimum spanning tree.
- Visual and algorithmic exploration of weighted graph problems.

The exact controls and available options depend on the current implementation in `app.py`.

## Algorithms Explained

### 1. Dijkstra's Shortest Path

**Purpose:** Find a shortest path from one source vertex to other vertices in a weighted graph, typically used to obtain a route from a chosen start node to a destination.

**How it works:**

1. Set the source distance to `0` and all other distances to infinity.
2. Select the not-yet-finalized vertex with the smallest known distance.
3. Examine its neighboring vertices.
4. If going through the selected vertex produces a shorter distance to a neighbor, update that neighbor's distance and predecessor.
5. Continue until the relevant vertices have been processed or the destination is reached.
6. Use predecessor information to reconstruct the path, if path reconstruction is implemented by the application.

**Time complexity:** With a priority queue and adjacency-list representation, a common implementation runs in `O((V + E) log V)`. A simpler implementation may have a different complexity.

**Important limitation:** Dijkstra's algorithm assumes non-negative edge weights. It is not suitable for graphs with negative-weight edges.

**Example use cases:** Road navigation, network routing, and finding a least-cost route.

### 2. Floyd–Warshall All-Pairs Shortest Paths

**Purpose:** Compute shortest-path distances between every pair of vertices in a weighted graph.

**How it works:**

1. Initialize a distance matrix from the graph's edge weights.
2. Set each vertex's distance to itself to `0`.
3. Consider each vertex `k` as a possible intermediate vertex.
4. For every pair `(i, j)`, compare the current distance from `i` to `j` with the route from `i` to `k` and then `k` to `j`.
5. Update the matrix when the route through `k` is shorter.

The core update rule is:

`dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`

**Time complexity:** `O(V^3)`.

**Space complexity:** `O(V^2)` for the distance matrix.

**Important notes:** Floyd–Warshall can handle negative edge weights, but shortest paths are not well-defined when a reachable negative-weight cycle exists. Implementations commonly detect such a cycle when a diagonal entry becomes negative.

**Example use cases:** All-pairs route planning, analyzing distances across a small network, and comparing connectivity costs.

### 3. Kruskal's Minimum Spanning Tree

**Purpose:** Find a minimum spanning tree (MST) in a connected, undirected, weighted graph. An MST connects every vertex while minimizing the total edge weight and avoiding cycles.

**How it works:**

1. Sort all edges by ascending weight.
2. Start with each vertex in its own component.
3. Examine edges from lowest to highest weight.
4. Add an edge if it joins two different components; skip it if adding it would create a cycle.
5. Stop after selecting `V - 1` edges for a connected graph with `V` vertices.

A Disjoint Set Union (DSU), also called Union-Find, is commonly used to track connected components efficiently.

**Time complexity:** Commonly `O(E log E)`, dominated by sorting the edges.

**Important limitation:** If the graph is disconnected, the result is a minimum spanning forest rather than one spanning tree, unless the application reports the graph as disconnected.

**Example use cases:** Designing low-cost network infrastructure, connecting locations with minimal total cable length, and building efficient communication networks.

### Quick Comparison

| Algorithm | Main question | Result | Typical time complexity |
|---|---|---|---|
| Dijkstra | What is the shortest route from one source? | Single-source shortest distances and possibly a path | `O((V + E) log V)` with a priority queue |
| Floyd–Warshall | What are the shortest routes between all pairs? | All-pairs distance matrix | `O(V^3)` |
| Kruskal | How can all vertices be connected with minimum total edge weight? | Minimum spanning tree or forest | `O(E log E)` |

Here, `V` is the number of vertices and `E` is the number of edges. Actual performance depends on the implementation and graph representation.

## Technology Stack

- **Python** — application and algorithm implementation.
- **Streamlit** — interactive web interface.
- **NetworkX** — graph data structures and graph-related operations, where used.
- **Plotly** — interactive visualizations, where used.
- **Pandas** — tabular data handling, where used.

## Project Structure

```text
Graph-Network-Analyzer/
├── app.py             # Streamlit application and user interface
├── algorithms.py      # Graph algorithm implementations
├── requirements.txt   # Python dependencies
├── .gitignore         # Files Git should ignore
└── README.md          # Project documentation
```

`render.yaml` is optional. If it is added, it can store Render deployment configuration; it is not required when entering the settings manually in the Render dashboard.

## Run Locally

### Prerequisites

- Python 3.10 or newer recommended.
- Git, if cloning the repository.

### 1. Clone the repository

```bash
git clone https://github.com/ayushasodariya/Graph-Network-Analyzer.git
cd Graph-Network-Analyzer
```

### 2. Create and activate a virtual environment (recommended)

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the application

```bash
streamlit run app.py
```

Streamlit will print a local URL, commonly `http://localhost:8501`, which you can open in your browser.

## Deploy on Render

The live deployment is available at:

**https://graph-network-analyzer.onrender.com/**

To deploy your own copy:

1. Push the project to a GitHub repository.
2. In Render, choose **New + → Web Service** and connect the repository.
3. Select the `main` branch.
4. Leave **Root Directory** blank if `app.py` and `requirements.txt` are in the repository root.
5. Set the build command to:

   ```bash
   pip install -r requirements.txt
   ```

6. Set the start command to:

   ```bash
   streamlit run app.py --server.address 0.0.0.0 --server.port $PORT
   ```

7. Create the service and check the deployment logs if the build or startup fails.

A `render.yaml` file is optional when these settings are configured in the dashboard.

## How to Use the App

1. Open the [live application](https://graph-network-analyzer.onrender.com/).
2. Explore the graph shown by the app and the controls provided in its interface.
3. Select the algorithm or analysis you want to explore.
4. Provide or select the required vertices and graph inputs, according to the available controls.
5. Run the algorithm and inspect the output and visualization.
6. Compare the different algorithms: shortest-path algorithms optimize routes, while a minimum spanning tree optimizes the total weight needed to connect a network.

The exact input workflow depends on the controls currently implemented in `app.py`.

## Limitations and Notes

- Dijkstra's algorithm requires non-negative edge weights.
- Floyd–Warshall is computationally expensive on large graphs because its running time grows cubically with the number of vertices.
- Kruskal's algorithm is designed for undirected weighted graphs; disconnected input graphs produce a forest rather than a single spanning tree.
- The complexity figures in this document describe common implementations. Check `algorithms.py` for the exact data structures and implementation details used in this project.
- Keep local virtual environments (such as `.venv/`) and secret configuration files out of version control.

## Contributing

Contributions, suggestions, and bug reports are welcome. To contribute:

1. Fork the repository.
2. Create a branch for your change.
3. Make and test your changes locally.
4. Open a pull request describing the change.

For bugs, include the steps to reproduce the issue and any relevant error output. Do not include credentials, tokens, or other secrets in issues.

## License

No license has been specified in this repository documentation yet. Unless a license is added to the repository, reuse and redistribution permissions may be limited. Add a `LICENSE` file if you want to publish the project under a specific open-source license.
