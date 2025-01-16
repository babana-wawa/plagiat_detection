import re
from typing import List
import PyPDF2
from docx import Document
import io

def get_file_text(file_content: bytes, file_type: str) -> str:
    """
    Extrait le texte selon le type de fichier.
    """
    if file_type.lower().endswith('pdf'):
        return extract_text_from_pdf(file_content)
    elif file_type.lower().endswith('docx'):
        return extract_text_from_docx(file_content)
    elif file_type.lower().endswith('txt'):
        return extract_text_from_txt(file_content)
    else:
        raise ValueError("Format de fichier non supporté")

def extract_text_from_pdf(file_content):
    """Extrait le texte d'un fichier PDF."""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise Exception(f"Erreur lors de la lecture du PDF: {str(e)}")

def extract_text_from_docx(file_content):
    """Extrait le texte d'un fichier DOCX."""
    try:
        doc = Document(io.BytesIO(file_content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        raise Exception(f"Erreur lors de la lecture du DOCX: {str(e)}")

def extract_text_from_txt(file_content):
    """Extrait le texte d'un fichier TXT."""
    try:
        return file_content.decode('utf-8')
    except UnicodeDecodeError:
        try:
            return file_content.decode('latin-1')
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture du TXT: {str(e)}")

def preprocess_text(text: str) -> List[str]:
    """
    Prétraite le texte en le nettoyant et en retirant les mots courants.
    """
    # Conversion en minuscules
    text = text.lower()

    # Suppression des caractères spéciaux et nombres
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)

    # Liste des mots courants français
    stop_words = {
        'le', 'la', 'les', 'un', 'une', 'des', 'et', 'ou', 'donc',
        'car', 'mais', 'où', 'qui', 'que', 'quoi', 'dont', 'pour',
        'dans', 'par', 'sur', 'avec', 'sans', 'sous', 'dans'
    }

    # Tokenization et suppression des mots courants
    words = text.split()
    words = [word for word in words if word not in stop_words]

    return words
