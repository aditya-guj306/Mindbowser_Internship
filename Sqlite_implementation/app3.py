from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
import logging
import sqlite3

logging.basicConfig(filename='app.log', level=logging.FATAL, format=f'%(levelname)s:%(name)s:%(asctime)s:%(message)s')

app = Flask(__name__)
api=Api(app)


req_user = reqparse.RequestParser()
req_user.add_argument('name', type=str, help='Name of the user is required', required=True)
req_user.add_argument('age', type=int, help='Age of the user is required', required=True)

req_put_user = reqparse.RequestParser()
req_put_user.add_argument('name', type=str)
req_put_user.add_argument('age', type=int)

class List_User(Resource):
    def get(self):
        con=sqlite3.connect('User.db')
        cur0=con.cursor()
        return cur0.execute('SELECT * FROM user').fetchall()
        

class user(Resource):
    
    def get(self, user_id):
        conn=sqlite3.connect('User.db')
        cur0=conn.cursor()
        print(cur0.execute('SELECT * FROM user WHERE id=?', (user_id,)).fetchone())
        conn.close()
        return 201
    
    def post(self, user_id):
        args = req_user.parse_args()
        conn=sqlite3.connect('User.db')
        cur1=conn.cursor()
        cur1.execute('CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, name VARCHAR(20), age INTEGER)')
        for row in cur1.execute('SELECT id FROM user').fetchall():
            if user_id not in row:
                flag=1
            flag=0    
        if flag==0:
            abort(404, message='User does not exist')
        else:
            cur1.execute('INSERT INTO user (id, name, age) VALUES (?, ?, ?)', (user_id, args['name'], args['age']))
            conn.commit() 
        print(cur1.execute('SELECT * FROM user WHERE id=?', (user_id,)).fetchone())
        conn.close()
        return  201
    
    def put(self, user_id):
        flag=0
        args = req_put_user.parse_args()
        conn=sqlite3.connect('User.db')
        cur2=conn.cursor()
        for row in cur2.execute('SELECT id FROM user').fetchall():
            if user_id not in row:
                flag=1
            flag=0    
        if flag==1:
            abort(404, message='User does not exist')
            
        if args['name']:
            cur2.execute("UPDATE user SET name=? WHERE id=?", (args['name'],user_id))
            conn.commit()
        if args['age']:
            cur2.execute("UPDATE user SET age=? WHERE id=?", (args['age'],user_id))
            conn.commit()   
        print(cur2.execute('SELECT * FROM user WHERE id=?',(user_id,)).fetchone())
        conn.close()    
        return  201
    
    def patch(self, user_id):
        flag=0
        args = req_put_user.parse_args()
        conn=sqlite3.connect('User.db')
        cur3=conn.cursor()
        for row in cur3.execute('SELECT id FROM user').fetchall():
            if user_id not in row:
                flag=1
            flag=0    
        if flag==1:
            abort(404, message='User does not exist')
        else:    
            if args['name']:
                cur3.execute("UPDATE user SET name=? WHERE id=?", (args['name'],user_id))
                conn.commit()    
        print(cur3.execute('SELECT * FROM user WHERE id=?',(user_id,)).fetchone())
        conn.close()    
        return  201 
           

    def head(self, user_id):
        header={'Content-Type':'application/json'}
        return "{{header}}", 200, header
    
    def delete(self,user_id):
        flag=0
        conn=sqlite3.connect('User.db')
        cur4=conn.cursor()
        for row in cur4.execute('SELECT id FROM user').fetchall():
            if user_id not in row:
                flag=1
            flag=0    
        if flag==1:
            abort(404, message='User does not exist')
        else:    
            cur4.execute('DELETE FROM user WHERE id=?', (user_id,))
            conn.commit()
        print(cur4.execute("select * from user").fetchall())
        conn.close()
        return  204
    
    
api.add_resource(user, '/user/<int:user_id>') 
api.add_resource(List_User, '/user')

if __name__ == '__main__':
    app.run(debug=True)
