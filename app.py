import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import kruskal
import matplotlib.pyplot as plt
import seaborn as sns # Importação de seaborn já está correta 

# Configuração inicial
st.set_page_config(page_title="Análise de Vermicompostos", layout="wide", page_icon="🪱") [cite: 1]

# =====================================================
# Funções auxiliares
# =====================================================
@st.cache_data
def load_sample_data_with_stdev(distribution_type='LogNormal'):
    """
    Gera dados de amostra simulados com base em médias e desvios padrão
    inspirados no artigo DERMENDZHIEVA et al. (2021) para N, P, K, pH e C:N Ratio.
    Utiliza uma distribuição log-normal.
    """
    # Dados de exemplo (substitua pelos dados EXATOS do artigo DERMENDZHIEVA et al. (2021))
    stats = {
        'TKN': {'Day 1': (20.8, 0.5), 'Day 30': (21.5, 0.6), 'Day 60': (22.2, 0.7), 'Day 90': (23.0, 0.8), 'Day 120': (24.5, 0.9)}, [cite: 1]
        'P': {'Day 1': (12.1, 0.3), 'Day 30': (12.8, 0.4), 'Day 60': (13.5, 0.4), 'Day 90': (14.2, 0.5), 'Day 120': (15.0, 0.6)}, [cite: 1]
        'K': {'Day 1': (1.28, 0.02), 'Day 30': (1.29, 0.02), 'Day 60': (1.30, 0.02), 'Day 90': (1.31, 0.02), 'Day 120': (1.32, 0.03)}, # O 0.02 foi ajustado para 0.03 no Day 120 para ter variância 
        'pH': {'Day 1': (7.5, 0.2), 'Day 30': (7.2, 0.2), 'Day 60': (7.0, 0.1), 'Day 90': (6.9, 0.1), 'Day 120': (6.8, 0.1)},
        'C:N Ratio': {'Day 1': (25.0, 1.5), 'Day 30': (20.0, 1.2), 'Day 60': (15.0, 1.0), 'Day 90': (12.0, 0.8), 'Day 120': (10.0, 0.7)},
    }

    data = [] [cite: 2]
    num_samples_per_day = 5 # Número de amostras simuladas por dia de tratamento

    for param, days_stats in stats.items():
        for day, (mean_orig, std_orig) in days_stats.items(): [cite: 3]
            if distribution_type == 'LogNormal': [cite: 3]
                # Converte média e desvio padrão para os parâmetros da distribuição log-normal
                if mean_orig <= 0:
                    st.error(f"Média original ({mean_orig}) para {param} no {day} deve ser positiva para LogNormal.")
                    continue
                if std_orig < 0:
                    st.error(f"Desvio padrão original ({std_orig}) para {param} no {day} não pode ser negativo.")
                    continue
                    
                if std_orig == 0:
                    values = np.full(num_samples_per_day, mean_orig)
                else:
                    mu_log = np.log(mean_orig**2 / np.sqrt(std_orig**2 + mean_orig**2)) [cite: 3]
                    sigma_log = np.sqrt(np.log(1 + (std_orig**2 / mean_orig**2))) [cite: 3]
                    values = np.random.lognormal(mu_log, sigma_log, num_samples_per_day) [cite: 4]
            else: 
                values = np.random.normal(mean_orig, std_orig, num_samples_per_day) [cite: 4]

            for val in values:
                data.append({
                    'Parameter': param,
                    'Treatment': day,
                    'Value': val
                })
    return pd.DataFrame(data) [cite: 4]

@st.cache_data
def load_jordao_sample_data():
    sample_data = {
        'Vermicompost Characterization': {
            'pH': (7.1, 0.03), [cite: 5]
            'Organic Matter': (42.0, 0.34), [cite: 5]
            'C/N ratio': (11.85, 0.2), [cite: 5]
            'Cu': (31.0, 6.7), [cite: 5]
            'Ni': (21.7, 2.1), [cite: 5]
            'Zn': (108, 4.4) [cite: 5]
        },
        'Lettuce Cultivation': {
            'Cu_leaves': (8.1, 1.5), [cite: 6]
            'Ni_leaves': (35.3, 3.2), [cite: 6]
            'Zn_leaves': (1074.8, 85), [cite: 6]
            'Cu_roots': (246.3, 25), [cite: 6]
            'Ni_roots': (587.7, 45), [cite: 6]
            'Zn_roots': (1339.2, 120) [cite: 6]
        }
    }

    rows = [] [cite: 7]
    for treatment, params in sample_data.items(): [cite: 7]
        for param, (mean, std) in params.items(): [cite: 7]
            for _ in range(3): [cite: 7]
                val = np.random.normal(mean, std) [cite: 7]
                rows.append({'Treatment': treatment, 'Parameter': param, 'Value': max(val, 0)}) [cite: 7]
    return pd.DataFrame(rows) [cite: 7]

# =====================================================
# Interface inicial
# =====================================================
def show_homepage():
    st.title("🪱 Análise de Vermicompostos")
    st.markdown("Selecione um artigo abaixo para realizar a análise estatística") [cite: 8]

    st.markdown("---")
    st.subheader("Selecione um Artigo para Análise:")
    col1, col2 = st.columns(2) 

    with col1:
        st.subheader("Dermendzhieva et al. (2021)") [cite: 9]
        st.markdown("Análise temporal de parâmetros de vermicomposto\n- TKN, Fósforo, Potássio\n- Teste de Kruskal-Wallis") [cite: 9]
        if st.button("Selecionar Artigo", key="derm"): [cite: 9]
            st.session_state['selected_article'] = 'dermendzhieva' [cite: 9]
            st.rerun() # Corrigido de experimental_rerun() 
    with col2:
        st.subheader("Jordão et al. (2007)") [cite: 10]
        st.markdown("Remoção de metais pesados e cultivo de alface\n- Cobre, Níquel, Zinco") [cite: 10]
        if st.button("Selecionar Artigo", key="jordao"): [cite: 10]
            st.session_state['selected_article'] = 'jordao' [cite: 10]
            st.rerun() # Corrigido de experimental_rerun() 

# =====================================================
# Análise Dermendzhieva
# =====================================================
def run_dermendzhieva_analysis():
    st.header("📊 Análise Temporal de Parâmetros de Vermicomposto")
    if st.button("← Voltar"):
        st.session_state['selected_article'] = None
        st.rerun() # Corrigido de experimental_rerun()

    st.subheader("⚙️ Configurações de Análise")
    st.markdown("A simulação usa distribuição **LogNormal**, adequada para dados ambientais e o teste de Kruskal-Wallis.")

    # Mover a chamada para carregar os dados para antes de usar 'df'
    df = load_sample_data_with_stdev("LogNormal")

    options = df['Parameter'].unique().tolist() [cite: 11]
    selected = st.multiselect("Selecione os parâmetros:", options, default=options) [cite: 11]
    if not selected:
        st.warning("Selecione ao menos um parâmetro.")
        return

    results = []
    for param in selected:
        data = [df[df['Parameter'] == param][day].values for day in ['Day 1', 'Day 30', 'Day 60', 'Day 90', 'Day 120']] [cite: 11]
        # Certifique-se de que todos os sub-arrays em 'data' têm elementos
        if all(len(d) > 0 for d in data):
            h, p = kruskal(*data) [cite: 12]
            results.append((param, h, p))

    st.subheader("📈 Resultados Estatísticos") [cite: 12]
    if results:
        res_df = pd.DataFrame(results, columns=["Parâmetro", "H", "p-valor"]) [cite: 16]
        st.dataframe(res_df) [cite: 16]
    else:
        st.info("Nenhum resultado estatístico disponível.") [cite: 16]

    # Plotting results
    st.subheader("📊 Visualização dos Dados por Parâmetro")
    for param in selected:
        fig, ax = plt.subplots(figsize=(10, 6))
        param_df = df[df['Parameter'] == param]
        
        # Ordenar os "Treatments" para o plot (Day 1, Day 30, etc.)
        treatment_order = [f'Day {d}' for d in [1, 30, 60, 90, 120]]
        param_df['Treatment'] = pd.Categorical(param_df['Treatment'], categories=treatment_order, ordered=True)
        param_df = param_df.sort_values('Treatment')

        # Boxplot para visualizar a distribuição
        sns.boxplot(x='Treatment', y='Value', data=param_df, ax=ax)
        sns.stripplot(x='Treatment', y='Value', data=param_df, color='black', size=4, jitter=True, ax=ax) 
        ax.set_title(f'Distribuição de {param} ao Longo do Tempo')
        ax.set_xlabel('Dia de Tratamento')
        ax.set_ylabel(param)
        st.pyplot(fig)
        plt.close(fig) 


# =====================================================
# Análise Jordão
# =====================================================
def run_jordao_analysis():
    st.header("⚗️ Análise de Remoção de Metais Pesados e Cultivo") [cite: 13]
    if st.button("← Voltar"): [cite: 13]
        st.session_state['selected_article'] = None [cite: 13]
        st.rerun() # Corrigido de experimental_rerun() 

    df = load_jordao_sample_data() [cite: 13]

    st.subheader("⚙️ Configurações de Análise") [cite: 13]
    analysis_type = st.radio("Tipo de análise:", ["Caracterização do Vermicomposto", "Cultivo de Alface"]) [cite: 13]
    if analysis_type == "Caracterização do Vermicomposto":
        options = df[~df['Parameter'].str.contains("leaves|roots")]['Parameter'].unique().tolist() [cite: 13]
    else:
        options = df[df['Parameter'].str.contains("leaves|roots")]['Parameter'].unique().tolist() [cite: 13]

    selected = st.multiselect("Selecione os parâmetros:", options, default=options[:2]) [cite: 13]
    if not selected:
        st.warning("Selecione ao menos um parâmetro.")
        return [cite: 14]

    st.subheader("🔍 Dados Simulados") [cite: 14]
    st.dataframe(df) [cite: 14]

    st.subheader("📈 Resultados Estatísticos") [cite: 14]
    results = [] [cite: 14]
    for param in selected: [cite: 14]
        param_data = [] [cite: 14]
        labels = [] [cite: 14]
        for treat in df['Treatment'].unique(): [cite: 14]
            vals = df[(df['Parameter'] == param) & (df['Treatment'] == treat)]['Value'].dropna().values [cite: 14]
            if len(vals) > 1: [cite: 14]
                param_data.append(vals) [cite: 15]
                labels.append(treat) [cite: 15]
        if len(param_data) >= 2: [cite: 15]
            h, p = kruskal(*param_data) [cite: 15]
            results.append((param, h, p)) [cite: 15]
        else:
            st.warning(f"Dados insuficientes para {param}") [cite: 15]

    if results:
        res_df = pd.DataFrame(results, columns=["Parâmetro", "H", "p-valor"]) [cite: 16]
        st.dataframe(res_df) [cite: 16]
    else:
        st.info("Nenhum resultado estatístico disponível.") [cite: 16]

# =====================================================
# Roteamento principal
# =====================================================
def main():
    if 'selected_article' not in st.session_state:
        st.session_state['selected_article'] = None

    if st.session_state['selected_article'] == 'dermendzhieva':
        run_dermendzhieva_analysis()
    elif st.session_state['selected_article'] == 'jordao':
        run_jordao_analysis()
    else:
        show_homepage() [cite: 17]

if __name__ == "__main__":
    main()
