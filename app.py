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

# CSS para tema escuro premium com cards clicáveis
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
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        border-color: rgba(100, 110, 200, 0.4);
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
    
    /* Botões invisíveis */
    .invisible-button {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        opacity: 0;
        cursor: pointer;
        z-index: 2;
    }
    
    .card-container {
        position: relative;
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

# ===================================================================
# TELA INICIAL
# ===================================================================
def show_homepage():
    """Tela inicial de seleção de artigo"""
    st.markdown(f"""
    <div class="header-card">
        <h1 style="margin:0;padding:0;background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-size:2.5rem;">
            🪱 Análise de Vermicompostos
        </h1>
        <p style="margin:0;padding-top:10px;color:#a0a7c0;font-size:1.1rem;">
            Selecione um artigo abaixo para realizar a análise estatística
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Container para o card clicável
        with st.container():
            st.markdown("""
            <div class="card-container">
                <div class="card">
                    <h2 style="color:#e0e5ff;">Dermendzhieva et al. (2021)</h2>
                    <p style="color:#a0a7c0;">Análise temporal de parâmetros de vermicomposto</p>
                    <ul class="custom-list">
                        <li>Evolução ao longo de 120 dias</li>
                        <li>Parâmetros: TKN, Fósforo, Potássio</li>
                        <li>Teste de Kruskal-Wallis</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Botão invisível que cobre todo o card
            if st.button("Selecionar Dermendzhieva", key="btn_dermendzhieva", 
                         help="Clique para selecionar este artigo",
                         use_container_width=True,
                         type="primary"):
                st.session_state['selected_article'] = 'dermendzhieva'
                st.rerun()
    
    with col2:
        # Container para o card clicável
        with st.container():
            st.markdown("""
            <div class="card-container">
                <div class="card">
                    <h2 style="color:#e0e5ff;">Jordão et al. (2007)</h2>
                    <p style="color:#a0a7c0;">Remoção de metais pesados e cultivo de alface</p>
                    <ul class="custom-list">
                        <li>Comparação entre doses de vermicomposto</li>
                        <li>Metais: Cobre, Níquel, Zinco</li>
                        <li>Absorção por folhas e raízes</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Botão invisível que cobre todo o card
            if st.button("Selecionar Jordão", key="btn_jordao", 
                         help="Clique para selecionar este artigo",
                         use_container_width=True,
                         type="primary"):
                st.session_state['selected_article'] = 'jordao'
                st.rerun()
                
    with col3:
        # Container para o card clicável
        with st.container():
            st.markdown("""
            <div class="card-container">
                <div class="card">
                    <h2 style="color:#e0e5ff;">Sharma (2019)</h2>
                    <p style="color:#a0a7c0;">Comparação de vermicompostos por espécie</p>
                    <ul class="custom-list">
                        <li>Três espécies de minhocas epigeicas</li>
                        <li>Parâmetros: N, P, K, pH, C/N</li>
                        <li>Comparação com solo original</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Botão invisível que cobre todo o card
            if st.button("Selecionar Sharma", key="btn_sharma", 
                         help="Clique para selecionar este artigo",
                         use_container_width=True,
                         type="primary"):
                st.session_state['selected_article'] = 'sharma'
                st.rerun()

# ===================================================================
# MÓDULO DERMENDZHIEVA ET AL. (2021) - ANÁLISE TEMPORAL
# ===================================================================
def run_dermendzhieva_analysis():
    """Módulo de análise temporal corrigido"""
    
    # Mapeamento de parâmetros
    PARAM_MAPPING = {
        "TKN (g/kg)": "Nitrogênio Total (N)",
        "Total P (g/kg)": "Fósforo Total (P)",
        "TK (g/kg)": "Potássio Total (K)",
        "pH (H₂O)": "pH",
        "C/N ratio": "Relação C/N"
    }

    # Mapeamento de dias
    DAY_MAPPING = {
        'Day 1': 1,
        'Day 30': 30,
        'Day 60': 60,
        'Day 90': 90, # Corrected '极 90' to 'Day 90'
        'Day 120': 120
    }

    # Função para carregar dados de exemplo
    @st.cache_data
    def load_sample_data_with_stdev(distribution_type='Normal'):
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
                        if distribution_type == 'Normal':
                            simulated_value = np.random.normal(
                                loc=stats['mean'], 
                                scale=stats['stdev']
                            )
                        elif distribution_type == 'LogNormal':
                            mu = stats['mean']
                            sigma = stats['stdev']
                            if sigma <= 0:
                                log_sigma = 0
                                log_mu = np.log(mu)
                            else:
                                log_sigma = np.sqrt(np.log(1 + (sigma/mu)**2))
                                log_mu = np.log(mu) - 0.5 * log_sigma**2
                            
                            simulated_value = np.random.lognormal(
                                mean=log_mu,
                                sigma=log_sigma
                            )
                        else:
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
                all_replicated_data.append(row_data)

        return pd.DataFrame(all_replicated_data)
    
    # Função para plotar evolução temporal
    def plot_parameter_evolution(ax, data, days, param_name):
        # Converter dias para numérico para ordenação
        numeric_days = [DAY_MAPPING[d] for d in days]
        
        # Paleta de cores moderna
        colors = ['#6f42c1', '#00c1e0', '#00d4b1', '#ffd166', '#ff6b6b']
        
        for i, (day, num_day) in enumerate(zip(days, numeric_days)):
            group_data = data[i]
            
            # Plotar pontos individuais com efeito de profundidade
            ax.scatter(
                [num_day] * len(group_data), 
                group_data, 
                alpha=0.85, 
                s=100,
                color=colors[i % len(colors)],
                edgecolors='white',
                linewidth=1.2,
                zorder=3,
                label=f"{day.replace('Day ', 'Dia ')}",
                marker='o'
            )
        
        # Calcular e plotar medianas com estilo premium
        medians = [np.median(group) for group in data]
        ax.plot(
            numeric_days, 
            medians, 
            'D-', 
            markersize=10,
            linewidth=3,
            color='#ffffff',
            markerfacecolor='#6f42c1',
            markeredgecolor='white',
            markeredgewidth=1.5,
            zorder=5,
            alpha=0.95
        )
        
        # Configurar eixo X com dias numéricos
        ax.set_xticks(numeric_days)
        ax.set_xticklabels([d.replace('Day ', '') for d in days], fontsize=11)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        
        # Melhorar formatação
        ax.set_xlabel("Dias de Vermicompostagem", fontsize=12, fontweight='bold', labelpad=15)
        ax.set_ylabel(PARAM_MAPPING.get(param_name, param_name), fontsize=12, fontweight='bold', labelpad=15)
        ax.set_title(f"Evolução do {PARAM_MAPPING.get(param_name, param_name)}", 
                             fontsize=14, fontweight='bold', pad=20)
        
        # Grid e estilo
        ax.grid(True, alpha=0.2, linestyle='--', color='#a0a7c0', zorder=1)
        ax.legend(loc='best', fontsize=10, framealpha=0.25)
        
        # Remover bordas
        for spine in ax.spines.values():
            spine.set_visible(False)
        
        # Fundo gradiente
        ax.set_facecolor('#0c0f1d')
        
        return ax

    # Função para exibir resultados
    def display_results_interpretation(results):
        st.markdown("""
        <div class="card">
            <h2 style="display:flex;align-items:center;gap:10px;">
                <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                    📝 Interpretação dos Resultados
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
            is_significant = p_val < 0.05 # Corrected 'p极' to 'p_val'
            
            card_class = "signif-card" if is_significant else "not-signif-card"
            icon = "✅" if is_significant else "❌"
            title_color = "#00c853" if is_significant else "#ff5252"
            status = "Significativo" if is_significant else "Não Significativo"
            
            st.markdown(f"""
            <div class="result-card {card_class}">
                <div style="display:flex; align-items:center; justify-content:space-between;">
                    <div style="display:flex; align-items:center; gap:12px;">
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
                st.markdown("""
                    <div style="color:#e0e5ff; line-height:1.8;">
                        <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                            <span style="color:#00c853; font-size:1.5rem;">•</span>
                            <b>Rejeitamos a hipótese nula (H₀)</b>
                        </p>
                        <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                            <span style="color:#00c853; font-size:1.5rem;">•</span>
                            Há evidências de que os valores do parâmetro mudam significativamente ao longo do tempo
                        </p>
                        <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                            <span style="color:#00c853; font-size:1.5rem;">•</span>
                            A vermicompostagem afeta este parâmetro
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="color:#e0e5ff; line-height:1.8;">
                        <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                            <span style="color:#ff5252; font-size:1.5rem;">•</span>
                            <b>Aceitamos a hipótese nula (H₀)</b>
                        </p>
                        <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                            <span style="color:#ff5252; font-size:1.5rem;">•</span>
                            Não há evidências suficientes de mudanças significativas
                        </p>
                        <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                            <span style="color:#ff5252; font-size:1.5rem;">•</span>
                            O parâmetro permanece estável durante o processo de vermicompostagem
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)

    # Interface principal do módulo
    st.markdown("""
    <div class="header-card">
        <h1 style="margin:0;padding:0;background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-size:2.5rem;">
            📊 Análise Temporal de Parâmetros de Vermicomposto
        </h1>
        <p style="margin:0;padding-top:10px;color:#a0a7c0;font-size:1.1rem;">
        Dermendzhieva et al. (2021) - Vermicompostagem de diferentes materiais orgânicos
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Voltar para seleção de artigos"):
        del st.session_state['selected_article']
        st.rerun()
    
    # Painel de configurações (agora na área principal)
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
        use_sample = st.checkbox("Usar dados de exemplo", value=True, key="use_sample_derm")
        distribution_type = "LogNormal"
    
    # Carregar dados ANTES de tentar acessar colunas
    df = load_sample_data_with_stdev(distribution_type)
    
    with col2:
        unique_params = df['Parameter'].unique()
        param_options = [PARAM_MAPPING.get(p, p) for p in unique_params]
        
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
                As amostras analisadas por esta ferramenta são geradas por simulação computacional a partir de dados de média e desvio padrão. Para cada parâmetro de vermicomposto e para cada ponto de tempo do experimento, nossa ferramenta utiliza a <b>média</b> como o valor central e o <b>desvio padrão</b> para definir a variabilidade das amostras individuais.
            </p>
            <p>
                Os dados são simulados utilizando uma Distribuição {distribution_type}.
                <ul>
                    <li><b>Distribuição Normal:</b> Assume que os dados se distribuem simetricamente em torno da média.</li>
                    <li><b>Distribuição Lognormal:</b> Frequentemente usada para dados que são estritamente positivos, assimétricos à direita e comuns em análises ambientais e biológicas. Seus logaritmos naturais seguem uma distribuição normal.</li>
                </ul>
                Aplicamos regras para garantir que os valores simulados de pH permaneçam dentro da escala lógica (0 a 14) e que as concentrações de substâncias não sejam negativas, tornando as amostras mais realistas para dados de vermicompostagem.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # Realizar Análise
    if not selected_params:
        st.warning("Selecione pelo menos um parâmetro para análise.")
        return

    # Converter de volta para nomes originais
    reverse_mapping = {v: k for k, v in PARAM_MAPPING.items()}
    selected_original_params = [reverse_mapping.get(p, p) for p in selected_params]
    
    results = []
    days_ordered = ['Day 1', 'Day 30', 'Day 60', 'Day 90', 'Day 120']
    
    # Configurar subplots
    num_plots = len(selected_params)
    
    if num_plots > 0:
        # Criar figura com espaço adicional entre os subplots
        fig = plt.figure(figsize=(10, 6 * num_plots))
        
        # Usar GridSpec para controlar o espaçamento
        gs = fig.add_gridspec(num_plots, 1, hspace=0.6)  # Espaço vertical entre gráficos
        
        axes = []
        for i in range(num_plots):
            ax = fig.add_subplot(gs[i])
            axes.append(ax)
    
        for i, param in enumerate(selected_original_params):
            param_df = df[df['Parameter'] == param]
            
            # Coletar dados por dia
            data_by_day = []
            valid_days = []
            for day in days_ordered:
                if day in param_df.columns:
                    day_data = param_df[day].dropna().values
                    if len(day_data) > 0:
                        data_by_day.append(day_data)
                        valid_days.append(day)
            
            # Executar teste de Kruskal-Wallis
            if len(data_by_day) >= 2:
                try:
                    h_stat, p_val = kruskal(*data_by_day)
                    results.append({
                        "Parâmetro": PARAM_MAPPING.get(param, param),
                        "H-Statistic": h_stat,
                        "p-value": p_val,
                        "Significativo (p<0.05)": p_val < 0.05
                    })
                    
                    # Plotar gráfico
                    ax = axes[i]
                    plot_parameter_evolution(ax, data_by_day, valid_days, param)
                    
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
                except Exception as e:
                    st.error(f"Erro ao processar {param}: {str(e)}")
                    continue
            else:
                st.warning(f"Dados insuficientes para {PARAM_MAPPING.get(param, param)}")
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
    
    if results:
        # Formatar a tabela de resultados
        results_df = pd.DataFrame(results)
        results_df['Significância'] = results_df['p-value'].apply(
            lambda p: "✅ Sim" if p < 0.05 else "❌ Não"
        )
        
        # Reordenar colunas
        results_df = results_df[['Parâmetro', 'H-Statistic', 'p-value', 'Significância']]
        
        # Estilizar a tabela
        st.dataframe(
            results_df.style
            .format({"p-value": "{:.4f}", "H-Statistic": "{:.2f}"})
            .set_properties(**{
                'color': 'white',
                'background-color': '#131625',
            })
            .apply(lambda x: ['background: rgba(70, 80, 150, 0.3)' 
                               if x['p-value'] < 0.05 else '' for i in x], axis=1)
        )
    else:
        st.info("Nenhum resultado estatístico disponível.")
    
    # Gráficos
    if num_plots > 0:
        st.markdown("""
        <div class="card">
            <h2 style="display:flex;align-items:center;gap:10px;">
                <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                    📊 Evolução Temporal dos Parâmetros
                </span>
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Adicionar espaçamento visual entre os gráficos
        st.markdown('<div class="graph-spacer"></div>', unsafe_allow_html=True)
        
        # Ajustar layout com espaço adicional
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    
    # Interpretação
    display_results_interpretation(results)
    
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
            DERMENDZHIEVA, D.; WRBKA, T.; KÜHBACHER, T. M.; et al. 
            Vermicomposting of different organic materials using the earthworm species Eisenia fetida. 
            <strong>Environmental Science and Pollution Research</strong>, 
            v. 28, p. 12372–12389, 2021. 
            Disponível em: https://doi.org/10.1007/s11356-020-11285-y. 
            Acesso em: 21 jun. 2023.
        </p>
        <p style="margin-top:20px; font-style:italic;">
            Nota: Os dados utilizados nesta análise são baseados no estudo supracitado. 
            Para mais detalhes metodológicos e resultados completos, consulte o artigo original.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ===================================================================
# MÓDULO JORDÃO ET AL. (2007) - ANÁLISE POR DOSE
# ===================================================================
def run_jordao_analysis():
    """Módulo para análise de doses com geração de amostras"""
    
    # Mapeamento de parâmetros
    PARAM_MAPPING = {
        "Cu_leaves": "Cobre nas Folhas (mg/kg)",
        "Ni_leaves": "Níquel nas Folhas (mg/kg)",
        "Zn_leaves": "Zinco nas Folhas (mg/kg)",
        "Cu_roots": "Cobre nas Raízes (mg/kg)",
        "Ni_roots": "Níquel nas Raízes (mg/kg)",
        "Zn_roots": "Zinco nas Raízes (mg/kg)",
    }
    
    # Mapeamento de doses
    DOSE_MAPPING = {
        'Dose 0%': 0,
        'Dose 25%': 25,
        'Dose 50%': 50,
        'Dose 100%': 100
    }

    # Função para carregar dados de exemplo
    @st.cache_data
    def load_sample_data(distribution_type='Normal'):
        sample_data = {
            'Dose 0%': {
                'Cu_leaves': {'mean': 8.1, 'stdev': 1.5},
                'Ni_leaves': {'mean': 35.3, 'stdev': 3.2},
                'Zn_leaves': {'mean': 1074.8, 'stdev': 85},
                'Cu_roots': {'mean': 246.3, 'stdev': 25},
                'Ni_roots': {'mean': 587.7, 'stdev': 45},
                'Zn_roots': {'mean': 1339.2, 'stdev': 120}
            },
            'Dose 25%': {
                'Cu_leaves': {'mean': 15.2, 'stdev': 2.1},
                'Ni_leaves': {'mean': 48.5, 'stdev': 4.3},
                'Zn_leaves': {'mean': 1280.5, 'stdev': 95},
                'Cu_roots': {'mean': 320.7, 'stdev': 28},
                'Ni_roots': {'mean': 720.3, 'stdev': 52},
                'Zn_roots': {'mean': 1580.4, 'stdev': 135}
            },
            'Dose 50%': {
                'Cu_leaves': {'mean': 22.8, 'stdev': 2.8},
                'Ni_leaves': {'mean': 62.1, 'stdev': 5.1},
                'Zn_leaves': {'mean': 1520.3, 'stdev': 110},
                'Cu_roots': {'mean': 410.5, 'stdev': 35},
                'Ni_roots': {'mean': 890.7, 'stdev': 65},
                'Zn_roots': {'mean': 1890.2, 'stdev': 150}
            },
            'Dose 100%': {
                'Cu_leaves': {'mean': 38.5, 'stdev': 3.5},
                'Ni_leaves': {'mean': 85.7, 'stdev': 6.8},
                'Zn_leaves': {'mean': 1950.4, 'stdev': 145},
                'Cu_roots': {'mean': 520.8, 'stdev': 42},
                'Ni_roots': {'mean': 1150.2, 'stdev': 85},
                'Zn_roots': {'mean': 2350.5, 'stdev': 180}
            }
        }
        
        num_replications = 4
        all_data = []
        
        for dose, params in sample_data.items():
            for param, stats in params.items():
                for _ in range(num_replications):
                    if distribution_type == 'LogNormal':
                        mu = stats['mean']
                        sigma = stats['stdev']
                        if sigma <= 0:
                            log_sigma = 0
                            log_mu = np.log(mu)
                        else:
                            log_sigma = np.sqrt(np.log(1 + (sigma/mu)**2))
                            log_mu = np.log(mu) - 0.5 * log_sigma**2
                        value = np.random.lognormal(mean=log_mu, sigma=log_sigma)
                    else:
                        value = np.random.normal(stats['mean'], stats['stdev'])
                    
                    # Garantir valores não-negativos
                    value = max(0, value)
                    
                    all_data.append({
                        'Parameter': param,
                        'Dose': dose,
                        'Value': value
                    })
                    
        return pd.DataFrame(all_data)

    # Função para plotar evolução por dose
    def plot_parameter_by_dose(ax, data, doses, param_name):
        # Converter doses para numérico para ordenação
        numeric_doses = [DOSE_MAPPING[d] for d in doses]
        
        # Paleta de cores moderna
        colors = ['#6f42c1', '#00c1e0', '#00d4b1', '#ffd166']
        
        for i, (dose, num_dose) in enumerate(zip(doses, numeric_doses)):
            group_data = data[i]
            
            # Plotar pontos individuais
            ax.scatter(
                [num_dose] * len(group_data), 
                group_data, 
                alpha=0.85, 
                s=100,
                color=colors[i % len(colors)],
                edgecolors='white',
                linewidth=1.2,
                zorder=3,
                label=dose,
                marker='o'
            )
        
        # Calcular e plotar medianas com estilo premium
        medians = [np.median(group) for group in data]
        ax.plot(
            numeric_doses, 
            medians, 
            'D-', 
            markersize=10,
            linewidth=3,
            color='#ffffff',
            markerfacecolor='#6f42c1',
            markeredgecolor='white',
            markeredgewidth=1.5,
            zorder=5,
            alpha=0.95
        )
        
        # Adicionar linhas de referência para níveis tóxicos
        if "Zinco" in param_name and "Folhas" in param_name:
            ax.axhline(y=500, color='#ff6b6b', linestyle='--', alpha=0.7)
            ax.text(5, 520, 'Nível Tóxico', color='#ff6b6b', fontsize=10)
        
        # Configurar eixo X com doses numéricas
        ax.set_xticks(numeric_doses)
        ax.set_xticklabels([d.replace('Dose ', '') for d in doses], fontsize=11)
        
        # Melhorar formatação
        ax.set_xlabel("Dose de Vermicomposto", fontsize=12, fontweight='bold', labelpad=15)
        ax.set_ylabel(PARAM_MAPPING.get(param_name, param_name), fontsize=12, fontweight='bold', labelpad=15)
        ax.set_title(f"Efeito da Dose em {PARAM_MAPPING.get(param_name, param_name)}", 
                     fontsize=14, fontweight='bold', pad=20)
        
        # Grid e estilo
        ax.grid(True, alpha=0.2, linestyle='--', color='#a0a7c0', zorder=1)
        ax.legend(loc='best', fontsize=10, framealpha=0.25)
        
        # Remover bordas
        for spine in ax.spines.values():
            spine.set_visible(False)
        
        # Fundo gradiente
        ax.set_facecolor('#0c0f1d')
        
        return ax

    # Função para exibir resultados com contexto específico
    def display_results_interpretation(results):
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
                <div style="display:flex; align-items:center; justify-content:space-between;">
                    <div style="display:flex; align-items:center; gap:12px;">
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
            
            # Contexto específico para metais pesados
            metal_context = ""
            if "Cobre" in param_name:
                metal_context = """
                <div style="background:#2a2f45;padding:10px;border-radius:8px;margin-top:10px;">
                    <b>Relevância no contexto do artigo:</b> O cobre é um micronutriente essencial 
                    para as plantas, mas em concentrações elevadas pode se tornar tóxico, 
                    afetando o crescimento e desenvolvimento vegetal.
                </div>
                """
            elif "Níquel" in param_name:
                metal_context = """
                <div style="background:#2a2f45;padding:10px;border-radius:8px;margin-top:10px;">
                    <b>Relevância no contexto do artigo:</b> O níquel é um elemento potencialmente 
                    tóxico para plantas mesmo em baixas concentrações. Seu acúmulo em tecidos vegetais 
                    pode indicar contaminação do solo.
                </div>
                """
            elif "Zinco" in param_name:
                metal_context = """
                <div style="background:#2a2f45;padding:10px;border-radius:8px;margin-top:10px;">
                    <b>Relevância no contexto do artigo:</b> O zinco é essencial para o metabolismo 
                    vegetal, porém em altas concentrações pode causar fitotoxicidade e redução 
                    no crescimento das plantas.
                </div>
                """
            
            if is_significant:
                st.markdown(f"""
                <div style="color:#e0e5ff; line-height:1.8;">
                    <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                        <span style="color:#00c853; font-size:1.5rem;">•</span>
                        <b>Diferenças significativas encontradas entre doses</b>
                    </p>
                    <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                        <span style="color:#00c853; font-size:1.5rem;">•</span>
                        A concentração de vermicomposto aplicada afeta este parâmetro de forma estatisticamente detectável
                    </p>
                    {metal_context}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="color:#e0e5ff; line-height:1.8;">
                    <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                        <span style="color:#ff5252; font-size:1.5rem;">•</span>
                        <b>Não foram encontradas diferenças significativas entre doses</b>
                    </p>
                    <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                        <span style="color:#ff5252; font-size:1.5rem;">•</span>
                        A concentração de vermicomposto não afeta este parâmetro de forma estatisticamente detectável
                    </p>
                    {metal_context}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)

    # Interface principal do módulo
    st.markdown("""
    <div class="header-card">
        <h1 style="margin:0;padding:0;background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-size:2.5rem;">
            ⚗️ Análise de Metais Pesados por Dose de Vermicomposto
        </h1>
        <p style="margin:0;padding-top:10px;color:#a0a7c0;font-size:1.1rem;">
        Jordão et al. (2007) - Redução de metais pesados em efluentes líquidos por vermicompostos
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Voltar para seleção de artigos"):
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
        distribution_type = st.radio(
            "Distribuição para geração de amostras:",
            ['Normal', 'LogNormal'],
            index=1,
            key="jordao_distribution"
        )
    
    with col2:
        # Carregar dados
        df = load_sample_data(distribution_type)
        
        # Seleção de parâmetros
        param_options = list(PARAM_MAPPING.keys())
        selected_params = st.multiselect(
            "Selecione os parâmetros:",
            options=param_options,
            default=param_options[:3],
            key="jordao_param_select"
        )
    
    # Pré-visualização dos dados
    st.markdown("""
    <div class="card">
        <h2 style="display:flex;align-items:center;gap:10px;">
            <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                🔍 Dados do Estudo
            </span>
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(df)
    st.markdown(f"**Total de amostras:** {len(df)}")
    
    # Explicação sobre geração de dados
    st.markdown(f"""
    <div class="info-card">
        <h3 style="display:flex;align-items:center;color:#00c1e0;">
            <span class="info-icon">ℹ️</span> Como as amostras foram produzidas
        </h3>
        <div style="margin-top:15px; color:#d7dce8; line-height:1.7;">
            <p>
                Os dados foram simulados a partir de médias e desvios padrão reportados no estudo de Jordão et al. (2007). 
                Para cada combinação de parâmetro e dose, foram geradas <b>4 réplicas</b> utilizando uma distribuição {distribution_type}.
            </p>
            <p>
                <b>Doses analisadas:</b>
                <ul>
                    <li><b>0%:</b> Controle (sem vermicomposto)</li>
                    <li><b>25%:</b> Baixa concentração</li>
                    <li><b>50%:</b> Concentração média</li>
                    <li><b>100%:</b> Alta concentração</li>
                </ul>
                Todos os valores foram garantidos como não-negativos para representar adequadamente concentrações de metais.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # Realizar análise
    if not selected_params:
        st.warning("Selecione pelo menos um parâmetro para análise.")
        return
    
    results = []
    doses_ordered = ['Dose 0%', 'Dose 25%', 'Dose 50%', 'Dose 100%']
    
    # Configurar subplots
    num_plots = len(selected_params)
    
    if num_plots > 0:
        fig = plt.figure(figsize=(10, 6 * num_plots))
        gs = fig.add_gridspec(num_plots, 1, hspace=0.6)
        axes = [fig.add_subplot(gs[i]) for i in range(num_plots)]
    
        for i, param in enumerate(selected_params):
            param_df = df[df['Parameter'] == param]
            
            # Coletar dados por dose
            data_by_dose = []
            valid_doses = []
            for dose in doses_ordered:
                dose_data = param_df[param_df['Dose'] == dose]['Value'].dropna().values
                if len(dose_data) > 0:
                    data_by_dose.append(dose_data)
                    valid_doses.append(dose)
            
            # Executar teste de Kruskal-Wallis
            if len(data_by_dose) >= 2:
                try:
                    h_stat, p_val = kruskal(*data_by_dose)
                    results.append({
                        "Parâmetro": PARAM_MAPPING.get(param, param),
                        "H-Statistic": h_stat,
                        "p-value": p_val,
                        "Significativo (p<0.05)": p_val < 0.05
                    })
                    
                    # Plotar gráfico
                    ax = axes[i]
                    plot_parameter_by_dose(ax, data_by_dose, valid_doses, param)
                    
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
                except Exception as e:
                    st.error(f"Erro ao processar {param}: {str(e)}")
                    continue
            else:
                st.warning(f"Dados insuficientes para {PARAM_MAPPING.get(param, param)}")
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
    
    if results:
        results_df = pd.DataFrame(results)
        results_df['Significância'] = results_df['p-value'].apply(
            lambda p: "✅ Sim" if p < 0.05 else "❌ Não"
        )
        results_df = results_df[['Parâmetro', 'H-Statistic', 'p-value', 'Significância']]
        
        st.dataframe(
            results_df.style
            .format({"p-value": "{:.4f}", "H-Statistic": "{:.2f}"})
            .set_properties(**{'color': 'white', 'background-color': '#131625'})
            .apply(lambda x: ['background: rgba(70, 80, 150, 0.3)' 
                            if x['p-value'] < 0.05 else '' for i in x], axis=1)
        )
    else:
        st.info("Nenhum resultado estatístico disponível.")
    
    # Gráficos
    if num_plots > 0:
        st.markdown("""
        <div class="card">
            <h2 style="display:flex;align-items:center;gap:10px;">
                <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                    📊 Efeito da Dose nos Parâmetros
                </span>
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    
    # Interpretação
    if results:
        display_results_interpretation(results)
    
    # Referência Bibliográfica
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
        <p style="margin-top:15px; font-style:italic;">
            Nota: Os dados utilizados nesta análise são baseados no estudo supracitado. 
            Para mais detalhes metodológicos e resultados completos, consulte o artigo original.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ===================================================================
# MÓDULO SHARMA ET AL. (2019) - COMPARAÇÃO DE VERMICOMPOSTOS
# ===================================================================
def run_sharma_analysis():
    """Módulo para análise comparativa de vermicompostos por espécie"""
    
    # Mapeamento de parâmetros
    PARAM_MAPPING = {
        "pH": "pH",
        "EC": "Condutividade Elétrica (mho)",
        "OC": "Carbono Orgânico (%)",
        "N": "Nitrogênio (%)",
        "P": "Fósforo (%)",
        "K": "Potássio (%)",
        "Ca": "Cálcio (%)",
        "Mg": "Magnésio (%)",
        "C_N_ratio": "Razão C/N"
    }
    
    # Dados do estudo (extraídos do artigo)
    VERMICOMPOST_DATA = {
        "VKA": {  # Amynthus diffringens
            "pH": (7.38, 0.11),
            "EC": (3.66, 0.78),
            "OC": (11.30, 0.51),
            "N": (1.05, 0.08),
            "P": (2.88, 0.20),
            "K": (1.05, 0.11),
            "Ca": (0.23, 0.04),
            "Mg": (0.15, 0.02),
            "C_N_ratio": (10.71, 0.68)
        },
        "VKM": {  # Metaphire houlleti
            "pH": (7.35, 0.20),
            "EC": (3.51, 0.59),
            "OC": (11.26, 0.17),
            "N": (1.05, 0.15),
            "P": (2.70, 0.05),
            "K": (1.03, 0.03),
            "Ca": (0.24, 0.03),
            "Mg": (0.14, 0.03),
            "C_N_ratio": (11.27, 1.51)
        },
        "VKO": {  # Octolasion tyrateum
            "pH": (7.28, 0.28),
            "EC": (3.82, 0.74),
            "OC": (11.66, 0.34),
            "N": (1.17, 0.20),
            "P": (2.97, 0.32),
            "K": (1.18, 0.15),
            "Ca": (0.26, 0.04),
            "Mg": (0.17, 0.04),
            "C_N_ratio": (10.19, 1.77)
        },
        "Original": {  # Solo original
            "pH": (7.98, 0.01),
            "EC": (1.35, 0.01),
            "OC": (7.96, 0.01),
            "N": (0.38, 0.01),
            "P": (1.23, 0.01),
            "K": (0.11, 0.01),
            "Ca": (0.09, 0.01),
            "Mg": (0.05, 0.01),
            "C_N_ratio": (20.94, 0.01)
        }
    }
    
    # Descrições dos grupos
    GROUP_DESCRIPTIONS = {
        "VKA": "Vermicomposto por Amynthus diffringens",
        "VKM": "Vermicomposto por Metaphire houlleti",
        "VKO": "Vermicomposto por Octolasion tyrateum",
        "Original": "Solo original (controle)"
    }

    # Função para carregar dados de exemplo
    @st.cache_data
    def load_sample_data(num_replications=5):
        all_data = []
        for group, params in VERMICOMPOST_DATA.items():
            for param, (mean, stdev) in params.items():
                for _ in range(num_replications):
                    # Gerar valor com distribuição normal
                    value = np.random.normal(mean, stdev)
                    # Garantir valores fisicamente possíveis
                    if param == "pH":
                        value = np.clip(value, 0, 14)
                    elif param in ["OC", "N", "P", "K", "Ca", "Mg"]:
                        value = max(0, value)
                    
                    all_data.append({
                        "Parameter": param,
                        "Group": group,
                        "Value": value
                    })
                    
        return pd.DataFrame(all_data)

    # Função para plotar comparação entre grupos
    def plot_group_comparison(ax, data, groups, param_name):
        # Paleta de cores moderna
        colors = ['#6f42c1', '#00c1e0', '#00d4b1', '#ffd166']
        
        for i, group in enumerate(groups):
            group_data = data[i]
            
            # Plotar pontos individuais
            ax.scatter(
                [i] * len(group_data), 
                group_data, 
                alpha=0.85, 
                s=100,
                color=colors[i % len(colors)],
                edgecolors='white',
                linewidth=1.2,
                zorder=3,
                label=GROUP_DESCRIPTIONS[group],
                marker='o'
            )
            
            # Plotar média e intervalo de confiança
            mean_val = np.mean(group_data)
            std_val = np.std(group_data)
            
            ax.errorbar(
                i, mean_val, 
                yerr=1.96*std_val/np.sqrt(len(group_data)),
                fmt='o',
                markersize=10,
                color='white',
                markeredgecolor='black',
                markeredgewidth=1.5,
                elinewidth=3,
                capsize=8,
                zorder=5
            )
        
        # Melhorar formatação
        ax.set_xticks(range(len(groups)))
        ax.set_xticklabels([GROUP_DESCRIPTIONS[g] for g in groups], rotation=15, ha="right", fontsize=10)
        
        ax.set_xlabel("Tipo de Amostra", fontsize=12, fontweight='bold', labelpad=15)
        ax.set_ylabel(PARAM_MAPPING.get(param_name, param_name), fontsize=12, fontweight='bold', labelpad=15)
        ax.set_title(f"Comparação de {PARAM_MAPPING.get(param_name, param_name)}", 
                     fontsize=14, fontweight='bold', pad=20)
        
        # Grid e estilo
        ax.grid(True, alpha=0.2, linestyle='--', color='#a0a7c0', zorder=1)
        ax.legend(loc='upper right', fontsize=9, framealpha=0.25)
        
        # Remover bordas
        for spine in ax.spines.values():
            spine.set_visible(False)
        
        # Fundo gradiente
        ax.set_facecolor('#0c0f1d')
        
        return ax

    # Função para exibir resultados
    def display_results_interpretation(results):
        st.markdown("""
        <div class="card">
            <h2 style="display:flex;align-items:center;gap:10px;">
                <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                    📝 Interpretação dos Resultados
                </span>
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        if not results:
            st.info("Nenhuma interpretação disponível.")
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
                <div style="display:flex; align-items:center; justify-content:space-between;">
                    <div style="display:flex; align-items:center; gap:12px;">
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
                st.markdown("""
                    <div style="color:#e0e5ff; line-height:1.8;">
                        <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                            <span style="color:#00c853; font-size:1.5rem;">•</span>
                            <b>Diferenças significativas entre os tipos de vermicomposto</b>
                        </p>
                        <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                            <span style="color:#00c853; font-size:1.5rem;">•</span>
                            A espécie de minhoca influencia significativamente este parâmetro
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Adicionar observação específica para nutrientes
                if "Nitrogênio" in param_name or "Fósforo" in param_name or "Potássio" in param_name:
                    st.markdown("""
                    <div style="background:#2a2f45;padding:10px;border-radius:8px;margin-top:10px;">
                        <b>Relevância agronômica:</b> Os vermicompostos mostraram teores significativamente 
                        maiores de nutrientes em comparação com o solo original, indicando seu potencial 
                        como fertilizante orgânico.
                    </div>
                    """, unsafe_allow_html=True)
                    
            else:
                st.markdown("""
                    <div style="color:#e0e5ff; line-height:1.8;">
                        <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                            <span style="color:#ff5252; font-size:1.5rem;">•</span>
                            <b>Não foram encontradas diferenças significativas</b>
                        </p>
                        <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                            <span style="color:#ff5252; font-size:1.5rem;">•</span>
                            A espécie de minhoca não afeta significativamente este parâmetro
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)

    # Interface principal do módulo
    st.markdown("""
    <div class="header-card">
        <h1 style="margin:0;padding:0;background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-size:2.5rem;">
            🪱 Comparação de Vermicompostos por Espécie de Minhoca
        </h1>
        <p style="margin:0;padding-top:10px;color:#a0a7c0;font-size:1.1rem;">
        Sharma (2019) - Gestão de resíduos de cozinha por vermicompostagem
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Voltar para seleção de artigos"):
        del st.session_state['selected_article']
        st.rerun()
    
    # Painel de informações do estudo
    st.markdown("""
    <div class="card">
        <h2 style="display:flex;align-items:center;gap:10px;">
            <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                🔬 Contexto do Estudo
            </span>
        </h2>
        <div style="margin-top:15px; padding:15px; background:rgba(26,29,50,0.5); border-radius:12px;">
            <p style="line-height:1.7;">
                Este estudo comparou a eficiência de três espécies de minhocas epigeicas locais de Jammu 
                (<i>Amynthus diffringens</i>, <i>Metaphire houlleti</i> e <i>Octolasion tyrateum</i>) 
                na produção de vermicomposto a partir de resíduos de cozinha. Os parâmetros físico-químicos 
                dos vermicompostos resultantes foram analisados e comparados com o solo original.
            </p>
            <p style="margin-top:10px; font-style:italic; color:#a0a7c0;">
                Fonte: Sharma, D. (2019). Kitchen waste management by vermicomposting using locally available 
                epigeic earthworm species. Journal of Applied and Natural Science, 11(2): 372-374
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregar dados
    df = load_sample_data()
    
    # Pré-visualização dos Dados
    st.markdown("""
    <div class="card">
        <h2 style="display:flex;align-items:center;gap:10px;">
            <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                🔍 Dados do Estudo
            </span>
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(df)
    st.markdown(f"**Total de amostras:** {len(df)}")
    
    # Explicação sobre geração de dados
    st.markdown("""
    <div class="info-card">
        <h3 style="display:flex;align-items:center;color:#00c1e0;">
            <span class="info-icon">ℹ️</span> Metodologia de Análise
        </h3>
        <div style="margin-top:15px; color:#d7dce8; line-height:1.7;">
            <p>
                Os dados foram gerados com base nas médias e desvios padrão reportados no estudo de Sharma (2019). 
                Para cada combinação de parâmetro e grupo, foram simuladas <b>5 réplicas</b> utilizando uma distribuição normal.
            </p>
            <p>
                <b>Grupos analisados:</b>
                <ul>
                    <li><b>VKA:</b> Vermicomposto por <i>Amynthus diffringens</i></li>
                    <li><b>VKM:</b> Vermicomposto por <i>Metaphire houlleti</i></li>
                    <li><b>VKO:</b> Vermicomposto por <i>Octolasion tyrateum</i></li>
                    <li><b>Original:</b> Solo original (controle)</li>
                </ul>
            </p>
            <p>
                O teste de Kruskal-Wallis foi aplicado para verificar se existem diferenças significativas 
                entre os grupos para cada parâmetro analisado.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # Seleção de parâmetros
    st.markdown("""
    <div class="card">
        <h2 style="display:flex;align-items:center;gap:10px;">
            <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                ⚙️ Parâmetros para Análise
            </span>
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    param_options = list(PARAM_MAPPING.values())
    selected_params = st.multiselect(
        "Selecione os parâmetros para análise:",
        options=param_options,
        default=param_options[:5],
        key="sharma_param_select"
    )
    
    # Realizar Análise
    if not selected_params:
        st.warning("Selecione pelo menos um parâmetro para análise.")
        return

    # Converter para nomes originais
    reverse_mapping = {v: k for k, v in PARAM_MAPPING.items()}
    selected_original_params = [reverse_mapping[p] for p in selected_params]
    
    results = []
    groups = list(GROUP_DESCRIPTIONS.keys())
    
    # Configurar subplots
    num_plots = len(selected_params)
    
    if num_plots > 0:
        fig = plt.figure(figsize=(10, 6 * num_plots))
        gs = fig.add_gridspec(num_plots, 1, hspace=0.6)
        axes = [fig.add_subplot(gs[i]) for i in range(num_plots)]
    
        for i, param in enumerate(selected_original_params):
            param_df = df[df['Parameter'] == param]
            
            # Coletar dados por grupo
            data_by_group = []
            for group in groups:
                group_data = param_df[param_df['Group'] == group]['Value'].values
                data_by_group.append(group_data)
            
            # Executar teste de Kruskal-Wallis
            try:
                h_stat, p_val = kruskal(*data_by_group)
                results.append({
                    "Parâmetro": PARAM_MAPPING[param],
                    "H-Statistic": h_stat,
                    "p-value": p_val,
                    "Significativo (p<0.05)": p_val < 0.05
                })
                
                # Plotar gráfico
                ax = axes[i]
                plot_group_comparison(ax, data_by_group, groups, param)
                
                # Adicionar resultado do teste
                significance = "SIGNIFICATIVO" if p_val < 0.05 else "NÃO SIGNIFICATIVO"
                color = "#00c853" if p_val < 0.05 else "#ff5252"
                
                annotation_text = f"Kruskal-Wallis: H = {h_stat:.2f}, p = {p_val:.4f} ({significance})"
                ax.text(
                    0.5, 0.95, 
                    annotation_text,
                    transform=ax.transAxes,
                    ha='center',
                    va='top',
                    fontsize=11,
                    color=color,
                    bbox=dict(
                        boxstyle="round,pad=0.3",
                        facecolor='#2a2f45',
                        alpha=0.8,
                        edgecolor='none'
                    )
                )
            except Exception as e:
                st.error(f"Erro ao processar {param}: {str(e)}")
                continue
    
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
        results_df = results_df[['Parâmetro', 'H-Statistic', 'p-value', 'Significância']]
        
        st.dataframe(
            results_df.style
            .format({"p-value": "{:.4f}", "H-Statistic": "{:.2f}"})
            .set_properties(**{
                'color': 'white',
                'background-color': '#131625',
            })
            .apply(lambda x: ['background: rgba(70, 80, 150, 0.3)' 
                               if x['p-value'] < 0.05 else '' for i in x], axis=1)
        )
    else:
        st.info("Nenhum resultado estatístico disponível.")
    
    # Gráficos
    if num_plots > 0:
        st.markdown("""
        <div class="card">
            <h2 style="display:flex;align-items:center;gap:10px;">
                <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                    📊 Comparação entre Grupos
                </span>
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    
    # Interpretação
    display_results_interpretation(results)
    
    # Conclusão do estudo
    st.markdown("""
    <div class="card">
        <h2 style="display:flex;align-items:center;gap:10px;">
            <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                💡 Principais Conclusões do Estudo
            </span>
        </h2>
        <div style="margin-top:15px; padding:20px; background:rgba(26,29,50,0.5); border-radius:12px;">
            <p style="line-height:1.7;">
                1. Todos os vermicompostos apresentaram valores nutricionais significativamente superiores 
                ao solo original, especialmente em Nitrogênio, Fósforo e Potássio.<br><br>
                
                2. O vermicomposto produzido por Octolasion tyrateum (VKO) mostrou os maiores teores 
                de nutrientes entre as espécies testadas.
                
                3. A razão C/N foi significativamente reduzida em todos os vermicompostos em comparação 
                com o solo original, indicando maior maturidade e estabilidade do composto.
                
                4. O estudo demonstra que a vermicompostagem com espécies locais é uma técnica eficaz 
                para transformar resíduos de cozinha em fertilizante orgânico de alta qualidade.
    </div>
    """, unsafe_allow_html=True)
    
    # Referência Bibliográfica
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
            SHARMA, D. Kitchen waste management by vermicomposting using locally available epigeic earthworm species. 
            <strong>Journal of Applied and Natural Science</strong>, 
            v. 11, n. 2, p. 372-374, 2019. 
        </p>
        <p style="margin-top:10px;">
            <strong>DOI:</strong> 10.31018/jans.v11i2.2058
        </p>
        <p style="margin-top:15px; font-style:italic;">
            Nota: Os dados utilizados nesta análise são baseados no estudo supracitado. 
            Para mais detalhes metodológicos e resultados completos, consulte o artigo original.
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
    
    # Roteamento
    if st.session_state['selected_article'] is None:
        show_homepage()
    elif st.session_state['selected_article'] == 'dermendzhieva':
        run_dermendzhieva_analysis()
    elif st.session_state['selected_article'] == 'jordao':
        run_jordao_analysis()
    elif st.session_state['selected_article'] == 'sharma':
        run_sharma_analysis()

if __name__ == "__main__":
    main()
