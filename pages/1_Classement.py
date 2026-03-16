import streamlit as st
import pandas as pd
from utils.supabase_client import supabase

if "robot" not in st.session_state:
    st.warning("Veuillez vous connecter.")
    st.switch_page("app.py")

robot = st.session_state.robot

st.title("Classement")

robots = supabase.table("robots") \
    .select("*") \
    .eq("poule_id", robot["poule_id"]) \
    .execute()

df = pd.DataFrame(robots.data)

st.dataframe(df)
