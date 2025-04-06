import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Carregue seus dados MODIFICADOS (certifique-se de que este arquivo existe
# e contém as colunas 'Interpretação_Comprimento', 'Cluster_Interpretacao', etc.)
try:
    df = pd.read_csv('respostas_estudantes_modificado.csv')
except FileNotFoundError:
    print("Erro: O arquivo 'respostas_estudantes_modificado.csv' não foi encontrado.")
    print("Certifique-se de salvar seu DataFrame modificado e atualizar o nome do arquivo se necessário.")
    exit()

# Crie os gráficos

def criar_histograma(data, coluna, titulo):
    if coluna in data.columns:
        fig = go.Figure(data=[go.Histogram(x=data[coluna])])
        fig.update_layout(title=titulo)
        return fig
    else:
        print(f"A coluna '{coluna}' não foi encontrada no DataFrame.")
        return {'data': [], 'layout': {'title': {'text': f"Erro: Coluna '{coluna}' não encontrada"}}}

def criar_barras(data, coluna, titulo):
    if coluna in data.columns:
        value_counts = data[coluna].value_counts()
        fig = go.Figure(data=[go.Bar(x=value_counts.index, y=value_counts.values)])
        fig.update_layout(title=titulo)
        return fig
    else:
        print(f"A coluna '{coluna}' não foi encontrada no DataFrame.")
        return {'data': [], 'layout': {'title': {'text': f"Erro: Coluna '{coluna}' não encontrada"}}}

def criar_boxplot(data, x_col, y_col, titulo):
    if x_col in data.columns and y_col in data.columns:
        fig = go.Figure(data=[go.Box(x=data[x_col], y=data[y_col])])
        fig.update_layout(title=titulo, xaxis_title=x_col, yaxis_title=y_col)
        return fig
    else:
        print(f"Uma ou ambas as colunas ('{x_col}', '{y_col}') não foram encontradas no DataFrame.")
        return {'data': [], 'layout': {'title': {'text': f"Erro: Colunas não encontradas"}}}

def criar_heatmap_clusters(data, col1, col2, titulo):
    if col1 in data.columns and col2 in data.columns:
        cross_tab = pd.crosstab(data[col1], data[col2])
        fig = go.Figure(data=go.Heatmap(z=cross_tab.values,
                                        x=cross_tab.columns,
                                        y=cross_tab.index,
                                        colorscale='Viridis',
                                        colorbar={'title': 'Contagem'}))
        fig.update_layout(title=titulo, xaxis_title=col2, yaxis_title=col1)
        return fig
    else:
        print(f"Uma ou ambas as colunas ('{col1}', '{col2}') não foram encontradas no DataFrame.")
        return {'data': [], 'layout': {'title': {'text': f"Erro: Colunas não encontradas"}}}

# Inicialize o aplicativo Dash
app = dash.Dash(__name__)

# Defina o layout do seu dashboard
app.layout = html.Div(children=[
    html.H1(children='Dashboard de Análise das Respostas dos Estudantes'),

    html.Div(children=[
        html.Div(children=[
            dcc.Graph(
                id='histograma-comprimento-interpretacao',
                figure=criar_histograma(df, 'Interpretação_Comprimento', 'Distribuição do Comprimento da Interpretação')
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div(children=[
            dcc.Graph(
                id='barras-cluster-interpretacao',
                figure=criar_barras(df, 'Cluster_Interpretacao', 'Distribuição dos Clusters de Interpretação')
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),
    ]),

    html.Div(children=[
        html.Div(children=[
            dcc.Graph(
                id='histograma-comprimento-estrategia',
                figure=criar_histograma(df, 'Estratégia_Comprimento', 'Distribuição do Comprimento da Estratégia')
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div(children=[
            dcc.Graph(
                id='barras-cluster-estrategia',
                figure=criar_barras(df, 'Cluster_Estratégia', 'Distribuição dos Clusters de Estratégia')
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),
    ]),

    html.Div(children=[
        html.Div(children=[
            dcc.Graph(
                id='histograma-comprimento-calculo',
                figure=criar_histograma(df, 'Cálculo/Técnica_Comprimento', 'Distribuição do Comprimento do Cálculo/Técnica')
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div(children=[
            dcc.Graph(
                id='barras-cluster-calculo',
                figure=criar_barras(df, 'Cluster_Cálculo/Técnica', 'Distribuição dos Clusters de Cálculo/Técnica')
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),
    ]),

    html.Div(children=[
        html.Div(children=[
            dcc.Graph(
                id='histograma-comprimento-resposta',
                figure=criar_histograma(df, 'Resposta_Comprimento', 'Distribuição do Comprimento da Resposta')
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div(children=[
            dcc.Graph(
                id='barras-cluster-resposta',
                figure=criar_barras(df, 'Cluster_Resposta', 'Distribuição dos Clusters da Resposta')
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),
    ]),

    html.Div(children=[
        dcc.Graph(
            id='boxplot-comprimento-por-cluster-interpretacao',
            figure=criar_boxplot(df, 'Cluster_Interpretacao', 'Interpretação_Comprimento', 'Comprimento da Interpretação por Cluster')
        ),
    ]),

    html.Div(children=[
        dcc.Graph(
            id='heatmap-cluster-interpretacao-estrategia',
            figure=criar_heatmap_clusters(df, 'Cluster_Interpretacao', 'Cluster_Estratégia', 'Relação entre Cluster de Interpretação e Estratégia')
        ),
    ]),

    # Adicione mais gráficos conforme necessário
])

if __name__ == '__main__':
    app.run(debug=True)