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

# classement dans chaque poule
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

meilleur4 = quatriemes.sort_values(
    ["points","victoires","manches_gagnees"],
    ascending=False
).head(1)

qualifies = pd.concat([
    premiers,
    deuxiemes,
    troisiemes,
    meilleur4
])

# éviter rencontres même poule
teams = qualifies.sample(frac=1).reset_index(drop=True)

matchs = []
used = set()

for i in range(len(teams)):

    if i in used:
        continue

    for j in range(i+1, len(teams)):

        if j in used:
            continue

        if teams.loc[i,"poule_id"] != teams.loc[j,"poule_id"]:

            matchs.append(
                (
                    teams.loc[i,"nom"],
                    teams.loc[j,"nom"]
                )
            )

            used.add(i)
            used.add(j)
            break

matchs = matchs[:8]

# affichage bracket
col1,col2,col3,col4 = st.columns(4)

with col1:

    st.subheader("Huitièmes")

    for m in matchs:

        st.markdown(
            f"""
            <div style="
            border:1px solid #ddd;
            padding:12px;
            margin-bottom:10px;
            border-radius:8px;
            text-align:center;
            background:#f8f9fa;
            ">
            {m[0]} <br> vs <br> {m[1]}
            </div>
            """,
            unsafe_allow_html=True
        )

with col2:

    st.subheader("Quarts")

    for _ in range(4):

        st.markdown(
            """
            <div style="
            border:1px dashed #bbb;
            padding:12px;
            margin-bottom:10px;
            border-radius:8px;
            text-align:center;
            ">
            à déterminer
            </div>
            """,
            unsafe_allow_html=True
        )

with col3:

    st.subheader("Demi")

    for _ in range(2):

        st.markdown(
            """
            <div style="
            border:1px dashed #bbb;
            padding:12px;
            margin-bottom:10px;
            border-radius:8px;
            text-align:center;
            ">
            à déterminer
            </div>
            """,
            unsafe_allow_html=True
        )

with col4:

    st.subheader("Finale")

    st.markdown(
        """
        <div style="
        border:2px solid gold;
        padding:16px;
        border-radius:10px;
        text-align:center;
        font-weight:bold;
        ">
        🏆 Finale
        </div>
        """,
        unsafe_allow_html=True
    )
