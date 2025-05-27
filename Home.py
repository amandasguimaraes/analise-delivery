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
st.sidebar.markdown('### Developed by @amandasguimaraes')

st.write( "# Curry Company - Growth Dashboard" )
st.empty()       
st.write("\nThis dashboard was created to manage important metrics about marketplace.")
st.markdown('''---''')
st.markdown(
   
    """
    ### How to use this Growth Dashboard?
    Explore the different views of our business through the pages in the side menu:
    - Company Vision:
        - Management View: Overall metrics.
        - Tactical View: Weekly statistics.
        - Geographic View: Geolocation insights.
    - Delivery Vision:
        - Monitoring weekly growth indicators.
    - Restaurant Vision:
        - Weekly restaurant growth indicators.
""" )