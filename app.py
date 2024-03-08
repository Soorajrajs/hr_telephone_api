from flask import Flask, request,jsonify
import sqlite3

app=Flask(__name__)

# @app.route('/')
# def home():
#     return "Hello World!"

# @app.route('/<name>')
# def name(name):
#     return f"Hi {name}, Welcome to the page"


def db_connection():
    conn=None
    try:
        conn=sqlite3.connect("telephone.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route('/telephone',methods=['GET','POST'])
def telephone():
    conn=db_connection()
    cursor=conn.cursor()
    if request.method=="GET":
        cursor=conn.execute("SELECT * FROM telephone")
        telephone=[
            dict(id=row[0],name=row[1],number=row[2],company=row[3])
            for  row in cursor.fetchall()
        ]
        if telephone is not None:
            return jsonify(telephone)

    if request.method=='POST':
        new_name=request.form['name']
        new_number=request.form['number']
        new_company=request.form['company']
        sql="""INSERT INTO telephone (name,number,company) VALUES(?,?,?)"""
        cursor.execute(sql,(new_name,new_number,new_company))
        conn.commit()
        return f"Telephone id: {cursor.lastrowid} added successfully."


@app.route('/telephone/<int:id>', methods=["GET","PUT","DELETE"])
def single_contact(id):
    if request.method=='GET':
        for num in telephone_list:
            if num['id']==id:
                return jsonify(num)
            pass
    if request.method=='PUT':
        for num in telephone_list:
            if num['id']==id:   
                num['name']=request.form['name']
                num['number']=request.form['number']
                num['company']=request.form['company']

                updated_telephone={
                    'id':id,
                    'name':num['name'],
                    'number':num['number'],
                    'company':num['company']
                }
                return jsonify(updated_telephone)
    if request.method=='DELETE':
        for index,num in enumerate(telephone_list):
            if num['id'] == id:
                telephone_list.pop(index)
                return jsonify({'message': 'Contact deleted successfully'})
        return jsonify({'message': 'Contact not found'}), 404


if  __name__=='__main__':
    app.run(debug=True)