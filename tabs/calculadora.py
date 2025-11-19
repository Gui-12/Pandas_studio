import streamlit as st
import pandas as pd
from utils import save_checkpoint

def render(df):
    st.subheader("Calculadora")
    nums = df.select_dtypes(include='number').columns
    c1, c2, c3 = st.columns(3)
    a = c1.selectbox("Col A", nums, key="calc_a")
    op = c2.selectbox("Op", ["+", "-", "*", "/"])
    b = c3.selectbox("Col B", nums, key="calc_b")
    res = st.text_input("Nome Resultado", "Calc")
    
    if st.button("Calcular"):
        save_checkpoint(df, "Calc")
        try:
            if op == "+": st.session_state.df[res] = df[a] + df[b]
            elif op == "-": st.session_state.df[res] = df[a] - df[b]
            elif op == "*": st.session_state.df[res] = df[a] * df[b]
            elif op == "/": st.session_state.df[res] = df[a] / df[b].replace(0, pd.NA)
            st.rerun()
        except Exception as e:
            st.error(e)