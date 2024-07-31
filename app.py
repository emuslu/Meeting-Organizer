from flask import Flask, render_template, request, redirect

import sqlite3

app = Flask(__name__)
create_message = ""
update_message = ""

@app.route('/')
def index():
    conn = get_db_connection()
    meetings = conn.execute('SELECT * FROM meetings').fetchall()
    conn.close()
    return render_template('index.html', meetings=meetings, create_message=create_message, update_message=update_message)

@app.route('/create', methods=['POST'])
def meeting():
    if request.method == 'POST':
        global create_message
        try:
            form = request.form
            validate_params(form)
        except Exception as e:
            create_message = str(e)
            return redirect('/')
        create_message = ""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO meetings (subject, date, start_time, end_time, participants) VALUES (?,?,?,?,?)', 
                       [request.form['subject'], request.form['date'], request.form['start_time'], request.form['end_time'], request.form['participants']])
        conn.commit()
        conn.close()
        return redirect('/')
    
@app.route('/meetings/<meeting_id>', methods=['POST'])
def update(meeting_id):
    if request.method == 'POST':
        global update_message
        try:
            form = request.form
            validate_params(form)
        except Exception as e:
            update_message = str(e)
            return redirect('/')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f'UPDATE meetings SET subject = ?, date = ?, start_time = ?, end_time = ?, participants = ? WHERE id = {meeting_id}', 
                       [request.form['subject'], request.form['date'], request.form['start_time'], request.form['end_time'], request.form['participants']])
        conn.commit()
        conn.close()
        return redirect('/')

@app.route('/delete/<meeting_id>', methods=['POST'])
def delete(meeting_id):
    if request.method == 'POST':
        global create_message
        create_message = "Deleted succesfully"
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f'DELETE FROM meetings WHERE id = {meeting_id}')
        conn.commit()
        conn.close()
        return redirect('/')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def validate_params(form):
    for field in form.keys():
        if not form[field] and field != 'subject':
            raise Exception(f"{field} can not be empty!")
    if form['end_time'] <= form ['start_time']:
        raise Exception("End time should be later than start timeé")
    participants = form['participants'].split(',')
    for participant in participants:
        if participant.strip().isalpha() == False:
            raise Exception("Participants list can only contain characters!")