import streamlit as st
import pandas as pd
from supabase import create_client

url = "https://yzupjrzhqmojefurpmrx.supabase.co"
key = "TA_CLE"

supabase = create_client(url, key)

st.title("🏆 Phase finale")

# récupérer les équipes
equipes_data = supabase.table("equipes").select("*").execute()
equipes = {e["id"]: e["nom"] for e in equipes_data.data}

# récupérer les matchs de phase finale
data = supabase.table("phase_finale").select("*").execute()

if not data.data:
    st.info("La phase finale n'est pas encore générée.")
    st.stop()

df = pd.DataFrame(data.data)

# convertir ID -> noms
df["Equipe1"] = df["equipe1"].map(equipes)
df["Equipe2"] = df["equipe2"].map(equipes)

# afficher par tour
tours = ["Huitieme","Quart","Demi","Finale"]

cols = st.columns(len(tours))

for i, tour in enumerate(tours):

    with cols[i]:

        st.subheader(tour)

        matchs = df[df["tour"] == tour]

        if matchs.empty:
            st.write("—")

        for _, m in matchs.iterrows():

            score = ""

            if m["termine"]:
                score = f"{m['score1']} - {m['score2']}"

            st.markdown(
                f"""
                <div style="
                border:1px solid #ddd;
                padding:10px;
                border-radius:8px;
                margin-bottom:10px;
                text-align:center;
                background:#f8f9fa;
                ">
                {m['Equipe1']} <br>
                vs <br>
                {m['Equipe2']} <br>
                <b>{score}</b>
                </div>
                """,
                unsafe_allow_html=True
            )
