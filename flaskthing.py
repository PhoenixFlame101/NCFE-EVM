from flask import Flask,redirect,url_for,render_template,request,session
import os
import json

valid_pwd = ['12345']
admin_pwd = '123'

house_choice = 'eagle'  #Make sure all the house are in lowercase
candidates = {}
current_pwd  = None  #This is the password which the voter entered
valid = False #This is flask's file variable for showing session validity
voting_started = True #This is the variable which controls if voting is going on and shows up accordingly on the admin dashboard

app = Flask(__name__,template_folder='./GUI/')
app.secret_key = 'abc'

results = dict([])

style = ["#000000"]

#Voting page things
@app.route('/',methods=["GET",'POST'])
def home():
    if request.method == "GET":
        session["logged"] = False
        return render_template('entry_page.html')
    else:
        receivedpwd = request.form['pwd_box']
        if receivedpwd in valid_pwd:
            #session['valid'] = True
            global valid
            valid = True
            session['current_pwd'] = receivedpwd
            return redirect(url_for('head_boy'))
        else:
            return render_template('entry_page.html')

@app.route('/head-boy',methods=["GET",'POST'])
def head_boy():
    global valid
    try:
        if valid:
                if request.method == "POST":
                    head_boy_choice = request.form["head_boy_choice"]
                    session["head_boy_choice"] = head_boy_choice
                    return redirect(url_for('head_girl'))
                elif request.method == "GET":
                    if len(candidates['head_boy']) == 1:
                        if (house_choice+'_vice_captain_choice') in session:
                            return redirect(url_for('final'))
                        else:
                            session['head_boy_choice'] = candidates['head_boy'][0]
                            return redirect(url_for('head_girl'))
                    else:
                        return render_template('head_boy.html',d=candidates,house_choice=house_choice)
    except Exception as e:
        print(e)
        return redirect(url_for('home'))

@app.route('/head-girl',methods=["GET",'POST'])
def head_girl():
    try:
        if session["head_boy_choice"]:      
            if request.method == "GET":
                if len(candidates["head_girl"]) == 1:
                    if (house_choice+'_vice_captain_choice') in session:
                        return redirect(url_for('final'))
                    else:
                        session['head_girl_choice'] = candidates["head_girl"][0]
                        return redirect(url_for('assistant_head_boy'))
                else:
                    return render_template('head_girl.html',d=candidates,house_choice=house_choice)
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
                if len(candidates["assistant_head_boy"]) == 1:
                    if (house_choice+'_vice_captain_choice') in session:
                        return redirect(url_for('final'))
                    else:
                        session['assistant_head_boy_choice'] = candidates["assistant_head_boy"][0]
                        return redirect(url_for('assistant_head_girl'))
                else:
                    return render_template('assistant_head_boy.html',d=candidates,house_choice=house_choice)
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
                if len(candidates["assistant_head_girl"]) == 1:
                    if (house_choice+'_vice_captain_choice') in session:
                        return redirect(url_for('final'))
                    else:
                        session['assistant_head_girl_choice'] = candidates["assistant_head_girl"][0]
                        return redirect(url_for('cultural_captain'))
                else:
                    return render_template('assistant_head_girl.html',d=candidates,house_choice=house_choice)
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
                if len(candidates["cultural_captain"]) == 1:
                    if (house_choice+'_vice_captain_choice') in session:
                        return redirect(url_for('final'))
                    else:
                        session['cultural_captain_choice'] = candidates["cultural_captain"][0]
                        return redirect(url_for('cultural_vice_captain'))
                else:
                    return render_template('cultural_captain.html',d=candidates,house_choice=house_choice)
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
                if len(candidates["cultural_vice_captain"]) == 1:
                    if (house_choice+'_vice_captain_choice') in session:
                        return redirect(url_for('final'))
                    else:
                        session['cultural_vice_captain_choice'] = candidates["cultural_vice_captain"][0]
                        return redirect(url_for('sports_captain'))
                else:
                    return render_template('cultural_vice_captain.html',d=candidates,house_choice=house_choice)
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
                if len(candidates["sports_captain"]) == 1:
                    if (house_choice+'_vice_captain_choice') in session:
                        return redirect(url_for('final'))
                    else:
                        session['sports_captain_choice'] = candidates["sports_captain"][0]
                        return redirect(url_for('sports_vice_captain'))
                else:
                    return render_template('sports_captain.html',d=candidates,house_choice=house_choice)
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
                if len(candidates["sports_vice_captain"]) == 1:
                    if (house_choice+'_vice_captain_choice') in session:
                        return redirect(url_for('final'))
                    else:
                        session['sports_vice_captain_choice'] = candidates["sports_vice_captain"][0]
                        return redirect(url_for(house_choice+'_captain'))
                else:
                    return render_template('sports_vice_captain.html',d=candidates,house_choice=house_choice)
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
                if len(candidates["kingfisher_captain"]) == 1:
                    if (house_choice+'_vice_captain_choice') in session:
                        return redirect(url_for('final'))
                    else:
                        session['kingfisher_captain_choice'] = candidates["kingfisher_captain"][0]
                        return redirect(url_for('kingfisher_vice_captain'))
                else:
                    return render_template('kingfisher_captain.html',d=candidates,house_choice=house_choice)
    except:
        return redirect(url_for('sports_vice_captain'))

@app.route('/kingfisher-vice-captain',methods=["GET","POST"])
def kingfisher_vice_captain():
    try:
        if session['kingfisher_captain_choice']:
            if request.method == "POST":
                kingfisher_vice_captain_choice = request.form["kingfisher_vice_captain_choice"]
                session["kingfisher_vice_captain_choice"] = kingfisher_vice_captain_choice
                return redirect(url_for('final'))
            elif request.method == "GET":
                if len(candidates["kingfisher_vice_captain"]) == 1:
                    if (house_choice+'_vice_captain_choice') in session:
                        return redirect(url_for('final'))
                    else:
                        session['kingfisher_vice_captain_choice'] = candidates["kingfisher_vice_captain"][0]
                        return redirect(url_for('final'))
                else:
                    return render_template('kingfisher_vice_captain.html',d=candidates,house_choice=house_choice)
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
                if len(candidates["flamingo_captain"]) == 1:
                    if (house_choice+'_vice_captain_choice') in session:
                        return redirect(url_for('final'))
                    else:
                        session['flamingo_captain_choice'] = candidates["flamingo_captain"][0]
                        return redirect(url_for('flamingo_vice_captain'))
                else:
                    return render_template('flamingo_captain.html',d=candidates,house_choice=house_choice)
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
                if len(candidates["flamingo_vice_captain"]) == 1:
                    if (house_choice+'_vice_captain_choice') in session:
                        return redirect(url_for('final'))
                    else:
                        session['flamingo_vice_captain_choice'] = candidates["flamingo_vice_captain"][0]
                        return redirect(url_for('final'))
                else:
                    return render_template('flamingo_vice_captain.html',d=candidates,house_choice=house_choice)
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
                if len(candidates["falcon_captain"]) == 1:
                    if (house_choice+'_vice_captain_choice') in session:
                        return redirect(url_for('final'))
                    else:
                        session['falcon_captain_choice'] = candidates["falcon_captain"][0]
                        return redirect(url_for('falcon_vice_captain'))
                else:
                    return render_template('falcon_captain.html',d=candidates,house_choice=house_choice)
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
                if len(candidates["falcon_vice_captain"]) == 1:
                    if (house_choice+'_vice_captain_choice') in session:
                        return redirect(url_for('final'))
                    else:
                        session['falcon_vice_captain_choice'] = candidates["falcon_vice_captain"][0]
                        return redirect(url_for('final'))
                else:
                    return render_template('falcon_vice_captain.html',d=candidates,house_choice=house_choice)
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
                if len(candidates["eagle_captain"]) == 1:
                    if (house_choice+'_vice_captain_choice') in session:
                        return redirect(url_for('final'))
                    else:
                        session['eagle_captain_choice'] = candidates["eagle_captain"][0]
                        return redirect(url_for('eagle_vice_captain'))
                else:
                    return render_template('eagle_captain.html',d=candidates,house_choice=house_choice)
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
                if len(candidates["eagle_vice_captain"]) == 1:
                    if (house_choice+'_vice_captain_choice') in session:
                        return redirect(url_for('final'))
                    else:
                        session['eagle_vice_captain_choice'] = candidates["eagle_vice_captain"][0]
                        return redirect(url_for('final'))
                else:
                    return render_template('eagle_vice_captain.html',d=candidates,house_choice=house_choice)
    except:
        return redirect(url_for('eagle_captain'))

@app.route('/review',methods=['GET','POST'])
def final():
    try:
        if session[house_choice+'_vice_captain_choice']:#Change accordingly
            if request.method == "GET":
                '''
                if 'valid' in session:
                    del session["valid"]
                '''
                return render_template('review_page.html',session=dict(session))
            else:
                return redirect(url_for('over'))
    except Exception as e:
        print(e)
        return redirect(url_for(house_choice+'_vice_captain'))
    '''
    try:
        if session[house_choice+'_vice_captain_choice']:#Change accordingly
            if request.method == "GET":
                if 'valid' in session:
                    del session["valid"]
                if 'logged' in session:
                    del session['logged']
                if 'current_pwd' in session:
                    global current_pwd
                    current_pwd = session['current_pwd']
                    del session['current_pwd']
                return render_template('review_page.html',session=dict(session))
            else:
                return redirect(url_for('over'))
    except Exception as e:
        print(e)
        return redirect(url_for(house_choice+'_vice_captain'))
    '''

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
            return render_template('enter_candidate.html',candidates=candidates,str=str)
    except Exception as  e:
        print(e)
        return redirect(url_for('admin_page'))

@app.route('/voting_toggle')
def voting_toggle():
    try:
        if session['logged'] == True:
            return render_template('voting_toggle.html',valid=voting_started)
    except:
        return redirect(url_for('admin_page'))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    try:
        global house_choice,admin_pwd
        if session['logged'] == True:
            if request.method == "GET":
                return render_template('settings.html',house_choice=house_choice)
            elif request.method == "POST":
                house_choice = request.form['hc']
                changed_pwd = request.form['changed_pwd']
                if changed_pwd != admin_pwd:
                    admin_pwd = changed_pwd
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
    global valid
    valid = False
    return redirect(url_for('home'))

#Non-decorated functions
def put_in_file(dt):#We can change this to call the function to send the voter's choices
    #here dt is the dictionary
    with open('jfile.txt', 'w') as json_file:
        try:
            '''
            if dt['valid']:
                dt.pop('valid')
            '''
        except Exception as e:
            print(e)
        finally:
            global current_pwd
            dt['current_pwd'] = current_pwd
            if 'logged' in dt:
                del dt['logged']
            json.dump(dt, json_file)

def fetch_changed_house_choice():
    hc = request.values.get('house_choice')
    print(hc)

def create_candidates():#This is a temporary function just for the sake of creating candidates
    global candidates
    timepass_candidates = ['Sanjay Chidambaram','Parthiv',"Divy","Joe"]
    posts = ['head_boy','head_girl','assistant_head_boy','assistant_head_girl','cultural_captain','cultural_vice_captain','sports_captain','sports_vice_captain','kingfisher_captain','kingfisher_vice_captain','flamingo_captain','flamingo_vice_captain','falcon_captain','falcon_vice_captain','eagle_captain','eagle_vice_captain']
    for x in posts:
        candidates[x]  = timepass_candidates
        #candidates[x] = ['Chumlee']
    #candidates['head_boy'] = ['Vivin']

def start(candidate_dict):
    #if __name__ == "__main__":
    global candidates
    create_candidates()
    candidates = candidate_dict
    app.run(debug=True)

start(candidates)