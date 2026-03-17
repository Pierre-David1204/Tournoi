import streamlit as st
import pandas as pd
import random
from supabase import create_client

url = "https://yzupjrzhqmojefurpmrx.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl6dXBqcnpocW1vamVmdXJwbXJ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM0MTY0ODcsImV4cCI6MjA4ODk5MjQ4N30.4qYKmPfDagkicbC31aob3egY2msh7mzuk7ECRJ2-M1A"

supabase = create_client(url, key)

st.title("🏆 Phase finale")

# récupérer équipes
data = supabase.table("equipes").select("*").execute()
df = pd.DataFrame(data.data)

# classement poules
df = df.sort_values(
    ["poule_id","points","victoires","manches_gagnees"],
    ascending=[True,False,False,False]
)

df["rang"] = df.groupby("poule_id").cumcount() + 1

# qualifiés
premiers = df[df["rang"] == 1]
deuxiemes = df[df["rang"] == 2]
troisiemes = df[df["rang"] == 3]
quatriemes = df[df["rang"] == 4]

best4 = quatriemes.sort_values(
    ["points","victoires","manches_gagnees"],
    ascending=False
).head(1)

qualifies = pd.concat([
    premiers,
    deuxiemes,
    troisiemes,
    best4
])

teams = qualifies.sample(frac=1).reset_index(drop=True)

# éviter mêmes poules
matchs = []
used = set()

for i in range(len(teams)):

    if i in used:
        continue

    for j in range(i+1,len(teams)):

        if j in used:
            continue

        if teams.loc[i,"poule_id"] != teams.loc[j,"poule_id"]:

            matchs.append((teams.loc[i],teams.loc[j]))

            used.add(i)
            used.add(j)

            break

matchs = matchs[:8]

# affichage bracket
col1,col2,col3,col4 = st.columns(4)

with col1:

    st.subheader("Huitièmes")

    winners_8 = []

    for m in matchs:

        equipe1 = m[0]["nom"]
        equipe2 = m[1]["nom"]

        choice = st.radio(
            f"{equipe1} vs {equipe2}",
            [equipe1,equipe2],
            key=f"huitieme_{equipe1}_{equipe2}"
        )

        winners_8.append(choice)

with col2:

    st.subheader("Quarts")

    winners_4 = []

    for i in range(0,len(winners_8),2):

        e1 = winners_8[i]
        e2 = winners_8[i+1]

        choice = st.radio(
            f"{e1} vs {e2}",
            [e1,e2],
            key=f"quart_{i}"
        )

        winners_4.append(choice)

with col3:

    st.subheader("Demi")

    winners_2 = []

    for i in range(0,len(winners_4),2):

        e1 = winners_4[i]
        e2 = winners_4[i+1]

        choice = st.radio(
            f"{e1} vs {e2}",
            [e1,e2],
            key=f"demi_{i}"
        )

        winners_2.append(choice)

with col4:

    st.subheader("Finale")

    champion = st.radio(
        f"{winners_2[0]} vs {winners_2[1]}",
        [winners_2[0],winners_2[1]],
        key="finale"
    )

    st.success(f"🏆 Champion : {champion}")
