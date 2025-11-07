import psycopg2, pandas as pd, warnings, numpy as np, os
warnings.simplefilter(action='ignore', category=UserWarning)


db_config = {
    "dbname": "postgres",
    "user": "postgres.gumtdqwzdskbjxzijnto",
    "password": "Lipidios10$*",
    "host": "aws-0-sa-east-1.pooler.supabase.com",
    "port": "6543",  # Padrão+1 do PostgreSQL porta pública
}


def Formulador():
    query = """
    
--  Planilha Lista: 


UPDATE z1lista_associados
SET acesso = COALESCE(acesso, email_gestor),
    senha = COALESCE(senha, '123456');


--Arruma a cagada do Laks de trocar nome das franquais

--Arruma Lista
UPDATE public."z1lista_associados"
SET franquia = CASE franquia
    WHEN 'UBERABA 1' THEN 'URA1'
    WHEN 'ARAXA'  THEN 'AAX1'
    WHEN 'CURITIBA 1'  THEN 'CWB2'
    WHEN 'UBERLÂNDIA'  THEN 'UDIA1'
    ELSE franquia
END
WHERE franquia IN ('UBERABA 1', 'ARAXA', 'CURITIBA 1', 'UBERLÂNDIA');






-- Planilha Saldo: 

-- Máximos entre data ultima permuta
UPDATE z3saldo_associados
SET data_ultima_permuta = GREATEST(data_ultima_compra, data_ultima_venda);

-- Contagem de dias ultima permuta: FORMULA
UPDATE z3saldo_associados
SET dias_ultima_permuta = CURRENT_DATE - data_ultima_permuta;


-- Calcula Limite aprovado
UPDATE z3saldo_associados
SET limite_aprovado = credito_disponivel - saldo_atual;


-- Calcula total permutado
UPDATE z3saldo_associados
SET total_permutado = total_compras + total_vendas;


-- Calcula quantidade_permutada
UPDATE z3saldo_associados
SET quantidade_permutada = qtd_compras + qtd_vendas;


-- Atualiza franquia Saldo com ListaAssociados: CAMPO NOVO
UPDATE z3saldo_associados AS dest
SET 
    link_franquia = orig.franquia
FROM z1lista_associados AS orig
WHERE dest.nome_fantasia = orig.nome_fantasia and orig.franquia <> 'OUTRA BASE';



--Arruma a cagada do Laks de trocar nome das franquais

--Arruma Saldo
UPDATE public."z3saldo_associados"
SET link_franquia = CASE link_franquia
    WHEN 'UBERABA 1' THEN 'URA1'
    WHEN 'ARAXA'  THEN 'AAX1'
    WHEN 'CURITIBA 1'  THEN 'CWB2'
    WHEN 'UBERLÂNDIA'  THEN 'UDIA1'
    ELSE link_franquia
END
WHERE link_franquia IN ('UBERABA 1', 'ARAXA', 'CURITIBA 1', 'UBERLÂNDIA');


/*
UPDATE z3saldo_associados
SET rank_monetario = 
    CASE 
        WHEN total_permutado >= 170000 THEN 5
        WHEN total_permutado >= 100000 THEN 4
        WHEN total_permutado >= 50000  THEN 3
        WHEN total_permutado >= 20000  THEN 2
        WHEN total_permutado >= 10000  THEN 1
        WHEN total_permutado >= 1      THEN 1
        ELSE 0
    END;


-- Rank recencia formula if => CASE: OLD Method:
UPDATE z3saldo_associados
SET rank_recencia = 
    CASE 
        WHEN dias_ultima_permuta <= 7  THEN 5
        WHEN dias_ultima_permuta <= 14 THEN 4
        WHEN dias_ultima_permuta <= 21 THEN 3
        WHEN dias_ultima_permuta <= 28 THEN 2
        WHEN dias_ultima_permuta <= 35 THEN 1
        ELSE 0
    END;
*/


-- -- Atualiza Ranks for ListaAss a partir do Saldo

/*

UPDATE z1lista_associados AS dest
SET 
    rank_monetario = orig.rank_monetario,
    rank_recencia = orig.rank_recencia
FROM z3saldo_associados AS orig
    WHERE dest.nome_fantasia = orig.nome_fantasia; 
*/



-- Apaga os IDS mais antigos. que estiverem duplicados

/*
--verf  de seguranca:

SELECT *
FROM z1lista_associados
WHERE id NOT IN (
    SELECT MIN(id)
    FROM z1lista_associados
    GROUP BY cnpj_ou_cpf
);

--Altamente demorado:
DELETE FROM public."z2lista_negociacoes"
WHERE id NOT IN (
    SELECT MAX(id)
    FROM public."z2lista_negociacoes"
    GROUP BY orcamento
);

--Esse debaixo:

DELETE FROM public."z1lista_associados"
WHERE id NOT IN (
    SELECT MAX(id)
    FROM public."z1lista_associados"
    GROUP BY cnpj_ou_cpf
);


DELETE FROM public."z3saldo_associados"
WHERE id NOT IN (
    SELECT MAX(id)
    FROM public."z3saldo_associados"
    GROUP BY cnpj_ou_cpf
);

*/


DELETE FROM public."z1lista_associados"
WHERE id NOT IN (
    SELECT id
    FROM (
        SELECT DISTINCT ON (nome_fantasia)
            id,
            nome_fantasia,
            franquia
        FROM public."z1lista_associados"
        ORDER BY 
            nome_fantasia,
            (franquia = 'OUTRA BASE') ASC,  -- mantém quem NÃO é 'OUTRA BASE'
            id DESC                          -- se empatar, fica a mais recente
    ) AS sub
);















-- ####################### Atualiza franquia Lista neg com ListaAssociados:

--Arruma Negociações
UPDATE public."z2lista_negociacoes"
SET franquia_comprador = CASE franquia_comprador
    WHEN 'UBERABA 1' THEN 'URA1'
    WHEN 'ARAXA'  THEN 'AAX1'
    WHEN 'CURITIBA 1'  THEN 'CWB2'
    WHEN 'UBERLÂNDIA'  THEN 'UDIA1'
    ELSE ''
END
WHERE franquia_comprador IN ('UBERABA 1', 'ARAXA', 'CURITIBA 1', 'UBERLÂNDIA');

UPDATE public."z2lista_negociacoes"
SET franquia_vendedor = CASE franquia_vendedor
    WHEN 'UBERABA 1' THEN 'URA1'
    WHEN 'ARAXA'  THEN 'AAX1'
    WHEN 'CURITIBA 1'  THEN 'CWB2'
    --WHEN 'RIBEIRAO PRETO 1'  THEN 'RIB1'
    WHEN 'UBERLÂNDIA'  THEN 'UDIA1'
    ELSE ''
END
WHERE franquia_vendedor IN ('UBERABA 1', 'ARAXA', 'CURITIBA 1', 'UBERLÂNDIA');







/*
UPDATE public."z2lista_negociacoes" AS dest
SET 
    franquia_comprador = CASE 
        WHEN orig.franquia <> 'OUTRA BASE' THEN orig.franquia
        ELSE 'OUTRA BASE'
    END
FROM public."z1lista_associados" AS orig
WHERE dest.franquia_comprador = orig.nome_fantasia;


UPDATE public."z2lista_negociacoes" AS dest
SET 
    franquia_vendedor = CASE 
        WHEN orig.franquia <> 'OUTRA BASE' THEN orig.franquia
        ELSE 'OUTRA BASE'
    END
FROM public."z1lista_associados" AS orig
WHERE dest.associado_vendedor = orig.nome_fantasia;

*/

-- ######## Atualiza franquia Lista neg com ListaAssociados:
UPDATE z2lista_negociacoes AS dest
SET 
    franquia_comprador = orig.franquia
FROM z1lista_associados AS orig
WHERE dest.associado_comprador = orig.nome_fantasia and orig.franquia <> 'OUTRA BASE';


UPDATE z2lista_negociacoes AS dest
SET 
    franquia_vendedor = orig.franquia
FROM z1lista_associados AS orig
WHERE dest.associado_vendedor = orig.nome_fantasia and orig.franquia <> 'OUTRA BASE';




-- Atualiza franquia Lista neg com ListaAssociados:
UPDATE z2lista_negociacoes AS dest
SET 
    segmento_comprador = orig.segmento
FROM z1lista_associados AS orig
WHERE dest.associado_comprador = orig.nome_fantasia and orig.franquia <> 'OUTRA BASE';

UPDATE z2lista_negociacoes AS dest
SET 
    segmento_vendedor = orig.segmento
FROM z1lista_associados AS orig
WHERE dest.associado_vendedor = orig.nome_fantasia and orig.franquia <> 'OUTRA BASE';


--Atualiza gerente: ###################################

UPDATE z2lista_negociacoes AS dest
SET 
    gerente_comprador = orig.gerente
FROM z1lista_associados AS orig
WHERE dest.associado_comprador = orig.nome_fantasia and orig.franquia <> 'OUTRA BASE';

UPDATE z2lista_negociacoes AS dest
SET 
    gerente_vendedor = orig.gerente
FROM z1lista_associados AS orig
WHERE dest.associado_vendedor = orig.nome_fantasia and orig.franquia <> 'OUTRA BASE';

-- ###############################################################

UPDATE z1lista_associados 
SET 
    gerente = 'OUTRA BASE'
      WHERE franquia = 'OUTRA BASE';


"""

    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Executar o SQL
    cursor.execute(query)
    conn.commit()

    # Fechar cursor e conexão
    cursor.close()
    conn.close()

    print('Atualização concluída!')
    return

# Formulador()














def update_nome_fantasia():

    df = pd.read_excel("mudancas_nome.xlsx")

    if df.empty:
        print("Nenhum nome fantasia alterado, para ser atualizado!")
        return # quit()
        
    df['nome_antigo'] = df['nome_antigo'].replace([ 'nan', np.nan, None], '')
    df['nome_novo'] = df['nome_novo'].replace([ 'nan', np.nan, None], '')


    # Gerar dinamicamente o trecho WHEN ... THEN ...
    when_then = "\n    ".join(
        [f"WHEN '{row.nome_antigo}' THEN '{row.nome_novo}'" for _, row in df.iterrows()]
    )

    # Criar o SQL final
    sql = f"""
    UPDATE public."z2lista_negociacoes"
    SET
        associado_comprador = CASE associado_comprador
            {when_then}
            ELSE associado_comprador
        END,
        associado_vendedor = CASE associado_vendedor
            {when_then}
            ELSE associado_vendedor
        END
    WHERE
        associado_comprador IN ({', '.join([f"'{n}'" for n in df['nome_antigo']])})
        OR associado_vendedor IN ({', '.join([f"'{n}'" for n in df['nome_antigo']])});
    """

    print(sql)
    query = """
    """
    query = sql

    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Executar o SQL
    cursor.execute(query)
    conn.commit()

    # Fechar cursor e conexão
    cursor.close()
    conn.close()
    df.__len__()
    print(f'{df['nome_novo'].__len__()} Nomes atualizados')
    
    # Salvar o resultado em um novo arquivo Excel
    if os.path.exists(f'mudancas_nome.xlsx'):
        os.remove(f'mudancas_nome.xlsx')

    return

# update_nome_fantasia()