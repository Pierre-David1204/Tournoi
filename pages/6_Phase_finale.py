import streamlit as st
import pandas as pd
from supabase import create_client

url = "https://yzupjrzhqmojefurpmrx.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl6dXBqcnpocW1vamVmdXJwbXJ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM0MTY0ODcsImV4cCI6MjA4ODk5MjQ4N30.4qYKmPfDagkicbC31aob3egY2msh7mzuk7ECRJ2-M1A"

supabase = create_client(url, key)

st.title("🏆 Phase finale")

# récupérer équipes
equipes_data = supabase.table("equipes").select("*").execute()
equipes = {e["id"]: e["nom"] for e in equipes_data.data}

# récupérer matchs
data = supabase.table("phase_finale").select("*").execute()

if not data.data:
    st.info("La phase finale n'est pas encore générée.")
    st.stop()

df = pd.DataFrame(data.data)

# vérifier colonnes
required_cols = ["equipe1", "equipe2"]
for col in required_cols:
    if col not in df.columns:
        st.error(f"Colonne manquante dans la table : {col}")
        st.stop()

df["Equipe1"] = df["equipe1"].map(equipes)
df["Equipe2"] = df["equipe2"].map(equipes)

for tour, matchs in df.groupby("tour"):

    st.header(tour)

    for _, m in matchs.iterrows():

        score = ""

        if m["termine"]:
            score = f"{m['score1']} - {m['score2']}"

        st.write(
            f"{m['Equipe1']} vs {m['Equipe2']} {score}"
        )
