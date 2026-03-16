import streamlit as st
from supabase import create_client

url = "https://yzupjrzhqmojefurpmrx.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl6dXBqcnpocW1vamVmdXJwbXJ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM0MTY0ODcsImV4cCI6MjA4ODk5MjQ4N30.4qYKmPfDagkicbC31aob3egY2msh7mzuk7ECRJ2-M1A"

supabase = create_client(url, key)

st.title("🤖 Tournoi Robot")

if "robot" not in st.session_state:
    st.session_state.robot = None

robot_name = st.text_input("Nom du robot")

if st.button("Connexion"):

    res = supabase.table("robots") \
        .select("*") \
        .eq("nom", robot_name) \
        .execute()

    if res.data:
        st.session_state.robot = res.data[0]
        st.success("Connexion réussie")
        st.switch_page("pages/1_Classement.py")

    else:
        st.error("Robot inconnu")

