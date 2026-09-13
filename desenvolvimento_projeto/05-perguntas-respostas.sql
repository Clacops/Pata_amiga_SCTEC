-- =====================================================================================
--  ARQUIVO 5:  AS CINCO PERGUNTAS DE NEGOCIO
--  Case: Pata Amiga - rede de petshops de SC  |  PostgreSQL 16
-- =====================================================================================
--  Rode depois de: 04-fato.sql
--
--  Cada pergunta e UMA consulta: um SELECT com JOIN e GROUP BY. A subconsulta
--  aparece na P2 e na P5, e serve para trazer o total da rede como denominador.
--
--  ATENCAO AO POSTGRESQL: int / int TRUNCA. Nos percentuais e taxas use o fator
--  100.0 / 1000.0 (com ponto); e ROUND(x, casas) exige x numerico.
-- =====================================================================================

-- =====================================================================================
--  P1 - ONDE ESTA O GARGALO DO PROCESSO DE ENTREGA?
-- =====================================================================================
--  Media (AVG) dos quatro intervalos ja calculados na carga, agrupada por porte
--  de loja. AVG ignora NULL - por isso a etapa nao cumprida foi gravada como NULL.
--  dias_total_ate_entrega e o processo inteiro, nao um dos quatro intervalos.

-- >>> ESCREVA AQUI a consulta da P1
SELECT 
    l.nome_loja,
    ROUND(AVG(f.dias_integracao_separacao), 2) AS media_integracao_separacao,
    ROUND(AVG(f.dias_separacao_nota), 2)       AS media_separacao_nota,
    ROUND(AVG(f.dias_nota_despacho), 2)        AS media_nota_despacho,
    ROUND(AVG(f.dias_despacho_entrega), 2)     AS media_despacho_entrega,
    ROUND(AVG(f.dias_total_ate_entrega), 2)    AS media_total_ate_entrega,
    COUNT(f.sk_pedido)                         AS total_pedidos_avaliados
FROM fato_pedido f
INNER JOIN dim_loja l ON f.sk_loja = l.sk_loja
GROUP BY l.nome_loja
ORDER BY media_total_ate_entrega DESC;


-- =====================================================================================
--  RESPOSTA DE P1 : ONDE ESTA O GARGALO DO PROCESSO DE ENTREGA?
-- =====================================================================================

--O abismo no tempo total: Perceba que as 9 primeiras lojas da lista (de Ituporanga até 
--Presidente Getúlio) demoram entre 14 e 16 dias no total para entregar o pedido. 
--Já o restante da rede (de Curitibanos para baixo) entrega em cerca de 7 a 8 dias. 
--Há um grupo específico de lojas levando o dobro do tempo!
--9 lojas mais lentas, a separação da mercadoria (media_separacao_nota) é rápida 
--(menos de 1 dia). O problema gritante está na coluna media_nota_despacho
-- (o tempo entre a emissão da nota fiscal e a transportadora de fato despachar o pedido).
--A descoberta: Nessas lojas mais lentas, a mercadoria fica parada esperando o despacho por 
--quase 8 a 9 dias, enquanto nas lojas eficientes essa espera é de apenas 3 dias.
-- A sua resposta de negócio para a diretoria seria: "O gargalo crítico da rede está na etapa de despacho (pós-faturamento) em um grupo específico de 9 lojas (liderado por Ituporanga e Santo Amaro da Imperatriz), onde a mercadoria fica retida por quase 10 dias.
-- O restante do processo logístico e as demais lojas operam dentro da normalidade."



-- =====================================================================================
--  P2 - QUAL CATEGORIA CONCENTRA O FATURAMENTO?
-- =====================================================================================
--  Esta e a pergunta que paga a dim_categoria. Agrupe pelo nome_categoria
--  PADRONIZADO (nunca pela grafia crua). O percentual do total usa uma
--  subconsulta com o faturamento da rede como denominador.

-- >>> ESCREVA AQUI a consulta da P2

SELECT 
    c.nome_categoria,
    SUM(f.vl_liquido) AS faturamento_categoria,
    ROUND(
        (SUM(f.vl_liquido) / (SELECT SUM(vl_liquido) FROM fato_pedido)) * 100.0, 2
    ) AS percentual_sobre_total
FROM fato_pedido f
INNER JOIN dim_categoria c ON f.sk_categoria = c.sk_categoria
GROUP BY c.nome_categoria
ORDER BY faturamento_categoria DESC;





-- =====================================================================================
--  P3 - O DESCONTO FUNCIONA IGUAL EM TODO CANAL?
-- =====================================================================================
--  Aqui NAO ha JOIN: desconto e canal foram padronizados na carga e moram na
--  propria fato. Compare o TICKET MEDIO com e sem desconto DENTRO de cada canal.
--  Confira se o WhatsApp aparece - se nao, o CASE do arquivo 04 testou APP antes
--  de WHATS.

-- >>> ESCREVA AQUI a consulta da P3

- =====================================================================================
--  P3 - A POLÍTICA DE DESCONTO E REPRESENTATIVIDADE POR CANAL
-- =====================================================================================
SELECT 
    canal_pedido,
    
    -- 1. Análise de Ticket Médio (A política funciona?)
    ROUND(AVG(CASE WHEN houve_desconto = 1 THEN vl_liquido END), 2) AS ticket_com_desconto,
    ROUND(AVG(CASE WHEN houve_desconto = 0 THEN vl_liquido END), 2) AS ticket_sem_desconto,
    
    -- 2. Volumes (Quantos pedidos recebem o incentivo e o total?)
    COUNT(sk_pedido) AS total_pedidos,
    SUM(houve_desconto) AS qtd_com_desconto,
    COUNT(sk_pedido) - SUM(houve_desconto) AS qtd_sem_desconto,
    
    -- 3. Representatividade Financeira (Qual o peso do canal?)
    SUM(vl_liquido) AS faturamento_canal,
    ROUND((SUM(vl_liquido) / (SELECT SUM(vl_liquido) FROM fato_pedido)) * 100.0, 2) AS share_faturamento_perc
    
FROM fato_pedido
GROUP BY canal_pedido
ORDER BY share_faturamento_perc DESC;

--ACRESCENTO AQUI A TABELA ANALISE SAZONALIDADE???

-- =====================================================================================
--  P4 - QUAL PRACA DE ATENDIMENTO CONCENTRA O FATURAMENTO?
-- =====================================================================================
--  Esta e a pergunta que paga a dim_praca e a ponte.
--  Caminho: fato_pedido -> dim_loja -> bridge_loja_praca -> dim_praca (a ponte
--  entra pelo cod_loja). O JOIN com a ponte DUPLICA a linha do pedido, uma por
--  praca - isso esta certo. Multiplique por b.fator_publico para o faturamento
--  nao ser contado duas vezes.

-- >>> ESCREVA AQUI a consulta da P4

-- =====================================================================================
--  P4 - QUAL PRAÇA DE ATENDIMENTO CONCENTRA O FATURAMENTO? (Com Rateio de Praça)
-- =====================================================================================
SELECT 
    p.nome_praca, 
    p.domicilios_com_pet, 
    ROUND(SUM(f.vl_liquido * b.fator_publico), 2) AS faturamento_rateado,
    COUNT(DISTINCT f.sk_pedido) AS total_pedidos_envolvidos
FROM fato_pedido f
JOIN dim_loja l ON f.sk_loja = l.sk_loja
JOIN bridge_loja_praca b ON l.cod_loja = b.cod_loja -- Se der erro aqui, me avise o nome da coluna na dim_loja
JOIN dim_praca p ON b.sk_praca = p.sk_praca
GROUP BY p.nome_praca, p.domicilios_com_pet
ORDER BY faturamento_rateado DESC;


-- =====================================================================================
--  P5 - ONDE ABRIR A PROXIMA LOJA, E O QUE OS DADOS NAO PERMITEM AFIRMAR?
-- =====================================================================================
--  (a) Ranqueie as lojas por itens POR MIL HABITANTES (numerador na fato,
--      denominador na dimensao), calculado AQUI na consulta - nunca gravado
--      pronto. Cruze com o tempo medio de entrega.
--  (b) Mostre o faturamento por faixa de franquia e explique por que ele NAO
--      responde "quanto veio de lojas que JA ERAM Ouro na data do pedido": o
--      cadastro so tem a foto de hoje.
--  (c) Meca o que ficou de fora: pedidos sem loja, entregas nao concluidas,
--      itens e valores em branco.

-- >>> ESCREVA AQUI as consultas da P5

-- =====================================================================================
-- P5 - MATRIZ DE CORTE COM SUBCONSULTA (Sem CTE e sem Window Function)
-- Foco: Isolar praças com alta densidade E tempo de entrega acima da média da rede
-- =====================================================================================

SELECT 
    l.nome_loja,
    ROUND((SUM(f.qt_itens * b.fator_publico) * 1000.0) / NULLIF(p.domicilios_com_pet, 0), 2) AS itens_por_mil_habitantes,
    ROUND(AVG(f.dias_total_ate_entrega), 2) AS tempo_medio_entrega_dias

FROM fato_pedido f
JOIN dim_loja l ON f.sk_loja = l.sk_loja
JOIN bridge_loja_praca b ON l.cod_loja = b.cod_loja
JOIN dim_praca p ON b.sk_praca = p.sk_praca

GROUP BY l.nome_loja, p.domicilios_com_pet

-- Filtra usando uma subconsulta simples para pegar a média geral de dias de entrega da rede
HAVING AVG(f.dias_total_ate_entrega) > (
    SELECT AVG(f_sub.dias_total_ate_entrega) 
    FROM fato_pedido f_sub
)

-- Ordena priorizando quem tem mais itens por mil habitantes e os maiores prazos
ORDER BY itens_por_mil_habitantes DESC, tempo_medio_entrega_dias DESC;

-- =====================================================================================
-- P5 (a) - DENSIDADE DE VENDAS (ITENS / MIL HABITANTES) E TEMPO MÉDIO DE LOGÍSTICA
-- ORDENADOS POR MIL HABITANTES (DESCENDENTE)
-- =====================================================================================
-- Regra: Numerador na Fato (qt_itens com rateio via bridge) e 
-- Denominador na Dimensão (domicilios_com_pet), calculado dinamicamente.
-- =====================================================================================

SELECT 
    l.nome_loja,
    p.nome_praca,
    p.domicilios_com_pet AS populacao_referencia,
    
    -- 1. Numerador na fato rateado pela ponte para evitar duplicação de vendas
    ROUND(SUM(f.qt_itens * b.fator_publico), 0) AS total_itens_rateados, 
    
    -- 2. Cálculo dinâmico da densidade: (Itens * 1000) / População da Dimensão
    ROUND((SUM(f.qt_itens * b.fator_publico) * 1000.0) / NULLIF(p.domicilios_com_pet, 0), 2) AS itens_por_mil_habitantes,
    
    -- 3. Cruzamento com o indicador de eficiência logística
    ROUND(AVG(f.dias_total_ate_entrega), 1) AS tempo_medio_entrega_dias

FROM fato_pedido f
JOIN dim_loja l ON f.sk_loja = l.sk_loja
JOIN bridge_loja_praca b ON l.cod_loja = b.cod_loja
JOIN dim_praca p ON b.sk_praca = p.sk_praca
GROUP BY l.nome_loja, p.nome_praca, p.domicilios_com_pet
ORDER BY itens_por_mil_habitantes DESC;


-- =====================================================================================
--  P5 (b) - FATURAMENTO POR FAIXA DE FRANQUIA (Visão do cadastro atual)
--  (b) --Mostre o faturamento por faixa de franquia e explique por que ele NAO
--      responde "quanto veio de lojas que JA ERAM Ouro na data do pedido": o
--      cadastro so tem a foto de hoje.
-- =====================================================================================
SELECT 
    l.faixa_franquia, 
    COUNT(DISTINCT f.sk_pedido) AS total_pedidos,
    ROUND(SUM(f.vl_liquido), 2) AS faturamento_total
FROM fato_pedido f
JOIN dim_loja l ON f.sk_loja = l.sk_loja
GROUP BY l.faixa_franquia
ORDER BY faturamento_total DESC;


-- =====================================================================================
--  P5 (c) - MEDIÇÃO DOS RESÍDUOS (Auditoria de Qualidade)
--  (c) --Meça o que ficou de fora: pedidos sem loja, entregas nao concluidas,
--      itens ou valores em branco/zerados  
-- =====================================================================================
SELECT 
    'Pedidos sem loja identificada' AS indicador, 
    COUNT(*) AS total_registros
FROM fato_pedido 
-- buscando a chave -1 
WHERE sk_loja = -1 

UNION ALL

SELECT 
    'Entregas não concluídas' AS indicador, 
    COUNT(*) AS total_registros
FROM fato_pedido 
WHERE dias_total_ate_entrega IS NULL

UNION ALL

SELECT 
    'Itens ou valores em branco/zerados' AS indicador, 
    COUNT(*) AS total_registros
FROM fato_pedido 
WHERE qt_itens IS NULL OR qt_itens = 0 OR vl_liquido IS NULL OR vl_liquido = 0;