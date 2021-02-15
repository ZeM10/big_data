import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
from dash_table import DataTable

app = dash.Dash(__name__)
server = app.server

df_un = pd.read_csv('https://raw.githubusercontent.com/ZeM10/big_data/main/uniswap.csv')
df_bn = pd.read_csv('https://raw.githubusercontent.com/ZeM10/big_data/main/binance.csv')
un_id = [f'a{i}' for i in range(df_un.shape[0])]
bn_id = [f'b{i}' for i in range(df_bn.shape[0])]
df_un['id'] = un_id
df_bn['id'] = bn_id

func_csv_un = "df_un = pd.read_csv('https://raw.githubusercontent.com/ZeM10/big_data/main/uniswap.csv')"
func_csv_bn = "df_bn = pd.read_csv('https://raw.githubusercontent.com/ZeM10/big_data/main/binance.csv')"
func_id_un = "[f'a{i}' for i in range(df_un.shape[0])], df_un['id'] = un_id"
func_id_bn = "[f'b{i}' for i in range(df_bn.shape[0])], df_un['id'] = bn_id"


project_summary = '''
The tables below were fetched, cleaned, and formatted with python automatically.\n
The only thing that is not in the raw csv file is the "ID" column. I am in the processes of learning the
best format for them so I expect them to change throughout my semester. The code used for their generation can be found
below their respective tables.\n
The code and csv files can be viewed by navigating to the link provided below,
'''

ui_summary = '''
The code that was used to generate this UI is also in the link above.\n
The UI was built with dash plotly and deployed with heroku.\n
This is a python-only project. To run the UI locally, just download the ui.py file and run the script in your favorite IDE.\n
To generate the same csv files, run bigdata-project1.py.\n
It should be noted that ui.py file does NOT require the csv files to be installed locally.\n
'''

link_base = 'http://www.coinranking.com/exchange/-zdvbieRdZ+binance/markets'
binance_links = [link_base + f'?page={i}' for i in range(2, 19)]
binance_links.insert(0, link_base)
uniswap_link = 'http://coinmarketcap.com/exchanges/uniswap-v2/'

app.layout = html.Div([
    html.Div(id='body', children=[
        html.H1('Project 1'),
        html.H5('Isaiah Morales'),
        html.Div([
            html.P(project_summary),
            html.A('https://github.com/ZeM10/big_data', href='https://github.com/ZeM10/big_data'),
            html.P(ui_summary)
        ]),
        html.H2('Table A - Uniswap Markets via CoinMarketCap'),
        html.Div(
            DataTable(
                id='tableA',
                columns=[{"name": i, "id": i} for i in df_un.columns],
                data=df_un.to_dict('records'),
                page_action='none',
                style_table={'height': '300px', 'overflowY': 'auto', 'width': '75%'}
            ),
        ),
        html.Div([
            html.H3('Generated From'),
            html.H4('Function to fetch csv:'),
            html.P(func_csv_un),
            html.H4('Functions which generated ids'),
            html.P(func_id_un)], 
            style={'height': '200px'}
        ),
        html.H2('Table B - Binance Markets via CoinRank'),
        html.Div(
                DataTable(
                id='tableB',
                columns=[{"name": i, "id": i} for i in df_bn.columns],
                data=df_bn.to_dict('records'),
                page_action='none',
                style_table={'height': '300px', 'overflowY': 'auto', 'width': '85%'}
            )
        ),
        html.Div([
            html.H3('Generated From'),
            html.H4('Function to fetch csv:'),
            html.P(func_csv_bn), 
            html.H4('Functions which generated ids'),
            html.P(func_id_bn)],
            style={'height': '200px'}
        ),
        html.H1('Links'),
        html.H3('Binance Links'),
        html.Div([
            html.A(binance_links[0], href=binance_links[0]),
            html.Br(),
            html.A(binance_links[1], href=binance_links[1]),
            html.Br(),
            html.A(binance_links[2], href=binance_links[2]),
            html.Br(),
            html.A(binance_links[3], href=binance_links[3]),
            html.Br(),
            html.A(binance_links[4], href=binance_links[4]),
            html.Br(),
            html.A(binance_links[5], href=binance_links[5]),
            html.Br(),
            html.A(binance_links[6], href=binance_links[6]),
            html.Br(),
            html.A(binance_links[7], href=binance_links[7]),
            html.Br(),
            html.A(binance_links[8], href=binance_links[8]),
            html.Br(),
            html.A(binance_links[9], href=binance_links[9]),
            html.Br(),
            html.A(binance_links[10], href=binance_links[10]),
            html.Br(),
            html.A(binance_links[11], href=binance_links[11]),
            html.Br(),
            html.A(binance_links[12], href=binance_links[12]),
            html.Br(),
            html.A(binance_links[13], href=binance_links[13]),
            html.Br(),
            html.A(binance_links[14], href=binance_links[14]),
            html.Br(),
            html.A(binance_links[15], href=binance_links[15]),
            html.Br(),
            html.A(binance_links[16], href=binance_links[16]),
            html.Br(),
            html.A(binance_links[17], href=binance_links[17]),
        ]),
        html.H3('Uniswap Links'),
        html.Div(
            html.A(uniswap_link, href=uniswap_link)
        ),
        html.Div(style={'height': '100px'})
    ]),
])
   
if __name__ == '__main__':
    app.run_server(debug=True)
    server = app.server
