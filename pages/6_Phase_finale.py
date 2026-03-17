import streamlit as st
import pandas as pd
from supabase import create_client

url = "https://yzupjrzhqmojefurpmrx.supabase.co"
key = "TA_CLE"

supabase = create_client(url, key)

st.title("🏆 Phase finale")

# récupérer équipes
data = supabase.table("equipes").select("*").execute()
df = pd.DataFrame(data.data)

# calcul qualifiés
df = df.sort_values(
    ["poule_id","points","victoires","manches_gagnees"],
    ascending=[True,False,False,False]
)

df["rang"] = df.groupby("poule_id").cumcount() + 1

top3 = df[df["rang"] <= 3]
quatriemes = df[df["rang"] == 4]

best4 = quatriemes.sort_values(
    ["points","victoires","manches_gagnees"],
    ascending=False
).head(1)

qualifies = pd.concat([top3,best4])

qualifies = qualifies.sort_values(
    ["points","victoires","manches_gagnees"],
    ascending=False
)

teams = qualifies["nom"].tolist()

# arbre tournoi
st.header("Huitièmes")

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.write(teams[0])
    st.write("vs")
    st.write(teams[15])

    st.write("---")

    st.write(teams[7])
    st.write("vs")
    st.write(teams[8])

with col2:
    st.write(teams[4])
    st.write("vs")
    st.write(teams[11])

    st.write("---")

    st.write(teams[3])
    st.write("vs")
    st.write(teams[12])

with col3:
    st.write(teams[5])
    st.write("vs")
    st.write(teams[10])

    st.write("---")

    st.write(teams[2])
    st.write("vs")
    st.write(teams[13])

with col4:
    st.write(teams[6])
    st.write("vs")
    st.write(teams[9])

    st.write("---")

    st.write(teams[1])
    st.write("vs")
    st.write(teams[14])
