"""/////////////////////////////////////          Salva BASEROW            ////////////////////////////////////////////////"""

# from PostBaserow import Get_Baserow
import pandas as pd, warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from ZZ_SQLSLD import Get_Postgres, BATCH_Create_Postgres, BATCH_Delete_Postgres, BATCH_Update_Postgres
# from time import sleep

def NP4SRFV():
    ### Parametros Comuns:
    INDEX = "cnpj_ou_cpf" # Column ID comum para comparação entre os arquivos
    ARQUIVOSITE = "Saldo_Associados3Totais.xlsx" # Arquivo baixado do site

    # Lê o Supabase:
    df = Get_Postgres(TableName="z6tabela_rfv", includes=['id','cnpj_ou_cpf','nome_fantasia','total_permutado_anual', 'quantidade_permutada_anual']) #'dias_ultima_permuta','rank_monetario','rank_recencia','ticket_anual'
    df.fillna('', inplace=True)

    df['total_permutado_anual'] = df['total_permutado_anual'].astype(float).map('{:.2f}'.format)
    # df['quantidade_permutada_anual'] = df['quantidade_permutada_anual'].astype(float).map('{:.2f}'.format) # int

    df=df.astype(str)

    print('tabela rfv')
    #Total lista principal
    df_SITE = pd.read_excel(ARQUIVOSITE)
    df_SITE = df_SITE[['CNPJ ou CPF','Nome Fantasia ou Abreviacao', 'Total Permutado Anual', 'Quantidade Permutada Anual']]

    df_SITE.rename(columns={
        "CNPJ ou CPF": 'cnpj_ou_cpf',
        "Nome Fantasia ou Abreviacao": "nome_fantasia",
        "Total Permutado Anual":"total_permutado_anual",
        "Quantidade Permutada Anual":"quantidade_permutada_anual"
    }, inplace=True)

    # print(df_SITE.iloc[0])

    df_SITE.fillna('', inplace=True)
    df_SITE = df_SITE.astype(str)
    df_SITE[INDEX] = df_SITE[INDEX].astype(str)

    # df_SITE['total_permutado'] = df_SITE['total_permutado'].astype(float).map('{:.2f}'.format)
    df_SITE['total_permutado_anual'] = df_SITE['total_permutado_anual'].astype(float).map('{:.2f}'.format)
    # df_SITE['quantidade_permutada_anual'] = df_SITE['quantidade_permutada_anual'].astype(float).map('{:.2f}'.format)

    df_SITE = df_SITE.astype(str)


    ListaBaserow = df.drop(df.columns[:1], axis=1).to_dict(orient='records') #AQui
    ListaAssociadosLaks = df_SITE.to_dict(orient='records')

    print(ListaBaserow[0] if ListaBaserow.__len__() else 'Baserow Vazio')
    print(ListaAssociadosLaks[0] if ListaAssociadosLaks.__len__() else '')

    print(f'Total de Valores no BASEROW: {ListaBaserow.__len__()}')
    print(f'Total de Valores no LAKS: {ListaAssociadosLaks.__len__()}')
    print('')


    # valores_presentes = [valor for valor in ListaBaserow if valor in ListaAssociadosLaks] # Valores a serem ignorados já foram criados

    if df.empty:
        valores_to_Create = [valor for valor in ListaAssociadosLaks]
    else: 
        valores_to_Create = [valor for valor in ListaAssociadosLaks if valor not in ListaBaserow and valor[INDEX] not in df[INDEX].tolist()] # valores a serem criados
    print(f'Valores to Create: {valores_to_Create.__len__()}')

    valores_to_Update = [valor for valor in ListaBaserow if valor not in ListaAssociadosLaks and valor[INDEX] in df_SITE[INDEX].tolist()] # valores a serem Updated
    valores_to_Delete =  [valor for valor in ListaBaserow if valor not in ListaAssociadosLaks and valor[INDEX] not in df_SITE[INDEX].tolist()] # valores a serem deletados

    print(f'Valores to Update: {valores_to_Update.__len__()}')
    print(f'Valores to Delete: {valores_to_Delete.__len__()}')

    # print(valores_to_Create)

    # Create:
    if valores_to_Create.__len__():
        BATCH_Create_Postgres(TableName="z6tabela_rfv",Completo=valores_to_Create)

    # sleep(50000)
    # Delete
    if valores_to_Delete.__len__():
        # Encontrar (IDs) Linha valores na tabela do BaseRow:
        valores_filtrar = [item[INDEX] for item in valores_to_Delete]

        # Filtrar o DataFrame para capturar as linhas correspondentes
        DeletedLinesBaserow = df[df[INDEX].isin(valores_filtrar)]
        DeletedIds = DeletedLinesBaserow['id'].tolist()

        BATCH_Delete_Postgres(TableName="z6tabela_rfv",Lista_ids=DeletedIds)



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


        BATCH_Update_Postgres(TableName="z6tabela_rfv",data_list=ListaUpdate)


# NP4SRFV()