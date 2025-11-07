"""/////////////////////////////////////          Salva BASEROW            ////////////////////////////////////////////////"""

import pandas as pd, warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from ZZ_SQLASSNotion import Get_Notion, BATCH_Update_Notion

def NP4PNotion():

    ### Parametros Comuns:
    INDEX = 'CPF ou CNPJ' # Column ID comum para comparação entre os arquivos
    # TABLEID = 608 # Arquivo BaseRow N° da Tabela
    ARQUIVOSITE = f"AssociadosTotais.xlsx" # Arquivo baixado do site

    # Lê o Notion:
    # df = Get_Notion()
    # df = Get_Notion(includes=[ "id", "CPF ou CNPJ", "Associado", "Status", "Data de Cadastro", "Responsável"])
    df = Get_Notion(includes=[ "id", "CPF ou CNPJ", "Associado", "Status", "Data de Cadastro"])
    df.to_excel("NotionF.xlsx", index=False)
    # df = pd.read_excel("NotionF.xlsx")
    # sleep(10000)
 
    df.fillna('', inplace=True)
    df=df.astype(str)
    df['Data de Cadastro'] = df['Data de Cadastro'].str.replace(r'T.*', '', regex=True)#.replace('', '2000-01-01')
    df['Data de Cadastro'] = pd.to_datetime(df['Data de Cadastro'], format='%Y-%m-%d', errors='coerce').dt.strftime('%Y-%m-%d')
    # print(df[df['Associado'] == 'APPLE BABY'].to_dict(orient='records'))


    df_SITE = pd.read_excel(ARQUIVOSITE)

    df_SITE.rename(columns={
        'CNPJ ou CPF': 'CPF ou CNPJ',
        # 'Razao Social ou Nome':'razao_social',
        'Nome Fantasia ou Abreviacao':'Associado',
        'Situacao':'Status',
        # 'Estado':'estado',
        # 'Cidade':'cidade',
        # 'Franquia':'franquia',
        # 'Segmento':'segmento',
        # 'CNPJ Franquia':'cnpj_franquia',
        'Data de Cadastro':'Data de Cadastro',
        # 'Produtos do Associado':'produtos_associados',
        # 'Contato do Gestor':'contato_gestor',
        # 'Telefone do Gestor':'telefone_gestor',
        # 'Email Gestor':'email_gestor'
    }, inplace=True)

    # Mantém só as colunas realmente usadas (as não comentadas)
    df_SITE = df_SITE[['CPF ou CNPJ', 'Associado', 'Status', 'Data de Cadastro']]


    df_SITE.fillna('', inplace=True)
    df_SITE = df_SITE.astype(str)
    df_SITE[INDEX] = df_SITE[INDEX].astype(str)

    # Mapeamento dos status (em capslock)
    mapeamento_status = {
        'ATIVO': 'Ativo',
        'INATIVO': 'Inativo',
        'ANÁLISE': 'Em Análise',
        'BLOQUEADO': 'Bloqueado'
    }

    # Aplicar o mapeamento
    df_SITE['Status'] = df_SITE['Status'].replace(mapeamento_status)


    ListaNotion = df.drop(df.columns[:1], axis=1).to_dict(orient='records') #AQui
    # ListaNotion = df.to_dict(orient='records') #AQui
    ListaAssociadosLaks = df_SITE.to_dict(orient='records')

    print(ListaNotion[0] if ListaNotion.__len__() else 'Baserow Vazio')
    print(ListaAssociadosLaks[0] if ListaAssociadosLaks.__len__() else '')
    print('')

    print(f'Total de Valores no NOTION: {ListaNotion.__len__()}')
    print(f'Total de Valores no LAKS: {ListaAssociadosLaks.__len__()}')
    print('')



    # valores_presentes = [valor for valor in ListaNotion if valor in ListaAssociadosLaks] # Valores a serem ignorados já foram criados

    """ #####
    if df.empty:
        valores_to_Create = [valor for valor in ListaAssociadosLaks]
    else: 
        valores_to_Create = [valor for valor in ListaAssociadosLaks if valor not in ListaNotion and valor[INDEX] not in df[INDEX].tolist()] # valores a serem criados
    print(f'Valores to Create: {valores_to_Create.__len__()}')

    ######
     """
    valores_to_Update = [valor for valor in ListaNotion if valor not in ListaAssociadosLaks and valor[INDEX] in df_SITE[INDEX].tolist()] # valores a serem Updated
    # valores_to_Delete =  [valor for valor in ListaNotion if valor not in ListaAssociadosLaks and valor[INDEX] not in df_SITE[INDEX].tolist()] # valores a serem deletados

    print(f'Valores to Update: {valores_to_Update.__len__()}')
    # print(f'Valores to Delete: {valores_to_Delete.__len__()}')

    # Chamada de atribuição dos nomes que foram mudados: (salva dict na planilha):
    # mudanca_nome_fantasia(ListaNotion, ListaAssociadosLaks)
    # from time import sleep; sleep(10000)


    # from time import sleep; sleep(1000000)

    """ 
    # Create:
    if valores_to_Create.__len__():
        BATCH_Create_Notion(TableName="z1lista_associados",Completo=valores_to_Create)
        # for val in valores_to_Create:
            # vectorizator(val)

    """

    """ 
    # Delete
    if valores_to_Delete.__len__():
        # Encontrar (IDs) Linha valores na tabela do BaseRow:
        valores_filtrar = [item[INDEX] for item in valores_to_Delete]

        # Filtrar o DataFrame para capturar as linhas correspondentes
        DeletedLinesBaserow = df[df[INDEX].isin(valores_filtrar)]
        DeletedIds = DeletedLinesBaserow['id'].tolist()

        BATCH_Delete_Notion(Lista_ids=DeletedIds)

    """
    # sleep(10000)


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


        # print(valores_to_Update[0])
        resultado = next((item for item in ListaAssociadosLaks if item.get('nome_fantasia') == valores_to_Update[0].get('nome_fantasia')), None)
        print(resultado)

        BATCH_Update_Notion(data_list=ListaUpdate)


# NP4PNotion()