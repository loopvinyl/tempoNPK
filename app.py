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

# Configurações gerais
st.set_page_config(page_title="Análise Estatística de Vermicompostagem", layout="wide")
st.title("📊 Análise Estatística de Parâmetros de Vermicomposto")
st.markdown("""
<div style="background-color:#f0f8ff; padding:15px; border-radius:10px; margin-bottom:20px;">
    <b>Aplicação para análise de diferenças significativas em parâmetros de vermicomposto ao longo do tempo</b><br>
    Utiliza o teste de Kruskal-Wallis (não paramétrico) para pequenas amostras.
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

## Função para verificar pressupostos estatísticos
def check_statistical_assumptions(data):
    results = []
    for i, group in enumerate(data):
        if len(group) > 3:  # Normaltest requer pelo menos 3 amostras
            _, p_val = normaltest(group)
            results.append({
                "Grupo": f"Grupo {i+1}",
                "p-value (normalidade)": p_val,
                "Normal (p>0.05)": p_val > 0.05
            })
    return pd.DataFrame(results)

## Função para plotar evolução temporal
def plot_parameter_evolution(ax, data, days, param_name):
    # Converter dias para numérico para ordenação
    numeric_days = [DAY_MAPPING[d] for d in days]
    
    for i, (day, num_day) in enumerate(zip(days, numeric_days)):
        group_data = data[i]
        ax.scatter(
            [num_day] * len(group_data), 
            group_data, 
            alpha=0.6, 
            s=80,
            label=f"{day.replace('Day ', 'Dia ')}"
        )
    
    # Calcular e plotar medianas
    medians = [np.median(group) for group in data]
    ax.plot(numeric_days, medians, 'ro-', markersize=8, linewidth=2)
    
    # Configurar eixo X com dias numéricos
    ax.set_xticks(numeric_days)
    ax.set_xticklabels([d.replace('Day ', '') for d in days])
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    
    # Melhorar formatação
    ax.set_xlabel("Dias de Vermicompostagem", fontsize=12)
    ax.set_ylabel(PARAM_MAPPING.get(param_name, param_name), fontsize=12)
    ax.set_title(f"Evolução do {PARAM_MAPPING.get(param_name, param_name)}", fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best', fontsize=10)
    
    return ax

## Função para exibir resultados com formatação melhorada
def display_results_interpretation(results):
    st.header("📝 Interpretação dos Resultados", anchor="interpretation")
    
    if not results:
        st.info("Nenhuma interpretação disponível, pois não há resultados estatísticos.")
        return
    
    for res in results:
        param_name = res["Parâmetro"]
        p_val = res["p-value"]
        is_significant = p_val < 0.05
        
        # Container com cor baseada na significância
        bg_color = "#e6f7e6" if is_significant else "#f9f9f9"
        border_color = "#4CAF50" if is_significant else "#9E9E9E"
        icon = "✅" if is_significant else "❌"
        title = f"{icon} {param_name}"
        
        st.markdown(
            f"""
            <div style="
                background-color: {bg_color};
                border-left: 5px solid {border_color};
                padding: 15px;
                border-radius: 0px 8px 8px 0px;
                margin-bottom: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            ">
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <h3 style="margin: 0; color: #333;">{title}</h3>
                    <span style="margin-left: auto; font-weight: bold; color: #555;">
                        p-valor = {p_val:.4f}
                    </span>
                </div>
                <div style="border-top: 1px solid #ddd; padding-top: 10px;">
            """,
            unsafe_allow_html=True
        )
        
        if is_significant:
            st.markdown("""
                <div style="color: #333;">
                    <p style="margin: 5px 0;"><b>Rejeitamos a hipótese nula (H₀)</b></p>
                    <p style="margin: 5px 0;">Há evidências de que os valores do parâmetro mudam significativamente ao longo do tempo</p>
                    <p style="margin: 5px 0;">A vermicompostagem afeta este parâmetro</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="color: #333;">
                    <p style="margin: 5px 0;"><b>Aceitamos a hipótese nula (H₀)</b></p>
                    <p style="margin: 5px 0;">Não há evidências suficientes de mudanças significativas</p>
                    <p style="margin: 5px 0;">O parâmetro permanece estável durante o processo de vermicompostagem</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)

## Função Principal
def main():
    # Inicialização de variáveis
    df = load_sample_data_with_stdev()
    
    # Opções de Dados na Sidebar
    st.sidebar.header("📂 Opções de Dados")
    use_sample = st.sidebar.checkbox("Usar dados de exemplo", value=True)
    
    if not use_sample:
        uploaded_file = st.sidebar.file_uploader("Carregue o artigo PDF", type="pdf")
        if uploaded_file:
            with st.spinner("Processando PDF..."):
                df_raw = extract_pdf_data(uploaded_file)
                
                if df_raw is not None:
                    st.sidebar.success("Tabela extraída do PDF com sucesso!")
                    st.sidebar.dataframe(df_raw.head(3))
                    
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

    # Pré-visualização dos Dados
    st.header("🔍 Pré-visualização dos Dados")
    st.dataframe(df.head().style.highlight_max(axis=0, color='#e6f7ff'))
    st.markdown(f"**Total de amostras:** {len(df)}")
    st.markdown("---")

    # Configuração de Análise
    st.sidebar.header("⚙️ Configuração de Análise")
    unique_params = df['Parameter'].unique()
    
    # Criar opções com nomes amigáveis
    param_options = [PARAM_MAPPING.get(p, p) for p in unique_params]
    
    selected_params = st.sidebar.multiselect(
        "Selecione os parâmetros:",
        options=param_options,
        default=param_options[:3] if len(param_options) > 3 else param_options
    )
    
    # Converter de volta para nomes originais
    reverse_mapping = {v: k for k, v in PARAM_MAPPING.items()}
    selected_original_params = [reverse_mapping.get(p, p) for p in selected_params]
    
    # Realizar Análise
    if not selected_params:
        st.warning("Selecione pelo menos um parâmetro para análise.")
        return

    results = []
    assumptions_results = []
    days_ordered = ['Day 1', 'Day 30', 'Day 60', 'Day 90', 'Day 120']
    
    # Configurar subplots dinamicamente
    num_plots = len(selected_params)
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
        
        # Verificar pressupostos
        assumptions = check_statistical_assumptions(data_by_day)
        if not assumptions.empty:
            assumptions_results.append({
                "Parâmetro": PARAM_MAPPING.get(param, param),
                "Resultados": assumptions
            })
        
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
                        ha='center', fontsize=10,
                        bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8))
        else:
            st.warning(f"Dados insuficientes para {PARAM_MAPPING.get(param, param)}")
    
    # Resultados Estatísticos
    st.header("📈 Resultados Estatísticos")
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
            return ['background-color: #e6f7e6' if row['p-value'] < 0.05 else '' for _ in row]
        
        st.dataframe(
            results_df.style
            .apply(highlight_significant, axis=1)
            .format({"p-value": "{:.4f}", "H-Statistic": "{:.2f}"})
            .set_properties(**{'text-align': 'center'})
        )
    else:
        st.info("Nenhum resultado estatístico disponível.")
    
    # Pressupostos Estatísticos
    if assumptions_results:
        st.subheader("📏 Verificação de Pressupostos (Normalidade)")
        for res in assumptions_results:
            st.markdown(f"**{res['Parâmetro']}**")
            st.dataframe(res['Resultados'])
    
    # Gráficos
    st.header("📊 Evolução Temporal dos Parâmetros")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    # Interpretação (usando a nova função com design melhorado)
    display_results_interpretation(results)
    
    # Metodologia
    st.sidebar.header("📚 Sobre a Metodologia")
    st.sidebar.markdown("""
    **Teste de Kruskal-Wallis**
    - Alternativa não paramétrica à ANOVA
    - Compara medianas de 3+ grupos
    - Hipóteses:
        - H₀: Distribuições idênticas
        - H₁: Pelo menos uma distribuição diferente
        
    **Interpretação:**
    - p < 0.05: Diferenças significativas
    - p ≥ 0.05: Sem evidência de diferenças
    """)

if __name__ == "__main__":
    main()
