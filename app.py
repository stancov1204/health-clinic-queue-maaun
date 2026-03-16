from flask import Flask, render_template, request, redirect, url_for, flash
from collections import deque
from datetime import datetime, date
from models import Patient

app = Flask(__name__)
app.secret_key = "supersecretkey"   # needed for messages

# Our Queue and list of served patients
waiting_queue = deque()
served_patients = []

@app.route('/')
def index():
    today = date.today()
    seen_today = sum(1 for p in served_patients if p.seen_time and p.seen_time.date() == today)
    
    queue_list = list(waiting_queue)
    
    return render_template('index.html', 
                           queue=queue_list, 
                           seen_today=seen_today)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        complaint = request.form['complaint']
        
        new_patient = Patient(name, age, complaint)
        waiting_queue.append(new_patient)
        
        flash(f"Patient {name} registered successfully!", "success")
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/serve')
def serve():
    if waiting_queue:
        next_patient = waiting_queue.popleft()
        next_patient.seen_time = datetime.now()
        served_patients.append(next_patient)
        
        flash(f"Called patient: {next_patient.name}", "info")
    else:
        flash("No patients waiting!", "danger")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)