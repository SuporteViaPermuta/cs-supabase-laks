import pandas as pd, os, warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def Send3():
    # Unidade = os.getenv('Unidade')
    AssociadosUberaba = pd.read_excel("AssociadosUberaba.xlsx")
    AssociadosAraxa = pd.read_excel("AssociadosAraxa.xlsx")
    AssociadosCuritiba = pd.read_excel("AssociadosCuritiba.xlsx")
    # AssociadosRibeirao_Preto = pd.read_excel("AssociadosRibeirao_Preto.xlsx")
    AssociadosUberlandia = pd.read_excel("AssociadosUberlandia.xlsx")
    
    # AssociadosOutros = pd.read_excel("AssociadosOutros.xlsx")

    # Outras Bases:
    OBUberaba = pd.read_excel("ListAssOutrasBases-Uberaba.xlsx")
    OBAraxa = pd.read_excel("ListAssOutrasBases-Araxa.xlsx")
    OBCuritiba = pd.read_excel("ListAssOutrasBases-Curitiba.xlsx")
    # OBRibeirao_Preto = pd.read_excel("ListAssOutrasBases-Ribeirao_Preto.xlsx")
    OBUberlandia = pd.read_excel("ListAssOutrasBases-Uberlandia.xlsx")

    # AssociadosOutrasBases = pd.concat([OBUberaba, OBAraxa, OBCuritiba, OBRibeirao_Preto, OBUberlandia], ignore_index=True)
    AssociadosOutrasBases = pd.concat([OBUberaba, OBAraxa, OBCuritiba, OBUberlandia], ignore_index=True)
    # AssociadosOutrasBases = AssociadosOutrasBases.drop_duplicates()

    # df_total = pd.concat([AssociadosUberaba, AssociadosAraxa, AssociadosCuritiba, AssociadosRibeirao_Preto, AssociadosUberlandia, AssociadosOutrasBases], ignore_index=True)
    df_total = pd.concat([AssociadosUberaba, AssociadosAraxa, AssociadosCuritiba, AssociadosUberlandia, AssociadosOutrasBases], ignore_index=True)

    df_total = df_total.drop_duplicates()

    """
    # Ordenar o DataFrame de forma que a "melhor" linha venha primeiro
    df_total = df_total.sort_values(
        by=['Nome Fantasia ou Abreviacao', 'Franquia', 'CNPJ ou CPF'],
        ascending=[True, True, False]
    )

    # Converter a condição (franquia == 'OUTRA BASE') em prioridade
    df_total = df_total.sort_values(
        by=['Nome Fantasia ou Abreviacao', (df_total['Franquia'] == 'OUTRA BASE'), 'CNPJ ou CPF'],
        ascending=[True, True, False]
    )

    # Dropar duplicados mantendo a melhor versão
    df_total = df_total.drop_duplicates(subset=['Nome Fantasia ou Abreviacao'], keep='first').reset_index(drop=True)
    """

    """
    # Exemplo: df_total já carregado

    # Cria uma coluna temporária de prioridade (0 para normal, 1 para 'OUTRA BASE')
    df_total['prioridade'] = (df_total['Franquia'] == 'OUTRA BASE').astype(int)

    # Ordena: primeiro pelo nome_fantasia, depois pela prioridade (quem não é OUTRA BASE vem antes)
    df_total = df_total.sort_values(by=['Nome Fantasia ou Abreviacao', 'prioridade'])

    # Remove duplicados, mantendo a primeira ocorrência (que será a de maior prioridade)
    df_total = df_total.drop_duplicates(subset=['Nome Fantasia ou Abreviacao'], keep='first')

    # Remove a coluna auxiliar
    df_total = df_total.drop(columns=['prioridade']).reset_index(drop=True)


    """ 

    # Salvar o resultado em um novo arquivo Excel
    if os.path.exists(f'AssociadosTotais.xlsx'):
        os.remove(f'AssociadosTotais.xlsx')

    # Mapeamento das franquias
    mapeamento_franquias = {
        'UBERABA 1': 'URA1',
        'ARAXA': 'AAX1',
        'CURITIBA 1': 'CWB2',
        # 'RIBEIRAO PRETO 1': 'RIB1',
        'UBERLÂNDIA': 'UDIA1'
    }
    df_total['Franquia'] = df_total['Franquia'].replace(mapeamento_franquias) 
    ''''''


    df_total.to_excel("AssociadosTotais.xlsx", index=False)

# Send3()