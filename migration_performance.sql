-- =====================================================================
-- Migration de performance (rodar UMA vez no SQL Editor do Supabase)
-- Gerada a partir do diagnóstico de write-amplification / view lenta.
-- Tudo aqui é reversível.
-- =====================================================================

-- 1) Remove índices sem uso (0 scans desde a criação) na z2lista_negociacoes (164k linhas).
--    Comprovado por pg_stat_user_indexes: nunca usados pelos UPDATE em massa
--    (o planner escolhe Hash Join + Seq Scan). Só custavam escrita.
DROP INDEX IF EXISTS ix_z2_fran_comprador;
DROP INDEX IF EXISTS ix_z2_fran_vendedor;
DROP INDEX IF EXISTS ix_z2_orcamento;

-- (Mantidos: ix_z1_cnpj [43k+ scans], ix_z3_cnpj, ix_z1_nome_fantasia — esses são usados.)

-- 2) Reescreve a view vw_saldo_ultimo_ano.
--    ANTES: OR no JOIN -> Nested Loop, ~86 milhões de linhas descartadas, disco
--    temporário, ~23s por ciclo.
--    DEPOIS: UNION ALL pré-agregado -> Hash Aggregate + Hash Join, ~66ms
--    (comprovado por EXPLAIN ANALYZE, ~350x mais rápido).
--    Obs.: assume que comprador e vendedor de uma negociação são associados
--    diferentes (regra do sistema de permuta). Auto-negociação contaria 2x.
CREATE OR REPLACE VIEW public.vw_saldo_ultimo_ano AS
WITH neg AS (
    SELECT nome, SUM(valor) AS total
    FROM (
        SELECT associado_comprador AS nome, valor FROM z2lista_negociacoes
          WHERE data >= (CURRENT_DATE - INTERVAL '1 year') AND data <= CURRENT_DATE
        UNION ALL
        SELECT associado_vendedor AS nome, valor FROM z2lista_negociacoes
          WHERE data >= (CURRENT_DATE - INTERVAL '1 year') AND data <= CURRENT_DATE
    ) x
    GROUP BY nome
)
SELECT s.cnpj_ou_cpf, s.nome_fantasia,
       COALESCE(ROUND(neg.total::numeric, 2), 0)::numeric(10,2) AS total_permutado
FROM z3saldo_associados s
LEFT JOIN neg ON neg.nome = s.nome_fantasia;

-- =====================================================================
-- Rollback (se precisar):
--   Índices:  CREATE INDEX ix_z2_orcamento ON z2lista_negociacoes (orcamento);  (etc.)
--   View:     restaurar a definição antiga (bloco ANTIGO comentado em ZZ_SQL.py)
-- =====================================================================
