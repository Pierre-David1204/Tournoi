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

# classement poules
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

# bracket HTML
bracket_html = f"""
<style>
.bracket {{
display:flex;
justify-content:center;
gap:40px;
font-size:16px;
}}

.round {{
display:flex;
flex-direction:column;
gap:30px;
}}

.match {{
border:1px solid #ccc;
padding:8px;
border-radius:6px;
background:#f9f9f9;
width:150px;
text-align:center;
}}
</style>

<div class="bracket">

<div class="round">
<h4>Huitièmes</h4>

<div class="match">{teams[0]}<br>vs<br>{teams[15]}</div>
<div class="match">{teams[7]}<br>vs<br>{teams[8]}</div>
<div class="match">{teams[4]}<br>vs<br>{teams[11]}</div>
<div class="match">{teams[3]}<br>vs<br>{teams[12]}</div>
<div class="match">{teams[5]}<br>vs<br>{teams[10]}</div>
<div class="match">{teams[2]}<br>vs<br>{teams[13]}</div>
<div class="match">{teams[6]}<br>vs<br>{teams[9]}</div>
<div class="match">{teams[1]}<br>vs<br>{teams[14]}</div>

</div>

<div class="round">
<h4>Quarts</h4>

<div class="match">Quart 1</div>
<div class="match">Quart 2</div>
<div class="match">Quart 3</div>
<div class="match">Quart 4</div>

</div>

<div class="round">
<h4>Demi</h4>

<div class="match">Demi 1</div>
<div class="match">Demi 2</div>

</div>

<div class="round">
<h4>Finale</h4>

<div class="match">Finale</div>

</div>

</div>
"""

st.markdown(bracket_html, unsafe_allow_html=True)
