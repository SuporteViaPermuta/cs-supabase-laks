"""/////////////////////////////////////          Salva BASEROW            ////////////////////////////////////////////////"""

import pandas as pd, warnings, os
warnings.simplefilter(action='ignore', category=FutureWarning)
# from ggt import Get_Baserow, BATCH_Create_Baserow, BATCH_Delete_Baserow, BATCH_Update_Baserow
from ZZ_SQLASS import Get_Postgres, BATCH_Create_Postgres, BATCH_Update_Postgres
from Send5 import mudanca_nome_fantasia
# from VectorEmbedding import vectorizator
def NP4P():

    ### Parametros Comuns:
    INDEX = 'cnpj_ou_cpf' # Column ID comum para comparação entre os arquivos
    # TABLEID = 608 # Arquivo BaseRow N° da Tabela
    ARQUIVOSITE = f"AssociadosTotais.xlsx" # Arquivo baixado do site

    # Lê o BASEROW:
    # df = Get_Baserow(TableID=TABLEID, includes=['CNPJ ou CPF','Razao Social ou Nome','Nome Fantasia ou Abreviacao','Situacao','Estado','Cidade','Franquia','Segmento','CNPJ Franquia','Data de Cadastro','Produtos do Associado','Contato do Gestor','Telefone do Gestor','Email Gestor'])
    df = Get_Postgres(includes=['id','cnpj_ou_cpf','razao_social','nome_fantasia','situacao','estado','cidade','franquia','segmento','cnpj_franquia','data_de_cadastro','produtos_associados','contato_gestor','telefone_gestor','email_gestor'])
    # if not df.empty:
        # df = df[['id','nome_fantasia','cnpj_ou_cpf','razao_social','situacao','estado','cidade','franquia','segmento','cnpj_franquia','data_de_cadastro','produtos_associados','contato_gestor','telefone_gestor','email_gestor']]

    df.fillna('', inplace=True)
    df=df.astype(str)

    # print(df.iloc[0])

    df_SITE = pd.read_excel(ARQUIVOSITE)


    df_SITE.rename(columns={
        'CNPJ ou CPF': 'cnpj_ou_cpf',
        'Razao Social ou Nome':'razao_social',
        'Nome Fantasia ou Abreviacao':'nome_fantasia',
        'Situacao':'situacao',
        'Estado':'estado',
        'Cidade':'cidade',
        'Franquia':'franquia',
        'Segmento':'segmento',
        'CNPJ Franquia':'cnpj_franquia',
        'Data de Cadastro':'data_de_cadastro',
        'Produtos do Associado':'produtos_associados',
        'Contato do Gestor':'contato_gestor',
        'Telefone do Gestor':'telefone_gestor',
        'Email Gestor':'email_gestor'
    }, inplace=True)


    df_SITE.fillna('', inplace=True)
    df_SITE = df_SITE.astype(str)
    df_SITE[INDEX] = df_SITE[INDEX].astype(str)


    """ 
    # Re-Mapeamento das franquias
    """


    ListaSupabase = df.drop(df.columns[:1], axis=1).to_dict(orient='records') #AQui
    ListaAssociadosLaks = df_SITE.to_dict(orient='records')

    print(ListaSupabase[0] if ListaSupabase.__len__() else 'Baserow Vazio')
    print(ListaAssociadosLaks[0] if ListaAssociadosLaks.__len__() else '')
    print('')

    print(f'Total de Valores no BASEROW: {ListaSupabase.__len__()}')
    print(f'Total de Valores no LAKS: {ListaAssociadosLaks.__len__()}')
    print('')


    # valores_presentes = [valor for valor in ListaSupabase if valor in ListaAssociadosLaks] # Valores a serem ignorados já foram criados

    if df.empty:
        valores_to_Create = [valor for valor in ListaAssociadosLaks]
    else: 
        valores_to_Create = [valor for valor in ListaAssociadosLaks if valor not in ListaSupabase and valor[INDEX] not in df[INDEX].tolist()] # valores a serem criados
    print(f'Valores to Create: {valores_to_Create.__len__()}')

    valores_to_Update = [valor for valor in ListaSupabase if valor not in ListaAssociadosLaks and valor[INDEX] in df_SITE[INDEX].tolist()] # valores a serem Updated
    # valores_to_Delete =  [valor for valor in ListaSupabase if valor not in ListaAssociadosLaks and valor[INDEX] not in df_SITE[INDEX].tolist()] # valores a serem deletados

    print(f'Valores to Update: {valores_to_Update.__len__()}')
    # print(f'Valores to Delete: {valores_to_Delete.__len__()}')

    # Chamada de atribuição dos nomes que foram mudados: (salva dict na planilha):
    mudanca_nome_fantasia(ListaSupabase, ListaAssociadosLaks)
    # from time import sleep; sleep(10000)



    # Create:
    if valores_to_Create.__len__():
        BATCH_Create_Postgres(TableName="z1lista_associados",Completo=valores_to_Create)
        # for val in valores_to_Create:
            # vectorizator(val)



    """ 
    # Delete
    if valores_to_Delete.__len__():
        # Encontrar (IDs) Linha valores na tabela do BaseRow:
        valores_filtrar = [item[INDEX] for item in valores_to_Delete]

        # Filtrar o DataFrame para capturar as linhas correspondentes
        DeletedLinesBaserow = df[df[INDEX].isin(valores_filtrar)]
        DeletedIds = DeletedLinesBaserow['id'].tolist()

        BATCH_Delete_Postgres(Lista_ids=DeletedIds)

    """



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

        # print(ListaUpdate[0])
        # sleep(5000)


        print(valores_to_Update[0])
        resultado = next((item for item in ListaAssociadosLaks if item.get('nome_fantasia') == valores_to_Update[0].get('nome_fantasia')), None)
        print(resultado)

        BATCH_Update_Postgres(data_list=ListaUpdate)


# NP4P()