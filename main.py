""" main file that initializes flask and the GUI """

import subprocess
import os
import sys
from flask import Flask, redirect, url_for, render_template, request, session, send_from_directory
import database_linker
import sec_code
import local_functions


# Fetches the house choice locally stored
house_choice = local_functions.get_house_choice().lower()

candidates = {}  # Store the candidates in the form {post:[cand1,cand2, ...]}
cur_posts = []  # Stores the order of voting
no_of_codes = 4  # Stores the number of pages of codes to be generated
color_scheme = {}  # Stores the various colors of the different houses
voting_order_modified = False  # Tells if the voting order has been modified

# Flask's file variable for showing session validity
valid = False
# Status of voting; affects the admin dashboard
voting_started = database_linker.set_voting_status()
# Shows if voting has ended
voting_ended = False


if getattr(sys, 'frozen', False):
    # Changes folder paths after freezing
    template_folder = os.path.join(sys._MEIPASS, 'GUI')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder,
                static_folder=static_folder)
    
    # Removes console logs when frozen
    import logging
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    from flask import cli
    cli.show_server_banner = lambda *_: None

else:
    app = Flask(__name__, template_folder='./GUI/')

app.secret_key = 'abc'


@app.route('/', methods=["GET", 'POST'])
def home():
    ''' This is the voting landing page; contains text box for entering sec code '''

    if request.method == "GET":
        # Template is rendered
        session["logged"] = False
        return render_template('voting_landing.html', voting_started=voting_started, voting_ended=voting_ended)

    else:
        # Checks validity of security code
        receivedpwd = request.form['pwd_box']
        validity = sec_code.code_is_valid(receivedpwd)

        # Checks that validity is not 'Invalid' or 'Already Used'
        if (validity == True) and voting_started:
            global valid
            valid = True
            session['home_choice'] = True
            return redirect(url_for('load_post', post=cur_posts[0]))

        return redirect(url_for('invalid_code', msg=(validity if voting_started else 'Invalid - Voting not started')))


@app.route('/invalid_code/<msg>')
def invalid_code(msg):
    ''' Loads the template in case of an invalid code and provides apt message '''

    return render_template('invalid_page.html', msg=msg)


@app.route('/post/<post>', methods=["GET", 'POST'])
def load_post(post):
    ''' This function is used to render the posts and receive the choices of the voter '''

    # Handles if the post to be rendered is not in cur_posts
    if post == 'home':
        return redirect(url_for('home'))
    elif post == 'final':
        return redirect(url_for('final'))

    # Initialize variables to get information about posts around the current post
    # global cur_posts
    p = post
    pc = post+'_choice'
    next_p = next_post(p)
    prev_p = prev_post(p)

    try:
        if session[prev_p+'_choice']:
            if request.method == "POST":
                #We take the choice of the voter
                post_choice = request.form[pc]
                session[pc] = post_choice

                #If the last post has been voted for already, then redirection should take place to the review page
                if (cur_posts[-1]+'_choice') not in session:
                    if next_p == 'final':
                        return redirect(url_for('final'))
                    else:
                        return redirect(url_for('load_post', post=next_p))
                else:
                    return redirect(url_for('final'))

            elif request.method == "GET":
                #Loads the page based on the conditions given

                if p in candidates:
                    if len(candidates[p]) <= 1:
                        #This block excutes if post's list of candidates is empty or has only one candidate

                        if (cur_posts[-1]+'_choice') not in session:
                            session[pc] = 'DNE'
                            return redirect(url_for('load_post', post=next_p))
                        else:
                            return redirect(url_for("final"))

                    else:
                        #This block executes if the post has more than one candidate

                        pname = "".join([x+' ' for x in p.split('_')])
                        lastthere = (cur_posts[-1]+'_choice') in session
                        house_keys = {
                            'kingfisher': 'kf', 'flamingo': 'fl', 'falcon': 'fa', 'eagle': 'ea'}

                        #Checks if the post is a house post
                        for house in house_keys:
                            if p.startswith(house):
                                #Template is rendered with the house name passed as parameter
                                return render_template('gen_base_page.html', base_page_name=house, p=p, pname=pname, d=candidates, cur_posts=cur_posts, lastthere=lastthere, house_choice=house_choice, prev_post=prev_post, color_scheme=color_scheme, len=len)
                        return render_template('gen_base_page.html', p=p, pname=pname, base_page_name='major', d=candidates, cur_posts=cur_posts, lastthere=lastthere, house_choice=house_choice, prev_post=prev_post, color_scheme=color_scheme, len=len)
                else:
                    #For a post not in candidates,we put a placeholder for the voter's choice which we remove later
                    session[pc] = 'DNE'
                    return redirect(url_for('load_post', post=next_p))
    except Exception as e:
        print(e)
        if prev_p == 'home':
            return redirect(url_for('home'))
        else:
            return redirect(url_for('load_post', post=prev_p))


def prev_post(p):
    '''This function returns the post behind the current one'''

    cur_post = p
    cur_index = cur_posts.index(cur_post)
    if cur_index > 0:
        return cur_posts[cur_index-1]
    else:
        #In case the post entered is the first post
        return 'home'


def next_post(p):
    '''This function returns the post in front of the current one'''

    cur_post = p
    cur_index = cur_posts.index(cur_post)
    if cur_index != len(cur_posts)-1:
        return cur_posts[cur_index + 1]
    else:
        #In case the post entered is the last
        return 'final'


@app.route('/review', methods=['GET', 'POST'])
def final():
    '''This function is called once all the posts have been voted for, renders the table'''

    try:
        #Checks if the last post has been voted for
        if session[cur_posts[-1]+'_choice']:
            if request.method == "GET":
                #Session dictionary is passed to make the table in the webpage
                return render_template('review_page.html', session=dict(session), cur_posts=cur_posts, title=title)
            else:
                return redirect(url_for('over'))

    except Exception as e:
        print(e)
        return redirect(url_for('load_post', post=cur_posts[-1]))


@app.route('/done')
def over():
    '''This function is executed once the voter has submitted their choice
        ->Stores voter\'s choices
        ->Clears the session\'s variables
        ->Makes the session invalid
    '''

    store_result(dict(session))

    session.clear()

    global valid
    valid = False

    return render_template('thank_you.html')


# Admin things


@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    '''This function renders the admin login page. In case of any exception/error redirection here.'''

    if request.method == 'GET':
        return render_template('admin_landing.html')
    elif request.method == "POST":
        #Validation of the admin password
        # session['logged'] stores whether the admin is logged in and is checked for when every admin page is opened
        receivedpwd = request.form['pwd_box']
        if sec_code.pass_is_valid(receivedpwd):
            session['logged'] = True
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('admin_page'))


@app.route('/dashboard')
def dashboard():
    '''This function renders the template for the admin dashboard page'''

    try:
        if session['logged'] == True:
            #Renders the dashboard only if the admin password is valid
            return render_template('dashboard.html', voting_started=voting_started, voting_ended=voting_ended, no_of_codes=no_of_codes, house_choice=house_choice, color_scheme=color_scheme, makeupper=makeupper)
        else:
            return redirect(url_for('admin_page'))
    except Exception as e:
        print(e)
        return redirect(url_for('admin_page'))


@app.route('/show_candidate', methods=['GET', 'POST'])
def show_candidate():
    '''This function renders the show/enter candidates page'''

    try:
        if session['logged'] == True:
            global candidates
            if request.method == "GET":
                load_list = [['Head Boy', 'Head Girl', 'Sports Captain', 'Cultural Captain'],
                             ['Assistant Head Boy', 'Assistant Head Girl',
                                 'Sports Vice Captain', 'Cultural Vice Captain'],
                             ['Kingfisher Captain', 'Flamingo Captain',
                                 'Falcon Captain', 'Eagle Captain'],
                             ['Kingfisher Vice Captain', 'Flamingo Vice Captain', 'Falcon Vice Captain', 'Eagle Vice Captain']]
                custom_post_load_list = get_custom_post_load_list()
                return render_template('show_candidates.html', candidates=candidates, str=str, voting_started=voting_started, voting_ended=voting_ended, getcolor=getcolor, load_list=load_list, title=title, startswith=startswith, custom_posts=custom_post_load_list, len=len)

            else:
                #Fetches and parses the candidates list from json format
                updated_candidates = request.form['candvalue']
                updated_candidates = eval(updated_candidates)

                #Filters the candidates
                for post in updated_candidates:
                    l = updated_candidates[post]
                    new_l = []
                    for y in l:
                        y = y.strip()
                        if y != '':
                            new_l.append(y)
                    updated_candidates[post] = new_l

                #Updates the candidates and stores the same in the database
                candidates = updated_candidates

                #If no custom post has been added,it creates the cur_post variable
                if not voting_order_modified:
                    add_to_cur_posts()

                database_linker.initializing(candidates)

                return redirect(url_for('show_candidate'))
        else:
            return redirect(url_for('admin_page'))
    except Exception as e:
        print(e)
        return redirect(url_for('admin_page'))


@app.route('/add_custom_post', methods=['GET', 'POST'])
def add_custom_post():
    '''This function renders the page for adding a custom post and changing the order of voting'''

    try:
        if session['logged'] == True:
            global cur_posts, candidates, voting_order_modified

            if request.method == 'GET':
                site = request.host
                return render_template('add_custom_post.html', str=str, cur_post=cur_posts, u=underscore_remove, replace_house_name=replace_house_name,site=site)

            else:
                #Get the response from the page's AJAX
                response = request.get_json()
                new_post_name = response['post_name'].lower().strip()

                #Formats the response and so as to set the value for cur_posts
                cur_posts_order = []
                if new_post_name != '':
                    #If the added post is not a house post
                    if not response['for_house']:
                        cur_posts_order = [new_post_name.replace(
                            ' ', '_') if pname == 'new_post' else pname for pname in response['cur_posts_order']]

                        #Doesn't add the post if it already exists
                        if new_post_name.replace(' ', '_') in cur_posts:
                            return redirect(url_for('show_candidate'))

                        candidates[new_post_name.replace(' ', '_')] = []

                    #If the added post is a house opst
                    else:
                        cur_posts_order = [house_choice+'_'+new_post_name.replace(
                            ' ', '_') if pname == 'new_post' else pname for pname in response['cur_posts_order']]

                        #Doesn't add the post if it already exists
                        if house_choice + '_' + new_post_name.replace(' ', '_') in cur_posts:
                            return redirect(url_for('show_candidate'))

                        for house in ['kingfisher', 'falcon', 'flamingo', 'eagle']:
                            candidates[house+'_' +
                                       new_post_name.replace(' ', '_')] = []
                        new_post_name = house_choice+'_' + \
                            new_post_name.replace(' ', '_')

                    cur_posts_order = [post.replace('house', house_choice) if post.startswith(
                        'house') else post for post in cur_posts_order]

                    #Store candidates in the database and updates value of cur_posts
                    database_linker.initializing(candidates)
                    cur_posts = cur_posts_order
                    voting_order_modified = True
                else:
                    #Changes the order of voting is no post is added
                    cur_posts_order = response['cur_posts_order']
                    cur_posts_order.remove('new_post')
                    cur_posts = [(post.replace('house', house_choice) if post.startswith(
                        'house') else post) for post in cur_posts_order]

                    return redirect(url_for('add_custom_post'))
        else:
            return redirect(url_for('admin_page'))
    except Exception as e:
        print(e)
        return redirect(url_for('admin_page'))


@app.route('/delete_post', methods=['GET', 'POST'])
def delete_post():
    '''This function renders the page for deleting a post'''

    try:
        global cur_posts, candidates
        if session['logged'] == True:
            if request.method == 'GET':
                site = request.host
                return render_template('delete_post.html', cur_post=cur_posts, u=underscore_remove, replace_house_name=replace_house_name,site=site)

            else:
                #Obtain the response from the page and parse the same
                response = request.get_json()
                post_to_delete = response['post_to_delete'].strip()
                post_to_delete = post_to_delete.replace(' ', '_').lower()

                if post_to_delete.startswith('house'):
                    post_to_delete = post_to_delete.replace(
                        'house', house_choice)

                try:
                    cur_posts.remove(post_to_delete)

                    for post in list(candidates.keys()):
                        #If the post is a house post then we have to delete the name of the candidates of all the houses for that post
                        if post_to_delete.startswith(house_choice):
                            if post.endswith("".join(["_"+x for x in post_to_delete.split('_')[1:]])):
                                del candidates[post]

                        #For a normal post, we can delete the key-value pair
                        else:
                            if post == post_to_delete:
                                del candidates[post]

                    database_linker.initializing(candidates)
                except Exception as e:
                    print(e)
                    pass

        else:
            return redirect(url_for('admin_page'))
    except:
        return redirect(url_for('admin_page'))


@app.route('/voting_settings')
def voting_settings():
    '''This function renders the page for changing the settings of voting status'''

    try:
        if session['logged'] == True:
            not_there = all_photo_check(set_photos_path())
            return render_template('voting_settings.html', d=candidates, valid=voting_started, no_of_codes=no_of_codes, not_there=not_there, makeupper=makeupper, len=len, underscore_remove=underscore_remove)
        else:
            return redirect(url_for('admin_page'))
    except Exception as e:
        print(e)
        return redirect(url_for('admin_page'))


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    '''This function renders the page for changing the general settings'''

    try:
        if session['logged'] == True:
            global house_choice, no_of_codes

            if request.method == "GET":
                return render_template('settings.html', house_choice=house_choice, no_of_codes=no_of_codes)

            elif request.method == "POST":
                #Checks for the changed house_choice and updates the same in cur_posts
                global cur_posts
                old_house_choice = house_choice
                house_choice = request.form['hc']
                house_choice = house_choice.lower()
                local_functions.store_house_choice(house_choice)
                update_cur_post(old_house_choice, house_choice)

                #Checks for the changed password and updates the same
                changed_pwd = request.form['changed_pwd']
                if not sec_code.pass_is_valid(changed_pwd) and changed_pwd != '':
                    sec_code.pass_set(changed_pwd)

                #Checks if the number of pages of codes to be printed is changed and updaes the same
                changed_no_of_codes = request.form['changed_no_of_codes']
                t = eval(changed_no_of_codes.split()[0])
                if type(t) is int:
                    if t > 0:
                        no_of_codes = t

                return redirect(url_for('settings'))

    except Exception as e:
        print(e)
        return redirect(url_for('admin_page'))


@app.route('/logout')
def logout():
    '''This function logs the admin out'''

    session.clear()
    return redirect(url_for("home"))

#Functions called by voting settings function


@app.route('/start_voting')
def start_voting():
    '''This function is called when then admin presses the start voting button'''

    global voting_started, voting_ended

    database_linker.set_voting_status(True)
    voting_started = True
    voting_ended = False


    #Prints the pdf containing the security codes for voting
    sec_code.code_print(no_of_codes)

    return redirect(url_for("voting_settings"))


@app.route('/stop_voting')
def stop_voting():
    '''This function is called when the admin presses the stop voting button'''

    global voting_started, voting_ended
    database_linker.set_voting_status(False)
    voting_started = False
    voting_ended = True

    #Prints the pdf containin the results of voting
    database_linker.results_print()

    return redirect(url_for('result'))


@app.route('/results')
def result():
    '''This function opens the admin dashboard and also the results in a new folder'''

    return render_template('results.html')


@app.route('/download_results')
def download_results():
    '''This function downloads the results and displays the same in the browser'''

    x = "".join(
        [y+'\\' for y in app.config['CANDIDATE_PHOTOS'].split('\\')[:-1]])

    try:
        return send_from_directory(x, filename='results.pdf')
    except Exception as e:
        print(e)
        return str(e)


@app.route('/uploads/<path:filename>')
def download_file(filename):
    '''This function downloads the given file'''

    try:
        x = get_image_folder_path(app.config['CANDIDATE_PHOTOS'], filename)
        folder = "".join([y+'/' for y in x.split('/')[:-1]])
        filename = x.split('/')[-1]
        return send_from_directory(folder, filename, as_attachment=True)
    except:
        pass


def get_image_folder_path(path, cand_name):
    '''This function returns the path of the image file with any extension'''

    for tup in os.walk(path):
        for file in tup[2]:
            if file.lower()[:len(file)-file[::-1].index('.')-1] == cand_name.lower():
                if not file.lower().startswith('default'):
                    return tup[0].replace('\\', '/')+'/'+file


def all_photo_check(path):
    '''This function checks if all the candidates' photos are there'''

    #Format of not_there : {post1:'missing_candidate_1,missing_candidate_2,..',post2:'...'...}
    not_there = {}

    for post, cands in database_linker.get_cands_from_db().items():
        for cand_name in cands:
            for tup in os.walk(path):
                exists = False
                for file in tup[2]:
                    if file.lower()[:len(file)-file[::-1].index('.')-1] == cand_name.lower():
                        exists = True
                else:
                    if not exists:
                        try:
                            not_there[post] = not_there[post]+[cand_name]
                        except KeyError:
                            not_there[post] = [cand_name]

    #Converts the posts into a single string to be passed into the html template
    for post in not_there:
        ret_str = ",".join(not_there[post])
        not_there[post] = ret_str

    return not_there


#Non-decorated functions


#Functions called to initialize variable
def add_to_cur_posts():
    '''This function creates the current posts variable'''

    global cur_posts, candidates

    cur_posts = []
    houses = ['kingfisher', 'flamingo', 'falcon', 'eagle']
    major_temp = []
    house_temp = []
    default_major_order = ['head_boy', 'head_girl', 'assistant_head_boy', 'assistant_head_girl',
                           'cultural_captain', 'cultural_vice_captain', 'sports_captain', 'sports_vice_captain']
    default_house_order = [house_choice +
                           '_captain', house_choice+'_vice_captain']

    #Classifies the posts into a house post or major post
    for post in candidates:
        is_house_post = False
        for house in houses:
            if post.startswith(house):
                is_house_post = True

        if is_house_post:
            if post.startswith(house_choice):
                house_temp.append(post)
        else:
            if len(candidates[post]) > 1 or post not in default_major_order:
                major_temp.append(post)

    #Adds the major posts in an order to cur_posts
    for post in default_major_order:
        #First adds default major posts
        if post in major_temp:
            cur_posts.append(post)
            major_temp.remove(post)
    for post in major_temp:
        #Second adds the custom major posts(if any)
        cur_posts.append(post)

    #Adds the house posts in an order to cur_posts
    for post in default_house_order:
        #First adds the default house posts
        if post in house_temp:
            cur_posts.append(post)
            house_temp.remove(post)
    for post in house_temp:
        #Second adds the custom house posts(if any)
        cur_posts.append(post)


def set_photos_path():
    '''This function sets the path for the candidates photos in the app.config'''

    try:
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(__file__)
        candidate_pictures = 'candidate_photos'
        photos_path = application_path + '\\' + candidate_pictures
        app.config['CANDIDATE_PHOTOS'] = photos_path
    except FileNotFoundError:
        #creates folder if not there
        app_path = "/".join(os.path.dirname(__file__).split('/'))
        os.mkdir(app_path+'/candidate_photos')
        set_photos_path()

    return photos_path


def colors_set():
    '''This function sets the colour scheme variable value'''

    global color_scheme
    #Format: (background_color,box,text)
    color_scheme['kingfisher'] = ('#30a4e2', '#036f96', '#ffffff')
    color_scheme['flamingo'] = ('#E05707', '#A63A0F', '#ffffff')
    color_scheme['falcon'] = ('#7E58BF', '#432A73', '#ffffff')
    color_scheme['eagle'] = ('#B81A1C', '#750407', '#ffffff')
    color_scheme['major'] = ('#161616', '#212121', '#FCED47')

#Miscellaneous functions used by the decorated functions


def store_result(dt):
    '''This function is called to store the choices of the voter'''

    #Remove unnecessary keys
    if 'logged' in dt:
        del dt['logged']
    if 'home_choice' in dt:
        del dt['home_choice']

    #Adds to a new dict if the choice is valid
    dt1 = {}
    for x in dt:
        if dt[x] != 'DNE':
            dt1[x] = dt[x]

    database_linker.add_votes_to_db(dict(dt1))


def get_custom_post_load_list():
    '''This function returns the list of custom posts to be loaded in the show/enter candidates page'''

    #This is the order that we want for the default posts
    load_list = ['Head Boy', 'Head Girl', 'Sports Captain', 'Cultural Captain', 'Kingfisher Captain', 'Flamingo Captain', 'Falcon Captain', 'Eagle Captain', 'Assistant Head Boy',
                 'Assistant Head Girl', 'Sports Vice Captain', 'Cultural Vice Captain', 'Kingfisher Vice Captain', 'Flamingo Vice Captain', 'Falcon Vice Captain', 'Eagle Vice Captain']
    load_list = [y.lower().replace(' ', "_") for y in load_list]

    #We load the name of the posts
    cp = candidates.keys()

    #We take the symmetric difference so we get custom posts (and also default posts without candidates if any)
    result = list(set(load_list) ^ set(cp))
    filtered_result = []

    #Adds recognized custom posts (sometimes there may be default posts without candidates the will be present in the symmetric difference)
    for post in result:
        if post not in load_list:
            filtered_result.append(post)
    result = filtered_result

    final = []
    major_posts = []
    house_posts = []

    #Classifies as a house post or as a major post
    for post in result:
        if is_house_post(post):
            if post.startswith('kingfisher'):
                house_posts.append(post)
        else:
            major_posts.append(post)

    #We add the house custom posts since we want to have them first
    for post in house_posts:
        post = post.split('_')[1:]
        for house in ["kingfisher", 'flamingo', 'falcon', 'eagle']:
            final.append(house+"".join(['_'+y for y in post]))
    #We keep the major posts at the end of the order
    final.extend(major_posts)

    return final


def update_cur_post(old_choice, cur_choice):
    '''This function updates the cur_posts variable when the house_choice is changed.'''

    global cur_posts
    temp_posts = []
    for post in cur_posts:
        temp = post.split('_')
        if temp[0] == old_choice:
            temp_posts.append(cur_choice + ''.join(['_'+y for y in temp[1:]]))
        else:
            temp_posts.append(post)

    cur_posts = temp_posts

#Functions used by the html templates


def underscore_remove(t):
    return t.replace('_', ' ').upper()


def makeupper(t):
    return t.upper()


def title(t):
    return t.title().replace('_', ' ')


def startswith(a, b):
    return a.startswith(b)


def getcolor(t):
    t = t.split()[0].lower()
    house_color = {'kingfisher': 'kf', 'flamingo': 'fl',
                   'falcon': 'fa', 'eagle': 'ea', 'major': 'ma'}
    for x in house_color:
        if x == t:
            return house_color[t]
    return house_color['major']


def is_house_post(t):
    for x in ["kingfisher", 'falcon', 'flamingo', 'eagle']:
        if t.lower().startswith(x):
            return True
    return False


def replace_house_name(l):
    return [post.replace(house_choice, 'house') if post.startswith(house_choice) else post for post in l]


def start():
    '''This is the main method for starting the app'''

    port_number = 5000
    
    global candidates
    candidates = database_linker.get_cands_from_db()

    add_to_cur_posts()
    local_functions.resize_images_in_folder(set_photos_path())
    colors_set()

    if getattr(sys, 'frozen', False):
        try:
            subprocess.run(
                f"\"%ProgramFiles%\\Google\\Chrome\\Application\\chrome_proxy.exe\" --profile-directory=Default --app=\"http://127.0.0.1:{port_number}\" --kiosk", shell=True)
            subprocess.run(
                f"\"%ProgramFiles(x86)%\\Google\\Chrome\\Application\\chrome_proxy.exe\" --profile-directory=Default --app=\"http://127.0.0.1:{port_number}\" --kiosk", shell=True)
        except:
            pass

    app.run(debug=False, port=port_number)

start()
