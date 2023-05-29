import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

class FoodRecommender:
    def __init__(self, recipe_path):
        self.recipe_df = pd.read_excel(recipe_path)
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.recipe_profiles = None

    def preprocess_data(self):
        self.recipe_df['preprocessed_ingredients'] = self.recipe_df['Ingredients'].apply(
            lambda x: ' '.join(sorted(x.split('\n')[1:-1]))
        )

    def compute_recipe_profiles(self):
        self.recipe_profiles = self.tfidf.fit_transform(self.recipe_df['preprocessed_ingredients'])

    def get_top_recipes(self, available, n=3):
        available_str = ' '.join(sorted(available))
        user_profile = self.tfidf.transform([available_str])
        similarity_scores = cosine_similarity(self.recipe_profiles, user_profile)
        top_recipes_idx = similarity_scores.argsort(axis=0)[::-1][:n].ravel()
        top_recipes = self.recipe_df.iloc[top_recipes_idx]
        top_recipes['Score'] = np.round((similarity_scores[top_recipes_idx]) * 100, 2).ravel()
        return top_recipes[['Recipe', 'Ingredients', 'Directions', 'Nutrition', 'Score']]