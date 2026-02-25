from flask import Flask, render_template, request
import PyPDF2
import webbrowser
import threading

app = Flask(__name__)

# Job role skills database
job_roles = {
    "Python Developer": ["python", "django", "sql", "git"],
    "Web Developer": ["html", "css", "javascript", "react"],
    "Data Analyst": ["python", "excel", "sql", "power bi"],
    "Java Developer": ["java", "spring", "mysql", "git"]
}


# Function to extract text from PDF
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text.lower()


@app.route("/", methods=["GET", "POST"])
def index():
    score = None
    matched = []
    missing = []

    if request.method == "POST":
        role = request.form["role"]
        resume = request.files["resume"]

        if resume:
            resume_text = extract_text_from_pdf(resume)
            required_skills = job_roles[role]

            for skill in required_skills:
                if skill in resume_text:
                    matched.append(skill)
                else:
                    missing.append(skill)

            score = int((len(matched) / len(required_skills)) * 100)

    return render_template("index.html",
                           score=score,
                           matched=matched,
                           missing=missing)


if __name__ == "__main__":
    # Open browser automatically
    threading.Timer(1, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(debug=True, use_reloader=False)