Resume Screener (MVP)

Portfolio Description:
Developed a Python tool that automatically ranks PDF resumes against multiple job descriptions using text processing and TF-IDF similarity. Generates recruiter-friendly Excel reports with color-coded top matches for easy identification of best-fit candidates.

Features:

* Extracts text from PDF resumes.
* Cleans and vectorizes text from resumes and job descriptions.
* Computes similarity scores between each resume and job description.
* Generates:

  * resume_scores_per_jd.csv → Raw scores for data analysis
  * resume_scores_per_jd.xlsx → Recruiter-friendly Excel with color-coded rankings (green = top matches, yellow = medium, red = lower matches)
* Supports multiple job descriptions and recursive resume folders

Project Structure:

resume-screener
├── data
│   ├── resumes              PDF resumes
│   ├── job_descriptions      Text files for JDs
│   ├── resume_scores_per_jd.csv
│   └── resume_scores_per_jd.xlsx
├── src
│   └── resume_screener.py
└── README.md

How to Run:

1. Install dependencies:
   pip install pandas scikit-learn PyPDF2 openpyxl

2. Place resumes (.pdf) and job descriptions (.txt) in the respective folders under data/

3. Run the script:
   python src/resume_screener.py

4. Results will be saved in the data/ folder:

* resume_scores_per_jd.csv → Raw scores
* resume_scores_per_jd.xlsx → Recruiter-friendly Excel report


Future Improvements:

* Integrate NLP libraries like spaCy for advanced skill and keyword extraction.
* Add support for scanned PDFs using OCR to improve text extraction accuracy.
* Enhance ranking metrics with weighted skills and experience matching.
* Build a web interface or dashboard for recruiters to filter and visualize results interactively.


