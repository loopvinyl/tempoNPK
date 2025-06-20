import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import kruskal
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MaxNLocator

# Configurações gerais com tema escuro
st.set_page_config(
    page_title="Análise de Metais Pesados em Alface", 
    layout="wide",
    page_icon="🌱"
)

# CSS para tema escuro premium
st.markdown("""
<style>
    /* [Manter todo o CSS original] */
</style>
""", unsafe_allow_html=True)

# Título com estilo moderno
st.markdown("""
<div class="header-card">
    <h1 style="margin:0;padding:0;background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-size:2.5rem;">
        🌱 Análise de Metais Pesados em Alface (Jordão et al., 2007)
    </h1>
    <p style="margin:0;padding-top:10px;color:#a0a7c0;font-size:1.1rem;">
    Concentrações de Cu, Ni e Zn em função de doses de vermicomposto
    </p>
</div>
""", unsafe_allow_html=True)

## Mapeamento de parâmetros para nomes amigáveis
PARAM_MAPPING = {
    "Cu in leaves (mg/kg)": "Concentração de Cu nas Folhas",
    "Cu in roots (mg/kg)": "Concentração de Cu nas Raízes",
    "Ni in leaves (mg/kg)": "Concentração de Ni nas Folhas",
    "Ni in roots (mg/kg)": "Concentração de Ni nas Raízes",
    "Zn in leaves (mg/kg)": "Concentração de Zn nas Folhas",
    "Zn in roots (mg/kg)": "Concentração de Zn nas Raízes"
}

## Mapeamento de doses
DOSE_MAPPING = {
    'Dose 25': 25,
    'Dose 50': 50,
    'Dose 65': 65,
    'Dose 80': 80
}

## Equações de regressão da Tabela 6
REGRESSION_EQUATIONS = {
    "Natural": {
        "Cu in leaves (mg/kg)": lambda x: 2.8,
        "Cu in roots (mg/kg)": lambda x: 10.9,
        "Ni in leaves (mg/kg)": lambda x: 2.1,
        "Ni in roots (mg/kg)": lambda x: 5.8,
        "Zn in leaves (mg/kg)": lambda x: 47.79,
        "Zn in roots (mg/kg)": lambda x: 60.6
    },
    "Enriquecido com Cu": {
        "Cu in leaves (mg/kg)": lambda x: 2.6 + 0.1253*x - 0.000716*x**2,
        "Cu in roots (mg/kg)": lambda x: 14.1 + 2.9027*x,
        "Ni in leaves (mg/kg)": lambda x: 1.3,
        "Ni in roots (mg/kg)": lambda x: 8.3,
        "Zn in leaves (mg/kg)": lambda x: 49.26,
        "Zn in roots (mg/kg)": lambda x: 58.8
    },
    "Enriquecido com Ni": {
        "Cu in leaves (mg/kg)": lambda x: 2.2 + 0.0165*x,
        "Cu in roots (mg/kg)": lambda x: 10.5,
        "Ni in leaves (mg/kg)": lambda x: 1.2 + 0.7168*x - 0.00377*x**2,
        "Ni in roots (mg/kg)": lambda x: 53.8 + 17.3756*x - 0.14137*x**2,
        "Zn in leaves (mg/kg)": lambda x: 42.93,
        "Zn in roots (mg/kg)": lambda x: 60.88
    },
    "Enriquecido com Zn": {
        "Cu in leaves (mg/kg)": lambda x: 2.2 + 0.0967*x - 0.00104*x**2,
        "Cu in roots (mg/kg)": lambda x: 12.9,
        "Ni in leaves (mg/kg)": lambda x: 2.0,
        "Ni in roots (mg/kg)": lambda x: 10.9,
        "Zn in leaves (mg/kg)": lambda x: -24.0 + 29.4827*x - 0.2068*x**2,
        "Zn in roots (mg/kg)": lambda x: 162.93 + 6.9758*x + 0.09659*x**2
    }
}

## Desvios padrão estimados com base no artigo
STDEV_ESTIMATES = {
    "Cu in leaves (mg/kg)": 0.5,
    "Cu in roots (mg/kg)": 15.0,
    "Ni in leaves (mg/kg)": 0.3,
    "Ni in roots (mg/kg)": 20.0,
    "Zn in leaves (mg/kg)": 5.0,
    "Zn in roots (mg/kg)": 30.0
}

## Função para Carregar Dados de Exemplo
@st.cache_data
def load_sample_data(vermicompost_type):
    doses = [25, 50, 65, 80]
    num_replications = 3
    all_data = []
    
    for param_name in PARAM_MAPPING.keys():
        for _ in range(num_replications):
            row = {'Parameter': param_name, 'Vermicompost Type': vermicompost_type}
            for dose in doses:
                # Calcular valor baseado na equação de regressão
                base_value = REGRESSION_EQUATIONS[vermicompost_type][param_name](dose)
                
                # Adicionar variação aleatória baseada no desvio padrão estimado
                stdev = STDEV_ESTIMATES[param_name]
                simulated_value = np.random.normal(loc=base_value, scale=stdev)
                
                # Garantir valores não negativos
                row[f'Dose {dose}'] = max(0.0, simulated_value)
                
            all_data.append(row)
    
    return pd.DataFrame(all_data)

## Função para plotar evolução das concentrações
def plot_parameter_evolution(ax, data, doses, param_name):
    # Paleta de cores moderna
    colors = ['#6f42c1', '#00c1e0', '#00d4b1', '#ffd166', '#ff6b6b']
    
    for i, dose in enumerate(doses):
        group_data = data[i]
        
        # Plotar pontos individuais
        ax.scatter(
            [dose] * len(group_data), 
            group_data, 
            alpha=0.85, 
            s=100,
            color=colors[i % len(colors)],
            edgecolors='white',
            linewidth=1.2,
            zorder=3,
            label=f"{dose} t ha⁻¹",
            marker='o'
        )
    
    # Calcular e plotar medianas
    medians = [np.median(group) for group in data]
    ax.plot(
        doses, 
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
    
    # Configurar eixo X
    ax.set_xticks(doses)
    ax.set_xticklabels([str(d) for d in doses], fontsize=11)
    
    # Melhorar formatação
    ax.set_xlabel("Dose de Vermicomposto (t ha⁻¹)", fontsize=12, fontweight='bold', labelpad=15)
    ax.set_ylabel(PARAM_MAPPING.get(param_name, param_name), fontsize=12, fontweight='bold', labelpad=15)
    ax.set_title(f"Evolução da {PARAM_MAPPING.get(param_name, param_name)}", 
                    fontsize=14, fontweight='bold', pad=20)
    
    # Grid e estilo
    ax.grid(True, alpha=0.2, linestyle='--', color='#a0a7c0', zorder=1)
    ax.legend(loc='best', fontsize=10, framealpha=0.25, title="Doses")
    
    # Remover bordas
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Fundo gradiente
    ax.set_facecolor('#0c0f1d')
    
    return ax

## Função para exibir resultados com design premium
def display_results_interpretation(results):
    # [Manter função idêntica ao original]

## Função Principal
def main():
    # Inicialização de variáveis
    vermicompost_types = list(REGRESSION_EQUATIONS.keys())
    default_type = vermicompost_types[0]
    
    # Sidebar premium
    with st.sidebar:
        st.markdown("""
        <div class="card">
            <h3 style="display:flex;align-items:center;gap:10px;">
                <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:3px 12px;border-radius:30px;font-size:1rem;">
                    📂 Configuração do Vermicomposto
                </span>
            </h3>
        """, unsafe_allow_html=True)
        
        selected_type = st.selectbox(
            "Tipo de Vermicomposto:",
            options=vermicompost_types,
            index=0,
            key="vermicompost_type"
        )
        
        st.markdown("""
        <div class="card">
            <h3 style="display:flex;align-items:center;gap:10px;">
                <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:3px 12px;border-radius:30px;font-size:1rem;">
                    ⚙️ Parâmetros de Análise
                </span>
            </h3>
        """, unsafe_allow_html=True)
        
        param_options = list(PARAM_MAPPING.values())
        selected_params = st.multiselect(
            "Selecione os parâmetros:",
            options=param_options,
            default=param_options[:2],
            key="param_select"
        )
        
        st.markdown("""
        <div class="card">
            <h3 style="display:flex;align-items:center;gap:10px;">
                <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:3px 12px;border-radius:30px;font-size:1rem;">
                    📚 Contexto Científico
                </span>
            </h3>
            <div style="color:#d7dce8; line-height:1.7;">
                <p>Estudo analisa a absorção de metais pesados (Cu, Ni, Zn) pela alface cultivada em solos com vermicomposto:</p>
                <ul style="padding-left:20px;">
                    <li>Vermicomposto natural e enriquecido com metais</li>
                    <li>4 doses de aplicação (25-80 t ha⁻¹)</li>
                    <li>Avaliação em folhas e raízes</li>
                    <li>Baseado em Jordão et al. (2007)</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Carregar dados
    df = load_sample_data(selected_type)
    
    # Pré-visualização dos Dados
    st.markdown("""
    <div class="card">
        <h2 style="display:flex;align-items:center;gap:10px;">
            <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                🔍 Dados Simulados (Baseados em Jordão et al., 2007)
            </span>
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(df)
    st.markdown(f"**Tipo de Vermicomposto:** {selected_type} | **Total de amostras:** {len(df)}")
    
    # Explicação sobre simulação de dados
    st.markdown("""
    <div class="info-card">
        <h3 style="display:flex;align-items:center;color:#00c1e0;">
            <span class="info-icon">ℹ️</span> Metodologia de Simulação de Dados
        </h3>
        <div style="margin-top:15px; color:#d7dce8; line-height:1.7;">
            <p>Os dados foram simulados com base nas equações de regressão publicadas por Jordão et al. (2007):</p>
            <ol>
                <li>Utilização das equações da Tabela 6 para calcular valores médios</li>
                <li>Adição de variação aleatória baseada em desvios padrão estimados</li>
                <li>Geração de 3 réplicas por tratamento</li>
                <li>Valores negativos convertidos para zero</li>
            </ol>
            <p><b>Equação exemplo (Cu nas folhas - Vermicomposto com Cu):</b><br>
            Y = 2.6 + 0.1253*X - 0.000716*X²</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # Converter parâmetros selecionados para nomes originais
    reverse_mapping = {v: k for k, v in PARAM_MAPPING.items()}
    selected_original_params = [reverse_mapping[p] for p in selected_params]
    
    # Realizar Análise Estatística
    results = []
    doses = [25, 50, 65, 80]
    dose_columns = [f'Dose {d}' for d in doses]
    
    # Configurar subplots
    num_plots = len(selected_original_params)
    if num_plots > 0:
        fig = plt.figure(figsize=(10, 6 * num_plots))
        gs = fig.add_gridspec(num_plots, 1, hspace=0.6)
        axes = [fig.add_subplot(gs[i]) for i in range(num_plots)]
        
        for i, param in enumerate(selected_original_params):
            param_df = df[df['Parameter'] == param]
            
            # Coletar dados por dose
            data_by_dose = []
            for dose_col in dose_columns:
                if dose_col in param_df.columns:
                    dose_data = param_df[dose_col].dropna().values
                    if len(dose_data) > 0:
                        data_by_dose.append(dose_data)
            
            # Executar teste de Kruskal-Wallis
            if len(data_by_dose) >= 2:
                try:
                    h_stat, p_val = kruskal(*data_by_dose)
                    results.append({
                        "Parâmetro": PARAM_MAPPING.get(param, param),
                        "H-Statistic": h_stat,
                        "p-value": p_val,
                        "Significativo (p<0.05)": p_val < 0.05
                    })
                    
                    # Plotar gráfico
                    ax = axes[i]
                    plot_parameter_evolution(ax, data_by_dose, doses, param)
                    
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
            else:
                st.warning(f"Dados insuficientes para {PARAM_MAPPING.get(param, param)}")
    
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
        results_df = pd.DataFrame(results)
        results_df['Significância'] = results_df['p-value'].apply(
            lambda p: "✅ Sim" if p < 0.05 else "❌ Não"
        )
        results_df = results_df[['Parâmetro', 'H-Statistic', 'p-value', 'Significância']]
        
        st.dataframe(
            results_df.style
            .format({"p-value": "{:.4f}", "H-Statistic": "{:.2f}"})
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
                    📊 Relação Dose-Concentração
                </span>
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f'<div style="margin-top:20px;margin-bottom:30px;color:#a0a7c0;font-size:1.1rem;text-align:center;">Tipo de Vermicomposto: <strong>{selected_type}</strong></div>', unsafe_allow_html=True)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    
    # Interpretação
    display_results_interpretation(results)
    
    # Referência Bibliográfica
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
            JORDÃO, C. P. et al. Reduction of heavy metal contents in liquid effluents by vermicomposts 
            and the use of the metal-enriched vermicomposts in lettuce cultivation. 
            <strong>Bioresource Technology</strong>, v. 98, n. 14, p. 2800-2813, 2007.
        </p>
        <p style="margin-top:15px;">
            <strong>Resumo:</strong> O estudo avaliou a eficiência do vermicomposto na remoção de metais pesados 
            (Cu, Ni, Zn) de efluentes de galvanoplastia e o uso subsequente do vermicomposto enriquecido 
            no cultivo de alface. Os resultados mostraram alta eficiência na remoção de metais (>95%) e 
            padrões distintos de acumulação nas folhas e raízes da alface.
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
