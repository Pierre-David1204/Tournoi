import streamlit as st
import pandas as pd
from utils.supabase_client import supabase

st.title("📊 Classement")

robot = st.session_state.robot
poule_id = robot["poule_id"]

robots = supabase.table("robots") \
    .select("*") \
    .eq("poule_id", poule_id) \
    .execute()

df = pd.DataFrame(robots.data)

df = df.sort_values(
    ["points", "score_total"],
    ascending=False
)

st.dataframe(df[[
    "nom",
    "points",
    "victoires",
    "nuls",
    "defaites",
    "score_total"
]])