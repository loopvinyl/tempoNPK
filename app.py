import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import kruskal
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MaxNLocator

# Configurações gerais com tema escuro
st.set_page_config(
    page_title="Análise Estatística de Vermicompostagem", 
    layout="wide",
    page_icon="📊"
)

# CSS para tema escuro premium
st.markdown("""
<style>
    /* Configurações gerais */
    body {
        color: #f0f2f6;
        background-color: #0e1117;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Containers e cards */
    .stApp {
        background: linear-gradient(135deg, #0c0f1d 0%, #131625 100%);
    }
    
    .card {
        background: rgba(20, 23, 40, 0.7) !important;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 28px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(100, 110, 200, 0.2);
    }
    
    .header-card {
        background: linear-gradient(135deg, #2a2f45 0%, #1a1d2b 100%);
        border-left: 4px solid #6f42c1;
        padding: 20px 30px;
    }
    
    .info-card {
        background: rgba(26, 29, 50, 0.8) !important;
        border-left: 4px solid #00c1e0;
        padding: 20px;
        border-radius: 0 12px 12px 0;
        margin-top: 15px;
    }
    
    .result-card {
        background: rgba(26, 29, 43, 0.9);
        border-left: 4px solid #6f42c1;
        padding: 20px;
        border-radius: 0 12px 12px 0;
        margin-bottom: 20px;
    }
    
    .signif-card {
        border-left: 4px solid #00c853 !important;
    }
    
    .not-signif-card {
        border-left: 4px solid #ff5252 !important;
    }
    
    .reference-card {
        background: rgba(20, 23, 40, 0.9) !important;
        border-left: 4px solid #00c1e0;
        padding: 20px;
        border-radius: 0 12px 12px 0;
        margin-top: 40px;
    }
    
    /* Títulos */
    h1, h2, h3, h4, h5, h6 {
        color: #e0e5ff !important;
        font-weight: 600;
    }
    
    /* Widgets */
    .stButton>button {
        background: rgba(26, 29, 43, 0.8) !important;
        color: white !important;
        border: 1px solid rgba(100, 110, 200, 0.3) !important;
        border-radius: 12px !important;
    }
    
    /* Tabelas */
    .dataframe {
        background: rgba(20, 23, 40, 0.7) !important;
        color: white !important;
        border-radius: 12px;
    }
    
    .dataframe th {
        background: rgba(70, 80, 150, 0.4) !important;
        color: #e0e5ff !important;
        font-weight: 600;
    }
    
    .dataframe tr:nth-child(even) {
        background: rgba(30, 33, 50, 0.5) !important;
    }
    
    .dataframe tr:hover {
        background: rgba(70, 80, 150, 0.3) !important;
    }
    
    /* Divider */
    .stDivider {
        border-top: 1px solid rgba(100, 110, 200, 0.2) !important;
        margin: 30px 0;
    }
    
    /* Espaçamento entre gráficos */
    .graph-spacer {
        height: 40px;
        background: transparent;
    }
    
    /* Ícones informativos */
    .info-icon {
        font-size: 1.2rem;
        margin-right: 10px;
        color: #00c1e0;
    }
    
    /* Listas formatadas */
    .custom-list li {
        margin-bottom: 10px;
        line-height: 1.6;
    }
    
    .custom-list ul {
        padding-left: 25px;
        margin-top: 8px;
    }
    
    .custom-list code {
        background: rgba(100, 110, 200, 0.2);
        padding: 2px 6px;
        border-radius: 4px;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# Configurar matplotlib para tema escuro premium
plt.style.use('dark_background')
mpl.rcParams.update({
    'axes.facecolor': '#131625',
    'figure.facecolor': '#0c0f1d',
    'axes.edgecolor': '#6f42c1',
    'axes.labelcolor': '#e0e5ff',
    'text.color': '#e0e5ff',
    'xtick.color': '#a0a7c0',
    'ytick.color': '#a0a7c0',
    'grid.color': '#2a2f45',
    'grid.alpha': 0.4,
    'font.family': 'Segoe UI',
    'axes.titleweight': '600',
    'axes.titlesize': 14,
})

# Título com estilo moderno
st.markdown("""
<div class="header-card">
    <h1 style="margin:0;padding:0;background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-size:2.5rem;">
        📊 Análise Estatística de Parâmetros de Vermicomposto
    </h1>
    <p style="margin:0;padding-top:10px;color:#a0a7c0;font-size:1.1rem;">
    Aplicação para análise de diferenças significativas em parâmetros de vermicomposto ao longo do tempo
    </p>
</div>
""", unsafe_allow_html=True)

## Mapeamento de parâmetros para nomes amigáveis
PARAM_MAPPING = {
    "TKN (g/kg)": "Nitrogênio Total (N)",
    "Total P (g/kg)": "Fósforo Total (P)",
    "TK (g/kg)": "Potássio Total (K)",
    "pH (H₂O)": "pH",
    "C/N ratio": "Relação C/N"
}

## Mapeamento de dias para ordenação numérica
DAY_MAPPING = {
    'Day 1': 1,
    'Day 30': 30,
    'Day 60': 60,
    'Day 90': 90,
    'Day 120': 120
}

## Função para Carregar Dados de Exemplo
@st.cache_data
def load_sample_data_with_stdev():
    sample_param_data = {
        'TKN (g/kg)': {
            'Day 1': {'mean': 20.8, 'stdev': 0.5},
            'Day 30': {'mean': 21.5, 'stdev': 0.6},
            'Day 60': {'mean': 22.2, 'stdev': 0.7},
            'Day 90': {'mean': 23.0, 'stdev': 0.8},
            'Day 120': {'mean': 24.5, 'stdev': 0.9}
        },
        'Total P (g/kg)': {
            'Day 1': {'mean': 12.1, 'stdev': 0.3},
            'Day 30': {'mean': 12.8, 'stdev': 0.4},
            'Day 60': {'mean': 13.5, 'stdev': 0.4},
            'Day 90': {'mean': 14.2, 'stdev': 0.5},
            'Day 120': {'mean': 15.0, 'stdev': 0.6}
        },
        'TK (g/kg)': {
            'Day 1': {'mean': 1.28, 'stdev': 0.02},
            'Day 30': {'mean': 1.29, 'stdev': 0.02},
            'Day 60': {'mean': 1.30, 'stdev': 0.02},
            'Day 90': {'mean': 1.31, 'stdev': 0.02},
            'Day 120': {'mean': 1.32, 'stdev': 0.02}
        },
        'pH (H₂O)': {
            'Day 1': {'mean': 7.04, 'stdev': 0.05},
            'Day 30': {'mean': 7.00, 'stdev': 0.05},
            'Day 60': {'mean': 6.95, 'stdev': 0.05},
            'Day 90': {'mean': 6.90, 'stdev': 0.05},
            'Day 120': {'mean': 6.85, 'stdev': 0.05}
        },
        'C/N ratio': {
            'Day 1': {'mean': 11.2, 'stdev': 0.2},
            'Day 30': {'mean': 10.9, 'stdev': 0.25},
            'Day 60': {'mean': 10.5, 'stdev': 0.3},
            'Day 90': {'mean': 10.0, 'stdev': 0.35},
            'Day 120': {'mean': 9.5, 'stdev': 0.4}
        }
    }

    num_replications = 3
    days = ['Day 1', 'Day 30', 'Day 60', 'Day 90', 'Day 120']
    all_replicated_data = []

    for param_name, daily_stats in sample_param_data.items():
        for _ in range(num_replications):
            row_data = {'Parameter': param_name, 'Substrate': 'VC-M'}
            for day in days:
                stats = daily_stats.get(day)
                if stats:
                    simulated_value = np.random.normal(
                        loc=stats['mean'], 
                        scale=stats['stdev']
                    )
                    
                    if param_name == 'pH (H₂O)':
                        simulated_value = np.clip(simulated_value, 0.0, 14.0)
                    elif 'g/kg' in param_name or 'ratio' in param_name:
                        simulated_value = max(0.0, simulated_value)
                    
                    row_data[day] = simulated_value
                else:
                    row_data[day] = np.nan
            all_replicated_data.append(row
