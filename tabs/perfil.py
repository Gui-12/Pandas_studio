import streamlit as st

def render(df):
    st.subheader("Data Profiling")
    c1, c2 = st.columns([2, 1])
    with c1:
        st.write("##### Nulos")
        st.bar_chart(df.isnull().sum())
        st.write("##### Estatísticas")
        st.dataframe(df.describe(), use_container_width=True)
    with c2:
        st.write("##### Top Valores")
        col = st.selectbox("Coluna:", df.columns, key="prof_c")
        st.dataframe(df[col].value_counts().head(20), use_container_width=True)