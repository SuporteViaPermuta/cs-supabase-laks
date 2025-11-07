import pandas as pd, glob, os, warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from Unparser import unparser
from datetime import datetime, timedelta
from time import sleep

def ListaNegUnidade(Unidade = "Uberaba", Days="90"):
    # Unidade = os.getenv('Unidade') or "Araxa"

    # ARQUIVO = 'ExtratoAssociado (1).xls'
    # Padrão para buscar o arquivo de download mais recente
    # pattern = 'C:\\Users\\Gabriel Oliveira\\Downloads\\ExtratoAssociado*.*'
    pattern = f'{os.path.join(os.path.expanduser("~"), "Downloads")}\\negociacoes_filtradas_*.*'
    matching_files = glob.glob(pattern)

    # Filtra apenas arquivos .xls e .xlsx e ordena pela ATUALIZAÇÃO de modificação
    matching_files = [f for f in matching_files if f.endswith(('.xls', '.xlsx'))]
    matching_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    # Se encontrou algum arquivo, tenta ler
    # ... restante do seu código que encontra o arquivo baixado

    if matching_files:
        ARQUIVO = matching_files[0]

        print(f"O arquivo mais recente que corresponde ao padrão é: {ARQUIVO}")

    """ 
    ////////////////////////////////////////////////////////////////////////////////
    """
    # df = pd.read_html(ARQUIVO, header=2)[0]  # Define a linha 3 como cabeçalho
    
    # df = unparser(ARQUIVO, header=2)
    """ 
    df = pd.concat([
            unparser(matching_files[0], header=2), 
            unparser(matching_files[1], header=2),
            unparser(matching_files[2], header=2)
        ], ignore_index=True)
     """
    
    """ Dinamic: """
    dfs = []; rge = int(int(Days)/30)
    
    for i in range(rge):  # de 0 a 121
        df_temp = unparser(matching_files[i], header=2)
        dfs.append(df_temp)

    df = pd.concat(dfs, ignore_index=True)
    
    # Remove linhas que contêm a frase "Sem registros para exportar" em qualquer coluna
    df = df[~df.apply(lambda x: x.astype(str).str.contains('Sem registros para exportar', case=False, na=False)).any(axis=1)]

    # Remove linhas que contêm a SITUAÇÃO <> Fechado
    # df = df[df["SITUAÇÃO"] == "Fechado"] # Puxar todas

    """  """
    # print(df)

    # df.drop_duplicates(subset='ORÇAM', keep='last', inplace=True)

    df.rename(columns={
        # 'ORÇAM':'eeee'
    }, inplace=True)

    # print(df.columns); sleep(100)


    # if df.empty:
    #     quit() #sai se empty

    # Remover colunas desnecessárias ou ajustar nomes
    df.columns = df.columns.str.strip()  # Remove espaços extras dos nomes das colunas
    # print(df.columns.to_list().__str__().encode("utf-8", errors="replace").decode("utf-8")); from time import sleep; sleep(10000)

    # Agrupar pelo ID do ORÇAM e unificar os dados
    df_grouped = df.groupby('ORÇAM').agg({
        'COMPRADOR': 'first',
        'FRANQUIA COMPRADORA': 'first',
        'VENDEDOR': 'first',
        'FRANQUIA VENDEDORA': 'first',
        'OFERTA': 'first',
        'ATUALIZAÇÃO': 'first',
        'VALOR': 'sum',  # Soma VALORes
        'SITUAÇÃO': 'first',
        'COMISSÃO': 'sum'
    }).reset_index()

    # print(type(df_grouped['VALOR'].iloc[0]))
    df_grouped['VALOR'] = df_grouped['VALOR'].astype(str) .replace('(N/I)','0') #.replace(regex=r'[A-Za-z]', value='0')

    # df_grouped['VALOR'] = df_grouped['VALOR'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float) / 100
    # df_grouped['VALOR Venda VP$'] = df_grouped['VALOR Venda VP$'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float) / 100
    df_grouped['VALOR'] = df_grouped['VALOR'].str.replace('.', '', regex=False).str.replace(',', '', regex=False).astype(float) / 100

    # Exclui as colunas desnecessárias
    df_grouped = df_grouped.drop(['COMISSÃO'], axis=1)

    #SORT():
    df_sorted = df_grouped.sort_values(by="ORÇAM", ascending=False)
    # df_sorted.to_excel("planilha_ordenada_reverse.xlsx", index=False)
    # print(df_sorted)



    """/////////////////////          Filtra ultimos 6 Meses              //////////////////////////////"""

    # Filtra por ATUALIZAÇÃO:
    df_sorted['ATUALIZAÇÃO'] = df_sorted['ATUALIZAÇÃO'].apply(
        lambda x: pd.to_datetime(x, format='%d/%m/%Y', errors='coerce').strftime('%Y-%m-%d') 
        if pd.notna(x) and x != "" else '2000-01-01'
    )

    # print(df_sorted['ATUALIZAÇÃO']); 

    # Converter a coluna 'ATUALIZAÇÃO' para o tipo datetime
    # df_grouped['ATUALIZAÇÃO'] = pd.to_datetime(df_grouped['ATUALIZAÇÃO'], format='%d/%m/%Y')

    # Filtrar as ATUALIZAÇÃOs de seis meses atrás até hoje
    hoje = datetime.now()
    seis_meses_atras = hoje - timedelta(days=366)  # Filtra o ano inteiro para colocar no Saldo Total Permutado e Qunatida Perm.

    # Aplicar o filtro de data
    # df_sorted = df_sorted[(df_sorted['ATUALIZAÇÃO'] >= seis_meses_atras) & (df_sorted['ATUALIZAÇÃO'] <= hoje)]
    # df_sorted = df_sorted[(df_sorted['ATUALIZAÇÃO'] >= seis_meses_atras)]

    # inverter ordem das colunas: 
    # df_sorted.to_excel("ReversaFiltered.xlsx", index=False)

    df_sorted.rename(columns={
        'ORÇAM': 'Orçamento',
        'COMPRADOR': 'Associado Comprador',
        'VENDEDOR': 'Associado Vendedor',
        'FRANQUIA COMPRADORA': 'Franquia Comprador',
        'FRANQUIA VENDEDORA': 'Franquia Vendedor',
        'ATUALIZAÇÃO': 'Data',
        'SITUAÇÃO': 'Situação',
        'VALOR': 'Valor'
    }, inplace=True)
    
    # df_sorted = df_sorted[['ORÇAM','COMPRADOR', 'VENDEDOR', 'FRANQUIA COMPRADORA', 'FRANQUIA VENDEDORA', 'ATUALIZAÇÃO', 'VALOR']]
    df_sorted = df_sorted[['Orçamento','Associado Comprador','Associado Vendedor','Franquia Comprador','Franquia Vendedor','Data','Valor', 'Situação']]
    # df_sorted = df_sorted[['Orçamento','Associado Comprador','Associado Vendedor','Franquia Comprador','Franquia Vendedor','Data','Valor']]


    mapeamento_franquias = {
        'UBERABA 1': 'URA1',
        'ARAXA': 'AAX1',
        'CURITIBA 1': 'CWB2',
        # 'RIBEIRAO PRETO 1': 'RIB1',
        'UBERLÂNDIA': 'UDIA1'
    }
    df_sorted['Franquia Comprador'] = df_sorted['Franquia Comprador'].replace(mapeamento_franquias) 
    df_sorted['Franquia Vendedor'] = df_sorted['Franquia Vendedor'].replace(mapeamento_franquias) 
    
    # df_sorted.to_excel(f"ReversaFiltered-{Unidade}.xlsx", index=False)
    df_sorted.to_csv(f"ReversaFiltered-{Unidade}.csv", index=False, sep=';', encoding='utf-8-sig')
    # print(df_sorted.iloc[0])


    '''//////////////////////           Total Negociado              ///////////////////////////////////////'''

    ff=df_sorted[['Associado Comprador', 'Associado Vendedor', 'Valor']]
    TotalNegociado = {}

    for i in range(len(ff)):
        # Extraindo os valores uma vez
        comprador = ff.iloc[i]['Associado Comprador']
        vendedor = ff.iloc[i]['Associado Vendedor']
        valor = float(ff.iloc[i]['Valor'])

        # Atualizando valor total para o comprador
        if comprador not in TotalNegociado:
            TotalNegociado[comprador] = {'Total Permutado':0, 'Quantidade Permutada':0}
        TotalNegociado[comprador]['Total Permutado'] += valor
        TotalNegociado[comprador]['Quantidade Permutada'] += 1

        # Atualizando valor total para o vendedor
        if vendedor not in TotalNegociado:
            TotalNegociado[vendedor] = {'Total Permutado':0, 'Quantidade Permutada':0}
        TotalNegociado[vendedor]['Total Permutado'] += valor
        TotalNegociado[vendedor]['Quantidade Permutada'] += 1
    
    # print(TotalNegociado)

    # Convertendo o dicionário para um DataFrame
    TotalNegDF = pd.DataFrame(list(TotalNegociado.items()), columns=['Nome Fantasia', 'Total'])

    # Extraindo os valores para novas colunas
    TotalNegDF['Total Permutado'] = TotalNegDF['Total'].apply(lambda x: x['Total Permutado'])
    TotalNegDF['Quantidade Permutada'] = TotalNegDF['Total'].apply(lambda x: x['Quantidade Permutada'])

    # Removendo a coluna original se necessário
    TotalNegDF = TotalNegDF.drop(columns=['Total'])

    # Salvando em Excel ou exportando para banco de dados
    # TotalNegDF.to_excel(f'TotalNegociado-{Unidade}.xlsx', index=False)
    TotalNegDF.to_csv(f'TotalNegociado-{Unidade}.csv', index=False, sep=';', encoding='utf-8-sig')




# ListaNegUnidade()

