SELECT 
    "Cod Loja" AS codigo,
    "Loja-Nome" AS nome_digitado_na_venda,
    COUNT(*) AS total_pedidos
FROM stg_pedido
GROUP BY "Cod Loja", "Loja-Nome"
ORDER BY "Cod Loja", total_pedidos DESC;