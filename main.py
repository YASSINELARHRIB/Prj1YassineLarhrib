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
    st.subheader("Description des données :")
    descr=data.describe().round(2)
    st.dataframe(descr, width=1000)
    #---------------
    st.subheader("Etude de correlation :")
    correlation=data.select_dtypes(include='number').corr().round(2)
    st.dataframe(correlation, width=1000)
    #---------------
    st.subheader("Carte de chaleur :")
    fig,ax=plt.subplots(figsize=(10,10))
    sns.heatmap(correlation,annot=True,cmap='coolwarm',fmt='.2f')
    plt.suptitle("Carte de chaleur", fontsize=16)
    st.pyplot(fig)
    #---------------
    st.subheader("Boite a moustache :")
    fig,ax=plt.subplots(figsize=(10,10))
    sns.boxplot(data=data,ax=ax)
    plt.suptitle("Boite a moustache", fontsize=16)
    st.pyplot(fig)
    #---------------
    st.subheader("Histogramme :")
    fig, ax = plt.subplots(2, 3, figsize=(10, 10))  # Adjusted to 2x3 grid for 6 plots
    data.hist(bins=15, ax=ax, rwidth=0.8, color='skyblue', edgecolor='black')
    plt.suptitle("Histogramme", fontsize=16)
    st.pyplot(fig)
    #---------------
    st.subheader("Matrice de dispersion :")
    fig, ax = plt.subplots(figsize=(15, 10))
    scatter_matrix(data, ax=ax, color='g')
    plt.suptitle("Matrice de dispersion", fontsize=22)
    st.pyplot(fig)
    #---------------
    st.subheader("Matrice de dispersion par la variable channel :")
    fig = sns.pairplot(data, hue='Channel')
    fig.fig.suptitle("Matrice de dispersion", fontsize=26)
    fig.fig.tight_layout()
    fig.fig.subplots_adjust(top=0.95)
    st.pyplot(fig)
   
    # Affichage d'un graphique en camembert
    fig, ax = plt.subplots()
    ventes_par_categorie.plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_title('Répartition des ventes par catégorie')
    st.pyplot(fig)

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

elif menu == 'Analyse' :
    st.markdown("""
    ### 1. Analyse de données
    ### Distribution Channel et Région
    - **Channel de vente** : 142 ventes proviennent de la plateforme Online, tandis que 298 proviennent de Store. Cela montre une préférence pour les ventes en magasin.
    - **Région** : La majorité des ventes proviennent de la région South (316), suivie de North (77) et Central (47). Cela pourrait indiquer une présence ou une popularité plus forte dans le Sud.

    ### Statistiques par Produit
    Voici les statistiques par type de café pour mieux comprendre leur popularité :
    - Les ventes moyennes et les écarts types pour chaque type de café.
    - Espresso et Robusta semblent être les produits les plus vendus, tandis que Latte et Cappuccino ont des ventes plus faibles.

    ### 2. Recherche de Modèles et Tendances
    #### Analyse par Channel
    En comparant les ventes moyennes de chaque produit pour les canaux Online et Store, nous pourrions observer des tendances telles que :
    - Espresso et Robusta sont populaires en magasin, probablement en raison de la préférence pour les produits prêts à emporter.
    - Lungo est davantage vendu en ligne, ce qui peut suggérer une préférence pour les produits plus spécifiques ou de niche dans ce canal.

    #### Corrélations Entre les Produits
    En examinant la matrice de corrélation, nous observons des corrélations notables entre certains types de café :
    - Espresso et Latte montrent une corrélation positive. Cela pourrait signifier que les clients qui achètent l'un sont également intéressés par l'autre, ce qui peut être exploité pour des offres combinées.
    """, unsafe_allow_html=True)
    

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
    st.markdown("[👉 Accéder au code source sur GitHub](https://github.com/YASSINELARHRIB/Prj1YassineLarhrib.git)", unsafe_allow_html=True)

    st.write("### 👨‍💻 Auteur du projet et contact")
    st.markdown("""
    - **Nom** : Yassine Larhrib
    - **Email** : Larhrib.yassine01@gmail.com
    - **Institut** : Teccart
    """)

    st.write("💡 **Merci d'avoir utilisé cette application !** 🚀")






    

