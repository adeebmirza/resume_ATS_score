from flask import Flask, render_template, request
from resume_parser import parse_resume, calculate_ats_score

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        resume = request.files['resume']
        job_description = request.form['job_description']
        
        # Parse resume and job description
        resume_text = parse_resume(resume)
        ats_score = calculate_ats_score(resume_text, job_description)
        
        return render_template('index.html', score=ats_score)
    
    return render_template('index.html', score=None)

if __name__ == "__main__":
    app.run(debug=True)
