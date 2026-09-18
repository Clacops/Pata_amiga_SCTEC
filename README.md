
--------------------------------------------

# 🐾 Pata Amiga - MiniProjeto Data Warehouse -  (SCTEC)

Este repositório é resultado do desenvolvimento de um modelo dimensional estruturado com o intuito de analisar processos varejistas e responder a dúvidas de negócio, principalmente quanto ao gerenciamento logístico das vendas em um Data Warehouse.
Foi demandado para avaliação de atividades durante a realização do Curso Carreira Tech -  Trilha Análise de Dados em setembro-2026. 
#### O miniprojeto em sua integra, inclusive com as bases de dados estão neste [link](https://drive.google.com/file/d/1wcCgg2XGKacYdnjAoL3gisvcA0-1XDHj/view?usp=sharing)

#### Autora: Clarice Maria Souza Copstein
#### Curso: SCTEC · Módulo 2

### 🎥 Apresentação em vídeo

A apresentação do projeto, incluindo a modelagem dimensional, as principais decisões de tratamento dos dados e as discussões sobre as respostas das perguntas, estão disponíveis no link abaixo: ▶️ ** [GitHub](https://github.com/Clacops/Pata_amiga_SCTEC)**

---
## 📌 Índice

- [Contextualização](#contextualização)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Fontes de Dados e Contexto do Projeto](#fontes-de-dados-e-contexto-do-projeto)
- [Etapas de Carga e Execução](#etapas-de-carga-e-execução)
- [Tecnologias e Ferramentas Utilizadas](#tecnologias-e-ferramentas-utilizadas)
- [Arquitetura e Modelagem Dimensional](#arquitetura-e-modelagem-dimensional)
- [Perguntas de Negócio e Análises Estratégicas (Etapa 05)](#perguntas-de-negocio-e-analises-estrategicas-etapa-05)
- [Reconciliação Quantitativa](#reconciliacao-qualitativa)
- [Limitações Analíticas](#limitações-analiticas)
- [Evolução Técnica ](#evoluçao-tecnica) 



##  Contextualização

🔍Foram analisados dados (4.044 pedidos) da rede - **Pata Amiga** - que possui  32 lojas de pet shops no Estado de Santa Catarina, nas datas que compreendem 01/09/2023 e 31/03/2024. 

O objetivo é utilizar estes sete meses para analisar o desenvolvimento do mercado da empresa e prever as possibilidades de melhorias de negócio no próximo ciclo. Para tal, a empresa entende a importância de localizar o gargalo logístico, entender a composição do faturamento e orientar um estudo de expansão com vistas a decidir onde deverá ser localizada a próxima loja.

Para tanto desenvolvi este Pipeline de dados e análise estratégica que integram uma modelagem dimensional em **PostgreSQL**, automação em **Python** e visualizações gerenciais (gráficos e tabelas) focadas em inteligência de mercado, expansão e governança de dados.

Foi realizada etapa final de Reconciliação quantitativa para validação dos dados. 

##  Estrutura do Repositório 

📂
```text
Pata_amiga_SCTEC/
├── .vscode/                                     # Configurações do ambiente no VS Code
│   └── settings.json
├── anexos/                                      # Entregáveis analíticos, gráficos e evidências
│   ├── p1/                                      # P1: Tempos de entrega e eficiência logística
│   │   ├── grafico_tempos_entrega_p1.png
│   │   └── tabela_pedidos_entregas_p1.txt
│   ├── p2/                                      # P2: Faturamento consolidado por categoria de produto
│   │   ├── grafico_faturamento_categoria_p2.png
│   │   ├── tabela_faturamento_categoria_port.txt
│   │   └── tabela_grafico_p2.py
│   ├── p3/                                      # P3: Impacto de descontos por canal de venda
│   │   ├── grafico_desconto_canal_p3.png
│   │   └── tabela_desconto_canal_p3.txt
│   ├── p4/                                      # P4: Rateio de faturamento por praça e loja (Bridge)
│   │   ├── gerar_grafico_p4.py
│   │   ├── grafico_3d_barras_pracas_p4.jpg
│   │   ├── grafico_3d_barras_pracas_p4.png
│   │   ├── grafico_faturamento_praca_p4.png
│   │   ├── tab_faturamento_praca_loja_p4.txt
│   │   └── tabela_faturamento_praca_p4.txt
│   └── p5/                                      # P5: Análises estratégicas e diagnósticos avançados
│       ├── p5a/                                 # P5a: Densidade de vendas por domicílio com pet
│       │   ├── grafico_top10_densidade_p5a.png
│       │   ├── tabela_grafico_p5a.py
│       │   └── tabela_ranking_densidade_p5a.txt
│       ├── p5b/                                 # P5b: Faturamento estratificado por porte de loja
│       │   ├── grafico_colunas_p5b.png
│       │   ├── tabela_faturamento_franquia_p5b.txt
│       │   └── tabela_grafico_p5b.py
│       └── p5c/                                 # P5c: Auditoria de qualidade e grafias na origem
│           ├── a-diagnostico-origem.sql
│           └── diagnostico_grafias_loja.csv
├── desenvolvimento_projeto/                     # Pipeline SQL do Data Warehouse (01 a 05)
│   ├── 00-conferencia.sql
│   ├── 01-carga-staging.sql
│   ├── 02-dimensoes-prontas.sql
│   ├── 03-dimensoes.sql
│   ├── 04-fato.sql
│   └── 05-perguntas-respostas.sql
├── reconciliacao_quantitativa/                  # Auditoria contábil e conferência de chaves do DW
│   ├── sincronizacao_dados_quantitativo_fi...
│   ├── sincronizacao_dados.sql
│   ├── validacao_etapas.txt
│   └── validacao_geral_etapas.txt
├── .env                                         # Credenciais locais e variáveis de ambiente (gitignored)
├── .gitignore                                   # Regras de exclusão do repositório Git
├── estrela_fato_pata.png                        # Diagrama relacional da modelagem dimensional (Star Schema)
├── README.md                                    # Documentação técnica e apresentação do case
└── requirements.txt                             # Dependências Python (pandas, matplotlib, seaborn, etc.)```
```

##   Fontes de Dados e Contexto do Projeto

📊 Os dados necessários para análise estavam distribuídos em três fontes distintas e que podem ser acessadas no [link](https://drive.google.com/file/d/1wcCgg2XGKacYdnjAoL3gisvcA0-1XDHj/view?usp=sharing):

* **`stg_loja`**: cadastro de lojas (32 registros).
* **`stg_loja_praca`**: cadastro de lojas (48 registros).
* **`stg_pedidos`**: cadastro das praças de atendimento (4.044 registros).
<br>
*Todas as bases apresentavam "defeitos" como: problemas na padronização de escrita, formatação de datas, espaços vazios ou nulos, e inconstâncias textuais. Conforme as diretrizes do miniprojeto, essas inconsistências exigiram tratamentos e adequações com o intuito de manter as bases de dados originais preservadas e sem alterações.*


##  Etapas de Carga e Execução

⚙️ Além dos dados entregues para a execução do projeto também foram entregues cinco arquivos como etapas principais e mais uma: o script de conferência. Todas ordenadas sequencialmente:

* **`00-conferencia.sql`**: script de validação e conferência das etapas.
* **`01-carga_staging.sql`**: carga inicial das tabelas de staging.
* **`02-dimensoes_prontas.sql`**: processamento das dimensões preparadas.
* **`03-dimensoes.sql`**: criação e carga das demais dimensões do modelo.
* **`04-fato.sql`**: processamento e carga da tabela fato.
* **`05-perguntas.sql`**: script contendo as consultas para responder às perguntas de negócio.

### 🏗️ Decisões de Modelagem e Arquitetura**

Durante o desenvolvimento deste *Data Warehouse*, três princípios fundamentais de engenharia e modelagem dimensional foram adotados:

* **Preservação da Origem (Staging):** Os dados brutos permaneceram imutáveis, sem operações de `UPDATE` ou `ALTER TABLE`. As anomalias de origem (como os 1.575 pedidos sem identificação de loja) foram mantidas na camada *staging* para garantir a rastreabilidade e permitir auditorias.
* **Camada Dimensional como "Camada Tradutora":** Inconsistências cadastrais (como as 37 variações textuais para categorias de produtos) foram tratadas na carga da `dim_categoria`. Esse processo padronizou o catálogo de negócio, permitindo que a tabela fato armazene apenas chaves substitutas limpas, isolando o ruído operacional dos sistemas legados.
* **Tratamento de Exceções e Chaves Órfãs:** Para preservar a integridade referencial sem descartar registros de faturamento, implementou-se o registro padrão de exceção (`-1` / "Não Informado") em todas as dimensões, impedindo a ocorrência de chaves estrangeiras (`FK`) nulas na fato.

---

> ⚠️ **Diretrizes de Execução e Reprodutibilidade:**  
> Os scripts SQL devem ser executados rigorosamente na sequência numérica indicada. Recomenda-se rodar o script de validação `00-conferencia.sql` após a conclusão de cada etapa para certificar a consistência dos registros no PostgreSQL/pgAdmin antes de avançar para a carga da tabela fato (`04-fato.sql`) e para as consultas analíticas (`05-perguntas.sql`).

---

### Decisões Técnicas Aplicadas nas Dimensões (Passos 1, 2 e 3)

* **Garantia de Integridade Referencial:** Inclusão prévia do registro sentinela `-1` ("Não Informado") em dimensões-chave (`dim_categoria`, `dim_praca`), mitigando falhas de *JOIN* em pedidos com dados ausentes.
* **Padronização e Precedência de Regras de Negócio (`dim_categoria`):** Para sanar ambiguidades de texto (como "Ração Medicamentosa"), o script priorizou a condição para medicamentos antes de rações gerais na cláusula `CASE WHEN`. A coluna `categoria_origem` foi mantida intacta para possibilitar o *de-para* com a área de *staging*.
* **Resolução de Relações Muitos-para-Muitos (N:N):** A relação entre lojas físicas e praças de mercado foi estruturada por meio da tabela de ligação (`bridge_loja_praca`), preservando o modelo dimensional sem duplicar faturamento na fato.
* **Sanitização e Conversão de Tipos:** Conversão de strings numéricas para tipos analíticos nativos, limpando separadores de milhar em `domicilios_com_pet` para `INT` e convertendo vírgulas em pontos decimais no `fator_publico` para `DECIMAL(6,4)`.

---

**Roteiro Sequencial de Desenvolvimento:**

1. **Tarefa 1 — Diagnóstico da Origem:** Mapeamento de anomalias, dados nulos e divergências de escrita na camada *staging*.
2. **Tarefa 2 — Tratamento e Limpeza:** Definição de regras de conversão de tipos, limpeza de caracteres especiais e tratamento de valores omissos.
3. **Tarefa 3 — Carga e Validação Dimensional:** Construção de `dim_categoria`, `dim_praca` e `bridge_loja_praca`, além da validação das dimensões `dim_tempo` e `dim_loja`.
4. **Tarefa 4 — Construção da Tabela Fato:** Carga da `fato_pedido` com cálculo de métricas de vendas e resolução de chaves estrangeiras.
5. **Tarefa 5 — Consultas Analíticas e Insights:** Extração de indicadores de desempenho, gargalos logísticos e auditoria de qualidade (P1 a P5).
____________________________________________________________________
Para garantir a qualidade dos dados e o correto funcionamento do modelo dimensional, as seguintes decisões técnicas foram aplicadas na construção das dimensões seguindo as orientações sugeridas para o bom desenvolvimento do projeto

* **Garantia de Integridade Referencial (Tratamento de Nulos):** Antes de qualquer carga de dados, inserimos a linha `-1` (Não Informado) em todas as dimensões (`dim_categoria`, `dim_praca`, etc.). Isso previne falhas de JOIN na tabela fato quando a origem apresentar dados em branco ou nulos.
* **Regras de Negócio na dim_categoria:** Havia o risco de ambiguidade na classificação (ex: "Ração Medicamentosa"). Para resolver, estruturamos o `CASE WHEN` testando a string "MED" rigorosamente antes de "RA". Além disso, mantivemos a coluna `categoria_origem` com a grafia crua exata para viabilizar o cruzamento futuro com a *staging area*.
* **Estrutura Snowflake e Tabela Ponte:** A relação muitos-para-muitos entre Lojas e Praças foi resolvida através da `bridge_loja_praca`. 
* **Tipagem de Dados:** Durante a carga da praça e da ponte, tratamos as strings numéricas, removendo pontos de milhar em `domicilios_com_pet` para conversão em `INT` e trocando vírgulas por pontos no `fator_publico` para conversão em `DECIMAL(6,4)`.


## 🚀 Como Executar o Projeto

1. Clone o repositório e acesse a pasta do projeto:
   ```bash
   git clone [https://github.com/Clacops/Pata_amiga_SCTEC.git]
   cd Pata_amiga_SCTEC
2. Instale as bibliotecas Python necessárias:
   ```bash
    pip install -r requirements.txt
3. Configure as credenciais do banco de dados;
* Crie um arquivo .env na raiz do projeto baseando-se no modelo .env.example;
* Informe suas credenciais de conexão do PostgreSQL (DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME);
* Execute os scripts SQL no pgAdmin em ordem sequencial.
4. Execute as cargas do Data Warehouse;
5. Siga a execução dos scripts SQL em ordem sequencial (da etapa 00 até a 05) no seu pgAdmin;
6. Gere os relatórios e gráficos analíticos;
7. Acesse a pasta "05-perguntas-respostas.sql" e execute os scripts em Python/SQL com as perguntas de 1 a 5 para atualizar as saídas em CSV e os gráficos. 
8. Na pasta anexos, voce encontrará as tabelas(csv) e graficos(png/jpg), além dos códigos em Python respectivamente às perguntas.

##  Tecnologias e Ferramentas Utilizadas 
🛠️ **Tecnologias necessárias para executar o projeto:**
Banco de Dados Relacional / DW: PostgreSQL / pgAdmin 4 - Postgres SQL 17
Linguagem de Consulta: SQL padrão (modelagem estrela, agregações condicionais e otimização de consultas sem CTEs/Window Functions) Linguagem de Automação & Visualização: Python 3.10 e 3.14 (Pandas, Matplotlib, SQLAlchemy, Psycopg2, Dotenv) import os e Controle de Versão: Git e GitHub. o projeto esta publicado no GigHub.
O histórico do projeto está publicado no [GitHub](https://github.com/Clacops/Pata_amiga_SCTEC), com branches e commits por etapa.


##  Arquitetura e Modelagem Dimensional
📊 O projeto foi construído sob uma rigorosa arquitetura de **Data Warehouse** em esquema estrela (Star Schema), estruturando tabelas dimensionais (dim_loja, dim_categoria, dim_praca, dim_tempo, dim_cliente, dim_canal, dim_desconto) e a tabela central de fatos (fato_pedido), além de tabelas ponte (bridge tables) para tratar adequadamente a variedade de atendimento das praças sem duplicar o faturamento.

👉 **Modelo Estrela - (Star Schema)**
![Diagrama do Modelo Estrela](estrela_fato_pata.png)



##  Perguntas de Negócio e Análises Estratégicas (Etapa 05)

📈A etapa final consolida a extração de valor analítico respondendo as cinco grandes perguntas gerenciais: perguntas de negócio

🎯 •   **P1** - *Onde está o gargalo do processo de entrega? Mapeamento dos intervalos entre integração, separação, emissão de nota, despacho e entrega final por porte de loja.*

    
    
    🏷️ 📊 Evidência dos Dados (Resultados)

    • O gargalo está na nota → despacho das lojas nos três portes (tempo entre a emissão da nota fiscal e a 
    transportadora de fato despachar o pedido).
    • Uma vez o pedido lançado no ERP a etapa que apresenta maior intervalo médio de dias na rede está entre a nota → despacho: 8,53 dias nas empresas porte pequeno ante 3,32 - nas grandes e 3,34 nas médias respectivamente.
    • A descoberta: Nessas lojas mais lentas, a mercadoria fica parada esperando o despacho por 
    quase 8 a 9 dias, enquanto nas lojas eficientes essa espera é de apenas 3 dias.
    • Ação: avaliar o que ocorre na expedição da nota, provavelmente a periodicidade da coleta e despacho das lojas pequenas, podendo haver processo manual de emissão de nota e assim fator também relacionado a numero  RH
    •Em todas as fases do processo percebe-se q os tempos sao maiores nas lojas pequenas, exceção a separação → nota. 


👉 [Ver Tabela ERP de Evidência da P1](anexos/p1/tabela_pedidos_entregas_p1.txt)
👉 [Ver Gráfico ERP de Evidência da P1](anexos/p1/grafico_tempos_entrega_p1.png)


---

🎯 •   **P2** - *Qual a categoria concentra o faturamento?*

   Foi realizada consulta SQL & Regra de Negócio:  Cruzamento da tabela `fato_pedido` com a `dim_categoria`   `(sk_categoria)`, aplicando uma subconsulta para somar o faturamento total da rede e calcular a participação percentual exata de cada categoria.
    
     🏷️ 📊 Evidência dos Dados 
     
      1º Lugar: Ração — Faturamento de R$ 1.076.202,55, representando 60,01% de toda a receita da rede.
      2º Lugar: Medicamento** — Faturamento de R$ 305.904,03, representando **17,06%**.
      Demais categorias:** Petisco (7,17%), Serviço (5,24%), Higiene (5,15%), Acessório (3,61%) e Brinquedo (1,76%).

   Existe uma alta Concentração de Receita com uma altíssima dependência do setor de nutrição animal **- Ração**, que sozinha ultrapassa a marca de **60%** de tudo o que a rede comercializa.

  **Recomendação estratégica**: diretoria e o setor de supply chain blindassem a cadeia de suprimentos e o estoque desta categoria.  É notável que qualquer ruptura ou atraso logístico na linha de rações causará um impacto imediato e severo na saúde financeira da empresa. Não há influência de porte de loja na concentração de receita: a categoria "Ração" lidera em todos os portes, com destaque para as lojas pequenas, que apresentam uma dependência ainda maior dessa categoria.

👉 [Ver Tabela Categoria de Evidência da P2](anexos/p2/tabela_faturamento_categoria_porte_p2.txt)
👉 [Ver Gráfico Categoria de Evidência da P2](anexos/p2/grafico_faturamento_categoria_p2.png)


🎯  •	**P3 (Política de Desconto):** *A política de incentivo funciona de forma homogênea em todos os canais de atendimento (App, WhatsApp, Site, Loja Física, Telefone)? Análise comparativa de ticket médio e representatividade financeira.*

Foi realizada consulta SQL & Regra de Negócio: Agrupamento por `canal_pedido`, utilizando condicionais `(CASE WHEN houve_desconto = 1)` para isolar o valor líquido `(vl_liquido)` pago pelo cliente e calcular a representatividade percentual de cada canal sobre o faturamento total da rede. 
Foi possível avaliar a eficiência da política de descontos da rede, comparando o volume de pedidos, o faturamento por canal e o comportamento do ticket médio entre compras com e sem desconto.

  
     🏷️ 📊 Evidência dos Dados

     • O App reina como o principal canal de vendas da rede, respondendo por cerca de 34,18% de todo o faturamento, seguido de perto pelo Site (28,73%) e pela Loja Física (22,43%). 
     • O Efeito do Desconto no Ticket Médio: Em absolutamente todos os canais, o ticket médio das compras que recebem desconto é quase três vezes maior do que o das compras sem desconto.
     • No App: O cliente sem desconto gasta em média R$ 170,48, enquanto o cliente que utiliza a política de descontos atinge um ticket médio líquido de R$ 488,04 (com um volume massivo de 1.542 pedidos).
     • Nos demais canais: O comportamento se repete de forma uniforme, com tickets com desconto variando de R$ 488 a R$ 514, contra cerca de R$ 180 a R$ 196 nas compras regulares sem desconto.
     
    Fato Observável nos Dados (Correlação Volume vs. Desconto):
     • Nos pedidos em que incide desconto, constata-se uma cesta média maior (maior quantidade de itens por pedido ou tíquetes nominais mais elevados). Isso sustenta a leitura de que o desconto atua associado a pedidos volumosos (típico de compras combinadas ou abastecimento), e não apenas como liquidação isolada de itens encalhados.

   O desconto na Pata Amiga não funciona como um "brinde para queimar estoque", mas sim como uma **alavanca estratégica de volume**. A diferença comprova que o benefício incentiva o cliente a encher o carrinho (comportamento típico de combos, como a junção de ração de grande porte + medicamentos). Ainda que perceba-se que não há efeito causal do desconto , pois não temos dados de custo ou margem, assim tickets maiores não demonstram maior rentabilidade ainda que possmos inferir uma certa relação. 
  
   **Recomendação Estratégica**: utilizar análises por canal para validar estes descontos e na falta destes ou inviabilidade, que os canais digitais (App e Site), que concentram até então o coração do negócio, poderiam ter campanhas de incentivo focadas no aplicativo, atrelando o desconto a regras de quantidade mínima de itens para blindar a margem e maximizar a receita por transação, até que se tivesse finalmente, dados suficientes para analisar o desconto e termos resultados completos.

👉 [Ver Tabela Descontos de Evidência da P3](anexos/p3/tabela_desconto_canal_p3.txt)
👉 [Ver Gráfico Descontos de Evidência da P3](anexos\p3\grafico_desconto_canal_p3.png)

---

🎯  •	**P4 (Expansão e Praças):** *Qual praça de atendimento concentra o faturamento, utilizando rateio ponderado por domicílios com pets para evitar duplicação de métricas.*
 
Foi realizada Consulta SQL & Regra de Negócio com utilização de uma tabela ponte `(bridge_loja_praca)` para conectar a `fato_pedido` à `dim_praca` através da `dim_loja`. O faturamento líquido `(vl_liquido)` é multiplicado pelo fator de público proporcional `(b.fator_publico)`, garantindo que a soma total por praça reflita fidedignamente a realidade da rede.
Assim foi possível mapear o faturamento geográfico da rede utilizando um rateio ponderado por domicílios com pets, cruzando os dados de vendas com o potencial de mercado de cada praça sem duplicar métricas.
  
     🏷️ 📊 Evidência dos Dados
     •  A liderança em 1º Lugar (Liderança Absoluta) está no Vale do Itajaí — Concentra R$ 633.746,09 em faturamento rateado (quase o dobro da segunda colocada) e conta com o maior mercado potencial da rede (148.000 domicílios com pets e 1.534 pedidos envolvidos).
     • Em 2º Lugar temos  a Grande Florianópolis com Faturamento rateado de R$ 283.546,75, apoiado por um mercado de 132.000 domicílios com pets (687 pedidos).
     • Nas demais praças temos  Norte Industrial (R$ 175,4 mil), Litoral Sul (R$ 137 mil), Litoral Norte (R$ 128,8 mil), entre outras praças da cobertura regional de Santa Catarina.

#### 💡 Insight de Negócio & Tomada de Decisão
A liderança isolada do Vale do Itajaí não ocorre por acaso. Ela valida a correlação direta entre o maior potencial de mercado mapeado (domicílios com pets) e o maior retorno financeiro efetivo da rede.
A aplicação correta do rateio matemático evitou a inflação de dados nas lojas que atendem a múltiplas regiões, aprovando o domínio da modelagem dimensional avançada (Star Schema + Bridge Table).
A Solução Técnica: A Tabela Ponte (Bridge Table) e o Rateio
Para resolver esse problema sem perder a precisão, utilizamos uma arquitetura avançada de banco de dados chamada Star Schema estendido com uma Tabela Ponte (bridge_loja_praca).

*O Caminho:* O pedido sai da tabela fato (fato_pedido), passa pela dimensão da loja (dim_loja), entra na tabela ponte (bridge_loja_praca) e chega na praça (dim_praca).

*O Fator de Rateio* (fator_publico): A tabela ponte guarda a proporção exata de atendimento. 

👉 [Ver Tabela Faturamento de Evidência da P4](anexos/p4/tabela_faturamento_praca_p4.txt)
👉 [Ver Gráfico Faturamento de Evidência da P4](anexos/p4/grafico_faturamento_praca_p4.png)
👉 [Ver Gráfico 3D Faturamento de Evidência da P4](anexos\p4\grafico_3d_barras_pracas_p4.jpg)

⚠️(*Caso o Gráfico 3D-Faturamento não seja exibido, você poderá acessá-lo direto na pasta anexos/p4)*

---

🎯  •	**P5a(Expansão & Governança)** - *Onde abrir a próxima loja? Ranqueie as lojas por itens POR MIL HABITANTES (numerador na fato, denominador na dimensao), calculado AQUI na consulta - nunca gravado pronto. Cruze com o tempo medio de entrega.*

 Cruzamento de densidade de itens por mil habitantes (itens/mil hab.) com a eficiência logística (tempo médio de entrega).

  
     🏷️ 📊 Evidência dos Dados

     • Para atender ao estudo conforme as diretrizes do projeto, o cálculo de densidade foi realizado utilizando a população do município como denominador e o total de itens faturados como numerador: 
     

>
      >$$\text{Itens por 1.000 hab} = \frac{1000.0 \times \sum \text{qt\_itens}}{\text{populacao\_cidade}}$$

      • Não foram identificados registros de devoluções ou cancelamentos na base consolidada.

     Diagnóstico das Lojas Líderes:
       • Rio dos Cedros: Lidera a rede com 41,87 itens/mil hab. e prazo médio de 14,24 dias (atende áreas do Vale do Itajaí e Norte Industrial).
       • Presidente Getúlio: 2ª colocada, com **34,84 itens/mil hab. e prazo médio de 14,16 dias. 
       • Ibirama: 3ª colocada, com 32,07 itens/mil hab. e prazo médio de 15,39 dias.


 **Onde intervir e onde abrir a próxima unidade:**

 As três primeiras colocadas concentram-se no cluster do Alto Vale do Itajaí e apresentam severo gargalo de entrega (> 14 dias). 

 Dentre as opções de recomendação para esta região a sugestão não é a abertura precipitada de uma segunda loja física em Rio dos Cedros, mas sim a **implantação de um Hub de Distribuição / Ponto de Apoio Logístico regional** para reduzir o lead time pela metade. 

 **O que os dados NÃO podem afirmar (Limitações do DW):**
 1. **Causa da Perda de Vendas:** O modelo estrela registra o tempo de trânsito, mas não armazena o valor do frete cobrado, carrinhos abandonados por custo de envio ou métricas de satisfação. Dizer que clientes deixaram de comprar pelo frete é uma hipótese analítica, não um dado 
 absoluto da tabela.
  2. **Comportamento Estritamente Local:** Como as lojas físicas atendem a múltiplas praças pela tabela de relacionamento, não se pode assumir que os compradores residem exclusivamente dentro dos limites da cidade sede.
 3. **Amostragem de Prazos:** Em Rio dos Cedros, dos 61 pedidos totais, apenas 29 possuem entrega concluída registrada no cálculo do lead time. A taxa de 41,87 itens/1000 hab decorre do divisor populacional reduzido (11.322 hab.), servindo como métrica de intensidade comparativa,
  e não de penetração total de mercado.
 
 **Plano de Ação:**

• Triagem Operacional: Antes de qualquer aporte de capital em novas unidades, analisar a fila de expedição da loja atual e simular o aumento na frequência de rotas terceirizadas. É mandatório confrontar o custo desse ajuste logístico imediato com o investimento de uma nova instalação física.

• Separação entre Rota e Expansão: A aplicação de cortes estatísticos permite distinguir gargalos pontuais de transportadora da real necessidade de expansão geográfica da rede.

• Ponto Cego do Frete e Subsídio: Os dados evidenciam o atraso no tempo de entrega, mas não informam o valor cobrado de frete. Caso a rede já subsidie o frete grátis para regiões como a Serra Catarinense, a abertura de um ponto físico serviria primordialmente para estancar o prejuízo operacional interno da empresa, e não para alterar o preço final percebido pelo consumidor.

• Abordagem Analítica (Cruzamento de Indicadores): Cruzar a densidade de consumo (itens/1.000 hab.) com o tempo médio de entrega para mapear demandas reprimidas por atrito logístico. Na modelagem SQL, aplicar agrupamento por praça/loja com filtro via HAVING (acima da média da rede) para isolar unidades de alta densidade e prazos críticos.


👉 [Ver Tabela Loja Evidência da P5a](anexos/p5/p5a/tabela_ranking_densidade_p5a.txt)
👉 [Ver Gráfico Loja Evidência da P5a](anexos\p5\p5a/grafico_top10_densidade_p5a.png)

---


🎯  •	**P5b:** - *Mostre o faturamento por faixa de franquia e explique por que ele NAO
responde "quanto veio de lojas que JA ERAM Ouro na data do pedido": o cadastro so tem a foto de hoje.*  -  Análise de faturamento por faixa de franquia e reflexão crítica sobre limitações temporais do cadastro atual 


         🏷️  📊 Evidência dos Dados (Resultados Consolidados)

         • 1º Lugar (Liderança em Receita): Faixa Ouro — Acumula R$ 1.011.264,38 em faturamento e um volume expressivo de 2.316 pedidos.
         • 2º Lugar: Faixa Diamante — Faturamento de R$ 382.209,74 (818 pedidos).
         •  3º Lugar: Faixa Prata — Faturamento de R$ 314.812,03 (719 pedidos).
         • Demais Faixas: Bronze (R$ 84.036,06 / 188 pedidos) e registros não informados/órfãos (R$ 986,30).
   
      
**Total da Rede: R$ 1.793.308,51 | 4.044 pedidos**

 *Por que a consulta NÃO responde " o quanto retornou de lojas que JÁ ERAM Ouro na data do pedido"?*
  
   • A dimensão dim_loja foi modelada como SCD Tipo 1 (Slowly Changing Dimension Tipo 1) registrando apenas o estado vigente ("foto atual"). **Não há versionamento histórico**.
 
   • Quando uma unidade atinge metas e sobe de categoria (por exemplo, de Prata para Ouro), seu registro na dimensão é atualizado via sobrescrita. Como a tabela fato (fato_pedido) referencia a mesma sk_loja de forma estática, qualquer agrupamento por faixa_franquia redistribui retroativamente todo o histórico de faturamento passado daquela loja para sua categoria presente.
  
   • Em termos analíticos, a consulta reflete: "Qual é o faturamento acumulado gerado por lojas que HOJE são Ouro", e não "Qual era a receita gerada sob a chancela da faixa Ouro quando as vendas ocorreram".

  

👉 [Ver Tabela Franquia Evidência da P5b](anexos\p5\p5b/tabela_faturamento_franquia_p5b.txt.csv)
👉 [Ver Gráfico Franquia Evidência da P5b](anexos\p5\p5b/grafico_colunas_p5b.png)

---


🎯  •	**P5c:**  - MEDIÇÃO DOS RESÍDUOS (Auditoria de Qualidade)
     
 *Meça o que ficou de fora: pedidos sem loja, entregas não concluidas, itens ou valores em branco e/zerados -  Auditoria rigorosa de qualidade de dados e resíduos (quantificação em volume e percentual de entregas não concluídas, itens em branco, itens sem valor e pedidos sem loja, incluindo o total geral da base).*

      🏷️  📊 Evidência dos Dados 
      (Total: 4.044 pedidos)
      
      • Entregas não concluídas: 1.953 registros, representando 48,29% (base monitorada)
      • Itens em branco: 257 registros, representando 6,36%.
      • Itens sem valor: 121 registros, representando 2,99%.
      • Pedidos sem loja identificada (órfãos): Apenas 3 registros, representando 0,07%
      
   
 A Consulta SQL & Regra de Negócio resultou da Aplicação de contagens condicionais `(COUNT` com filtros lógicos) sobre o universo de 4.044 pedidos da base, avaliando falhas de processo e garantindo que o fechamento financeiro global do rateio geográfico cruze com precisão contábil exata (diferença zero). 
    `Reconciliação = zero`

 
#### 💡 Insight de Engenharia de Dados & Confiabilidade
* **Fechamento Contábil e Arredondamento:** O processo de rateio ponderado por praças envolve divisões proporcionais `(fator_publico)`. Para evitar desvios causados por arredondamentos isolados por linha, a modelagem aplicou o fechamento do saldo global por último.
* **Precisão Técnica:** Essa abordagem garantiu que a soma do faturamento por praça somada aos pedidos órfãos cruzasse exatamente com o faturamento bruto total da rede, zerando qualquer discrepância residual e fechando o escopo de auditoria com perfeição técnica.

👉 [Ver Tabela Auditoria Evidência da P5c](anexos\p5\p5c/tabela_auditoria_residuos_p5c.txt)
👉 [Ver Gráfico Auditoria Evidência da P5c](anexos\p5\p5c\grafico_auditoria_residuos_p5c.png)



## Reconciliação Quantitativa  validação de


⚖️ AUDITORIA DE DADOS 

| Teste Auditado | Obtido | Esperado | Status |
| :--- | :---: | :---: | :---: |
| `stg_pedido` | 4.044 | 4.044 | OK |
| `stg_loja` | 32 | 32 | OK |
| `stg_loja_praca` | 48 | 48 | OK |
| `dim_tempo` | 236 | 236 | OK |
| `dim_loja` | 33 | 33 | OK |
| `dim_categoria` | 38 | 38 | OK |
| `dim_praca` | 13 | 13 | OK |
| `bridge_loja_praca` | 48 | 48 | OK |
| `fato_pedido` | 4.044 | 4.044 | OK |
| Categorias padronizadas | 8 | 8 | OK |
| `sk_loja` nula/órfã | 0 | 0 | OK |
| `sk_categoria` nula/órfã | 0 | 0 | OK |
| `sk_tempo_entrega` nula/órfã | 0 | 0 | OK |
| Pedidos sem loja (`sk_loja = -1`) | 3 | 3 | OK |
| Pedidos sem entrega (`sk_tempo_entrega = -1`) | 1.953 | 1.953 | OK |
| Pedidos via WhatsApp | 414 | 414 | OK |
| Pedidos sem itens (`qt_itens` nulo) | 257 | 257 | OK |
| Pedidos sem valor (`vl_liquido` nulo) | 121 | 121 | OK |




⚖️ AUDITORIA CONTÁBIL E INTEGRIDADE FINANCEIRA:

| Indicador Financeiro / Contábil | Valor Obtido (R$) | Valor de Referência (R$) | Status |
| :--- | :---: | :---: | :---: |
| **Faturamento Total (Staging)** | 1.793.308,51 | 1.793.308,51 |  OK |
| **Faturamento Total (Fato Pedido)** | 1.793.308,51 | 1.793.308,51 |  OK |
| **Faturamento Rateado (Praças)** | 1.792.322,21 | 1.792.322,21 |  OK |
| **Faturamento Sem Lora (`sk_loja = -1`)** | 986,30 | 986,30 |  Auditado |
| **Total Consolidado (Rateio + Sem Loja)** | 1.793.308,51 | 1.793.308,51 |  OK |
| **Divergência / Erro de Reconciliação** | **0,00** | **0,00** |  Zero Dif. |

* O montante bruto faturado de **R$ 1.793.308,51** da camada *staging* foi integralmente absorvido pela `fato_pedido` sem perdas ou duplicaçõe.
* A soma do rateio proporcional aplicado às praças via `bridge_loja_praca` (**R$ 1.792.322,21**) somada aos 3 pedidos sem loja (**R$ 986,30**) reconstrói exatamente o faturamento total da rede, resultando em uma divergência contábil de **R$ 0,00**.

 `Reconciliação = zero`

 ## Validação  - Etapas

 🔒 Diagnóstico Etapa 1 - solicitação da 00-conferencia *(Estes numeros estão no README.)*
 >| Marco de Processamento Logístico | Em Aberto (Campos Vazios) | Esperado (Gabarito) | Status de Validação |
>| :--- | :---: | :---: | :---: |
>| Dt Separacao Estoque** | 1.077 | 1077 |  OK |
>| DtNotaFiscal** | 1.338 | 1338 |  OK |
>| Dt_Despacho_Transportadora** | 1.665 | 1665 |  OK |
>| DtEntregaCliente** | 1.953 | 1953 |  OK |


   🔒 Solicitação 00-conferencia *(apos etapa 3 ESTE e o teste que vale nota, e ele NAO muda de banco para banco).*

> Métrica Auditada | Valor Obtido | Valor Esperado | Status |
>| :--- | :---: | :---: | :---: |
>| **Categorias Padronizadas** | 8 | 8 (7 categorias + linha -1) |  OK |

Consolidação Categórica: As 38 grafias originais mapeadas na staging foram devidamente tratadas por meio da regra condicional (CASE WHEN), consolidando o catálogo em 7 categorias comerciais de negócio somadas ao registro sentinela (sk_categoria = -1).


## Limitações Analíticas 
🏷️ 1. O que os dados NÃO permitem afirmar (Limitações de Inferência):

**Causalidade de Conversão por Praça:** Os dados mostram o volume de itens rateados e a densidade populacional por praça, mas não permitem afirmar que a variação nas vendas ocorreu exclusivamente por falta de interesse do público local. O volume pode ser afetado por fatores externos invisíveis na base, como barreiras logísticas regionais, campanhas de marketing local não tagueadas ou sazonalidades específicas de cada microrrregião.

**Histórico Temporal de Fidelidade de Franquia:** Conforme diagnosticado na P5b (SCD Tipo 1), os dados atuais não permitem afirmar o faturamento exato gerado por lojas que mudaram de categoria no passado, pois a base sobrescreve o status anterior pelo perfil atual.


## Evolução Técnica
✨ O que eu melhoraria no SQL / Arquitetura se tivesse mais tempo:

Implementação de SCD Tipo 2: Substituir o modelo estático (dim_loja atual) por uma modelagem com versionamento temporal e Surrogate Keys (sk_loja), garantindo que a vigência de alteração de faixa de franquia seja preservada com data de início e fim.

Otimização de Performance e CTEs: Refatorar as consultas de rateio complexas (P4 e P5a) utilizando tabelas temporárias indexadas ou Materialized Views para acelerar o tempo de processamento em bases de dados maiores.

Tratamento Automatizado de Nulos/Órfãos: Criar rotinas robustas de data cleansing diretamente nas procedures de carga (ETL) para tratar resíduos como "itens em branco" e "entregas não concluídas" (P5c) antes que cheguem à camada analítica do Data Warehouse.

Para finalizar o projeto, fiz questão de destacar as limitações dos dados — como a restrição do SCD Tipo 1 e a impossibilidade de inferir causalidade direta sem dados de marketing —, além de apontar melhorias arquiteturais que implementaria em um cenário de produção em larga escala."


