from flask import Flask, render_template, request,jsonify
import sqlite3

DB_NAME='commentdb'
app=Flask(__name__)
def create_table():
    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()
    cursor.execute("""
    create table if not exists commenttbl(
                    name text not null,
                    comment text not null
                    )
    """)
    conn.commit()
    conn.close()
def select():
    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()
    cursor.execute("""select * from commenttbl""")
    rows=cursor.fetchall()
    print(rows)
    conn.commit()
    conn.close()
    return rows
def insert(name,comment):
    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()
    cursor.execute("""
        insert into commenttbl(name,comment) values(?,?)
""",(name,comment))
    conn.commit()
    conn.close()
def delete(id):
    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()
    cursor.execute("""
        delete from commenttbl where id=(?)
""",(id,))
    conn.commit()
    conn.close()
def update(id,name,age):
    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()
    cursor.execute("""
        update commenttbl set name=?, age=? where id=?
""",(name,age,id))
    conn.commit()
    conn.close()
@app.route('/')
def main():
    return render_template('ch07.html')
@app.route('/api/visit',methods=['POST'])
def visit():
    data=request.get_json()
    insert(data['name'],data['comment'])
    return jsonify({'status':'success','message':'삽입 완료'})
@app.route('/api/visitors',methods=['GET'])
def visitors():
    rows=select()
    list=[]
    for row in rows:
        name,comment=row
        list.append({'name':name,'comment':comment})
    return list

if __name__=='__main__':
    create_table()
    app.run()