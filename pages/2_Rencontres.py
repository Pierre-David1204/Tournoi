import streamlit as st
from utils.supabase_client import supabase

st.title("⚔️ Rencontres")

robot = st.session_state.robot
poule_id = robot["poule_id"]

matchs = supabase.table("matchs") \
    .select("*, robots!robot1(nom), robots!robot2(nom)") \
    .eq("poule_id", poule_id) \
    .execute()

for m in matchs.data:

    r1 = m["robots"]["nom"]
    r2 = m["robots_1"]["nom"]

    if m["termine"]:
        st.write(f"✅ {r1} vs {r2}")
    else:
        st.write(f"⏳ {r1} vs {r2}")