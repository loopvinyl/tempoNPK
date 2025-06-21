import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import kruskal
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MaxNLocator

# Configurações gerais com tema escuro
st.set_page_config(
    page_title="Análise de Vermicompostos",  # Título alterado
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
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h2 style="color:#e0e5ff;">Dermendzhieva et al. (2021)</h2>
            <p style="color:#a0a7c0;">Análise temporal de parâmetros de vermicomposto</p>
            <ul class="custom-list">
                <li>Evolução ao longo de 120 dias</li>
                <li>Parâmetros: TKN, Fósforo, Potássio</li>
                <li>Teste de Kruskal-Wallis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Selecionar Artigo", key="btn_dermendzhieva"):
            st.session_state['selected_article'] = 'dermendzhieva'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="card">
            <h2 style="color:#e0e5ff;">Jordão et al. (2007)</h2>
            <p style="color:#a0a7c0;">Remoção de metais pesados e cultivo de alface</p>
            <ul class="custom-list">
                <li>Comparação entre tratamentos</li>
                <li>Metais: Cobre, Níquel, Zinco</li>
                <li>Absorção por folhas e raízes</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Selecionar Artigo", key="btn_jordao"):
            st.session_state['selected_article'] = 'jordao'
            st.rerun()

# ===================================================================
# MÓDULO DERMENDZHIEVA ET AL. (2021) - ANÁLISE TEMPORAL
# ===================================================================
def run_dermendzhieva_analysis():
    """Módulo original de análise temporal"""
    
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
        'Day 90': 90,
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
        use_sample = st.checkbox("Usar dados de exemplo", value=True, key="use_sample")
        distribution_type = "LogNormal"
    
    with col2:
        # Carregar dados temporariamente para obter os parâmetros
        temp_df = load_sample_data_with_stdev(distribution_type)
        unique_params = temp_df['Parameter'].unique()
        param_options = [PARAM_MAPPING.get(p, p) for p in unique_params]
        
        selected_params = st.multiselect(
            "Selecione os parâmetros:",
            options=param_options,
            default=param_options,
            key="param_select"
        )
    
    # Carregar dados
    df = load_sample_data_with_stdev(distribution_type)
    
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
# MÓDULO JORDÃO ET AL. (2007) - ANÁLISE COMPARATIVA
# ===================================================================
def run_jordao_analysis():
    """Módulo para análise comparativa de tratamentos"""
    
    # Mapeamento de parâmetros
    PARAM_MAPPING = {
        "pH": "pH",
        "Organic Matter": "Matéria Orgânica",
        "C/N ratio": "Relação C/N",
        "Cu": "Cobre",
        "Ni": "Níquel",
        "Zn": "Zinco",
        "Cu_leaves": "Cobre nas Folhas",
        "Ni_leaves": "Níquel nas Folhas",
        "Zn_leaves": "Zinco nas Folhas",
        "Cu_roots": "Cobre nas Raízes",
        "Ni_roots": "Níquel nas Raízes",
        "Zn_roots": "Zinco nas Raízes",
    }
    
    # Função para carregar dados específicos do artigo
    @st.cache_data
    def load_jordao_sample_data():
        sample_data = {
            'Vermicompost Characterization': {
                'pH': {'mean': 7.1, 'stdev': 0.03},
                'Organic Matter': {'mean': 42.0, 'stdev': 0.34},
                'C/N ratio': {'mean': 11.85, 'stdev': 0.2},
                'Cu': {'mean': 31.0, 'stdev': 6.7},
                'Ni': {'mean': 21.7, 'stdev': 2.1},
                'Zn': {'mean': 108, 'stdev': 4.4}
            },
            'Lettuce Cultivation': {
                'Cu_leaves': {'mean': 8.1, 'stdev': 1.5},
                'Ni_leaves': {'mean': 35.3, 'stdev': 3.2},
                'Zn_leaves': {'mean': 1074.8, 'stdev': 85},
                'Cu_roots': {'mean': 246.3, 'stdev': 25},
                'Ni_roots': {'mean': 587.7, 'stdev': 45},
                'Zn_roots': {'mean': 1339.2, 'stdev': 120}
            }
        }
        
        num_replications = 3
        data = []
        
        for treatment, params in sample_data.items():
            for param_name, stats in params.items():
                for _ in range(num_replications):
                    row = {'Parameter': param_name, 'Treatment': treatment}
                    row['Value'] = np.random.normal(stats['mean'], stats['stdev'])
                    # Garantir valores não-negativos
                    if 'leaves' in param_name or 'roots' in param_name:
                        row['Value'] = max(0, row['Value'])
                    data.append(row)
        
        return pd.DataFrame(data)
    
    # Função para plotar comparação entre tratamentos
    def plot_parameter_comparison(ax, data, treatment_names, param_name):
        colors = ['#6f42c1', '#00c1e0', '#00d4b1']
        
        for i, (treatment_data, treatment_name) in enumerate(zip(data, treatment_names)):
            # Plotar pontos individuais
            ax.scatter(
                [i] * len(treatment_data),  
                treatment_data,
                color=colors[i],
                alpha=0.7,
                s=80,
                label=treatment_name,
                edgecolors='white',
                linewidth=1,
                zorder=3
            )
            
            # Plotar mediana
            median_val = np.median(treatment_data)
            ax.plot(
                [i-0.2, i+0.2],
                [median_val, median_val],
                color='white',
                linewidth=3,
                zorder=5
            )
        
        # Configurações do gráfico
        ax.set_xticks(range(len(treatment_names)))
        ax.set_xticklabels(treatment_names, fontsize=11)
        ax.set_ylabel(PARAM_MAPPING.get(param_name, param_name), fontsize=12, fontweight='bold')
        ax.set_title(f"Comparação de {PARAM_MAPPING.get(param_name, param_name)} entre Tratamentos",  
                                  fontsize=14, fontweight='bold', pad=15)
        ax.legend(loc='best', fontsize=10, framealpha=0.3)
        ax.grid(True, alpha=0.2, linestyle='--', color='#a0a7c0')
        
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
                            <b>Rejeitamos a hipótese nula (H₀)</b>
                        </p>
                        <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                            <span style="color:#00c853; font-size:1.5rem;">•</span>
                            Há evidências de que os valores do parâmetro diferem significativamente entre os tratamentos.
                        </p>
                        <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                            <span style="color:#00c853; font-size:1.5rem;">•</span>
                            O tratamento de vermicompostagem (ou as condições de cultivo) afetou este parâmetro.
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
                            Não há evidências suficientes para afirmar que os valores do parâmetro diferem significativamente entre os tratamentos.
                        </p>
                        <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                            <span style="color:#ff5252; font-size:1.5rem;">•</span>
                            O parâmetro parece não ser influenciado pelos diferentes tratamentos aplicados.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)

    # Interface principal do módulo
    st.markdown("""
    <div class="header-card">
        <h1 style="margin:0;padding:0;background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-size:2.5rem;">
            ⚗️ Análise de Remoção de Metais Pesados e Cultivo
        </h1>
        <p style="margin:0;padding-top:10px;color:#a0a7c0;font-size:1.1rem;">
        Jordão et al. (2007) - Vermicompostagem de resíduos da indústria de celulose
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Voltar para seleção de artigos", key="btn_back_jordao"):
        del st.session_state['selected_article']
        st.rerun()
    
    st.markdown("""
    <div class="card">
        <h2 style="display:flex;align-items:center;gap:10px;">
            <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                ⚙️ Configurações de Análise
            </span>
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    df = load_jordao_sample_data()
    
    analysis_type = st.radio(
        "Selecione o tipo de análise:",
        ["Caracterização do Vermicomposto", "Cultivo de Alface"],
        key="analysis_type_jordao"
    )
    
    # Filtrar opções de parâmetro baseadas no tipo de análise
    if analysis_type == "Caracterização do Vermicomposto":
        options = [p for p in df['Parameter'].unique() if not ("leaves" in p or "roots" in p)]
    else:
        options = [p for p in df['Parameter'].unique() if "leaves" in p or "roots" in p]

    param_options_display = [PARAM_MAPPING.get(p, p) for p in options]
    
    selected_params = st.multiselect(
        "Selecione os parâmetros para análise:",
        options=param_options_display,
        default=param_options_display[:min(2, len(param_options_display))],
        key="jordao_param_select"
    )
    
    if not selected_params:
        st.warning("Selecione ao menos um parâmetro para análise.")
        return

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
    
    st.markdown("""
    <div class="info-card">
        <h3 style="display:flex;align-items:center;color:#00c1e0;">
            <span class="info-icon">ℹ️</span> Como as amostras foram produzidas
        </h3>
        <div style="margin-top:15px; color:#d7dce8; line-height:1.7;">
            <p>
                As amostras para esta análise são geradas por simulação com base em dados de média e desvio padrão. Cada ponto de dado é criado usando uma <b>distribuição normal</b> para simular a variabilidade dos experimentos reais. Para parâmetros como concentrações de metais em plantas, os valores são ajustados para garantir que não sejam negativos, refletindo a natureza física dos dados.
            </p>
            <p>
                Essa abordagem permite explorar a variabilidade esperada dos resultados em diferentes tratamentos ou condições de cultivo, como a caracterização do vermicomposto e a absorção de metais por alface.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # Converter de volta para nomes originais
    reverse_mapping_jordao = {v: k for k, v in PARAM_MAPPING.items()}
    selected_original_params_jordao = [reverse_mapping_jordao.get(p, p) for p in selected_params]
    
    results_jordao = []
    
    num_plots_jordao = len(selected_params)
    
    if num_plots_jordao > 0:
        fig_jordao = plt.figure(figsize=(10, 6 * num_plots_jordao))
        gs_jordao = fig_jordao.add_gridspec(num_plots_jordao, 1, hspace=0.6)
        
        axes_jordao = []
        for i in range(num_plots_jordao):
            ax = fig_jordao.add_subplot(gs_jordao[i])
            axes_jordao.append(ax)

        for i, param in enumerate(selected_original_params_jordao):
            param_data = []
            treatment_names = []
            
            # Coletar dados por tratamento
            for treat in df['Treatment'].unique():
                # Filtrar apenas os parâmetros relevantes para o tipo de análise selecionado
                if (analysis_type == "Caracterização do Vermicomposto" and not ("leaves" in param or "roots" in param)) or \
                   (analysis_type == "Cultivo de Alface" and ("leaves" in param or "roots" in param)):
                    
                    vals = df[(df['Parameter'] == param) & (df['Treatment'] == treat)]['Value'].dropna().values
                    if len(vals) > 1:
                        param_data.append(vals)
                        treatment_names.append(treat)
            
            # Executar teste de Kruskal-Wallis
            if len(param_data) >= 2:
                try:
                    h_stat, p_val = kruskal(*param_data)
                    results_jordao.append({
                        "Parâmetro": PARAM_MAPPING.get(param, param),
                        "H-Statistic": h_stat,
                        "p-value": p_val,
                        "Significativo (p<0.05)": p_val < 0.05
                    })
                    
                    # Plotar gráfico
                    ax = axes_jordao[i]
                    plot_parameter_comparison(ax, param_data, treatment_names, param)
                    
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
            .apply(lambda x: ['background: rgba(70, 80, 150, 0.3)' 
                                 if x['p-value'] < 0.05 else '' for i in x], axis=1)
        )
    else:
        st.info("Nenhum resultado estatístico disponível.")
    
    # Gráficos
    if num_plots_jordao > 0:
        st.markdown("""
        <div class="card">
            <h2 style="display:flex;align-items:center;gap:10px;">
                <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                    📊 Comparação de Parâmetros entre Tratamentos
                </span>
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="graph-spacer"></div>', unsafe_allow_html=True)
        plt.tight_layout()
        st.pyplot(fig_jordao)
        plt.close(fig_jordao)
    
    # Interpretação
    display_results_interpretation(results_jordao)
    
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
            JORDÃO, C. L.; PEREIRA, M. G.; FONTANELLA, S. A.; et al. 
            Vermicompostagem de resíduos da indústria de celulose para produção de substrato agrícola e remediação de metais pesados. 
            <strong>Revista Brasileira de Ciência do Solo</strong>, 
            v. 31, p. 741-750, 2007. 
            Disponível em: https://www.scielo.br/j/rbcs/a/5NfK4ZgM7Q8J2yYqT8j6X3S/?lang=pt. 
            Acesso em: 21 jun. 2023.
        </p>
        <p style="margin-top:20px; font-style:italic;">
            Nota: Os dados utilizados nesta análise são baseados no estudo supracitado. 
            Para mais detalhes metodológicos e resultados completos, consulte o artigo original.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ===================================================================
# ROTEAMENTO PRINCIPAL
# ===================================================================
def main():
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
