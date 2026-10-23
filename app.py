import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import pandas as pd
from algorithms import dijkstra, floyd_warshall, kruskal_mst

st.set_page_config(page_title="Graph Network Analyzer", page_icon="🕸️", layout="wide")
st.title("Graph Algorithms for Network Analysis")
st.caption("Analyze communication, social, and transportation networks with Dijkstra, Floyd–Warshall, and Kruskal.")

PRESETS = {
    "Transportation network": [
        ("College", "Railway Station", 4), ("College", "Bus Stand", 2),
        ("Bus Stand", "Railway Station", 1), ("Bus Stand", "Hospital", 5),
        ("Railway Station", "Hospital", 3), ("Hospital", "Airport", 6),
        ("Railway Station", "Airport", 8), ("College", "Market", 7),
        ("Market", "Hospital", 2), ("Market", "Airport", 10)
    ],
    "Communication network": [
        ("Router A", "Router B", 4), ("Router A", "Router C", 2),
        ("Router B", "Router C", 1), ("Router B", "Router D", 5),
        ("Router C", "Router D", 8), ("Router C", "Router E", 10),
        ("Router D", "Router E", 2), ("Router D", "Router F", 6),
        ("Router E", "Router F", 3)
    ],
    "Social network": [
        ("Ayush", "Riya", 1), ("Ayush", "Darshan", 2), ("Riya", "Darshan", 1),
        ("Riya", "Mira", 3), ("Darshan", "Karan", 2), ("Mira", "Karan", 1),
        ("Karan", "Neel", 2), ("Mira", "Neel", 4)
    ],
}

if "edges" not in st.session_state:
    st.session_state.edges = PRESETS["Transportation network"].copy()
if "nodes" not in st.session_state:
    st.session_state.nodes = sorted({x for e in st.session_state.edges for x in e[:2]})

with st.sidebar:
    st.header("Network setup")
    preset = st.selectbox("Load example network", list(PRESETS))
    if st.button("Load selected network", use_container_width=True):
        st.session_state.edges = PRESETS[preset].copy()
        st.session_state.nodes = sorted({x for e in st.session_state.edges for x in e[:2]})
        st.rerun()
    st.divider()
    st.subheader("Add a connection")
    node_a = st.text_input("From node", placeholder="e.g. College")
    node_b = st.text_input("To node", placeholder="e.g. Library")
    weight = st.number_input("Weight (distance / cost / delay)", min_value=0.1, value=1.0, step=0.5)
    if st.button("Add connection", use_container_width=True):
        if not node_a.strip() or not node_b.strip():
            st.error("Enter both node names.")
        elif node_a.strip() == node_b.strip():
            st.error("A connection must link two different nodes.")
        else:
            a, b = node_a.strip(), node_b.strip()
            st.session_state.nodes = sorted(set(st.session_state.nodes + [a, b]))
            st.session_state.edges = [e for e in st.session_state.edges if set(e[:2]) != {a, b}]
            st.session_state.edges.append((a, b, float(weight)))
            st.success(f"Connection added: {a} — {b}")
    st.divider()
    if st.button("Reset to transportation example", use_container_width=True):
        st.session_state.edges = PRESETS["Transportation network"].copy()
        st.session_state.nodes = sorted({x for e in st.session_state.edges for x in e[:2]})
        st.rerun()

G = nx.Graph()
G.add_nodes_from(st.session_state.nodes)
for a, b, w in st.session_state.edges:
    G.add_edge(a, b, weight=float(w))

if G.number_of_nodes() == 0:
    st.info("Load an example network or add a connection in the sidebar.")
    st.stop()

tab1, tab2, tab3, tab4 = st.tabs(["Network overview", "Dijkstra", "Floyd–Warshall", "Kruskal MST"])

def draw_graph(graph, highlighted=None, title="Network graph"):
    highlighted = set(highlighted or [])
    pos = nx.spring_layout(graph, seed=13, weight="weight")
    edge_x, edge_y, edge_text = [], [], []
    for u, v, data in graph.edges(data=True):
        x0, y0 = pos[u]; x1, y1 = pos[v]
        edge_x += [x0, x1, None]; edge_y += [y0, y1, None]
        edge_text.append(f"{u} — {v}: {data.get('weight', 1)}")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode="lines",
        line=dict(width=1.5, color="#64748b"), hoverinfo="none", name="Connections"))
    for u, v, data in graph.edges(data=True):
        x0, y0 = pos[u]; x1, y1 = pos[v]
        is_hi = (u, v) in highlighted or (v, u) in highlighted
        fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode="lines",
            line=dict(width=4 if is_hi else 0.1, color="#f97316" if is_hi else "rgba(0,0,0,0)"),
            hoverinfo="none", showlegend=False))
        fig.add_annotation(x=(x0+x1)/2, y=(y0+y1)/2, text=str(data.get("weight", 1)),
            showarrow=False, font=dict(size=11, color="#0f172a"),
            bgcolor="white", bordercolor="#cbd5e1", borderwidth=1)
    fig.add_trace(go.Scatter(x=[pos[n][0] for n in graph.nodes()],
        y=[pos[n][1] for n in graph.nodes()], mode="markers+text",
        text=list(graph.nodes()), textposition="top center",
        marker=dict(size=24, color="#38bdf8", line=dict(width=2, color="#0f172a")),
        hovertext=[f"{n}" for n in graph.nodes()], hoverinfo="text", name="Nodes"))
    fig.update_layout(title=title, showlegend=False, height=510,
        margin=dict(l=15, r=15, t=50, b=15), plot_bgcolor="white",
        paper_bgcolor="white", xaxis=dict(visible=False), yaxis=dict(visible=False))
    return fig

with tab1:
    c1, c2, c3 = st.columns(3)
    c1.metric("Nodes (vertices)", G.number_of_nodes())
    c2.metric("Connections (edges)", G.number_of_edges())
    c3.metric("Total edge weight", f"{sum(d['weight'] for _, _, d in G.edges(data=True)):.1f}")
    st.plotly_chart(draw_graph(G), use_container_width=True)
    st.subheader("Connection list")
    st.dataframe(pd.DataFrame(
        [{"From": a, "To": b, "Weight": w} for a, b, w in st.session_state.edges]
    ), use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Dijkstra's shortest path")
    col1, col2 = st.columns(2)
    source = col1.selectbox("Starting node", list(G.nodes()), key="dsrc")
    target = col2.selectbox("Destination node", list(G.nodes()), index=min(1, len(G.nodes())-1), key="dtgt")
    if st.button("Find shortest path", key="dijkstra_btn"):
        distance, path = dijkstra(G, source, target)
        if path:
            path_edges = list(zip(path, path[1:]))
            st.success(f"Shortest path: {' → '.join(path)} | Total weight: {distance:g}")
            st.plotly_chart(draw_graph(G, path_edges, "Dijkstra: highlighted shortest path"), use_container_width=True)
        else:
            st.warning(f"No path exists between {source} and {target}.")

with tab3:
    st.subheader("Floyd–Warshall all-pairs shortest paths")
    if st.button("Calculate all-pairs distances", key="floyd_btn"):
        distances = floyd_warshall(G)
        labels = list(G.nodes())
        matrix = pd.DataFrame([[distances[a][b] for b in labels] for a in labels],
                              index=labels, columns=labels)
        matrix = matrix.replace(float("inf"), "∞")
        st.dataframe(matrix, use_container_width=True)
        st.caption("∞ indicates that no path exists between those two nodes.")

with tab4:
    st.subheader("Kruskal's minimum spanning tree")
    if st.button("Build minimum spanning tree", key="kruskal_btn"):
        mst_edges, total = kruskal_mst(G)
        if len(mst_edges) != max(0, G.number_of_nodes()-1) and G.number_of_nodes() > 1:
            st.warning("The network is disconnected. The result is a minimum spanning forest.")
        st.success(f"Minimum total connection weight: {total:g}")
        st.write("Selected connections:")
        st.dataframe(pd.DataFrame([{"From": u, "To": v, "Weight": w} for u, v, w in mst_edges]),
                     use_container_width=True, hide_index=True)
        st.plotly_chart(draw_graph(G, [(u, v) for u, v, _ in mst_edges],
                                  "Kruskal: minimum spanning tree / forest"), use_container_width=True)

st.divider()
