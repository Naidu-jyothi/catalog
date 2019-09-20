from flask import Flask,redirect,url_for,render_template,request,flash
from flask_mail import Mail,Message
from random import randint
from project_database import Register,Base,user
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_login import LoginManager,login_user,current_user,logout_user,login_required,UserMixin
engine=create_engine('sqlite:///iii.db')
engine=create_engine('sqlite:///iii.db',connect_args={'check_same_thread':False},echo=True)
Base.metadata.bind=engine
DBsession=sessionmaker(bind=engine)
session=DBsession()


app=Flask(__name__)

login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'



app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='jyothinaidu48@gmail.com'
app.config['MAIL_PASSWORD']='naidukumari'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
app.secret_key='abc'

mail=Mail(app)
otp=randint(000000,999999)



@app.route("/sample")

def demo():
	return "welcome to iiit jhfjdh"


@app.route("/demo_msg")
def d():
	return "<h1>hello demo page </h1>"

@app.route("/info/details")
def details():
	return "hello details"


@app.route("/details/<name>/<int:age>/<float:salary>")
def info(name,age,salary):
	return "hello {} age {} and salary {}".format(name,age,salary)

@app.route("/admin")
def admin():
	return "hello admin"

@app.route("/student")
def student():
	return "hello student"

@app.route("/staff")
def staff():
	return "hello staff"

#redirect fn
@app.route("/info/<name>")
def admin_info(name):
	if name=='admin':
		return redirect(url_for('admin'))
	elif name=='student':
		return redirect(url_for('student'))
	elif name=='staff':
		return redirect(url_for('admin'))
	else:
		return "NO URL"

@app.route("/data/<name>/<int:age>/<float:sal>")
def demo_html(name,age,sal):
	return render_template('sample.html',n=name,a=age,s=sal)
#read single record
@app.route("/info-data")
def info_data():
	sno=21
	name='jyo'
	branch='cse'
	dept='trainer'
	return render_template('tast.html',s_no=sno,n=name,br=branch,dp=dept)

#read multiple records
data=[{'sno':123,'name':'jyo','branch':'cse','dept':'trainer'},
{'sno':12,'name':'jyothi','branch':'ece','dept':'dev'}]
@app.route("/dummy_data")
def dummy():
	return render_template('multiple.html',dummy_data=data)
#table
@app.route("/table/<int:num>")
def tabl(num):
	return render_template('table.html',n=num)

#file uploading
@app.route("/file_upload",methods=['GET','POST'])
def file_upload():
	return render_template("file_upload.html")
@app.route("/success",methods=['GET','POST'])
def success():
	if request.method=='POST':
		f=request.files['file']
		f.save(f.filename)
		return render_template("success.html",f_name=f.filename)

#mail otp generation
@app.route("/email", methods=['POST','GET'])
def email_send():
	return render_template("email.html")

@app.route("/email_verify", methods=['POST','GET'])
def verify_email():
	email=request.form['email']
	msg=Message("one time password",sender="jyothinaidu48@gmail.com",recipients=[email])
	msg.body=str(otp)
	mail.send(msg)
	return render_template("v_email.html")

@app.route("/email_success", methods=['POST','GET'])
def success_email():
	user_otp=request.form['otp']
	if otp==int(user_otp):
		return render_template("email_success.html")
	return "In valid otp"

#retrive
#display the data from project database in browser
@app.route("/show")
@login_required
def showData():

	#get the data for other file
	register=session.query(Register).all()
	return render_template('show.html',reg=register)

@app.route("/showit",methods=['POST','GET'])
def addData():
	if request.method=='POST':
		newData=Register(name=request.form['name'],
			surname=request.form['surname'],
			mobile=request.form['mobile'],
			email=request.form['email'],
		    branch=request.form['branch'],
		    role=request.form['role'])
		session.add(newData)
		session.commit()
		flash("new data added.....")
		return redirect(url_for('showData'))

	return render_template('showit.html')



@app.route("/")
def reg(): 
	return render_template('taskreg.html')

@app.route("/reggg")
def reggg(): 
	return render_template('login.html')

@app.route("/edit/<int:register_id>",methods=['POST','GET'])
def editData(register_id):
	editedData=session.query(Register).filter_by(id=register_id).one()
	if request.method=='POST':
			editedData.name=request.form['name']
			editedData.surname=request.form['surname']
			editedData.mobile=request.form['mobile']
			editedData.email=request.form['email']
			editedData.branch=request.form['branch']
			editedData.role=request.form['role']

			session.add(editedData)
			session.commit()
			flash("edited successfully...{}".format(editedData.name))
			return redirect(url_for('showData'))
	else:
		return render_template('edit.html',register=editedData)
#delete
@app.route("/delete/<int:register_id>",methods=['POST','GET'])
def deleteData(register_id):
	deletedData=session.query(Register).filter_by(id=register_id).one()
	if request.method=='POST':
		session.delete(deletedData)
		session.commit()
		flash("deleted successfully...{}".format(deletedData.name))

		return redirect(url_for('showData'))
	else:
		return render_template('delete.html',register=deletedData)

@app.route("/")
def index():
	return render_template('index1.html')

@app.route("/account",methods=['POST','GET'])
@login_required
def account():
	return render_template('account.html')

@app.route("/regg", methods=['POST','GET'])
def regg():
	if request.method=='POST':
		userData=User(name=request.form['name'],
			email=request.form['email'],
			password=request.form['password'])
		session.add(userData)
		session.commit()
		return redirect(url_for('index'))
	else:
		return render_template('registration.html')

@login_required		
@app.route("/login", methods=['POST','GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('showData'))
	try:
		if request.method=='POST':
			user=session.query(User).filter_by(email=request.form['email'],password=request.form['password']).first()
			if user:
				login_user(user)
				return redirect(url_for('showData'))
			else:
				flash("invalid login....")
		else:
			return render_template('login.html',title="login")
	except Exception as e:
		flash("login failed...")
	else:
		return render_template('login.html',title='login')


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('index'))
@login_manager.user_loader
def load_user(user_id):
	return session.query(User).get(int(user_id))

if __name__=="__main__":
    app.run(debug=True)


