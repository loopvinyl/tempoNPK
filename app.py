import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import kruskal
import matplotlib.pyplot as plt
import seaborn as sns
import tabula
import base64

# Configurações gerais
st.set_page_config(page_title="Análise Estatística de Vermicompostagem", layout="wide")
st.title("📊 Análise Estatística de Parâmetros de Vermicomposto")
st.markdown("""
**Aplicação para análise de diferenças significativas em parâmetros de vermicomposto ao longo do tempo**  
Utiliza o teste de Kruskal-Wallis (não paramétrico) para pequenas amostras.
""")

# Função para carregar dados de exemplo
def load_sample_data():
    """Dados de exemplo baseados no artigo DERMENDZHIEVA et al. (2021)"""
    return pd.DataFrame({
        'Parameter': ['TKN (gkg⁻¹)', 'TKN (gkg⁻¹)', 'TKN (gkg⁻¹)', 'TKN (gkg⁻¹)', 'TKN (gkg⁻¹)',
                      'Total P (gkg⁻¹)', 'Total P (gkg⁻¹)', 'Total P (gkg⁻¹)', 'Total P (gkg⁻¹)', 'Total P (gkg⁻¹)',
                      'TK (gkg⁻¹)', 'TK (gkg⁻¹)', 'TK (gkg⁻¹)', 'TK (gkg⁻¹)', 'TK (gkg⁻¹)',
                      'pH (H₂O)', 'pH (H₂O)', 'pH (H₂O)', 'pH (H₂O)', 'pH (H₂O)',
                      'C/N ratio', 'C/N ratio', 'C/N ratio', 'C/N ratio', 'C/N ratio'],
        'Substrate': ['VC-M']*25,
        'Day 1': [20.8, 12.1, 1.28, 7.04, 11.2] * 5,
        'Day 30': [21.2, 13.0, 1.24, 5.60, 10.9] * 5,
        'Day 60': [22.8, 13.9, 1.30, 5.56, 9.67] * 5,
        'Day 90': [23.3, 14.6, 1.34, 5.27, 9.65] * 5,
        'Day 120': [25.5, 15.3, 1.45, 5.78, 7.91] * 5
    })

# Função principal
def main():
    # Upload do PDF ou uso de dados de exemplo
    st.sidebar.header("Opções de Dados")
    use_sample = st.sidebar.checkbox("Usar dados de exemplo", value=True)
    
    if use_sample:
        df = load_sample_data()
        st.sidebar.success("Usando dados de exemplo do artigo DERMENDZHIEVA et al. (2021)")
    else:
        uploaded_file = st.sidebar.file_uploader("Carregue o artigo PDF", type="pdf")
        if not uploaded_file:
            st.info("Por favor, carregue um PDF ou marque 'Usar dados de exemplo'")
            return
            
        st.sidebar.info(f"Arquivo carregado: {uploaded_file.name}")
        try:
            # Extrair tabela da página 4
            tables = tabula.read_pdf(uploaded_file, pages=4, multiple_tables=True)
            df = tables[0]
            st.sidebar.success("Tabela extraída com sucesso!")
        except Exception as e:
            st.sidebar.error(f"Erro na extração: {str(e)}")
            st.error("Não foi possível extrair a tabela. Usando dados de exemplo.")
            df = load_sample_data()

    # Pré-processamento dos dados
    st.header("Pré-visualização dos Dados")
    st.dataframe(df.head())
    
    # Selecionar parâmetros para análise
    st.sidebar.header("Configuração de Análise")
    parameters = st.sidebar.multiselect(
        "Selecione os parâmetros para análise:",
        options=["Nitrogênio (N)", "Fósforo (P)", "Potássio (K)", "pH", "Relação C/N"],
        default=["Nitrogênio (N)", "Fósforo (P)", "pH"]
    )
    
    # Mapeamento de parâmetros para colunas
    param_mapping = {
        "Nitrogênio (N)": "TKN (gkg⁻¹)",
        "Fósforo (P)": "Total P (gkg⁻¹)",
        "Potássio (K)": "TK (gkg⁻¹)",
        "pH": "pH (H₂O)",
        "Relação C/N": "C/N ratio"
    }
    
    # Realizar testes estatísticos
    results = []
    fig, axes = plt.subplots(len(parameters), 1, figsize=(10, 5*len(parameters)))
    if len(parameters) == 1:
        axes = [axes]
    
    for i, param in enumerate(parameters):
        col_name = param_mapping[param]
        param_df = df[df['Parameter'] == col_name]
        
        # Extrair dados para cada dia
        days = ['Day 1', 'Day 30', 'Day 60', 'Day 90', 'Day 120']
        data = [param_df[day].values for day in days]
        
        # Teste de Kruskal-Wallis
        h_stat, p_val = kruskal(*data)
        results.append({
            "Parâmetro": param,
            "H-Statistic": h_stat,
            "p-value": p_val,
            "Significativo (p<0.05)": p_val < 0.05
        })
        
        # Criar gráfico
        ax = axes[i]
        for j, day_data in enumerate(data):
            ax.scatter([j]*len(day_data), day_data, alpha=0.6, label=f"Dia {[1,30,60,90,120][j]}")
        
        # Adicionar linha de tendência
        medians = [np.median(day_data) for day_data in data]
        ax.plot(medians, 'ro-', markersize=8)
        
        ax.set_title(f"Evolução do {param}")
        ax.set_ylabel(param.split('(')[0].strip())
        ax.set_xticks(range(5))
        ax.set_xticklabels(['1', '30', '60', '90', '120'])
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Adicionar resultado do teste ao gráfico
        ax.annotate(f"Kruskal-Wallis: H = {h_stat:.2f}, p = {p_val:.4f}",
                    xy=(0.5, 0.05), xycoords='axes fraction',
                    ha='center', fontsize=9,
                    bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.3))

    # Mostrar resultados estatísticos
    st.header("Resultados Estatísticos")
    results_df = pd.DataFrame(results)
    st.dataframe(results_df.style.apply(
        lambda x: ['background-color: #fffd8e' if x['p-value'] < 0.05 else '' for _ in x], 
        axis=1
    ))
    
    # Mostrar gráficos
    st.header("Evolução Temporal dos Parâmetros")
    st.pyplot(fig)
    
    # Interpretação dos resultados
    st.header("Interpretação dos Resultados")
    for res in results:
        st.subheader(res["Parâmetro"])
        if res["p-value"] < 0.05:
            st.success(f"✅ Diferenças estatisticamente significativas (p = {res['p-value']:.4f})")
            st.markdown("""
            - **Rejeitamos a hipótese nula (H₀)**
            - Há evidências de que os valores do parâmetro mudam significativamente ao longo do tempo
            - A vermicompostagem afeta este parâmetro
            """)
        else:
            st.warning(f"❌ Sem diferenças significativas (p = {res['p-value']:.4f})")
            st.markdown("""
            - **Aceitamos a hipótese nula (H₀)**
            - Não há evidências suficientes de mudanças significativas
            - O parâmetro permanece estável durante o processo
            """)
    
    # Explicação metodológica
    st.sidebar.header("Sobre a Metodologia")
    st.sidebar.info("""
    **Teste de Kruskal-Wallis:**
    - Teste não paramétrico equivalente à ANOVA
    - Usado quando os dados não atendem aos pressupostos de normalidade
    - Adequado para pequenas amostras (n = 3 neste estudo)
    
    **Hipóteses:**
    - H₀: As distribuições são iguais em todos os grupos
    - H₁: Pelo menos um grupo difere dos demais
    
    **Significância:**
    - p < 0.05 → Rejeita H₀ (diferenças significativas)
    """)

if __name__ == "__main__":
    main()
