from flask import Flask,redirect,url_for,render_template,request,session
# from flask.ext.script import Manager
from sec_code import checks_code

app = Flask(__name__, template_folder='./GUI/')
app.secret_key = 'abc'
results = dict([])

@app.route('/',methods=["GET",'POST'])
def home():
	if request.method == "GET":
		return render_template('entry_page.html')
	else:
		receivedpwd = request.form['pwd_box']
		if checks_code(receivedpwd):
			return redirect(url_for('head_boy'))
		else:
			return render_template('entry_page.html')


@app.errorhandler(404)
def URL_not_found(e):
	return redirect(url_for('home'))


@app.route('/head-boy',methods=["GET",'POST'])
def head_boy():
	if request.method == "POST":
		head_boy_choice = request.form["head_boy_choice"]
		session["head_boy_choice"] = head_boy_choice
		return redirect(url_for('head_girl'))
	elif request.method == "GET":
		return render_template('head_boy.html')


@app.route('/head-girl',methods=["GET",'POST'])
def head_girl():
	if request.method == "GET":
		return render_template('head_girl.html')
	elif request.method == "POST":
		head_girl_choice = request.form["head_girl_choice"]
		session["head_girl_choice"] = head_girl_choice
		return redirect(url_for('assistant_head_boy'))


@app.route('/assistant-head-boy',methods=["GET",'POST'])
def assistant_head_boy():
	if request.method == "POST":
		assistant_head_boy_choice = request.form["assistant_head_boy_choice"]
		session["assistant_head_boy_choice"] = assistant_head_boy_choice
		return redirect(url_for('assistant_head_girl'))
	elif request.method == "GET":
		return render_template('assistant_head_boy.html')


@app.route('/assistant-head-girl',methods=["GET",'POST'])
def assistant_head_girl():
	if request.method == "POST":
		assistant_head_girl_choice = request.form["assistant_head_girl_choice"]
		session["assistant_head_girl_choice"] = assistant_head_girl_choice
		return redirect(url_for('cultural_captain'))
	elif request.method == "GET":
		return render_template('assistant_head_girl.html')


@app.route('/cultural-captain',methods=["GET",'POST'])
def cultural_captain():
	if request.method == "POST":
		cultural_captain_choice = request.form["cultural_captain_choice"]
		session["cultural_captain_choice"] = cultural_captain_choice
		return redirect(url_for('cultural_vice_captain'))
	elif request.method == "GET":
		return render_template('cultural_captain.html')


@app.route('/cultural-vice-captain',methods=["GET",'POST'])
def cultural_vice_captain():
	if request.method == "POST":
		cultural_vice_captain_choice = request.form["cultural_vice_captain_choice"]
		session["cultural_vice_captain_choice"] = cultural_vice_captain_choice
		return redirect(url_for('sports_captain'))
	elif request.method == "GET":
		return render_template('cultural_vice_captain.html')


@app.route('/sports-captain',methods=["GET",'POST'])
def sports_captain():
	if request.method == "POST":
		sports_captain_choice = request.form["sports_captain_choice"]
		session["sports_captain_choice"] = sports_captain_choice
		return redirect(url_for('sports_vice_captain'))
	elif request.method == "GET":
		return render_template('sports_captain.html')


@app.route('/sports-vice-captain',methods=["GET",'POST'])
def sports_vice_captain():
	if request.method == "POST":
		sports_vice_captain_choice = request.form["sports_vice_captain_choice"]
		session["sports_vice_captain_choice"] = sports_vice_captain_choice
		return redirect(url_for('kingfisher_captain'))
	elif request.method == "GET":
		return render_template('sports_vice_captain.html')


@app.route('/kingfisher-captain',methods=["GET",'POST'])
def kingfisher_captain():
	if request.method == "POST":
		kingfisher_captain_choice = request.form["kingfisher_captain_choice"]
		session["kingfisher_captain_choice"] = kingfisher_captain_choice
		return redirect(url_for('kingfisher_vice_captain'))
	elif request.method == "GET":
		return render_template('kingfisher_captain.html')


@app.route('/kingfisher-vice-captain',methods=["GET","POST"])
def kingfisher_vice_captain():
	if request.method == "POST":
		kingfisher_vice_captain_choice = request.form["kingfisher_vice_captain_choice"]
		session["kingfisher_vice_captain_choice"] = kingfisher_vice_captain_choice
		return redirect(url_for('final'))
	elif request.method == "GET":
		return render_template('kingfisher_vice_captain.html')


@app.route('/review',methods=['GET','POST'])
def final():
	if request.method == "GET":
		return render_template('review_page.html',session=dict(session))
	else:
		return session # return redirect(url_for('over'))


@app.route('/done')
def over():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')   
	func()
	return 'Thank you'


def start():
	app.run(debug=True)
	return dict(session)
	redirect(url_for('over'))


# start()