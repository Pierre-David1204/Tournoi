import streamlit as st
from supabase import create_client

if "SUPABASE_URL" not in st.secrets:
    st.error("SUPABASE_URL manquant dans les secrets")
    st.stop()

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)
