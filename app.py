# Explicação detalhada sobre a produção das amostras (VERSÃO CORRIGIDA)
st.markdown("""
<div class="info-card">
    <div style="display:flex; align-items:center; margin-bottom:15px;">
        <span class="info-icon">ℹ️</span>
        <h3 style="color:#00c1e0; margin:0;">Como as amostras foram produzidas</h3>
    </div>
    <div style="color:#d7dce8; line-height:1.7;">
        <p>As amostras foram geradas por simulação computacional seguindo um protocolo rigoroso:</p>
    </div>
""", unsafe_allow_html=True)

# Lista formatada
st.markdown("""
<ol class="custom-list">
    <li><strong>Base em dados científicos</strong>: Valores médios e desvios padrão foram extraídos do estudo de referência</li>
    <li><strong>Estratégia de réplicas</strong>: Para cada combinação de parâmetro/dia, foram geradas 3 réplicas independentes</li>
    <li><strong>Modelagem estatística</strong>: Cada valor foi simulado usando distribuição normal: 
        <br><code>valor = normal(média, desvio_padrão)</code></li>
    <li><strong>Controle de qualidade</strong>: Valores foram ajustados para evitar resultados não-físicos:
        <ul>
            <li>pH limitado ao intervalo [0, 14]</li>
            <li>Concentrações e relações mantidas como valores positivos</li>
        </ul>
    </li>
    <li><strong>Estrutura de dados</strong>: Cada linha representa uma réplica experimental contendo:
        <ul>
            <li>Parâmetro analisado</li>
            <li>Substrato (VC-M = Vermicomposto com Materiais Mistos)</li>
            <li>Medições nos dias 1, 30, 60, 90 e 120</li>
        </ul>
    </li>
</ol>
""", unsafe_allow_html=True)

# Texto final
st.markdown("""
<div style="color:#d7dce8; line-height:1.7; margin-top:-15px;">
    <p style="margin-top:15px; font-style:italic;">
        Esta abordagem permite explorar a variabilidade experimental esperada em estudos reais de vermicompostagem.
    </p>
</div>
</div>  <!-- Fecha a div do info-card -->
""", unsafe_allow_html=True)
