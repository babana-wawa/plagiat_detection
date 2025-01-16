 
import re
from typing import List

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

def get_text_from_file(file_content: str) -> str:
    """
    Extrait le texte du contenu du fichier.
    """
    return file_content.strip()