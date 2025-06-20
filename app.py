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
            all_replicated_data.append(row_data)

    return pd.DataFrame(all_replicated_data)

## Função para plotar evolução temporal com estilo moderno
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

## Função para exibir resultados com design premium
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

## Função Principal
def main():
    # Inicialização de variáveis
    df = load_sample_data_with_stdev()
    
    # Sidebar premium
    with st.sidebar:
        st.markdown("""
        <div class="card">
            <h3 style="display:flex;align-items:center;gap:10px;">
                <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:3px 12px;border-radius:30px;font-size:1rem;">
                    📂 Opções de Dados
                </span>
            </h3>
        """, unsafe_allow_html=True)
        
        use_sample = st.checkbox("Usar dados de exemplo", value=True, key="use_sample")
        
        if not use_sample:
            uploaded_file = st.file_uploader("Carregue o artigo PDF", type="pdf", key="pdf_uploader")
            if uploaded_file:
                st.success("Funcionalidade PDF em desenvolvimento. Usando dados de exemplo.")
            else:
                st.info("Nenhum PDF carregado. Usando dados de exemplo.")
        
        st.markdown("""
        <div class="card">
            <h3 style="display:flex;align-items:center;gap:10px;">
                <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:3px 12px;border-radius:30px;font-size:1rem;">
                    ⚙️ Configuração de Análise
                </span>
            </h3>
        """, unsafe_allow_html=True)
        
        unique_params = df['Parameter'].unique()
        param_options = [PARAM_MAPPING.get(p, p) for p in unique_params]
        
        selected_params = st.multiselect(
            "Selecione os parâmetros:",
            options=param_options,
            default=param_options,
            key="param_select"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h3 style="display:flex;align-items:center;gap:10px;">
                <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:3px 12px;border-radius:30px;font-size:1rem;">
                    📚 Metodologia Estatística
                </span>
            </h3>
            <div style="color:#d7dce8; line-height:1.7;">
                <p><b>Teste de Kruskal-Wallis</b></p>
                <ul style="padding-left:20px;">
                    <li>Alternativa não paramétrica à ANOVA</li>
                    <li>Compara medianas de múltiplos grupos</li>
                    <li>Hipóteses:
                        <ul>
                            <li>H₀: Distribuições idênticas</li>
                            <li>H₁: Pelo menos uma distribuição diferente</li>
                        </ul>
                    </li>
                    <li>Interpretação:
                        <ul>
                            <li>p &lt; 0.05: Diferenças significativas</li>
                            <li>p ≥ 0.05: Sem evidência de diferenças</li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

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
    
    # Explicação detalhada sobre a produção das amostras (CORRIGIDA)
    st.markdown("""
    <div class="info-card">
        <h3 style="display:flex;align-items:center;color:#00c1e0;">
            <span class="info-icon">ℹ️</span> Como as amostras foram produzidas
        </h3>
        <div style="margin-top:15px; color:#d7dce8; line-height:1.7;">
            <p>As amostras foram geradas por simulação computacional seguindo um protocolo rigoroso:</p>
            
            <ol class="custom-list">
                <li><strong>Base em dados científicos</strong>: Valores médios e desvios padrão foram extraídos do estudo de referência</li>
                <li><strong>Estratégia de réplicas</strong>: Para cada combinação de parâmetro/dia, foram geradas 3 réplicas independentes</li>
                <li><strong>Modelagem estatística</strong>: Cada valor foi simulado usando distribuição normal: 
                    <br><code>valor = normal(média, desvio_padrão)</code></li>
                <li><strong>Controle de qualidade</strong>: Valores foram ajustados para evitar resultados não-físicos:
                    <ul>
                        <li>pH limitado ao intervalo [0, 14]</li>
                        <li>Concentrações e relações mantidas como valores positivos</li>
                    </ul>
                </li>
                <li><strong>Estrutura de dados</strong>: Cada linha representa uma réplica experimental contendo:
                    <ul>
                        <li>Parâmetro analisado</li>
                        <li>Substrato (VC-M = Vermicomposto com Materiais Mistos)</li>
                        <li>Medições nos dias 1, 30, 60, 90 e 120</li>
                    </ul>
                </li>
            </ol>
            
            <p style="margin-top:15px; font-style:italic;">
                Esta abordagem permite explorar a variabilidade experimental esperada em estudos reais de vermicompostagem.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=False) 
    
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

if __name__ == "__main__":
    main()
