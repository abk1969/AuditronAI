import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

def show_stats_page(history, usage_stats):
    """Affiche la page des statistiques."""
    st.title("📊 Statistiques d'utilisation")
    
    # Métriques globales
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total analyses", usage_stats.stats['total_analyses'])
    with col2:
        st.metric("Erreurs", usage_stats.stats['errors'])
    with col3:
        success_rate = ((usage_stats.stats['total_analyses'] - usage_stats.stats['errors']) 
                       / max(1, usage_stats.stats['total_analyses']) * 100)
        st.metric("Taux de succès", f"{success_rate:.1f}%")
    
    # Graphique des analyses par jour
    analyses_by_date = pd.DataFrame.from_dict(
        usage_stats.stats['analyses_by_date'],
        orient='index',
        columns=['count']
    )
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=analyses_by_date.index,
        y=analyses_by_date['count'],
        name="Analyses"
    ))
    
    fig.update_layout(
        title="Analyses par jour",
        xaxis_title="Date",
        yaxis_title="Nombre d'analyses",
        template="plotly_dark"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Historique récent
    st.subheader("Analyses récentes")
    recent_entries = history.get_entries(limit=10)
    
    if recent_entries:
        for entry in recent_entries:
            with st.expander(f"📄 {entry['file']} - {entry['timestamp']}"):
                st.json(entry['stats'])
                st.markdown("### Analyse")
                st.markdown(entry['analysis'])
    else:
        st.info("Aucune analyse dans l'historique") 