import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import kruskal, normaltest
import matplotlib.pyplot as plt
import seaborn as sns
import tabula
import base64
import io
import re
from matplotlib.ticker import MaxNLocator
import matplotlib as mpl

# Configurações gerais com tema escuro
st.set_page_config(
    page_title="Análise Estatística de Vermicompostagem", 
    layout="wide",
    page_icon="📊"
)

# CSS para tema escuro personalizado
st.markdown("""
<style>
    /* Configurações gerais */
    body {
        color: #ffffff;
        background-color: #0e1117;
    }
    
    /* Containers e cards */
    .stApp, .stContainer, .stDataFrame, .stPlotlyChart {
        background-color: #0e1117 !important;
    }
    
    .card {
        background-color: #1e2130 !important;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.3);
        border: 1px solid #2a2f45;
    }
    
    .header-card {
        background: linear-gradient(135deg, #2a2f45 0%, #1a1d2b 100%);
        border-left: 4px solid #6f42c1;
    }
    
    .result-card {
        background: #1a1d2b;
        border-left: 4px solid #6f42c1;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 15px;
    }
    
    .signif-card {
        border-left: 4px solid #00c853 !important;
    }
    
    .not-signif-card {
        border-left: 4px solid #ff5252 !important;
    }
    
    /* Títulos */
    h1, h2, h3, h4, h5, h6 {
        color: #d7dce8 !important;
    }
    
    /* Widgets */
    .st-bb, .st-at, .st-ae, .st-af, .stButton>button, .stTextInput>div>div>input {
        background-color: #1a1d2b !important;
        color: white !important;
        border: 1px solid #2a2f45 !important;
    }
    
    /* Tabelas */
    .dataframe {
        background-color: #1a1d2b !important;
        color: white !important;
    }
    
    .dataframe th {
        background-color: #2a2f45 !important;
        color: white !important;
    }
    
    .dataframe tr:nth-child(even) {
        background-color: #1e2130 !important;
    }
    
    .dataframe tr:hover {
        background-color: #2a2f45 !important;
    }
    
    /* Gráficos */
    .stPlotlyChart, .stPydeckChart {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Divider */
    .stDivider {
        border-top: 1px solid #2a2f45 !important;
    }
</style>
""", unsafe_allow_html=True)

# Configurar matplotlib para tema escuro
plt.style.use('dark_background')
mpl.rcParams.update({
    'axes.facecolor': '#1a1d2b',
    'figure.facecolor': '#0e1117',
    'axes.edgecolor': '#d7dce8',
    'axes.labelcolor': '#d7dce8',
    'text.color': '#d7dce8',
    'xtick.color': '#d7dce8',
    'ytick.color': '#d7dce8',
    'grid.color': '#2a2f45',
})

# Título com estilo moderno
st.markdown("""
<div class="header-card">
    <h1 style="margin:0;padding:10px 0;">📊 Análise Estatística de Parâmetros de Vermicomposto</h1>
    <p style="margin:0;padding-bottom:10px;color:#a0a7c0;">
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

## Função para extrair dados do PDF com cache
@st.cache_data(show_spinner="Extraindo tabela do PDF...")
def extract_pdf_data(uploaded_file):
    try:
        area_table2 = [385, 90, 680, 810] 
        columns_table2 = [190, 260, 320, 380, 440, 500, 560, 620, 680, 740]
        
        tables = tabula.read_pdf(
            io.BytesIO(uploaded_file.getvalue()),
            pages=4,
            multiple_tables=False,
            area=area_table2,
            columns=columns_table2,
            output_format='dataframe',
            lattice=True,
            pandas_options={'header': None}
        )
        
        return tables[0] if tables else None
    except Exception as e:
        st.error(f"Erro na extração do PDF: {str(e)}")
        return None

## Função para processar tabela extraída do PDF
def process_raw_table(df_raw):
    pdf_param_names = {
        'TKN (g kg-1)': 'TKN (g/kg)',
        'Total P (g kg-1)': 'Total P (g/kg)',
        'TK (g kg-1)': 'TK (g/kg)',
        'pH (H2O)': 'pH (H₂O)',
        'C/N ratio': 'C/N ratio'
    }
    
    pdf_days = ['Initial', 'Day 30', 'Day 60', 'Day 90', 'Day 120']
    extracted_data = {}

    for _, row in df_raw.iterrows():
        param_raw_name = str(row.iloc[0]).strip()
        
        # Encontrar nome padronizado do parâmetro
        standard_param_name = None
        for pdf_name, std_name in pdf_param_names.items():
            if pdf_name in param_raw_name:
                standard_param_name = std_name
                break
        
        if standard_param_name:
            extracted_data[standard_param_name] = {}
            col_offset = 1
            
            for i, day_name in enumerate(pdf_days):
                cell_value = str(row.iloc[col_offset + i*2]).strip()
                match = re.match(r"(\d+\.?\d*)\s*±\s*(\d+\.?\d*)", cell_value)
                if match:
                    mean_val = float(match.group(1))
                    stdev_val = float(match.group(2))
                    extracted_data[standard_param_name][day_name] = {
                        'mean': mean_val,
                        'stdev': stdev_val
                    }
                else:
                    try:
                        mean_val = float(cell_value)
                        stdev_val = 0.01 * mean_val
                        if stdev_val == 0: 
                            stdev_val = 0.01
                        extracted_data[standard_param_name][day_name] = {
                            'mean': mean_val,
                            'stdev': stdev_val
                        }
                    except ValueError:
                        extracted_data[standard_param_name][day_name] = {'mean': np.nan, 'stdev': np.nan}
    
    return extracted_data

## Função para plotar evolução temporal com estilo moderno
def plot_parameter_evolution(ax, data, days, param_name):
    # Converter dias para numérico para ordenação
    numeric_days = [DAY_MAPPING[d] for d in days]
    
    # Paleta de cores moderna
    colors = ['#6f42c1', '#00c1e0', '#00d4b1', '#ffd166', '#ff6b6b']
    
    for i, (day, num_day) in enumerate(zip(days, numeric_days)):
        group_data = data[i]
        
        # Plotar pontos individuais
        ax.scatter(
            [num_day] * len(group_data), 
            group_data, 
            alpha=0.8, 
            s=90,
            color=colors[i % len(colors)],
            edgecolors='white',
            linewidth=0.8,
            zorder=3,
            label=f"{day.replace('Day ', 'Dia ')}"
        )
    
    # Calcular e plotar medianas
    medians = [np.median(group) for group in data]
    ax.plot(
        numeric_days, 
        medians, 
        'D-', 
        markersize=8, 
        linewidth=2.5,
        color='#ffffff',
        markerfacecolor='#6f42c1',
        markeredgecolor='white',
        markeredgewidth=1.2,
        zorder=4
    )
    
    # Configurar eixo X com dias numéricos
    ax.set_xticks(numeric_days)
    ax.set_xticklabels([d.replace('Day ', '') for d in days])
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    
    # Melhorar formatação
    ax.set_xlabel("Dias de Vermicompostagem", fontsize=12, fontweight='bold')
    ax.set_ylabel(PARAM_MAPPING.get(param_name, param_name), fontsize=12, fontweight='bold')
    ax.set_title(f"Evolução do {PARAM_MAPPING.get(param_name, param_name)}", 
                fontsize=14, fontweight='bold', pad=15)
    
    # Grid e estilo
    ax.grid(True, alpha=0.25, linestyle='--', color='#a0a7c0')
    ax.legend(loc='best', fontsize=10, framealpha=0.3)
    
    # Remover bordas
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Fundo gradiente
    ax.set_facecolor('#1a1d2b')
    
    return ax

## Função para exibir resultados com design moderno
def display_results_interpretation(results):
    st.markdown("""
    <div class="card">
        <h2>📝 Interpretação dos Resultados</h2>
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
                <h3 style="margin:0; color:{title_color};">{icon} {param_name}</h3>
                <div style="background:#2a2f45; padding:5px 12px; border-radius:20px;">
                    <span style="font-weight:bold; color:{title_color};">{status}</span>
                    <span style="color:#a0a7c0;"> | p = {p_val:.4f}</span>
                </div>
            </div>
            <div style="margin-top:12px;">
        """, unsafe_allow_html=True)
        
        if is_significant:
            st.markdown("""
                <div style="color:#d7dce8;">
                    <p style="margin:8px 0;"><b>Rejeitamos a hipótese nula (H₀)</b></p>
                    <p style="margin:8px 0;">Há evidências de que os valores do parâmetro mudam significativamente ao longo do tempo</p>
                    <p style="margin:8px 0;">A vermicompostagem afeta este parâmetro</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="color:#d7dce8;">
                    <p style="margin:8px 0;"><b>Aceitamos a hipótese nula (H₀)</b></p>
                    <p style="margin:8px 0;">Não há evidências suficientes de mudanças significativas</p>
                    <p style="margin:8px 0;">O parâmetro permanece estável durante o processo de vermicompostagem</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)

## Função Principal
def main():
    # Inicialização de variáveis
    df = load_sample_data_with_stdev()
    
    # Sidebar com tema escuro
    with st.sidebar:
        st.markdown("""
        <div class="card">
            <h3>📂 Opções de Dados</h3>
        """, unsafe_allow_html=True)
        
        use_sample = st.checkbox("Usar dados de exemplo", value=True)
        
        if not use_sample:
            uploaded_file = st.file_uploader("Carregue o artigo PDF", type="pdf")
            if uploaded_file:
                with st.spinner("Processando PDF..."):
                    df_raw = extract_pdf_data(uploaded_file)
                    
                    if df_raw is not None:
                        st.success("Tabela extraída do PDF com sucesso!")
                        
                        extracted_data = process_raw_table(df_raw)
                        num_replications = 3
                        replicated_data = []
                        app_days_map = {
                            'Initial': 'Day 1',
                            'Day 30': 'Day 30',
                            'Day 60': 'Day 60',
                            'Day 90': 'Day 90',
                            'Day 120': 'Day 120'
                        }

                        for param_name, daily_stats in extracted_data.items():
                            for _ in range(num_replications):
                                row_data = {'Parameter': param_name, 'Substrate': 'VC-M'}
                                for pdf_day, app_day in app_days_map.items():
                                    stats = daily_stats.get(pdf_day)
                                    if stats:
                                        value = np.random.normal(
                                            loc=stats['mean'], 
                                            scale=stats['stdev']
                                        )
                                        
                                        if param_name == 'pH (H₂O)':
                                            value = np.clip(value, 0.0, 14.0)
                                        elif 'g/kg' in param_name or 'ratio' in param_name:
                                            value = max(0.0, value)
                                            
                                        row_data[app_day] = value
                                    else:
                                        row_data[app_day] = np.nan
                                replicated_data.append(row_data)
                        
                        df = pd.DataFrame(replicated_data)
                        df = df.dropna(how='all')
                    else:
                        st.warning("Falha na extração. Usando dados de exemplo.")
            else:
                st.info("Nenhum PDF carregado. Usando dados de exemplo.")
        
        st.markdown("""
        <div class="card">
            <h3>⚙️ Configuração de Análise</h3>
        """, unsafe_allow_html=True)
        
        unique_params = df['Parameter'].unique()
        param_options = [PARAM_MAPPING.get(p, p) for p in unique_params]
        
        selected_params = st.multiselect(
            "Selecione os parâmetros:",
            options=param_options,
            default=param_options[:3] if len(param_options) > 3 else param_options
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h3>📚 Sobre a Metodologia</h3>
            <p><b>Teste de Kruskal-Wallis</b></p>
            <ul style="padding-left:20px;color:#d7dce8;">
                <li>Alternativa não paramétrica à ANOVA</li>
                <li>Compara medianas de 3+ grupos</li>
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
        """, unsafe_allow_html=True)

    # Pré-visualização dos Dados
    st.markdown("""
    <div class="card">
        <h2>🔍 Pré-visualização dos Dados</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(df.head().style.background_gradient(cmap='viridis'))
    st.markdown(f"**Total de amostras:** {len(df)}")
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
    
    # Configurar subplots dinamicamente
    num_plots = len(selected_params)
    
    if num_plots > 0:
        fig, axes = plt.subplots(
            num_plots, 1, 
            figsize=(10, 5 * num_plots),
            squeeze=False
        )
        axes = axes.flatten()
    
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
                ax.annotate(f"Kruskal-Wallis: H = {h_stat:.2f}, p = {p_val:.4f}",
                            xy=(0.5, 0.95), xycoords='axes fraction',
                            ha='center', fontsize=10, color='white',
                            bbox=dict(boxstyle="round,pad=0.3", fc="#2a2f45", alpha=0.9))
            else:
                st.warning(f"Dados insuficientes para {PARAM_MAPPING.get(param, param)}")
    else:
        st.warning("Nenhum parâmetro selecionado para análise.")
        return

    # Resultados Estatísticos
    st.markdown("""
    <div class="card">
        <h2>📈 Resultados Estatísticos</h2>
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
        def highlight_significant(row):
            color = '#1a3b1d' if row['p-value'] < 0.05 else '#3b1a1a'
            return [f'background-color: {color}'] * len(row)
        
        st.dataframe(
            results_df.style
            .apply(highlight_significant, axis=1)
            .format({"p-value": "{:.4f}", "H-Statistic": "{:.2f}"})
            .set_properties(**{
                'color': 'white',
                'background-color': '#1a1d2b',
                'border': '1px solid #2a2f45'
            })
        )
    else:
        st.info("Nenhum resultado estatístico disponível.")
    
    # Gráficos
    st.markdown("""
    <div class="card">
        <h2>📊 Evolução Temporal dos Parâmetros</h2>
    </div>
    """, unsafe_allow_html=True)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    # Interpretação
    display_results_interpretation(results)

if __name__ == "__main__":
    main()
