from flask import Flask, request, render_template, jsonify, Response
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS data
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  date_time TEXT,
                  v_code TEXT,
                  raw TEXT,
                  cadet TEXT)''')
    conn.commit()
    conn.close()

@app.route('/', methods= ['GET', "POST"])
def index():
    if request.method == 'GET':
        init_db()
        return render_template('index.html')
    elif request.method == 'POST':
        data = request.json
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("INSERT INTO data (date_time, v_code, raw, cadet) VALUES (?, ?, ?, ?)",
                  (data['date_time'], data['v_code'], data['raw'], data['cadet']))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})

@app.route('/stream')
def stream():
    def event_stream():
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        last_id = 0
        while True:
            c.execute("SELECT * FROM data WHERE id > ? ORDER BY id DESC LIMIT 1", (last_id,))
            new_data = c.fetchone()
            if new_data:
                last_id = new_data[0]
                yield f"data: {json.dumps(dict(zip(['id', 'date_time', 'v_code', 'raw', 'cadet'], new_data)))}\n\n"
    return Response(event_stream(), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)