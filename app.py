import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data
resumes = pd.read_csv('data/resumes.csv')
jobs = pd.read_csv('data/job_descriptions.csv')

st.title('Job Recommendation System')

# Select resume
selected_resume_id = st.selectbox('Select Your Resume:', resumes['id'])
selected_resume_text = resumes[resumes['id'] == selected_resume_id]['resume_text'].values[0]

# Combine texts
texts = jobs['job_description'].tolist()
texts.insert(0, selected_resume_text)

# TF-IDF and cosine similarity
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(texts)
cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

# Show results
jobs['Similarity Score'] = cosine_sim
top_matches = jobs.sort_values('Similarity Score', ascending=False)

st.subheader('Top Job Matches:')
st.dataframe(top_matches[['job_description', 'Similarity Score']])
