from flask import Flask, request,jsonify
import sqlite3

app=Flask(__name__)

def db_connection():
    #return a connection to the database or None if it fails.
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
    conn = db_connection()
    cursor=conn.cursor()
    telephone=None

    if request.method=='GET':
        # Get a specific contact
        cursor.execute("SELECT * FROM telephone WHERE id=?",(id,))
        rows=cursor.fetchall()
        for r in rows:
            telephone=r
        if telephone is not None:
            return jsonify(telephone),200
        else:
            return "Something Wrong",404

    if request.method=='PUT':
        # Update the information of a specific contact
        sql= """UPDATE telephone SET name=?, number=?, company=? WHERE id=?"""
        name=request.form['name']
        number=request.form['number']
        company=request.form['company']

        updated_telephone={
            'id':id,
            'name':name,
            'number':number,
            'company':company
        }
        conn.execute(sql,(name,number,company,id))
        conn.commit()
        return jsonify(updated_telephone)

    if request.method=='DELETE':
        # Delete a specific contact
        sql= "DELETE FROM telephone WHERE id=?"
        conn.execute(sql,(id,))
        conn.commit()
        return f"The telephone record with {id} has been deleted.",200



if  __name__=='__main__':
    app.run(debug=True)