WITH metricas AS (
    SELECT 'stg_pedido' AS teste, COUNT(*) AS obtido, 4044 AS esperado FROM stg_pedido
    UNION ALL
    SELECT 'stg_loja', COUNT(*), 32 FROM stg_loja
    UNION ALL
    SELECT 'stg_loja_praca', COUNT(*), 48 FROM stg_loja_praca
    UNION ALL
    SELECT 'dim_tempo', COUNT(*), 236 FROM dim_tempo
    UNION ALL
    SELECT 'dim_loja', COUNT(*), 33 FROM dim_loja
    UNION ALL
    SELECT 'dim_categoria', COUNT(*), 38 FROM dim_categoria
    UNION ALL
    SELECT 'dim_praca', COUNT(*), 13 FROM dim_praca
    UNION ALL
    SELECT 'bridge_loja_praca', COUNT(*), 48 FROM bridge_loja_praca
    UNION ALL
    SELECT 'fato_pedido', COUNT(*), 4044 FROM fato_pedido
    UNION ALL
    -- Validação das 8 categorias padronizadas distintas
    SELECT 'categorias padronizadas', COUNT(DISTINCT nome_categoria), 8 FROM dim_categoria
    UNION ALL
    SELECT 'sk_loja nula/orfa', COUNT(*), 0 FROM fato_pedido WHERE sk_loja IS NULL OR sk_loja NOT IN (SELECT sk_loja FROM dim_loja)
    UNION ALL
    SELECT 'sk_categoria nula/orfa', COUNT(*), 0 FROM fato_pedido WHERE sk_categoria IS NULL OR sk_categoria NOT IN (SELECT sk_categoria FROM dim_categoria)
    UNION ALL
    SELECT 'sk_tempo_entrega nula/orfa', COUNT(*), 0 FROM fato_pedido WHERE sk_tempo_entrega IS NULL OR sk_tempo_entrega NOT IN (SELECT sk_tempo FROM dim_tempo)
    UNION ALL
    SELECT 'sem loja', COUNT(*), 3 FROM fato_pedido WHERE sk_loja = -1
    UNION ALL
    SELECT 'sem entrega', COUNT(*), 1953 FROM fato_pedido WHERE sk_tempo_entrega = -1
    UNION ALL
    -- Nome correto da coluna verificado: canal_pedido
    SELECT 'WhatsApp', COUNT(*), 414 FROM fato_pedido WHERE canal_pedido ILIKE '%whats%'
    UNION ALL
    SELECT 'pedidos sem itens', COUNT(*), 257 FROM fato_pedido WHERE qt_itens IS NULL
    UNION ALL
    SELECT 'pedidos sem valor', COUNT(*), 121 FROM fato_pedido WHERE vl_liquido IS NULL
)
SELECT 
    teste, 
    obtido, 
    esperado,
    CASE WHEN obtido = esperado THEN 'OK' ELSE 'DIVERGENTE' END AS status
FROM metricas;