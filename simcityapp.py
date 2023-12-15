# Importation des packages
import numpy as np
import matplotlib as plt
import seaborn as sns
import streamlit as st
import streamlit.components.v1 as stc
from PIL import Image

from arswapp import run_model_app
#Habillage titre
HTML_BANNER = """
    <div style="background-color:#00a3a6;padding:6px;border-radius:6px">
    <h1 style="color:white;text-align:center;">QSExplorer</h1>
    </div>
    """

#Structure de l'application
def main():
    menu=["Model1","Model2","Model3"]
    st.sidebar.image("logo_inrae.png", use_column_width=True, width=100)
    st.sidebar.header("Choisir un modèle")
    choice=st.sidebar.selectbox("Models",menu)

    #Ajout du logo pour les pages en le centrant
    col1, col2, col3 = st.columns(3)
    with col1:
         st.write("")
    with col2:
        st.image("city.jpg", use_column_width=True, width=200, caption="A-Digit Crédits : Getty Images")
    with col3:
        st.write("")
    st.markdown("***")
    #st.title(":blue[QSExplorer]")
    stc.html(HTML_BANNER)
    st.markdown("""
            >> - **By Morgan UBEDA, Abdoul DIALLO**
            >> - **UMR CESAER 2023 (INRAE, INSTITUT AGRO DIJON)**
               """)
    st.markdown("***")
    st.markdown("""
            > Cette application met en oeuvre le modèle développé par par Ahlfeldt, G. M., Redding, S. J., Sturm, D. M., & Wolf, N. (2015)
            > et il s'agit d'un modèle quantitatif sur la structure interne de la ville qui présente des forces d'agglomération et de dispersion 
            et un nombre arbitraire d'îlots hétérogènes. Vous retrouverez l'article publié par les auteurs sur ce lien https://onlinelibrary.wiley.com/doi/abs/10.3982/ECTA10876
               """)
    st.markdown("***")
    if choice=="Model1":
        run_model_app()
    elif choice=="Model2":
        pass
    elif choice=="Model3":
        pass

if __name__=='__main__':
    main()