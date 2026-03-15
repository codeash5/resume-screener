Resume Screener

Description:
* Developed an AI-assisted Resume Screener in Python that ranks PDF resumes against multiple job descriptions using TF-IDF similarity and skill-based matching.
* The system extracts text from resumes, identifies relevant skills, computes similarity and skill match scores, detects missing skills, and generates recruiter-friendly CSV and Excel reports.
* A Streamlit interface is also included for interactive execution and result viewing.

Features:
* Extracts text from PDF resumes
* Cleans and preprocesses resume and job description text
* Uses TF-IDF vectorization and cosine similarity for resume-job matching
* Detects skills from resumes using a predefined skill dictionary
* Computes skill match score against job description skills
* Identifies missing skills for each candidate
* Calculates final weighted score using similarity and skill match
* Generates:
  1. resume_scores_per_jd.csv for raw structured output
  2. resume_scores_per_jd.xlsx for recruiter-friendly reporting
* Displays results in a Streamlit web interface
* Supports multiple job descriptions and recursive resume folders

Tech Stack:
* Python
* Pandas
* Scikit-learn
* PyPDF2
* Openpyxl
* Streamlit

Project Structure:
* resume_screener/

  * data/

    * resumes/
    * job_descriptions/
    * resume_scores_per_jd.csv
    * resume_scores_per_jd.xlsx
  * src/

    * resume_screener.py
    * streamlit_app.py
  * README.md

How It Works:
1. Resume PDFs are loaded and text is extracted.
2. Job descriptions are loaded from text files.
3. TF-IDF similarity is calculated between each resume and job description.
4. Skills are extracted from resume text.
5. Skill match score is calculated using job description skills.
6. Missing skills are detected for each resume.
7. Final score is computed using weighted similarity and skill match.
8. Results are exported to CSV and Excel and shown in Streamlit.

How to Run:
Install dependencies:
pip install pandas scikit-learn PyPDF2 openpyxl streamlit

Place files:
* Put resumes (.pdf) inside data/resumes/
* Put job descriptions (.txt) inside data/job_descriptions/

Run Python script:
python src/resume_screener.py

Run Streamlit app:
streamlit run src/streamlit_app.py

Output:
* The project generates the following outputs:
  1. resume_scores_per_jd.csv for raw candidate-job matching results
  2. resume_scores_per_jd.xlsx for formatted Excel report with rankings
  3. Streamlit table view with downloadable results

Typical columns include:
* Job Description
* Resume Filename
* Category
* Similarity Score
* Skill Match
* Final Score
* Match %
* Rank
* Missing Skills

Use Case:
* This project simulates a lightweight Applicant Tracking System workflow for recruiters or hiring teams by helping shortlist the most relevant resumes and highlighting skill gaps.

Future Improvements:
* Improve job description skill extraction logic
* Add support for scanned PDFs using OCR
* Include experience and education weighting
* Add filtering and charts in Streamlit
* Use NLP libraries like spaCy for smarter keyword extraction




