import streamlit as st
import pandas as pd

def init_session():
    """Inicializa as variáveis de sessão se não existirem."""
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'history' not in st.session_state:
        st.session_state.history = []

def save_checkpoint(df, action_name):
    """Salva o estado atual no histórico."""
    st.session_state.history.append({"df": df.copy(), "action": action_name})
    # Mantém apenas os últimos 10 passos
    if len(st.session_state.history) > 10:
        st.session_state.history.pop(0)

def undo_last_action():
    """Reverte para o estado anterior."""
    if st.session_state.history:
        last_state = st.session_state.history.pop()
        st.session_state.df = last_state["df"]
        st.success(f"Desfeito: {last_state['action']}")
        st.rerun()
    else:
        st.warning("Nada para desfazer.")

def reset_session():
    """Callback para limpar dados ao trocar de arquivo."""
    st.session_state.df = None
    st.session_state.history = []

def load_file_robust(uploaded_file):
    """Tenta carregar CSV/Excel com tratamento de erros."""
    try:
        if uploaded_file.name.endswith('.csv'):
            try:
                uploaded_file.seek(0)
                return pd.read_csv(uploaded_file)
            except:
                try:
                    uploaded_file.seek(0)
                    return pd.read_csv(uploaded_file, sep=';')
                except:
                    uploaded_file.seek(0)
                    st.warning("⚠️ CSV irregular. Forçando leitura...")
                    return pd.read_csv(uploaded_file, sep=None, engine='python', on_bad_lines='skip')
        else:
            return pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Erro fatal: {e}")
        return None