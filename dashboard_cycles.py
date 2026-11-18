import pandas as pd
import networkx as nx
import plotly.graph_objects as go


def generate_anomaly_network(edges_file, scores_file):
    print("Loading data...")
    edges = pd.read_csv(edges_file)
    scores = pd.read_csv(scores_file)

    top_anomalies = scores.nlargest(50, 'coordination_score')['account_id'].tolist()


    sus_edges = edges[(edges['nameOrig'].isin(top_anomalies)) | (edges['nameDest'].isin(top_anomalies))]

    print(f"Building network with {len(sus_edges)} suspicious transactions...")
    G = nx.from_pandas_edgelist(sus_edges, 'nameOrig', 'nameDest', ['total_amount'], create_using=nx.DiGraph())

    pos = nx.spring_layout(G, seed=42)

    print("Generating interactive dashboard visual...")
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y, line=dict(width=1, color='#555'),
        hoverinfo='none', mode='lines'
    )

    node_x, node_y, hover_texts, node_colors = [], [], [], []
    for node in G.nodes():
        node_x.append(pos[node][0])
        node_y.append(pos[node][1])


        score_row = scores[scores['account_id'] == node]
        score = score_row['coordination_score'].values[0] if not score_row.empty else 0

        hover_texts.append(f"Account: {node}<br>Coord Score: {score}")
        node_colors.append(score)

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode='markers',
        hoverinfo='text', hovertext=hover_texts,
        marker=dict(
            showscale=True, colorscale='Reds', size=18,
            color=node_colors, colorbar=dict(title="Anomaly Score"),
            line=dict(width=1, color='white')
        )
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title="Anomaly Network: High-Risk Transaction Clusters",
                        showlegend=False, hovermode='closest',
                        plot_bgcolor='black', paper_bgcolor='black',
                        font=dict(color='white'),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                    ))

    fig.write_html("dashboard_anomalies.html")
    print("Saved! Open 'dashboard_anomalies.html' in your browser.")


if __name__ == "__main__":
    generate_anomaly_network("processed_transaction_edges.csv", "final_coordination_scores.csv")