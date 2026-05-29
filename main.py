from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

DB_NAME = "guestbook.db"
app = Flask(__name__)

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    create table if not exists visitors(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   comment TEXT NOT NULL
                    )
    """)
    conn.commit()
    conn.close()

def select():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
        cursor.execute("""select * from visitors""")
    rows = cursor.fetchall()
    print(rows)
    conn.close()
    return rows

def insert(name, comment):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        insert into visitors(name,comment) values(?,?)
    """, (name, comment))
    conn.commit()
    conn.close()

def delete(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        delete from visitors where id=(?)
    """, (id,))
    conn.commit()
    conn.close()

def update(id, name, comment):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        update visitors set name=?, comment=? where id=?
    """, (name, comment, id))
    conn.commit()
    conn.close()

@app.route('/api/visitors', methods=['GET'])
def get_visitors():
    rows = select()
    visitors_data = [
        {"id": row[0], "name": row[1], "comment": row[2]} 
        for row in rows
    ]
    return jsonify(visitors_data)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        comment = request.form['comment']
        insert(name, comment)
        return jsonify({"result": "success", "message": "성공적으로 저장되었습니다."})
        
    visitors_list = select()
    return render_template('ch07.html', visitors=visitors_list)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)