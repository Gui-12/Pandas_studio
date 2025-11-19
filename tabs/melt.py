import streamlit as st
from utils import save_checkpoint

def render(df):
    st.subheader("Transformação: Melt (Unpivot)")
    st.markdown(
        """
        Transforma colunas em linhas. Útil quando você tem colunas como "Jan", "Fev", "Mar" 
        e quer transformar em uma coluna "Mês" e outra "Valor".
        """
    )
    
    # Seleção de variáveis
    all_cols = df.columns.tolist()
    
    id_vars = st.multiselect(
        "Colunas Identificadoras (Que NÃO mudam):", 
        options=all_cols,
        help="Ex: Nome do Produto, Categoria, ID"
    )
    
    # As colunas que sobrarem são candidatas a value_vars
    remaining = [c for c in all_cols if c not in id_vars]
    
    value_vars = st.multiselect(
        "Colunas para 'Derreter' (Que virarão linhas):", 
        options=remaining,
        default=remaining,
        help="Ex: Jan/2023, Fev/2023, Mar/2023"
    )
    
    c1, c2 = st.columns(2)
    var_name = c1.text_input("Nome da Coluna de Variável:", value="Variavel")
    val_name = c2.text_input("Nome da Coluna de Valor:", value="Valor")
    
    if st.button("Executar Melt"):
        if id_vars and value_vars:
            save_checkpoint(df, "Melt / Unpivot")
            try:
                new_df = df.melt(
                    id_vars=id_vars, 
                    value_vars=value_vars, 
                    var_name=var_name, 
                    value_name=val_name
                )
                st.session_state.df = new_df
                st.success(f"Transformação concluída! Agora temos {new_df.shape[0]} linhas.")
                st.rerun()
            except Exception as e:
                st.error(f"Erro no Melt: {e}")
        else:
            st.warning("Selecione as colunas identificadoras e as colunas de valor.")