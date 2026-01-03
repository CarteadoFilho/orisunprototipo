import streamlit as st
import time
from datetime import date
import base64
import mimetypes
from io import BytesIO
import streamlit.components.v1 as components

# --- CONFIGURAÇÃO DA PÁGINA E TEMA ---
st.set_page_config(
    page_title="Orisun - Análise de Fontes",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar catálogo simulado na sessão
if "catalog" not in st.session_state:
    st.session_state["catalog"] = []

# CSS mais robusto (data-testid / seletores genéricos)
st.markdown(
    """
    <style>
    /* Container principal */
    [data-testid="stAppViewContainer"] {
        background-color: #0F0C29;
        color: #F0EBD8;
    }

    /* Sidebar */
    [data-testid="stSidebarNav"] {
        background-color: #1a1638;
    }

    /* Inputs e textareas: tornar legíveis no fundo escuro */
    input, textarea, select {
        color: #FFFFFF !important;
        background-color: rgba(255,255,255,0.03) !important;
    }

    /* Cabeçalhos */
    h1, h2, h3 {
        color: #F0EBD8 !important;
    }

    /* Botões (pequeno refinamento) */
    .stButton>button {
        background-color: rgba(255,255,255,0.04);
        color: #F0EBD8;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Funções utilitárias ----------
def embed_pdf(file_bytes, height=600):
    """Insere um PDF inline usando iframe base64 (pode ser pesado para PDFs grandes)."""
    b64 = base64.b64encode(file_bytes).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="{height}px" type="application/pdf"></iframe>'
    components.html(pdf_display, height=height)

def show_ai_suggestions(uploaded_name=None):
    """Bloco de sugestão da IA (reutilizável)."""
    st.subheader("🤖 Sugestão da IA")
    st.info("Confiança Alta: Título, Data | Confiança Baixa: Autor")
    suggested_title = st.text_input("Título Sugerido", value="Carta de Alforria - Manoel")
    suggested_date = st.date_input("Data Sugerida", value=date(1888, 5, 13))
    summary = st.text_area("Resumo Extraído", value="Documento formal concedendo liberdade a...", height=120)
    col_b1, col_b2 = st.columns(2)
    if col_b1.button("✅ Aprovar e Salvar"):
        # Simula salvar objeto no catálogo
        entry = {
            "Título": suggested_title,
            "Data": suggested_date.isoformat(),
            "Origem": uploaded_name or "Upload IA",
            "Resumo": summary,
            "Fonte": "IA"
        }
        st.session_state["catalog"].append(entry)
        st.success("Salvo no Catálogo!")
    if col_b2.button("❌ Descartar"):
        # Recarrega a página (compatível)
        st.experimental_rerun()

# ---------- BARRA LATERAL / NAVEGAÇÃO ----------
with st.sidebar:
    st.image(
        "https://placeholder.com/wp-content/uploads/2018/10/placeholder.com-logo1.png",
        caption="ORISUN",
        width=150,
    )
    st.markdown("---")
    menu_option = st.radio(
        "Navegação",
        ["Dashboard", "Registro de Fontes", "Análise Inteligente (IA)", "Catálogo", "Configurações"],
        label_visibility="collapsed",
    )

# ---------- PÁGINA: DASHBOARD ----------
if menu_option == "Dashboard":
    st.markdown("### Home > Dashboard")
    st.title("Dashboard")

    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Documentos", str(len(st.session_state["catalog"]) or 124))
    col2.metric("Favoritos", "12")
    col3.metric("Em Análise", "5")
    col4.metric("Pesquisadores", "3")

    st.markdown("---")
    st.subheader("Atividades Recentes")
    st.dataframe(
        [
            {"Título": "Carta de Alforria 1889", "Data": "1889-05-12", "Tipo": "Manuscrito"},
            {"Título": "Foto do Porto de Salvador", "Data": "1920", "Tipo": "Fotografia"},
            {"Título": "Diário de Bordo", "Data": "1750", "Tipo": "Diário Pessoal"},
        ],
        use_container_width=True,
    )

# ---------- PÁGINA: REGISTRO DE FONTES ----------
elif menu_option == "Registro de Fontes":
    st.markdown("### Home > Registro de Fontes")
    st.title("Cadastro Manual de Fonte")

    with st.form("registro_form"):
        st.subheader("1. Identificação Básica")
        c1, c2 = st.columns(2)
        titulo = c1.text_input("Título do Documento *")
        titulo_orig = c2.text_input("Título Original")
        autor = c1.text_input("Criador/Autor")
        local = c2.text_input("Localização de Origem")

        st.subheader("2. Classificação")
        c3, c4, c5 = st.columns(3)
        tipo = c3.selectbox(
            "Tipo de Documento *",
            ["", "Manuscrito", "Impresso", "Carta", "Fotografia", "Mapa", "Livro", "Outros"],
        )
        idioma = c4.text_input("Idioma")
        periodo = c5.selectbox(
            "Período Histórico *",
            ["", "Pré-história", "Antiguidade", "Medieval", "Moderno", "Contemporâneo"],
        )

        st.subheader("3. Datação")
        c6, c7 = st.columns(2)
        data_precisa = c6.date_input("Data do Documento (Precisa)", value=date.today())
        data_approx = c7.text_input("Data Aproximada (Ex: 'c. 1800', 'Século XIX')")

        st.subheader("4. Preservação")
        c8, c9, c10 = st.columns(3)
        repositorio = c8.text_input("Repositório")
        estado = c9.selectbox("Estado de Preservação", ["", "Excelente", "Bom", "Regular", "Ruim", "Crítico"])
        autenticidade = c10.selectbox("Status Autenticidade", ["", "Em análise", "Autêntico", "Incerto"])

        st.subheader("5. Descrição e Conteúdo")
        descricao = st.text_area("Descrição Geral *", height=100)
        resumo = st.text_area("Resumo do Conteúdo")
        tags = st.text_input("Tags (separadas por vírgula)")

        st.subheader("6. Arquivos")
        arquivos = st.file_uploader("Upload de Imagens/PDFs", accept_multiple_files=True)

        submitted = st.form_submit_button("Salvar Documento")
        if submitted:
            # Validação simples
            errors = []
            if not titulo or titulo.strip() == "":
                errors.append("O campo 'Título do Documento' é obrigatório.")
            if not tipo or tipo == "":
                errors.append("O campo 'Tipo de Documento' é obrigatório.")
            if not descricao or descricao.strip() == "":
                errors.append("O campo 'Descrição Geral' é obrigatório.")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                # Simular salvamento: adicionar ao catálogo em sessão
                entry = {
                    "Título": titulo,
                    "Título Original": titulo_orig,
                    "Autor": autor,
                    "Local": local,
                    "Tipo": tipo,
                    "Idioma": idioma,
                    "Periodo": periodo,
                    "Data Precisa": data_precisa.isoformat() if isinstance(data_precisa, date) else str(data_precisa),
                    "Data Aproximada": data_approx,
                    "Repositório": repositorio,
                    "Estado": estado,
                    "Autenticidade": autenticidade,
                    "Descrição": descricao,
                    "Resumo": resumo,
                    "Tags": [t.strip() for t in tags.split(",")] if tags else [],
                    "Arquivos": [f.name for f in arquivos] if arquivos else [],
                }
                st.session_state["catalog"].append(entry)
                st.success("Documento salvo com sucesso (Simulação)!")

                # Mostrar links/baixar arquivos enviados (se houver)
                if arquivos:
                    st.markdown("### Arquivos enviados")
                    for f in arquivos:
                        st.write(f"- {f.name} ({f.type or 'desconhecido'})")
                        st.download_button("Baixar " + f.name, data=f.getvalue(), file_name=f.name)

# ---------- PÁGINA: ANÁLISE INTELIGENTE (IA) ----------
elif menu_option == "Análise Inteligente (IA)":
    st.markdown("### Home > Análise Inteligente")
    st.title("Orisun AI Analyst")

    uploaded_file = st.file_uploader("Arraste sua fonte aqui (JPG, PNG, PDF)", type=["png", "jpg", "jpeg", "pdf"])

    if uploaded_file is not None:
        with st.spinner("A Orisun está analisando a fonte e extraindo metadados..."):
            time.sleep(1.5)  # Simulação leve

        st.success("Análise concluída!")
        st.markdown("---")

        file_bytes = uploaded_file.getvalue()
        mime_type = uploaded_file.type or mimetypes.guess_type(uploaded_file.name)[0] or "application/octet-stream"

        show_image = st.checkbox("Mostrar Imagem/Preview", value=True)

        # Lógica de exibição: imagens vs pdfs
        if mime_type.startswith("image") and show_image:
            col_img, col_form = st.columns([1, 2])
            with col_img:
                st.image(file_bytes, caption=f"Preview: {uploaded_file.name}", use_container_width=True)
            with col_form:
                show_ai_suggestions(uploaded_name=uploaded_file.name)

        elif mime_type == "application/pdf":
            # Oferecer embed (pode falhar para arquivos muito grandes) e download
            if show_image:
                try:
                    embed_pdf(file_bytes, height=600)
                except Exception:
                    st.warning("Não foi possível renderizar o PDF inline. Use o botão de download.")
            st.download_button("Baixar PDF", data=file_bytes, file_name=uploaded_file.name)
            show_ai_suggestions(uploaded_name=uploaded_file.name)

        else:
            # Caso arquivo não seja imagem nem pdf, exibir sugestões sem preview
            st.warning("Preview não disponível para este tipo de arquivo.")
            show_ai_suggestions(uploaded_name=uploaded_file.name)

# ---------- PÁGINA: CATÁLOGO ----------
elif menu_option == "Catálogo":
    st.markdown("### Home > Catálogo")
    c_head1, c_head2 = st.columns([3, 1])
    c_head1.title("Catálogo de Fontes")
    if c_head2.button("Registrar Nova Fonte"):
        # alterna para o formulário de registro
        st.experimental_set_query_params(page="registro")
        st.success("Use o menu 'Registro de Fontes' para cadastrar uma nova entrada.")

    view_mode = st.radio("Visualização:", ["Grade", "Lista"], horizontal=True)

    if not st.session_state["catalog"]:
        st.info("Nenhum documento salvo ainda. Registre um documento ou faça upload via Análise Inteligente (IA).")

    if view_mode == "Grade":
        st.write("Exibindo em Grade...")
        cols = st.columns(3)
        for idx, entry in enumerate(st.session_state["catalog"]):
            with cols[idx % 3]:
                title = entry.get("Título") or f"Documento {idx+1}"
                st.info(f"**{title}**")
                st.caption(entry.get("Data") or entry.get("Data Precisa") or entry.get("Data Aproximada", ""))
                st.write(entry.get("Resumo", "")[:120] + ("..." if entry.get("Resumo") and len(entry.get("Resumo")) > 120 else ""))
    else:
        st.write("Exibindo em Lista...")
        # Montar uma tabela simples
        if st.session_state["catalog"]:
            rows = []
            for i, e in enumerate(st.session_state["catalog"], start=1):
                rows.append(
                    {
                        "ID": i,
                        "Título": e.get("Título"),
                        "Data": e.get("Data") or e.get("Data Precisa") or e.get("Data Aproximada"),
                        "Origem": e.get("Fonte", e.get("Origem", "")),
                    }
                )
            st.table(rows)
        else:
            st.write("Sem entradas para listar.")

# ---------- PÁGINA: CONFIGURAÇÕES ----------
elif menu_option == "Configurações":
    st.markdown("### Home > Configurações")
    st.title("Configurações")
    st.info("Configurações de conta e preferências (simulação).")
    if st.button("Limpar Catálogo (Simulação)"):
        st.session_state["catalog"] = []
        st.success("Catálogo limpo (simulação).")
