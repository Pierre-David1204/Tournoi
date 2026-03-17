import streamlit as st
import pandas as pd
from supabase import create_client

url = "https://yzupjrzhqmojefurpmrx.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl6dXBqcnpocW1vamVmdXJwbXJ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM0MTY0ODcsImV4cCI6MjA4ODk5MjQ4N30.4qYKmPfDagkicbC31aob3egY2msh7mzuk7ECRJ2-M1A"

supabase = create_client(url, key)

st.title("🏆 Phase finale")

# récupérer équipes
data = supabase.table("equipes").select("*").execute()
df = pd.DataFrame(data.data)

# classement dans chaque poule
df = df.sort_values(
    ["poule_id","points","victoires","manches_gagnees"],
    ascending=[True,False,False,False]
)

df["rang"] = df.groupby("poule_id").cumcount() + 1

premiers = df[df["rang"] == 1]
deuxiemes = df[df["rang"] == 2]
troisiemes = df[df["rang"] == 3]
quatriemes = df[df["rang"] == 4]

best4 = quatriemes.sort_values(
    ["points","victoires","manches_gagnees"],
    ascending=False
).head(1)

qualifies = pd.concat([premiers,deuxiemes,troisiemes,best4])

st.subheader("Equipes qualifiées")

st.dataframe(qualifies[["nom","poule_id","points"]])

# génération automatique
if st.button("Générer les huitièmes"):

    teams = qualifies.sample(frac=1).reset_index(drop=True)

    matchs = []
    used = set()

    for i in range(len(teams)):

        if i in used:
            continue

        for j in range(i+1,len(teams)):

            if j in used:
                continue

            if teams.loc[i,"poule_id"] != teams.loc[j,"poule_id"]:

                matchs.append(
                    (teams.loc[i,"id"],teams.loc[j,"id"])
                )

                used.add(i)
                used.add(j)
                break

    matchs = matchs[:8]

    for i,m in enumerate(matchs):

        supabase.table("phase_finale").insert({

            "tour":"Huitieme",
            "match_num":i+1,

            "equipe1":m[0],
            "equipe2":m[1]

        }).execute()

    st.success("Huitièmes générés !")
