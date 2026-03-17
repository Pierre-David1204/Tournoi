import streamlit as st
import pandas as pd
from supabase import create_client

url = "https://yzupjrzhqmojefurpmrx.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl6dXBqcnpocW1vamVmdXJwbXJ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM0MTY0ODcsImV4cCI6MjA4ODk5MjQ4N30.4qYKmPfDagkicbC31aob3egY2msh7mzuk7ECRJ2-M1A"

supabase = create_client(url, key)

if "equipe" not in st.session_state or st.session_state.equipe is None:
    st.switch_page("app.py")

equipe = st.session_state.equipe
poule_id = equipe["poule_id"]

st.title("📅 Planning des matchs")

# récupérer équipes
equipes_data = supabase.table("equipes").select("*").execute()
equipes = {e["id"]: e["nom"] for e in equipes_data.data}

# récupérer matchs
matchs = supabase.table("matchs") \
    .select("*") \
    .eq("poule_id", poule_id) \
    .order("heure") \
    .execute()

df = pd.DataFrame(matchs.data)

# convertir noms équipes
df["Equipe1"] = df["equipe1"].map(equipes)
df["Equipe2"] = df["equipe2"].map(equipes)

# grouper par heure
for heure, matchs_heure in df.groupby("heure"):

    heure_affichee = pd.to_datetime(str(heure)).strftime("%H:%M")

    st.subheader(heure_affichee)

    st.subheader(heure)

    for _, m in matchs_heure.sort_values("terrain").iterrows():

        statut = "⏳"

        if m["termine"]:
            statut = "✅"

        st.write(
            f"**Terrain {m['terrain']}** : "
            f"{m['Equipe1']} vs {m['Equipe2']} {statut}"
        )
