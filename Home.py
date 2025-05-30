import streamlit as st
from PIL import Image

st.set_page_config( 
    page_title="Home"
)

image = Image.open('assets/logo.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown( '# Curry Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( """---""" )

st.write( "# Curry Company - Growth Dashboard" )
st.empty()       
st.write(
    "Bem-vindo ao painel de controle estratégico da Curry Company, uma empresa de tecnologia no setor de Marketplace."
    "O objetivo é conectar restaurantes, entregadores e clientes de forma eficiente, garantindo a **entrega mais rápida da cidade**."
)
st.write(
    "Este dashboard foi cuidadosamente desenvolvido para fornecer insights estratégicos e táticos, apoiando o CEO na tomada de decisões baseadas em dados para impulsionar o crescimento contínuo da operação de delivery."
)
st.markdown("---")
st.markdown(

    """
    ### Como utilizar este painel?
    Explore as diferentes visões estratégicas disponíveis no **menu lateral** (à esquerda) para mergulhar nos dados:

    - ### **Visão da Empresa:**
        - **Visão Gerencial:** Métricas sobre o comportamento geral da demanda e da operação.
        - **Visão Tática:** Análise da evolução semanal de indicadores críticos de logística e performance.
        - **Visão Geográfica:** Insights sobre a distribuição geográfica das entregas, identificando áreas de maior volume ou desafio.

    - ### **Visão dos Entregadores:**
        - **Desempenho Individual:** Acompanhe a performance média dos nossos entregadores, avaliando tempos de entrega e condições que os afetam (tráfego, clima).
        - **Demografia e Avaliações:** Entenda o perfil da força de entrega e como as avaliações se distribuem.

    - ### **Visão dos Restaurantes:**
        - **Métricas de Performance:** Monitore o tempo de preparação e entrega dos pedidos por restaurante, cidade e tipo de pedido.
        - **Impacto de Eventos:** Analise como eventos especiais (como festivais) afetam os tempos de entrega.
""")

st.markdown( """---""" )
st.write(
    "Lembre-se que todas as páginas do dashboard possuem **filtros interativos** na barra lateral."
    " Você pode refinar sua análise por:"
)
st.markdown(
    """
    - **Período:** Selecione o intervalo de tempo desejado.
    - **Cidade:** Escolha as cidades de interesse.
    - **Condição de Tráfego:** Filtre por densidade de tráfego.
    - **Condição Climática:** Analise o impacto do clima.
    - **Tipo de Veículo:** Compare a performance de diferentes modais de transporte.
    """
)
