
import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import kruskal

st.set_page_config(page_title="Análise de Vermicompostos", layout="wide", page_icon="🪱")

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
            for _ in range(4):  # 4 repetições
                val = np.random.normal(mean, std)
                rows.append({'Treatment': treatment, 'Parameter': param, 'Value': max(val, 0)})
    return pd.DataFrame(rows)

def run_jordao_analysis():
    st.header("⚗️ Análise de Remoção de Metais Pesados e Cultivo")
    if st.button("← Voltar"):
        st.session_state['selected_article'] = None
        st.rerun()

    df = load_jordao_sample_data()

    st.subheader("🔍 Dados Simulados (Visualize antes de selecionar)")
    st.dataframe(df)

    st.subheader("⚙️ Configurações de Análise")
    analysis_type = st.radio("Tipo de análise:", ["Caracterização do Vermicomposto", "Cultivo de Alface"])
    if analysis_type == "Caracterização do Vermicomposto":
        options = sorted(df[df['Treatment'] == "Vermicompost Characterization"]['Parameter'].unique())
    else:
        options = sorted(df[df['Treatment'] == "Lettuce Cultivation"]['Parameter'].unique())

    selected = st.multiselect("Selecione os parâmetros:", options, default=options[:2])
    if not selected:
        st.warning("Selecione ao menos um parâmetro.")
        return

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
            st.warning(f"🔸 Dados insuficientes para análise estatística do parâmetro: {param}")

    if results:
        res_df = pd.DataFrame(results, columns=["Parâmetro", "H", "p-valor"])
        st.dataframe(res_df)
    else:
        st.info("Nenhum resultado estatístico disponível.")

def main():
    st.title("🪱 Análise de Vermicompostos")
    if 'selected_article' not in st.session_state:
        st.session_state['selected_article'] = None

    if st.session_state['selected_article'] == 'jordao':
        run_jordao_analysis()
        return

    st.markdown("Selecione um artigo abaixo para iniciar:")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Dermendzhieva et al. (2021)")
        if st.button("Selecionar Artigo", key="derm"):
            st.session_state['selected_article'] = 'dermendzhieva'
            st.rerun()
    with col2:
        st.subheader("Jordão et al. (2007)")
        if st.button("Selecionar Artigo", key="jordao"):
            st.session_state['selected_article'] = 'jordao'
            st.rerun()

if __name__ == "__main__":
    main()
