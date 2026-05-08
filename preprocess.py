import re
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required files
nltk.download('punkt')
nltk.download('stopwords')

# Load stopwords
stop_words = set(stopwords.words('english'))

# Function to clean text
def clean_text(text):

    # Convert to lowercase
    text = text.lower()

    # Remove special characters
    text = re.sub(r'[^a-zA-Z ]', '', text)

    # Tokenization
    words = word_tokenize(text)

    # Remove stopwords
    filtered_words = []

    for word in words:
        if word not in stop_words:
            filtered_words.append(word)

    # Join words
    cleaned_text = " ".join(filtered_words)

    return cleaned_text