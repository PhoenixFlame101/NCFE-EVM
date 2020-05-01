from flask import Flask,redirect,url_for,render_template,request,session

valid_pwd = ['12345']

app = Flask(__name__)

@app.route('/',methods=["GET",'POST'])
def home():
    if request.method == "GET":
        return render_template('entry_page.html')
    else:
        receivedpwd = request.form['pwd_box']
        if receivedpwd in valid_pwd:
            print(receivedpwd)
            return redirect(url_for('ahb'))
        else:
            return render_template('entry_page.html')

@app.route('/assistant-head-boy')
def ahb():
    return render_template('voting_page.html')

if __name__ == "__main__":
    app.run(debug=True) 