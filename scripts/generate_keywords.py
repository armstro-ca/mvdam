import pandas as pd
import random

import nltk
from nltk.corpus import words
import random

# Download the words dataset
nltk.download('words')

# Get a list of English words
english_words = words.words()

# Shuffle the list to make it random
random.shuffle(english_words)

# Select the first 100 words from the shuffled list
random_words = english_words[:100]


# Load Dataframe
with open('assets.csv', 'r') as f:
    df = pd.read_csv(f)

# Function to generate random keywords
def generate_keywords():
    return ', '.join(random.sample(random_words, k=random.randint(3, 10)))

# Apply the function to create a new 'Keywords' column
df['Keywords'] = df.apply(lambda row: generate_keywords(), axis=1)

# Save the DataFrame
df.to_csv('assets_with_keywords.csv', index=False, encoding='utf-8')