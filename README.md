

## Passo 3: Modelo Estrela
![Diagrama do Modelo Estrela](estrela_fato_pata.png)

As cinco perguntas de negócio:

•	P1 : Onde está o gargalo da entrega? Qual o tempo médio, em dias, entre o pedido entrar no ERP e chegar na casa do cliente? E qual dos quatro intervalos do processo  Integração → Separação, Separação → Nota, Nota → Despacho, Despacho → Entrega  é o mais lento? O gargalo é o mesmo nos três portes de loja?

•	P2 : Qual categoria concentra o faturamento? Do faturamento total da rede, quanto vem de cada categoria de produto? Agrupe pelo nome padronizado, nunca pela grafia crua, e mostre também o percentual do total. A categoria campeã é a mesma nos três portes de loja?

•	P3 : O desconto funciona igual em todo canal? Compare o ticket médio COM e SEM desconto dentro de cada canal de venda (App, Site, Loja Física, Telefone, WhatsApp). Se o desconto derruba o ticket em um canal e não em outro, a política não deveria ser a mesma nos dois. Diga também quanto cada canal representa do faturamento.

•	P4 : Qual praça de atendimento concentra o faturamento? Atenção: uma loja entrega em mais de uma praça. O rateio precisa ser feito pelo percentual do público, e a soma por praça tem de fechar com o faturamento da rede. Cruze o faturamento rateado com o número de domicílios com pet de cada praça.

•	P5 : Onde abrir a próxima loja, e o que os dados NÃO permitem afirmar? 
a.	Ranqueie as lojas por itens vendidos por mil habitantes da cidade  não em valor absoluto  e cruze com o tempo médio de entrega. 
b.	A faixa de franquia no cadastro é a de hoje: o passado foi sobrescrito. Mostre o faturamento por faixa ATUAL e explique por que isso não responde “quanto veio de lojas que JÁ ERAM Ouro na data do pedido”.
c.	Meça o que ficou de fora: pedidos sem loja identificada, entregas ainda não concluídas, itens e valores em branco.
## Decisões de Modelagem e Limpeza (Passos 1 a 3)

Para garantir a qualidade dos dados e o correto funcionamento do modelo dimensional, as seguintes decisões técnicas foram aplicadas na construção das dimensões:

* **Garantia de Integridade Referencial (Tratamento de Nulos):** Antes de qualquer carga de dados, inserimos a linha `-1` (Não Informado) em todas as dimensões (`dim_categoria`, `dim_praca`, etc.). Isso previne falhas de JOIN na tabela fato quando a origem apresentar dados em branco ou nulos.
* **Regras de Negócio na dim_categoria:** Havia o risco de ambiguidade na classificação (ex: "Ração Medicamentosa"). Para resolver, estruturamos o `CASE WHEN` testando a string "MED" rigorosamente antes de "RA". Além disso, mantivemos a coluna `categoria_origem` com a grafia crua exata para viabilizar o cruzamento futuro com a *staging area*.
* **Estrutura Snowflake e Tabela Ponte:** A relação muitos-para-muitos entre Lojas e Praças foi resolvida através da `bridge_loja_praca`. 
* **Tipagem de Dados:** Durante a carga da praça e da ponte, tratamos as strings numéricas, removendo pontos de milhar em `domicilios_com_pet` para conversão em `INT` e trocando vírgulas por pontos no `fator_publico` para conversão em `DECIMAL(6,4)`.
--------------------------------------------

## Tarefa 1: Diagnóstico da Origem

Durante a análise exploratória das três tabelas de origem, identificamos problemas críticos de qualidade de dados que orientaram as decisões de modelagem:

* **Tabela de Pedidos:** Apresentou falhas severas de preenchimento de chaves e datas, o que exigiu o tratamento de nulos e a criação da chave `-1` (Não Informado) para garantir a integridade da Tabela Fato.
* **Tabela de Lojas/Praças:** Apresentou inconsistência na tipagem e formatação de métricas (ex: fator público com vírgula e domicílios com pontos separadores).
* **Tabela de Categorias:** Apresentou ambiguidade nas nomenclaturas, exigindo a criação de regras de prioridade (ex: testar 'MED' antes de 'RA') para evitar dupla classificação.

##**Métricas do Diagnóstico:**
##* **Grafias de Loja:** Foram identificadas [X] grafias diferentes.
## * **Grafias de Categoria:** Existem [X] grafias distintas na origem.

* **Grafias de Loja:** A tabela de pedidos (`stg_pedido`) apresenta inconsistências graves, registrando **32 grafias diferentes** para os nomes das lojas devido a variações de digitação, enquanto o cadastro oficial (`stg_loja`) possui o quantitativo normalizado.

Dimensão da falha: Saber que temos 1.575 registros sem código de loja nos mostra que um simples INNER JOIN (que descartaria registros sem correspondência) destruiria quase 40% da nossa base de vendas. Por isso, a escolha pelo LEFT JOIN combinada com o COALESCE(..., -1) é a decisão técnica ideal.

Exceções pontuais: Saber que apenas 3 registros estão sem nome de loja nos indica que são casos extremamente isolados (talvez um erro de digitação único na ponta), o que reforça a necessidade de tratá-los de forma genérica pela chave substituta de erro/não informado.

* **Grafias de Categoria:** Identificada variação nas formas de preenchimento (ex: colunas como `CategoriaProduto`), exigindo regras estritas de tratamento via `CASE WHEN`.

* **Tratamento de Nulos e Chaves:** A presença de registros sem preenchimento correto exigiu a adoção de chaves substitutas (`-1`) para preservar a integridade referencial na Tabela Fato.
* **Pedidos sem código de loja:** [X] pedidos vieram sem a identificação do código.
* **Pedidos sem nome de loja:** [X] pedidos vieram sem o nome da loja.
* **Marcos de processo em branco:** [X] marcos (datas) vieram em branco.

--------------------------------------------
O porquê do arquivo fato: 
A tabela fato é o coração do seu Data Warehouse. Enquanto as dimensões que já criamos respondem ao "quem, onde, quando e o quê" (o contexto descritivo), a tabela fato responde ao "quanto" (os números, a métrica do evento).

Na modelagem dimensional, o objetivo real de criarmos a fato é centralizar o histórico de eventos do negócio de uma forma estruturada para leitura muito rápida e agregações analíticas (somas, médias, contagens).

Especificamente no projeto "Pata Amiga", a criação da fato_pedido atende a três propósitos fundamentais:

Registrar o Evento de Negócio (O Grão): Ela materializa a transação principal. Você definiu que "1 linha = 1 pedido". A fato garante que cada pedido feito se torne um registro único conectando todas as pontas daquela venda.

Armazenar as Métricas: É exclusivamente na tabela fato que guardamos os valores quantitativos que o negócio quer analisar. Aqui, será o valor_venda.

Centralizar os Cruzamentos (SKs): A fato não guarda textos (como nome da loja ou da categoria). Ela guarda apenas as chaves substitutas (sk_loja, sk_categoria, sk_tempo). Quando você precisar responder a uma pergunta como "Qual o valor total vendido de medicamentos na praça X no mês Y?", o banco de dados vai direto na fato, soma os valores e usa essas chaves para puxar os filtros das dimensões ao redor rapidamente.

Em resumo, nós criamos a tabela fato para deixar o banco de dados otimizado para a extração de relatórios e construção de painéis (dashboards). É essa tabela que vai nos permitir responder matematicamente às perguntas do Passo 5 do seu edital.

🏗️ Decisões de Modelagem e Arquitetura
Durante o desenvolvimento deste Data Warehouse, três princípios fundamentais foram adotados:

Preservação da Origem (Staging): Os dados brutos não sofreram operações de UPDATE ou ALTER. As falhas da origem (como os 1.575 pedidos sem código de loja) foram preservadas para fins de auditoria.

Camada Dimensional como "Tradutora": As inconsistências textuais (como as 37 grafias diferentes para categorias) foram resolvidas na carga da dim_categoria. Isso criou um catálogo limpo e padronizado, permitindo que a Tabela Fato apenas relacione as chaves numéricas sem carregar o "caos" do sistema legado.

Tratamento de Exceções e Chaves Órfãs: Para garantir a integridade referencial da Tabela Fato sem perder registros de faturamento, adotou-se o uso de chaves substitutas (-1 / "Não Informado") em todas as Dimensões, garantindo que nenhuma Foreign Key (FK) ficasse nula na Fato.

A estrutura completa e oficial da fato_pedido (com todas as colunas de métricas, dias de entrega, canal e desconto) já foi criada no seu banco de dados quando rodamos o arquivo 02-dimensoes-prontas.sql lá atrás.
____________________________________________________________________________________________
O erro sintaxe de entrada é inválida para tipo integer: "" significa que nós tentamos pegar um campo vazio (um texto em branco, "") e forçar a conversão dele para número inteiro (INT).Lá no texto do Encarte (no trecho sobre os desafios da P5), o projeto avisou discretamente: "Meça o que ficou de fora: pedidos sem loja identificada, entregas ainda não concluídas, itens e valores em branco."  Nós tratamos os valores vazios no Faturamento, mas deixamos passar os valores vazios na coluna Quantidade de Itens (qt_itens). O nosso script estava fazendo simplesmente um CAST(stg."QTD.Itens" AS INT), o que faz o banco "engasgar" quando chega numa linha onde a quantidade veio vazia.Para resolver, nós aplicamos a mesma Regra dos Números que o encarte mandou usar para todos os casos: se for vazio, grava NULL.  (correcao tabela fato)

________________________________________________________________________
A tabela fato é o coração do Data Warehouse. 
Ele é o momento exato em que fazemos o ETL (Extração, Transformação e Carga).
Vamos "traduzir" os blocos principais desse código para você entender a engenharia por trás dele:

1. Preparando o Palco (A Estrutura)
    O bloco DROP TABLE e CREATE TABLE garante que a tabela seja montada exatamente com o "molde" exigido pelo projeto (as chaves estrangeiras, os campos de texto padronizados e as métricas numéricas). 

    O DELETE FROM é uma trava de segurança. Ele limpa a tabela para garantir que, se você precisar rodar o script de novo, os dados não sejam duplicados.

2. As Chaves de Tempo (Ligando com o Calendário)
    A origem mandou a data de compra no formato americano cheio de texto (MM/DD/YYYY HH12:MI AM). O código converte isso em um número inteiro simples (ex: 20231116), que é como a nossa dim_tempo funciona. 

    Na data de entrega, usamos a função COALESCE(..., -1). Isso resolve o problema dos 1.953 pedidos em aberto: se a data estiver vazia, o banco grava -1 (Não Informado) em vez de deixar o campo nulo e quebrar o cruzamento. 

     3. As Chaves de Negócio (Loja e Categoria)
        Aqui nós usamos os COALESCE(..., -1) de novo. Se o pedido for um daqueles 3 que vieram sem loja identificada, nós não perdemos a venda; nós apenas a direcionamos para a loja fictícia -1. 

     4. A Padronização em Tempo Real (Desconto e Canal)
        Para o Desconto, o script varre todas as dezenas de formas que escreveram "Sim" ou "Não" e uniformiza o texto. 
        
        No Canal de Vendas, aplicamos a regra estrita do encarte: testamos '%WHATS%' antes de testar '%APP%' no CASE WHEN. Isso impede que a palavra "WhatsApp" seja classificada erroneamente como "App", garantindo a precisão da Pergunta 3. 

     5. A Regra dos Números e Tratamento de VaziosQuantidade de Itens: 

        Foi aqui que o erro anterior nos pegou. Adicionamos o CASE WHEN para transformar espaços em branco ou hifens em NULL, em vez de tentar forçar um texto vazio a virar número inteiro.  
        
        Valor Líquido: O script faz uma faxina pesada no texto. Ele arranca o "R$", tira os espaços, remove os pontos de milhar e troca a vírgula dos centavos por ponto, finalmente transformando tudo no tipo DECIMAL(15,2) aceito pelo banco. 
        
     6. O Cálculo do Gargalo Logístico (Subtração de Datas)

        Em vez de gravar as datas originais, o código subtrai o "fim" menos o "início" (ex: DtNotaFiscal::date - Dt_Separacao::date) para gerar o número exato de dias de cada etapa. 

        A inteligência aqui é gravar NULL (e nunca zero) se o evento final ainda estiver em branco, para que a média de atrasos (AVG) calculada pela diretoria lá na Pergunta 1 seja matematicamente correta.  
        
    7. Os Cruzamentos (JOINs)
    
        Lá no final do script, os LEFT JOIN funcionam como uma ponte. Nós pegamos a stg_pedido (que está suja) e cruzamos com a dim_categoria (que acabamos de limpar no passo 03) usando a grafia crua original.  
        
        Para a Loja, como 39% vieram sem código, nós fazemos o cruzamento padronizando e comparando os nomes, arrumando até os apelidos de cidade no meio do caminho. 
        
     Em resumo: o código lê a sujeira, limpa, calcula os tempos, descobre as chaves corretas e só então grava a versão pura na fato_pedido.

     ________________________________________________________
     Todo o esforço de engenharia de dados que fizemos até aqui serviu exatamente para não dependermos mais dessas bases "sujas" e desestruturadas. 
     O objetivo central de um Data Warehouse é ser a única fonte da verdade para o negócio. 
     Como já extraímos, limpamos, padronizamos e carregamos os dados, toda a inteligência necessária agora mora exclusivamente dentro do seu banco de dados PostgreSQL, dividida perfeitamente entre a fato_pedido e as dimensões.