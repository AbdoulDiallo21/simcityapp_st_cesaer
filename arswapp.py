import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import simul_model as simul
import base64
import plotly.graph_objects as go
import plotly.subplots as sp
import pyautogui



def run_model_app():
    # Definition value parameter
    st.sidebar.header("Définir vos paramètres")
    a =st.sidebar.slider("$\\alpha$: Part du bâti dans la fonction de production des firmes", 0.0, 1.0, 0.2, step=0.01)
    b =st.sidebar.slider('$\\beta$: Part du logement dans la dépense des ménages', 0.0, 1.0, 0.3, step=0.01)
    e =st.sidebar.number_input("$\epsilon$: Paramètre dispersion de la distribution des termes d'erreur", 1.0,10000000.0,7.0)
    t =st.sidebar.number_input("$\\tau$: Paramètre désutilité distance dans choix de localisation", 1.0,10000000.0,1.2)
    m =st.sidebar.number_input("$\mu$ : Elasticité prix de l'offre de logements", 0.0,10000000.0,1.0)
    lr =st.sidebar.number_input("lr: Intensité des effets d'agglomération pour les aménités résidentielles", 0.0,1000000000.0,0.3)
    dr =st.sidebar.number_input("dr: Atténuation spatiale effets d'agglo aménités résidentielles", 0.0,10000000.0, 0.5)
    lm =st.sidebar.number_input("lm: Intensité des effets d'agglo productivité des firmes", 0.0,1000000000.0,0.03)
    dm =st.sidebar.number_input("dm: Atténuation spatiale des effets d'agglo productivité des firmes", 0.0,1000000000.0,0.3)
    HT =st.sidebar.number_input("H: Population totale", 1.0,1000000000.0,1e6)

    # Dictionnaire par 
    par={'a' : a, 'b' : b, 'e':e,'t' : t, 'm' : m, 'lr' : lr, 'dr' : dr,'lm':lm,'dm':dm,'HT':HT}
    # Definition matrice: Fake city on a SxS grid
    S = 21
    J = S**2
    # Vector inputs: set everything to one
    inputs = np.ones((J,4))

    # ajouter oprion edit matrice
    st.markdown("""
                🎈Avant de lancer la prédiction, vous pouvez modifier les valeurs de la matrice en cliquant sur **Éditer**
                    ou sinon vous pouvez directement aller sur **Predict value**.
                """)
    # Afficher l'éditeur de données
    if st.button("Éditer"):
        inputs = st.data_editor(inputs, key="matrix_editor")
    #     st.write(inputs)
    #ajout donload csv
    # ou editer les valeurs pour la matrice (page d'acceuil)
    # Distances
    # Start by creating a matrix of coordinates.
    coords = np.zeros((J,2))
    coords[:,0] = np.floor((np.arange(J))/S)
    coords[:,1] = (np.arange(J) - (coords[:,0])*S)
    
    # Then create the matrix of distances
    dx = np.subtract.outer(coords[:,0], coords[:,0])
    dy = np.subtract.outer(coords[:,1], coords[:,1])
    d  = np.sqrt( np.subtract.outer(coords[:,0], coords[:,0])**2 + 
        np.subtract.outer(coords[:,1], coords[:,1])**2)
    
    # Start w/ random populations
    H_0 = np.random.rand(J,J)
    H_0 = H_0 * par['HT'] / H_0.sum()
    
    st.markdown("""
            > - **Pour afficher les résultats, vous devez cliquer sur Predict value**
               """)
    if st.button("Predict value"):
        st.text("Valeurs choisies")
        st.write(par)
        H, Q, w, A, B, trace = simul.simsim(par, inputs, d, H_0)
        st.markdown("***")
        t = []
        t.extend(range(0, len(trace)))
        st.subheader("Courbe de convergence")
        fig1 = px.scatter(x=t, y=np.log(trace), labels={"x": "Temps", "y": "Erreur"})
        fig1.update_layout(
        title=dict(text="Convergence", x=0.5, y=0.9),
        xaxis=dict(title="Temps", showline=True, showgrid=False),
        yaxis=dict(title="Erreur", showline=True, showgrid=False),
        showlegend=False,
        hovermode="closest"
        )
        st.plotly_chart(fig1)
        st.markdown("***")
        st.subheader("Valeurs")
        #ajout fig2

        fig2 = sp.make_subplots(rows=2, cols=3, shared_xaxes=True, shared_yaxes=True,
                        subplot_titles=["Workforce", "Residents", "Wage", "Rent", "A", "B"])
        S = int(np.sqrt(J))
        # Ajouter les graphiques à la figure
        fig2.add_trace(go.Heatmap(z=np.reshape(H.sum(0), (S, S)), colorscale='viridis', showscale=False), row=1, col=1)
        fig2.add_trace(go.Heatmap(z=np.reshape(H.sum(1), (S, S)), colorscale='viridis',showscale=False), row=1, col=2)
        fig2.add_trace(go.Heatmap(z=np.reshape(w, (S, S)), colorscale='viridis',showscale=False), row=1, col=3)
        fig2.add_trace(go.Heatmap(z=np.reshape(Q, (S, S)), colorscale='viridis',showscale=False), row=2, col=1)
        fig2.add_trace(go.Heatmap(z=np.reshape(A, (S, S)), colorscale='viridis',showscale=False), row=2, col=2)
        fig2.add_trace(go.Heatmap(z=np.reshape(B, (S, S)), colorscale='viridis', showscale=False), row=2, col=3)

        for i in range(1, 7):
            for j in range(1,4):
                fig2.update_xaxes(tickvals=[], row=i, col=j)
                fig2.update_yaxes(tickvals=[], row=i, col=j)
            #fig2.update_xaxes(tickvals=[], row=i, col=2)
            #fig2.update_yaxes(tickvals=[], row=i, col=2)
        # Afficher la figure avec Streamlit
        st.plotly_chart(fig2, use_container_width=False)
        # ajout export csv H, et Q, W, A,B concat csv
        
        H_df = pd.DataFrame(H)
        Q_df = pd.DataFrame(Q)
        w_df = pd.DataFrame(w)
        A_df = pd.DataFrame(A)
        B_df = pd.DataFrame(B)
        trace_df = pd.DataFrame(trace)

        H_df.to_csv('H.csv', index=False)
        Q_df.to_csv('Q.csv', index=False)
        w_df.to_csv('w.csv', index=False)
        A_df.to_csv('A.csv', index=False)
        B_df.to_csv('B.csv', index=False)
        
        trace_df.to_csv('trace.csv', index=False)

        # Export fichier CSV
        st.markdown("***")
        st.subheader("Exportez les résultats au format csv")

        def create_download_link(df, title, filename):
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">{title}</a>'
            return href

        col1, col2, col3 = st.columns(3)

        col1.markdown(create_download_link(H_df, "H", "H"), unsafe_allow_html=True)
        col2.markdown(create_download_link(Q_df, "Q", "Q"), unsafe_allow_html=True)
        col3.markdown(create_download_link(w_df, "w", "w"), unsafe_allow_html=True)

        col1.markdown(create_download_link(A_df, "A", "A"), unsafe_allow_html=True)
        col2.markdown(create_download_link(B_df, "B", "B"), unsafe_allow_html=True)
        col3.markdown(create_download_link(trace_df, "trace", "trace"), unsafe_allow_html=True)

    st.markdown("***")
       
    st.markdown("""
    Pour rénitialiser tout à zéro, vous devez cliquez sur **Reset** ou vous entrez **ctrl+F5**.
    """)
    if st.button("Reset",type="primary"):
        pyautogui.hotkey("ctrl","F5")

    st.markdown("***")


       
      

       



