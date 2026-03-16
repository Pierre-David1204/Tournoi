import streamlit as st
from utils.supabase_client import supabase

st.set_page_config(page_title="Tournoi Robot", layout="wide")

st.title("🤖 Tournoi Robot")

robot_name = st.text_input("Nom du robot")

if st.button("Connexion"):

    res = supabase.table("robots") \
        .select("*") \
        .eq("nom", robot_name) \
        .execute()

    if len(res.data) == 1:
        st.session_state.robot = res.data[0]
        st.success("Connexion réussie")
        st.switch_page("pages/1_Classement.py")

    else:
        st.error("Robot inconnu")