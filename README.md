# Dashboard de Análise de Filmes

Dashboard interativo desenvolvido em Python para analisar dados de filmes de uma base consolidada. O projeto permite visualizar informações sobre receita, orçamento, lucro, avaliações, diretores, gêneros e períodos de lançamento por meio de gráficos e tabelas.

Este projeto foi desenvolvido como parte do **Projeto Integrador do 2º semestre do curso de Análise e Desenvolvimento de Sistemas do Senac**.

## Funcionalidades

O dashboard está dividido em cinco áreas acessíveis pelo menu lateral:

- **Base de Dados:** mostra todos os registros da planilha e métricas gerais da base.
- **Desempenho por Diretor:** relaciona a bilheteria acumulada com a nota média dos diretores.
- **Orçamento, Lucro e Nota:** compara orçamento, lucro e avaliação dos filmes.
- **Sazonalidade e Tendências:** apresenta a bilheteria e o lucro médios por mês de lançamento.
- **Média de Avaliação por Gênero:** compara a nota média e a quantidade de filmes por gênero.

O sistema também inclui formatação de valores no padrão brasileiro, gráficos interativos com informações ao passar o mouse e conclusões baseadas nos dados apresentados.

## Tecnologias utilizadas

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/) para a interface web interativa
- [Pandas](https://pandas.pydata.org/) para carregamento, tratamento e agrupamento dos dados
- [Plotly](https://plotly.com/python/) para a criação dos gráficos
- [OpenPyXL](https://openpyxl.readthedocs.io/) para leitura da planilha Excel

## Estrutura da base de dados

O arquivo principal utilizado pelo dashboard é `movies_limpo.xlsx`. Ele contém 916 registros e as seguintes informações:

| Coluna | Descrição |
|---|---|
| `ID` | Identificador do filme |
| `nome` | Nome do filme |
| `lancamento` | Ano de lançamento |
| `mês_lancamento` | Número do mês de lançamento |
| `gênero` | Gênero do filme |
| `nota` | Nota média |
| `votos` | Quantidade de votos |
| `duracao` | Duração em minutos |
| `orcamento` | Orçamento em dólares |
| `bilheteria` | Bilheteria em dólares |
| `lucro` | Lucro em dólares |
| `retorno` | Indicador de retorno financeiro |
| `diretor` | Nome do diretor |

O arquivo `movies.csv` também está disponível no repositório como fonte original dos dados em formato CSV.

## Pré-requisitos

É necessário ter instalado:

- Python 3.10 ou superior
- `pip`

## Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/biancachella/Senac---Projeto-Integrador---Dashboard-ADS-.git
cd Senac---Projeto-Integrador---Dashboard-ADS-
```

### 2. Crie e ative um ambiente virtual

No Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install streamlit pandas plotly openpyxl
```

### 4. Execute o dashboard

Certifique-se de que os arquivos `app.py` e `movies_limpo.xlsx` estejam na mesma pasta e execute:

```bash
streamlit run app.py
```

Após a execução, o Streamlit abrirá o dashboard no navegador. Caso isso não aconteça automaticamente, acesse a URL mostrada no terminal, normalmente `http://localhost:8501`.

## Estrutura do projeto

```text
Senac---Projeto-Integrador---Dashboard-ADS-/
├── app.py.py
├── movies_limpo.xlsx
├── movies.csv
├── Esboço - Dashboard de Análise de Filmes.pdf
└── README.md
```

## Funcionalidades técnicas

- Limpeza dos nomes das colunas e conversão dos campos numéricos
- Tratamento de erro caso a planilha não seja encontrada
- Cálculo de médias, agrupamentos e métricas gerais
- Conversão de valores em dólares para milhões
- Formatação dos números no padrão brasileiro
- Seleção das visualizações por meio de um menu lateral

## Observações

- A planilha `movies_limpo.xlsx` é obrigatória para o funcionamento do dashboard.
- O arquivo deve permanecer na mesma pasta do script `app.py.py`.
- Os dados representam os registros disponíveis no arquivo utilizado pelo projeto e não devem ser considerados como atualização do mercado cinematográfico em tempo real.