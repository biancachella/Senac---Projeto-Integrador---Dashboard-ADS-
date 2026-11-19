# ==========================================
# DASHBOARD DE ANÁLISE DE FILMES
# ==========================================
# PARA RODAR O CÓDIGO DIGITE NO TERMINAL: streamlit run projeto.py
# A PLANILHA DE DADOS (MOVIES_LIMPO.XLSX) PRECISA ESTAR NA MESMA PASTA QUE O CÓDIGO

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ----------------------------
# CONFIGURAÇÃO DA PÁGINA
# ----------------------------

st.set_page_config(
    page_title="Dashboard de Filmes",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Dashboard de Análise de Filmes")

# Cores usadas nos gráficos
AZUL = "royalblue"      # orçamento
AMARELO = "#F2C230"   # nota
VERDE = "#2A9D8F"     # bilheteria
CORAL = "#E76F51"     # lucro
LARANJA = "#F28E2B"   # retorno

# ----------------------------
# CARREGAMENTO DOS DADOS
# ----------------------------

try:
    dados = pd.read_excel("movies_limpo.xlsx")

except FileNotFoundError:
    st.error("Arquivo movies_limpo.xlsx não encontrado na pasta.")
    st.stop()

except Exception as erro:
    st.error(f"Erro ao carregar arquivo: {erro}")
    st.stop()

# ----------------------------
# LIMPEZA DAS COLUNAS
# ----------------------------

dados.columns = dados.columns.str.strip()

# Converter colunas numéricas
colunas_numericas = [
    "nota", "votos", "duracao", "orcamento", "bilheteria", "lucro", "retorno"
]

for coluna in colunas_numericas:
    if coluna in dados.columns:
        dados[coluna] = pd.to_numeric(dados[coluna], errors="coerce")


# ----------------------------
# FUNÇÕES AUXILIARES
# ----------------------------

def numero(valor, casas=2):
    """Mostra o número com vírgula decimal (padrão brasileiro)."""
    return f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def barras_agrupadas(categorias, series, titulo, titulo_y, titulo_y2=None):
    """
    Gráfico de barras verticais lado a lado.
    """
    fig = go.Figure()

    qtd = len(series)
    largura = 0.8 / qtd

    for i, serie in enumerate(series):
        posicoes = [p + (i - (qtd - 1) / 2) * largura for p in range(len(categorias))]

        fig.add_trace(
            go.Bar(
                x=posicoes,
                y=serie["valores"],
                width=largura * 0.92,
                name=serie["nome"],
                marker_color=serie["cor"],
                yaxis=serie.get("eixo", "y"),
                text=serie["texto"],
                textposition="outside",
                cliponaxis=False,
                customdata=categorias,
                hovertemplate="<b>%{customdata}</b><br>" + serie["nome"] + ": %{text}<extra></extra>"
            )
        )

    maior_y = max(max(s["valores"]) for s in series if s.get("eixo", "y") == "y")

    fig.update_layout(
        title=titulo,
        barmode="overlay",
        separators=",.",
        height=560,
        margin=dict(b=140, t=100),
        legend=dict(orientation="h", y=1.12, x=0),
        xaxis=dict(
            tickmode="array",
            tickvals=list(range(len(categorias))),
            ticktext=categorias,
            tickangle=-30,
            range=[-0.6, len(categorias) - 0.4]
        ),
        yaxis=dict(title=titulo_y, range=[0, maior_y * 1.15])
    )

    if titulo_y2:
        fig.update_layout(
            yaxis2=dict(
                title=titulo_y2,
                overlaying="y",
                side="right",
                range=[0, 11],
                showgrid=False
            )
        )

    return fig


# ----------------------------
# MENU LATERAL
# ----------------------------

with st.sidebar:

    st.header("📊 Navegação")

    analise = st.radio(
        "Escolha uma seção:",
        [
            "Base de Dados",
            "Desempenho por Diretor",
            "Orçamento, Lucro e Nota",
            "Sazonalidade e Tendências",
            "Média de Avaliação por Gênero"
        ]
    )


# ==================================================
# 0. BASE DE DADOS (HOMEPAGE)
# ==================================================

if analise == "Base de Dados":
    st.subheader("📄 Base de Dados Completa")
    st.markdown("Abaixo estão os dados consolidados da planilha `movies_limpo.xlsx` carregada no sistema.")
    
    # Métricas rápidas de resumo no topo
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Filmes", len(dados))
    col2.metric("Nota Média Geral", numero(dados["nota"].mean(), 1))
    col3.metric("Orçamento Médio", f"US$ {numero(dados['orcamento'].mean() / 1e6, 1)} mi")
    col4.metric("Bilheteria Média", f"US$ {numero(dados['bilheteria'].mean() / 1e6, 1)} mi")
    
    st.divider()

    st.dataframe(dados, use_container_width=True)


# ==================================================
# 1. DESEMPENHO POR DIRETOR 
# ==================================================

elif analise == "Desempenho por Diretor":
    st.subheader("🎯 Bilheteria Total vs. Nota Média")

    res_diretor = (
        dados.groupby("diretor")
        .agg({"bilheteria": ["sum", "count"], "nota": "mean"})
        .reset_index()
    )
    res_diretor.columns = [
        "diretor",
        "bilheteria_total",
        "qtd_filmes",
        "nota_media",
    ]
    res_diretor["bilheteria_total_mi"] = res_diretor["bilheteria_total"] / 1e6

    top_bilh = set(
        res_diretor.sort_values("bilheteria_total", ascending=False)
        .head(30)["diretor"]
    )
    top_nota = set(
        res_diretor.sort_values("nota_media", ascending=False).head(30)["diretor"]
    )
    elite_diretores = top_bilh.union(top_nota)

    res_diretor["is_destaque"] = res_diretor["diretor"].isin(elite_diretores)

    fig = go.Figure()

    fundo = res_diretor[~res_diretor["is_destaque"]]
    fig.add_trace(
        go.Scatter(
            x=fundo["bilheteria_total_mi"],
            y=fundo["nota_media"],
            mode="markers",
            text=fundo["diretor"],
            marker=dict(size=6, color="gray", opacity=0.25),
            hovertemplate=(
                "<b>%{text}</b><br>Bilheteria Total: US$ %{x:.1f}"
                " mi<br>Nota: %{y:.2f}<extra></extra>"
            ),
            name="Demais",
        )
    )

    dest = res_diretor[res_diretor["is_destaque"]]
    fig.add_trace(
        go.Scatter(
            x=dest["bilheteria_total_mi"],
            y=dest["nota_media"],
            mode="markers",
            text=dest["diretor"],
            marker=dict(
                size=dest["qtd_filmes"] * 2.5 + 7,
                color=dest["nota_media"],
                colorscale=[
                    [0, CORAL],
                    [0.5, AMARELO],
                    [1, VERDE],
                ],
                showscale=True,
                colorbar=dict(title="Nota média"),
                opacity=0.95,
            ),
            hovertemplate=(
                "<b>🌟 %{text}</b><br>Bilheteria Total: US$ %{x:.1f}"
                " mi<br>Nota Média: %{y:.2f}<extra></extra>"
            ),
            name="Destaques",
        )
    )

    media_nota = res_diretor["nota_media"].mean()
    fig.add_hline(
        y=media_nota,
        line_dash="dash",
        line_color="gray",
        annotation_text="Média Geral de Nota",
        annotation_position="bottom right",
    )

    fig.update_layout(
        title="(Passe o mouse para inspecionar)",
        xaxis=dict(title="Bilheteria Total (US$ milhões)", rangemode="tozero"),
        yaxis=dict(title="Nota Média", range=[5.5, 9.6]),
        height=600,
        margin=dict(t=80, b=40, l=40, r=40),
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption("Dica: Os pontos cinzentos mostram toda a base. Os coloridos destacam os 30 principais nomes em bilheteria total e os 30 com melhores avaliações.")

    st.markdown(
        "**Conclusão da análise:** Analisando a bilheteria acumulada (total) em contraponto à nota média, "
        "reforça-se que os maiores geradores de receita comercial posicionam-se isolados no extremo direito, "
        "enquanto as produções mais bem avaliadas pelo público distribuem-se em diferentes patamares financeiros."
    )

# ==================================================
# 2. ORÇAMENTO, LUCRO E NOTA
# ==================================================

elif analise == "Orçamento, Lucro e Nota":

    # ---------- Gráfico 1: 10 maiores orçamentos ----------
    st.subheader("💰 Filmes com maiores orçamentos VS nota")

    top10 = dados.sort_values("orcamento", ascending=True).tail(10).copy()
    top10["orcamento_mi"] = top10["orcamento"] / 1e6

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=top10["nome"],
            x=top10["orcamento_mi"],
            orientation="h",
            name="Orçamento (US$ milhões)",
            marker_color=AZUL,
            opacity=0.85,
            text=[f"US$ {numero(v, 1)} mi" for v in top10["orcamento_mi"]],
            textposition="inside",
            insidetextanchor="start",
            textfont=dict(color="white", size=11),
            hoverinfo="none"
        )
    )

    fig.add_trace(
        go.Scatter(
            y=top10["nome"],
            x=top10["nota"],
            xaxis="x2",
            mode="lines+markers+text",
            name="Nota (0 a 10)",
            line=dict(color=AMARELO, width=3),
            marker=dict(size=10, color=AMARELO),
            text=[numero(v, 1) for v in top10["nota"]],
            textposition="top center",
            textfont=dict(color=AMARELO, size=11),
            hoverinfo="none"
        )
    )

    fig.update_layout(
        separators=",.",
        height=560,
        margin=dict(l=220, r=50, t=120, b=60),
        legend=dict(orientation="h", y=1.22, x=0),
        xaxis=dict(
            title="Orçamento (US$ milhões)",
            range=[0, top10["orcamento_mi"].max() * 1.15]
        ),
        xaxis2=dict(
            title="Nota",
            overlaying="x",
            side="top",
            range=[0, 11],
            tickmode="linear",
            dtick=2,
            showgrid=False
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        "**Conclusão da análise:** Observa-se que os filmes com maiores orçamentos apresentam notas "
        "bastante variadas. Isso indica que investir mais dinheiro em uma produção não garante "
        "necessariamente uma melhor avaliação do público."
    )

    st.divider()

    # ---------- Gráfico 2: 10 bem avaliados com menor lucro ----------

    st.subheader("⭐ Filmes bem avaliados com menor lucro financeiro proporcional")

    dados["razao_retorno"] = dados["lucro"] / dados["orcamento"]

    aclamados_baixo_lucro = (
        dados[dados["nota"] >= 9]
        .sort_values("razao_retorno", ascending=True)
        .head(10)
        .copy()
    )
    aclamados_baixo_lucro["orcamento_mi"] = aclamados_baixo_lucro["orcamento"] / 1e6
    aclamados_baixo_lucro["lucro_mi"] = aclamados_baixo_lucro["lucro"] / 1e6

    fig2 = go.Figure()

    # 1. Barra de Orçamento
    fig2.add_trace(
        go.Bar(
            y=aclamados_baixo_lucro["nome"],
            x=aclamados_baixo_lucro["orcamento_mi"],
            orientation="h",
            name="Orçamento (US$ mi)",
            marker_color=AZUL,
            opacity=0.85,
            text=[f"US$ {numero(v, 1)} mi" for v in aclamados_baixo_lucro["orcamento_mi"]],
            textposition="outside",
            cliponaxis=False,
            textfont=dict(color="white", size=11),
            hoverinfo="none"
        )
    )

    # 2. Barra de Lucro
    fig2.add_trace(
        go.Bar(
            y=aclamados_baixo_lucro["nome"],
            x=aclamados_baixo_lucro["lucro_mi"],
            orientation="h",
            name="Lucro (US$ mi)",
            marker_color=VERDE,
            opacity=0.85,
            text=[f"US$ {numero(v, 1)} mi" for v in aclamados_baixo_lucro["lucro_mi"]],
            textposition="outside",
            cliponaxis=False,
            textfont=dict(color="white", size=11),
            hoverinfo="none"
        )
    )

    # 3. Linha de Nota
    fig2.add_trace(
        go.Scatter(
            y=aclamados_baixo_lucro["nome"],
            x=aclamados_baixo_lucro["nota"],
            xaxis="x2",
            mode="lines+markers+text",
            name="Nota (0 a 10)",
            line=dict(color=AMARELO, width=3),
            marker=dict(size=11, color=AMARELO),
            text=[numero(v, 1) for v in aclamados_baixo_lucro["nota"]],
            textposition="top right",
            textfont=dict(color=AMARELO, size=12),
            hoverinfo="none"
        )
    )

    fig2.update_layout(
        separators=",.",
        barmode="group",
        height=700, # Gráfico mais alto para dar respiro vertical às barras duplas
        margin=dict(l=220, r=100, t=120, b=60), # Margem direita maior para acomodar o texto 'outside'
        legend=dict(orientation="h", y=1.22, x=0),
        xaxis=dict(
            title="Valores em Milhões (US$)",
            range=[0, max(aclamados_baixo_lucro["orcamento_mi"].max() * 1.3, 26)]
        ),
        xaxis2=dict(
            title="Nota",
            overlaying="x",
            side="top",
            range=[8, 10],
            tickmode="linear",
            dtick=1,
            showgrid=False
        )
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.caption("Critério: entre os filmes com nota 9,0 ou mais, os 10 com menor proporção de lucro em relação ao orçamento.")

    st.markdown(
        "**Conclusão da análise:** Filmes aclamados pela crítica e pelo público que geraram o menor "
        "lucro proporcional sobre o capital investido, reforçando que excelência artística nem sempre "
        "se traduz em margem financeira expressiva."
    )

# ==================================================
# 3. SAZONALIDADE E TENDÊNCIAS
# ==================================================

elif analise == "Sazonalidade e Tendências":

    st.subheader("📅 Bilheteria e lucro médios por mês de lançamento")

    meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    meses_extenso = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
                     "agosto", "setembro", "outubro", "novembro", "dezembro"]

    por_mes = (
        dados.groupby("mês_lancamento")
        .agg({"bilheteria": "mean", "lucro": "mean"})
        .reindex(range(1, 13))
    )

    fig = barras_agrupadas(
        categorias=meses,
        series=[
            {
                "nome": "Bilheteria média (US$ milhões)",
                "valores": (por_mes["bilheteria"] / 1e6).tolist(),
                "cor": VERDE,
                "texto": [numero(v / 1e6, 1) for v in por_mes["bilheteria"]]
            },
            {
                "nome": "Lucro médio (US$ milhões)",
                "valores": (por_mes["lucro"] / 1e6).tolist(),
                "cor": CORAL,
                "texto": [numero(v / 1e6, 1) for v in por_mes["lucro"]]
            }
        ],
        titulo=None,
        titulo_y="US$ milhões"
    )

    fig.update_layout(margin=dict(b=60, t=100))

    st.plotly_chart(fig, use_container_width=True)

    mes_top = por_mes["lucro"].idxmax()
    melhores = sorted(por_mes["lucro"].nlargest(4).index.tolist())
    nomes = [meses_extenso[m - 1] for m in melhores]
    lista_meses = ", ".join(nomes[:-1]) + " e " + nomes[-1]
    outros = por_mes.drop(index=melhores)

    st.markdown(
        f"**Conclusão da análise:** {meses_extenso[mes_top - 1]} é o mês com maior bilheteria média "
        f"(US$ {numero(por_mes.loc[mes_top, 'bilheteria'] / 1e6, 1)} mi) e maior lucro médio "
        f"(US$ {numero(por_mes.loc[mes_top, 'lucro'] / 1e6, 1)} mi). Os meses de {lista_meses} "
        "concentram os melhores resultados, formando uma temporada de blockbusters nítida na base: "
        f"nos demais meses, a bilheteria média fica em torno de US$ {numero(outros['bilheteria'].mean() / 1e6, 1)} mi "
        f"e o lucro médio em torno de US$ {numero(outros['lucro'].mean() / 1e6, 1)} mi."
    )

# ==================================================
# 4. MÉDIA DE AVALIAÇÃO PRO GÊNERO
# ==================================================

elif analise == "Média de Avaliação por Gênero":
    st.subheader("🎭 Média de Avaliação por Gênero")

    resultado = (
        dados.groupby("gênero")
        .agg(
            nota_media=("nota", "mean"),
            quantidade=("nome", "count")
        )
        .sort_values("nota_media")
    )

    min_nota = resultado["nota_media"].min()
    max_nota = resultado["nota_media"].max()

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=resultado.index,
            x=resultado["nota_media"],
            orientation="h",
            marker=dict(
                color=resultado["nota_media"],
                colorscale="Viridis",
                showscale=True,
                colorbar=dict(title="Nota")
            ),
            text=[
                f"{nota:.2f} ⭐ ({qtd} filmes)"
                for nota, qtd in zip(
                    resultado["nota_media"],
                    resultado["quantidade"]
                )
            ],
            textposition="outside",
            customdata=resultado["quantidade"],
            hovertemplate=
            "<b>%{y}</b><br>" +
            "Nota média: %{x:.2f}<br>" +
            "Quantidade de filmes: %{customdata}<extra></extra>"
        )
    )

    fig.update_layout(
        height=max(700, len(resultado) * 45),
        xaxis=dict(
            title="Nota Média",
            range=[min_nota - 0.05, max_nota + 0.05]
        ),
        yaxis=dict(
            title="Gênero"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
            "**Conclusão da Análise**: Os gêneros possuem avaliações médias muito semelhantes, sugerindo que o gênero, "
            "isoladamente, não é um fator determinante para a nota dos filmes na base analisada."
        )