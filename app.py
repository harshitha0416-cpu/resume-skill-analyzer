from flask import Flask, render_template, request
import PyPDF2
import os

app = Flask(__name__)

job_roles = {
    "Python Developer": ["python", "django", "sql", "git"],
    "Web Developer": ["html", "css", "javascript", "react"],
    "Data Analyst": ["python", "excel", "sql", "power bi"],
    "Java Developer": ["java", "spring", "mysql", "git"]
}

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text.lower()

@app.route("/", methods=["GET", "POST"])
def index():
    score = None
    matched = []
    missing = []

    if request.method == "POST":
        role = request.form.get("role")
        file = request.files.get("resume")

        if file and role in job_roles:
            resume_text = extract_text_from_pdf(file)
            required_skills = job_roles[role]

            for skill in required_skills:
                if skill in resume_text:
                    matched.append(skill)
                else:
                    missing.append(skill)

            score = int((len(matched) / len(required_skills)) * 100)

    return render_template(
        "index.html",
        score=score,
        matched=matched,
        missing=missing
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
