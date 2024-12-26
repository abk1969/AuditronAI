import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any

def show_severity_chart(severity_counts: Dict[str, int]):
    """Affiche un graphique des sévérités."""
    colors = {
        'critical': '#ff4444',
        'high': '#ff8800',
        'medium': '#ffbb33',
        'low': '#00C851'
    }
    
    fig = go.Figure()
    
    for severity, count in severity_counts.items():
        fig.add_trace(go.Bar(
            name=severity.capitalize(),
            x=[severity],
            y=[count],
            marker_color=colors.get(severity, '#888'),
        ))
    
    fig.update_layout(
        title="Vulnérabilités par niveau de sévérité",
        template="plotly_dark",
        showlegend=False,
        height=300
    )
    
    return fig

def show_security_report(security_results: Dict[str, Any]):
    """Affiche le rapport de sécurité."""
    st.markdown("## 🔒 Analyse de Sécurité")
    
    # Résumé des vulnérabilités
    severity_counts = security_results['summary']['severity_counts']
    total_issues = sum(severity_counts.values())
    
    # Score de sécurité
    security_score = 100 - (
        severity_counts['critical'] * 20 +
        severity_counts['high'] * 10 +
        severity_counts['medium'] * 5 +
        severity_counts['low'] * 1
    )
    security_score = max(0, security_score)
    
    # Affichage du score
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(
            f"""
            <div style='background: #1E1E1E; padding: 20px; border-radius: 10px; text-align: center;'>
                <h3 style='margin: 0; color: {"#00C851" if security_score > 80 else "#ff4444"}'>
                    {security_score}/100
                </h3>
                <p style='margin: 5px 0 0 0; color: #888;'>Score de sécurité</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.plotly_chart(
            show_severity_chart(severity_counts),
            use_container_width=True
        )
    
    # Détails des vulnérabilités
    if total_issues > 0:
        st.markdown("### Vulnérabilités détectées")
        
        # Bandit
        if 'bandit' in security_results and security_results['bandit'].get('issues'):
            with st.expander("🔍 Analyse Bandit", expanded=True):
                for issue in security_results['bandit']['issues']:
                    st.markdown(
                        f"""
                        <div style='background: #2E2E2E; padding: 15px; border-radius: 8px; margin: 10px 0;
                                  border-left: 4px solid {
                                      "#ff4444" if issue['severity'] == "HIGH"
                                      else "#ffbb33" if issue['severity'] == "MEDIUM"
                                      else "#00C851"
                                  };'>
                            <h4 style='margin: 0; color: white;'>{issue['test_name']}</h4>
                            <p style='margin: 5px 0; color: #888;'>{issue['description']}</p>
                            <code style='background: #1a1a1a; padding: 5px; border-radius: 4px;'>
                                Ligne {issue.get('line_number', 'N/A')}
                            </code>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        
        # Semgrep
        if 'semgrep' in security_results and security_results['semgrep'].get('matches'):
            with st.expander("🔍 Analyse Semgrep", expanded=True):
                for match in security_results['semgrep']['matches']:
                    st.markdown(
                        f"""
                        <div style='background: #2E2E2E; padding: 15px; border-radius: 8px; margin: 10px 0;
                                  border-left: 4px solid #ffbb33;'>
                            <h4 style='margin: 0; color: white;'>{match['rule']['id']}</h4>
                            <p style='margin: 5px 0; color: #888;'>{match['rule']['message']}</p>
                            <code style='background: #1a1a1a; padding: 5px; border-radius: 4px;'>
                                {match['extra'].get('lines', 'N/A')}
                            </code>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
    else:
        st.success("✅ Aucune vulnérabilité critique détectée")
    
    # Recommandations
    st.markdown("### 💡 Recommandations")
    recommendations = []
    
    if severity_counts['critical'] > 0:
        recommendations.append("⚠️ Corriger immédiatement les vulnérabilités critiques")
    if severity_counts['high'] > 0:
        recommendations.append("🔴 Planifier la correction des vulnérabilités importantes")
    if severity_counts['medium'] > 0:
        recommendations.append("🟡 Examiner les vulnérabilités moyennes")
    if len(recommendations) == 0:
        recommendations.append("✅ Maintenir les bonnes pratiques de sécurité")
    
    for rec in recommendations:
        st.markdown(f"- {rec}") 