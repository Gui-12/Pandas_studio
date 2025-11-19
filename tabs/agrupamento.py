import streamlit as st
from utils import save_checkpoint

def render(df):
    st.subheader("Agrupamento (Group By)")
    st.warning("⚠️ Atenção: Esta operação agrupa os dados e reduz o número de linhas.")
    
    c1, c2, c3 = st.columns(3)
    
    # Inputs
    gb_cols = c1.multiselect("Agrupar por (Dimensões):", df.columns)
    
    # Filtra apenas colunas numéricas para o cálculo, mas permite todas se quiser
    calc_col = c2.selectbox("Coluna para Calcular (Métrica):", df.columns)
    
    func = c3.selectbox("Operação:", ["sum", "mean", "count", "min", "max", "nunique", "first", "last"])
    
    if st.button("Aplicar Agrupamento"):
        if gb_cols and calc_col:
            save_checkpoint(df, f"GroupBy {gb_cols} ({func})")
            try:
                # Realiza o GroupBy e reseta o index para virar tabela plana novamente
                new_df = df.groupby(gb_cols)[calc_col].agg(func).reset_index()
                
                # Renomeia a coluna de cálculo para ficar claro (ex: Valor -> Valor_sum)
                new_df = new_df.rename(columns={calc_col: f"{calc_col}_{func}"})
                
                st.session_state.df = new_df
                st.success("Agrupamento realizado com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao agrupar: {e}. Verifique se a coluna de cálculo suporta a operação '{func}'.")
        else:
            st.warning("Selecione pelo menos uma coluna para agrupar e uma para calcular.")