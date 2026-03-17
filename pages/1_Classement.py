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
mon_equipe = equipe["nom"]

st.title("📊 Classement de la poule")

# récupérer équipes de la poule
data = supabase.table("equipes") \
    .select("*") \
    .eq("poule_id", poule_id) \
    .execute()

df = pd.DataFrame(data.data)

df = df.sort_values(
    ["points", "victoires", "manches_gagnees"],
    ascending=False
)

df.insert(0, "#", range(1, len(df) + 1))

df = df.rename(columns={
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


def highlight_team(row):
    if row["Equipe"] == mon_equipe:
        return ["font-weight: bold"] * len(row)
    return [""] * len(row)

styled = df.style.apply(highlight_team, axis=1)

st.dataframe(styled, use_container_width=True)


# --------------------------
# CLASSEMENT DES 4EMES
# --------------------------

st.title("🏁 Classement des 4èmes")

data_all = supabase.table("equipes").select("*").execute()

df_all = pd.DataFrame(data_all.data)

# classement dans chaque poule
df_all = df_all.sort_values(
    ["poule_id", "points", "victoires", "manches_gagnees"],
    ascending=[True, False, False, False]
)

df_all["rang"] = df_all.groupby("poule_id").cumcount() + 1

quatriemes = df_all[df_all["rang"] == 4]

quatriemes = quatriemes.sort_values(
    ["points", "victoires", "manches_gagnees"],
    ascending=False
)

quatriemes.insert(0, "Rang", range(1, len(quatriemes) + 1))

quatriemes = quatriemes.rename(columns={
    "nom": "Equipe",
    "poule_id": "Poule",
    "points": "Pts",
    "victoires": "V",
    "manches_gagnees": "Manches +"
})

quatriemes = quatriemes[[
    "Rang",
    "Equipe",
    "Poule",
    "Pts",
    "V",
    "Manches +"
]]

st.dataframe(quatriemes, use_container_width=True)
