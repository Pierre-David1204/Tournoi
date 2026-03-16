import streamlit as st
from supabase import create_client

url = "https://yzupjrzhqmojefurpmrx.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl6dXBqcnpocW1vamVmdXJwbXJ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM0MTY0ODcsImV4cCI6MjA4ODk5MjQ4N30.4qYKmPfDagkicbC31aob3egY2msh7mzuk7ECRJ2-M1A"

supabase = create_client(url, key)

if "robot" not in st.session_state or st.session_state.robot is None:
    st.warning("Veuillez vous connecter")
    st.switch_page("app.py")

robot = st.session_state.robot
poule_id = robot["poule_id"]

st.title("⚔️ Rencontres")

matchs = supabase.table("matchs") \
    .select("*") \
    .eq("poule_id", poule_id) \
    .execute()

for m in matchs.data:

    st.write(
        f"{m['robot1']} vs {m['robot2']} | terminé : {m['termine']}"
    )
