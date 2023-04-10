# CriacaoFatoDimensao
# DESAFIO: Criação das tabelas Fato e dimensões do método cubo OLAP a partir da tabela MOCK_DATA.csv
 
#PASSOS

1. Análise da tabela MOCK_DATA.csv para a construção hierarquica das tabelas dimensões

2. Leitura do arquivo CSV, transformação das células NaN da coluna 'state' em 'N/A', converção da coluna 'date' em datetime formato ISO e granularização da coluna 'date' em trimestre, mês do ano, semana do ano, dia da semana e dia do mês.

3. Criação da tabela dimensão 'dim_date' excluindo as linhas duplicadas e transformação da coluna 'id_date' em categorica númerica através do método 'astype' em conjunto ao método 'cat.codes.values'

4. Criação da tabela dimensão 'dim_product', agrupamento da tabela por 'brand' e 'model' em conjunto ao método size e reset_index para contagem de repetições e transformação da coluna 'id_date' em categoria númerica através do método 'ngroup', 'astype' em conjunto ao método 'cat.codes.values'.

5. Criação da tabela dimensão 'dim_location' excluindo as linhas duplicadas, agrupamento da tabela por 'state', 'city' e 'store' na coluna 'id_location' em conjunto ao método ngroup em categoria númerica através do método 'astype' em conjunto ao método 'cat.codes.values.

6. Criação da tabela fato através do método merge, iniciando pela tabela dim_date com left join e assim sucessivamente para as outras duas tabelas dimensões e por ultimo é filtrada a tabela fato com as devidas colunas.

7. Criação dos arquivos CSV de cada tabela com separação de células por ';'.
