import streamlit as st
from PIL import Image

from pandas import read_csv
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
from pandas.plotting import scatter_matrix

# Cette app est fait pour analyser et visualiser les données de vente de l’entreprise Beans & Pods.


st.sidebar.title('Beans & Pods')
# Navbar
menu = st.sidebar.selectbox('Navigation', ['Accueil', 'Visualisation', 'Analyse', 'Stratégies et recommandations', 'À propos'])

st.markdown(
        """
        <div style='text-align: center'>
            <h1 style='color:blue' > Analyse des données de vente </h1>
            
        </div>

        """, unsafe_allow_html=True
    )
#------------------------------------------------------
# Chargement des données
try:
    fichier = 'data/BeansDataSet.csv'
    data = read_csv(fichier)
except:
    st.write("Erreur 500: Fichier non trouvé")

#------------------------------------------------------
# Page d'acceuill

if menu == 'Accueil':
    st.write("## Introduction")
    st.write("Cette application est une analyse des données de vente de l’entreprise Beans & Pods.")

    st.write("#### Si vous voulez visualiser les données, veuillez choisir Visualisation dans le menu de gauche.")

elif menu == 'Visualisation':
    st.write("## Nos données")
    
    st.write(data.head())
    # Filtres pour sélectionner le canal de vente (store/online) et la région (North, Center, South)
    canal = st.selectbox('Canal de vente', data['Channel'].unique())
    region = st.selectbox('Region', data['Region'].unique())

    # Filtrage des données
    data_filtre = data[(data['Channel'] == canal) & (data['Region'] == region)]
    st.write(data_filtre)
    
    #Graphiques pour analyser les ventes par catégorie de produits (Robusta, Arabica, Espresso, Lungo, Latte, Cappuccino)
    st.write("## Analyse des ventes par catégorie de produits")

    # Sélection des colonnes de ventes des différents produits
    categories = ['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']
    ventes_par_categorie = data_filtre[categories].sum()

    # Repartition des produits
    fig, ax = plt.subplots()
    ventes_par_categorie.plot(kind='bar', ax=ax, color=['brown', 'green', 'black', 'orange', 'beige', 'chocolate'])
    ax.set_title('Total des ventes par catégorie de produits')
    ax.set_ylabel('Nombre de ventes')
    ax.set_xlabel('Type de produit')

    st.pyplot(fig)

    # # Affichage d'un graphique en camembert
    # fig, ax = plt.subplots()
    # ventes_par_categorie.plot(kind='pie', autopct='%1.1f%%', ax=ax)
    # ax.set_title('Répartition des ventes par catégorie')
    # st.pyplot(fig)
elif menu == 'Analyse' :
    
    st.write("## Analyse des tendances de ventes")

    # Sélection des ventes par catégorie
    categories = ['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']
    
    # Comparaison Store vs Online
    st.write("### Store vs Online")
    ventes_par_canal = data.groupby('Channel')[categories].sum()

    fig, ax = plt.subplots(figsize=(8, 5))
    ventes_par_canal.T.plot(kind='bar', ax=ax)
    ax.set_title('Comparaison des ventes par canal (Store vs Online)')
    ax.set_ylabel('Nombre de ventes')
    st.pyplot(fig)

    # Produits les plus vendus et ceux qui se vendent le moins
    st.write("### Produits le plus et moins vendus")
    ventes_totales = data[categories].sum()

    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### Produits les plus vendus")
        st.write(ventes_totales.head(3))

        fig, ax = plt.subplots()
        ventes_totales.head(3).plot(kind='bar', ax=ax, color=['gold', 'silver', 'brown'])
        ax.set_title('Produits les plus vendus')
        st.pyplot(fig)

    with col2:
        st.write("#### Produits les moins vendus")
        st.write(ventes_totales.tail(3))

        fig, ax = plt.subplots()
        ventes_totales.tail(3).plot(kind='bar', ax=ax, color=['red', 'orange', 'yellow'])
        ax.set_title('Produits les moins vendus')
        st.pyplot(fig)

elif menu == 'Stratégies et recommandations':
    
    st.write("## 📢 Stratégies et recommandations marketing")

    st.write("### 🎯 Suggestions pour améliorer les ventes")
    st.markdown("""
    - **Miser sur les produits les plus vendus** 🏆 : Augmenter la production et la promotion des produits ayant le plus de succès (ex: Arabica, Espresso).
    - **Booster les ventes des produits moins populaires** 📉 : Réductions, offres groupées ou campagnes publicitaires pour les produits moins vendus (ex: Latté, Cappuccino).
    - **Optimisation des stocks** 🏪 : Ajuster les niveaux de stocks en fonction des tendances de vente par région.
    """)

    st.write("### 📊 Idées de campagnes marketing ciblées")
    st.markdown("""
    - **Publicité locale par région** 📍 : Identifier les régions où certains produits se vendent mieux et cibler les campagnes en conséquence.
    - **Offres spéciales pour les clients en ligne** 💻 : Réductions et promotions pour inciter plus d’achats en ligne.
    - **Programme de fidélité** 🎁 : Récompenser les clients réguliers avec des remises et des offres exclusives.
    - **Collaboration avec influenceurs** 📱 : Travailler avec des influenceurs spécialisés dans le café pour toucher une plus grande audience.
    """)

    st.write("### 🔍 Données supplémentaires à collecter pour des analyses futures")
    st.markdown("""
    - **Données clients** 👤 : Collecter des informations anonymes sur les clients (âge, préférences, historique d’achat).
    - **Périodes d’achat** ⏳ : Ajouter un suivi des dates d’achat pour mieux analyser l’évolution des ventes sur le temps.
    - **Feedbacks clients** 📝 : Intégrer des sondages pour comprendre les attentes et préférences des consommateurs.
    - **Analyse des abandons de panier** 🛒 : Étudier pourquoi certains clients abandonnent leur achat en ligne avant paiement.
    """)

    st.write("💡 **Ces recommandations aideront Beans & Pods à optimiser ses ventes et ses stratégies marketing !** 🚀")

elif menu == 'À propos':
    st.write("## ℹ️ À propos du projet")

    st.write("### 📖 Explication de la démarche")
    st.markdown("""
    Ce projet a été réalisé dans le cadre de l'analyse des ventes de **Beans & Pods**.
    
    L'objectif était de :
    - Explorer et visualiser les données de ventes pour identifier des tendances.
    - Comparer les ventes entre magasins physiques et en ligne.
    - Proposer des stratégies pour optimiser le marketing et les ventes.
    - Fournir des recommandations sur les données à collecter à l’avenir.
    """)

    st.write("### 🔗 Lien vers le dépôt GitHub")
    st.markdown("[👉 Accéder au code source sur GitHub]()", unsafe_allow_html=True)

    st.write("### 👨‍💻 Auteur du projet et contact")
    st.markdown("""
    - **Nom** : Yassine Larhrib
    - **Email** : Larhrib.yassine01@gmail.com
    - **Institut** : Teccart
    """)

    st.write("💡 **Merci d'avoir utilisé cette application !** 🚀")






    

