import streamlit as st
import tempfile
import os
from src.jogo import JogoAventura
from src.pdf_generator import gerar_pdf
from dotenv import load_dotenv

load_dotenv()

def carregar_estilo():
    st.markdown("""
    <link href='https://fonts.googleapis.com/css?family=MedievalSharp' rel='stylesheet'>
    """, unsafe_allow_html=True)
    
    try:
        with open("assets/medieval.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Estilos extras não carregados: {str(e)}")

def exibir_header(mundo):
    st.markdown(f"""
    <div class="header-container">
        <div class="header-banner">
            <div class="header-content">
                <h1 class="title">📜 {mundo}</h1>
                <div class="header-description">
                    <p>Um grimório interativo onde suas escolhas moldam o destino do reino.</p>
                    <div class="header-features">
                        <span>⚔️ Geração procedural de histórias</span>
                        <span>🧙 Sistema de ações estratégicas</span>
                        <span>🏰 Mundo dinâmico</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def exibir_footer(personagem):
    st.markdown(f"""
    <div class="footer-container">
        <div class="footer-content">
            <div class="footer-section centered">
                <h4>📜 Sobre o Projeto</h4>
                <p>Escriba Real v1.3<br>Código: LICENÇA DE DESENVOLVEDOR EXCLUSIVA (LDE)<br>Feito com ❤️ por Alan José</p>
            </div>
        </div>
        <div class="footer-credits">
            <p>© 2025 Alan José - Todos os direitos reservados</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Cronicas do Escriba Real",
        layout="wide",
        page_icon="📜"
    )
    carregar_estilo()

    if 'jogo' not in st.session_state:
        st.session_state.jogo = None

    if not st.session_state.jogo:
        exibir_tela_inicial()
    else:
        exibir_jogo()
        exibir_footer(st.session_state.jogo.personagem['nome'])

def exibir_tela_inicial():
    with st.container():
        exibir_header("Crônicas do Escriba Real")
        
        with st.form("config_inicial"):
            st.markdown("## 🧙 Forja do Destino")
            
            col1, col2 = st.columns(2)
            with col1:
                personagem_nome = st.text_input("Nome do Herói:", value="Lancelot")
                personagem_classe = st.selectbox(
                    "Classe:",
                    [
    "Cavaleiro", "Mago", "Arqueiro", "Clérigo", "Ladino", "Bárbaro", "Paladino", "Feiticeiro", "Druida", "Guerreiro", 
    "Monge", "Espadachim Arcano", "Guardião Sagrado", "Bardo Sombrio", "Atirador Arcano", "Xamã da Tempestade", 
    "Caçador de Sombras", "Guerreiro Sangrento", "Monge Celestial", "Mestre do Fogo", "Guardião da Terra", "Senhor das Águas", 
    "Tempestade Viva", "Invocador de Gelo", "Chamado do Vento", "Avatar do Caos", "Necromante", "Ceifador Sombrio", 
    "Bruxo do Abismo", "Cavaleiro da Morte", "Vampiro Arcano", "Mestre das Marionetes", "Profeta do Vazio", "Mercador de Almas", 
    "Cruzado Sagrado", "Arauto dos Deuses", "Paladino Radiante", "Sacerdote do Sol", "Guardião Celestial", "Exorcista", 
    "Santo Guerreiro", "Ascendido", "Xamã", "Druida Metamorfo", "Guardião das Feras", "Caçador Selvagem", "Andarilho da Floresta", 
    "Mestre das Vinhas", "Filho da Lua", "Senhor das Feras", "Engenheiro de Guerra", "Artífice Arcano", "Pistoleiro Mágico", 
    "Mecânico de Golems", "Senhor das Máquinas", "Inventor do Caos", "Tecnomante", "Cavaleiro de Aço", "Guardião do Tempo", 
    "Manipulador Dimensional", "Oráculo do Destino", "Andarilho do Vazio", "Tecelão da Realidade", "Senhor do Fluxo Temporal", 
    "Guerreiro Estelar", "Viajante Interplanar", "Ilusionista", "Encantador de Sonhos", "Mestre do Karma", "Domador de Espíritos", 
    "Visionário Astral", "Arquiteto das Fábulas", "Canalizador do Caos", "Equilibrador Cósmico"
]

                )
                
            with col2:
                personagem_habilidade = st.text_input(
                    "Habilidade:",
                    value="Clarividência",
                    help="Habilidade única do personagem"
                )
                mundo_principal = st.text_input(
                    "Reino:",
                    value="Terras de Eldoria"
                )

            enredo = st.text_area(
                "Profecia Ancestral:",
                height=150,
                value="A lenda fala de um herói destinado derrotar os Deuses externos e salvar o mundo",
                help="Escreva o prólogo da aventura"
            )

            if st.form_submit_button("⚔️ Iniciar Epopeia"):
                st.session_state.jogo = JogoAventura(
                    enredo=enredo,
                    personagem={
                        'nome': personagem_nome,
                        'classe': personagem_classe,
                        'habilidade': personagem_habilidade
                    },
                    mundo=mundo_principal
                )
                st.rerun()

def exibir_jogo():
    jogo = st.session_state.jogo
    exibir_header(jogo.mundo)
    
    with st.container():
        with st.container():
            st.markdown(f"### 🌠 Jornada de **{jogo.personagem['nome']}**")
            
            for idx, cena in enumerate(jogo.historico):
                with st.expander(f"📜 Capítulo {idx+1}: {cena['titulo']}", expanded=(idx==len(jogo.historico)-1)):
                    st.markdown(
                        f'<div class="descricao-cena">{cena["descricao"]}</div>', 
                        unsafe_allow_html=True
                    )
                    
                    if cena.get('acao_escolhida'):
                        st.markdown(
                            f'<div class="escolha-feita">🛡 Escolha do Destino: {cena["acao_escolhida"]}</div>',
                            unsafe_allow_html=True
                        )

        if jogo.historico:
            ultima_cena = jogo.historico[-1]
            st.markdown("## 🧭 Encruzilhada do Destino")
            cols = st.columns(3)
            for i, (col, acao) in enumerate(zip(cols, ultima_cena['acoes'])):
                with col:
                    with st.container(border=True):
                        st.markdown(f"<div style='font-size:1.5rem; margin-bottom:10px;'>{acao['tipo'].icon()}</div>", unsafe_allow_html=True)
                        st.markdown(f"**{acao['texto']}**")
                        st.caption(acao.get('dica', ''))
                        if st.button("Escolher", key=f"acao_{i}"):
                            ultima_cena['acao_escolhida'] = acao['texto']
                            jogo.processar_acao(acao)
                            st.rerun()

    with st.sidebar:
        with st.container(border=True):
            st.markdown("### 🛡️ Arquivos do Escriba")
            st.markdown(f"**Herói:** {jogo.personagem['nome']}")
            st.markdown(f"**Classe:** {jogo.personagem['classe']}")
            st.markdown(f"**Habilidade:** {jogo.personagem['habilidade']}")
            st.markdown(f"**Reino:** {jogo.mundo}")
            
            if st.button("🌀 Revelação dos Deuses", help="Invoque uma reviravolta épica!"):
                jogo.adicionar_plot_twist()
                st.rerun()

            if st.button("📜 Gerar PDF"):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                    gerar_pdf(jogo.para_json(), tmpfile.name)
                    with open(tmpfile.name, "rb") as f:
                        st.download_button(
                            label="⬇️ Baixar Crônica",
                            data=f.read(),
                            file_name="cronicas_medievais.pdf",
                            mime="application/pdf"
                        )

        with st.container(border=True):
            st.markdown("### ⚔️ Apoie o Desenvolvedor")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(
                    "https://github.com/Mogutaa/Cronicas-do-escriba-real/blob/main/pix.png?raw=true",
                    width=120,
                    caption="QR Code PIX"
                )
            
            with col2:
                st.markdown("**Chave PIX:**")
                pix_key = "00020126360014br.gov.bcb.pix0114+5581987499210520400005303986540510.005802BR5910ALAN FILHO6009SAO PAULO62580520SAN2025032420195159250300017br.gov.bcb.brcode01051.0.063041F7E"
                st.code(pix_key, language="text")
                
                if st.button("📋 Copiar Chave", key="copy_pix"):
                    st.markdown(
                        f"""
                        <script>
                            navigator.clipboard.writeText("{pix_key}");
                        </script>
                        """,
                        unsafe_allow_html=True
                    )
            
            st.divider()
            
            st.markdown("**🔗 Conecte-se:**")
            st.markdown("""
                <style>
                    .contact-links a { 
                        color: #d4af37 !important;
                        text-decoration: none !important;
                    }
                </style>
                <div class="contact-links">
                    📌 <a href="https://www.linkedin.com/in/alan-jose-filho/" target="_blank">LinkedIn</a><br>
                    💻 <a href="https://github.com/Mogutaa" target="_blank">GitHub</a>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()