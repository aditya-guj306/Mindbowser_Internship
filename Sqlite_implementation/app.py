from flask import Flask, render_template, request, redirect, session
import json, logging

logging.basicConfig(filename='app.log', level=logging.FATAL, format=f'%(levelname)s:%(name)s:%(asctime)s:%(message)s')
app = Flask(__name__)
app.secret_key = 'my_secret_key'
users = {
	'Aditya': 'Pass',
	'Adi': 'password'
}
user1=[]
passw=[]

@app.route('/')
def view_form():
	return render_template('login.html')

@app.route('/handle_get', methods=['GET'])
def handle_get():
	if request.method == 'GET':
		username = request.args['username']
		password = request.args['password']
		print(username, password)
		if username in users and users[username] == password:
			return '<h1>Welcome!!!</h1>'
		else:
			return '<h1>invalid credentials!</h1>'
	else:
		return render_template('login.html')


@app.route('/handle_post', methods=['POST'])
def handle_post():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		print(username, password)
		if username in users and users[username] == password:
			# f=open('credentials.txt','a')
			# f.write(app.logger.info('Logged in successfully'))
			
			return '<h1>Welcome!!!</h1>'
		else:
			
			f=open('credentials.txt','a')
			f.write("{{app.logger.warning('Invalid credentials')}}")
			
			return '<h1>invalid credentials!</h1>'
	else:
		return render_template('login.html')

@app.route('/handle_put', methods=['PUT'])
def handle_put():
	if request.method == 'PUT':
		username = request.form['username']
		password = request.form['password']
		print(username, password)
		if username not in users and users[username] != password:
			# f= open('credentials.txt','a')
			# f.write(username + ' ' + password + '\n')
			user1.update(username)
			passw.update(password)
		else:
			return '<h1>credentials already exists!</h1>'
	else:
		return render_template('login.html')	

if __name__ == '__main__':
	app.run(debug=True)
