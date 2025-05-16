# Resume to Job Matching System

This application helps users find job opportunities that match their skills and experience by analyzing their uploaded resume and comparing it with job listings.

---

## How to Use

1. **Enter Job Query**  
   Input the type of job you are looking for (default is "software developer").

2. **Upload Resume**  
   Upload your resume in PDF format.

3. **View Job Matches**  
   The system will extract text from your resume, fetch relevant job listings in India, and display them along with a match percentage based on text similarity.

---

## Features

- Fetches job listings from Google Jobs using SerpAPI  
- Extracts text from PDF resumes  
- Uses TF-IDF and cosine similarity to calculate match scores between resume and job descriptions  
- Displays detailed job information and match percentages in an interactive interface  

---

## Requirements

- Python 3.7 or higher  
- Streamlit  
- Requests  
- PyPDF2  
- Pandas  
- scikit-learn  

Install dependencies using:

```bash
pip install streamlit requests PyPDF2 pandas scikit-learn

## Running the Application
 - streamlit run app.py