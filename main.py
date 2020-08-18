from flask import Flask,redirect,url_for,render_template,request,session,send_from_directory
import database_linker
import sec_code
import os,sys

house_choice = 'eagle'  #Make sure all the house are in lowercase
candidates = {}
valid = False  # Flask's file variable for showing session validity
voting_started = True  # Status of voting; affects the admin dashboard
cur_posts =[] #Shows which posts are there for voting

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
            return redirect(url_for('invalid_code'))

@app.route('/invalid_code')
def invalid_code():
    return render_template('invalid_page.html')

@app.route('/head-boy',methods=["GET",'POST'])
def head_boy():
    global valid
    try:
        if valid:
            if request.method == "POST":
                #This block adds the voter's choice to the session variable
                head_boy_choice = request.form["head_boy_choice"]
                session["head_boy_choice"] = head_boy_choice
                if (cur_posts[-1]+'_choice') not in session:
                    #This redirects to the next page
                    return redirect(url_for('head_girl'))
                else:
                    return redirect(url_for('final'))

            elif request.method == "GET":
                p = 'head_boy'
                pc = p+"_choice"
                next_p = 'head_girl'
                if p in candidates:#It checks if the post exists
                    if len(candidates[p])==1:#If there is one candidate
                        if (cur_posts[-1]+'_choice') not in session:#The part makes a temporary storage of candidate show that it doesn't show up on the review page
                            session[pc] = 'DNE'
                            return redirect(url_for(next_p))#This part takes them to the next page
                        else:
                            return redirect("final")#This part prevents them from coming from the review page to see
                    else:
                        pname = "".join([x+' ' for x in p.split('_')])
                        lastthere = (cur_posts[-1]+'_choice') in session
                        return render_template('gen_page.html',p='head_boy',pname=pname,d=candidates,cur_posts=cur_posts,lastthere=lastthere,house_choice=house_choice,prev_post=prev_post)
                        #return render_template(p+'.html',d=candidates,house_choice=house_choice,prev_post=prev_post)#If all is normal then the template gets loaded
                else:
                    session[pc] = 'DNE'
                    return redirect(url_for(next_p))
        else:
            return redirect(url_for('home'))

    except Exception as e:
        #If any error occurs, then the program goes back one page
        print(e)
        return redirect(url_for('home'))

@app.route('/head-girl',methods=["GET",'POST'])
def head_girl():
    try:
        if session["head_boy_choice"]:
            if request.method == "GET":
                p = 'head_girl'
                pc = p+"_choice"
                next_p = 'assistant_head_boy'
                if p in candidates:
                    if len(candidates[p])==1:
                        if (cur_posts[-1]+'_choice') not in session:
                            session[pc] = 'DNE'
                            return redirect(url_for(next_p))
                        else:
                            return redirect(url_for("final"))
                    else:
                        pname = "".join([x+' ' for x in p.split('_')])
                        lastthere = (cur_posts[-1]+'_choice') in session
                        return render_template('gen_page.html',p='head_girl',pname=pname,d=candidates,cur_posts=cur_posts,lastthere=lastthere,house_choice=house_choice,prev_post=prev_post)
                else:
                    session[pc] = 'DNE'
                    return redirect(url_for(next_p))
            elif request.method == "POST":
                head_girl_choice = request.form["head_girl_choice"]
                session["head_girl_choice"] = head_girl_choice
                if (cur_posts[-1]+'_choice') not in session:
                    return redirect(url_for('assistant_head_boy'))
                else:
                    return redirect(url_for('final'))
    except Exception as e:
        print(e)
        return redirect(url_for('head_boy'))

@app.route('/assistant-head-boy',methods=["GET",'POST'])
def assistant_head_boy():
    try:
        if session["head_girl_choice"]:
            if request.method == "POST":
                assistant_head_boy_choice = request.form["assistant_head_boy_choice"]
                session["assistant_head_boy_choice"] = assistant_head_boy_choice
                if (cur_posts[-1]+'_choice') not in session:
                    #This redirects to the next page
                    return redirect(url_for('assistant_head_girl'))
                else:
                    return redirect(url_for('final'))
            elif request.method == "GET":
                p = 'assistant_head_boy'
                pc = p+"_choice"
                next_p = 'assistant_head_girl'
                if p in candidates:
                    if len(candidates[p])==1:
                        if (cur_posts[-1]+'_choice') not in session:
                            session[pc] = 'DNE'
                            return redirect(url_for(next_p))
                        else:
                            return redirect("final")
                    else:
                        pname = "".join([x+' ' for x in p.split('_')])
                        lastthere = (cur_posts[-1]+'_choice') in session
                        return render_template('gen_page.html',p='assistant_head_boy',pname=pname,d=candidates,cur_posts=cur_posts,lastthere=lastthere,house_choice=house_choice,prev_post=prev_post)
                else:
                    session[pc] = 'DNE'
                    return redirect(url_for(next_p))
    except Exception as e:
        print(e)
        return redirect(url_for('head_girl'))

@app.route('/assistant-head-girl',methods=["GET",'POST'])
def assistant_head_girl():
    try:
        if session["assistant_head_boy_choice"]:
            if request.method == "POST":
                assistant_head_girl_choice = request.form["assistant_head_girl_choice"]
                session["assistant_head_girl_choice"] = assistant_head_girl_choice
                if (cur_posts[-1]+'_choice') not in session:
                    #This redirects to the next page
                    return redirect(url_for('cultural_captain'))
                else:
                    return redirect(url_for('final'))
            elif request.method == "GET":
                p = 'assistant_head_girl'
                pc = p+"_choice"
                next_p = 'cultural_captain'
                if p in candidates:
                    if len(candidates[p])==1:
                        if (cur_posts[-1]+'_choice') not in session:
                            session[pc] = 'DNE'
                            return redirect(url_for(next_p))
                        else:
                            return redirect("final")
                    else:
                        pname = "".join([x+' ' for x in p.split('_')])
                        lastthere = (cur_posts[-1]+'_choice') in session
                        return render_template('gen_page.html',p='assistant_head_girl',pname=pname,d=candidates,cur_posts=cur_posts,lastthere=lastthere,house_choice=house_choice,prev_post=prev_post)
                else:
                    session[pc] = 'DNE'
                    return redirect(url_for(next_p))
    except Exception as e:
        print(e)
        return redirect(url_for('assistant_head_boy'))

@app.route('/cultural-captain',methods=["GET",'POST'])
def cultural_captain():
    try:
         if session['assistant_head_girl_choice']:
            if request.method == "POST":
                cultural_captain_choice = request.form["cultural_captain_choice"]
                session["cultural_captain_choice"] = cultural_captain_choice
                if (cur_posts[-1]+'_choice') not in session:
                    return redirect(url_for('cultural_vice_captain'))
                else:
                    return redirect(url_for('final'))

            elif request.method == "GET":
                p = 'cultural_captain'
                pc = p+"_choice"
                next_p = 'cultural_vice_captain'
                if p in candidates:
                    if len(candidates[p])==1:
                        if (cur_posts[-1]+'_choice') not in session:
                            session[pc] = 'DNE'
                            return redirect(url_for(next_p))
                        else:
                            return redirect("final")
                    else:
                        pname = "".join([x+' ' for x in p.split('_')])
                        lastthere = (cur_posts[-1]+'_choice') in session
                        return render_template('gen_page.html',p=p,pname=pname,d=candidates,cur_posts=cur_posts,lastthere=lastthere,house_choice=house_choice,prev_post=prev_post)
                else:
                    session[pc] = 'DNE'
                    return redirect(url_for(next_p))
    except :
        return redirect(url_for('assistant_head_girl'))

@app.route('/cultural-vice-captain',methods=["GET",'POST'])
def cultural_vice_captain():
    try:
        if session['cultural_captain_choice']:
            if request.method == "POST":
                cultural_vice_captain_choice = request.form["cultural_vice_captain_choice"]
                session["cultural_vice_captain_choice"] = cultural_vice_captain_choice
                if (cur_posts[-1]+'_choice') not in session:
                    return redirect(url_for('sports_captain'))
                else:
                    return redirect(url_for('final'))
                
            elif request.method == "GET":
                p = 'cultural_vice_captain'
                pc = p+"_choice"
                next_p = 'sports_captain'
                if p in candidates:
                    if len(candidates[p])==1:
                        if (cur_posts[-1]+'_choice') not in session:
                            session[pc] = 'DNE'
                            return redirect(url_for(next_p))
                        else:
                            return redirect("final")
                    else:
                        pname = "".join([x+' ' for x in p.split('_')])
                        lastthere = (cur_posts[-1]+'_choice') in session
                        return render_template('gen_page.html',p=p,pname=pname,d=candidates,cur_posts=cur_posts,lastthere=lastthere,house_choice=house_choice,prev_post=prev_post)
                else:
                    session[pc] = 'DNE'
                    return redirect(url_for(next_p))
    except:
        return redirect(url_for('cultural_captain'))

@app.route('/sports-captain',methods=["GET",'POST'])
def sports_captain():
    try:
        if session['cultural_vice_captain_choice']:
            if request.method == "POST":
                sports_captain_choice = request.form["sports_captain_choice"]
                session["sports_captain_choice"] = sports_captain_choice
                if (cur_posts[-1]+'_choice') not in session:
                    return redirect(url_for('sports_vice_captain'))
                else:
                    return redirect(url_for('final'))
            elif request.method == "GET":
                p = 'sports_captain'
                pc = p+"_choice"
                next_p = 'sports_vice_captain'
                if p in candidates:
                    if len(candidates[p])==1:
                        if (cur_posts[-1]+'_choice') not in session:
                            session[pc] = 'DNE'
                            return redirect(url_for(next_p))
                        else:
                            return redirect("final")
                    else:
                        pname = "".join([x+' ' for x in p.split('_')])
                        lastthere = (cur_posts[-1]+'_choice') in session
                        return render_template('gen_page.html',p=p,pname=pname,d=candidates,cur_posts=cur_posts,lastthere=lastthere,house_choice=house_choice,prev_post=prev_post)
                else:
                    session[pc] = 'DNE'
                    return redirect(url_for(next_p))
    except:
        return  redirect(url_for('cultural_vice_captain'))

@app.route('/sports-vice-captain',methods=["GET",'POST'])
def sports_vice_captain():
    try:
        if session['sports_captain_choice']:
            if request.method == "POST":
                print(house_choice)
                sports_vice_captain_choice = request.form["sports_vice_captain_choice"]
                session["sports_vice_captain_choice"] = sports_vice_captain_choice
                if (cur_posts[-1]+'_choice') not in session:
                    #This redirects to the next page
                    return redirect(url_for(house_choice+'_captain'))
                else:
                    return redirect(url_for('final'))
            elif request.method == "GET":
                p = 'sports_vice_captain'
                pc = p+"_choice"
                next_p = house_choice+"_captain"
                if p in candidates:
                    if len(candidates[p])==1:
                        if (cur_posts[-1]+'_choice') not in session:
                            session[pc] = 'DNE'
                            return redirect(url_for(next_p))
                        else:
                            return redirect("final")
                    else:
                        pname = "".join([x+' ' for x in p.split('_')])
                        lastthere = (cur_posts[-1]+'_choice') in session
                        return render_template('gen_page.html',p=p,pname=pname,d=candidates,cur_posts=cur_posts,lastthere=lastthere,house_choice=house_choice,prev_post=prev_post)
                else:
                    session[pc] = 'DNE'
                    return redirect(url_for(next_p))
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
                if (cur_posts[-1]+'_choice') not in session:
                    #This redirects to the next page
                    return redirect(url_for('kingfisher_vice_captain'))
                else:
                    return redirect(url_for('final'))

            elif request.method == "GET":
                p = 'kingfisher_captain'
                pc = p+"_choice"
                next_p = 'kingfisher_vice_captain'
                if p in candidates:
                    if len(candidates[p])==1:
                        if (cur_posts[-1]+'_choice') not in session:
                            session[pc] = 'DNE'
                            return redirect(url_for(next_p))
                        else:
                            return redirect("final")
                    else:
                        pname = "".join([x+' ' for x in p.split('_')])
                        lastthere = (cur_posts[-1]+'_choice') in session
                        return render_template('gen_page_kf.html',p=p,pname=pname,d=candidates,cur_posts=cur_posts,lastthere=lastthere,house_choice=house_choice,prev_post=prev_post)
                else:
                    session[pc] = 'DNE'
                    return redirect(url_for(next_p))
    except:
        return redirect(url_for('sports_vice_captain'))

@app.route('/kingfisher-vice-captain',methods=["GET","POST"])
def kingfisher_vice_captain():
    try:
        if session['kingfisher_captain_choice']:
            if request.method == "POST":
                kingfisher_vice_captain_choice = request.form["kingfisher_vice_captain_choice"]
                session["kingfisher_vice_captain_choice"] = kingfisher_vice_captain_choice
                if (cur_posts[-1]+'_choice') not in session:
                    #This redirects to the next page
                    return redirect(url_for('final'))
                else:
                    return redirect(url_for('final'))

            elif request.method == "GET":
                p = 'kingfisher_vice_captain'
                pc = p+"_choice"
                next_p = 'final'
                if p in candidates:
                    if len(candidates[p])==1:
                        if (cur_posts[-1]+'_choice') not in session:
                            session[pc] = 'DNE'
                            return redirect(url_for(next_p))
                        else:
                            return redirect("final")
                    else:
                        pname = "".join([x+' ' for x in p.split('_')])
                        lastthere = (cur_posts[-1]+'_choice') in session
                        return render_template('gen_page_kf.html',p=p,pname=pname,d=candidates,cur_posts=cur_posts,lastthere=lastthere,house_choice=house_choice,prev_post=prev_post)
                else:
                    session[pc] = 'DNE'
                    return redirect(url_for(next_p))
    except:
        return redirect(url_for('kingfisher_captain'))

@app.route('/flamingo-captain',methods=["GET",'POST'])
def flamingo_captain():
    try:
        if session['sports_vice_captain_choice']:
            if request.method == "POST":
                flamingo_captain_choice = request.form["flamingo_captain_choice"]
                session["flamingo_captain_choice"] = flamingo_captain_choice
                if (cur_posts[-1]+'_choice') not in session:
                    #This redirects to the next page
                    return redirect(url_for('flamingo_vice_captain'))
                else:
                    return redirect(url_for('final'))

            elif request.method == "GET":
                p = 'flamingo_captain'
                pc = p+"_choice"
                next_p = 'flamingo_vice_captain'
                if p in candidates:
                    if len(candidates[p])==1:
                        if (cur_posts[-1]+'_choice') not in session:
                            session[pc] = 'DNE'
                            return redirect(url_for(next_p))
                        else:
                            return redirect("final")
                    else:
                        pname = "".join([x+' ' for x in p.split('_')])
                        lastthere = (cur_posts[-1]+'_choice') in session
                        return render_template('gen_page_fl.html',p=p,pname=pname,d=candidates,cur_posts=cur_posts,lastthere=lastthere,house_choice=house_choice,prev_post=prev_post)
                else:
                    session[pc] = 'DNE'
                    return redirect(url_for(next_p))
    except Exception as e:
        print(e)
        print(candidates)
        return redirect(url_for('sports_vice_captain'))

@app.route('/flamingo-vice-captain',methods=["GET",'POST'])
def flamingo_vice_captain():
    try:
        if session['flamingo_captain_choice']:
            if request.method == "POST":
                flamingo_vice_captain_choice = request.form["flamingo_vice_captain_choice"]
                session["flamingo_vice_captain_choice"] = flamingo_vice_captain_choice
                if (cur_posts[-1]+'_choice') not in session:
                    #This redirects to the next page
                    return redirect(url_for('final'))
                else:
                    return redirect(url_for('final'))

            elif request.method == "GET":
                p = 'flamingo_vice_captain'
                pc = p+"_choice"
                next_p = 'final'
                if p in candidates:
                    if len(candidates[p])==1:
                        if (cur_posts[-1]+'_choice') not in session:
                            session[pc] = 'DNE'
                            return redirect(url_for(next_p))
                        else:
                            return redirect("final")
                    else:
                        pname = "".join([x+' ' for x in p.split('_')])
                        lastthere = (cur_posts[-1]+'_choice') in session
                        return render_template('gen_page_fl.html',p=p,pname=pname,d=candidates,cur_posts=cur_posts,lastthere=lastthere,house_choice=house_choice,prev_post=prev_post)
                else:
                    session[pc] = 'DNE'
                    return redirect(url_for(next_p))
    except:
        return redirect(url_for('flamingo_captain'))

@app.route('/falcon-captain',methods=["GET",'POST'])
def falcon_captain():
    try:
        if session['sports_vice_captain_choice']:
            if request.method == "POST":
                falcon_captain_choice = request.form["falcon_captain_choice"]
                session["falcon_captain_choice"] = falcon_captain_choice
                if (cur_posts[-1]+'_choice') not in session:
                    #This redirects to the next page
                    return redirect(url_for('falcon_vice_captain'))
                else:
                    return redirect(url_for('final'))

            elif request.method == "GET":
                p = 'falcon_captain'
                pc = p+"_choice"
                next_p = 'falcon_vice_captain'
                if p in candidates:
                    if len(candidates[p])==1:
                        if (cur_posts[-1]+'_choice') not in session:
                            session[pc] = 'DNE'
                            return redirect(url_for(next_p))
                        else:
                            return redirect("final")
                    else:
                        pname = "".join([x+' ' for x in p.split('_')])
                        lastthere = (cur_posts[-1]+'_choice') in session
                        return render_template('gen_page_fa.html',p=p,pname=pname,d=candidates,cur_posts=cur_posts,lastthere=lastthere,house_choice=house_choice,prev_post=prev_post)
                else:
                    session[pc] = 'DNE'
                    return redirect(url_for(next_p))
    except:
        return redirect(url_for('sports_vice_captain'))

@app.route('/falcon-vice-captain',methods=["GET",'POST'])
def falcon_vice_captain():
    try:
        if session['falcon_captain_choice']:
            if request.method == "POST":
                falcon_vice_captain_choice = request.form["falcon_vice_captain_choice"]
                session["falcon_vice_captain_choice"] = falcon_vice_captain_choice
                if (cur_posts[-1]+'_choice') not in session:
                    #This redirects to the next page
                    return redirect(url_for('final'))
                else:
                    return redirect(url_for('final'))

            elif request.method == "GET":
                p = 'falcon_vice_captain'
                pc = p+"_choice"
                next_p = 'final'
                if p in candidates:
                    if len(candidates[p])==1:
                        if (cur_posts[-1]+'_choice') not in session:
                            session[pc] = 'DNE'
                            return redirect(url_for(next_p))
                        else:
                            return redirect("final")
                    else:
                        pname = "".join([x+' ' for x in p.split('_')])
                        lastthere = (cur_posts[-1]+'_choice') in session
                        return render_template('gen_page_fa.html',p=p,pname=pname,d=candidates,cur_posts=cur_posts,lastthere=lastthere,house_choice=house_choice,prev_post=prev_post)
                else:
                    session[pc] = 'DNE'
                    return redirect(url_for(next_p))
    except:
        return redirect(url_for('falcon_captain'))

@app.route('/eagle-captain',methods=["GET",'POST'])
def eagle_captain():
    try:
        if session['sports_vice_captain_choice']:
            if request.method == "POST":
                eagle_captain_choice = request.form["eagle_captain_choice"]
                session["eagle_captain_choice"] = eagle_captain_choice
                if (cur_posts[-1]+'_choice') not in session:
                    #This redirects to the next page
                    return redirect(url_for('eagle_vice_captain'))
                else:
                    return redirect(url_for('final'))

                
            elif request.method == "GET":
                p = 'eagle_captain'
                pc = p+"_choice"
                next_p = 'eagle_vice_captain'
                if p in candidates:
                    if len(candidates[p])==1:
                        if (cur_posts[-1]+'_choice') not in session:
                            session[pc] = 'DNE'
                            return redirect(url_for(next_p))
                        else:
                            return redirect("final")
                    else:
                        pname = "".join([x+' ' for x in p.split('_')])
                        lastthere = (cur_posts[-1]+'_choice') in session
                        return render_template('gen_page_ea.html',p=p,pname=pname,d=candidates,cur_posts=cur_posts,lastthere=lastthere,house_choice=house_choice,prev_post=prev_post)
                else:
                    session[pc] = 'DNE'
                    return redirect(url_for(next_p))
    except:
        return redirect(url_for('sports_vice_captain'))

@app.route('/eagle-vice-captain',methods=["GET",'POST'])
def eagle_vice_captain():
    try:
        if session['eagle_captain_choice']:
            if request.method == "POST":
                eagle_vice_captain_choice = request.form["eagle_vice_captain_choice"]
                session["eagle_vice_captain_choice"] = eagle_vice_captain_choice
                if (cur_posts[-1]+'_choice') not in session:
                    #This redirects to the next page
                    return redirect(url_for('final'))
                else:
                    return redirect(url_for('final'))

            elif request.method == "GET":
                p = 'eagle_vice_captain'
                pc = p+"_choice"
                next_p = 'final'
                if p in candidates:
                    if len(candidates[p])==1:
                        if (cur_posts[-1]+'_choice') not in session:
                            session[pc] = 'DNE'
                            return redirect(url_for(next_p))
                        else:
                            return redirect("final")
                    else:
                        pname = "".join([x+' ' for x in p.split('_')])
                        lastthere = (cur_posts[-1]+'_choice') in session
                        return render_template('gen_page_ea.html',p=p,pname=pname,d=candidates,cur_posts=cur_posts,lastthere=lastthere,house_choice=house_choice,prev_post=prev_post)
                else:
                    session[pc] = 'DNE'
                    return redirect(url_for(next_p))
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
            print("yes")
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('admin_page'))

@app.route('/dashboard')
def dashboard():
    try:
        if session['logged'] == True:
            #Renders the dashboard only if the admin password is valid
            return render_template('dashboard.html')
        else:
            return redirect(url_for('admin_page'))
    except Exception as e:
        print(e)
        return redirect(url_for('admin_page'))

@app.route('/show_candidate', methods=['GET', 'POST'])
def show_candidate():
    try:
        if session['logged'] == True:
            if request.method == "GET":
                global candidates
                return render_template('show_candidates.html',candidates=candidates,str=str)
            else:
                updated_candidates = request.form['candvalue']#fetches the parsed new candidates list
                updated_candidates = eval(updated_candidates)
                for post in updated_candidates:#filters the candidates
                    l = updated_candidates[post]
                    for y in l:
                        if y == '':
                            updated_candidates[post].remove(y)
                print(updated_candidates)
                candidates = updated_candidates
                return redirect(url_for('show_candidate'))
        else:
            return redirect(url_for('admin_page'))
    except Exception as  e:
        print(e)
        return redirect(url_for('admin_page'))

@app.route('/enter_candidate')
def enter_candidate():
    try:
        if session['logged'] == True:
            #This part shows the candidates
            return render_template('enter_candidates.html',candidates=candidates,str=str,len=len)
        else:
            return redirect(url_for('admin_page'))
    except Exception as e:
        print(e)
        return redirect(url_for('admin_page'))

@app.route('/voting_settings')
def voting_settings():
    try:
        if session['logged'] == True:
            return render_template('voting_settings.html',valid=voting_started)
        else:
            return redirect(url_for('admin_page'))
    except:
        return redirect(url_for('admin_page'))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    try:
        if session['logged'] == True:
            global house_choice
            if request.method == "GET":
                return render_template('settings.html',house_choice=house_choice)
            elif request.method == "POST":
                #Here the admin changes the password for the local admin
                #This block confirms the changes
                global cur_posts
                house_choice = request.form['hc']
                cur_posts = cur_posts[0:-2]
                cur_posts.extend([house_choice+'_captain',house_choice+'_vice_captain'])

                #This block confirms the changes
                changed_pwd = request.form['changed_pwd']
                if not sec_code.pass_is_valid(changed_pwd):
                    sec_code.pass_set(changed_pwd)
                return redirect(url_for('settings'))
    except Exception as e:
        print(e)
        return redirect(url_for('admin_page'))

@app.route('/logout')
def logout():
    #Upon logging out the session and come out of the admin page
    session.clear()
    return redirect(url_for("home"))#while copying this part should redirect to entry page

#Functions for the voting settings function
@app.route('/start_voting')
def start_voting():#This function is called when then admin presses the start voting button
    #database_linker.initializing(#idk what to put here)
    return redirect(url_for("voting_settings"))

@app.route('/stop_voting')
def stop_voting():#This function is called when the admin presses the stop voting button
    database_linker.results_print()
    return redirect(url_for("voting_settings"))

@app.route('/generate-code')
def generate_code():#This function is called when the admin presses the generate security codes button
    sec_code.code_print()
    return redirect(url_for('voting_settings'))

#Function to send photos to the webpage
@app.route('/uploads/<path:filename>')
def download_file(filename,ishouse):
    return send_from_directory(app.config['CANDIDATE_PHOTOS'],filename.upper(), as_attachment=True)


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
    dt1 = {}
    for x in dt:
        if dt[x] != 'DNE':
            dt1[x] = dt[x]
    print(dt1)
    database_linker.add_votes_to_db(dict(dt1))

def fetch_changed_house_choice():
    hc = request.values.get('house_choice')
    print(hc)

def prev_post(p):#This function tells the back button which page to go back to
    cur_post = p
    cur_index = cur_posts.index(cur_post)
    if cur_index>0:
        return cur_posts[cur_index-1]
    else:
        return 'home'

def add_to_cur_posts():#To create teh current posts variable
    global cur_posts
    l = ['head_boy','head_girl','assistant_head_boy','assistant_head_girl','cultural_captain','cultural_vice_captain','sports_captain','sports_vice_captain',house_choice+'_captain',house_choice+'_vice_captain']
    for y in l:
        if y in candidates:
            if len(candidates[y])>1:
                cur_posts.append(y)

def create_candidates():#Temporary testing function to create the candidates dictionary
    global candidates
    candidates = {'head_boy':{'Jeb','Notch'},'head_girl': {'Divy', 'Joe', 'Sanjay Chidambaram', 'Parthiv'},
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

def cc():#Temporary testing function to create the candidates dictionary
    global candidates
    for x in ['head_boy','head_girl','assistant_head_boy','assistant_head_girl','cultural_captain','cultural_vice_captain','sports_captain','sports_vice_captain','kingfisher_captain','kingfisher_vice_captain','flamingo_captain','flamingo_vice_captain','falcon_captain','falcon_vice_captain','eagle_captain','eagle_vice_captain']:
        candidates[x] = ['A','B','C','D']
    candidates['head_girl'] = ["A","B","X"]
    candidates['eagle_captain'] = ["A","B","X"]

def set_photos_path():#This function sets the path for the candidates photos in the app.config
    candidate_pictures = 'candidate_photos'
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)
    photos_path = application_path + '\\' + candidate_pictures 
    app.config['CANDIDATE_PHOTOS'] = photos_path

def general_get(p,to):
    pc = p+"_choice"
    #Here the method is the get method
    if p in candidates and len(candidates[p]) >1:
        #If there are more than one candidates then it'll load the template
        return render_template(p+'.html',d=candidates,house_choice=house_choice)
    #We dont need to render the page if there is only one candidate
    else:
        if pc not in session:
            #If the page hasn't been voted through then it registers the choice
            session[pc] = 'DNE'
            return redirect(url_for(to))
        elif (house_choice+'_vice_captain_choice') in session:
            #Prevents some one from rendering from the review page
            return redirect(url_for('final'))

def start():
    #This is the main method for starting the app
    global candidates
    cc()#temp function to initialize  the candidates variable
    #We fetch the list of candidates from the database and continue
    #candidates = database_linker.get_cands_from_db()
    add_to_cur_posts()
    set_photos_path()
    app.run(debug=True)

start()
