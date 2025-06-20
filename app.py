import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import kruskal
import matplotlib.pyplot as plt
import seaborn as sns
import tabula
import base64
import io
import re # Importa o módulo de expressões regulares

# Configurações gerais
st.set_page_config(page_title="Análise Estatística de Vermicompostagem", layout="wide")
st.title("📊 Análise Estatística de Parâmetros de Vermicomposto")
st.markdown("""
**Aplicação para análise de diferenças significativas em parâmetros de vermicomposto ao longo do tempo**
Utiliza o teste de Kruskal-Wallis (não paramétrico) para pequenas amostras.
""")

## Função para Carregar Dados de Exemplo (Simulando Réplicas com Média e DP)
def load_sample_data_with_stdev():
    """
    Dados de exemplo baseados no artigo DERMENDZHIEVA et al. (2021).
    Simula um número fixo de réplicas por dia para cada parâmetro,
    utilizando valores de média e desvio padrão para gerar os dados.
    Estes valores são **ilustrativos** e devem ser substituídos por dados reais do artigo
    quando a extração do PDF for bem-sucedida.
    """
    # Exemplo de médias e desvios padrão (valores ilustrativos para demonstrar variabilidade)
    # Estes valores foram ajustados para que o teste de Kruskal-Wallis tenha uma boa chance de
    # encontrar significância para TKN, Total P e C/N, e não para pH e TK (para mostrar ambos os casos).
    sample_param_data = {
        'TKN (gkg⁻¹)': {
            'Day 1': {'mean': 20.8, 'stdev': 0.5},
            'Day 30': {'mean': 21.5, 'stdev': 0.6},
            'Day 60': {'mean': 22.2, 'stdev': 0.7},
            'Day 90': {'mean': 23.0, 'stdev': 0.8},
            'Day 120': {'mean': 24.5, 'stdev': 0.9}
        },
        'Total P (gkg⁻¹)': {
            'Day 1': {'mean': 12.1, 'stdev': 0.3},
            'Day 30': {'mean': 12.8, 'stdev': 0.4},
            'Day 60': {'mean': 13.5, 'stdev': 0.4},
            'Day 90': {'mean': 14.2, 'stdev': 0.5},
            'Day 120': {'mean': 15.0, 'stdev': 0.6}
        },
        'TK (gkg⁻¹)': { # Este terá pouca variação para mostrar "sem diferenças significativas"
            'Day 1': {'mean': 1.28, 'stdev': 0.02},
            'Day 30': {'mean': 1.29, 'stdev': 0.02},
            'Day 60': {'mean': 1.30, 'stdev': 0.02},
            'Day 90': {'mean': 1.31, 'stdev': 0.02},
            'Day 120': {'mean': 1.32, 'stdev': 0.02}
        },
        'pH (H₂O)': { # Este terá pouca variação para mostrar "sem diferenças significativas"
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

    num_replications = 3 # Número de réplicas por ponto de dados, conforme o artigo
    days = ['Day 1', 'Day 30', 'Day 60', 'Day 90', 'Day 120']
    all_replicated_data = []

    for param_name, daily_stats in sample_param_data.items():
        for i in range(num_replications): # Gera 'num_replications' linhas para cada parâmetro
            row_data = {'Parameter': param_name, 'Substrate': 'VC-M'}
            for day in days:
                stats = daily_stats.get(day)
                if stats:
                    # Gera um valor aleatório com base na média e desvio padrão
                    # Usamos `np.random.normal` para simular uma distribuição normal.
                    simulated_value = np.random.normal(loc=stats['mean'], scale=stats['stdev'], size=1)[0]
                    
                    # Garante que valores simulados para pH não saiam do intervalo [0, 14]
                    if param_name == 'pH (H₂O)':
                        simulated_value = max(0.0, min(14.0, simulated_value))
                    # Garante que outros valores (como concentrações, ratios) não sejam negativos
                    elif 'gkg⁻¹' in param_name or 'ratio' in param_name:
                        simulated_value = max(0.0, simulated_value)
                    
                    row_data[day] = simulated_value
                else:
                    row_data[day] = np.nan # Se não houver dados para o dia
            all_replicated_data.append(row_data)

    return pd.DataFrame(all_replicated_data)

## Função Principal
def main():
    # Opções de Dados na Sidebar
    st.sidebar.header("Opções de Dados")
    use_sample = st.sidebar.checkbox("Usar dados de exemplo", value=True)

    df = pd.DataFrame() # Inicializa df para garantir que sempre haja um DataFrame

    if use_sample:
        df = load_sample_data_with_stdev()
        st.sidebar.success("Usando dados de exemplo (réplicas simuladas com média e DP).")
    else:
        uploaded_file = st.sidebar.file_uploader("Carregue o artigo PDF", type="pdf")
        if not uploaded_file:
            st.info("Por favor, carregue um PDF ou marque 'Usar dados de exemplo'.")
            return

        st.sidebar.info(f"Arquivo carregado: {uploaded_file.name}")
        try:
            # --- Início da Extração Específica para o PDF Anexado (DERMENDZHIEVA et al. (2021)) ---
            # A Tabela 2 está na página 4. Os parâmetros são as linhas e os dias são as colunas (Mean ± SD).
            # Vamos tentar extrair a área da tabela 2 para VC-M e VC-P.
            
            st.sidebar.info("Tentando extrair a Tabela 2 (página 4) do PDF.")
            
            # Coordenadas da área da Tabela 2 (para ambos VC-M e VC-P).
            # Ajuste estas coordenadas [top, left, bottom, right] conforme necessário.
            # Usei valores aproximados com base na visualização do PDF.
            area_table2 = [385, 90, 680, 810] 
            
            # Colunas aproximadas para 'Parameter', e os dias (0, 30, 60, 90, 120)
            # O tabula tentará dividir com base nestes pontos de corte.
            # A tabela tem colunas como 'Parameter', 'Initial', 'Day 30', etc., e sub-colunas para 'Mean' e 'SD'.
            # tabula.read_pdf pode juntar Mean e SD na mesma célula ou separá-los em colunas diferentes.
            # O pós-processamento será crucial.
            columns_table2 = [190, 260, 320, 380, 440, 500, 560, 620, 680, 740] # Ajustar essas colunas para pegar Mean e SD

            tables = tabula.read_pdf(
                io.BytesIO(uploaded_file.getvalue()), # Passa o conteúdo do arquivo como bytes
                pages=4,
                multiple_tables=False,
                area=area_table2,
                columns=columns_table2,
                output_format='dataframe',
                lattice=True, # Usar lattice=True para tabelas com linhas de grade (que é o caso da Tabela 2)
                pandas_options={'header': None} # tabula nem sempre infere o cabeçalho corretamente
            )
            
            if tables:
                df_raw = tables[0]
                st.sidebar.write("DataFrame cru extraído (Tabela 2, Pág 4):")
                st.sidebar.dataframe(df_raw)

                # --- Pós-processamento do DataFrame extraído ---
                # A Tabela 2 do artigo tem uma estrutura de cabeçalho multinível e dados "Mean ± SD".
                # O tabula pode extrair de forma complexa. Vamos focar em pegar os valores Mean e SD.

                # A primeira coluna geralmente é o parâmetro.
                # As colunas 1, 3, 5, 7, 9 contêm os valores para 'Initial' (Day 0), 'Day 30', 'Day 60', 'Day 90', 'Day 120'.
                # As colunas 2, 4, 6, 8, 10 conteriam os SDs, mas muitas vezes tabula agrupa "Mean ± SD"
                
                # Nomes dos parâmetros como aparecem no PDF
                pdf_param_names = {
                    'TKN (g kg-1)': 'TKN (gkg⁻¹)',
                    'Total P (g kg-1)': 'Total P (gkg⁻¹)',
                    'TK (g kg-1)': 'TK (gkg⁻¹)',
                    'pH (H2O)': 'pH (H₂O)',
                    'C/N ratio': 'C/N ratio'
                }
                
                # Dias no artigo (Day 0 é Day 1 na nossa aplicação)
                pdf_days = ['Initial', 'Day 30', 'Day 60', 'Day 90', 'Day 120']
                
                # Lista para armazenar os dados de média e desvio padrão para simulação
                extracted_data_for_simulation = {}

                # Iterar sobre as linhas do DataFrame extraído para parsear
                # As linhas dos parâmetros começam tipicamente na linha 2 (índex 1) do DF bruto,
                # assumindo que a primeira linha pode ser parte do cabeçalho
                for idx, row in df_raw.iterrows():
                    param_raw_name = str(row.iloc[0]).strip() # Assume que o parâmetro está na primeira coluna
                    
                    # Ignorar linhas que não são parâmetros ou são cabeçalhos residuais
                    if param_raw_name not in pdf_param_names and not any(p in param_raw_name for p in pdf_param_names):
                        continue
                    
                    # Tentar encontrar o nome padronizado do parâmetro
                    standard_param_name = None
                    for pdf_name, std_name in pdf_param_names.items():
                        if pdf_name in param_raw_name:
                            standard_param_name = std_name
                            break
                    
                    if standard_param_name:
                        extracted_data_for_simulation[standard_param_name] = {}
                        col_offset = 1 # A partir da segunda coluna (índex 1) começam os dados dos dias
                        
                        for i, day_name in enumerate(pdf_days):
                            cell_value = str(row.iloc[col_offset + i*2]).strip() # Assume Mean em colunas ímpares
                            
                            # Expressão regular para extrair média e desvio padrão (ex: "20.8 ± 0.5")
                            match = re.match(r"(\d+\.?\d*)\s*±\s*(\d+\.?\d*)", cell_value)
                            if match:
                                mean_val = float(match.group(1))
                                stdev_val = float(match.group(2))
                                extracted_data_for_simulation[standard_param_name][day_name] = {
                                    'mean': mean_val,
                                    'stdev': stdev_val
                                }
                            else:
                                # Tenta extrair apenas o número se não encontrar '±'
                                try:
                                    mean_val = float(cell_value)
                                    # Se não houver SD explícito, usamos um SD pequeno ou 0 para simular
                                    stdev_val = 0.01 * mean_val # Um pequeno percentual da média
                                    if stdev_val == 0: stdev_val = 0.01 # Evita SD zero
                                    extracted_data_for_simulation[standard_param_name][day_name] = {
                                        'mean': mean_val,
                                        'stdev': stdev_val
                                    }
                                except ValueError:
                                    # Não foi possível extrair. Deixa como NaN ou lida com o erro.
                                    extracted_data_for_simulation[standard_param_name][day_name] = {'mean': np.nan, 'stdev': np.nan}
                
                # Agora, simular réplicas com base nos dados extraídos do PDF
                num_replications_from_pdf = 3 # Assumindo 3 réplicas pelo estudo (ou valor que você especificar)
                replicated_pdf_data = []
                
                app_days_map = {
                    'Initial': 'Day 1', # Mapeia 'Initial' do PDF para 'Day 1' na aplicação
                    'Day 30': 'Day 30',
                    'Day 60': 'Day 60',
                    'Day 90': 'Day 90',
                    'Day 120': 'Day 120'
                }

                for param_name, daily_stats in extracted_data_for_simulation.items():
                    for _ in range(num_replications_from_pdf):
                        row_data = {'Parameter': param_name, 'Substrate': 'VC-M'} # Assumindo VC-M para este exemplo
                        for pdf_day_name, app_day_name in app_days_map.items():
                            stats = daily_stats.get(pdf_day_name)
                            if stats and not np.isnan(stats['mean']) and not np.isnan(stats['stdev']):
                                simulated_value = np.random.normal(loc=stats['mean'], scale=stats['stdev'], size=1)[0]
                                
                                # Aplicar limites para valores simulados (pH, não-negativos)
                                if param_name == 'pH (H₂O)':
                                    simulated_value = max(0.0, min(14.0, simulated_value))
                                elif 'gkg⁻¹' in param_name or 'ratio' in param_name:
                                    simulated_value = max(0.0, simulated_value)
                                    
                                row_data[app_day_name] = simulated_value
                            else:
                                row_data[app_day_name] = np.nan
                        replicated_pdf_data.append(row_data)

                df = pd.DataFrame(replicated_pdf_data)
                
                # Remove linhas que possam ter vindo vazias ou com apenas NaN nos dias
                df = df.dropna(subset=['Day 1', 'Day 30', 'Day 60', 'Day 90', 'Day 120'], how='all')

                if df.empty:
                    st.warning("Tabela extraída, mas nenhum dado relevante foi encontrado ou simulado após a limpeza. Usando dados de exemplo.")
                    df = load_sample_data_with_stdev()
                else:
                    st.sidebar.success("Tabela extraída e réplicas simuladas com sucesso!")

            else:
                st.sidebar.warning("Nenhuma tabela encontrada na página 4 com os parâmetros especificados. Usando dados de exemplo.")
                df = load_sample_data_with_stdev()
            # --- Fim da Extração Específica para o PDF Anexado ---

        except Exception as e:
            st.sidebar.error(f"Erro na extração ou processamento do PDF: {str(e)}")
            st.error("Não foi possível extrair ou processar a tabela. Usando dados de exemplo.")
            df = load_sample_data_with_stdev()

    ## Pré-visualização dos Dados
    st.header("Pré-visualização dos Dados")
    st.dataframe(df.head())
    st.markdown("---")

    ## Configuração de Análise
    st.sidebar.header("Configuração de Análise")
    
    unique_params_in_df = df['Parameter'].unique().tolist()
    
    # Mapeamento para exibição amigável
    display_param_mapping = {
        "TKN (gkg⁻¹)": "Nitrogênio Total (N)",
        "Total P (gkg⁻¹)": "Fósforo Total (P)",
        "TK (gkg⁻¹)": "Potássio Total (K)",
        "pH (H₂O)": "pH",
        "C/N ratio": "Relação C/N"
    }
    
    # Criar uma lista para o multiselect que usa os nomes amigáveis
    options_for_multiselect = [
        display_param_mapping.get(p_df, p_df) for p_df in unique_params_in_df
        if p_df in display_param_mapping or p_df # Inclui se está no mapeamento ou se não tem mapeamento
    ]

    # Definir os padrões com base nas opções disponíveis
    default_selected_params = []
    for p_key in ["TKN (gkg⁻¹)", "Total P (gkg⁻¹)", "pH (H₂O)", "C/N ratio"]: # Incluindo C/N como default
        if p_key in unique_params_in_df:
            default_selected_params.append(display_param_mapping.get(p_key, p_key))

    parameters = st.sidebar.multiselect(
        "Selecione os parâmetros para análise:",
        options=options_for_multiselect,
        default=default_selected_params
    )
    
    # Mapeamento reverso para obter o nome da coluna do DataFrame
    param_mapping_reverse = {v: k for k, v in display_param_mapping.items()}

    ## Realizar Testes Estatísticos
    results = []
    
    # Determinar o número de gráficos para subplots
    num_plots = len(parameters)
    if num_plots > 0:
        # Ajusta o tamanho da figura dinamicamente
        fig, axes = plt.subplots(num_plots, 1, figsize=(10, 5 * num_plots))
        if num_plots == 1:
            axes = [axes] # Garante que axes seja sempre uma lista para iteração

        for i, param_display_name in enumerate(parameters):
            col_name_in_df = param_mapping_reverse.get(param_display_name, param_display_name) # Usar o nome real da coluna no DF
            param_df = df[df['Parameter'] == col_name_in_df]

            # Extrair dados para cada dia
            app_days_ordered = ['Day 1', 'Day 30', 'Day 60', 'Day 90', 'Day 120']
            
            # Coleta os dados de cada dia. Cada elemento em 'data' será uma array de valores
            # para aquele dia (todas as réplicas simuladas para aquele parâmetro naquele dia).
            data = []
            valid_days_for_plot = []
            for day in app_days_ordered:
                if day in param_df.columns:
                    day_values = param_df[day].dropna().values
                    if len(day_values) > 0:
                        data.append(day_values)
                        valid_days_for_plot.append(day) # Apenas dias com dados para o gráfico
            
            # O teste de Kruskal-Wallis requer pelo menos 2 grupos com dados.
            if len(data) >= 2 and all(len(d) > 0 for d in data):
                h_stat, p_val = kruskal(*data)
                results.append({
                    "Parâmetro": param_display_name,
                    "H-Statistic": h_stat,
                    "p-value": p_val,
                    "Significativo (p<0.05)": p_val < 0.05
                })

                # Criar gráfico
                ax = axes[i]
                for j, day_data in enumerate(data):
                    # Plotar cada ponto individualmente
                    ax.scatter([j] * len(day_data), day_data, alpha=0.6, label=f"{app_days_ordered[j].replace('Day ', 'Dia ')}")

                # Adicionar linha de tendência (medianas)
                medians = [np.median(day_data) for day_data in data]
                ax.plot(range(len(data)), medians, 'ro-', markersize=8)

                ax.set_title(f"Evolução do {param_display_name}")
                ax.set_ylabel(param_display_name.split('(')[0].strip())
                ax.set_xticks(range(len(data)))
                ax.set_xticklabels([d.replace('Day ', '') for d in valid_days_for_plot]) # Rótulos dos dias
                ax.grid(True, alpha=0.3)
                ax.legend()

                # Adicionar resultado do teste ao gráfico
                ax.annotate(f"Kruskal-Wallis: H = {h_stat:.2f}, p = {p_val:.4f}",
                            xy=(0.5, 0.05), xycoords='axes fraction',
                            ha='center', fontsize=9,
                            bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.3))
            else:
                st.warning(f"Dados insuficientes ou inconsistentes para o parâmetro '{param_display_name}' para realizar a análise de Kruskal-Wallis. Verifique a extração do PDF ou os dados de exemplo.")
    else:
        st.warning("Nenhum parâmetro selecionado para análise.")
        return

    st.header("Resultados Estatísticos")
    results_df = pd.DataFrame(results)
    if not results_df.empty:
        st.dataframe(results_df.style.apply(
            lambda x: ['background-color: #fffd8e' if x['p-value'] < 0.05 else '' for _ in x],
            axis=1
        ))
    else:
        st.info("Nenhum resultado estatístico para exibir. Verifique a seleção de parâmetros e os dados.")
    st.markdown("---")

    ## Evolução Temporal dos Parâmetros
    st.header("Evolução Temporal dos Parâmetros")
    # Tenta plotar apenas se houver uma figura criada e parâmetros selecionados
    if 'fig' in locals() and fig is not None and num_plots > 0:
        st.pyplot(fig)
    else:
        st.info("Nenhum gráfico para exibir. Selecione parâmetros para visualizá-los.")
    st.markdown("---")

    ## Interpretação dos Resultados
    st.header("Interpretação dos Resultados")
    if not results_df.empty:
        for res in results:
            st.subheader(res["Parâmetro"])
            if res["p-value"] < 0.05:
                st.success(f"✅ Diferenças estatisticamente significativas (p = {res['p-value']:.4f})")
                st.markdown("""
                - **Rejeitamos a hipótese nula (H₀)**.
                - Há evidências de que os valores do parâmetro **mudam significativamente** ao longo do tempo.
                - A vermicompostagem afeta este parâmetro.
                """)
            else:
                st.warning(f"❌ Sem diferenças significativas (p = {res['p-value']:.4f})")
                st.markdown("""
                - **Aceitamos a hipótese nula (H₀)**.
                - Não há evidências suficientes de mudanças significativas.
                - O parâmetro permanece estável durante o processo de vermicompostagem.
                """)
    else:
        st.info("Nenhuma interpretação disponível, pois não há resultados estatísticos.")
    st.markdown("---")

    ## Sobre a Metodologia
    st.sidebar.header("Sobre a Metodologia")
    st.sidebar.info("""
    **Teste de Kruskal-Wallis:**
    - Teste não paramétrico equivalente à ANOVA de uma via.
    - Usado quando os dados não atendem aos pressupostos de normalidade ou para pequenas amostras.
    - Compara as medianas de três ou mais grupos independentes para determinar se há diferenças significativas.

    **Hipóteses:**
    - H₀ (Hipótese Nula): As distribuições dos valores do parâmetro são iguais em todos os grupos (dias).
    - H₁ (Hipótese Alternativa): Pelo menos um grupo (dia) difere dos demais em sua distribuição.

    **Significância (p-valor):**
    - **p < 0.05**: Rejeita H₀. Há diferenças estatisticamente significativas entre os grupos, indicando que a vermicompostagem influencia o parâmetro.
    - **p ≥ 0.05**: Aceita H₀. Não há evidências suficientes para afirmar diferenças significativas, sugerindo que o parâmetro é estável ou não é impactado de forma estatisticamente detectável.
    """)

if __name__ == "__main__":
    main()
