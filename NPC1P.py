"""/////////////////////////////////////          Salva BASEROW            ////////////////////////////////////////////////"""

# from PostBaserow import Get_Baserow
import pandas as pd, warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from ZZ_SQLNEG import Get_Postgres, BATCH_Create_Postgres, BATCH_SoftDelete_Postgres, BATCH_Update_Postgres

def NPC1P(Days = "90"):
    ### Parametros Comuns:
    INDEX = 'orcamento' # Column ID comum para comparação entre os arquivos

    ARQUIVOSITE = "ReversaFilteredTotais.xlsx" # Arquivo baixado do site
    ARQUIVOSITE = "ReversaFilteredTotais.csv"  # Arquivo baixado do site

    # Header 1 == sem data limite;
    df = Get_Postgres(header=0, Days=Days, TableName="z2lista_negociacoes", includes=['id','orcamento','associado_comprador','associado_vendedor','franquia_comprador','franquia_vendedor','data','valor', 'situacao'])

    df.fillna('', inplace=True)
    df = df.astype(str)
    if not df.empty:
        df['valor'] = df['valor'].astype(float).map('{:.2f}'.format)


    # print('Lista de Negociacoes')
    # df_SITE = pd.read_excel(ARQUIVOSITE)
    df_SITE = pd.read_csv(ARQUIVOSITE, sep=';', encoding='utf-8-sig')


    df_SITE.rename(columns={
        "Orçamento": "orcamento",
        "Associado Comprador": "associado_comprador",
        "Associado Vendedor": "associado_vendedor",
        "Franquia Comprador": "franquia_comprador",
        "Franquia Vendedor": "franquia_vendedor",
        "Data": "data",
        "Valor": "valor",
        "Situação":"situacao",
        "Segmento Comprador": "segmento_comprador",
        "Segmento Vendedor": "segmento_vendedor",
        "Link Comprador": "link_comprador",
        "Link Vendedor": "link_vendedor"
    }, inplace=True)

    # df_SITE = df_SITE.drop(['Franquia Comprador', 'Franquia Vendedor'], axis=1)
    df_SITE.fillna('', inplace=True)

    df_SITE[INDEX] = df_SITE[INDEX].astype(str)
    df_SITE['valor'] = df_SITE['valor'].astype(float).map('{:.2f}'.format)
    df_SITE = df_SITE.astype(str)


    # print(df_SITE.iloc[0])

    # Transforma em DICT:
    ListaSupabase = df.drop(df.columns[:1], axis=1).to_dict(orient='records') #AQui
    ListaAssociadosLaks = df_SITE.to_dict(orient='records')

    # Printa Valores no DICT: Primeira Linha:
    print(ListaSupabase[0] if ListaSupabase.__len__() else 'Baserow Vazio')
    print(ListaAssociadosLaks[0] if ListaAssociadosLaks.__len__() else '')
    # sleep(5000)
    print(f'Total de Valores no BASEROW: {ListaSupabase.__len__()}')
    print(f'Total de Valores no LAKS: {ListaAssociadosLaks.__len__()}')
    print('')
    

    # Complexidade assintótica reduzida:
    if df.empty:
        valores_to_Create = list(ListaAssociadosLaks)
    else:
        # Criando conjuntos apenas com os valores de INDEX para busca eficiente
        set_supabase = {valor[INDEX] for valor in ListaSupabase}
        set_df_index = set(df[INDEX])  

        valores_to_Create = [valor for valor in ListaAssociadosLaks if valor[INDEX] not in set_supabase and valor[INDEX] not in set_df_index]

    set_df_site_index = set(df_SITE[INDEX])  

    valores_to_Update = [valor for valor in ListaSupabase if valor[INDEX] in set_df_site_index and valor not in ListaAssociadosLaks]
    valores_to_Delete = [valor for valor in ListaSupabase if valor[INDEX] not in set_df_site_index and valor not in ListaAssociadosLaks]


    print(f'Valores to Create: {valores_to_Create.__len__()}')
    print(f'Valores to Update: {valores_to_Update.__len__()}')
    print(f'Valores to Delete: {valores_to_Delete.__len__()}')

    # from time import sleep; sleep(10000)
    # from time import sleep; sleep(10000)

    # Create:
    if valores_to_Create.__len__():   
        BATCH_Create_Postgres(TableName="z2lista_negociacoes", Completo=valores_to_Create)


    """ 
    # Delete
    if valores_to_Delete.__len__():
        # Encontrar (IDs) Linha valores na tabela do BaseRow:
        valores_filtrar = [item[INDEX] for item in valores_to_Delete]

        # Filtrar o DataFrame para capturar as linhas correspondentes
        DeletedLinesBaserow = df[df[INDEX].isin(valores_filtrar)]
        DeletedIds = DeletedLinesBaserow['id'].tolist()

        BATCH_Delete_Postgres(TableName="z2lista_negociacoes", Lista_ids=DeletedIds)

    """

    # New Delete SET EXCLUIDO
    if valores_to_Delete.__len__():
        # Encontrar (IDs) Linha valores na tabela do BaseRow:
        valores_filtrar = [item[INDEX] for item in valores_to_Delete]

        # Filtrar o DataFrame para capturar as linhas correspondentes
        DeletedLinesBaserow = df[df[INDEX].isin(valores_filtrar)]
        DeletedIds = DeletedLinesBaserow['id'].tolist()

        BATCH_SoftDelete_Postgres(TableName="z2lista_negociacoes", Lista_ids=DeletedIds)








    # Update:
    if valores_to_Update.__len__():
        # Encontrar (IDs) Linha valores na tabela do BaseRow:
        valores_filtrar = [item[INDEX] for item in valores_to_Update]

        UpdatedLinesBaserow = df[df[INDEX].isin(valores_filtrar)][['id', INDEX]]
        # print(UpdatedLinesBaserow)

        ListaUpdate = [
            {
                'id': next(  # Adiciona o campo 'ID' com o valor correspondente
                    item['id'] for item in UpdatedLinesBaserow.to_dict(orient='records')
                    if item[INDEX] == valor[INDEX]
                ),
                **valor  # Inclui todas as chaves existentes no dicionário atual  
            }
            for valor in ListaAssociadosLaks if valor[INDEX] in UpdatedLinesBaserow[INDEX].tolist()
        ]

        print(ListaUpdate[0])
        # sleep(5000)

        BATCH_Update_Postgres(TableName="z2lista_negociacoes", data_list=ListaUpdate)

# NPC1P()