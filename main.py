from flask import Flask,redirect,url_for,render_template,request,session
import database_linker
import sec_code

house_choice = 'eagle'  #Make sure all the house are in lowercase
candidates = {}
valid = False  # Flask's file variable for showing session validity
voting_started = True  # Status of voting; affects the admin dashboard

app = Flask(__name__,template_folder='./GUI/')
app.secret_key = 'abc'

results = dict([])

#Voting page things
@app.route('/',methods=["GET",'POST'])
def home():
    if request.method == "GET": 
        #This part shows renders the template (get template)
        session["logged"] = False
        return render_template('entry_page.html')
    else:
        #This part whether the security code is valid by asking the database
        receivedpwd = request.form['pwd_box']
        if sec_code.code_is_valid(receivedpwd):
            global valid
            valid = True
            return redirect(url_for('head_boy'))
        else:
            return render_template('entry_page.html')

@app.route('/head-boy',methods=["GET",'POST'])
def head_boy():
    global valid
    try:
        if valid:
            if request.method == "POST":
                #This block adds the voter's choice to the session variable
                head_boy_choice = request.form["head_boy_choice"]
                session["head_boy_choice"] = head_boy_choice
                #This redirects to the next page
                return redirect(url_for('head_girl'))
            elif request.method == "GET":
                #Here the method is the get method
                if len(candidates['head_boy']) == 1:
                    #We dont need to render the page if there is only one candidate
                    if (house_choice+'_vice_captain_choice') in session:
                        #Prevents some one from rendering from the review page
                        return redirect(url_for('final'))
                    else:
                        #If the page hasn't been voted through then it registers the choice
                        session['head_boy_choice'] = candidates['head_boy'][0]
                        return redirect(url_for('head_girl'))
                else:
                    #If there are more than one candidates then it'll load the template
                    return render_template('head_boy.html',d=candidates,house_choice=house_choice)
    except Exception as e:
        #If any error occurs, then the program goes back one page
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
                        #Here the branching of the program takes place with respect to the house chosen by the admin
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
        if session[house_choice+'_vice_captain_choice']:
            if request.method == "GET":
                #Here we render the review page by passing the session dictionary as the parameter
                return render_template('review_page.html',session=dict(session))
            else:
                return redirect(url_for('over'))
    except Exception as e:
        print(e)
        return redirect(url_for(house_choice+'_vice_captain'))

# Admin things
@app.route('/admin',methods=['GET','POST'])
def admin_page():
    if request.method == 'GET':
        return render_template('admin_landing.html')
    elif request.method =="POST" :
        #Validation of the admin password
        receivedpwd = request.form['pwd_box']
        if sec_code.pass_is_valid(receivedpwd):
            session['logged'] = True
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('admin_page'))

@app.route('/dashboard')
def dashboard():
    try:
        if session['logged'] == True:
            #Renders the dashboard only if the admin password is valid
            return render_template('dashboard.html')
    except:
        return redirect(url_for('admin_page'))

@app.route('/show_candidate')
def show_candidate():
    try:
        if session['logged'] == True:
            #This part shows the candidates
            return render_template('show_candidates.html',candidates=candidates,str=str)
    except Exception as  e:
        print(e)
        return redirect(url_for('admin_page'))

@app.route('/voting_settings')
def voting_toggle():
    try:
        if session['logged'] == True:
            return render_template('voting_settings.html',valid=voting_started)
    except:
        return redirect(url_for('admin_page'))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    try:
        global house_choice
        if session['logged'] == True:
            if request.method == "GET":
                return render_template('settings.html',house_choice=house_choice)
            elif request.method == "POST":
                #Here the admin changes the password for the local admin
                #This block confirms the changes
                house_choice = request.form['hc']
                changed_pwd = request.form['changed_pwd']
                if not sec_code.pass_is_valid(changed_pwd):
                    sec_code.pass_set(changed_pwd)
                return redirect(url_for('settings'))
    except:
        return redirect(url_for('admin_page'))

@app.route('/logout')
def logout():
    #Upon logging out the session and come out of the admin page
    session.clear()
    return redirect(url_for("home"))#while copying this part should redirect to entry page

#Functions for the voting toggle function
@app.route('/start_voting')
def start_voting():#This function is called when then admin presses the start voting button
    #database_linker.initializing(#idk what to put here)
    return redirect(url_for("voting_toggle"))

@app.route('/stop_voting')
def stop_voting():#This function is called when the admin presses the stop voting button
    database_linker.results_print()
    return redirect(url_for("voting_toggle"))

@app.route('/generate-code')
def generate_code():#This function is called when the admin presses the generate security codes button
    sec_code.code_print()
    return redirect(url_for('voting_toggle'))

#Final touches
@app.route('/done')
def over():
    #Once it is over, we store the voter's choices and clear the voter's choices by clearing the session variable
    store_result(dict(session))
    session.clear()
    global valid
    valid = False #To express the invalidity of the session of the voter
    return render_template('thank_you.html')

#Non-decorated functions
def store_result(dt):#We can change this to call the function to store the voter's choices
    #here dt is the dictionary
    if 'logged' in dt:
        del dt['logged']
    global results
    database_linker.add_votes_to_db(dict(dt))

def fetch_changed_house_choice():
    hc = request.values.get('house_choice')
    print(hc)

def create_candidates():#Temporary testing function to create the candidates dictionary
    global candidates
    candidates = {'head_boy': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
    'head_girl': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
    'assistant_head_boy': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
    'assistant_head_girl': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
    'cultural_captain': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
    'cultural_vice_captain': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
    'sports_captain': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
    'sports_vice_captain': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
    'kingfisher_captain': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
    'kingfisher_vice_captain': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
    'flamingo_captain': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
    'flamingo_vice_captain': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
    'falcon_captain': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
    'falcon_vice_captain': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
    'eagle_captain': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
    'eagle_vice_captain': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'}}

def t():
    print('hi')
    return redirect(url_for("voting_toggle"))

def start():
    #This is the main method for starting the app
    global candidates
    create_candidates()#temp function to initialize  the candidates variable
    #We fetch the list of candidates from the database and continue
    candidates = database_linker.get_cands_from_db()
    app.run(debug=True)

start()
