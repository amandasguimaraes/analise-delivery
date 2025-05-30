# Análise de Delivery - Curry Company
Este projeto apresenta um dashboard estratégico para a Curry Company, uma empresa de tecnologia que opera sob o modelo de negócio Marketplace, conectando restaurantes e entregadores à demanda de clientes. O objetivo principal deste dashboard é fornecer ao CEO uma visibilidade clara e rápida sobre os principais KPIs de crescimento, combatendo a dor da falta de dados consolidados e interativos. A solução oferece uma visão centralizada da performance dos dois pilares operacionais da empresa: os Restaurantes e os Entregadores, fundamentais para o sucesso do modelo de negócio.

O desenvolvimento deste dashboard seguiu uma abordagem estruturada e orientada a resultados, garantindo que a solução não apenas exibisse dados, mas fornecesse insights acionáveis para o negócio.

####  1. Definição do Problema
O ponto de partida foi a identificação da necessidade do CEO por uma visão consolidada do crescimento. As seguintes perguntas guiaram a coleta de requisitos:

- Quais são os volumes e padrões de pedidos por cidade e densidade de tráfego?
- Como está o desempenho dos entregadores em termos de tempo de entrega, idade e avaliação?
- Como as condições climáticas e o tráfego rodoviário afetam as operações logísticas?
- Qual a distância média das entregas, e isso varia por tipo de veículo?
- Existem diferenças significativas no tempo de entrega durante eventos como festivais?

#### 2. Estruturação e Premissas
Adotamos uma abordagem de "Árvore de Problemas" para desmembrar o desafio e organizar as métricas em visões claras de negócio.

**Premissas:**
- Os dados analisados correspondem ao período de 11/02/2022 a 06/04/2022.
- O modelo de negócio Marketplace é central para todas as análises.
- As análises foram divididas em três Visões Estratégicas: Empresa, Restaurantes e Entregadores.

#### 3. Priorização
Focamos na construção de um conjunto de gráficos e tabelas que pudessem ser rapidamente utilizados pelo CEO para obter insights acionáveis e subsidiar decisões estratégicas, permitindo futuras expansões.

#### 4. Análise e Desenvolvimento Técnico
Esta fase foi crucial para transformar dados brutos em insights significativos:

- **Processamento de Dados (ETL):** Realizamos as etapas de extração (carregamento dos dados brutos), transformação (limpeza, tratamento de valores ausentes, correção de formatos, padronização e enriquecimento dos dados) e carga (preparação para o consumo no dashboard). Isso garantiu alta qualidade e consistência para todas as análises.
- **Cálculo de KPIs e Métricas:** Desenvolvemos lógicas robustas em Python para calcular cada um dos indicadores estratégicos.
- **Construção do Dashboard Interativo:** O Streamlit foi a ferramenta escolhida por sua capacidade de criar interfaces de usuário ricas com poucas linhas de código Python, permitindo a integração fluida de tabelas, gráficos e filtros dinâmicos.
- **Visualização de Dados:** Geramos gráficos interativos e mapas otimizados para cada KPI, focando na clareza visual e na facilidade de interpretação.

#### 5. Apresentação
O dashboard é dividido em três visões principais, acessíveis através da barra lateral, e todas as páginas contam com filtros interativos por data, cidade, tráfego, clima e tipo de veículo.

- **Visão da Empresa:** Foca no desempenho geral da Curry Company.
- **Visão dos Entregadores:** Monitora a performance e características da nossa força de entrega.
- **Visão dos Restaurantes:** Acompanha a performance e o impacto nos restaurantes parceiros.

O painel está hospedado e pode ser acessado online através deste link: [INSERIR O LINK DO DASHBOARD AQUI]

#### Insights
Algumas das descobertas mais relevantes obtidas através do dashboard incluem:

- **Sazonalidade Diária:** A quantidade de pedidos é significativamente afetada pela hora do dia, sugerindo oportunidades para ações táticas como promoções e reforço logístico em picos.
- **Impacto do Trânsito:** O trânsito em áreas semi-urbanas apresenta-se consistentemente de moderado a alto, o que impacta diretamente os tempos de entrega e requer atenção estratégica.
- **Clima e Demanda:** Apesar do clima ensolarado, este apresenta uma maior variância no tempo de entrega, o que pode estar relacionado a picos de maior demanda não linear.

#### Próximos Passos e Melhorias Futuras
Este dashboard é uma ferramenta poderosa, mas há sempre espaço para expansão e aprimoramento:

- **Integração em Tempo Real:** Conectar o dashboard com sistemas internos e APIs logísticas para fornecer insights sobre o fluxo de pedidos e a operação em tempo real.
- **Análise Preditiva:** Desenvolver modelos para prever a demanda de pedidos, o tempo de entrega e a necessidade de entregadores, otimizando a alocação de recursos.
- **Análise Financeira:** Incluir novos dados para análises de custo por pedido, lucratividade por cliente (LTV) e custo de aquisição de cliente (CAC).
- **Integração com Feedback de Clientes:** Incorporar dados de pesquisas de satisfação (NPS/CSAT) e feedback direto para uma visão mais qualitativa do serviço.
- **Alertas Automatizados:** Implementar um sistema de alertas por e-mail para notificar sobre anomalias em KPIs críticos (ex: queda abrupta de pedidos, aumento súbito do tempo de entrega).
