import pandas as pd, os

def Send1Unidade(Unidade='Araxa'):
    # Unidade = os.getenv('Unidade')

    # Ler o arquivo Excel
    # df = pd.read_excel(f'ReversaFiltered-{Unidade}.xlsx')
    df = pd.read_csv(f'ReversaFiltered-{Unidade}.csv', sep=';', encoding='utf-8-sig')

    # Definir as unidades negociadas
    valores_permitidos = ['URA1', 'AAX1', 'CWB2', 'RIB1', 'UDIA1']
    valores_permitidos = ['URA1', 'AAX1', 'CWB2', 'UDIA1']

    # Filtrar os dados
    NossasBases = df[
        (df['Franquia Comprador'].isin(valores_permitidos)) & 
        (df['Franquia Vendedor'].isin(valores_permitidos))
    ]

    OutrasBases = df[
        (~df['Franquia Comprador'].isin(valores_permitidos)) |  
        (~df['Franquia Vendedor'].isin(valores_permitidos))
    ]

    # Salvar OutrasBases em um Excel
    # OutrasBases.to_excel('OutrosAssociados.xlsx', index=False)

    # Criar uma lista de associados
    Lista_Outros_Associados = []

    for _, row in OutrasBases.iterrows():
        if row['Franquia Comprador'] not in valores_permitidos:
            Lista_Outros_Associados.append({
                'CNPJ ou CPF': row['Associado Comprador'],
                'Nome Fantasia ou Abreviacao': row['Associado Comprador'],
                'Franquia': 'OUTRA BASE',# row['Franquia Comprador']
                'Data de Cadastro':f'2000-01-01'
            
            })
        if row['Franquia Vendedor'] not in valores_permitidos:
            Lista_Outros_Associados.append({
                'CNPJ ou CPF': row['Associado Vendedor'],
                'Nome Fantasia ou Abreviacao': row['Associado Vendedor'],
                'Franquia':  'OUTRA BASE',# row['Franquia Vendedor']
                'Data de Cadastro':f'2000-01-01'
            })

    # Converter a lista em um DataFrame
    OutraBase = pd.DataFrame(Lista_Outros_Associados)
    OutraBase = OutraBase.drop_duplicates()

    # Salvar o DataFrame final em um Excel
    OutraBase.to_excel(f'ListAssOutrasBases-{Unidade}.xlsx', index=False)

# Send1Unidade(Unidade='Uberaba')