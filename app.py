import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import kruskal
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MaxNLocator

# Configurações gerais com tema escuro
st.set_page_config(
    page_title="Análise de Vermicompostos",
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
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }

    .header-card {
        background: rgba(20, 23, 40, 0.7) !important;
        border-radius: 20px;
        padding: 30px 40px;
        margin-bottom: 35px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(100, 110, 200, 0.3);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        text-align: center;
    }
    
    /* Botões */
    .stButton>button {
        background-color: #6f42c1;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 10px 20px;
        font-size: 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(111, 66, 193, 0.4);
    }
    .stButton>button:hover {
        background-color: #8c5de0;
        box-shadow: 0 6px 20px rgba(111, 66, 193, 0.6);
        transform: translateY(-2px);
    }

    /* Multiselect e Selectbox */
    .stMultiSelect > div > div > div > div, .stSelectbox > div > div {
        background-color: #2a2f45;
        border-radius: 10px;
        border: 1px solid #4a506e;
        color: #e0e5ff;
    }
    .stMultiSelect span, .stSelectbox span {
        color: #a0a7c0 !important;
    }
    .stMultiSelect div[data-baseweb="select"] > div, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #2a2f45;
        color: #e0e5ff;
    }

    /* Radio buttons */
    .stRadio div[role="radiogroup"] {
        background-color: #2a2f45;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #4a506e;
    }
    .stRadio label {
        color: #e0e5ff !important;
    }

    /* Checkbox */
    .stCheckbox span {
        color: #e0e5ff !important;
    }

    /* Input de texto */
    .stTextInput>div>div>input {
        background-color: #2a2f45;
        border-radius: 10px;
        border: 1px solid #4a506e;
        color: #e0e5ff;
    }

    /* Dataframe */
    .stDataFrame {
        border: 1px solid rgba(100, 110, 200, 0.2);
        border-radius: 12px;
        overflow: hidden;
    }

    .info-card {
        background: rgba(42, 47, 69, 0.6);
        border-left: 5px solid #00c1e0;
        border-radius: 12px;
        padding: 20px;
        margin-top: 25px;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0, 193, 224, 0.15);
    }
    .info-icon {
        font-size: 2rem;
        color: #00c1e0;
        margin-right: 10px;
    }

    .reference-card {
        background: rgba(20, 23, 40, 0.7);
        border-radius: 16px;
        padding: 25px;
        margin-top: 20px;
        border: 1px solid rgba(100, 110, 200, 0.2);
    }
    .reference-card p {
        color: #a0a7c0;
        font-size: 0.95rem;
    }

    /* Cards de resultado de significância */
    .result-card {
        background: rgba(20, 23, 40, 0.7);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
        border: 1px solid rgba(100, 110, 200, 0.2);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    .signif-card {
        border-left: 6px solid #00c853;
    }
    .not-signif-card {
        border-left: 6px solid #ff5252;
    }

    .stPlotlyChart {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    .graph-spacer {
        height: 30px; /* Espaçamento extra abaixo dos títulos de gráfico */
    }

</style>
""", unsafe_allow_html=True)

# Configurações do Matplotlib para tema escuro
mpl.rcParams['text.color'] = '#f0f2f6'
mpl.rcParams['axes.labelcolor'] = '#f0f2f6'
mpl.rcParams['xtick.color'] = '#f0f2f6'
mpl.rcParams['ytick.color'] = '#f0f2f6'
mpl.rcParams['axes.edgecolor'] = '#4a506e'
mpl.rcParams['figure.facecolor'] = '#0e1117'
mpl.rcParams['axes.facecolor'] = '#1a1e2b'
mpl.rcParams['grid.color'] = '#4a506e'
mpl.rcParams['grid.alpha'] = 0.3
mpl.rcParams['figure.constrained_layout.use'] = True # Ajuda no layout automático
mpl.rcParams['axes.titlesize'] = 16
mpl.rcParams['axes.labelsize'] = 14
mpl.rcParams['xtick.labelsize'] = 12
mpl.rcParams['ytick.labelsize'] = 12
mpl.rcParams['legend.fontsize'] = 12
mpl.rcParams['lines.linewidth'] = 2

# ===================================================================
# PÁGINA INICIAL
# ===================================================================
def show_homepage():
    """Exibe a página inicial para seleção do artigo."""
    st.markdown("""
    <div class="header-card">
        <h1 style="margin:0;padding:0;background:linear-gradient(135deg, #00c1e0 0%, #00d4b1 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-size:3rem;">
            🔬 Análise de Dados de Vermicompostagem
        </h1>
        <p style="margin:0;padding-top:15px;color:#a0a7c0;font-size:1.2rem;">
            Explore e analise resultados de artigos científicos sobre vermicompostagem.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h2 style="display:flex;align-items:center;gap:10px;">
            <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                📚 Selecione o Artigo para Análise
            </span>
        </h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Dermendzhieva et al. (2021) ⏳", help="Análise temporal da estabilidade de vermicompostos", key="btn_dermendzhieva"):
            st.session_state['selected_article'] = 'dermendzhieva'
            st.rerun()

    with col2:
        if st.button("Jordão et al. (2007) 🧪", help="Análise comparativa da remoção de metais pesados por doses/tratamentos", key="btn_jordao"):
            st.session_state['selected_article'] = 'jordao'
            st.rerun()

    st.markdown("""
    <div class="info-card">
        <h3 style="display:flex;align-items:center;color:#00c1e0;">
            <span class="info-icon">ℹ️</span> Sobre esta ferramenta
        </h3>
        <div style="margin-top:15px; color:#d7dce8; line-height:1.7;">
            <p>Esta ferramenta oferece uma interface interativa para explorar dados simulados (baseados em artigos científicos) e aplicar testes estatísticos, como o teste de Kruskal-Wallis, para analisar a significância de diferentes parâmetros ao longo do tempo ou entre diferentes tratamentos.</p>
            <p>Selecione um dos artigos acima para começar a análise.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===================================================================
# MÓDULO DERMENDZHIEVA ET AL. (2021) - ANÁLISE TEMPORAL
# ===================================================================

# Mapeamento de Parâmetros para exibição
PARAM_MAPPING_DERM = {
    "pH": "pH",
    "Electrical Conductivity": "Condutividade Elétrica (dS/m)",
    "Organic Carbon": "Carbono Orgânico (%)",
    "Total Nitrogen": "Nitrogênio Total (%)",
    "C/N ratio": "Relação C/N",
    "Available Phosphorus": "Fósforo Disponível (mg/kg)",
    "Potassium": "Potássio (mg/kg)",
    "Calcium": "Cálcio (mg/kg)",
    "Magnesium": "Magnésio (mg/kg)"
}

# Funções de ajuda para simulação (mantidas idênticas)
@st.cache_data
def load_sample_data_with_stdev(distribution_type='LogNormal'):
    """
    Carrega dados de exemplo baseados em Dermendzhieva et al. (2021)
    com desvio padrão para simulação, considerando diferentes distribuições.
    """
    # Dados fictícios baseados em Dermendzhieva et al. (2021) para ilustração.
    # Os valores reais devem ser extraídos do artigo.
    sample_data = {
        "pH": {'mean': 7.5, 'stdev': 0.5},
        "Electrical Conductivity": {'mean': 3.0, 'stdev': 0.8},
        "Organic Carbon": {'mean': 30.0, 'stdev': 5.0},
        "Total Nitrogen": {'mean': 2.0, 'stdev': 0.3},
        "C/N ratio": {'mean': 15.0, 'stdev': 2.0},
        "Available Phosphorus": {'mean': 1500.0, 'stdev': 300.0},
        "Potassium": {'mean': 20.0, 'stdev': 4.0},
        "Calcium": {'mean': 3000.0, 'stdev': 500.0},
        "Magnesium": {'mean': 500.0, 'stdev': 100.0}
    }

    time_points = [0, 30, 60, 90, 120] # Dias
    num_replications = 5 # Número de repetições simuladas por ponto de tempo

    all_replicated_data = []

    for param_name, stats in sample_data.items():
        for time_point in time_points:
            # Simular uma mudança ao longo do tempo para alguns parâmetros
            adjusted_mean = stats['mean']
            adjusted_stdev = stats['stdev']

            if "pH" in param_name: # pH tende a estabilizar
                adjusted_mean = stats['mean'] - (time_point / 120) * 0.5
            elif "Electrical Conductivity" in param_name: # CE pode aumentar e depois diminuir
                adjusted_mean = stats['mean'] + (time_point / 60) * 0.5 - (time_point / 120)**2 * 0.2
            elif "Organic Carbon" in param_name: # Carbono Orgânico tende a diminuir
                adjusted_mean = stats['mean'] * (1 - (time_point / 150) * 0.6)
            elif "C/N ratio" in param_name: # C/N tende a diminuir
                adjusted_mean = stats['mean'] * (1 - (time_point / 150) * 0.4)
            
            # Garantir que a média não seja negativa e desvio padrão positivo
            adjusted_mean = max(0.1, adjusted_mean)
            adjusted_stdev = max(0.01, adjusted_stdev)

            for _ in range(num_replications):
                if distribution_type == 'Normal':
                    simulated_value = np.random.normal(loc=adjusted_mean, scale=adjusted_stdev)
                elif distribution_type == 'LogNormal':
                    # Calcular mu e sigma para lognormal a partir de média e desvio padrão
                    mu = adjusted_mean
                    sigma = adjusted_stdev
                    
                    if sigma <= 0: # Evitar log de zero ou negativo para sigma
                        log_sigma = 0
                        log_mu = np.log(mu) if mu > 0 else 0 # Handle mu=0 case
                    else:
                        log_sigma = np.sqrt(np.log(1 + (sigma/mu)**2))
                        log_mu = np.log(mu) - 0.5 * log_sigma**2
                    
                    simulated_value = np.random.lognormal(mean=log_mu, sigma=log_sigma)
                else:
                    simulated_value = np.random.normal(loc=adjusted_mean, scale=adjusted_stdev) # Default to Normal

                # Aplicar limites lógicos para os valores
                if 'pH' in param_name:
                    simulated_value = np.clip(simulated_value, 0.0, 14.0)
                else:
                    simulated_value = max(0.0, simulated_value) # Não pode ser negativo

                all_replicated_data.append({
                    "Parameter": param_name,
                    "Time (days)": time_point,
                    "Value": simulated_value
                })

    return pd.DataFrame(all_replicated_data)

# Função de plotagem (mantida idêntica)
def plot_parameter_over_time(ax, df_param, param_name):
    """
    Plota os valores de um parâmetro ao longo do tempo, mostrando pontos individuais e medianas.
    """
    time_points = sorted(df_param["Time (days)"].unique())
    medians = []
    
    colors = ['#00c1e0', '#00d4b1', '#ffd166', '#ff6b6b', '#a78bfa'] # Ajuste de cores
    
    for i, t in enumerate(time_points):
        values = df_param[df_param["Time (days)"] == t]["Value"]
        if not values.empty:
            ax.scatter(
                [t] * len(values),
                values,
                color=colors[i % len(colors)],
                alpha=0.85,
                s=100, # Tamanho do ponto
                edgecolors='white', # Borda branca
                linewidth=1.2, # Largura da borda
                zorder=3 # Para ficar acima da linha da mediana
            )
            median_val = np.median(values)
            medians.append(median_val)
            ax.plot([t-5, t+5], [median_val, median_val], color='white', linewidth=3, zorder=5) # Linha da mediana

    if medians:
        ax.plot(time_points, medians, color='#6f42c1', linestyle='--', marker='s', markersize=8, label="Mediana", zorder=4) # Linha conectando medianas

    ax.set_xlabel("Tempo (dias)", fontsize=12, fontweight='bold', labelpad=15)
    ax.set_ylabel(PARAM_MAPPING_DERM.get(param_name, param_name), fontsize=12, fontweight='bold', labelpad=15)
    ax.set_title(f"{PARAM_MAPPING_DERM.get(param_name, param_name)} ao longo do Tempo", 
                         fontsize=14, fontweight='bold', pad=20)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True)) # Garante ticks inteiros no tempo
    ax.grid(True, alpha=0.2, linestyle='--', color='#a0a7c0', zorder=1) # Grade de fundo
    
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_facecolor('#0c0f1d')
    ax.legend(loc='best', fontsize=10, framealpha=0.25)
    return ax

# Função de interpretação de resultados (mantida idêntica)
def display_dermendzhieva_results_interpretation(results):
    st.markdown("""
    <div class="card">
        <h2 style="display:flex;align-items:center;gap:10px;">
            <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                📝 Interpretação dos Resultados - Dermendzhieva et al. (2021)
            </span>
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    if not results:
        st.info("Nenhuma interpretação disponível, pois não há resultados estatísticos.")
        return

    for res in results:
        param_name = res["Parâmetro"]
        p_val = res["p-value"]
        is_significant = p_val < 0.05
        
        card_class = "signif-card" if is_significant else "not-signif-card"
        icon = "✅" if is_significant else "❌"
        title_color = "#00c853" if is_significant else "#ff5252"
        status = "Significativo" if is_significant else "Não Significativo"
        
        st.markdown(f"""
        <div class="result-card {card_class}">
            <div style="display:flex;align-items:center; justify-content:space-between;">
                <div style="display:flex;align-items:center; gap:12px;">
                    <div style="font-size:28px; color:{title_color};">{icon}</div>
                    <h3 style="margin:0; color:{title_color}; font-weight:600;">{param_name}</h3>
                </div>
                <div style="background:rgba(42, 47, 69, 0.7); padding:8px 18px; border-radius:30px; border:1px solid {title_color}30;">
                    <span style="font-weight:bold; font-size:1.1rem; color:{title_color};">{status}</span>
                    <span style="color:#a0a7c0; margin-left:8px;">p = {p_val:.4f}</span>
                </div>
            </div>
            <div style="margin-top:20px; padding-top:15px; border-top:1px solid rgba(100, 110, 200, 0.2);">
        """, unsafe_allow_html=True)
        
        if is_significant:
            st.markdown(f"""
                <div style="color:#e0e5ff; line-height:1.8;">
                    <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                        <span style="color:#00c853; font-size:1.5rem;">•</span>
                        <b>Houve uma mudança estatisticamente significativa</b> no valor de **{param_name}** ao longo do tempo.
                    </p>
                    <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                        <span style="color:#00c853; font-size:1.5rem;">•</span>
                        Isso indica que o processo de vermicompostagem influenciou este parâmetro, e a variação observada não é devido apenas ao acaso.
                    </p>
                    <div style="background:#2a2f45;padding:10px;border-radius:8px;margin-top:10px;">
                        <b>Contexto do artigo:</b> Para Dermendzhieva et al. (2021), a estabilidade e maturação do vermicomposto são avaliadas através das mudanças nesses parâmetros ao longo do tempo. Uma mudança significativa pode indicar o progresso do processo de compostagem.
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="color:#e0e5ff; line-height:1.8;">
                    <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                        <span style="color:#ff5252; font-size:1.5rem;">•</span>
                        Não foi encontrada uma <b>mudança estatisticamente significativa</b> no valor de **{param_name}** ao longo do tempo.
                    </p>
                    <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                        <span style="color:#ff5252; font-size:1.5rem;">•</span>
                        Isso sugere que o processo de vermicompostagem pode não ter afetado este parâmetro de forma detectável no período analisado, ou sua variação se deve ao acaso.
                    </p>
                    <div style="background:#2a2f45;padding:10px;border-radius:8px;margin-top:10px;">
                        <b>Contexto do artigo:</b> Em alguns casos, a ausência de mudança significativa pode indicar que o parâmetro já atingiu um ponto de estabilidade, ou que a metodologia empregada não detectou variações esperadas.
                    </div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

def run_dermendzhieva_analysis():
    """Módulo para análise de Dermendzhieva et al. (2021)"""
    st.markdown("""
    <div class="header-card">
        <h1 style="margin:0;padding:0;background:linear-gradient(135deg, #00c1e0 0%, #00d4b1 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-size:2.5rem;">
            ⏳ Análise Temporal de Vermicompostos
        </h1>
        <p style="margin:0;padding-top:10px;color:#a0a7c0;font-size:1.1rem;">
        Dermendzhieva et al. (2021) - Estabilidade e maturação de vermicompostos.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("← Voltar para seleção de artigos", key="btn_back_dermendzhieva"):
        del st.session_state['selected_article']
        st.rerun()

    # Painel de configurações
    st.markdown("""
    <div class="card">
        <h2 style="display:flex;align-items:center;gap:10px;">
            <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                ⚙️ Configurações de Análise
            </span>
        </h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        use_sample = st.checkbox("Usar dados de exemplo (Dermendzhieva)", value=True, key="use_sample_derm")
        distribution_type = st.radio(
            "Tipo de Distribuição para Amostras:",
            ('LogNormal', 'Normal'),
            index=0,
            key="dist_type_derm"
        )

    # Carregar dados ANTES de tentar acessar colunas
    df = load_sample_data_with_stdev(distribution_type)

    with col2:
        unique_params = df['Parameter'].unique()
        param_options = [PARAM_MAPPING_DERM.get(p, p) for p in unique_params]
        selected_params = st.multiselect(
            "Selecione os parâmetros:",
            options=param_options,
            default=param_options,
            key="param_select_derm"
        )

    # Pré-visualização dos Dados (TODAS AS AMOSTRAS)
    st.markdown("""
    <div class="card">
        <h2 style="display:flex;align-items:center;gap:10px;">
            <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                🔍 Pré-visualização Completa dos Dados
            </span>
        </h2>
    </div>
    """, unsafe_allow_html=True)
    st.dataframe(df)
    st.markdown(f"**Total de amostras:** {len(df)}")

    # Explicação detalhada sobre a produção das amostras
    st.markdown(f"""
    <div class="info-card">
        <h3 style="display:flex;align-items:center;color:#00c1e0;">
            <span class="info-icon">ℹ️</span> Como as amostras foram produzidas
        </h3>
        <div style="margin-top:15px; color:#d7dce8; line-height:1.7;">
            <p>
                As amostras analisadas por esta ferramenta são geradas por simulação computacional a partir de dados de média e desvio padrão, para cada **ponto de tempo** e para cada parâmetro estudado. A ferramenta utiliza a <b>média</b> como o valor central e o <b>desvio padrão</b> para definir a variabilidade das amostras individuais.
            </p>
            <p>
                Os dados são simulados utilizando uma Distribuição <b>{distribution_type}</b>.
                <ul>
                    <li><b>Distribuição Normal:</b> Assume que os dados se distribuem simetricamente em torno da média.</li>
                    <li><b>Distribuição Lognormal:</b> Frequentemente usada para dados que são estritamente positivos, assimétricos à direita e comuns em análises ambientais e biológicas. Seus logaritmos naturais seguem uma distribuição normal.</li>
                </ul>
                Aplicamos regras para garantir que os valores simulados permaneçam dentro da escala lógica (ex: pH entre 0 e 14) e que as concentrações de substâncias não sejam negativas, tornando as amostras mais realistas para dados de vermicompostagem.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Realizar Análise
    if not selected_params:
        st.warning("Selecione pelo menos um parâmetro para análise.")
        return

    # Converter de volta para nomes originais para filtragem no DataFrame
    reverse_mapping = {v: k for k, v in PARAM_MAPPING_DERM.items()}
    selected_original_params = [reverse_mapping.get(p, p) for p in selected_params]

    results = []
    time_points = sorted(df["Time (days)"].unique())

    # Configurar subplots dinamicamente
    num_plots = len(selected_original_params)
    if num_plots > 0:
        fig = plt.figure(figsize=(10, 6 * num_plots))
        gs = fig.add_gridspec(num_plots, 1, hspace=0.6) # Espaço vertical entre gráficos
        
        axes = []
        for i in range(num_plots):
            ax = fig.add_subplot(gs[i])
            axes.append(ax)

        for i, param in enumerate(selected_original_params):
            param_df = df[df['Parameter'] == param]
            
            # Preparar dados para Kruskal-Wallis: lista de arrays (um para cada grupo/tempo)
            data_per_time = [param_df[param_df["Time (days)"] == t]["Value"].dropna().values for t in time_points]
            
            # Filtrar grupos vazios antes de passar para Kruskal-Wallis
            data_per_time_filtered = [data for data in data_per_time if len(data) > 0]

            if len(data_per_time_filtered) >= 2: # Kruskal-Wallis precisa de pelo menos 2 grupos
                try:
                    h_stat, p_val = kruskal(*data_per_time_filtered)
                    results.append({
                        "Parâmetro": PARAM_MAPPING_DERM.get(param, param),
                        "H-Statistic": h_stat,
                        "p-value": p_val,
                        "Significativo (p<0.05)": p_val < 0.05
                    })
                    
                    # Plotar gráfico
                    ax = axes[i]
                    plot_parameter_over_time(ax, param_df, param)
                    
                    # Adicionar resultado do teste ao gráfico
                    annotation_text = f"Kruskal-Wallis: H = {h_stat:.2f}, p = {p_val:.4f}"
                    ax.text(
                        0.5, 0.95,
                        annotation_text,
                        transform=ax.transAxes,
                        ha='center',
                        va='top',
                        fontsize=11,
                        color='white',
                        bbox=dict(
                            boxstyle="round,pad=0.3",
                            facecolor='#2a2f45',
                            alpha=0.8,
                            edgecolor='none'
                        )
                    )

                except ValueError as e:
                    st.warning(f"Não foi possível realizar o teste Kruskal-Wallis para {PARAM_MAPPING_DERM.get(param, param)}: {e}. Certifique-se de que há variação nos dados de tempo.")
                except Exception as e:
                    st.error(f"Ocorreu um erro inesperado ao processar {PARAM_MAPPING_DERM.get(param, param)}: {e}")
            else:
                st.info(f"Dados insuficientes para {PARAM_MAPPING_DERM.get(param, param)} para realizar o teste de Kruskal-Wallis (mínimo de 2 pontos de tempo com dados).")

    # Resultados Estatísticos
    st.markdown("""
    <div class="card">
        <h2 style="display:flex;align-items:center;gap:10px;">
            <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                📈 Resultados Estatísticos
            </span>
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    if results:
        results_df = pd.DataFrame(results)
        results_df['Significância'] = results_df['p-value'].apply(
            lambda p: "✅ Sim" if p < 0.05 else "❌ Não"
        )
        
        # Reordenar colunas para melhor visualização
        results_df = results_df[['Parâmetro', 'H-Statistic', 'p-value', 'Significância']]
        
        st.dataframe(
            results_df.style
            .format({"p-value": "{:.4f}", "H-Statistic": "{:.2f}"})
            .set_properties(**{
                'color': 'white',
                'background-color': '#131625',
            })
            .apply(lambda x: ['background: rgba(70, 80, 150, 0.3)' if x['p-value'] < 0.05 else '' for i in x], axis=1)
        )
    else:
        st.info("Nenhum resultado estatístico disponível para os parâmetros selecionados.")

    # Gráficos
    if num_plots > 0:
        st.markdown("""
        <div class="card">
            <h2 style="display:flex;align-items:center;gap:10px;">
                <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                    📊 Gráficos de Variação ao Longo do Tempo
                </span>
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="graph-spacer"></div>', unsafe_allow_html=True)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # Interpretação
    display_dermendzhieva_results_interpretation(results)

    # Referência Bibliográfica (Formato ABNT)
    st.markdown("""
    <div class="card">
        <h2 style="display:flex;align-items:center;gap:10px;">
            <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                📚 Referência Bibliográfica
            </span>
        </h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="reference-card">
        <p style="line-height:1.8; text-align:justify;">
            DERMENDZHIEVA, D. et al. Stability and Maturity of Vermicomposts and Potential for Soil Application. 
            <strong>Agronomy</strong>, Basel, v. 11, n. 4, p. 1-18, abr. 2021.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ===================================================================
# MÓDULO JORDÃO ET AL. (2007) - ANÁLISE COMPARATIVA POR DOSES
# ===================================================================
def run_jordao_analysis():
    """Módulo para análise comparativa de tratamentos/doses"""

    # Mapeamento de parâmetros para Jordão et al. (2007)
    PARAM_MAPPING_JORDAO = { 
        "pH": "pH",
        "Organic Matter": "Matéria Orgânica (%)",
        "C/N ratio": "Relação C/N",
        "Cu": "Cobre (mg/kg)",
        "Ni": "Níquel (mg/kg)",
        "Zn": "Zinco (mg/kg)",
        "Cu_leaves": "Cobre nas Folhas (mg/kg)",
        "Ni_leaves": "Níquel nas Folhas (mg/kg)",
        "Zn_leaves": "Zinco nas Folhas (mg/kg)",
        "Cu_roots": "Cobre nas Raízes (mg/kg)",
        "Ni_roots": "Níquel nas Raízes (mg/kg)",
        "Zn_roots": "Zinco nas Raízes (mg/kg)",
    }

    # Definir "doses" ou "tratamentos" para Jordão et al. (2007)
    # Estes são apenas exemplos, devem ser baseados nos dados reais do Jordão et al.
    DOSES_MAPPING = {
        '0% VC': 0, # Controle (0% Vermicomposto)
        '25% VC': 25,
        '50% VC': 50,
        '75% VC': 75,
        '100% VC': 100,
    }
    
    # Função para carregar dados específicos do artigo Jordão et al. com simulação
    @st.cache_data
    def load_jordao_simulated_data(distribution_type='LogNormal'):
        # Dados de exemplo para simular diferentes doses/tratamentos
        # Ajuste esses valores para refletir os dados reais do Jordão et al. (2007)
        # para cada tratamento/dose.
        sample_dose_data = {
            "pH": {
                '0% VC': {'mean': 6.5, 'stdev': 0.3},
                '25% VC': {'mean': 6.8, 'stdev': 0.25},
                '50% VC': {'mean': 7.0, 'stdev': 0.2},
                '75% VC': {'mean': 7.2, 'stdev': 0.2},
                '100% VC': {'mean': 7.3, 'stdev': 0.2}
            },
            "Organic Matter": {
                '0% VC': {'mean': 20.0, 'stdev': 2.0},
                '25% VC': {'mean': 25.0, 'stdev': 2.5},
                '50% VC': {'mean': 30.0, 'stdev': 3.0},
                '75% VC': {'mean': 35.0, 'stdev': 3.5},
                '100% VC': {'mean': 40.0, 'stdev': 4.0}
            },
            "C/N ratio": {
                '0% VC': {'mean': 25.0, 'stdev': 3.0},
                '25% VC': {'mean': 22.0, 'stdev': 2.5},
                '50% VC': {'mean': 18.0, 'stdev': 2.0},
                '75% VC': {'mean': 15.0, 'stdev': 1.5},
                '100% VC': {'mean': 12.0, 'stdev': 1.2}
            },
            "Cu": { # Concentração de Cobre no substrato/efluente
                '0% VC': {'mean': 50.0, 'stdev': 5.0},
                '25% VC': {'mean': 40.0, 'stdev': 4.5},
                '50% VC': {'mean': 30.0, 'stdev': 3.0},
                '75% VC': {'mean': 25.0, 'stdev': 2.5},
                '100% VC': {'mean': 20.0, 'stdev': 2.0}
            },
            "Ni": { # Concentração de Níquel no substrato/efluente
                '0% VC': {'mean': 30.0, 'stdev': 3.0},
                '25% VC': {'mean': 25.0, 'stdev': 2.5},
                '50% VC': {'mean': 20.0, 'stdev': 2.0},
                '75% VC': {'mean': 18.0, 'stdev': 1.8},
                '100% VC': {'mean': 15.0, 'stdev': 1.5}
            },
            "Zn": { # Concentração de Zinco no substrato/efluente
                '0% VC': {'mean': 150.0, 'stdev': 15.0},
                '25% VC': {'mean': 120.0, 'stdev': 12.0},
                '50% VC': {'mean': 90.0, 'stdev': 9.0},
                '75% VC': {'mean': 70.0, 'stdev': 7.0},
                '100% VC': {'mean': 50.0, 'stdev': 5.0}
            },
            "Cu_leaves": { # Cobre absorvido pelas folhas de alface
                '0% VC': {'mean': 10.0, 'stdev': 1.0},
                '25% VC': {'mean': 9.5, 'stdev': 0.9},
                '50% VC': {'mean': 9.0, 'stdev': 0.8},
                '75% VC': {'mean': 8.5, 'stdev': 0.7},
                '100% VC': {'mean': 8.0, 'stdev': 0.6}
            },
            "Ni_leaves": { # Níquel absorvido pelas folhas de alface
                '0% VC': {'mean': 5.0, 'stdev': 0.5},
                '25% VC': {'mean': 4.8, 'stdev': 0.4},
                '50% VC': {'mean': 4.5, 'stdev': 0.4},
                '75% VC': {'mean': 4.2, 'stdev': 0.3},
                '100% VC': {'mean': 4.0, 'stdev': 0.3}
            }
            # Adicione mais parâmetros conforme necessário do artigo de Jordão et al.
        }

        num_replications = 3 # Número de repetições por dose para simulação
        doses = list(DOSES_MAPPING.keys())
        all_replicated_data = []

        for param_name, dose_stats in sample_dose_data.items():
            for _ in range(num_replications):
                row_data = {'Parameter': param_name}
                for dose in doses:
                    stats = dose_stats.get(dose)
                    if stats:
                        # Lógica de simulação (Normal ou LogNormal)
                        if distribution_type == 'Normal':
                            simulated_value = np.random.normal(loc=stats['mean'], scale=stats['stdev'])
                        elif distribution_type == 'LogNormal':
                            mu = stats['mean']
                            sigma = stats['stdev']
                            if sigma <= 0: # Evitar log de zero ou negativo para sigma
                                log_sigma = 0
                                log_mu = np.log(mu) if mu > 0 else 0 # Handle mu=0 case
                            else:
                                log_sigma = np.sqrt(np.log(1 + (sigma/mu)**2))
                                log_mu = np.log(mu) - 0.5 * log_sigma**2
                            simulated_value = np.random.lognormal(mean=log_mu, sigma=log_sigma)
                        else:
                            simulated_value = np.random.normal(loc=stats['mean'], scale=stats['stdev']) # Default
                        
                        # Garantir valores não-negativos e pH dentro do range
                        if 'pH' in param_name:
                            simulated_value = np.clip(simulated_value, 0.0, 14.0)
                        else:
                            simulated_value = max(0.0, simulated_value) # Não pode ser negativo
                        
                        row_data[dose] = simulated_value
                    else:
                        row_data[dose] = np.nan
                all_replicated_data.append(row_data)

        return pd.DataFrame(all_replicated_data)

    # Adaptação da função de plotagem para "doses"
    def plot_parameter_comparison_doses(ax, data_by_dose, doses_labels, param_name):
        colors = ['#6f42c1', '#00c1e0', '#00d4b1', '#ffd166', '#ff6b6b'] 
        
        # Verificar se temos dados para plotar
        if not data_by_dose or any(len(group) == 0 for group in data_by_dose):
            ax.text(0.5, 0.5, 'Dados insuficientes para plotar', ha='center', va='center', fontsize=12, color='white')
            return ax

        # Calcular limites para eixo Y
        all_values = [val for group in data_by_dose for val in group]
        if not all_values:
            ax.text(0.5, 0.5, 'Sem dados disponíveis', ha='center', va='center', fontsize=12, color='white')
            return ax
        y_min = min(all_values) * 0.9 if min(all_values) > 0 else 0
        y_max = max(all_values) * 1.1

        # Plotar pontos individuais e medianas para cada dose/tratamento
        for i, (dose_data, dose_label) in enumerate(zip(data_by_dose, doses_labels)):
            ax.scatter(
                [i] * len(dose_data), 
                dose_data, 
                color=colors[i % len(colors)], 
                alpha=0.85, 
                s=100, 
                label=dose_label,
                edgecolors='white',
                linewidth=1.2,
                zorder=3,
                marker='o'
            )
            
            if len(dose_data) > 0:
                median_val = np.median(dose_data)
                ax.plot(
                    [i-0.2, i+0.2], # Extender a linha da mediana um pouco
                    [median_val, median_val], 
                    color='white', 
                    linewidth=3, 
                    zorder=5,
                    alpha=0.95
                )

        # Configurações do gráfico
        ax.set_xticks(range(len(doses_labels)))
        ax.set_xticklabels(doses_labels, fontsize=11)
        ax.set_xlabel("Dose / Tratamento", fontsize=12, fontweight='bold', labelpad=15)
        ax.set_ylabel(PARAM_MAPPING_JORDAO.get(param_name, param_name), fontsize=12, fontweight='bold', labelpad=15)
        ax.set_title(f"Comparação de {PARAM_MAPPING_JORDAO.get(param_name, param_name)} por Dose/Tratamento", 
                             fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='best', fontsize=10, framealpha=0.25)
        ax.grid(True, alpha=0.2, linestyle='--', color='#a0a7c0', zorder=1) 
        ax.set_ylim(y_min, y_max)

        for spine in ax.spines.values(): 
            spine.set_visible(False) 
        ax.set_facecolor('#0c0f1d') 
        return ax

    # Função para exibir resultados com contexto específico
    def display_jordao_results_interpretation(results):
        st.markdown("""
        <div class="card">
            <h2 style="display:flex;align-items:center;gap:10px;">
                <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                    📝 Interpretação dos Resultados - Jordão et al. (2007)
                </span>
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        if not results:
            st.info("Nenhuma interpretação disponível, pois não há resultados estatísticos.")
            return

        for res in results:
            param_name = res["Parâmetro"]
            p_val = res["p-value"]
            is_significant = p_val < 0.05
            
            card_class = "signif-card" if is_significant else "not-signif-card"
            icon = "✅" if is_significant else "❌"
            title_color = "#00c853" if is_significant else "#ff5252"
            status = "Significativo" if is_significant else "Não Significativo"
            
            st.markdown(f"""
            <div class="result-card {card_class}">
                <div style="display:flex;align-items:center; justify-content:space-between;">
                    <div style="display:flex;align-items:center; gap:12px;">
                        <div style="font-size:28px; color:{title_color};">{icon}</div>
                        <h3 style="margin:0; color:{title_color}; font-weight:600;">{param_name}</h3>
                    </div>
                    <div style="background:rgba(42, 47, 69, 0.7); padding:8px 18px; border-radius:30px; border:1px solid {title_color}30;">
                        <span style="font-weight:bold; font-size:1.1rem; color:{title_color};">{status}</span>
                        <span style="color:#a0a7c0; margin-left:8px;">p = {p_val:.4f}</span>
                    </div>
                </div>
                <div style="margin-top:20px; padding-top:15px; border-top:1px solid rgba(100, 110, 200, 0.2);">
            """, unsafe_allow_html=True)
            
            metal_context = ""
            if any(metal in param_name for metal in ["Cobre", "Níquel", "Zinco"]):
                metal_context = """
                    <div style="background:#2a2f45;padding:10px;border-radius:8px;margin-top:10px;">
                        <b>Relevância no contexto do artigo:</b> Este parâmetro foi estudado como indicador de eficiência na remoção de metais pesados e seu impacto no cultivo de alface em diferentes tratamentos/doses de vermicomposto. Diferenças significativas podem indicar que a dose ou tratamento teve um efeito notável na absorção ou presença do metal.
                    </div>
                """

            if is_significant:
                st.markdown(f"""
                    <div style="color:#e0e5ff; line-height:1.8;">
                        <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                            <span style="color:#00c853; font-size:1.5rem;">•</span>
                            <b>Diferenças significativas encontradas entre as doses/tratamentos</b>
                        </p>
                        <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                            <span style="color:#00c853; font-size:1.5rem;">•</span>
                            A aplicação de diferentes doses/tratamentos de vermicomposto afeta este parâmetro de forma estatisticamente detectável.
                        </p>
                        {metal_context}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="color:#e0e5ff; line-height:1.8;">
                        <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                            <span style="color:#ff5252; font-size:1.5rem;">•</span>
                            <b>Não foram encontradas diferenças significativas entre as doses/tratamentos</b>
                        </p>
                        <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                            <span style="color:#ff5252; font-size:1.5rem;">•</span>
                            A aplicação de diferentes doses/tratamentos de vermicomposto não afeta este parâmetro de forma estatisticamente detectável.
                        </p>
                        {metal_context}
                    </div>
                """, unsafe_allow_html=True)
            st.markdown("</div></div>", unsafe_allow_html=True)

    # Interface principal do módulo Jordão
    st.markdown("""
    <div class="header-card">
        <h1 style="margin:0;padding:0;background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-size:2.5rem;">
            ⚗️ Análise Comparativa por Doses/Tratamentos
        </h1>
        <p style="margin:0;padding-top:10px;color:#a0a7c0;font-size:1.1rem;">
        Jordão et al. (2007) - Redução de metais pesados em efluentes líquidos por vermicompostos e cultivo de alface.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Voltar para seleção de artigos", key="btn_back_jordao"): 
        del st.session_state['selected_article'] 
        st.rerun() 

    # Painel de configurações
    st.markdown("""
    <div class="card">
        <h2 style="display:flex;align-items:center;gap:10px;">
            <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                ⚙️ Configurações de Análise
            </span>
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2) 
    
    with col1: 
        use_sample_jordao = st.checkbox("Usar dados de exemplo (Jordão)", value=True, key="use_sample_jordao")
        distribution_type_jordao = st.radio(
            "Tipo de Distribuição para Amostras:",
            ('LogNormal', 'Normal'),
            index=0,
            key="dist_type_jordao"
        ) 
    
    # Carregar dados ANTES de tentar acessar colunas
    df_jordao = load_jordao_simulated_data(distribution_type_jordao)
    
    with col2: 
        unique_params_jordao = df_jordao['Parameter'].unique() 
        param_options_jordao = [PARAM_MAPPING_JORDAO.get(p, p) for p in unique_params_jordao] 
        
        selected_params_jordao = st.multiselect(
            "Selecione os parâmetros:",
            options=param_options_jordao,
            default=param_options_jordao,
            key="param_select_jordao"
        ) 

    # Pré-visualização dos Dados (TODAS AS AMOSTRAS)
    st.markdown("""
    <div class="card">
        <h2 style="display:flex;align-items:center;gap:10px;">
            <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                🔍 Pré-visualização Completa dos Dados
            </span>
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(df_jordao) 
    st.markdown(f"**Total de amostras:** {len(df_jordao)}") 

    # Explicação detalhada sobre a produção das amostras (adaptada)
    st.markdown(f"""
    <div class="info-card">
        <h3 style="display:flex;align-items:center;color:#00c1e0;">
            <span class="info-icon">ℹ️</span> Como as amostras foram produzidas
        </h3>
        <div style="margin-top:15px; color:#d7dce8; line-height:1.7;">
            <p>
                As amostras analisadas por esta ferramenta são geradas por simulação computacional a partir de dados de média e desvio padrão, para cada **dose/tratamento** e para cada parâmetro estudado. A ferramenta utiliza a <b>média</b> como o valor central e o <b>desvio padrão</b> para definir a variabilidade das amostras individuais.
            </p>
            <p>
                Os dados são simulados utilizando uma Distribuição <b>{distribution_type_jordao}</b>.
                <ul>
                    <li><b>Distribuição Normal:</b> Assume que os dados se distribuem simetricamente em torno da média.</li>
                    <li><b>Distribuição Lognormal:</b> Frequentemente usada para dados que são estritamente positivos, assimétricos à direita e comuns em análises ambientais e biológicas. Seus logaritmos naturais seguem uma distribuição normal.</li>
                </ul>
                Aplicamos regras para garantir que os valores simulados permaneçam dentro da escala lógica (ex: pH entre 0 e 14) e que as concentrações de substâncias não sejam negativas, tornando as amostras mais realistas para dados de vermicompostagem.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Realizar Análise
    if not selected_params_jordao:
        st.warning("Selecione pelo menos um parâmetro para análise.")
        return

    # Converter de volta para nomes originais
    reverse_mapping_jordao = {v: k for k, v in PARAM_MAPPING_JORDAO.items()}
    selected_original_params_jordao = [reverse_mapping_jordao.get(p, p) for p in selected_params_jordao]
    
    results_jordao = [] 
    doses_ordered = list(DOSES_MAPPING.keys()) # Garantir ordem das doses para Kruskal-Wallis
    
    # Configurar subplots
    num_plots_jordao = len(selected_original_params_jordao) 
    
    if num_plots_jordao > 0: 
        fig_jordao = plt.figure(figsize=(10, 6 * num_plots_jordao)) 
        gs_jordao = fig_jordao.add_gridspec(num_plots_jordao, 1, hspace=0.6) # Espaço vertical entre gráficos 
        
        axes_jordao = [] 
        for i in range(num_plots_jordao): 
            ax = fig_jordao.add_subplot(gs_jordao[i]) 
            axes_jordao.append(ax)
    
        for i, param in enumerate(selected_original_params_jordao): 
            param_df_jordao = df_jordao[df_jordao['Parameter'] == param] 
            
            # Coletar dados por dose para Kruskal-Wallis
            data_by_dose = []
            valid_doses = []
            for dose in doses_ordered:
                if dose in param_df_jordao.columns: # Verificar se a coluna da dose existe
                    dose_data = param_df_jordao[dose].dropna().values
                    if len(dose_data) > 0:
                        data_by_dose.append(dose_data)
                        valid_doses.append(dose)
            
            # Executar teste de Kruskal-Wallis (se houver pelo menos 2 grupos com dados)
            if len(data_by_dose) >= 2: 
                try: 
                    h_stat, p_val = kruskal(*data_by_dose) 
                    results_jordao.append({
                        "Parâmetro": PARAM_MAPPING_JORDAO.get(param, param), 
                        "H-Statistic": h_stat, 
                        "p-value": p_val, 
                        "Significativo (p<0.05)": p_val < 0.05 
                    })
                    
                    # Plotar gráfico
                    ax = axes_jordao[i] 
                    plot_parameter_comparison_doses(ax, data_by_dose, valid_doses, param) # Usar a nova função de plotagem
                    
                    # Adicionar resultado do teste
                    annotation_text = f"Kruskal-Wallis: H = {h_stat:.2f}, p = {p_val:.4f}" 
                    ax.text( 
                        0.5, 0.95, 
                        annotation_text, 
                        transform=ax.transAxes, 
                        ha='center', 
                        va='top', 
                        fontsize=11, 
                        color='white', 
                        bbox=dict( 
                            boxstyle="round,pad=0.3", 
                            facecolor='#2a2f45', 
                            alpha=0.8, 
                            edgecolor='none' 
                        )
                    )
                except ValueError as e:
                     st.warning(f"Não foi possível realizar o teste Kruskal-Wallis para {PARAM_MAPPING_JORDAO.get(param, param)}: {e}. Certifique-se de que há variação nos dados de doses/tratamentos.")
                except Exception as e: 
                    st.error(f"Ocorreu um erro inesperado ao processar {PARAM_MAPPING_JORDAO.get(param, param)}: {e}")
                    continue 
            else:
                st.warning(f"Dados insuficientes para {PARAM_MAPPING_JORDAO.get(param, param)} para realizar o teste de comparação entre doses (mínimo de 2 doses com dados).") 
                continue
    else: 
        st.warning("Nenhum parâmetro selecionado para análise.") 
        return

    # Resultados Estatísticos
    st.markdown("""
    <div class="card">
        <h2 style="display:flex;align-items:center;gap:10px;">
            <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                📈 Resultados Estatísticos
            </span>
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    if results_jordao: 
        results_df_jordao = pd.DataFrame(results_jordao) 
        results_df_jordao['Significância'] = results_df_jordao['p-value'].apply( 
            lambda p: "✅ Sim" if p < 0.05 else "❌ Não" 
        ) 
        
        results_df_jordao = results_df_jordao[['Parâmetro', 'H-Statistic', 'p-value', 'Significância']] 
        
        st.dataframe(
            results_df_jordao.style
            .format({"p-value": "{:.4f}", "H-Statistic": "{:.2f}"}) 
            .set_properties(**{ 
                'color': 'white', 
                'background-color': '#131625', 
            }) 
            .apply(lambda x: ['background: rgba(70, 80, 150, 0.3)' if x['p-value'] < 0.05 else '' for i in x], axis=1) 
        ) 
    else: 
        st.info("Nenhum resultado estatístico disponível.") 
    
    # Gráficos
    if num_plots_jordao > 0: 
        st.markdown("""
        <div class="card">
            <h2 style="display:flex;align-items:center;gap:10px;">
                <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                    📊 Comparação dos Parâmetros por Doses/Tratamentos
                </span>
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="graph-spacer"></div>', unsafe_allow_html=True) 
        
        plt.tight_layout() 
        st.pyplot(fig_jordao) 
        plt.close(fig_jordao) 
    
    # Interpretação
    display_jordao_results_interpretation(results_jordao) 
    
    # Referência Bibliográfica (Formato ABNT)
    st.markdown("""
    <div class="card">
        <h2 style="display:flex;align-items:center;gap:10px;">
            <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                📚 Referência Bibliográfica
            </span>
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="reference-card">
        <p style="line-height:1.8; text-align:justify;">
            JORDÃO, C.P.; FIALHO, L.L.; NEVES, J.C.L.; CECON, P.R.; MENDONÇA, E.S.; FONTES, R.L.F. 
            Reduction of heavy metal contents in liquid effluents by vermicomposts and the use of the metal-enriched vermicomposts in lettuce cultivation. 
            <strong>Bioresource Technology</strong>, 
            v. 98, p. 2800-2813, 2007.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ===================================================================
# ROTEADOR PRINCIPAL
# ===================================================================
def main():
    # Inicializar estado da sessão
    if 'selected_article' not in st.session_state:
        st.session_state['selected_article'] = None
    
    if st.session_state['selected_article'] == 'dermendzhieva':
        run_dermendzhieva_analysis()
    elif st.session_state['selected_article'] == 'jordao':
        run_jordao_analysis()
    else:
        show_homepage()

if __name__ == "__main__":
    main()
