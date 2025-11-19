import streamlit as st

def render(df):
    st.subheader("Visualização da Tabela")
    st.caption("Visualize, ordene e filtre os dados brutos abaixo.")
    
    # Exibe o dataframe com altura fixa e largura total
    st.dataframe(df, use_container_width=True, height=600)