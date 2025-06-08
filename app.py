import streamlit as st
import os
from dotenv import load_dotenv
from utils.parser import extract_text_from_pdf, extract_skills
import requests

# Load API key from .env file
load_dotenv()
api_key = os.getenv("RAPIDAPI_KEY")

# Function to fetch live jobs using RapidAPI JSearch
def fetch_live_jobs(query):
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    params = {"query": query, "page": 1, "num_pages": 1}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get("data", [])
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Error fetching jobs: {e}")
    return []

# Streamlit UI
st.set_page_config(page_title="Smart Job Recommender", layout="centered")
st.title("📄 Smart Job Recommendation System")
st.write("Upload your resume and get live job suggestions based on your skills!")

# File upload
uploaded_file = st.file_uploader("📤 Upload your resume (PDF only)", type="pdf")

if uploaded_file:
    with st.spinner("🔍 Extracting skills from resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    # Handle unreadable PDFs
    if resume_text is None:
        st.error("❌ Unable to read the uploaded file. Please upload a valid PDF.")
    else:
        extracted_skills = extract_skills(resume_text)

        if extracted_skills:
            st.success("✅ Skills Extracted Successfully!")
            st.write("**Skills Identified:**", ", ".join(extracted_skills))

            # Fetch real jobs
            st.subheader("🌐 Matching Live Job Listings")
            query = " ".join(extracted_skills[:3]) if extracted_skills else "developer"
            live_jobs = fetch_live_jobs(query)

            if live_jobs:
                for job in live_jobs:
                    st.markdown(f"### {job.get('job_title', 'No Title')}")
                    st.markdown(f"**{job.get('employer_name', 'Unknown Company')} - {job.get('job_city', 'Unknown Location')}**")
                    st.markdown(f"[Apply Here]({job.get('job_apply_link', '#')})")
                    st.markdown("---")
            else:
                st.info("🔍 No jobs found for extracted skills. Try uploading a more detailed resume.")
        else:
            st.warning("❌ No skills detected. Please upload a more detailed resume.")
