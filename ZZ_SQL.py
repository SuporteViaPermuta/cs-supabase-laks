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


-- ANTIGO (reescrevia todas as linhas todo ciclo):
-- UPDATE z1lista_associados
-- SET acesso = COALESCE(acesso, email_gestor),
--     senha = COALESCE(senha, '123456');
-- NOVO: só toca quem realmente está nulo
UPDATE z1lista_associados
SET acesso = COALESCE(acesso, email_gestor),
    senha = COALESCE(senha, '123456')
WHERE acesso IS NULL OR senha IS NULL;


--Arruma a cagada do Laks de trocar nome das franquais

--Arruma Lista
UPDATE public."z1lista_associados"
SET franquia = CASE franquia
    WHEN 'UBERABA 1' THEN 'URA1'
    WHEN 'ARAXA'  THEN 'AAX1'
    WHEN 'CURITIBA 1'  THEN 'CWB2'
    WHEN 'UBERLÂNDIA'  THEN 'UDIA1'
    WHEN 'VIA PERMUTA FRANCA'  THEN 'FRA1'
    ELSE franquia
END
-- Franca adicionada -> linha antiga (sem Franca) comentada logo abaixo:
-- WHERE franquia IN ('UBERABA 1', 'ARAXA', 'CURITIBA 1', 'UBERLÂNDIA');
WHERE franquia IN ('UBERABA 1', 'ARAXA', 'CURITIBA 1', 'UBERLÂNDIA', 'VIA PERMUTA FRANCA');






-- Planilha Saldo: 

-- Máximos entre data ultima permuta
-- ANTIGO: UPDATE ... SET data_ultima_permuta = GREATEST(...);  (sem WHERE -> reescrevia tudo)
UPDATE z3saldo_associados
SET data_ultima_permuta = GREATEST(data_ultima_compra, data_ultima_venda)
WHERE data_ultima_permuta IS DISTINCT FROM GREATEST(data_ultima_compra, data_ultima_venda);

-- Contagem de dias ultima permuta: FORMULA
-- ANTIGO: UPDATE ... SET dias_ultima_permuta = CURRENT_DATE - data_ultima_permuta;
UPDATE z3saldo_associados
SET dias_ultima_permuta = CURRENT_DATE - data_ultima_permuta
WHERE dias_ultima_permuta IS DISTINCT FROM (CURRENT_DATE - data_ultima_permuta);


-- Calcula Limite aprovado
-- ANTIGO: UPDATE ... SET limite_aprovado = credito_disponivel - saldo_atual;
UPDATE z3saldo_associados
SET limite_aprovado = credito_disponivel - saldo_atual
WHERE limite_aprovado IS DISTINCT FROM (credito_disponivel - saldo_atual);


-- Calcula total permutado
-- ANTIGO: UPDATE ... SET total_permutado = total_compras + total_vendas;
UPDATE z3saldo_associados
SET total_permutado = total_compras + total_vendas
WHERE total_permutado IS DISTINCT FROM (total_compras + total_vendas);


-- Calcula quantidade_permutada
-- ANTIGO: UPDATE ... SET quantidade_permutada = qtd_compras + qtd_vendas;
UPDATE z3saldo_associados
SET quantidade_permutada = qtd_compras + qtd_vendas
WHERE quantidade_permutada IS DISTINCT FROM (qtd_compras + qtd_vendas);


-- Atualiza franquia Saldo com ListaAssociados: CAMPO NOVO
-- ANTIGO: sem checagem de mudança -> reescrevia todas as linhas casadas todo ciclo
UPDATE z3saldo_associados AS dest
SET
    link_franquia = orig.franquia
FROM z1lista_associados AS orig
WHERE dest.nome_fantasia = orig.nome_fantasia and orig.franquia <> 'OUTRA BASE'
  AND dest.link_franquia IS DISTINCT FROM orig.franquia;



--Arruma a cagada do Laks de trocar nome das franquais

--Arruma Saldo
UPDATE public."z3saldo_associados"
SET link_franquia = CASE link_franquia
    WHEN 'UBERABA 1' THEN 'URA1'
    WHEN 'ARAXA'  THEN 'AAX1'
    WHEN 'CURITIBA 1'  THEN 'CWB2'
    WHEN 'UBERLÂNDIA'  THEN 'UDIA1'
    WHEN 'VIA PERMUTA FRANCA'  THEN 'FRA1'
    ELSE link_franquia
END
-- Franca adicionada -> linha antiga (sem Franca) comentada logo abaixo:
-- WHERE link_franquia IN ('UBERABA 1', 'ARAXA', 'CURITIBA 1', 'UBERLÂNDIA');
WHERE link_franquia IN ('UBERABA 1', 'ARAXA', 'CURITIBA 1', 'UBERLÂNDIA', 'VIA PERMUTA FRANCA');


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


-- ANTIGO (varria a tabela inteira com NOT IN(subquery) todo ciclo):
-- DELETE FROM public."z1lista_associados"
-- WHERE id NOT IN (
--     SELECT id
--     FROM (
--         SELECT DISTINCT ON (nome_fantasia)
--             id, nome_fantasia, franquia
--         FROM public."z1lista_associados"
--         ORDER BY nome_fantasia, (franquia = 'OUTRA BASE') ASC, id DESC
--     ) AS sub
-- );
-- NOVO: só apaga a linha que PERDE p/ outra do mesmo nome_fantasia (mantém não-'OUTRA BASE',
-- desempate = maior id). Linha única nunca casa o EXISTS -> nenhuma escrita quando não há duplicata.
DELETE FROM public."z1lista_associados" a
WHERE EXISTS (
    SELECT 1
    FROM public."z1lista_associados" b
    WHERE b.nome_fantasia = a.nome_fantasia
      AND b.id <> a.id
      AND (
            ( (COALESCE(a.franquia,'') = 'OUTRA BASE') AND (COALESCE(b.franquia,'') <> 'OUTRA BASE') )
         OR ( (COALESCE(a.franquia,'') = 'OUTRA BASE') = (COALESCE(b.franquia,'') = 'OUTRA BASE') AND b.id > a.id )
      )
);















-- ####################### Atualiza franquia Lista neg com ListaAssociados:

--Arruma Negociações
UPDATE public."z2lista_negociacoes"
SET franquia_comprador = CASE franquia_comprador
    WHEN 'UBERABA 1' THEN 'URA1'
    WHEN 'ARAXA'  THEN 'AAX1'
    WHEN 'CURITIBA 1'  THEN 'CWB2'
    WHEN 'UBERLÂNDIA'  THEN 'UDIA1'
    WHEN 'VIA PERMUTA FRANCA'  THEN 'FRA1'
    ELSE ''
END
-- Franca adicionada -> linha antiga (sem Franca) comentada logo abaixo:
-- WHERE franquia_comprador IN ('UBERABA 1', 'ARAXA', 'CURITIBA 1', 'UBERLÂNDIA');
WHERE franquia_comprador IN ('UBERABA 1', 'ARAXA', 'CURITIBA 1', 'UBERLÂNDIA', 'VIA PERMUTA FRANCA');

UPDATE public."z2lista_negociacoes"
SET franquia_vendedor = CASE franquia_vendedor
    WHEN 'UBERABA 1' THEN 'URA1'
    WHEN 'ARAXA'  THEN 'AAX1'
    WHEN 'CURITIBA 1'  THEN 'CWB2'
    --WHEN 'RIBEIRAO PRETO 1'  THEN 'RIB1'
    WHEN 'UBERLÂNDIA'  THEN 'UDIA1'
    WHEN 'VIA PERMUTA FRANCA'  THEN 'FRA1'
    ELSE ''
END
-- Franca adicionada -> linha antiga (sem Franca) comentada logo abaixo:
-- WHERE franquia_vendedor IN ('UBERABA 1', 'ARAXA', 'CURITIBA 1', 'UBERLÂNDIA');
WHERE franquia_vendedor IN ('UBERABA 1', 'ARAXA', 'CURITIBA 1', 'UBERLÂNDIA', 'VIA PERMUTA FRANCA');







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
-- ANTIGO: sem "IS DISTINCT FROM" -> reescrevia as ~164 mil linhas casadas todo ciclo
UPDATE z2lista_negociacoes AS dest
SET
    franquia_comprador = orig.franquia
FROM z1lista_associados AS orig
WHERE dest.associado_comprador = orig.nome_fantasia and orig.franquia <> 'OUTRA BASE'
  AND dest.franquia_comprador IS DISTINCT FROM orig.franquia;


UPDATE z2lista_negociacoes AS dest
SET
    franquia_vendedor = orig.franquia
FROM z1lista_associados AS orig
WHERE dest.associado_vendedor = orig.nome_fantasia and orig.franquia <> 'OUTRA BASE'
  AND dest.franquia_vendedor IS DISTINCT FROM orig.franquia;




-- Atualiza franquia Lista neg com ListaAssociados:
-- ANTIGO: sem "IS DISTINCT FROM" -> reescrevia as ~164 mil linhas casadas todo ciclo
UPDATE z2lista_negociacoes AS dest
SET
    segmento_comprador = orig.segmento
FROM z1lista_associados AS orig
WHERE dest.associado_comprador = orig.nome_fantasia and orig.franquia <> 'OUTRA BASE'
  AND dest.segmento_comprador IS DISTINCT FROM orig.segmento;

UPDATE z2lista_negociacoes AS dest
SET
    segmento_vendedor = orig.segmento
FROM z1lista_associados AS orig
WHERE dest.associado_vendedor = orig.nome_fantasia and orig.franquia <> 'OUTRA BASE'
  AND dest.segmento_vendedor IS DISTINCT FROM orig.segmento;


--Atualiza gerente: ###################################

-- ANTIGO: sem "IS DISTINCT FROM" -> reescrevia as ~164 mil linhas casadas todo ciclo
UPDATE z2lista_negociacoes AS dest
SET
    gerente_comprador = orig.gerente
FROM z1lista_associados AS orig
WHERE dest.associado_comprador = orig.nome_fantasia and orig.franquia <> 'OUTRA BASE'
  AND dest.gerente_comprador IS DISTINCT FROM orig.gerente;

UPDATE z2lista_negociacoes AS dest
SET
    gerente_vendedor = orig.gerente
FROM z1lista_associados AS orig
WHERE dest.associado_vendedor = orig.nome_fantasia and orig.franquia <> 'OUTRA BASE'
  AND dest.gerente_vendedor IS DISTINCT FROM orig.gerente;

-- ###############################################################

-- ANTIGO: reescrevia todas as linhas 'OUTRA BASE' mesmo já estando 'OUTRA BASE'
UPDATE z1lista_associados
SET
    gerente = 'OUTRA BASE'
WHERE franquia = 'OUTRA BASE'
  AND gerente IS DISTINCT FROM 'OUTRA BASE';


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
    # Formulador2();
    return
















def update_nome_fantasia():

    df = pd.read_excel("mudancas_nome.xlsx")

    if df.empty:
        print("Nenhum nome fantasia alterado, para ser atualizado!")
        return # quit()
        
    df['nome_antigo'] = df['nome_antigo'].replace([ 'nan', np.nan, None], '')
    df['nome_novo'] = df['nome_novo'].replace([ 'nan', np.nan, None], '')


    # Escapa aspas simples p/ não quebrar o literal SQL (ex: "ESPAÇO D'ALMA")
    def _q(v):
        return str(v).replace("'", "''")

    # Gerar dinamicamente o trecho WHEN ... THEN ...
    # --- ANTIGO (comentado p/ time dev): não escapava aspas -> syntax error
    #     em nomes com apóstrofo (ESPAÇO D'ALMA, ANA CLÁUDIA D'AMICO) ---
    # when_then = "\n    ".join(
    #     [f"WHEN '{row.nome_antigo}' THEN '{row.nome_novo}'" for _, row in df.iterrows()]
    # )
    when_then = "\n    ".join(
        [f"WHEN '{_q(row.nome_antigo)}' THEN '{_q(row.nome_novo)}'" for _, row in df.iterrows()]
    )

    # Criar o SQL final
    # --- ANTIGO (comentado p/ time dev): IN(...) sem escapar aspas ---
    # sql = f"""
    # UPDATE public."z2lista_negociacoes"
    # SET
    #     associado_comprador = CASE associado_comprador
    #         {when_then}
    #         ELSE associado_comprador
    #     END,
    #     associado_vendedor = CASE associado_vendedor
    #         {when_then}
    #         ELSE associado_vendedor
    #     END
    # WHERE
    #     associado_comprador IN ({', '.join([f"'{n}'" for n in df['nome_antigo']])})
    #     OR associado_vendedor IN ({', '.join([f"'{n}'" for n in df['nome_antigo']])});
    # """
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
        associado_comprador IN ({', '.join([f"'{_q(n)}'" for n in df['nome_antigo']])})
        OR associado_vendedor IN ({', '.join([f"'{_q(n)}'" for n in df['nome_antigo']])});
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
    print(f"{df['nome_novo'].__len__()} Nomes atualizados")
    
    # Salvar o resultado em um novo arquivo Excel
    if os.path.exists(f'mudancas_nome.xlsx'):
        os.remove(f'mudancas_nome.xlsx')

    return

# update_nome_fantasia()



def Formuladore():
    Formulador()
    query = """

-- BEFOORE: ULTIMO AJUSTE DA ULTIMA PARTE:

-- OFFICIAL: LIMPA EXCLUIDOS ERRADOS & DUPLICADOS->(RECRIADOS)
-- ANTIGO (materializava ROW_NUMBER da tabela inteira -> 164k varridas todo ciclo):
--  WITH ranked AS (
--     SELECT id, orcamento, situacao,
--         ROW_NUMBER() OVER (PARTITION BY orcamento
--             ORDER BY (CASE WHEN situacao != 'excluido' THEN 1 ELSE 0 END) DESC, id DESC) AS rn
--     FROM public."z2lista_negociacoes"
-- )
-- DELETE FROM public."z2lista_negociacoes" WHERE id IN (SELECT id FROM ranked WHERE rn > 1);
-- NOVO: só apaga a linha que PERDE p/ outra do mesmo orcamento (mantém não-'excluido',
-- desempate = maior id). Usa índice ix_z2_orcamento; linha única nunca casa o EXISTS.
DELETE FROM public."z2lista_negociacoes" a
WHERE EXISTS (
    SELECT 1
    FROM public."z2lista_negociacoes" b
    WHERE b.orcamento = a.orcamento
      AND b.id <> a.id
      AND (
            ( (COALESCE(a.situacao,'') = 'excluido') AND (COALESCE(b.situacao,'') <> 'excluido') )
         OR ( (COALESCE(a.situacao,'') = 'excluido') = (COALESCE(b.situacao,'') = 'excluido') AND b.id > a.id )
      )
);

-- 111111111






-- ANTIGO (item 4): recriava a VIEW a cada execução (745+ vezes) sem necessidade.
-- Além disso a definição antiga usava OR no JOIN -> Nested Loop com ~86 milhões de
-- linhas descartadas + disco temporário (~23s por ciclo).
-- DROP VIEW IF EXISTS vw_saldo_ultimo_ano;
-- CREATE OR REPLACE VIEW public.vw_saldo_ultimo_ano AS
-- SELECT s.cnpj_ou_cpf, s.nome_fantasia,
--     COALESCE(ROUND(SUM(n.valor)::numeric, 2), 0)::numeric(10,2) AS total_permutado
-- FROM z3saldo_associados s
-- LEFT JOIN z2lista_negociacoes n
--     ON n.data >= (CURRENT_DATE - INTERVAL '1 year') AND n.data <= CURRENT_DATE
--     AND ( n.associado_comprador = s.nome_fantasia OR n.associado_vendedor = s.nome_fantasia )
-- GROUP BY s.cnpj_ou_cpf, s.nome_fantasia;
--
-- NOVO (rode UMA vez como migration; a view NÃO deve ser recriada a cada ciclo):
-- reescrita com UNION ALL pré-agregado -> Hash Aggregate + Hash Join, ~66ms (350x mais rápido).
-- Comprovado por EXPLAIN ANALYZE: some o Nested Loop, as 86M linhas e o disco temporário.
-- CREATE OR REPLACE VIEW public.vw_saldo_ultimo_ano AS
-- WITH neg AS (
--     SELECT nome, SUM(valor) AS total
--     FROM (
--         SELECT associado_comprador AS nome, valor FROM z2lista_negociacoes
--           WHERE data >= (CURRENT_DATE - INTERVAL '1 year') AND data <= CURRENT_DATE
--         UNION ALL
--         SELECT associado_vendedor AS nome, valor FROM z2lista_negociacoes
--           WHERE data >= (CURRENT_DATE - INTERVAL '1 year') AND data <= CURRENT_DATE
--     ) x
--     GROUP BY nome
-- )
-- SELECT s.cnpj_ou_cpf, s.nome_fantasia,
--        COALESCE(ROUND(neg.total::numeric, 2), 0)::numeric(10,2) AS total_permutado
-- FROM z3saldo_associados s
-- LEFT JOIN neg ON neg.nome = s.nome_fantasia;

-----------------------------------------------------------

/* ALTER TABLE z3saldo_associados
ADD COLUMN permutado_por_ano double precision;  */

/* UPDATE z3saldo_associados s
SET permutado_por_ano = COALESCE((
    SELECT SUM(n.valor)
    FROM z2lista_negociacoes n
    WHERE n.data >= (CURRENT_DATE - INTERVAL '1 year')
      AND n.data <= CURRENT_DATE
      AND (
            n.associado_comprador = s.nome_fantasia
         OR n.associado_vendedor = s.nome_fantasia
      )
), 0); */


--coloca na view depois -> atualiza da view na tabela de saldo
--Atualiza da View:

/* ALTER TABLE z3saldo_associados
ADD COLUMN vw_permutado_por_ano double precision;  */

UPDATE z3saldo_associados s
SET vw_permutado_por_ano = v.total_permutado
FROM vw_saldo_ultimo_ano v
WHERE s.cnpj_ou_cpf = v.cnpj_ou_cpf
  AND s.vw_permutado_por_ano IS DISTINCT FROM v.total_permutado;


------------------------------------------------------------------------

--Rank Monetário top5

WITH top5 AS (
    SELECT 
        s.link_franquia,
        s.cnpj_ou_cpf,
        s.vw_permutado_por_ano,
        ROW_NUMBER() OVER (PARTITION BY s.link_franquia ORDER BY s.vw_permutado_por_ano DESC) AS rn
    FROM z3saldo_associados s
),
max_by_top5 AS (
    SELECT 
        link_franquia,
        vw_permutado_por_ano AS max_valor_top5
    FROM top5
    WHERE rn = 5  -- pega o 5º maior valor
),
rank_calc AS (
    SELECT 
        s.id,
        s.link_franquia,
        s.vw_permutado_por_ano,
        COALESCE(m.max_valor_top5, 0) AS max_valor_top5,
        CASE
            WHEN s.vw_permutado_por_ano IS NULL OR s.vw_permutado_por_ano = 0 THEN 0
            WHEN m.max_valor_top5 = 0 THEN 0 
            WHEN s.vw_permutado_por_ano <= m.max_valor_top5 * 0.05 THEN 0
            WHEN s.vw_permutado_por_ano <= m.max_valor_top5 * 0.20 THEN 1
            WHEN s.vw_permutado_por_ano <= m.max_valor_top5 * 0.40 THEN 2
            WHEN s.vw_permutado_por_ano <= m.max_valor_top5 * 0.60 THEN 3
            WHEN s.vw_permutado_por_ano <= m.max_valor_top5 * 0.80 THEN 4
            ELSE 5
        END AS novo_rank
    FROM z3saldo_associados s
    LEFT JOIN max_by_top5 m 
        ON m.link_franquia = s.link_franquia
)
UPDATE z3saldo_associados s
SET rank_monetario = r.novo_rank
FROM rank_calc r
WHERE s.id = r.id
  AND s.rank_monetario IS DISTINCT FROM r.novo_rank;

-----------------------------------------------------------------

-- Contagem de dias ultima compra/venda: FORMULA
UPDATE z3saldo_associados
SET dias_ultima_compra = CURRENT_DATE - data_ultima_compra
WHERE dias_ultima_compra IS DISTINCT FROM (CURRENT_DATE - data_ultima_compra);

-- Contagem de dias ultima permuta: FORMULA
UPDATE z3saldo_associados
SET dias_ultima_venda = CURRENT_DATE - data_ultima_venda
WHERE dias_ultima_venda IS DISTINCT FROM (CURRENT_DATE - data_ultima_venda);

-->


--Recencia de Compra
UPDATE z3saldo_associados AS t
SET rank_recencia_compra = calc.rank_recencia_compra
FROM (
    SELECT
        s.id,
        CASE
            WHEN s.dias_ultima_compra IS NULL THEN 0
            ELSE
                CASE
                    WHEN s.dias_ultima_compra < 7 THEN 5
                    WHEN s.dias_ultima_compra < 14 THEN 4
                    WHEN s.dias_ultima_compra < 21 THEN 3
                    WHEN s.dias_ultima_compra < 35 THEN 2
                    WHEN s.dias_ultima_compra < 42 THEN 1
                    ELSE 0
                END
        END AS rank_recencia_compra
    FROM (
        SELECT
            s1.*
        FROM z3saldo_associados s1
    ) s
) AS calc
WHERE t.id = calc.id
  AND t.rank_recencia_compra IS DISTINCT FROM calc.rank_recencia_compra;




--Recencia de Venda
UPDATE z3saldo_associados AS t
SET rank_recencia_venda = calc.rank_recencia_venda
FROM (
    SELECT
        s.id,
        CASE
            WHEN s.dias_ultima_venda IS NULL THEN 0
            ELSE
                CASE
                    WHEN s.dias_ultima_venda < 7 THEN 5
                    WHEN s.dias_ultima_venda < 14 THEN 4
                    WHEN s.dias_ultima_venda < 21 THEN 3
                    WHEN s.dias_ultima_venda < 35 THEN 2
                    WHEN s.dias_ultima_venda < 42 THEN 1
                    ELSE 0
                END
        END AS rank_recencia_venda
    FROM (
        SELECT
            s1.*
        FROM z3saldo_associados s1
    ) s
) AS calc
WHERE t.id = calc.id
  AND t.rank_recencia_venda IS DISTINCT FROM calc.rank_recencia_venda;


"""

    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Executar o SQL
    cursor.execute(query)
    conn.commit()

    # Fechar cursor e conexão
    cursor.close()
    conn.close()

    print('Atualização 2 concluída!')
    return

# Formuladore()
