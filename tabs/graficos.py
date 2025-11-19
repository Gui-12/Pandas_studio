import streamlit as st

def render(df):
    st.subheader("Gráficos Rápidos")
    t = st.selectbox("Tipo", ["Barras", "Linha", "Scatter"])
    x = st.selectbox("Eixo X", df.columns, key="g_x")
    y = st.multiselect("Eixo Y", df.select_dtypes(include='number').columns, key="g_y")
    
    if y:
        if t == "Barras": st.bar_chart(df, x=x, y=y)
        elif t == "Linha": st.line_chart(df, x=x, y=y)
        elif t == "Scatter": st.scatter_chart(df, x=x, y=y[0])