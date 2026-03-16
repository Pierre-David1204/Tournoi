import streamlit as st
from utils.supabase_client import supabase

st.title("📋 Résultats")

matchs = supabase.table("matchs") \
    .select("*") \
    .eq("termine", True) \
    .execute()

for m in matchs.data:

    if m["division"] == "D1":

        scores = supabase.table("scores_d1") \
            .select("*") \
            .eq("match_id", m["id"]) \
            .execute()

        st.write(scores.data)

    else:

        manches = supabase.table("scores_d2") \
            .select("*") \
            .eq("match_id", m["id"]) \
            .execute()

        st.write(manches.data)