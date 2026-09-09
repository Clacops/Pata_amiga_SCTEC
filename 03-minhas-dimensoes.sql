-- =====================================================================================
-- ARQUIVO 03: CARGA DAS MINHAS DIMENSÕES E PONTE
-- =====================================================================================

-- -------------------------------------------------------------------------------------
-- 1. CARGA DA DIM_CATEGORIA
-- -------------------------------------------------------------------------------------
-- Limpa a tabela para não dar erro se rodarmos mais de uma vez
DELETE FROM dim_categoria;

-- Linha -1 OBRIGATÓRIA
INSERT INTO dim_categoria (sk_categoria, categoria_origem, nome_categoria, grupo_categoria)
VALUES (-1, 'Nao Informado', 'Nao Informado', 'Nao Informado');

-- Carga das categorias 
INSERT INTO dim_categoria (categoria_origem, nome_categoria, grupo_categoria)
SELECT DISTINCT
    "CategoriaProduto" AS categoria_origem,
    CASE 
        WHEN UPPER(TRANSLATE("CategoriaProduto", 'ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇáàâãäéèêëíìîïóòôõöúùûüç', 'AAAAAEEEEIIIIOOOOOUUUUCaaaaaeeeeiiiiooooouuuuc')) LIKE '%MED%' THEN 'Medicamento'
        WHEN UPPER(TRANSLATE("CategoriaProduto", 'ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇáàâãäéèêëíìîïóòôõöúùûüç', 'AAAAAEEEEIIIIOOOOOUUUUCaaaaaeeeeiiiiooooouuuuc')) LIKE '%PETISC%' THEN 'Petisco'
        WHEN UPPER(TRANSLATE("CategoriaProduto", 'ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇáàâãäéèêëíìîïóòôõöúùûüç', 'AAAAAEEEEIIIIOOOOOUUUUCaaaaaeeeeiiiiooooouuuuc')) LIKE '%RA%' THEN 'Racao'
        WHEN UPPER(TRANSLATE("CategoriaProduto", 'ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇáàâãäéèêëíìîïóòôõöúùûüç', 'AAAAAEEEEIIIIOOOOOUUUUCaaaaaeeeeiiiiooooouuuuc')) LIKE '%HIG%' THEN 'Higiene'
        WHEN UPPER(TRANSLATE("CategoriaProduto", 'ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇáàâãäéèêëíìîïóòôõöúùûüç', 'AAAAAEEEEIIIIOOOOOUUUUCaaaaaeeeeiiiiooooouuuuc')) LIKE '%BRINQ%' THEN 'Brinquedo'
        WHEN UPPER(TRANSLATE("CategoriaProduto", 'ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇáàâãäéèêëíìîïóòôõöúùûüç', 'AAAAAEEEEIIIIOOOOOUUUUCaaaaaeeeeiiiiooooouuuuc')) LIKE '%ACESS%' THEN 'Acessorio'
        WHEN UPPER(TRANSLATE("CategoriaProduto", 'ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇáàâãäéèêëíìîïóòôõöúùûüç', 'AAAAAEEEEIIIIOOOOOUUUUCaaaaaeeeeiiiiooooouuuuc')) LIKE '%SERV%' THEN 'Servico'
        ELSE 'Nao Informado'
    END AS nome_categoria,
    CASE 
        WHEN UPPER(TRANSLATE("CategoriaProduto", 'ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇáàâãäéèêëíìîïóòôõöúùûüç', 'AAAAAEEEEIIIIOOOOOUUUUCaaaaaeeeeiiiiooooouuuuc')) LIKE '%MED%' THEN 'Saude e Higiene'
        WHEN UPPER(TRANSLATE("CategoriaProduto", 'ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇáàâãäéèêëíìîïóòôõöúùûüç', 'AAAAAEEEEIIIIOOOOOUUUUCaaaaaeeeeiiiiooooouuuuc')) LIKE '%PETISC%' THEN 'Alimentacao'
        WHEN UPPER(TRANSLATE("CategoriaProduto", 'ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇáàâãäéèêëíìîïóòôõöúùûüç', 'AAAAAEEEEIIIIOOOOOUUUUCaaaaaeeeeiiiiooooouuuuc')) LIKE '%RA%' THEN 'Alimentacao'
        WHEN UPPER(TRANSLATE("CategoriaProduto", 'ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇáàâãäéèêëíìîïóòôõöúùûüç', 'AAAAAEEEEIIIIOOOOOUUUUCaaaaaeeeeiiiiooooouuuuc')) LIKE '%HIG%' THEN 'Saude e Higiene'
        WHEN UPPER(TRANSLATE("CategoriaProduto", 'ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇáàâãäéèêëíìîïóòôõöúùûüç', 'AAAAAEEEEIIIIOOOOOUUUUCaaaaaeeeeiiiiooooouuuuc')) LIKE '%BRINQ%' THEN 'Bem-estar'
        WHEN UPPER(TRANSLATE("CategoriaProduto", 'ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇáàâãäéèêëíìîïóòôõöúùûüç', 'AAAAAEEEEIIIIOOOOOUUUUCaaaaaeeeeiiiiooooouuuuc')) LIKE '%ACESS%' THEN 'Bem-estar'
        WHEN UPPER(TRANSLATE("CategoriaProduto", 'ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇáàâãäéèêëíìîïóòôõöúùûüç', 'AAAAAEEEEIIIIOOOOOUUUUCaaaaaeeeeiiiiooooouuuuc')) LIKE '%SERV%' THEN 'Bem-estar'
        ELSE 'Nao Informado'
    END AS grupo_categoria
FROM stg_pedido;


-- -------------------------------------------------------------------------------------
-- 2. CARGA DA DIM_PRACA E BRIDGE_LOJA_PRACA
-- -------------------------------------------------------------------------------------
DELETE FROM bridge_loja_praca;
DELETE FROM dim_praca;

-- Linha -1 OBRIGATÓRIA na dimensão
INSERT INTO dim_praca (sk_praca, cod_praca, nome_praca, regional, domicilios_com_pet)
VALUES (-1, 'N/I', 'Nao Informado', 'Nao Informado', NULL);

-- Carga da dim_praca
INSERT INTO dim_praca (cod_praca, nome_praca, regional, domicilios_com_pet)
SELECT DISTINCT
    "CodPraca",
    "NomePraca",
    "Regional",
    CAST(REPLACE("DomiciliosComPet", '.', '') AS INT) AS domicilios_com_pet
FROM stg_loja_praca
WHERE "CodPraca" IS NOT NULL;

-- Carga da bridge_loja_praca
INSERT INTO bridge_loja_praca (cod_loja, sk_praca, fator_publico)
SELECT 
    stg."CodLoja" AS cod_loja,
    dp.sk_praca,
    CAST(REPLACE(stg."PercentualPublico", ',', '.') AS DECIMAL(6,4)) AS fator_publico
FROM stg_loja_praca stg
INNER JOIN dim_praca dp ON stg."CodPraca" = dp.cod_praca;


-- -------------------------------------------------------------------------------------
-- 3. AUDITORIA FINAL
-- -------------------------------------------------------------------------------------
SELECT 'dim_categoria' AS tabela, COUNT(*) AS total FROM dim_categoria
UNION ALL
SELECT 'dim_praca' AS tabela, COUNT(*) AS total FROM dim_praca
UNION ALL
SELECT 'bridge_loja_praca' AS tabela, COUNT(*) AS total FROM bridge_loja_praca;