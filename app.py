import streamlit as st
from utils.supabase_client import supabase

st.title("Test Supabase")

data = supabase.table("robots").select("*").execute()

st.write(data.data)
