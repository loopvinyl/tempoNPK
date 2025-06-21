import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import kruskal
import matplotlib.pyplot as plt
import seaborn as sns 

# Configuração inicial
st.set_page_config(page_title="Análise de Vermicompostos", layout="wide", page_icon="🪱")

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
        'TKN': {'Day 1': (20.8, 0.5), 'Day 30': (21.5, 0.6), 'Day 60': (22.2, 0.7), 'Day 90': (23.0, 0.8), 'Day 120': (24.5, 0.9)},
        'P': {'Day 1': (12.1, 0.3), 'Day 30': (12.8, 0.4), 'Day 60': (13.5, 0.4), 'Day 90': (14.2, 0.5), 'Day 120': (15.0, 0.6)},
        'K': {'Day 1': (1.28, 0.02), 'Day 30': (1.29, 0.02), 'Day 60': (1.30, 0.02), 'Day 90': (1.31, 0.02), 'Day 120': (1.32, 0.03)}, # O 0.02 foi ajustado para 0.03 no Day 120 para ter variância
        'pH': {'Day 1': (7.5, 0.2), 'Day 30': (7.2, 0.2), 'Day 60': (7.0, 0.1), 'Day 90': (6.9, 0.1), 'Day 120': (6.8, 0.1)},
        'C:N Ratio': {'Day 1': (25.0, 1.5), 'Day 30': (20.0, 1.2), 'Day 60': (15.0, 1.0), 'Day 90': (12.0, 0.8), 'Day 120': (10.0, 0.7)},
    }

    data = []
    num_samples_per_day = 5 # Número de amostras simuladas por dia de tratamento

    for param, days_stats in stats.items():
        for day, (mean_orig, std_orig) in days_stats.items():
            if distribution_type == 'LogNormal':
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
                    mu_log = np.log(mean_orig**2 / np.sqrt(std_orig**2 + mean_orig**2))
                    sigma_log = np.sqrt(np.log(1 + (std_orig**2 / mean_orig**2)))
                    values = np.random.lognormal(mu_log, sigma_log, num_samples_per_day)
            else: 
                values = np.random.normal(mean_orig, std_orig, num_samples_per_day)

            for val in values:
                data.append({
                    'Parameter': param,
                    'Treatment': day,
                    'Value': val
                })
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

    st.markdown("---")
    st.subheader("Selecione um Artigo para Análise:")
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

    # Carrega os dados antes de usar 'df'
    df = load_sample_data_with_stdev("LogNormal")

    options = df['Parameter'].unique().tolist()
    selected = st.multiselect("Selecione os parâmetros:", options, default=options)
    if not selected:
        st.warning("Selecione ao menos um parâmetro.")
        return

    results = []
    for param in selected:
        # Acessa os valores dos dias diretamente, assumindo que eles são colunas no DataFrame
        # A estrutura original do df de Dermendzhieva estava mais próxima de {Parameter, Treatment, Value}
        # e aqui estamos esperando Day 1, Day 30, etc como colunas.
        # Vamos ajustar o load_sample_data_with_stdev para retornar no formato pivotado
        # para que esta parte do código funcione, ou ajustar esta parte para o formato original.
        # Considerando a estrutura original do `load_sample_data_with_stdev` que retorna
        # um DataFrame com 'Parameter', 'Treatment', 'Value', a linha abaixo precisa ser adaptada.
        
        # Adaptação para o formato df com 'Parameter', 'Treatment', 'Value'
        # Group by 'Treatment' for the selected parameter
        data_for_kruskal = []
        for day in ['Day 1', 'Day 30', 'Day 60', 'Day 90', 'Day 120']:
            values_for_day = df[(df['Parameter'] == param) & (df['Treatment'] == day)]['Value'].values
            if len(values_for_day) > 0:
                data_for_kruskal.append(values_for_day)
        
        if all(len(d) > 0 for d in data_for_kruskal) and len(data_for_kruskal) >= 2:
            try:
                h, p = kruskal(*data_for_kruskal)
                results.append((param, h, p))
            except ValueError as e:
                st.warning(f"Erro ao calcular Kruskal-Wallis para {param}: {e}. Verifique se há variância nos dados.")
        else:
            st.info(f"Dados insuficientes para realizar o teste de Kruskal-Wallis para '{param}'. Necessita de dados para ao menos dois 'Treatments'.")


    st.subheader("📈 Resultados Estatísticos")
    if results:
        res_df = pd.DataFrame(results, columns=["Parâmetro", "H", "p-valor"])
        st.dataframe(res_df)
        
        st.subheader("Interpretação dos Resultados:")
        for _, row in res_df.iterrows():
            param = row["Parâmetro"]
            p_value = row["p-valor"]
            st.write(f"**Parâmetro: {param}**")
            if p_value < 0.05:
                st.success(f"✅ Diferenças estatisticamente significativas (p = {p_value:.4f})")
                st.markdown("""
                - **Rejeitamos a hipótese nula (H₀)**: As distribuições dos valores do parâmetro *não* são as mesmas em todos os dias de tratamento.
                - Há evidências de que os valores do parâmetro **mudam significativamente ao longo do tempo** de vermicompostagem.
                """)
            else:
                st.warning(f"❌ Sem diferenças estatisticamente significativas (p = {p_value:.4f})")
                st.markdown("""
                - **Aceitamos a hipótese nula (H₀)**: As distribuições dos valores do parâmetro são as mesmas em todos os dias de tratamento.
                - Não há evidências suficientes para afirmar que os valores do parâmetro **mudam significativamente ao longo do tempo** de vermicompostagem. O parâmetro permanece estável durante o processo.
                """)
    else:
        st.info("Nenhum resultado estatístico disponível.")

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
