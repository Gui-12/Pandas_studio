import streamlit as st
from utils import save_checkpoint

def render(df):
    st.subheader("Gerenciar Colunas")
    
    col1, col2 = st.columns(2)
    
    # --- Seleção/Exclusão ---
    with col1:
        st.markdown("##### Selecionar/Excluir")
        # O multiselect já vem preenchido com todas as colunas atuais
        cols_to_keep = st.multiselect(
            "Selecione as colunas para MANTER:", 
            options=df.columns, 
            default=df.columns
        )
        
        if st.button("Atualizar Colunas"):
            # Verifica se o usuário tirou alguma coluna
            if len(cols_to_keep) < len(df.columns):
                save_checkpoint(df, "Filtrar Colunas")
                st.session_state.df = df[cols_to_keep]
                st.rerun()
            else:
                st.info("Nenhuma coluna foi removida.")

    # --- Renomear ---
    with col2:
        st.markdown("##### Renomear")
        col_target = st.selectbox("Escolha a coluna:", df.columns, key="ren_col_select")
        new_name = st.text_input("Novo nome:", key="ren_new_name")
        
        if st.button("Aplicar Nome"):
            if new_name and new_name != col_target:
                save_checkpoint(df, f"Renomear {col_target} -> {new_name}")
                st.session_state.df = df.rename(columns={col_target: new_name})
                st.rerun()
            elif new_name == col_target:
                st.warning("O novo nome é igual ao atual.")
            else:
                st.warning("Digite um nome válido.")