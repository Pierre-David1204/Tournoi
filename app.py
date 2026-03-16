import streamlit as st
from supabase import create_client

# connexion supabase
url = "https://yzupjrzhqmojefurpmrx.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl6dXBqcnpocW1vamVmdXJwbXJ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM0MTY0ODcsImV4cCI6MjA4ODk5MjQ4N30.4qYKmPfDagkicbC31aob3egY2msh7mzuk7ECRJ2-M1A"

supabase = create_client(url, key)

st.title("🤖 Tournoi Robot - Connexion")

# session
if "equipe" not in st.session_state:
    st.session_state.equipe = None


# récupérer les équipes
data = supabase.table("equipes").select("*").order("nom").execute()

equipes = data.data

noms_equipes = [e["nom"] for e in equipes]


# menu déroulant
equipe_selection = st.selectbox(
    "Choisissez votre équipe",
    noms_equipes
)


if st.button("Se connecter"):

    equipe = next(e for e in equipes if e["nom"] == equipe_selection)

    st.session_state.equipe = equipe

    st.success(f"Connecté : {equipe_selection}")

    st.switch_page("pages/1_Classement.py")import streamlit as st
