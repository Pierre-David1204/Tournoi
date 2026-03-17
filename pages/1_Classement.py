import streamlit as st
import pandas as pd
from supabase import create_client

# connexion supabase
url = "https://yzupjrzhqmojefurpmrx.supabase.co"
key = "TA_CLE"

supabase = create_client(url, key)

# vérifier connexion
if "equipe" not in st.session_state or st.session_state.equipe is None:
    st.switch_page("app.py")

equipe = st.session_state.equipe
poule_id = equipe["poule_id"]
mon_equipe = equipe["nom"]

st.title("📊 Classement de la poule")

# récupérer les équipes
data = supabase.table("equipes") \
    .select("*") \
    .eq("poule_id", poule_id) \
    .execute()

df = pd.DataFrame(data.data)

# tri classement
df = df.sort_values(
    ["points", "victoires", "manches_gagnees"],
    ascending=False
)

# ajouter position
df.insert(0, "pos", range(1, len(df) + 1))

df = df.rename(columns={
    "pos": "#",
    "nom": "Equipe",
    "points": "Pts",
    "victoires": "V",
    "nuls": "N",
    "defaites": "D",
    "manches_gagnees": "Manches +",
    "manches_perdues": "Manches -"
})

df = df[[
    "#",
    "Equipe",
    "Pts",
    "V",
    "N",
    "D",
    "Manches +",
    "Manches -"
]]

# fonction pour mettre ton équipe en gras
def highlight_team(row):
    if row["Equipe"] == mon_equipe:
        return ["font-weight: bold"] * len(row)
    return [""] * len(row)

styled = df.style.apply(highlight_team, axis=1)

st.dataframe(
    styled,
    use_container_width=True
)
