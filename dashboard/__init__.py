import streamlit as st
from .app_state import AppState

if 'app_state' not in st.session_state:
    st.session_state.app_state = AppState()

app_state: AppState = st.session_state.app_state

__all__ = ['app_state']
