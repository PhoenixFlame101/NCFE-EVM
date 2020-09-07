from flask import Flask,redirect,url_for,render_template,request,session

app = Flask(__name__,template_folder='./GUI/')
app.secret_key = 'abc'

valid = False

house_choice = 'eagle'
cur_posts = []
candidates = {}

def cc():#Temporary testing function to create the candidates dictionary
    global candidates
    for x in ['head_boy','assistant_head_boy','assistant_head_girl','cultural_captain','cultural_vice_captain','sports_captain','sports_vice_captain','kingfisher_captain','kingfisher_vice_captain','flamingo_captain','flamingo_vice_captain','falcon_captain','falcon_vice_captain','eagle_vice_captain']:
        candidates[x] = ['A','B','C','D']

def add_to_cur_posts():#To create teh current posts variable
    global cur_posts
    l = ['head_boy','head_girl','assistant_head_boy','assistant_head_girl','cultural_captain','cultural_vice_captain','sports_captain','sports_vice_captain',house_choice+'_captain',house_choice+'_vice_captain']
    for y in l:
        if y in candidates:
            if len(candidates[y])>1:
                cur_posts.append(y)

def prev_post(cur_post):#This function tells the back button which page to go back to
    cur_index = cur_posts.index(cur_post)
    if cur_index>0:
        return cur_posts[cur_index-1]
    else:
        return 'home'

def next_post(cur_post):#This function talks about which page to go next
    p = cur_post
    x = cur_posts.index(p)
    if x<len(cur_posts)-1:
        return cur_posts[x+1]
    else:
        return 'final'

@app.route('/',methods=["GET",'POST'])
def home():
    if request.method == "GET": 
        #This part shows renders the template (get template)
        session["logged"] = False
        return render_template('entry_page.html')
    else:
        valid = True
        #This part whether the security code is valid by asking the database
        return redirect(url_for('major_post',post=cur_posts[0]))

@app.route('/<post>',methods=['GET','POST'])
def major_post(post):
    try:
        if valid or (prev_post(post)+'_choice') in session:#error for head_boy since we have to check the validity there
            next_p = next_post(post)#out of index error
            p = post
            pc = p + "_choice"

            if request.method =='GET':
                if p in candidates:
                    if len(candidates[p]) == 1:
                        if (cur_posts[-1]+'_choice') not in session:
                            session[pc] = 'DNE'
                            return redirect(url_for(next_p))
                        else:
                            return redirect("final")
                    else:
                        return render_template('gen_page.html',p=post,d=candidates,house_choice=house_choice,prev_post=prev_post,next_post=next_post)
                else:
                    #Why is this block even there
                    session[pc] = "DNE"
                    return redirect(url_for(next_p))
            elif request.method =='POST':
                session[pc] = request.form[pc]
                return redirect(url_for(next_p))
    except Exception as e:
        print(e)
        return redirect(url_for(prev_post(post)))


def start():
    cc()
    add_to_cur_posts()

    print(cur_posts)
    print(candidates)

    app.run(debug=True)


start()