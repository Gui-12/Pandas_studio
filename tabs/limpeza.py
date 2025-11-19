import streamlit as st
import pandas as pd
from utils import save_checkpoint

def render(df):
    st.subheader("Limpeza Avançada")
    t1, t2, t3 = st.tabs(["Datas & Básico", "Exclusão Condicional", "Exclusão por ID"])
    
    # --- Datas & Básico ---
    with t1:
        st.markdown("### 🗓️ Conversor Inteligente de Datas")
        col_date = st.selectbox("Coluna de Data:", df.columns, key="date_col_smart")
        
        # Inputs
        input_formats = {
            "Automático": "auto",
            "202501 (Numérico)": "%Y%m",
            "jan/2025 (Texto PT-BR)": "%b/%Y",
            "jan-25 (Texto Curto)": "%b-%y",
            "01/01/2025": "%d/%m/%Y",
            "2025-01-01": "%Y-%m-%d",
            "Customizado": "custom"
        }
        input_mode = st.selectbox("1. Como a data ESTÁ?", list(input_formats.keys()))
        fmt_in = input_formats[input_mode]
        if fmt_in == "custom":
            fmt_in = st.text_input("Formato entrada:", key="fmt_in_custom")

        # Outputs
        output_formats = {
            "Objeto Data (Recomendado)": "datetime",
            "Texto: 01/01/2025": "%d/%m/%Y",
            "Texto: 2025-01-01": "%Y-%m-%d"
        }
        output_mode = st.selectbox("2. Saída desejada?", list(output_formats.keys()))
        fmt_out = output_formats[output_mode]

        if st.button("🔄 Converter"):
            save_checkpoint(df, f"Date: {col_date}")
            try:
                # Tratamento PT-BR
                if "jan" in str(df[col_date].iloc[0]).lower():
                    map_months = {'jan': 'Jan', 'fev': 'Feb', 'mar': 'Mar', 'abr': 'Apr', 'mai': 'May', 'jun': 'Jun', 'jul': 'Jul', 'ago': 'Aug', 'set': 'Sep', 'out': 'Oct', 'nov': 'Nov', 'dez': 'Dec'}
                    for pt, en in map_months.items():
                        st.session_state.df[col_date] = st.session_state.df[col_date].astype(str).str.lower().str.replace(pt, en, regex=False)
                    st.session_state.df[col_date] = st.session_state.df[col_date].str.title()

                if fmt_in == "auto":
                    temp = pd.to_datetime(df[col_date], errors='coerce')
                else:
                    temp = pd.to_datetime(df[col_date].astype(str), format=fmt_in, errors='coerce')

                if fmt_out == "datetime":
                    st.session_state.df[col_date] = temp
                else:
                    st.session_state.df[col_date] = temp.dt.strftime(fmt_out)
                
                st.success("Convertido!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro: {e}")

        st.divider()
        c1, c2 = st.columns(2)
        if c1.button("Remover Duplicatas"):
            save_checkpoint(df, "Deduplicate")
            st.session_state.df = df.drop_duplicates()
            st.rerun()
        if c2.button("Remover Nulos"):
            save_checkpoint(df, "DropNA")
            st.session_state.df = df.dropna()
            st.rerun()

    # --- Condicional ---
    with t2:
        rc1, rc2, rc3 = st.columns(3)
        target = rc1.selectbox("Coluna", df.columns, key="cond_tg")
        op = rc2.selectbox("Condição", ["Igual a", "Maior que", "Menor que", "Contém"], key="cond_op")
        val = rc3.text_input("Valor", key="cond_val")
        
        if st.button("Excluir Linhas"):
            save_checkpoint(df, "Filter Cond")
            try:
                mask = None
                if op == "Maior que": mask = df[target] > float(val)
                elif op == "Menor que": mask = df[target] < float(val)
                elif op == "Igual a": mask = df[target].astype(str) == val
                elif op == "Contém": mask = df[target].astype(str).str.contains(val, na=False, case=False)
                
                if mask is not None:
                    st.session_state.df = df[~mask]
                    st.rerun()
            except Exception as e:
                st.error(f"Erro: {e}")

    # --- IDs ---
    with t3:
        ids = st.text_area("IDs (separados por vírgula)")
        if st.button("Remover IDs"):
            save_checkpoint(df, "Remove IDs")
            id_list = [x.strip() for x in ids.split(',')]
            if pd.api.types.is_integer_dtype(df.index):
                id_list = [int(x) for x in id_list if x.isdigit()]
            st.session_state.df = df.drop([i for i in id_list if i in df.index])
            st.rerun()