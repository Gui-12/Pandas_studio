import streamlit as st
import pandas as pd
import re
from utils import save_checkpoint

def render(df):
    st.subheader("Manipulação de Texto")
    t1, t2, t3 = st.tabs(["Split", "Extrair Números", "Combinar"])
    
    with t1:
        col = st.selectbox("Coluna", df.select_dtypes(include='object').columns, key="split_c")
        sep = st.text_input("Separador", " ")
        if st.button("Dividir"):
            save_checkpoint(df, "Split")
            sp = df[col].str.split(sep, expand=True)
            sp.columns = [f"{col}_{i+1}" for i in range(sp.shape[1])]
            st.session_state.df = pd.concat([df, sp], axis=1)
            st.rerun()
            
    with t2:
        col = st.selectbox("Coluna", df.columns, key="ext_c")
        if st.button("Extrair Números"):
            save_checkpoint(df, "Extract Num")
            st.session_state.df[col] = df[col].astype(str).apply(lambda x: re.sub(r'[^0-9.]', '', x))
            st.rerun()
            
    with t3:
        c1, c2 = st.columns(2)
        a = c1.selectbox("Col A", df.columns, key="c_a")
        b = c2.selectbox("Col B", df.columns, key="c_b")
        sep = st.text_input("Separador", "-")
        name = st.text_input("Nome Nova Coluna", "Combinado")
        if st.button("Combinar"):
            save_checkpoint(df, "Combine")
            st.session_state.df[name] = df[a].astype(str) + sep + df[b].astype(str)
            st.rerun()