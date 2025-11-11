
import pandas as pd, glob, os, warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from Unparser import unparser

def ListaAssUnidade(Unidade = "Araxa"):
    # Acesso = os.getenv('Acesso')
    # Unidade = os.getenv('Unidade')

    # Padrão para buscar o arquivo de download mais recente
    # pattern = 'C:\\Users\\Gabriel Oliveira\\Downloads\\Associados*.*'
    pattern = os.path.join(os.path.expanduser("~"), "Downloads", "Associados*")
    # print(pattern)

    matching_files = glob.glob(pattern)

    # Filtra apenas arquivos .xls e .xlsx e ordena pela data de modificação
    matching_files = [f for f in matching_files if f.endswith(('.xls', '.xlsx'))]
    matching_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    # Se encontrou algum arquivo, tenta ler
    # ... restante do seu código que encontra o arquivo baixado

    if matching_files: 
        latest_matching_file = matching_files[0]
        print(f"O arquivo mais recente que corresponde ao padrão é: {latest_matching_file}")

    # df_Associados = pd.read_html(latest_matching_file)[0]
    # print(df_Associados.iloc[0],"\n\n")
    # df_filtrado = df_Associados[df_Associados["Nome Fantasia ou Abreviacao"].str.contains("ESSENCY", na=False)]
    # print(df_filtrado.iloc[0]['Nome Fantasia ou Abreviacao'])
    df_Associados = unparser(latest_matching_file)
    # print(df_Associados.iloc[0])
    # df_filtrado = df_Associados[df_Associados["Nome Fantasia ou Abreviacao"].str.contains("ESSENCY", na=False)]
    # print(df_filtrado.iloc[0]['Nome Fantasia ou Abreviacao'])

    df_Associados['Data de Cadastro'] = df_Associados['Data de Cadastro'].apply(
        lambda x: pd.to_datetime(x, format='%d/%m/%Y', errors='coerce').strftime('%Y-%m-%d') 
        if pd.notna(x) and x != "" else ""
    )

    # df_sorted['Data'] = pd.to_datetime(df_sorted['Data'], format='%d/%m/%Y').astype(str)

    if os.path.exists(f"Associados{Unidade}.xlsx"):
        os.remove(f"Associados{Unidade}.xlsx")


    # Mapeamento das franquias
    mapeamento_franquias = {
        'UBERABA 1': 'URA1',
        'ARAXA': 'AAX1',
        'CURITIBA 1': 'CWB2',
        # 'RIBEIRAO PRETO 1': 'RIB1',
        'UBERLÂNDIA': 'UDIA1'
    }
    df_Associados['Franquia'] = df_Associados['Franquia'].replace(mapeamento_franquias) 

    df_Associados.to_excel(f"Associados{Unidade}.xlsx", index=False)




# ListaAssUnidade()
