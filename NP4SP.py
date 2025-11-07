"""/////////////////////////////////////          Salva BASEROW            ////////////////////////////////////////////////"""

# from PostBaserow import Get_Baserow
import pandas as pd, warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from ZZ_SQLSLD import Get_Postgres, BATCH_Create_Postgres, BATCH_Delete_Postgres, BATCH_Update_Postgres
from time import sleep

def NP4SP():
    ### Parametros Comuns:
    INDEX = "cnpj_ou_cpf" # Column ID comum para comparação entre os arquivos
    TABLEID = 626 # Arquivo BaseRow N° da Tabela
    ARQUIVOSITE = "Saldo_Associados3Totais.xlsx" # Arquivo baixado do site

    # Lê o Supabase:
    # df = Get_Postgres(TableName="z3saldo_associados", includes=['id','cnpj_ou_cpf','nome_fantasia','total_permutado','quantidade_permutada','saldo_atual','credito_disponivel','data_ultima_permuta','dias_ultima_permuta','rank_monetario','rank_recencia','ticket_anual'])
    df = Get_Postgres(TableName="z3saldo_associados", includes=['id','cnpj_ou_cpf','nome_fantasia','saldo_atual','credito_disponivel','total_compras','total_vendas', 'qtd_compras', 'qtd_vendas', 'tkt_compra', 'tkt_venda', 'data_ultima_compra','data_ultima_venda']) #'dias_ultima_permuta','rank_monetario','rank_recencia','ticket_anual'
    df.fillna('', inplace=True)

    df['saldo_atual'] = df['saldo_atual'].astype(float).map('{:.2f}'.format)
    df['credito_disponivel'] = df['credito_disponivel'].astype(float).map('{:.2f}'.format)

    df['total_compras'] = df['total_compras'].astype(float).map('{:.2f}'.format)
    df['total_vendas'] = df['total_vendas'].astype(float).map('{:.2f}'.format)

    df['tkt_compra'] = df['tkt_compra'].astype(float).map('{:.2f}'.format)
    df['tkt_venda'] = df['tkt_venda'].astype(float).map('{:.2f}'.format)

    df=df.astype(str)

    print('Saldo Ass')
    #Total lista principal
    df_SITE = pd.read_excel(ARQUIVOSITE)
    # df_SITE = df_SITE.drop(['Total Permutado Anual', 'Quantidade Permutada Anual'], axis=1)

    df_SITE.rename(columns={
        "CNPJ ou CPF": 'cnpj_ou_cpf',
        "Nome Fantasia ou Abreviacao": "nome_fantasia",
        # 'Limite Aprovado':'limite_aprovado',
        "Saldo Atual": "saldo_atual",
        "Crédito Disponível": "credito_disponivel",
        'Total Compra':'total_compras',
        'Total Venda':'total_vendas',
        # "Total Permutado": "total_permutado",
        'Qtd Compras':'qtd_compras',
        'Qtd Venda':'qtd_vendas',
        # "Quantidade Permutada": "quantidade_permutada",
        # "Data Ultima Permuta": "data_ultima_permuta",
        # "Dias Ultima Permuta": "dias_ultima_permuta",
        # "Rank Monetário": "rank_monetario",
        # "Rank Recência": "rank_recencia",
        # "Ticket Anual": "ticket_anual",
        # "LINK ASSOCIADO": "link_associado"
        "Tkt Compra": "tkt_compra",
        "Tkt Venda": "tkt_venda",
        "Data Ultima Compra": "data_ultima_compra",
        "Data Ultima Venda": "data_ultima_venda",
    }, inplace=True)



    df_SITE.fillna('', inplace=True)
    df_SITE = df_SITE.astype(str)
    df_SITE[INDEX] = df_SITE[INDEX].astype(str)

    # df_SITE['total_permutado'] = df_SITE['total_permutado'].astype(float).map('{:.2f}'.format)
    df_SITE['total_compras'] = df_SITE['total_compras'].astype(float).map('{:.2f}'.format)
    df_SITE['total_vendas'] = df_SITE['total_vendas'].astype(float).map('{:.2f}'.format)

    df_SITE['credito_disponivel'] = df_SITE['credito_disponivel'].astype(float).map('{:.2f}'.format)
    df_SITE['saldo_atual'] = df_SITE['saldo_atual'].astype(float).map('{:.2f}'.format)

    df_SITE['tkt_compra'] = df_SITE['tkt_compra'].astype(float).map('{:.2f}'.format)
    df_SITE['tkt_venda'] = df_SITE['tkt_venda'].astype(float).map('{:.2f}'.format)

    df_SITE = df_SITE.astype(str)

    # df_SITE['data_ultima_permuta'] = df_SITE['data_ultima_permuta'].apply(
    #     lambda x: '2000-01-01' if x=='' else x
    # )


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
        BATCH_Create_Postgres(TableName="z3saldo_associados",Completo=valores_to_Create)

    """ 
    # Delete
    if valores_to_Delete.__len__():
        # Encontrar (IDs) Linha valores na tabela do BaseRow:
        valores_filtrar = [item[INDEX] for item in valores_to_Delete]

        # Filtrar o DataFrame para capturar as linhas correspondentes
        DeletedLinesBaserow = df[df[INDEX].isin(valores_filtrar)]
        DeletedIds = DeletedLinesBaserow['id'].tolist()

        BATCH_Delete_Postgres(TableName="z3saldo_associados",Lista_ids=DeletedIds)

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

        # print(valores_to_Update[0])
        # resultado = next((item for item in ListaAssociadosLaks if item.get('nome_fantasia') == 'AUTO CENTER SANTOS'), None)
        # print(resultado)
        BATCH_Update_Postgres(TableName="z3saldo_associados",data_list=ListaUpdate)


# NP4SP()