import streamlit as st
from algorithms.text_processor import preprocess_text, get_text_from_file
from algorithms.similarity import lcs_similarity, levenshtein_similarity, cosine_similarity

# Configuration de la page
st.set_page_config(
    page_title="Détecteur de Plagiat",
    layout="wide"
)

# Titre et description
st.title("🔍 Détecteur de Plagiat")
st.markdown("""
    Cette application permet de détecter les similarités entre deux documents
    en utilisant trois algorithmes différents.
""")

# CSS personnalisé
st.markdown("""
<style>
    .stApp {
        background-color: #f0f8ff;
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Zone de téléchargement des fichiers
col1, col2 = st.columns(2)

with col1:
    st.subheader("Document 1")
    file1 = st.file_uploader("Choisissez le premier document", type=["txt"])

with col2:
    st.subheader("Document 2")
    file2 = st.file_uploader("Choisissez le second document", type=["txt"])

def analyze_similarity(text1, text2):
    # Prétraitement des textes
    processed_text1 = preprocess_text(text1)
    processed_text2 = preprocess_text(text2)
    
    # Calcul des similarités
    results = {
        "LCS": lcs_similarity(processed_text1, processed_text2),
        "Levenshtein": levenshtein_similarity(processed_text1, processed_text2),
        "Cosinus": cosine_similarity(processed_text1, processed_text2)
    }
    
    return results

def get_plagiarism_level(score):
    if score < 30:
        return "🟢 Plagiat peu probable", "green"
    elif score < 70:
        return "🟡 Plagiat soupçonnable", "orange"
    else:
        return "🔴 Plagiat très probable", "red"

if file1 is not None and file2 is not None:
    text1 = file1.read().decode()
    text2 = file2.read().decode()
    
    if st.button("Analyser les documents"):
        results = analyze_similarity(text1, text2)
        
        # Affichage des résultats
        st.subheader("Résultats de l'analyse")
        
        cols = st.columns(3)
        for idx, (method, score) in enumerate(results.items()):
            with cols[idx]:
                st.metric(
                    label=f"Similarité {method}",
                    value=f"{score:.1f}%"
                )
        
        # Moyenne des scores
        average_score = sum(results.values()) / len(results)
        message, color = get_plagiarism_level(average_score)
        
        st.markdown(f"""
        <div style='text-align: center; margin-top: 2rem;'>
            <h2 style='color: {color};'>{message}</h2>
            <h3>Score moyen de similarité: {average_score:.1f}%</h3>
        </div>
        """, unsafe_allow_html=True)