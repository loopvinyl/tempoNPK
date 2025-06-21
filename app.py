# ===================================================================
# MÓDULO SHARMA ET AL. (2019) - COMPARAÇÃO DE VERMICOMPOSTOS
# ===================================================================
def run_sharma_analysis():
    """Módulo para análise comparativa de vermicompostos por espécie"""
    
    # Mapeamento de parâmetros
    PARAM_MAPPING = {
        "pH": "pH",
        "EC": "Condutividade Elétrica (mho)",
        "OC": "Carbono Orgânico (%)",
        "N": "Nitrogênio (%)",
        "P": "Fósforo (%)",
        "K": "Potássio (%)",
        "Ca": "Cálcio (%)",
        "Mg": "Magnésio (%)",
        "C_N_ratio": "Razão C/N"
    }
    
    # Dados do estudo (extraídos do artigo)
    VERMICOMPOST_DATA = {
        "VKA": {  # Amynthus diffringens
            "pH": (7.38, 0.11),
            "EC": (3.66, 0.78),
            "OC": (11.30, 0.51),
            "N": (1.05, 0.08),
            "P": (2.88, 0.20),
            "K": (1.05, 0.11),
            "Ca": (0.23, 0.04),
            "Mg": (0.15, 0.02),
            "C_N_ratio": (10.71, 0.68)
        },
        "VKM": {  # Metaphire houlleti
            "pH": (7.35, 0.20),
            "EC": (3.51, 0.59),
            "OC": (11.26, 0.17),
            "N": (1.05, 0.15),
            "P": (2.70, 0.05),
            "K": (1.03, 0.03),
            "Ca": (0.24, 0.03),
            "Mg": (0.14, 0.03),
            "C_N_ratio": (11.27, 1.51)
        },
        "VKO": {  # Octolasion tyrateum
            "pH": (7.28, 0.28),
            "EC": (3.82, 0.74),
            "OC": (11.66, 0.34),
            "N": (1.17, 0.20),
            "P": (2.97, 0.32),
            "K": (1.18, 0.15),
            "Ca": (0.26, 0.04),
            "Mg": (0.17, 0.04),
            "C_N_ratio": (10.19, 1.77)
        },
        "Original": {  # Solo original
            "pH": (7.98, 0.01),
            "EC": (1.35, 0.01),
            "OC": (7.96, 0.01),
            "N": (0.38, 0.01),
            "P": (1.23, 0.01),
            "K": (0.11, 0.01),
            "Ca": (0.09, 0.01),
            "Mg": (0.05, 0.01),
            "C_N_ratio": (20.94, 0.01)
        }
    }
    
    # Descrições dos grupos
    GROUP_DESCRIPTIONS = {
        "VKA": "Vermicomposto por Amynthus diffringens",
        "VKM": "Vermicomposto por Metaphire houlleti",
        "VKO": "Vermicomposto por Octolasion tyrateum",
        "Original": "Solo original (controle)"
    }

    # Função para carregar dados de exemplo
    @st.cache_data
    def load_sample_data(num_replications=5):
        all_data = []
        for group, params in VERMICOMPOST_DATA.items():
            for param, (mean, stdev) in params.items():
                for _ in range(num_replications):
                    # Gerar valor com distribuição normal
                    value = np.random.normal(mean, stdev)
                    # Garantir valores fisicamente possíveis
                    if param == "pH":
                        value = np.clip(value, 0, 14)
                    elif param in ["OC", "N", "P", "K", "Ca", "Mg"]:
                        value = max(0, value)
                    
                    all_data.append({
                        "Parameter": param,
                        "Group": group,
                        "Value": value
                    })
                    
        return pd.DataFrame(all_data)

    # Função para plotar comparação entre grupos
    def plot_group_comparison(ax, data, groups, param_name):
        # Paleta de cores moderna
        colors = ['#6f42c1', '#00c1e0', '#00d4b1', '#ffd166']
        
        for i, group in enumerate(groups):
            group_data = data[i]
            
            # Plotar pontos individuais
            ax.scatter(
                [i] * len(group_data), 
                group_data, 
                alpha=0.85, 
                s=100,
                color=colors[i % len(colors)],
                edgecolors='white',
                linewidth=1.2,
                zorder=3,
                label=GROUP_DESCRIPTIONS[group],
                marker='o'
            )
            
            # Plotar média e intervalo de confiança
            mean_val = np.mean(group_data)
            std_val = np.std(group_data)
            
            ax.errorbar(
                i, mean_val, 
                yerr=1.96*std_val/np.sqrt(len(group_data)),
                fmt='o',
                markersize=10,
                color='white',
                markeredgecolor='black',
                markeredgewidth=1.5,
                elinewidth=3,
                capsize=8,
                zorder=5
            )
        
        # Melhorar formatação
        ax.set_xticks(range(len(groups)))
        ax.set_xticklabels([GROUP_DESCRIPTIONS[g] for g in groups], rotation=15, ha="right", fontsize=10)
        
        ax.set_xlabel("Tipo de Amostra", fontsize=12, fontweight='bold', labelpad=15)
        ax.set_ylabel(PARAM_MAPPING.get(param_name, param_name), fontsize=12, fontweight='bold', labelpad=15)
        ax.set_title(f"Comparação de {PARAM_MAPPING.get(param_name, param_name)}", 
                     fontsize=14, fontweight='bold', pad=20)
        
        # Grid e estilo
        ax.grid(True, alpha=0.2, linestyle='--', color='#a0a7c0', zorder=1)
        ax.legend(loc='upper right', fontsize=9, framealpha=0.25)
        
        # Remover bordas
        for spine in ax.spines.values():
            spine.set_visible(False)
        
        # Fundo gradiente
        ax.set_facecolor('#0c0f1d')
        
        return ax

    # Função para exibir resultados
    def display_results_interpretation(results):
        st.markdown("""
        <div class="card">
            <h2 style="display:flex;align-items:center;gap:10px;">
                <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                    📝 Interpretação dos Resultados
                </span>
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        if not results:
            st.info("Nenhuma interpretação disponível.")
            return
        
        for res in results:
            param_name = res["Parâmetro"]
            p_val = res["p-value"]
            is_significant = p_val < 0.05
            
            card_class = "signif-card" if is_significant else "not-signif-card"
            icon = "✅" if is_significant else "❌"
            title_color = "#00c853" if is_significant else "#ff5252"
            status = "Significativo" if is_significant else "Não Significativo"
            
            st.markdown(f"""
            <div class="result-card {card_class}">
                <div style="display:flex; align-items:center; justify-content:space-between;">
                    <div style="display:flex; align-items:center; gap:12px;">
                        <div style="font-size:28px; color:{title_color};">{icon}</div>
                        <h3 style="margin:0; color:{title_color}; font-weight:600;">{param_name}</h3>
                    </div>
                    <div style="background:rgba(42, 47, 69, 0.7); padding:8px 18px; border-radius:30px; border:1px solid {title_color}30;">
                        <span style="font-weight:bold; font-size:1.1rem; color:{title_color};">{status}</span>
                        <span style="color:#a0a7c0; margin-left:8px;">p = {p_val:.4f}</span>
                    </div>
                </div>
                <div style="margin-top:20px; padding-top:15px; border-top:1px solid rgba(100, 110, 200, 0.2);">
            """, unsafe_allow_html=True)
            
            if is_significant:
                st.markdown("""
                    <div style="color:#e0e5ff; line-height:1.8;">
                        <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                            <span style="color:#00c853; font-size:1.5rem;">•</span>
                            <b>Diferenças significativas entre os tipos de vermicomposto</b>
                        </p>
                        <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                            <span style="color:#00c853; font-size:1.5rem;">•</span>
                            A espécie de minhoca influencia significativamente este parâmetro
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Adicionar observação específica para nutrientes
                if "Nitrogênio" in param_name or "Fósforo" in param_name or "Potássio" in param_name:
                    st.markdown("""
                    <div style="background:#2a2f45;padding:10px;border-radius:8px;margin-top:10px;">
                        <b>Relevância agronômica:</b> Os vermicompostos mostraram teores significativamente 
                        maiores de nutrientes em comparação com o solo original, indicando seu potencial 
                        como fertilizante orgânico.
                    </div>
                    """, unsafe_allow_html=True)
                    
            else:
                st.markdown("""
                    <div style="color:#e0e5ff; line-height:1.8;">
                        <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                            <span style="color:#ff5252; font-size:1.5rem;">•</span>
                            <b>Não foram encontradas diferenças significativas</b>
                        </p>
                        <p style="margin:12px 0; display:flex; align-items:center; gap:8px;">
                            <span style="color:#ff5252; font-size:1.5rem;">•</span>
                            A espécie de minhoca não afeta significativamente este parâmetro
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)

    # Interface principal do módulo
    st.markdown("""
    <div class="header-card">
        <h1 style="margin:0;padding:0;background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-size:2.5rem;">
            🪱 Comparação de Vermicompostos por Espécie de Minhoca
        </h1>
        <p style="margin:0;padding-top:10px;color:#a0a7c0;font-size:1.1rem;">
        Sharma (2019) - Gestão de resíduos de cozinha por vermicompostagem
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Voltar para seleção de artigos"):
        del st.session_state['selected_article']
        st.rerun()
    
    # Painel de informações do estudo
    st.markdown("""
    <div class="card">
        <h2 style="display:flex;align-items:center;gap:10px;">
            <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                🔬 Contexto do Estudo
            </span>
        </h2>
        <div style="margin-top:15px; padding:15px; background:rgba(26,29,50,0.5); border-radius:12px;">
            <p style="line-height:1.7;">
                Este estudo comparou a eficiência de três espécies de minhocas epigeicas locais de Jammu 
                (<i>Amynthus diffringens</i>, <i>Metaphire houlleti</i> e <i>Octolasion tyrateum</i>) 
                na produção de vermicomposto a partir de resíduos de cozinha. Os parâmetros físico-químicos 
                dos vermicompostos resultantes foram analisados e comparados com o solo original.
            </p>
            <p style="margin-top:10px; font-style:italic; color:#a0a7c0;">
                Fonte: Sharma, D. (2019). Kitchen waste management by vermicomposting using locally available 
                epigeic earthworm species. Journal of Applied and Natural Science, 11(2): 372-374
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregar dados
    df = load_sample_data()
    
    # Pré-visualização dos Dados
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
    
    # Explicação sobre geração de dados
    st.markdown("""
    <div class="info-card">
        <h3 style="display:flex;align-items:center;color:#00c1e0;">
            <span class="info-icon">ℹ️</span> Metodologia de Análise
        </h3>
        <div style="margin-top:15px; color:#d7dce8; line-height:1.7;">
            <p>
                Os dados foram gerados com base nas médias e desvios padrão reportados no estudo de Sharma (2019). 
                Para cada combinação de parâmetro e grupo, foram simuladas <b>5 réplicas</b> utilizando uma distribuição normal.
            </p>
            <p>
                <b>Grupos analisados:</b>
                <ul>
                    <li><b>VKA:</b> Vermicomposto por <i>Amynthus diffringens</i></li>
                    <li><b>VKM:</b> Vermicomposto por <i>Metaphire houlleti</i></li>
                    <li><b>VKO:</b> Vermicomposto por <i>Octolasion tyrateum</i></li>
                    <li><b>Original:</b> Solo original (controle)</li>
                </ul>
            </p>
            <p>
                O teste de Kruskal-Wallis foi aplicado para verificar se existem diferenças significativas 
                entre os grupos para cada parâmetro analisado.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # Seleção de parâmetros
    st.markdown("""
    <div class="card">
        <h2 style="display:flex;align-items:center;gap:10px;">
            <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                ⚙️ Parâmetros para Análise
            </span>
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    param_options = list(PARAM_MAPPING.values())
    selected_params = st.multiselect(
        "Selecione os parâmetros para análise:",
        options=param_options,
        default=param_options[:5],
        key="sharma_param_select"
    )
    
    # Realizar Análise
    if not selected_params:
        st.warning("Selecione pelo menos um parâmetro para análise.")
        return

    # Converter para nomes originais
    reverse_mapping = {v: k for k, v in PARAM_MAPPING.items()}
    selected_original_params = [reverse_mapping[p] for p in selected_params]
    
    results = []
    groups = list(GROUP_DESCRIPTIONS.keys())
    
    # Configurar subplots
    num_plots = len(selected_params)
    
    if num_plots > 0:
        fig = plt.figure(figsize=(10, 6 * num_plots))
        gs = fig.add_gridspec(num_plots, 1, hspace=0.6)
        axes = [fig.add_subplot(gs[i]) for i in range(num_plots)]
    
        for i, param in enumerate(selected_original_params):
            param_df = df[df['Parameter'] == param]
            
            # Coletar dados por grupo
            data_by_group = []
            for group in groups:
                group_data = param_df[param_df['Group'] == group]['Value'].values
                data_by_group.append(group_data)
            
            # Executar teste de Kruskal-Wallis
            try:
                h_stat, p_val = kruskal(*data_by_group)
                results.append({
                    "Parâmetro": PARAM_MAPPING[param],
                    "H-Statistic": h_stat,
                    "p-value": p_val,
                    "Significativo (p<0.05)": p_val < 0.05
                })
                
                # Plotar gráfico
                ax = axes[i]
                plot_group_comparison(ax, data_by_group, groups, param)
                
                # Adicionar resultado do teste
                significance = "SIGNIFICATIVO" if p_val < 0.05 else "NÃO SIGNIFICATIVO"
                color = "#00c853" if p_val < 0.05 else "#ff5252"
                
                annotation_text = f"Kruskal-Wallis: H = {h_stat:.2f}, p = {p_val:.4f} ({significance})"
                ax.text(
                    0.5, 0.95, 
                    annotation_text,
                    transform=ax.transAxes,
                    ha='center',
                    va='top',
                    fontsize=11,
                    color=color,
                    bbox=dict(
                        boxstyle="round,pad=0.3",
                        facecolor='#2a2f45',
                        alpha=0.8,
                        edgecolor='none'
                    )
                )
            except Exception as e:
                st.error(f"Erro ao processar {param}: {str(e)}")
                continue
    
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
            .set_properties(**{
                'color': 'white',
                'background-color': '#131625',
            })
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
                    📊 Comparação entre Grupos
                </span>
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    
    # Interpretação
    display_results_interpretation(results)
    
    # Conclusão do estudo
    st.markdown("""
    <div class="card">
        <h2 style="display:flex;align-items:center;gap:10px;">
            <span style="background:linear-gradient(135deg, #a78bfa 0%, #6f42c1 100%);padding:5px 15px;border-radius:30px;font-size:1.2rem;">
                💡 Principais Conclusões do Estudo
            </span>
        </h2>
        <div style="margin-top:15px; padding:20px; background:rgba(26,29,50,0.5); border-radius:12px;">
            <p style="line-height:1.7;">
                1. Todos os vermicompostos apresentaram valores nutricionais significativamente superiores 
                ao solo original, especialmente em Nitrogênio, Fósforo e Potássio.<br><br>
                
                2. O vermicomposto produzido por <i>Octolasion tyrateum</i> (VKO) mostrou os maiores teores 
                de nutrientes entre as espécies testadas.<br><br>
                
                3. A razão C/N foi significativamente reduzida em todos os vermicompostos em comparação 
                com o solo original, indicando maior maturidade e estabilidade do composto.<br><br>
                
                4. O estudo demonstra que a vermicompostagem com espécies locais é uma técnica eficaz 
                para transformar resíduos de cozinha em fertilizante orgânico de alta qualidade.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
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
            SHARMA, D. Kitchen waste management by vermicomposting using locally available epigeic earthworm species. 
            <strong>Journal of Applied and Natural Science</strong>, 
            v. 11, n. 2, p. 372-374, 2019. 
        </p>
        <p style="margin-top:10px;">
            <strong>DOI:</strong> 10.31018/jans.v11i2.2058
        </p>
        <p style="margin-top:15px; font-style:italic;">
            Nota: Os dados utilizados nesta análise são baseados no estudo supracitado. 
            Para mais detalhes metodológicos e resultados completos, consulte o artigo original.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Atualizar o roteador principal
def main():
    if 'selected_article' not in st.session_state:
        st.session_state['selected_article'] = None
    
    # Roteamento
    if st.session_state['selected_article'] is None:
        show_homepage()
    elif st.session_state['selected_article'] == 'dermendzhieva':
        run_dermendzhieva_analysis()
    elif st.session_state['selected_article'] == 'jordao':
        run_jordao_analysis()
    elif st.session_state['selected_article'] == 'sharma':  # Novo caso
        run_sharma_analysis()

# Atualizar a homepage para incluir o novo card
def show_homepage():
    # ... (código existente)
    
    # Adicionar terceiro card para Sharma
    col3 = st.columns(1)[0]  # Criar nova coluna
    
    with col3:
        with st.container():
            st.markdown("""
            <div class="card-container">
                <div class="card">
                    <h2 style="color:#e0e5ff;">Sharma (2019)</h2>
                    <p style="color:#a0a7c0;">Comparação de vermicompostos por espécie de minhoca</p>
                    <ul class="custom-list">
                        <li>Três espécies de minhocas epigeicas</li>
                        <li>Parâmetros: N, P, K, pH, C/N</li>
                        <li>Comparação com solo original</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Selecionar Sharma", key="btn_sharma", 
                         use_container_width=True,
                         type="primary"):
                st.session_state['selected_article'] = 'sharma'
                st.rerun()
