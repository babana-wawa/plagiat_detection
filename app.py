import streamlit as st
from algorithms.text_processor import preprocess_text, get_file_text
from algorithms.similarity import lcs_similarity, levenshtein_similarity, cosine_similarity
import base64

# Configuration de la page
st.set_page_config(
    page_title="Détecteur de Plagiat",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé
st.markdown("""
    <style>
    /* Styles personnalisés pour l'application Streamlit */
    .stApp {
        background-color: #167db8c1; /* Couleur de fond bleu grisé */
    }

    .main-container {
        background: rgba(255, 255, 255, 0.85); /* Ajusté pour la translucidité */
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem auto;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        max-width: 1200px;
    }

    .title-container {
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: linear-gradient(135deg, #6e8efb, #4a6ee0);
        border-radius: 15px;
        color: white;
    }

    .upload-container, .results-container, .metric-card, .final-score {
        background: rgba(255, 255, 255, 0.85); /* Ajusté pour la translucidité */
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .upload-container {
        margin: 1rem 0;
    }

    .metric-card {
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
    }

    .final-score {
        text-align: center;
        margin-top: 2rem;
        padding: 1.5rem;
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #6e8efb, #4a6ee0);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        border: none;
        font-weight: 600;
        margin-top: 1rem;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #4a6ee0, #6e8efb);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(74, 110, 224, 0.4);
    }

    .upload-text {
        font-size: 1rem;
        color: #444;
        margin-bottom: 0.5rem;
    }

    </style>
    """, unsafe_allow_html=True)

# Container principal
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Titre et description
    st.markdown('''
        <div class="title-container">
            <h1>🔍 Détecteur de Plagiat</h1>
            <p>Analysez la similarité entre vos documents en quelques clics</p>
        </div>
    ''', unsafe_allow_html=True)

    # Zone de téléchargement
    st.markdown('<div class="upload-container">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📄 Premier document")
        st.markdown('<p class="upload-text">Sélectionnez le premier document à analyser</p>', unsafe_allow_html=True)
        file1 = st.file_uploader("Premier document", type=["txt", "pdf", "docx"], key="file1", label_visibility="collapsed")

    with col2:
        st.markdown("### 📄 Second document")
        st.markdown('<p class="upload-text">Sélectionnez le second document à analyser</p>', unsafe_allow_html=True)
        file2 = st.file_uploader("Second document", type=["txt", "pdf", "docx"], key="file2", label_visibility="collapsed")

    st.markdown('</div>', unsafe_allow_html=True)

    if file1 is not None and file2 is not None:
        try:
            # Utilisation de la nouvelle fonction get_file_text
            text1 = get_file_text(file1.read(), file1.name)
            text2 = get_file_text(file2.read(), file2.name)

            if st.button("Lancer l'analyse"):
                with st.spinner('Analyse en cours...'):
                    # Prétraitement des textes
                    processed_text1 = preprocess_text(text1)
                    processed_text2 = preprocess_text(text2)

                    # Calcul des similarités
                    results = {
                        "LCS": lcs_similarity(processed_text1, processed_text2),
                        "Levenshtein": levenshtein_similarity(processed_text1, processed_text2),
                        "Cosinus": cosine_similarity(processed_text1, processed_text2)
                    }

                    st.markdown('<div class="results-container">', unsafe_allow_html=True)

                    # Affichage des résultats
                    cols = st.columns(3)
                    for idx, (method, score) in enumerate(results.items()):
                        with cols[idx]:
                            st.markdown(f'''
                                <div class="metric-card">
                                    <h4>{method}</h4>
                                    <h2>{score:.1f}%</h2>
                                </div>
                            ''', unsafe_allow_html=True)

                    # Score moyen et message
                    average_score = sum(results.values()) / len(results)
                    if average_score < 30:
                        message = "🟢 Similarité faible"
                        color = "green"
                    elif average_score < 70:
                        message = "🟡 Similarité modérée"
                        color = "orange"
                    else:
                        message = "🔴 Forte similarité"
                        color = "red"

                    st.markdown(f"""
                        <div class="final-score">
                            <h2 style='color: {color}'>{message}</h2>
                            <h3>Score global de similarité: {average_score:.1f}%</h3>
                        </div>
                    """, unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Une erreur est survenue lors de l'analyse: {str(e)}")

    st.markdown('</div>', unsafe_allow_html=True)
