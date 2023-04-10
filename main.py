import pandas as pd

# Leitura do arquivo CSV, transformação das células NaN da coluna 'state' em 'N/A',
# converção da coluna 'date' em datetime formato ISO e granularização da coluna 'date'
# em trimestre, mês do ano, semana do ano, dia da semana e dia do mês

df = pd.read_csv(r'C:\Users\luizm\PycharmProjects\cubo_olap\data\MOCK_DATA.csv', sep=';')
df["state"].fillna("N/A", inplace=True)
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
df.loc[:, 'month'] = df['date'].dt.month
df.loc[:, 'quarter'] = df['date'].dt.quarter
df.loc[:, 'week'] = df['date'].dt.isocalendar().week
df.loc[:, 'weekday'] = df['date'].dt.weekday
df.loc[:, 'day'] = df['date'].dt.day

# Criação da tabela dimensão 'dim_date' excluindo as linhas duplicadas e transformação da coluna 'id_date'
# em categorica númerica através do método 'astype' em conjunto ao método 'cat.codes.values'

dim_date = df[['date', 'month', 'quarter', 'week', 'weekday', 'day']].copy().drop_duplicates()
dim_date['id_date'] = dim_date['date'].astype('category').cat.codes.values
dim_date = dim_date[['id_date', 'date', 'month', 'quarter', 'week', 'weekday', 'day']]

# Criação da tabela dimensão 'dim_product', agrupamento da tabela por 'brand' e 'model' em
# conjunto ao método size e reset_index para contagem de repetições e transformação da coluna 'id_date'
# em categoria númerica através do método 'ngroup', 'astype' em conjunto ao método 'cat.codes.values'

dim_product = df[['brand', 'model']].groupby(['brand', 'model']).size().reset_index(name='count')
dim_product['id_product'] = dim_product.groupby(['brand', 'model']).ngroup().astype('category').cat.codes.values

# Criação da tabela dimensão 'dim_location' excluindo as linhas duplicadas, agrupamento da tabela por 'state', 'city'
# e 'store' na coluna 'id_location' em conjunto ao método ngroup em categoria númerica através do método 'astype' em
# conjunto ao método 'cat.codes.values

dim_location = df[['state', 'city', 'store']].drop_duplicates()
dim_location['id_location'] = dim_location.groupby(['state', 'city', 'store']).ngroup()
dim_location = dim_location[['id_location', 'state', 'city', 'store']]

# Criação da tabela fato através do método merge, iniciando pela tabela dim_date com left join e assim sucessivamente
# para as outras duas tabelas dimensões e por ultimo é filtrada a tabela fato com as devidas colunas
fato = df
fato = pd.merge(df, dim_date, on=['date', 'month', 'quarter', 'week', 'weekday', 'day'], how='left')
fato = pd.merge(fato, dim_product, on=['brand', 'model'], how='left')
fato = pd.merge(fato, dim_location, on=['state', 'city', 'store'], how='left')
fato = fato[['id_date', 'id_product', 'id_location', 'value', 'qty']]

#Criação dos arquivos de cada tabela com separação de células por ';'

fato.to_csv('fato.csv', index=False, sep=';')
dim_date.to_csv('dim_date.csv', index=False, sep=';')
dim_location.to_csv('dim_location.csv', index=False, sep=';')
dim_product.to_csv('dim_product.csv', index=False, sep=';')

print(fato.info())
