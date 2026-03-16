import streamlit as st
from supabase import create_client

url = "https://yzupjrzhqmojefurpmrx.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl6dXBqcnpocW1vamVmdXJwbXJ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM0MTY0ODcsImV4cCI6MjA4ODk5MjQ4N30.4qYKmPfDagkicbC31aob3egY2msh7mzuk7ECRJ2-M1A"

supabase = create_client(url, key)

if "equipe" not in st.session_state or st.session_state.equipe is None:
    st.switch_page("app.py")

equipe = st.session_state.equipe
id_equipe = equipe["id"]

st.title("🤖 Mes matchs")

matchs = supabase.table("matchs") \
    .select("*") \
    .execute()

for m in matchs.data:

    if m["equipe1"] == id_equipe or m["equipe2"] == id_equipe:

        statut = "⏳ à jouer"

        if m["termine"]:
            statut = "✅ terminé"

        st.write(
            f"Terrain {m['terrain']} | {m['heure']} | "
            f"{m['equipe1']} vs {m['equipe2']} | {statut}"
        )
