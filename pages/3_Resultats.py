import streamlit as st
from supabase import create_client

url = "https://yzupjrzhqmojefurpmrx.supabase.co"
key = "TA_CLE"

supabase = create_client(url, key)

st.title("📋 Résultats")

matchs = supabase.table("matchs") \
    .select("*") \
    .eq("termine", True) \
    .execute()

for m in matchs.data:

    st.write(
        f"{m['robot1']} {m['score1']} - {m['score2']} {m['robot2']}"
    )
