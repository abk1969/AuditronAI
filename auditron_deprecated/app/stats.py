import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path
import json
from .navigation import show_stats_navigation

def load_analysis_history():
    """Charge l'historique des analyses."""
    history_file = Path("datasets") / "analysis_history.json"
    if not history_file.exists():
        return []
    
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_analysis_history(history):
    """Sauvegarde l'historique des analyses."""
    history_file = Path("datasets") / "analysis_history.json"
    history_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2)

def add_to_history(analysis_result: dict):
    """Ajoute une analyse à l'historique."""
    history = load_analysis_history()
    
    history.append({
        "timestamp": datetime.now().isoformat(),
        "file": analysis_result["file"],
        "stats": analysis_result["stats"],
        "service": st.session_state.get('current_service', 'openai')
    })
    
    # Garder seulement les 100 dernières analyses
    if len(history) > 100:
        history = history[-100:]
    
    save_analysis_history(history)

def show_overview_stats(df: pd.DataFrame):
    """Affiche les statistiques générales."""
    st.subheader("📊 Vue d'ensemble")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total analyses", len(df))
    with col2:
        st.metric("Fichiers uniques", df['file'].nunique())
    with col3:
        st.metric("Services utilisés", df['service'].nunique())
    with col4:
        avg_lines = df['stats'].apply(lambda x: x['Lignes de code']).mean()
        st.metric("Moy. lignes/fichier", f"{avg_lines:.1f}")

def show_temporal_analysis(df: pd.DataFrame):
    """Affiche l'analyse temporelle."""
    st.subheader("📈 Analyse temporelle")
    
    # Analyses par jour
    daily_counts = df.groupby(df['timestamp'].dt.date).size()
    fig = go.Figure(data=[
        go.Bar(x=daily_counts.index, y=daily_counts.values)
    ])
    fig.update_layout(
        title="Analyses par jour",
        xaxis_title="Date",
        yaxis_title="Nombre d'analyses"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Tendance horaire
    hourly_counts = df.groupby(df['timestamp'].dt.hour).size()
    fig = go.Figure(data=[
        go.Scatter(x=hourly_counts.index, y=hourly_counts.values, mode='lines+markers')
    ])
    fig.update_layout(
        title="Distribution horaire des analyses",
        xaxis_title="Heure",
        yaxis_title="Nombre d'analyses"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_service_comparison(df: pd.DataFrame):
    """Affiche la comparaison des services."""
    st.subheader("🔄 Comparaison des services")
    
    # Distribution des services
    service_counts = df['service'].value_counts()
    fig = go.Figure(data=[
        go.Pie(
            labels=service_counts.index,
            values=service_counts.values,
            hole=.3
        )
    ])
    fig.update_layout(title="Utilisation des services AI")
    st.plotly_chart(fig, use_container_width=True)
    
    # Temps moyen par service
    service_times = df.groupby('service')['timestamp'].agg(['count', 'min', 'max'])
    st.dataframe(service_times)

def show_code_metrics(df: pd.DataFrame):
    """Affiche les métriques de code."""
    st.subheader("📏 Métriques de code")
    
    # Distribution des tailles de fichiers
    lines_dist = df['stats'].apply(lambda x: x['Lignes de code'])
    fig = go.Figure(data=[
        go.Histogram(x=lines_dist, nbinsx=20)
    ])
    fig.update_layout(
        title="Distribution des tailles de fichiers",
        xaxis_title="Lignes de code",
        yaxis_title="Nombre de fichiers"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_detailed_history(df: pd.DataFrame):
    """Affiche l'historique détaillé."""
    st.subheader("📜 Historique détaillé")
    
    # Filtres
    col1, col2 = st.columns(2)
    with col1:
        service_filter = st.multiselect(
            "Service",
            options=df['service'].unique()
        )
    with col2:
        date_range = st.date_input(
            "Période",
            value=(df['timestamp'].min().date(), df['timestamp'].max().date())
        )
    
    # Appliquer les filtres
    filtered_df = df.copy()
    if service_filter:
        filtered_df = filtered_df[filtered_df['service'].isin(service_filter)]
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['timestamp'].dt.date >= date_range[0]) &
            (filtered_df['timestamp'].dt.date <= date_range[1])
        ]
    
    # Afficher les résultats
    st.dataframe(
        filtered_df[['timestamp', 'file', 'service']].sort_values('timestamp', ascending=False),
        use_container_width=True
    )

def show_statistics_page():
    """Affiche la page des statistiques."""
    st.title("📊 Statistiques d'analyse")
    
    history = load_analysis_history()
    if not history:
        st.warning("Aucune analyse n'a encore été effectuée.")
        return
    
    # Convertir l'historique en DataFrame
    df = pd.DataFrame(history)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Navigation des statistiques
    stats_page = show_stats_navigation()
    
    # Afficher la page sélectionnée
    if stats_page == "Vue d'ensemble":
        show_overview_stats(df)
    elif stats_page == "Analyse temporelle":
        show_temporal_analysis(df)
    elif stats_page == "Comparaison des services":
        show_service_comparison(df)
    elif stats_page == "Métriques de code":
        show_code_metrics(df)
    else:  # Historique détaillé
        show_detailed_history(df)
    
    # Option de téléchargement toujours disponible
    st.sidebar.markdown("---")
    if st.sidebar.button("📥 Exporter les données"):
        csv = df.to_csv(index=False)
        st.sidebar.download_button(
            label="Confirmer l'export",
            data=csv,
            file_name="historique_analyses.csv",
            mime="text/csv"
        ) 