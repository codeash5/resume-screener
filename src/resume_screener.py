import os
import re
import PyPDF2
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl.utils.dataframe import dataframe_to_rows

# ---------- CONFIG ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def find_folder(folder_name):
    path_1 = os.path.join(BASE_DIR, "data", folder_name)
    if os.path.exists(path_1):
        return path_1
    path_2 = os.path.join(os.path.dirname(BASE_DIR), "data", folder_name)
    if os.path.exists(path_2):
        return path_2
    return None

RESUMES_FOLDER = find_folder("resumes")
JOBS_FOLDER = find_folder("job_descriptions")
TOP_N = 5  # Top matches per job

# ---------- Utility functions ----------
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f" Error reading {pdf_path}: {e}")
    return text

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

# ---------- Load resumes (recursive) ----------
def load_resumes():
    resumes = {}
    if not RESUMES_FOLDER:
        print(" Could not find 'resumes' folder")
        return resumes

    print(f" Searching for PDFs in {RESUMES_FOLDER} (recursive)...")
    for root, _, files in os.walk(RESUMES_FOLDER):
        for file in files:
            if file.lower().endswith(".pdf"):
                path = os.path.join(root, file)
                relative_path = os.path.relpath(path, RESUMES_FOLDER)
                text = clean_text(extract_text_from_pdf(path))
                if text.strip():
                    resumes[relative_path] = text
                else:
                    print(f"⚠️ Skipping {relative_path} (no text extracted)")

    if resumes:
        print(f" Loaded {len(resumes)} resumes:")
        for r in resumes.keys():
            print(f"   - {r}")
    else:
        print(f" No valid resumes found in {RESUMES_FOLDER}")
    return resumes

# ---------- Load job descriptions ----------
def load_job_descriptions():
    jobs = {}
    if not JOBS_FOLDER:
        print(" Could not find 'job_descriptions' folder")
        return jobs

    files = [f for f in os.listdir(JOBS_FOLDER) if f.lower().endswith(".txt")]
    for file in files:
        path = os.path.join(JOBS_FOLDER, file)
        with open(path, 'r', encoding='utf-8') as f:
            jobs[file] = clean_text(f.read())

    if jobs:
        print(f" Loaded {len(jobs)} job descriptions:")
        for j in jobs.keys():
            print(f"   - {j}")
    else:
        print(f" No job descriptions found in {JOBS_FOLDER}")
    return jobs

# ---------- Matching function ----------
def match_resumes_to_jobs(resumes, jobs):
    all_results = []
    for job_name, job_text in jobs.items():
        print(f"\n Job: {job_name}")
        all_texts = [job_text] + list(resumes.values())
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        ranked = sorted(zip(resumes.keys(), similarities), key=lambda x: x[1], reverse=True)
        for resume_name, score in ranked[:TOP_N]:
            print(f"   {resume_name} → {score:.2f}")
        for rank, (resume_name, score) in enumerate(ranked, start=1):
            all_results.append([
                job_name, resume_name, round(score,4), round(score*100,2), rank
            ])
    return all_results

# ---------- Save Excel ----------
def save_to_excel(df, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Resume Scores"

    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)

    green = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    yellow = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
    red = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")

    for jd in df["Job Description"].unique():
        jd_rows = [i+2 for i, val in enumerate(df["Job Description"]) if val == jd]
        jd_ranks = df[df["Job Description"]==jd]["Rank"].tolist()
        for i, rank in zip(jd_rows, jd_ranks):
            cell = ws.cell(row=i, column=5)  # Match % column
            if rank <=2:
                cell.fill = green
            elif rank <=5:
                cell.fill = yellow
            else:
                cell.fill = red

    for col in ws.columns:
        max_len = max(len(str(cell.value)) if cell.value else 0 for cell in col) + 2
        ws.column_dimensions[col[0].column_letter].width = max_len

    wb.save(path)
    print(f" Excel saved to: {path}")

# ---------- Main ----------
if __name__ == "__main__":
    print(f" Current working directory: {os.getcwd()}")
    print(f" Resumes folder path: {RESUMES_FOLDER or '❌ Not found'}")
    print(f" Jobs folder path: {JOBS_FOLDER or '❌ Not found'}")

    resumes = load_resumes()
    jobs = load_job_descriptions()

    if not resumes or not jobs:
        print(" Cannot proceed — missing resumes or job descriptions.")
    else:
        results = match_resumes_to_jobs(resumes, jobs)
        df = pd.DataFrame(results, columns=[
            "Job Description","Resume Filename","Similarity Score","Match %","Rank"
        ])
        csv_path = os.path.join(os.path.dirname(BASE_DIR), "data", "resume_scores_per_jd.csv")
        df.to_csv(csv_path, index=False)
        print(f" CSV saved to: {csv_path}")
        excel_path = os.path.join(os.path.dirname(BASE_DIR), "data", "resume_scores_per_jd.xlsx")
        save_to_excel(df, excel_path)




