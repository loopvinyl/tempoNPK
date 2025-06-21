import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import kruskal
import matplotlib.pyplot as plt

# Configuração inicial
st.set_page_config(page_title="Análise de Vermicompostos", layout="wide", page_icon="🪱")

# =====================================================
# Funções auxiliares
# =====================================================
@st.cache_data
def load_sample_data_with_stdev(distribution_type='LogNormal'):
    stats = {
        'TKN': {'Day 1': (20.8, 0.5), 'Day 30': (21.5, 0.6), 'Day 60': (22.2, 0.7), 'Day 90': (23.0, 0.8), 'Day 120': (24.5, 0.9)},
        'P': {'Day 1': (12.1, 0.3), 'Day 30': (12.8, 0.4), 'Day 60': (13.5, 0.4), 'Day 90': (14.2, 0.5), 'Day 120': (15.0, 0.6)},
        'K': {'Day 1': (1.28, 0.02), 'Day 30': (1.29, 0.02), 'Day 60': (1.30, 0.02), 'Day 90': (1.31, 0.02), 'Day 120': (1.32, 0.02)},
    }

    days = ['Day 1', 'Day 30', 'Day 60', 'Day 90', 'Day 120']
    data = []

    for param, daily_values in stats.items():
        for rep in range(3):
            row = {'Parameter': param}
            for day in days:
                mean, std = daily_values[day]
                if distribution_type == "LogNormal":
                    sigma = np.sqrt(np.log(1 + (std / mean)**2))
                    mu = np.log(mean) - 0.5 * sigma**2
                    val = np.random.lognormal(mu, sigma)
                else:
                    val = np.random.normal(mean, std)
                row[day] = val
            data.append(row)

    return pd.DataFrame(data)

@st.cache_data
def load_jordao_sample_data():
    sample_data = {
        'Vermicompost Characterization': {
            'pH': (7.1, 0.03),
            'Organic Matter': (42.0, 0.34),
            'C/N ratio': (11.85, 0.2),
            'Cu': (31.0, 6.7),
            'Ni': (21.7, 2.1),
            'Zn': (108, 4.4)
        },
        'Lettuce Cultivation': {
            'Cu_leaves': (8.1, 1.5),
            'Ni_leaves': (35.3, 3.2),
            'Zn_leaves': (1074.8, 85),
            'Cu_roots': (246.3, 25),
            'Ni_roots': (587.7, 45),
            'Zn_roots': (1339.2, 120)
        }
    }

    rows = []
    for treatment, params in sample_data.items():
        for param, (mean, std) in params.items():
            for _ in range(3):
                val = np.random.normal(mean, std)
                rows.append({'Treatment': treatment, 'Parameter': param, 'Value': max(val, 0)})
    return pd.DataFrame(rows)

# =====================================================
# Interface inicial
# =====================================================
def show_homepage():
    st.title("🪱 Análise de Vermicompostos")
    st.markdown("Selecione um artigo abaixo para realizar a análise estatística")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Dermendzhieva et al. (2021)")
        st.markdown("Análise temporal de parâmetros de vermicomposto\n- TKN, Fósforo, Potássio\n- Teste de Kruskal-Wallis")
        if st.button("Selecionar Artigo", key="derm"):
            st.session_state['selected_article'] = 'dermendzhieva'
            st.rerun()
    with col2:
        st.subheader("Jordão et al. (2007)")
        st.markdown("Remoção de metais pesados e cultivo de alface\n- Cobre, Níquel, Zinco")
        if st.button("Selecionar Artigo", key="jordao"):
            st.session_state['selected_article'] = 'jordao'
            st.rerun()

# =====================================================
# Análise Dermendzhieva
# =====================================================
def run_dermendzhieva_analysis():
    st.header("📊 Análise Temporal de Parâmetros de Vermicomposto")
    if st.button("← Voltar"):
        st.session_state['selected_article'] = None
        st.rerun()

    st.subheader("⚙️ Configurações de Análise")
    st.markdown("A simulação usa distribuição **LogNormal**, adequada para dados ambientais e o teste de Kruskal-Wallis.")

    df = load_sample_data_with_stdev("LogNormal")

    options = df['Parameter'].unique().tolist()
    selected = st.multiselect("Selecione os parâmetros:", options, default=options)
    if not selected:
        st.warning("Selecione ao menos um parâmetro.")
        return

    results = []
    for param in selected:
        data = [df[df['Parameter'] == param][day].values for day in ['Day 1', 'Day 30', 'Day 60', 'Day 90', 'Day 120']]
        if all(len(d) > 0 for d in data):
            h, p = kruskal(*data)
            results.append((param, h, p))

    st.subheader("📈 Resultados Estatísticos")
    if results:
        res_df = pd.DataFrame(results, columns=["Parâmetro", "H", "p-valor"])
        st.dataframe(res_df)
    else:
        st.info("Nenhum resultado estatístico disponível.")

# =====================================================
# Análise Jordão
# =====================================================
def run_jordao_analysis():
    st.header("⚗️ Análise de Remoção de Metais Pesados e Cultivo")
    if st.button("← Voltar"):
        st.session_state['selected_article'] = None
        st.rerun()

    df = load_jordao_sample_data()

    st.subheader("⚙️ Configurações de Análise")
    analysis_type = st.radio("Tipo de análise:", ["Caracterização do Vermicomposto", "Cultivo de Alface"])
    if analysis_type == "Caracterização do Vermicomposto":
        options = df[~df['Parameter'].str.contains("leaves|roots")]['Parameter'].unique().tolist()
    else:
        options = df[df['Parameter'].str.contains("leaves|roots")]['Parameter'].unique().tolist()

    selected = st.multiselect("Selecione os parâmetros:", options, default=options[:2])
    if not selected:
        st.warning("Selecione ao menos um parâmetro.")
        return

    st.subheader("🔍 Dados Simulados")
    st.dataframe(df)

    st.subheader("📈 Resultados Estatísticos")
    results = []
    for param in selected:
        param_data = []
        labels = []
        for treat in df['Treatment'].unique():
            vals = df[(df['Parameter'] == param) & (df['Treatment'] == treat)]['Value'].dropna().values
            if len(vals) > 1:
                param_data.append(vals)
                labels.append(treat)
        if len(param_data) >= 2:
            h, p = kruskal(*param_data)
            results.append((param, h, p))
        else:
            st.warning(f"Dados insuficientes para {param}")

    if results:
        res_df = pd.DataFrame(results, columns=["Parâmetro", "H", "p-valor"])
        st.dataframe(res_df)
    else:
        st.info("Nenhum resultado estatístico disponível.")

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
        show_homepage()

if __name__ == "__main__":
    main()
