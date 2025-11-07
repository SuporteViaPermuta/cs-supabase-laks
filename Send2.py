import pandas as pd, os, warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings("ignore")
from datetime import datetime, timedelta

def Send2(Days):
        
    # Days = os.getenv('Days') or 0 # ) é só aquele dia

    
    """ 
    # Unidade = os.getenv('Unidade')
    ReversaUberaba = pd.read_excel("ReversaFiltered-Uberaba.xlsx")
    ReversaAraxa = pd.read_excel("ReversaFiltered-Araxa.xlsx")
    ReversaCuritiba = pd.read_excel("ReversaFiltered-Curitiba.xlsx")
    # ReversaRibeirao_Preto = pd.read_excel("ReversaFiltered-Ribeirao_Preto.xlsx")
    ReversaUberlandia = pd.read_excel("ReversaFiltered-Uberlandia.xlsx")
    # ReversaOutros = Já incluso!!
    # ReversaOutrasBases = ReversaOutrasBases.drop_duplicates()

    # dfReversa_total = pd.concat([ReversaUberaba, ReversaAraxa, ReversaCuritiba, ReversaRibeirao_Preto, ReversaUberlandia], ignore_index=True)
    dfReversa_total = pd.concat([ReversaUberaba, ReversaAraxa, ReversaCuritiba, ReversaUberlandia], ignore_index=True)

    df_total = dfReversa_total.drop_duplicates()

    # Salvar o resultado em um novo arquivo Excel
    if os.path.exists(f'ReversaFilteredTotais.xlsx'):
        os.remove(f'ReversaFilteredTotais.xlsx')
     """
    



    # Ler os arquivos CSV em vez de XLSX
    ReversaUberaba = pd.read_csv("ReversaFiltered-Uberaba.csv", sep=';', encoding='utf-8-sig')
    ReversaAraxa = pd.read_csv("ReversaFiltered-Araxa.csv", sep=';', encoding='utf-8-sig')
    ReversaCuritiba = pd.read_csv("ReversaFiltered-Curitiba.csv", sep=';', encoding='utf-8-sig')
    # ReversaRibeirao_Preto = pd.read_csv("ReversaFiltered-Ribeirao_Preto.csv", sep=';', encoding='utf-8-sig')
    ReversaUberlandia = pd.read_csv("ReversaFiltered-Uberlandia.csv", sep=';', encoding='utf-8-sig')
    # ReversaOutros = Já incluso!!
    # ReversaOutrasBases = ReversaOutrasBases.drop_duplicates()

    # Concatenar todos os DataFrames
    # dfReversa_total = pd.concat([ReversaUberaba, ReversaAraxa, ReversaCuritiba, ReversaRibeirao_Preto, ReversaUberlandia], ignore_index=True)
    dfReversa_total = pd.concat([ReversaUberaba, ReversaAraxa, ReversaCuritiba, ReversaUberlandia], ignore_index=True)

    # Remover duplicados
    df_total = dfReversa_total.drop_duplicates()

    # Se já existir o arquivo antigo, remover
    if os.path.exists('ReversaFilteredTotais.csv'):
        os.remove('ReversaFilteredTotais.csv')
    




    hoje = datetime.now() # Remove
    seis_meses_atras = hoje - timedelta(days=int(Days)+1)  # Filtra os 120 dias somente na planilha de negociações no Saldo deixa 1 ano ###(agora meio ano!!!!)

    # print(type(df_total["Data"].iloc[0]))
    
    # Formatação to datetime:
    df_total["Data"] = pd.to_datetime(df_total["Data"], errors="coerce") # Remove

    # Aplicar o filtro de data # Remove
    df_total = df_total[(df_total['Data'] >= seis_meses_atras) & (df_total['Data'] <= hoje)] # Rever a necessidade disso aqui:

    # Formatação to str: # Remove
    df_total['Data'] = df_total['Data'].apply(
        lambda x: pd.to_datetime(x, format='%d/%m/%Y', errors='coerce').strftime('%Y-%m-%d') 
        if pd.notna(x) and x != "" else '2000-01-01'
    )
        
    # df_total.to_excel("ReversaFilteredTotais.xlsx", index=False)
    # Salvar o resultado final em CSV (mesmo padrão de separador)
    df_total.to_csv('ReversaFilteredTotais.csv', index=False, sep=';', encoding='utf-8-sig')

# Send2(120)
