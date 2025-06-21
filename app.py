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
        'K': {'Day 1': (1.28, 0.02), 'Day 30': (1.29, 0.02), 'Day 60': (1.30, 0.02), 'Day 90': (1.31, 0.02), 'Day 120': (1.32, 0.03)},
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

def display_results_dermendzhieva():
    st.header("Análise Estatística - DERMENDZHIEVA et al. (2021) 📚")
    st.write("Esta seção simula a análise dos parâmetros N, P, K, pH e C:N Ratio ao longo do tempo (dias 1, 30, 60, 90, 120) usando dados inspirados no artigo de Dermendzhieva et al. (2021). Os dados são gerados com uma distribuição log-normal e o teste de Kruskal-Wallis é aplicado.")

    # Botão Voltar
    if st.button("⬅️ Voltar para a Página Inicial"):
        st.session_state['selected_article'] = None
        st.experimental_rerun() # Recarrega a página para refletir a mudança de estado

    st.subheader("Parâmetros Disponíveis:")
    options = df['Parameter'].unique().tolist()
    
    # Pre-seleciona todos os parâmetros para esta análise específica
    selected = st.multiselect("Selecione os parâmetros para análise:", options=options, default=options) 
    if not selected:
        st.warning("Selecione ao menos um parâmetro.")
        return

    st.subheader("🔍 Dados Simulados")
    df = load_sample_data_with_stdev(distribution_type='LogNormal') # Carrega os dados aqui para garantir que df esteja definido
    st.dataframe(df)

    st.subheader("📈 Resultados Estatísticos (Teste de Kruskal-Wallis)")
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
            try:
                h, p = kruskal(*param_data)
                results.append((param, h, p))
            except ValueError as e:
                st.warning(f"Erro ao calcular Kruskal-Wallis para {param}: {e}. Verifique se há variância nos dados.")
        else:
            st.info(f"Dados insuficientes para realizar o teste de Kruskal-Wallis para '{param}'. Necessita de dados para ao menos dois 'Treatments'.")

    if results:
        res_df = pd.DataFrame(results, columns=["Parâmetro", "H (estatística)", "p-valor"])
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
    else:
        st.info("Nenhum resultado estatístico disponível para os parâmetros selecionados.")

# =====================================================
# Roteamento principal
# =====================================================
def main():
    if 'selected_article' not in st.session_state:
        st.session_state['selected_article'] = None

    if st.session_state['selected_article'] == 'dermendzhieva':
        display_results_dermendzhieva()
    # elif st.session_state['selected_article'] == 'artigo_2':
    #     # future function for article 2
    #     st.write("Análise para Artigo 2 (em desenvolvimento)...")
    else:
        st.title("📊 Análise Estatística de Parâmetros de Vermicomposto")
        st.markdown("---")
        st.subheader("Bem-vindo à Análise de Vermicompostos! 🪱")
        st.write("Esta aplicação permite simular e analisar dados de parâmetros de vermicompostagem.")
        st.write("Selecione um artigo abaixo para ver a análise estatística dos dados simulados.")
        st.write("O objetivo é ajudar a interpretar diferenças significativas em parâmetros químicos ao longo do tempo, utilizando testes não paramétricos como o Kruskal-Wallis.")
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Vermicompost_pile.jpg/640px-Vermicompost_pile.jpg", caption="Exemplo de Vermicompostagem", use_container_width=True)

        st.markdown("---")
        st.subheader("Selecione um Artigo para Análise:")
        col1, col2 = st.columns(2) # Cria colunas para os botões

        with col1:
            if st.button("📖 Artigo: DERMENDZHIEVA et al. (2021)"):
                st.session_state['selected_article'] = 'dermendzhieva'
                st.experimental_rerun() # Recarrega a página para ir para a análise
        
        with col2:
            # Exemplo para um futuro artigo (pode adicionar mais colunas ou expandir)
            if st.button("📚 Artigo: FUTURO ARTIGO (Em Breve)"):
                st.warning("Funcionalidade para este artigo ainda não implementada.")
                # st.session_state['selected_article'] = 'artigo_2'
                # st.experimental_rerun()

if __name__ == "__main__":
    main()
