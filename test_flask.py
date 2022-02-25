from flask import Flask,render_template,request,redirect,url_for
from flask import session
import json
import os
import time
app=Flask(__name__)
@app.route('/',methods=['POST','GET'])
def index():
	if request.method =='POST':
		if request.values['send']=='送出':
			return render_template('1234.html',name=request.values['user'])
	return render_template('1234.html',name="")
app.secret_key = b'ViOsQyvBC#W&oaFFl%M4'
@app.route('/register',methods=['POST','GET'])
@app.route('/register',methods=['POST','GET'])
def register():
	with open('./member.json','r') as file_object:
		member = json.load(file_object)
	if request.method=='POST':
		if request.values['send']=='送出':
			if request.values['userid'] in member:
				for find in member:
					if member[find]['nick']==request.values['username']:
						return render_template('register.html',alert='this account and nickname are used.')
				return render_template('register.html',alert='this account is used.',nick=request.values['username'])
			else:
				for find in member:
					if member[find]['nick']==request.values['username']:
						return render_template('register.html',alert='this nickname are used.',id=request.values['userid'],pw=request.values['userpw'])
				member[request.values['userid']]={'password':request.values['userpw'],'nick':request.values['username']}
				with open('./member.json','w') as f:
					json.dump(member, f)
				return render_template('index.html')
	return render_template('register.html')
@app.route('/login',methods=['GET','POST'])
def login():

	if request.method== 'POST' :
		with open('./member.json','r') as file_object:
			member = json.load(file_object)

		if request.values['userid'] in member:
			if member[request.values['userid']]['password']==request.values['userpw']:
				session['username']=request.values['userid']
				return redirect ( url_for ( 'index' ))
			else:
				return render_template('login.html',alert="Your password is wrong, please check again!")
		else:
			return render_template('login.html',alert="Your account is unregistered.")
	return render_template('login.html')
@app.route('/logout',methods=['GET','POST'])
def logout ():
	if request.method=='POST':
		if request.values['send']=='確定':
			session.pop('username',None)
		return redirect(url_for('index'))
	basepath = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
	os.mkdir(os.path.join(basepath, request.values['userid']))
	return render_template('logout.html')


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
	basepath = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
	dirs = os.listdir(os.path.join(basepath, session.get('username')))
	dirs.insert(0, 'New Folder')
	dirs.insert(0, 'Not Choose')

	if request.method == 'POST':
		flist = request.files.getlist("file[]")

		for f in flist:
			format = f.filename[f.filename.index('.'):]
			fileName = time.time()
			if format in ('.jpg', '.png', '.jpeg', '.HEIC', '.jfif'):
				format = '.jpg'
			else:
				format = '.mp4'

			if request.values['folder'] == '0':
				return render_template('uploads.html', alert='Please choose a folder or creat a folder', dirs=dirs)

			elif request.values['folder'] == '1':
				if not os.path.isdir(os.path.join(basepath, session.get('username'), request.values['foldername'])):
					os.mkdir(os.path.join(basepath, session.get('username'), request.values['foldername']))
					os.mkdir(os.path.join(basepath, session.get('username'), request.values['foldername'], 'video'))
					os.mkdir(os.path.join(basepath, session.get('username'), request.values['foldername'], 'photo'))

				if format == '.mp4':
					upload_path = os.path.join(basepath, session.get('username'), request.values['foldername'], 'video',
											   str(fileName).replace('.', '') + str(format))
				else:
					upload_path = os.path.join(basepath, session.get('username'), request.values['foldername'], 'photo',
											   str(fileName).replace('.', '') + str(format))

			else:
				if format == '.mp4':
					upload_path = os.path.join(basepath, session.get('username'), dirs[int(request.values['folder'])],
											   'video', str(fileName).replace('.', '') + str(format))
				else:
					upload_path = os.path.join(basepath, session.get('username'), dirs[int(request.values['folder'])],
											   'photo', str(fileName).replace('.', '') + str(format))

			f.save(upload_path)

		return redirect(url_for('upload'))
	return render_template('uploads.html', dirs=dirs)


if __name__ == '__main__':
	app.run(host='0.0.0.0',port='5000',debug=True)
