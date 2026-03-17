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
df = pd.DataFrame(data.data)

df["Equipe1"] = df["equipe1"].map(equipes)
df["Equipe2"] = df["equipe2"].map(equipes)

# affichage par tour
for tour, matchs in df.groupby("tour"):

    st.header(tour)

    cols = st.columns(4)

    for i, m in enumerate(matchs.iterrows()):

        m = m[1]

        col = cols[i % 4]

        score = ""

        if m["termine"]:
            score = f"{m['score1']} - {m['score2']}"

        with col:

            st.markdown(
                f"""
                <div style="
                border:1px solid #ddd;
                padding:12px;
                border-radius:8px;
                text-align:center;
                background:#f8f9fa;
                margin-bottom:10px;
                ">
                {m['Equipe1']} <br>
                vs <br>
                {m['Equipe2']} <br>
                <b>{score}</b>
                </div>
                """,
                unsafe_allow_html=True
            )
