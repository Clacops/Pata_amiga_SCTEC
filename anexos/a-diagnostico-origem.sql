SELECT 
    -- 1. Total de grafias distintas de loja
    (SELECT COUNT(DISTINCT "Loja-Nome") FROM "stg_pedido") AS grafias_loja,
    
    -- 2. Total de grafias distintas de categoria
    (SELECT COUNT(DISTINCT "CategoriaProduto") FROM "stg_pedido") AS grafias_categoria,
    
    -- 3. Pedidos sem código de loja preenchido
    (SELECT COUNT(*) FROM "stg_pedido" 
     WHERE "Cod Loja" IS NULL OR TRIM("Cod Loja") IN ('', '-')) AS pedidos_sem_cod_loja,
    
    -- Pedidos sem nome de loja
    (SELECT COUNT(*) FROM "stg_pedido" 
     WHERE "Loja-Nome" IS NULL OR TRIM("Loja-Nome") IN ('', '-')) AS pedidos_sem_nome_loja,
    
    -- 4. Marcos de processo de entrega em branco
    COUNT(*) FILTER (WHERE "Dt Separacao Estoque" IS NULL OR TRIM("Dt Separacao Estoque") IN ('', '-')) AS separacao_em_branco,
    COUNT(*) FILTER (WHERE "DtNotaFiscal" IS NULL OR TRIM("DtNotaFiscal") IN ('', '-')) AS nota_em_branco,
    COUNT(*) FILTER (WHERE "Dt_Despacho_Transportadora" IS NULL OR TRIM("Dt_Despacho_Transportadora") IN ('', '-')) AS despacho_em_branco,
    COUNT(*) FILTER (WHERE "DtEntregaCliente" IS NULL OR TRIM("DtEntregaCliente") IN ('', '-')) AS entrega_em_branco
FROM "stg_pedido";
