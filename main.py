from flask import Flask,redirect,url_for,render_template,request,session,send_from_directory
import database_linker
import sec_code
import os,sys
import local_functions

house_choice = local_functions.get_house_choice().lower()  #Make sure all the house are in lowercase
candidates = {}
valid = False  # Flask's file variable for showing session validity
voting_started = False  # Status of voting; affects the admin dashboard
voting_ended = False #Shows if voting has ended
cur_posts =[] #Shows which posts are there for voting
no_of_codes = 4 #Stores the number of pages of codes to be generated
all_candidates_photos_there = None #Tells whether all the candidates' photos are there
color_scheme = {}#Stores the various colors of the different houses

app = Flask(__name__,template_folder='./GUI/')
app.secret_key = 'abc'

results = dict([])

#Voting page things
@app.route('/',methods=["GET",'POST'])
def home():
	if request.method == "GET":
		#This part shows renders the template (get template)
		session["logged"] = False
		return render_template('voting_landing.html',voting_started=voting_started,voting_ended=voting_ended)
	else:
		#This part whether the security code is valid by asking the database
		receivedpwd = request.form['pwd_box']
		validity = sec_code.code_is_valid(receivedpwd)
		if validity and voting_started:
			global valid
			valid = True
			session['home_choice'] = True
			print(cur_posts)
			return redirect(url_for('load_post',post=cur_posts[0]))
		else:
			return redirect(url_for('invalid_code',msg=(validity if voting_started else 'Invalid - Voting not started')))

@app.route('/invalid_code/<msg>')
def invalid_code(msg):
	return render_template('invalid_page.html',msg=msg)

@app.route('/post/<post>',methods=["GET",'POST'])
def load_post(post):
	if post == 'home':
		return redirect(url_for('home'))
	if post == 'final':
		return redirect(url_for('final'))

	global cur_posts
	p = post
	pc = post+'_choice'
	next_p = next_post(p)
	prev_p = prev_post(p)
	prev_pc = prev_p+'_choice'
	print(post,cur_posts,candidates)
	print(prev_p,next_p)
	print(dict(session))

	try:
		if session[prev_pc]:
			if request.method == "POST":
				post_choice = request.form[pc]
				session[pc] = post_choice
				if (cur_posts[-1]+'_choice') not in session:
					#This redirects to the next page
					if next_p == 'final':
						return redirect(url_for('final'))
					else:
						return redirect(url_for('load_post',post=next_p))
				else:
					return redirect(url_for('final'))
			elif request.method == "GET":
				if p in candidates:
					if len(candidates[p])<=1:
						if (cur_posts[-1]+'_choice') not in session:
							session[pc] = 'DNE'
							return redirect(url_for('load_post',post=next_p))
						else:
							return redirect(url_for("final"))
					else:
						pname = "".join([x+' ' for x in p.split('_')])
						lastthere = (cur_posts[-1]+'_choice') in session
						house_keys={'kingfisher':'kf','flamingo':'fl','falcon':'fa','eagle':'ea'}
						for house in house_keys:
							if p.startswith(house):
								return render_template('gen_base_page.html',base_page_name=house,p=p,pname=pname,d=candidates,cur_posts=cur_posts,lastthere=lastthere,house_choice=house_choice,prev_post=prev_post,color_scheme=color_scheme,len=len)
						return render_template('gen_base_page.html',p=p,pname=pname,base_page_name='major',d=candidates,cur_posts=cur_posts,lastthere=lastthere,house_choice=house_choice,prev_post=prev_post,color_scheme=color_scheme,len=len)
				else:
					session[pc] = 'DNE'
					return redirect(url_for('load_post',post=next_p))
	except Exception as e:
		print(e)
		if prev_p == 'home':
			return redirect(url_for('home'))
		else:
			return redirect(url_for('load_post',post=prev_p))

def prev_post(p):#This function tells the back button which page to go back to
	cur_post = p
	cur_index = cur_posts.index(cur_post)
	if cur_index>0:
		return cur_posts[cur_index-1]
	else:
		return 'home'

def next_post(p):#This function tells which page to go to next
	cur_post = p
	cur_index = cur_posts.index(cur_post)
	if cur_index != len(cur_posts)-1:
		return cur_posts[cur_index + 1]
	else:
		return 'final'

@app.route('/review',methods=['GET','POST'])
def final():
	try:
		if session[cur_posts[-1]+'_choice']:
			if request.method == "GET":
				#Here we render the review page by passing the session dictionary as the parameter
				return render_template('review_page.html',session=dict(session),cur_posts=cur_posts)
			else:
				return redirect(url_for('over'))
	except Exception as e:
		print(e)
		return redirect(url_for('load_post',post=cur_posts[-1]))

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
			return render_template('dashboard.html',voting_started=voting_started,voting_ended=voting_ended,no_of_codes=no_of_codes,house_choice=house_choice,color_scheme=color_scheme,makeupper=makeupper)
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
				load_list = [['Head Boy','Head Girl','Sports Captain','Cultural Captain'],['Assistant Head Boy','Assistant Head Girl','Sports Vice Captain','Cultural Vice Captain'],['Kingfisher Captain','Flamingo Captain','Falcon Captain','Eagle Captain'],['Kingfisher Vice Captain','Flamingo Vice Captain','Falcon Vice Captain','Eagle Vice Captain']]
				custom_post_load_list = get_custom_post_load_list()
				return render_template('show_candidates.html',candidates=candidates,str=str,voting_started=voting_started,voting_ended=voting_ended,getcolor=getcolor,load_list=load_list,title=title,startswith=startswith,custom_posts=custom_post_load_list,len=len)
			else:
				updated_candidates = request.form['candvalue']#fetches the parsed new candidates list
				updated_candidates = eval(updated_candidates)
				for post in updated_candidates:#filters the candidates
					l = updated_candidates[post]
					new_l = []
					for y in l:
						y = y.strip()
						if y != '':
							new_l.append(y)
					updated_candidates[post] = new_l
				
				candidates = updated_candidates
				database_linker.initializing(candidates)
				return redirect(url_for('show_candidate'))
		else:
			return redirect(url_for('admin_page'))
	except Exception as  e:
		print(e)
		return redirect(url_for('admin_page'))

@app.route('/add_custom_post',methods=['GET', 'POST'])
def add_custom_post():
	try:
		if session['logged'] == True:
			global cur_posts,candidates
			if request.method== 'GET':
				return render_template('add_custom_post.html',str=str,cur_post=cur_posts,u=underscore_remove,replace_house_name=replace_house_name)
			else:
				response = request.get_json()
				new_post_name = response['post_name'].lower().strip()
				cur_posts_order = []
				if new_post_name != '':
					if not response['for_house']:
						cur_posts_order = [new_post_name.replace(' ','_') if pname == 'new_post' else pname for pname in response['cur_posts_order']]
						candidates[new_post_name.replace(' ','_')] = []
					else:
						cur_posts_order = [house_choice+'_'+new_post_name.replace(' ','_') if pname == 'new_post' else pname for pname in response['cur_posts_order']]
						for house in ['kingfisher','falcon','flamingo','eagle']:
							candidates[house+'_'+new_post_name.replace(' ','_')] = []
						new_post_name = house_choice+'_'+new_post_name.replace(' ','_')
					cur_posts_order = [post.replace('house',house_choice) if post.startswith('house') else post for post in cur_posts_order]

					database_linker.initializing(candidates)
					cur_posts = cur_posts_order
				else:
					return redirect(url_for('add_custom_post'))
		else:
			return redirect(url_for('admin_page'))
	except Exception as  e:
		print(e)
		return redirect(url_for('admin_page'))

@app.route('/delete_post',methods=['GET', 'POST'])
def delete_post():
	try:
		global cur_posts,candidates
		if session['logged'] == True:
			if request.method == 'GET':
				return render_template('delete_post.html',cur_post=cur_posts,u=underscore_remove,replace_house_name=replace_house_name)
			else:
				response = request.get_json()
				post_to_delete = response['post_to_delete'].strip()
				post_to_delete = post_to_delete.replace(' ','_').lower()
				if post_to_delete.startswith('house'):
					post_to_delete = post_to_delete.replace('house',house_choice)

				try:
					cur_posts.remove(post_to_delete)
					for post in list(candidates.keys()):
						if post_to_delete.startswith(house_choice):
							if post.endswith("".join(["_"+x for x in post_to_delete.split('_')[1:]])):
								del candidates[post]
						else:
							if post == post_to_delete:
								del candidates[post]
				except Exception as e:
					print(e)
					pass

		else:
			return redirect(url_for('admin_page'))
	except:
		return redirect(url_for('admin_page'))

@app.route('/voting_settings')
def voting_settings():
	try:
		if session['logged'] == True:
			not_there = all_photo_check(set_photos_path())
			return render_template('voting_settings.html',d=candidates,valid=voting_started,no_of_codes=no_of_codes,not_there=not_there,makeupper=makeupper,len=len,underscore_remove=underscore_remove)
		else:
			return redirect(url_for('admin_page'))
	except Exception as e:
		print(e)
		return redirect(url_for('admin_page'))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
	try:
		if session['logged'] == True:
			global house_choice,no_of_codes
			if request.method == "GET":
				return render_template('settings.html',house_choice=house_choice,no_of_codes=no_of_codes)
			elif request.method == "POST":
				#Here the admin changes the password for the local admin
				#This block confirms the changes
				global cur_posts
				old_house_choice = house_choice
				house_choice = request.form['hc']
				house_choice = house_choice.lower()
				local_functions.store_house_choice(house_choice)
				update_cur_post(old_house_choice,house_choice)

				#This block confirms the changes
				changed_pwd = request.form['changed_pwd']
				if not sec_code.pass_is_valid(changed_pwd) and changed_pwd != '':
					sec_code.pass_set(changed_pwd)

				changed_no_of_codes = request.form['changed_no_of_codes']
				t = eval(changed_no_of_codes.split()[0])
				if type(t) is int:
					if t>0:
						no_of_codes = t
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
	global voting_started,voting_ended
	voting_started = True
	voting_ended = False
	sec_code.code_print()
	return redirect(url_for("voting_settings"))

@app.route('/stop_voting')
def stop_voting():#This function is called when the admin presses the stop voting button
	database_linker.results_print()
	global voting_started,voting_ended
	voting_started = False
	voting_ended = True
	return redirect(url_for('result'))
	#return redirect(url_for('dashboard'))

@app.route('/results')
def result():
	return render_template('results.html')
	#return redirect('C:/Users/USER/Documents/GitHub/NCFE-EVM/results.pdf')

#Function to send photos to the webpage
@app.route('/uploads/<path:filename>')
def download_file(filename):#Function to download the file
	try:
		x = get_image_folder_path(app.config['CANDIDATE_PHOTOS'],filename)
		folder = "".join([y+'/' for y in x.split('/')[:-1]])
		filename = x.split('/')[-1]
		return send_from_directory(folder,filename, as_attachment=True)
	except:
		pass

def get_image_folder_path(path,cand_name):#Function that returns file with any extension
	for tup in os.walk(path):
		for file in tup[2]:
			if file.lower()[:len(file)-file[::-1].index('.')-1] == cand_name.lower():
				if not file.lower().startswith('default'):
					return tup[0].replace('\\', '/')+'/'+file

@app.route('/download_results')
def download_results():
	x = "".join([y+'\\' for y in app.config['CANDIDATE_PHOTOS'].split('\\')[:-1]])
	try:
		return send_from_directory(x,filename='results.pdf')
	except Exception as e:
		print(e)
		return str(e)

#Function to check if all the candidates' photos are there
def all_photo_check(path):
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
	return not_there

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
	if 'home_choice' in dt:
		del dt['home_choice']
	dt1 = {}
	for x in dt:
		if dt[x] != 'DNE':
			dt1[x] = dt[x]
	database_linker.add_votes_to_db(dict(dt1))

def underscore_remove(t):#This function is used to remove all the underscores in string and return it in captial
	t = t.split('_')
	l = ''
	for x in t:
		l+=x
		l+=' '
	return l.upper()

def makeupper(t):#returns the uppercase string
	return t.upper()

def title(t):
	return t.title().replace('_',' ')

def startswith(a,b):
	return a.startswith(b)

def getcolor(t):
	t = t.split()[0].lower()
	house_color = {'kingfisher':'kf','flamingo':'fl','falcon':'fa','eagle':'ea','major':'ma'}
	for x in house_color:
		if x == t:
			return house_color[t]
	return house_color['major']

def get_custom_post_load_list():
	load_list = ['Head Boy','Head Girl','Sports Captain','Cultural Captain','Kingfisher Captain','Flamingo Captain','Falcon Captain','Eagle Captain','Assistant Head Boy','Assistant Head Girl','Sports Vice Captain','Cultural Vice Captain','Kingfisher Vice Captain','Flamingo Vice Captain','Falcon Vice Captain','Eagle Vice Captain']
	load_list = [y.lower().replace(' ',"_") for y in load_list]
	cp = candidates.keys()
	result = list(set(load_list)^set(cp))
	filtered_result = []
	for post in result:
		if post not in load_list:
			filtered_result.append(post)
	result = filtered_result
	final = []
	temp = []
	temp1 = []
	for post in result:
		if is_house_post(post):
			if post.startswith('kingfisher'):
				temp1.append(post)
		else:
			temp.append(post)
	for post in temp1:
		post = post.split('_')[1:]
		for house in ["kingfisher",'flamingo','falcon','eagle']:
			final.append(house+"".join(['_'+y for y in post]))
	final.extend(temp)
	return final

def is_house_post(t):
	for x in ["kingfisher",'falcon','flamingo','eagle']:
		if t.lower().startswith(x):
			return True
	return False

def replace_house_name(l):
	return [post.replace(house_choice,'house') if post.startswith(house_choice) else post for post in l]

def fetch_changed_house_choice():
	hc = request.values.get('house_choice')

def add_to_cur_posts():#To create teh current posts variable
	global cur_posts
	l = ['head_boy','head_girl','assistant_head_boy','assistant_head_girl','cultural_captain','cultural_vice_captain','sports_captain','sports_vice_captain',house_choice+'_captain',house_choice+'_vice_captain']
	for y in l:
		if y in candidates:
			if len(candidates[y])>1:
				cur_posts.append(y)

def update_cur_post(old_choice,cur_choice):#To update the house posts
	global cur_posts
	temp_posts = []
	for post in cur_posts:
		temp = post.split('_')
		if temp[0] == old_choice:
			temp_posts.append(cur_choice + ''.join(['_'+y for y in temp[1:]]))
		else:
			temp_posts.append(post)
	cur_posts = temp_posts


def set_photos_path():#This function sets the path for the candidates photos in the app.config
	candidate_pictures = 'candidate_photos'
	if getattr(sys, 'frozen', False):
		application_path = os.path.dirname(sys.executable)
	elif __file__:
		application_path = os.path.dirname(__file__)
	photos_path = application_path + '/' + candidate_pictures 
	local_functions.resize_images_in_folder(photos_path)
	app.config['CANDIDATE_PHOTOS'] = photos_path
	return photos_path

def colors_set():
	global color_scheme
	#Format: (background_color,box,text)
	color_scheme['kingfisher'] = ('#30a4e2','#036f96','#ffffff')
	color_scheme['flamingo']  = ('#E05707','#A63A0F','#ffffff')
	color_scheme['falcon']  = ('#7E58BF','#432A73','#ffffff')
	color_scheme['eagle']  = ('#B81A1C','#750407','#ffffff')
	color_scheme['major']  = ('#161616','#212121','#FCED47')


def start():
	#This is the main method for starting the app
	global candidates
	candidates = database_linker.get_cands_from_db()
	add_to_cur_posts()
	set_photos_path()
	colors_set()
	app.run(debug=True)

start()
