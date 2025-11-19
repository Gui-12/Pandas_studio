import streamlit as st
import pandas as pd
import io
import utils
import os
import time

# Importando os módulos da pasta tabs
from tabs import (
    perfil, visualizacao, calculadora, graficos, 
    limpeza, colunas, texto, agrupamento, melt
)

# --- Configuração ---
st.set_page_config(page_title="Pandas Studio Modular", page_icon="🐼", layout="wide")
utils.init_session()

# --- Sidebar (Carregamento) ---
with st.sidebar:
    st.title("🐼 Studio Modular")
    
    uploaded_file = st.file_uploader(
        "Carregar Arquivo", 
        type=['xlsx', 'xls', 'csv'],
        on_change=utils.reset_session,
        key="uploader"
    )
    
    if uploaded_file:
        if st.session_state.df is None:
            df_new = utils.load_file_robust(uploaded_file)
            if df_new is not None:
                st.session_state.df = df_new
                st.success(f"Carregado: {uploaded_file.name}")
                st.rerun()

    st.divider()
    # Botões de Controle
    c1, c2 = st.columns(2)
    with c1:
        if st.button("↩️ Undo"):
            utils.undo_last_action()
    with c2:
        if st.button("🗑️ Limpar"):
            utils.reset_session()
            st.rerun()
            
    # Exportação
    if st.session_state.df is not None:
        st.divider()
        st.header("Exportar")
        buffer = io.BytesIO()
        ftype = st.radio("Formato", ["Excel", "CSV"])
        fname = st.text_input("Nome:", "dados_processados")
        if st.button("Baixar"):
            if ftype == "Excel":
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    st.session_state.df.to_excel(writer, index=False)
                data, mime, ext = buffer.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "xlsx"
            else:
                data, mime, ext = st.session_state.df.to_csv(index=False).encode('utf-8'), "text/csv", "csv"
            st.download_button(label="⬇️ Download", data=data, file_name=f"{fname}.{ext}", mime=mime)

    # --- Botão de Sair (NOVO) ---
    st.markdown("---") 
    if st.button("❌ Sair do App"):
        st.warning("Encerrando aplicação... Pode fechar esta aba do navegador.")
        time.sleep(2) # Dá um tempo para o usuário ler a mensagem
        os._exit(0)   # Mata o processo do Python/Streamlit

# --- Área Principal ---
if st.session_state.df is not None:
    df = st.session_state.df
    
    # Métricas Globais
    m1, m2, m3 = st.columns(3)
    m1.metric("Linhas", df.shape[0])
    m2.metric("Colunas", df.shape[1])
    m3.metric("Nulos", df.isna().sum().sum())

    # Definição das Abas
    tab_names = [
        "🧐 Perfil", "👁️ Visualização", "🧹 Limpeza", "🔡 Texto", 
        "🔧 Colunas", "➕ Calculadora", "📊 Gráficos", 
        "📈 Agrupamento", "🔄 Melt"
    ]
    tabs = st.tabs(tab_names)

    # Renderização de cada módulo
    with tabs[0]: perfil.render(df)
    with tabs[1]: visualizacao.render(df)
    with tabs[2]: limpeza.render(df)
    with tabs[3]: texto.render(df)
    with tabs[4]: colunas.render(df)
    with tabs[5]: calculadora.render(df)
    with tabs[6]: graficos.render(df)
    with tabs[7]: agrupamento.render(df)
    with tabs[8]: melt.render(df)

else:
    st.info("Por favor, carregue um arquivo na barra lateral.")