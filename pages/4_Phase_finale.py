import streamlit as st
from utils.supabase_client import supabase

st.title("🏆 Phase finale")

matchs = supabase.table("matchs") \
    .select("*") \
    .is_("poule_id", None) \
    .execute()

for m in matchs.data:

    st.write(
        f"{m['division']} : {m['robot1']} vs {m['robot2']}"
    )