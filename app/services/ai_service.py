import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import joblib
import os
import random
from app.database import db

class AIService:
    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(__file__), '../models/expertise_model.pkl')
        self.vectorizer = TfidfVectorizer()
        self.expertise_areas = [
            "Software Development", "Web Development", "Mobile Apps", 
            "Artificial Intelligence", "Machine Learning", "Data Science", 
            "Database Systems", "Computer Networks", "Cybersecurity", 
            "Cloud Computing", "DevOps", "Game Development"
        ]
        
        # Try to load pre-trained model if it exists
        try:
            self.model = joblib.load(self.model_path)
        except:
            self.model = None
    
    def match_examiners(self, presentation, available_examiners, num_required):
        """
        Match examiners to a presentation based on expertise
        """
        if not available_examiners or len(available_examiners) < num_required:
            return []
        
        # Get technology category from presentation
        tech_category = presentation.get('technology_category', '')
        if not tech_category:
            # If no technology category specified, just return random examiners
            return random.sample(available_examiners, num_required)
        
        # Get expertise areas for each examiner
        examiner_expertise = []
        for examiner in available_examiners:
            expertise = ' '.join(examiner.get('areas_of_expertise', []))
            examiner_expertise.append(expertise)
        
        # If we have fewer than 2 examiners, TF-IDF won't work well
        # So just use simple matching
        if len(available_examiners) < 2:
            return available_examiners[:num_required]
        
        # Create TF-IDF matrix
        tfidf_matrix = self.vectorizer.fit_transform(examiner_expertise + [tech_category])
        
        # Calculate similarity between technology category and each examiner's expertise
        tech_index = len(examiner_expertise)
        similarities = cosine_similarity(tfidf_matrix[tech_index], tfidf_matrix[:tech_index])[0]
        
        # Get indices of examiners sorted by similarity (highest first)
        sorted_indices = np.argsort(-similarities)
        
        # Return the top N examiners
        matched_examiners = [available_examiners[i] for i in sorted_indices[:num_required]]
        return matched_examiners
    
    def train_expertise_model(self, examiner_data):
        """
        Train a model to match examiners based on expertise
        """
        # Extract expertise areas and create a corpus
        expertise_texts = []
        for examiner in examiner_data:
            expertise = examiner.get('areas_of_expertise', [])
            expertise_texts.append(' '.join(expertise))
        
        # Create TF-IDF matrix
        tfidf_matrix = self.vectorizer.fit_transform(expertise_texts)
        
        # Save the model
        self.model = {'vectorizer': self.vectorizer, 'tfidf_matrix': tfidf_matrix}
        joblib.dump(self.model, self.model_path)
        
        return self.model