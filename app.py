import streamlit as st
import requests
import PyPDF2
import pandas as pd
import urllib.parse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.title("🔍 Resume to Job Matching System")
st.markdown("Upload your resume and find job opportunities that align with your skills and goals.")

# Job search input
job_query = st.text_input("Enter the type of job you are looking for:", value="software developer", max_chars=50)

# Resume upload
uploaded_file = st.file_uploader("Upload your resume (PDF format only):", type=["pdf"])

def get_indian_jobs(query=job_query, location="India", num=8):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "api_key": "b631831f3b725d9e725eb03035fccdd7763c026a25aba5d9d47023c639b7c9e2"  # Replace with your real SerpAPI key
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            results = response.json().get("jobs_results", [])[:num]
            jobs = []
            for job in results:
                title = job.get("title", "Untitled")
                company = job.get("company_name", "")
                raw_link = job.get("related_links", [{}])[0].get("link", "")
                search_query = f"{title} {company} jobs India"
                search_fallback = f"https://www.google.com/search?q={urllib.parse.quote_plus(search_query)}"
                jobs.append({
                    "title": title,
                    "description": job.get("description", "No description provided."),
                    "link": raw_link if raw_link else search_fallback
                })
            return jobs
        else:
            st.error(f"Failed to fetch job data. Status code: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"An error occurred while fetching jobs: {e}")
        return []

if uploaded_file is not None:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    resume_text = ""
    for page in pdf_reader.pages:
        resume_text += page.extract_text()

    st.subheader("📄 Extracted Resume Text:")
    st.write(resume_text[:1000] + "...")

    jobs = get_indian_jobs(job_query)

    if jobs:
        st.subheader("📌 Job Opportunities in India")
        for i, job in enumerate(jobs):
            with st.expander(f"{i+1}. {job['title']}"):
                st.write(job['description'][:1500] + "...")
                st.markdown(f"[View Full Job Listing]({job['link']})", unsafe_allow_html=True)

        job_texts = [job["description"] for job in jobs]
        texts = [resume_text] + job_texts

        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(texts)
        scores = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

        job_matches = pd.DataFrame({
            "Job Title": [job["title"] for job in jobs],
            "Match %": [round(score * 100, 2) for score in scores]
        }).sort_values(by="Match %", ascending=False)

        st.subheader("✅ Resume-to-Job Match Results")
        st.dataframe(job_matches)

        top_match = job_matches.iloc[0]
        st.success(f"Top Match: {top_match['Job Title']} ({top_match['Match %']}% match)")
        st.markdown("🔗 [Explore more jobs](https://www.google.com/search?q=jobs+India)")
    else:
        st.warning("No job listings found. Please try a different query or check your network.")
else:
    st.info("Please upload your resume to get started.")
