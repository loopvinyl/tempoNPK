# ===================================================================
# MÓDULO JORDÃO ET AL. (2007) - ANÁLISE COMPARATIVA (CORRIGIDA)
# ===================================================================
def run_jordao_analysis():
    """Módulo para análise comparativa de tratamentos (versão corrigida)"""
    
    # Mapeamento de parâmetros
    PARAM_MAPPING = {
        "pH": "pH",
        "Organic Matter": "Matéria Orgânica",
        "C/N ratio": "Relação C/N",
        "Cu": "Cobre",
        "Ni": "Níquel",
        "Zn": "Zinco",
        "Cu_leaves": "Cobre nas Folhas",
        "Ni_leaves": "Níquel nas Folhas",
        "Zn_leaves": "Zinco nas Folhas",
        "Cu_roots": "Cobre nas Raízes",
        "Ni_roots": "Níquel nas Raízes",
        "Zn_roots": "Zinco nas Raízes",
    }
    
    # Função para carregar dados específicos do artigo
    @st.cache_data
    def load_jordao_sample_data():
        sample_data = {
            'Vermicompost Characterization': {
                'pH': {'mean': 7.1, 'stdev': 0.03},
                'Organic Matter': {'mean': 42.0, 'stdev': 0.34},
                'C/N ratio': {'mean': 11.85, 'stdev': 0.2},
                'Cu': {'mean': 31.0, 'stdev': 6.7},
                'Ni': {'mean': 21.7, 'stdev': 2.1},
                'Zn': {'mean': 108, 'stdev': 4.4}
            },
            'Lettuce Cultivation': {
                'Cu_leaves': {'mean': 8.1, 'stdev': 1.5},
                'Ni_leaves': {'mean': 35.3, 'stdev': 3.2},
                'Zn_leaves': {'mean': 1074.8, 'stdev': 85},
                'Cu_roots': {'mean': 246.3, 'stdev': 25},
                'Ni_roots': {'mean': 587.7, 'stdev': 45},
                'Zn_roots': {'mean': 1339.2, 'stdev': 120}
            }
        }
        
        treatments = ['Vermicompost Characterization', 'Lettuce Cultivation']
        num_replications = 3
        data = []
        
        for treatment, params in sample_data.items():
            for param_name, stats in params.items():
                for _ in range(num_replications):
                    row = {'Parameter': param_name, 'Treatment': treatment}
                    row['Value'] = np.random.normal(stats['mean'], stats['stdev'])
                    # Garantir valores não-negativos
                    if 'leaves' in param_name or 'roots' in param_name:
                        row['Value'] = max(0, row['Value'])
                    data.append(row)
        
        return pd.DataFrame(data)
    
    # Função para plotar comparação entre tratamentos (CORRIGIDA)
    def plot_parameter_comparison(ax, data, treatment_names, param_name):
        colors = ['#6f42c1', '#00c1e0', '#00d4b1']
        
        # Verificar se temos dados para plotar
        if not data or any(len(group) == 0 for group in data):
            ax.text(0.5, 0.5, 'Dados insuficientes para plotar', 
                    ha='center', va='center', fontsize=12, color='white')
            return ax
        
        # Calcular limites para eixo Y
        all_values = [val for group in data for val in group]
        if not all_values:
            ax.text(0.5, 0.5, 'Sem dados disponíveis', 
                    ha='center', va='center', fontsize=12, color='white')
            return ax
        
        y_min = min(all_values) * 0.9
        y_max = max(all_values) * 1.1
        
        for i, (treatment_data, treatment_name) in enumerate(zip(data, treatment_names)):
            # Plotar pontos individuais
            ax.scatter(
                [i] * len(treatment_data), 
                treatment_data,
                color=colors[i % len(colors)],
                alpha=0.7,
                s=80,
                label=treatment_name,
                edgecolors='white',
                linewidth=1,
                zorder=3
            )
            
            # Plotar mediana
            if len(treatment_data) > 0:
                median_val = np.median(treatment_data)
                ax.plot(
                    [i-0.2, i+0.2],
                    [median_val, median_val],
                    color='white',
                    linewidth=3,
                    zorder=5
                )
        
        # Configurações do gráfico
        ax.set_xticks(range(len(treatment_names)))
        ax.set_xticklabels(treatment_names, fontsize=11)
        ax.set_ylabel(PARAM_MAPPING.get(param_name, param_name), fontsize=12, fontweight='bold')
        ax.set_title(f"Comparação de {PARAM_MAPPING.get(param_name, param_name)}", 
                     fontsize=14, fontweight='bold', pad=15)
        ax.legend(loc='best', fontsize=10, framealpha=0.3)
        ax.grid(True, alpha=0.2, linestyle='--', color='#a0a7c0')
        ax.set_ylim(y_min, y_max)
        
        # Remover bordas
        for spine in ax.spines.values():
            spine.set_visible(False)
        
        # Fundo gradiente
        ax.set_facecolor('#0c0f1d')
        
        return ax

    # Interface principal do módulo Jordão
    st.markdown("""
    <div class="header-card">
        <h1 style="margin:0;padding:0;background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-size:2.5rem;">
            ⚗️ Análise de Remoção de Metais Pesados e Cultivo
        </h1>
        <p style="margin:0;padding-top:10px;color:#a0a7c0;font-size:1.1rem;">
        Jordão et al. (2007) - Redução de metais pesados em efluentes líquidos por vermicompostos
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Voltar para seleção de artigos"):
        del st.session_state['selected_article']
        st.rerun()
    
    # Carregar dados
    df = load_jordao_sample_data()
    
    # Painel de configurações (agora na área principal)
    st.markdown("""
    <div class="card">
        <h2 style="display:flex;align-items:center;gap:10px;">
            <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                ⚙️ Configurações de Análise
            </span>
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        analysis_type = st.radio(
            "Tipo de análise:",
            ('Caracterização do Vermicomposto', 'Cultivo de Alface'),
            index=0,
            key="jordao_analysis_type"
        )
    
    with col2:
        # Filtrar parâmetros baseado no tipo de análise
        if analysis_type == 'Caracterização do Vermicomposto':
            param_options = [p for p in df['Parameter'].unique() 
                           if p in ['pH', 'Organic Matter', 'C/N ratio', 'Cu', 'Ni', 'Zn']]
        else:
            param_options = [p for p in df['Parameter'].unique() 
                           if p in ['Cu_leaves', 'Ni_leaves', 'Zn_leaves', 
                                    'Cu_roots', 'Ni_roots', 'Zn_roots']]
        
        selected_params = st.multiselect(
            "Selecione os parâmetros:",
            options=param_options,
            default=param_options[:2] if param_options else [],
            key="jordao_param_select"
        )
    
    # Pré-visualização dos dados
    st.markdown("""
    <div class="card">
        <h2 style="display:flex;align-items:center;gap:10px;">
            <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                🔍 Dados do Estudo
            </span>
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(df)
    st.markdown(f"**Total de amostras:** {len(df)}")
    
    # Análise estatística
    results = []
    
    # Configurar subplots
    num_plots = len(selected_params) if selected_params else 0
    
    if num_plots > 0:
        fig = plt.figure(figsize=(10, 6 * num_plots))
        gs = fig.add_gridspec(num_plots, 1, hspace=0.6)
        axes = [fig.add_subplot(gs[i]) for i in range(num_plots)]
        
        for i, param in enumerate(selected_params):
            param_data = []
            treatment_labels = []
            
            # Coletar dados apenas para tratamentos relevantes
            relevant_treatments = ['Vermicompost Characterization'] if analysis_type == 'Caracterização do Vermicomposto' else ['Lettuce Cultivation']
            
            for treatment in relevant_treatments:
                # Filtrar dados para o parâmetro e tratamento específico
                treatment_data = df[(df['Parameter'] == param) & 
                                  (df['Treatment'] == treatment)]['Value'].dropna().values
                
                # Verificar se temos dados
                if len(treatment_data) > 0:
                    param_data.append(treatment_data)
                    treatment_labels.append(treatment)
                else:
                    st.warning(f"Parâmetro '{param}' não encontrado no tratamento '{treatment}'")

            # Verificar se temos dados suficientes para análise
            if len(param_data) >= 1:
                # Plotar gráfico
                ax = axes[i]
                plot_parameter_comparison(ax, param_data, treatment_labels, param)
                
                # Adicionar título descritivo
                ax.set_title(f"{PARAM_MAPPING.get(param, param)} - {analysis_type}", 
                            fontsize=14, fontweight='bold', pad=15)
                
                # Adicionar estatísticas descritivas
                if len(param_data) > 0:
                    all_vals = np.concatenate(param_data)
                    mean_val = np.mean(all_vals)
                    std_val = np.std(all_vals)
                    
                    stats_text = f"Média: {mean_val:.2f} | Desvio Padrão: {std_val:.2f}"
                    ax.text(
                        0.5, 0.05, 
                        stats_text,
                        transform=ax.transAxes,
                        ha='center',
                        va='bottom',
                        fontsize=11,
                        color='white',
                        bbox=dict(
                            boxstyle="round,pad=0.3",
                            facecolor='#2a2f45',
                            alpha=0.8,
                            edgecolor='none'
                        )
                    )
            else:
                # Plotar gráfico vazio com mensagem de aviso
                ax = axes[i]
                ax.text(0.5, 0.5, 'Dados insuficientes para análise', 
                        ha='center', va='center', fontsize=12, color='yellow')
    
    # Resultados estatísticos
    st.markdown("""
    <div class="card">
        <h2 style="display:flex;align-items:center;gap:10px;">
            <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                📊 Visualização dos Parâmetros
            </span>
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Gráficos
    if num_plots > 0:
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Nenhum parâmetro selecionado para visualização.")
    
    # Referência
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
            JORDÃO, C.P.; FIALHO, L.L.; NEVES, J.C.L.; CECON, P.R.; MENDONÇA, E.S.; FONTES, R.L.F. 
            Reduction of heavy metal contents in liquid effluents by vermicomposts and the use of the metal-enriched vermicomposts in lettuce cultivation. 
            <strong>Bioresource Technology</strong>, 
            v. 98, p. 2800-2813, 2007.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Informações adicionais sobre o estudo
    st.markdown("""
    <div class="info-card">
        <h3 style="display:flex;align-items:center;color:#00c1e0;">
            <span class="info-icon">ℹ️</span> Sobre o Estudo de Jordão et al. (2007)
        </h3>
        <div style="margin-top:15px; color:#d7dce8; line-height:1.7;">
            <p>
                Este estudo investiga a capacidade dos vermicompostos na remoção de metais pesados
                de efluentes líquidos e seu uso subsequente no cultivo de alface. A pesquisa
                demonstra que vermicompostos enriquecidos com metais podem ser utilizados com
                segurança na agricultura, desde que monitorados os níveis de acúmulo nas plantas.
            </p>
            <p>
                <b>Principais conclusões:</b>
                <ul>
                    <li>Vermicompostos removem eficientemente metais pesados de efluentes</li>
                    <li>Metais são imobilizados em formas menos biodisponíveis</li>
                    <li>Alface cultivada com vermicomposto mostrou crescimento satisfatório</li>
                    <li>Metais acumulam-se principalmente nas raízes, não nas partes comestíveis</li>
                </ul>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
