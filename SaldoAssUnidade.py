import pandas as pd, os, glob, warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from Unparser import unparser
# from time import sleep

def SaldoAssUnidade(Unidade = 'Uberaba'):
    # Unidade = os.getenv('Unidade') or 'Uberaba'


    # Padrão para buscar o arquivo de download mais recente
    # pattern = 'C:\\Users\\Gabriel Oliveira\\Downloads\\Saldo Associados*.*'
    # pattern = f'{os.path.join(os.path.expanduser("~"), "Downloads")}\\Saldo Associados*.*'
    pattern = os.path.join(os.path.expanduser("~"), "Downloads", "Saldo Associados*")
    matching_files = glob.glob(pattern)

    # Filtra apenas arquivos .xls e .xlsx e ordena pela data de modificação
    matching_files = [f for f in matching_files if f.endswith(('.xls', '.xlsx'))]
    matching_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    # Se encontrou algum arquivo, tenta ler
    # ... restante do seu código que encontra o arquivo baixado

    if matching_files:
        latest_matching_file = matching_files[0]
        print(f"O arquivo mais recente que corresponde ao padrão é: {latest_matching_file}")



    # Lê o arquivo baixado como HTML e remove duplicatas
    # df_arquivobaixado = pd.read_html(latest_matching_file)[0]
    df_arquivobaixado = unparser(latest_matching_file)

    df_arquivobaixado.drop_duplicates(subset='CNPJ ou CPF', keep='last', inplace=True)

    df_arquivobaixado.rename(columns={
        'Qtd Total': 'Quantidade Permutada',
        'CrÃ©dito DisponÃ­vel': 'Crédito Disponível',
        'Crð©dito Disponð­vel': 'Crédito Disponível',
    }, inplace=True)


    # Tratamento da coluna

    # df_arquivobaixado['Limite Aprovado'] = df_arquivobaixado['Limite Aprovado'].str.replace('.', '', regex=False).str.replace(',', '', regex=False).astype(float) /100
    # df_arquivobaixado['Limite Aprovado'] = df_arquivobaixado['Limite Aprovado'].apply(lambda x: f"{float(x):.2f}")
    # n nescesario sql

    # TOTAL PERMUTADO

    df_arquivobaixado['Total Compra'] = df_arquivobaixado['Total Compra'].str.replace('.', '', regex=False).str.replace(',', '', regex=False).astype(float) /100
    df_arquivobaixado['Total Compra'] = df_arquivobaixado['Total Compra'].apply(lambda x: f"{float(x):.2f}")

    df_arquivobaixado['Total Venda'] = df_arquivobaixado['Total Venda'].str.replace('.', '', regex=False).str.replace(',', '', regex=False).astype(float) /100
    df_arquivobaixado['Total Venda'] = df_arquivobaixado['Total Venda'].apply(lambda x: f"{float(x):.2f}")

    # df_arquivobaixado['Total Permutado'] = df_arquivobaixado['Total Permutado'].str.replace('.', '', regex=False).str.replace(',', '', regex=False).astype(float) /100
    # df_arquivobaixado['Total Permutado'] = df_arquivobaixado['Total Permutado'].apply(lambda x: f"{float(x):.2f}")
    #Desnec sql

    # QTD PERMUTADA

    df_arquivobaixado['Qtd Compras'] = df_arquivobaixado['Qtd Compras'].astype(str).apply(
        lambda x: f"{int(x.replace('.', '').replace(',', '.'))}" if x != '000' else "0"
    )
    df_arquivobaixado['Qtd Venda'] = df_arquivobaixado['Qtd Venda'].astype(str).apply(
        lambda x: f"{int(x.replace('.', '').replace(',', '.'))}" if x != '000' else "0"
    )

    """ 
    df_arquivobaixado['Quantidade Permutada'] = df_arquivobaixado['Quantidade Permutada'].astype(str).apply(
        lambda x: f"{int(x.replace('.', '').replace(',', '.'))}" if x != '000' else "0"
    )
    Descn
    """

    # Tratamento da coluna
    # df_arquivobaixado['Saldo Atual'] = df_arquivobaixado['Saldo Atual'].apply(
    #     lambda x: f"{float(x.replace('.', '').replace(',', '.')):.2f}" if x != '000' else "0.00"
    # )
    df_arquivobaixado['Saldo Atual'] = df_arquivobaixado['Saldo Atual'].str.replace('.', '', regex=False).str.replace(',', '', regex=False).astype(float) /100
    df_arquivobaixado['Saldo Atual'] = df_arquivobaixado['Saldo Atual'].apply(lambda x: f"{float(x):.2f}")

    df_arquivobaixado['Crédito Disponível'] = df_arquivobaixado['Crédito Disponível'].str.replace('.', '', regex=False).str.replace(',', '', regex=False).astype(float) /100
    df_arquivobaixado['Crédito Disponível'] = df_arquivobaixado['Crédito Disponível'].apply(lambda x: f"{float(x):.2f}")


    """ 
    # df_arquivobaixado['Data Ultima Permuta'] = pd.to_datetime(df_arquivobaixado['Data Ultima Permuta'], format='%d/%m/%Y').astype(str) 
    df_arquivobaixado['Data Ultima Permuta'] = df_arquivobaixado['Data Ultima Permuta'].apply(
        lambda x: pd.to_datetime(x, format='%d/%m/%Y', errors='coerce').strftime('%Y-%m-%d') 
        if pd.notna(x) and x != "" else '2000-01-01'
    ) """
    df_arquivobaixado['Tkt Compra'] = df_arquivobaixado['Tkt Compra'].str.replace('.', '', regex=False).str.replace(',', '', regex=False).astype(float) /100
    df_arquivobaixado['Tkt Compra'] = df_arquivobaixado['Tkt Compra'].apply(lambda x: f"{float(x):.2f}")

    df_arquivobaixado['Tkt Venda'] = df_arquivobaixado['Tkt Venda'].str.replace('.', '', regex=False).str.replace(',', '', regex=False).astype(float) /100
    df_arquivobaixado['Tkt Venda'] = df_arquivobaixado['Tkt Venda'].apply(lambda x: f"{float(x):.2f}")


    df_arquivobaixado['Data Ultima Compra'] = df_arquivobaixado['Data Ultima Compra'].apply(
        lambda x: pd.to_datetime(x, format='%d/%m/%Y', errors='coerce').strftime('%Y-%m-%d') 
        if pd.notna(x) and x != "" else '2000-01-01'
    )

    # df_arquivobaixado['Data Ultima Permuta'] = pd.to_datetime(df_arquivobaixado['Data Ultima Permuta'], format='%d/%m/%Y').astype(str) 
    df_arquivobaixado['Data Ultima Venda'] = df_arquivobaixado['Data Ultima Venda'].apply(
        lambda x: pd.to_datetime(x, format='%d/%m/%Y', errors='coerce').strftime('%Y-%m-%d') 
        if pd.notna(x) and x != "" else '2000-01-01'
    )


    df_arquivobaixado[['CNPJ ou CPF', 'Nome Fantasia ou Abreviacao', 'Saldo Atual', 'Crédito Disponível', 'Total Compra', 'Total Venda', 'Qtd Compras', 'Qtd Venda', 'Tkt Compra', 'Tkt Venda', 'Data Ultima Compra', 'Data Ultima Venda' ]].to_excel(f"Saldo_Associados3-{Unidade}.xlsx", index=False)
    # df_arquivobaixado[['CNPJ ou CPF', 'Nome Fantasia ou Abreviacao', 'Total Permutado Anual', 'Quantidade Permutada Anual',]].to_excel(f"SaldoRFV/rfv-{Unidade}.xlsx", index=False)



# SaldoAssUnidade()
