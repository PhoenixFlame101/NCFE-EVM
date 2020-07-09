from flask import Flask,redirect,url_for,render_template,request,session
import os
import json

valid_pwd = ['12345']
admin_pwd = '123'
house_choice = 'flamingo'  #Make sure all the house are in lowercase

app = Flask(__name__)
app.secret_key = 'abc'
results = dict([])

style = ["#000000"]

#Voting page things
@app.route('/',methods=["GET",'POST'])
def home():
    if request.method == "GET":
        return render_template('entry_page.html')
    else:
        receivedpwd = request.form['pwd_box']
        if receivedpwd in valid_pwd:
            session['valid'] = True
            return redirect(url_for('head_boy'))
        else:
            return render_template('entry_page.html')

@app.route('/head-boy',methods=["GET",'POST'])
def head_boy():
    try:
        if session['valid']:
                if request.method == "POST":
                    head_boy_choice = request.form["head_boy_choice"]
                    session["head_boy_choice"] = head_boy_choice
                    return redirect(url_for('head_girl'))
                elif request.method == "GET":
                    return render_template('head_boy.html')
    except:
        return redirect(url_for('home'))

@app.route('/head-girl',methods=["GET",'POST'])
def head_girl():
    try:
        if session["head_boy_choice"]:      
            if request.method == "GET":
                return render_template('head_girl.html')
            elif request.method == "POST":
                head_girl_choice = request.form["head_girl_choice"]
                session["head_girl_choice"] = head_girl_choice
                return redirect(url_for('assistant_head_boy'))
    except:
        return redirect(url_for('head_boy'))

@app.route('/assistant-head-boy',methods=["GET",'POST'])
def assistant_head_boy():
    try:
        if session["head_girl_choice"]:
            if request.method == "POST":
                assistant_head_boy_choice = request.form["assistant_head_boy_choice"]
                session["assistant_head_boy_choice"] = assistant_head_boy_choice
                return redirect(url_for('assistant_head_girl'))
            elif request.method == "GET":
                return render_template('assistant_head_boy.html')
    except:
        return redirect(url_for('head_girl'))

@app.route('/assistant-head-girl',methods=["GET",'POST'])
def assistant_head_girl():
    try:
        if session["assistant_head_boy_choice"]:        
            if request.method == "POST":
                assistant_head_girl_choice = request.form["assistant_head_girl_choice"]
                session["assistant_head_girl_choice"] = assistant_head_girl_choice
                return redirect(url_for('cultural_captain'))
            elif request.method == "GET":
                return render_template('assistant_head_girl.html')
    except:
        return redirect(url_for('assistant_head_boy'))

@app.route('/cultural-captain',methods=["GET",'POST'])
def cultural_captain():
    try:
         if session['assistant_head_girl_choice']:
            if request.method == "POST":
                cultural_captain_choice = request.form["cultural_captain_choice"]
                session["cultural_captain_choice"] = cultural_captain_choice
                return redirect(url_for('cultural_vice_captain'))
            elif request.method == "GET":
                return render_template('cultural_captain.html')
    except :
        return redirect(url_for('assistant_head_girl'))

@app.route('/cultural-vice-captain',methods=["GET",'POST'])
def cultural_vice_captain():
    try:
        if session['cultural_captain_choice']:
            if request.method == "POST":
                cultural_vice_captain_choice = request.form["cultural_vice_captain_choice"]
                session["cultural_vice_captain_choice"] = cultural_vice_captain_choice
                return redirect(url_for('sports_captain'))
            elif request.method == "GET":
                return render_template('cultural_vice_captain.html')
    except:
        return redirect(url_for('cultural_captain'))

@app.route('/sports-captain',methods=["GET",'POST'])
def sports_captain():
    try:
        if session['cultural_vice_captain_choice']:       
            if request.method == "POST":
                sports_captain_choice = request.form["sports_captain_choice"]
                session["sports_captain_choice"] = sports_captain_choice
                return redirect(url_for('sports_vice_captain'))
            elif request.method == "GET":
                return render_template('sports_captain.html')
    except:
        return  redirect(url_for('cultural_vice_captain'))

@app.route('/sports-vice-captain',methods=["GET",'POST'])
def sports_vice_captain():
    try:
        if session['sports_captain_choice']:
            if request.method == "POST":
                sports_vice_captain_choice = request.form["sports_vice_captain_choice"]
                session["sports_vice_captain_choice"] = sports_vice_captain_choice

                return redirect(url_for(house_choice+'_captain'))
            elif request.method == "GET":
                return render_template('sports_vice_captain.html')
    except:
        return redirect(url_for('sports_captain'))

#The house functions
@app.route('/kingfisher-captain',methods=["GET",'POST'])
def kingfisher_captain():
    try:
        if session['sports_vice_captain_choice']:
            if request.method == "POST":
                kingfisher_captain_choice = request.form["kingfisher_captain_choice"]
                session["kingfisher_captain_choice"] = kingfisher_captain_choice
                return redirect(url_for('kingfisher_vice_captain'))
            elif request.method == "GET":
                return render_template('kingfisher_captain.html')
    except:
        return redirect(url_for('sports_vice_captain'))

@app.route('/kingfisher-vice-captain',methods=["GET","POST"])
def kingfisher_vice_captain():
    try:
        if session['kingfisher_captain_choice']:
            if request.method == "POST":
                kingfisher_vice_captain_choice = request.form["kingfisher_vice_captain_choice"]
                session["kingfisher_vice_captain_choice"] = kingfisher_vice_captain_choice
                print(kingfisher_vice_captain_choice)
                return redirect(url_for('final'))
            elif request.method == "GET":
                return render_template('kingfisher_vice_captain.html')
    except:
        return redirect(url_for('kingfisher_captain'))

@app.route('/flamingo-captain',methods=["GET",'POST'])
def flamingo_captain():
    try:
        if session['sports_vice_captain_choice']:
            if request.method == "POST":
                flamingo_captain_choice = request.form["flamingo_captain_choice"]
                session["flamingo_captain_choice"] = flamingo_captain_choice
                return redirect(url_for('flamingo_vice_captain'))
            elif request.method == "GET":
                return render_template('flamingo_captain.html')
    except:
        return redirect(url_for('sports_vice_captain'))

@app.route('/flamingo-vice-captain',methods=["GET",'POST'])
def flamingo_vice_captain():
    try:
        if session['flamingo_captain_choice']:
            if request.method == "POST":
                flamingo_vice_captain_choice = request.form["flamingo_vice_captain_choice"]
                session["flamingo_vice_captain_choice"] = flamingo_vice_captain_choice
                return redirect(url_for('final'))
            elif request.method == "GET":
                return render_template('flamingo_vice_captain.html')
    except:
        return redirect(url_for('flamingo_captain'))

@app.route('/falcon-captain',methods=["GET",'POST'])
def falcon_captain():
    try:
        if session['sports_vice_captain_choice']:
            if request.method == "POST":
                falcon_captain_choice = request.form["falcon_captain_choice"]
                session["falcon_captain_choice"] = falcon_captain_choice
                return redirect(url_for('falcon_vice_captain'))
            elif request.method == "GET":
                return render_template('falcon_captain.html')
    except:
        return redirect(url_for('sports_vice_captain'))

@app.route('/falcon-vice-captain',methods=["GET",'POST'])
def falcon_vice_captain():
    try:
        if session['falcon_captain_choice']:
            if request.method == "POST":
                falcon_vice_captain_choice = request.form["falcon_vice_captain_choice"]
                session["falcon_vice_captain_choice"] = falcon_vice_captain_choice
                return redirect(url_for('final'))
            elif request.method == "GET":
                return render_template('falcon_vice_captain.html')
    except:
        return redirect(url_for('falcon_captain'))

@app.route('/eagle-captain',methods=["GET",'POST'])
def eagle_captain():
    try:
        if session['sports_vice_captain_choice']:
            if request.method == "POST":
                eagle_captain_choice = request.form["eagle_captain_choice"]
                session["eagle_captain_choice"] = eagle_captain_choice
                return redirect(url_for('eagle_vice_captain'))
            elif request.method == "GET":
                return render_template('eagle_captain.html')
    except:
        return redirect(url_for('sports_vice_captain'))

@app.route('/eagle-vice-captain',methods=["GET",'POST'])
def eagle_vice_captain():
    try:
        if session['eagle_captain_choice']:
            if request.method == "POST":
                eagle_vice_captain_choice = request.form["eagle_vice_captain_choice"]
                session["eagle_vice_captain_choice"] = eagle_vice_captain_choice
                return redirect(url_for('final'))
            elif request.method == "GET":
                return render_template('eagle_vice_captain.html')
    except:
        return redirect(url_for('eagle_captain'))

@app.route('/review',methods=['GET','POST'])
def final():
    try:
        if session[house_choice+'_vice_captain_choice']:#Change accordingly
            if request.method == "GET":
                if 'valid' in session:
                    del session["valid"]
                return render_template('review_page.html',session=dict(session))
            else:
                return redirect(url_for('over'))
    except Exception as e:
        print(e)
        return redirect(url_for(house_choice+'_vice_captain'))

#Admin things

@app.route('/admin',methods=['GET','POST'])
def admin_page():
    if request.method == 'GET':
        return render_template('admin_landing.html')
    elif request.method =="POST" :
        receivedpwd = request.form['pwd_box']
        if receivedpwd == admin_pwd:
            session['logged'] = True
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

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    try:
        global house_choice
        if session['logged'] == True:
            if request.method == "GET":
                print(house_choice)
                return render_template('settings.html',house_choice=house_choice)
            elif request.method == "POST":
                house_choice = request.form['hc']
                return redirect(url_for('settings'))
    except:
        return redirect(url_for('admin_page'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("home"))#while copying this part should redirect to entry page

#Final touches
@app.route('/done')
def over():
    put_in_file(dict(session))
    '''
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')   
    func()
    '''
    session.clear()
    return redirect(url_for('home'))

#Non-decorated functions
def put_in_file(dt):
    #here dt is the dictionary
    with open('jfile.txt', 'w') as json_file:
        try:
            if dt['valid']:
                dt.pop('valid')
        except:
            pass
        finally:
            json.dump(dt, json_file)

def fetch_changed_house_choice():
    hc = request.values.get('house_choice')
    print(hc)

def start():
    #if __name__ == "__main__":
    app.run(debug=True)

start()