from flask import Flask,redirect,url_for,render_template,request,session
from sec_code import checks_code

valid_pwd = ['12345']

app = Flask(__name__, template_folder = './GUI/')

@app.route('/',methods=["GET",'POST'])
def home():
    if request.method == "GET":
        return render_template('entry_page.html')
    else:
        receivedpwd = request.form['pwd_box']
        if checks_code(receivedpwd):
            print(receivedpwd)
            return redirect(url_for('ahb'))
        else:
            return render_template('entry_page.html')

@app.route('/assistant-head-boy')
def ahb():
    return render_template('voting_page.html')

if __name__ == "__main__":
    app.run(debug=True) 