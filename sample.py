#pip install werkzeug==0.16.0
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from passlib.hash import sha256_crypt
from functools import wraps
from flask_uploads import UploadSet, configure_uploads, IMAGES
import timeit
import datetime
from flask_mail import Mail, Message
import os
from wtforms.fields.html5 import EmailField
from flask import Flask, request, jsonify, json, make_response, redirect, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta #for time to define how long session is active
from werkzeug.utils import secure_filename
import random 
import string 
import os
import random
from datetime import datetime

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

UPLOAD_FOLDER = '/home/rahul/Desktop/Desbox_flask/static/profile_pic/'


app = Flask(__name__)

app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(days=5)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	

# Config MySQL
mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root@123'
app.config['MYSQL_DB'] = 'Desbox'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize the app for use with this MySQL class
mysql.init_app(app)





@app.route('/')
@app.route('/index')
def index():
	if 'email' in session:
		#form = OrderForm(request.form)
		# Create cursor
		classData_list=[]
		cur = mysql.connection.cursor()
		email=session['email']

		cur.execute("SELECT * FROM profile WHERE email ='"+email+"'") #check user is exist or not
		user = cur.fetchall()

		cur.execute("SELECT classcode FROM join1 WHERE email ='"+email+"'")#now fetch those class that i created or joined both entry are in join1 table
		classcode=cur.fetchall()

		classcode_list=[x['classcode'] for x in classcode]
		print(classcode_list)


		for code in range(0,len(classcode_list)):
			classcode_list[code]
			cur.execute("select classcreate.cid,classcreate.cname,classcreate.subject,classcreate.classcode,classcreate.classpic,classcreate.color,profile.name,profile.pic from classcreate inner join profile on profile.email=classcreate.email and classcode='"+classcode_list[code]+"' ")
			classData=cur.fetchall()
			classData_list.append(classData[0])
		cur.close()
		#print(classData_list)
		return render_template('index.html',user=user[0],classData=classData_list)
	else:
		return redirect(url_for('login'))



@app.route('/classDescription/<string:classcode>', methods=['GET', 'POST'])
def classDescription(classcode):
	if 'email' in session:
		#form = OrderForm(request.form)
		# Create cursor
		cur = mysql.connection.cursor()
		email=session['email']

		cur.execute("SELECT * FROM profile WHERE email ='"+email+"'") #check user is exist or not
		user = cur.fetchall()
		print(classcode)

		cur.execute("SELECT * FROM join1 WHERE classcode ='"+classcode+"' and email='"+email+"' ")#now fetch those class that i created or joined both entry are in join1 table
		CheckUSERClassExist=cur.fetchall()
		# print(len(CheckUSERClassExist))
		if len(CheckUSERClassExist)>0:#it means class exist

			cur.execute("SELECT classcreate.cname,classcreate.section,classcreate.subject,classcreate.marks,classcreate.submittime,classcreate.classpic,classcreate.classcode,classcreate.color,profile.pic from classcreate inner join profile on classcreate.classcode='"+classcode+"' and profile.email = classcreate.email")#now fetch those class that i created or joined both entry are in join1 table
			ClassData=cur.fetchall()
			print(ClassData[0])
			return render_template('classDescription.html',user=user[0],ClassData=ClassData[0])
		else:
			return redirect(url_for('index'))
		#return render_template('404.html',)
	else:
		return redirect(url_for('login'))
    #do your code here
	send_data = {'success': False,"error":"user already Exist...",'id':id}
	return make_response(jsonify(send_data), 200)
    # return render_template("template.html",para1=meter1, para2=meter2)


@app.errorhandler(404) 
# inbuilt function which takes error as parameter 
def not_found(e): 
	if 'email' in session:
		#form = OrderForm(request.form)
		# Create cursor
		cur = mysql.connection.cursor()
		email=session['email']

		cur.execute("SELECT * FROM profile WHERE email ='"+email+"'") #check user is exist or not
		user = cur.fetchall()
		#print(user[0])
		return render_template('404.html',user=user[0])
	else:
		return redirect(url_for('login'))




@app.route('/profile')
def profile():
	if 'email' in session:
		#form = OrderForm(request.form)
		# Create cursor
		cur = mysql.connection.cursor()
		email=session['email']

		cur.execute("SELECT * FROM profile WHERE email ='"+email+"'") #check user is exist or not
		user = cur.fetchall()
		#print(user[0])
		return render_template('profile.html',user=user[0])
	else:
		return redirect(url_for('login'))

@app.route('/blogpost')
def blogpost():
	if 'email' in session:
		#form = OrderForm(request.form)
		# Create cursor
		cur = mysql.connection.cursor()
		email=session['email']

		cur.execute("SELECT * FROM profile WHERE email ='"+email+"'") #check user is exist or not
		user = cur.fetchall()
		#print(user[0])
		return render_template('blogpost.html',user=user[0])
	else:
		return redirect(url_for('login'))

@app.route('/create')
def create():
	if 'email' in session:
		#form = OrderForm(request.form)
		# Create cursor
		cur = mysql.connection.cursor()
		email=session['email']

		cur.execute("SELECT * FROM profile WHERE email ='"+email+"'") #check user is exist or not
		user = cur.fetchall()
		#print(user[0])
		return render_template('create.html',user=user[0])
	else:
		return redirect(url_for('login'))

@app.route('/join')
def join():
	if 'email' in session:
		#form = OrderForm(request.form)
		# Create cursor
		cur = mysql.connection.cursor()
		email=session['email']

		cur.execute("SELECT * FROM profile WHERE email ='"+email+"'") #check user is exist or not
		user = cur.fetchall()
		#print(user[0])
		return render_template('join.html',user=user[0])
	else:
		return redirect(url_for('login'))

@app.route('/tables')
def tables():
	if 'email' in session:
		cur = mysql.connection.cursor()
		email=session['email']

		cur.execute("SELECT * FROM profile WHERE email ='"+email+"'") #check user is exist or not
		user = cur.fetchall()
		#print(user[0])
		return render_template('tables.html',user=user[0])
	else:
		return redirect(url_for('login'))

@app.route('/mail')
def mail():
	if 'email' in session:
		#form = OrderForm(request.form)
		# Create cursor
		cur = mysql.connection.cursor()
		email=session['email']

		cur.execute("SELECT * FROM profile WHERE email ='"+email+"'") #check user is exist or not
		user = cur.fetchall()
		#print(user[0])
		return render_template('mail.html',user=user[0])
	else:
		return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])#this route insert Signup data
def register():
	if 'email' in session:
		return redirect(url_for('index'))
	return render_template('register.html')


@app.route("/login", methods=['GET', 'POST'])#this route insert Signup data

def login():
	if 'email' in session:
		return redirect(url_for('index'))
	return render_template('login.html')



@app.route("/user/register", methods=['GET', 'POST'])#this route insert Signup data
def userRegister():
	try:
		if request.method=='POST':
			#print("register")
			name = str(request.form["name"])
			email = str(request.form["email"])
			password = generate_password_hash(request.form["password"])
			cur = mysql.connection.cursor()
			cur.execute("SELECT * FROM profile WHERE email ='"+email+"'") #check user is exist or not
			user = cur.fetchall()

			if len(user) >0: #if length is greater 1 then user email is exist
				#return render_template("demo.html", title="User already Exist please try again another email")
				send_data = {'success': False,"error":"user already Exist..."}
				return make_response(jsonify(send_data), 200)
				#return redirect(url_for('demo'))

			else:      #user not exist insert detail in database

				pic="http://127.0.0.1:5000/static/profile_pic/user.jpg"
				cur.execute("INSERT INTO profile(name, email, password,about,pic,online) VALUES(%s, %s, %s, %s, %s,%s)",
							(name, email,password,'Not Mention',pic,1))

				# Commit cursor
				mysql.connection.commit()
				#session.permanent = True
				session['email']=email #if i user is exist at login time then create session and redirect to profile
				send_data = {'success': True,"email":email,"name":name}
				return make_response(jsonify(send_data), 200)
				#return redirect(url_for("inspection"))

		else:
			send_data = {'success': False,"error":"please First Register"}
			return make_response(jsonify(send_data), 200)
			#pass
	except Exception as e:
			print(str(e))
			send_data = {'success': False,'error':'Please Sign-in first'}
			return make_response(jsonify(send_data), 200)


@app.route('/user/login', methods=['GET','POST'])
def Userlogin():
	try:
		if request.method == 'POST':
			email = request.form['email']
			password = request.form['password']
			cur = mysql.connection.cursor()
			query = "SELECT password,name,email FROM profile WHERE email ='"+email+"'"
			cur.execute(query)
			data = cur.fetchall()
			#print(data)
			# print(data)
			if len(data) and check_password_hash(data[0]['password'], password):
				#session['user_id'] = data[0][3]

			#create session here----------------------------------------------------------
				session['email']=email
				#print(session)

				#session['logged_in'] = True
				x = '1'
				cur.execute("UPDATE profile SET online=%s WHERE email=%s", (x, email))

			#create session here----------------------------------------------------------
				send_data = {'success': True, 'name': data[0]['name'], 'email': data[0]['email']}
				#print(session)
				mysql.connection.commit()

				return make_response(jsonify(send_data), 200)
			else:
				send_data = {'success': False,'error':'Please Sign-in first'}
				return make_response(jsonify(send_data), 200)
		else:
			send_data = {'success': False,'error':'Please Sign-in first'}
			return make_response(jsonify(send_data), 200)
	except Exception as e:
			print(str(e))
			send_data = {'success': False,'error':'Please Sign-in first'}
			return make_response(jsonify(send_data), 200)

@app.route('/user/profile/update/', methods=['GET','POST'])
def updateProfile():
	try:
		if 'email' in session:
			if request.method == 'POST':
				name= request.form['uname']
				email = request.form['email']
				about = request.form['about']
				cur1 = mysql.connection.cursor()
				cur1.execute("UPDATE profile SET name=%s,about=%s WHERE email=%s", (name,about,email))
				mysql.connection.commit()
				#print("update profile success")
				redirect(url_for('profile'))
			return redirect(url_for('profile'))
			
		else:
			return redirect(url_for('login'))
	except Exception as e:
		return redirect(url_for('profile'))





@app.route('/user/profile/update/profilePic/', methods=['GET','POST'])
def upload_file():
	if 'email' in session:
		email=session['email']
		# check if the post request has the file part
		if 'files[]' not in request.files:
			resp = jsonify({'message' : 'No file part in the request'})
			resp.status_code = 400
			return resp
		
		files = request.files.getlist('files[]')
		
		print(files)
		errors = {}
		success = False
		
		for file in files:
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				directory = ''.join(random.choices(string.ascii_uppercase +string.digits, k = 15))

				path = os.path.join(app.config['UPLOAD_FOLDER'], directory) 
				os.mkdir(path)

				file.save(os.path.join(path, filename))
				#file_update_name=path+'/'+filename

				file_update_name="http://127.0.0.1:5000/static/profile_pic/"+directory+"/"+filename

				cur = mysql.connection.cursor()
				cur.execute("UPDATE profile SET pic=%s WHERE email=%s", (file_update_name,email))
				mysql.connection.commit()

				print("filename=",file_update_name)
				success = True
				redirect(url_for('profile'))
			else:
				errors[file.filename] = 'File type is not allowed'
		
		if success and errors:
			errors['message'] = 'File(s) successfully uploaded'
			resp = jsonify(errors)
			resp.status_code = 206
			return resp
		if success:
			resp = jsonify({'message' : 'Files successfully uploaded'})
			resp.status_code = 201
			return resp
		else:
			resp = jsonify(errors)
			resp.status_code = 400
			return resp
	else:
		send_data = {'success': False,'message':'Please Sign-in first'}
		return make_response(jsonify(send_data), 200)


@app.route('/user/class/create/', methods=['GET','POST'])
def userClassCreate():
	if 'email' in session:
		if request.method == 'POST':
			email=session['email']
			color_list=["badge-dark","badge-info","badge-primary","badge-warning","badge-success","badge-danger","badge-secondary","badge-success","info-color","info-color-dark","secondary-color-dark","default-color-dark","primary-color-dark","secondary-color-dark","secondary-color","default-color"]
			colorName=random.choice(color_list)
			classNo=random.randint(0,22)
			classPic="http://127.0.0.1:5000/static/classpic1/"+str(classNo)+'.jpeg'
			classCode=''.join(random.choices(string.ascii_uppercase +string.digits, k = 6))
			className= request.form['cname']
			Section = request.form['section']
			Subject = request.form['subject']
			Marks = request.form['marks']
			submitTime = request.form['submittime']
			cur = mysql.connection.cursor()
			currentDate=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			cur.execute("INSERT INTO classcreate(email,cname,section,subject,marks,submittime,classcode,classpic,color) VALUES(%s, %s, %s, %s, %s,%s,%s,%s,%s)",(email,className,Section,Subject,Marks,submitTime,classCode,classPic,colorName))
			cur.execute("INSERT INTO join1(email,classcode,dat) VALUES(%s, %s, %s)",(email,classCode,currentDate))
			mysql.connection.commit()
			data={'className':className,'Subject':Subject,'Section':Section,'Marks':Marks,'submitTime':submitTime,'classPic':classPic,'colorName':colorName,'classCode':classCode,'email':email}
			print(data)
			return redirect(url_for('index'))
		return redirect(url_for('profile'))
		
	else:
		return redirect(url_for('login'))


@app.route('/user/class/join/', methods=['GET','POST'])
def userClassJoin():
	if 'email' in session:
		if request.method == 'POST':
			email=session['email']
			classCode = str(request.form["classcode"])
			cur = mysql.connection.cursor()
			cur.execute("SELECT * FROM join1 WHERE email ='"+email+"' and classcode='"+classCode+"'") #check user is exist or not
			classData = cur.fetchall()
			print(classData)
			if len(classData)>0:
				send_data = {'success': False,"error":"class already Exist..."}
				return make_response(jsonify(send_data), 200)
			else:
				#now check that class is exist or not
				cur.execute("select * from join1 where classcode='"+classCode+"'")
				isClassExist=cur.fetchall() #check that class exist or not
				print(isClassExist)
				if len(isClassExist)>0:#class exist insert data
					currentDate=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
					cur.execute("INSERT INTO join1(email,classcode,dat) VALUES(%s,%s,%s)",(email,classCode,currentDate))
					mysql.connection.commit()
					send_data = {'success': True}
					return make_response(jsonify(send_data), 200)
				else:
					return make_response(jsonify({"error":'Class not exist'}))

		return make_response(jsonify({"error":'Class Not Found'}))
	else:
		return redirect(url_for('login'))





@app.route('/logout')
def logout():
	try:
		if 'email' in session:
			# Create cursor
			cur = mysql.connection.cursor()
			email = session['email']
			x = '0'
			cur.execute("UPDATE profile SET online=%s WHERE email=%s", (x, email))
			mysql.connection.commit()
			session.pop("email",None)
			flash('You are logged out', 'success')
			return redirect(url_for('index'))
		return redirect(url_for('login'))
	except Exception as e:
		return redirect(url_for('login'))


if __name__ == '__main__':
	app.run(debug=True,port='5000')
