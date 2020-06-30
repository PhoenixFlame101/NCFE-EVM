from flask import Flask,redirect,url_for,request,render_template,session

app = Flask(__name__)
app.secret_key = 'abc'
admin_pwd = '123'


@app.route('/admin',methods=['GET','POST'])
def admin_page():
    if request.method == 'GET':
        return render_template('admin_landing.html')
    elif request.method =="POST" :
        receivedpwd = request.form['pwd_box']
        if receivedpwd == admin_pwd:
            session['logged'] = True
            print('hi')
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('admin_page'))

@app.route('/dashboard')
def dashboard():
    try:
        if session['logged'] == True:
            return render_template('dashboard.html')
    except:
        return redirect(url_for('admin_page'))

@app.route('/enter_candidate')
def enter_candidate():
    try:
        if session['logged'] == True:
            return render_template('enter_candidate.html')
    except:
        return redirect(url_for('admin_page'))

@app.route('/voting_toggle')
def voting_toggle():
    try:
        if session['logged'] == True:
            return render_template('voting_toggle.html')
    except:
        return redirect(url_for('admin_page'))

@app.route('/settings')
def settings():
    try:
        if session['logged'] == True:
            return render_template('settings.html')
    except:
        return redirect(url_for('admin_page'))

@app.route('/logout')
def logout():
    session.clear()
    return 'hi'#while copying this part should redirect to entry page

if __name__ == "__main__":
    app.run(debug=True)