import streamlit as st
import pandas as pd
from supabase import create_client

url = "https://yzupjrzhqmojefurpmrx.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl6dXBqcnpocW1vamVmdXJwbXJ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM0MTY0ODcsImV4cCI6MjA4ODk5MjQ4N30.4qYKmPfDagkicbC31aob3egY2msh7mzuk7ECRJ2-M1A"

supabase = create_client(url, key)

if "equipe" not in st.session_state or st.session_state.equipe is None:
    st.switch_page("app.py")

equipe = st.session_state.equipe
id_equipe = equipe["id"]
mon_equipe = equipe["nom"]

st.title("🤖 Mes matchs")

# récupérer équipes
equipes_data = supabase.table("equipes").select("*").execute()
equipes = {e["id"]: e["nom"] for e in equipes_data.data}

# récupérer matchs
matchs = supabase.table("matchs") \
    .select("*") \
    .order("heure") \
    .execute()

df = pd.DataFrame(matchs.data)

df["Equipe1"] = df["equipe1"].map(equipes)
df["Equipe2"] = df["equipe2"].map(equipes)

# garder seulement mes matchs
df = df[(df["equipe1"] == id_equipe) | (df["equipe2"] == id_equipe)]

for _, m in df.iterrows():

    heure_affichee = pd.to_datetime(str(m["heure"])).strftime("%H:%M")

    statut = "⏳"

    if m["termine"]:
        statut = "✅"

    texte = f"{m['Equipe1']} vs {m['Equipe2']}"

    st.write(
        f"{heure_affichee} | Terrain {m['terrain']} | {texte} {statut}"
    )


