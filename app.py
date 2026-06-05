import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
# On importe ta fonction de détection
from fraud_detection import detect_fraud

st.set_page_config(page_title="Système de Détection de Fraude", layout="wide")
st.title("🛡️ Plateforme Anti-Fraude — Hackathon INTELO2026")

# Création des 3 onglets demandés dans ton TP
tab1, tab2, tab3 = st.tabs(["✍️ Saisie de Données (Data Entry)", "🔍 Analyse (Analysis)", "📊 Tableau de Bord (Dashboard)"])

# ---------------------------------------------------------
# ONGLET 1 : SAISIE DE DONNÉES
# ---------------------------------------------------------
with tab1:
    st.header("Enregistrement d'une nouvelle transaction")
    st.write("Entrez les détails de la transaction pour analyser le risque de fraude instantanément.")
    
    with st.form("transaction_form"):
        col1, col2 = st.columns(2)
        with col1:
            amount = st.number_input("Montant de la transaction (€)", min_value=0.0, value=50.0)
            location = st.text_input("Lieu de la transaction", value="Lomé")
        with col2:
            time_input = st.time_input("Heure de la transaction", value=datetime.now().time())
            device = st.selectbox("Type d'appareil", ["Mobile", "Ordinateur", "Distributeur"])
            
        submitted = st.form_submit_button("Analyser la transaction")
        
        if submitted:
            # Simulation d'un dictionnaire de transaction pour ton algo
            current_hour = time_input.hour
            
            # Appel de ta fonction
            # 1. On crée une fausse transaction au format attendu par ton algo
            fake_transaction = {
                'amount': amount,
                'hour': current_hour,
                'location': location
            }
            
            # 2. On la met dans une liste car ton algo attend une liste [transactions]
            # Et on récupère le résultat
            resultat = detect_fraud([fake_transaction])
            
            # 3. Gestion de l'affichage selon ce que renvoie ton algo
            # (Par sécurité, on extrait la réponse)
            is_fraud = False
            level = 0
            
            if isinstance(resultat, tuple):
                is_fraud = resultat[0]
                level = resultat[1] if len(resultat) > 1 else 1
            elif isinstance(resultat, bool):
                is_fraud = resultat
            
            st.write("---")
            if is_fraud:
                st.error(f"🚨 Alerte Fraude Détectée ! (Niveau {level})")
                st.warning("Comportement suspect détecté par l'algorithme.")
            else:
                st.success("✅ Transaction légitime. Aucun comportement suspect détecté.")
            if is_fraud:
                st.error(f"🚨 Alerte Fraude Détectée ! (Niveau {level})")
                st.warning(f"Raison : {msg}")
            else:
                st.success("✅ Transaction légitime. Aucun comportement suspect détecté.")

# ---------------------------------------------------------
# ONGLET 2 : ANALYSE
# ---------------------------------------------------------
with tab2:
    st.header("Espace d'Analyse des Transactions")
    st.write("Filtrez et analysez l'historique des transactions suspectes.")
    
    # Simulation de données pour l'analyse
    data = pd.DataFrame({
        'ID': range(1, 6),
        'Utilisateur': ['User_A', 'User_B', 'User_C', 'User_D', 'User_E'],
        'Montant (€)': [12000, 45, 2500, 80, 9500],
        'Heure': [2, 14, 23, 10, 3],
        'Lieu': ['Paris', 'Lomé', 'New York', 'Lomé', 'Inconnu'],
        'Statut': ['Fraude Niveau 2', 'Normal', 'Fraude Niveau 1', 'Normal', 'Fraude Niveau 2']
    })
    
    status_filter = st.multiselect("Filtrer par statut :", options=data['Statut'].unique(), default=data['Statut'].unique())
    filtered_data = data[data['Statut'].isin(status_filter)]
    st.dataframe(filtered_data, use_container_width=True)

# ---------------------------------------------------------
# ONGLET 3 : TABLEAU DE BORD
# ---------------------------------------------------------
with tab3:
    st.header("Tableau de Bord Global")
    
    # Métriques flash
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric(label="Total Analysé", value="1,245", delta="12% ce jour")
    kpi2.metric(label="Fraudes Bloquées", value="34", delta="Niveau 1 & 2", delta_color="inverse")
    kpi3.metric(label="Taux de Fraude", value="2.7%", delta="-0.4%")
    
    # Un petit graphique visuel avec Plotly
    st.write("---")
    st.subheader("Répartition des alertes par niveau de gravité")
    chart_data = pd.DataFrame({
        'Catégorie': ['Normal', 'Fraude Niveau 1', 'Fraude Niveau 2'],
        'Nombre': [1211, 24, 10]
    })
    fig = px.bar(chart_data, x='Catégorie', y='Nombre', color='Catégorie', color_discrete_sequence=["#2ecc71", "#e67e22", "#e74c3c"])
    st.plotly_chart(fig, use_container_width=True)
