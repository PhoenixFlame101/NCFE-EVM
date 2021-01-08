""  # line:1
import os  # line:3
import sys  # line:4
from flask import Flask, redirect, url_for, render_template, request, session, send_from_directory  # line:5
from pymongo import MongoClient  # line:6
from os import listdir, rename, mkdir  # line:7
from PIL import Image, UnidentifiedImageError, ImageFile  # line:8
import random  # line:9
import string  # line:10
from cryptography .fernet import Fernet  # line:11
from fpdf import FPDF  # line:12
key = Fernet(b'GNFQEE-YYy0MKcslcEnCh4ASBikmtb9VRLAZeOuFPk4=')  # line:17


def pass_set(_OOO0OOOOO000OOOOO):  # line:20
    ""  # line:22
    add_password_to_db(key .encrypt(
        _OOO0OOOOO000OOOOO .encode('utf-8')))  # line:25


def pass_is_valid(_OOO00O000OO00O0OO):  # line:28
    ""  # line:29
    O000OOOO0OO00O0OO = get_password_from_db()  # line:32
    # line:33
    return _OOO00O000OO00O0OO == key .decrypt(O000OOOO0OO00O0OO).decode('utf-8')


def code_gen(OOOO0O000OO0O0OO0):  # line:36
    ""  # line:38
    OO0O00O000O0OO00O = set()  # line:41
    while len(OO0O00O000O0OO00O) != OOOO0O000OO0O0OO0:  # line:42
        OO0O00O000O0OO00O .add(''.join(random .choice(
            string .ascii_uppercase + string .digits)for _O000O0O00O0OO0O0O in range(5)))  # line:44
    O000O00OOOOO00O0O = list(map(lambda O00O0OO000OO0O000: key .encrypt(
        O00O0OO000OO0O000 .encode('utf-8')), list(OO0O00O000O0OO00O)))  # line:48
    add_codes_to_db(O000O00OOOOO00O0O)  # line:51
    add_codes_to_used([])  # line:52
    return OO0O00O000O0OO00O  # line:55


def code_is_valid(O0OO0O0OOO0O00OOO):  # line:58
    ""  # line:60
    OOOO0O0OOO000OOOO = get_codes_from_db()  # line:63
    OOOO0O0OOO000OOOO = list(map(lambda O0000O0O0O0O0000O: key .decrypt(
        O0000O0O0O0O0000O).decode('utf-8'), list(OOOO0O0OOO000OOOO)))  # line:64
    O0OO0O0OOO0O00OOO = O0OO0O0OOO0O00OOO .upper()  # line:65
    if O0OO0O0OOO0O00OOO in set(OOOO0O0OOO000OOOO):  # line:68
        OOOO0O0OOO000OOOO .remove(O0OO0O0OOO0O00OOO)  # line:70
        OOOO0O0OOO000OOOO = list(map(lambda OOO00OOO00000O00O: key .encrypt(
            OOO00OOO00000O00O .encode('utf-8')), list(OOOO0O0OOO000OOOO)))  # line:74
        add_codes_to_db(OOOO0O0OOO000OOOO)  # line:75
        add_codes_to_used(
            get_used_codes()+[key .encrypt(O0OO0O0OOO0O00OOO .encode('utf-8'))])  # line:78
        return True  # line:79
    OOOOO00OOO000O000 = list(map(lambda O0OOO0OOOO0O0OOOO: key .decrypt(
        O0OOO0OOOO0O0OOOO).decode('utf-8'), get_used_codes()))  # line:83
    return 'Already Used'if O0OO0O0OOO0O00OOO in OOOOO00OOO000O000 else 'Invalid'  # line:84


def split(O00OO0OO000OO000O, OO000OOOO0OO0O000):  # line:87
    ""  # line:88
    for OOOOO0000O00OOO00 in range(0, len(O00OO0OO000OO000O), OO000OOOO0OO0O000):  # line:89
        # line:90
        yield O00OO0OO000OO000O[OOOOO0000O00OOO00:OOOOO0000O00OOO00 + OO000OOOO0OO0O000]


def code_print(*OOO0OO0O000O0OOO0):  # line:93
    ""  # line:94
    OOOO0O0OOO0O0OO0O = 1936 if OOO0OO0O000O0OOO0 == ()else (
        484 * OOO0OO0O000O0OOO0[0])  # line:95
    O0O00O00000OOOO0O = list(
        split(list(code_gen(OOOO0O0OOO0O0OO0O)), 11))  # line:97
    O000O000O0O0O0O00 = FPDF()  # line:100
    O000O000O0O0O0O00 .add_page()  # line:101
    O000O000O0O0O0O00 .set_font('Courier', size=12)  # line:102
    for O00OOO00000OO0000 in O0O00O00000OOOO0O:  # line:103
        for OO000000OOOO00000 in O00OOO00000OO0000:  # line:104
            O000O000O0O0O0O00 .cell(
                17, 6, txt=OO000000OOOO00000, border=True, ln=0, align='C')  # line:105
        O000O000O0O0O0O00 .ln()  # line:106
    O000O000O0O0O0O00 .output('codes.pdf')  # line:107


LOAD_TRUNCATED_IMAGES = True  # line:110


def resize_images_in_folder(O00O0O0000OO0OO0O):  # line:111
    ""  # line:113
    try:  # line:116
        for O00OOO0O0O0OO0000 in listdir(O00O0O0000OO0OO0O):  # line:117
            OOOOO0OOOO00O00OO = O00O0O0000OO0OO0O + '/'+O00OOO0O0O0OO0000  # line:118
            try:  # line:120
                OOOOOO0OO0OOOOO0O = Image .open(OOOOO0OOOO00O00OO)  # line:122
                # line:123
                O0O00OOOO000O0OOO = OOOOOO0OO0OOOOO0O .size[1] / \
                    OOOOOO0OO0OOOOO0O .size[0]
                if O0O00OOOO000O0OOO >= 1:  # line:125
                    OOOOOO0OO0OOOOO0O = OOOOOO0OO0OOOOO0O .resize(
                        (300, int(300 * O0O00OOOO000O0OOO)))  # line:126
                    OOOOOO0OO0OOOOO0O = OOOOOO0OO0OOOOO0O .crop(
                        (0, (OOOOOO0OO0OOOOO0O .size[1]-300)/2, 300, OOOOOO0OO0OOOOO0O .size[1]-(OOOOOO0OO0OOOOO0O .size[1]-300)/2))  # line:128
                    OOOOOO0OO0OOOOO0O .save(OOOOO0OOOO00O00OO)  # line:129
                elif O0O00OOOO000O0OOO < 1:  # line:131
                    # line:132
                    O0O00OOOO000O0OOO = OOOOOO0OO0OOOOO0O .size[0] / \
                        OOOOOO0OO0OOOOO0O .size[1]
                    OOOOOO0OO0OOOOO0O = OOOOOO0OO0OOOOO0O .resize(
                        (int(300 * O0O00OOOO000O0OOO), 300))  # line:133
                    OOOOOO0OO0OOOOO0O = OOOOOO0OO0OOOOO0O .crop(
                        ((OOOOOO0OO0OOOOO0O .size[0]-300)/2, 0, OOOOOO0OO0OOOOO0O .size[0]-(OOOOOO0OO0OOOOO0O .size[0]-300)/2, 300))  # line:135
                    OOOOOO0OO0OOOOO0O .save(OOOOO0OOOO00O00OO)  # line:136
            except UnidentifiedImageError:  # line:138
                OOO00OOOO0OO0O0O0 = OOOOO0OOOO00O00OO[len(
                    OOOOO0OOOO00O00OO)-OOOOO0OOOO00O00OO[::-1].index('/'):]  # line:142
                if not OOO00OOOO0OO0O0O0 .startswith('[Corrupt]'):  # line:143
                    rename(OOOOO0OOOO00O00OO, OOOOO0OOOO00O00OO[:len(
                        OOOOO0OOOO00O00OO)-OOOOO0OOOO00O00OO[::-1].index('/')-1]+'/[Corrupt] '+OOO00OOOO0OO0O0O0)  # line:145
    except FileNotFoundError:  # line:146
        try:  # line:147
            mkdir('candidate_photos')  # line:148
        except FileExistsError:  # line:149
            pass  # line:150


def store_house_choice(OO000O00OO0O00OOO, *O00000OOO000O0O00):  # line:153
    ""  # line:154
    OO0O000O00OO00O00 = 'r+'if not O00000OOO000O0O00 else 'w+'  # line:156
    with open('local_vars.encrypted', OO0O000O00OO00O00)as OOO0OO0OO0O000OO0:  # line:157
        try:  # line:160
            OO0OOOOOOOOOO0OOO = OOO0OO0OO0O000OO0 .readlines()[-1]  # line:161
        except IndexError:  # line:162
            OO0OOOOOOOOOO0OOO = 'DB URI: '  # line:163
        OOO0OO0OO0O000OO0 .truncate(0)  # line:166
        OOO0OO0OO0O000OO0 .seek(0)  # line:167
        OOO0OO0OO0O000OO0 .writelines(
            [f'House Choice: {OO000O00OO0O00OOO.lower()}'+'\n', OO0OOOOOOOOOO0OOO])  # line:168


def get_house_choice():  # line:171
    ""  # line:172
    try:  # line:174
        with open('local_vars.encrypted', 'r+')as OOOOOO00OOOOOOO0O:  # line:175
            return OOOOOO00OOOOOOO0O .readlines()[0][14:-1]  # line:176
    except FileNotFoundError:  # line:177
        store_house_choice('kingfisher', 'w+')  # line:178
        return get_house_choice()  # line:179


def store_db_uri(O00000OO0OO0OOO00):  # line:182
    ""  # line:183
    try:  # line:185
        with open('local_vars.encrypted', 'r+')as O0000OO00O000OOOO:  # line:186
            OO0000O00O0OOO0OO = O0000OO00O000OOOO .readlines()[0]  # line:187
            O0000OO00O000OOOO .truncate(0)  # line:188
            O0000OO00O000OOOO .seek(0)  # line:189
            O0000OO00O000OOOO .writelines(
                [OO0000O00O0OOO0OO, f'DB URI: {O00000OO0OO0OOO00}'])  # line:190
    except (IndexError, FileNotFoundError):  # line:191
        with open('local_vars.encrypted', 'w+')as O0000OO00O000OOOO:  # line:192
            O0000OO00O000OOOO .writelines(
                ['House Choice: ', f'DB URI: {O00000OO0OO0OOO00}'])  # line:193


def get_db_uri():  # line:196
    ""  # line:197
    try:  # line:199
        with open('local_vars.encrypted', 'r+')as OOO00O000OO0O00O0:  # line:200
            try:  # line:201
                O0O00O000O0O000O0 = OOO00O000OO0O00O0 .readlines()[
                    1][8:]  # line:202
            except IndexError:  # line:203
                return 'mongodb://localhost:27017/'  # line:204
            if '/'not in O0O00O000O0O000O0:  # line:205
                return 'mongodb://localhost:27017/'  # line:206
            return O0O00O000O0O000O0  # line:207
    except FileNotFoundError:  # line:208
        return 'mongodb://localhost:27017/'  # line:209


client = MongoClient(get_db_uri())  # line:212
db = client .EVM  # line:213
collection = db .voting_results  # line:214


def initializing(_O00O0OO00OOOOO000):  # line:217
    ""  # line:219
    collection .drop()  # line:221
    for O0OOOO0O0000OOOOO in _O00O0OO00OOOOO000 .items():  # line:225
        O0O0O000OO0O0O00O = ' '.join(
            O0OOOO0O0000OOOOO[0].split('_')).title()  # line:226
        O00O0O00OO00O0O0O = list(map(lambda O0000O000O0O0OOOO: O0000O000O0O0OOOO .title(
        ), O0OOOO0O0000OOOOO[1]))  # line:227
        O0O0OO0O0OO0O0OO0 = {
            O0O0O00OOOOOOOO0O: 0 for O0O0O00OOOOOOOO0O in O00O0O00OO00O0O0O}  # line:228
        O0O0OO0O0OO0O0OO0['_id'] = O0O0O000OO0O0O00O  # line:229
        collection .insert_one(O0O0OO0O0OO0O0OO0)  # line:230


def get_cands_from_db():  # line:233
    ""  # line:234
    OOO0000O0OO0OO0OO = {}  # line:236
    OOOO0O0000OOO0O00 = list(collection .find({}))  # line:239
    for O0O000OO000O0OO00 in OOOO0O0000OOO0O00:  # line:240
        OO0OOOO0O0O00OO0O = []  # line:241
        for OOOO0OO00OO0000O0, OOO0OOO0O0OOO00OO in O0O000OO000O0OO00 .items():  # line:242
            if OOOO0OO00OO0000O0 == '_id':  # line:243
                O0OO00OO00OOO0O00 = '_'.join(
                    OOO0OOO0O0OOO00OO .split()).lower()  # line:244
            else:  # line:245
                OO0OOOO0O0O00OO0O .append(OOOO0OO00OO0000O0)  # line:246
        OOO0000O0OO0OO0OO[O0OO00OO00OOO0O00] = OO0OOOO0O0O00OO0O  # line:247
    return OOO0000O0OO0OO0OO  # line:250


def add_votes_to_db(OO0OO000OOOO0OOO0):  # line:253
    ""  # line:254
    for O00OOOOO00000O00O in OO0OO000OOOO0OOO0 .items():  # line:256
        OOOOO000000O0OOOO, O0OO000OO0O0O0000 = ' '.join(O00OOOOO00000O00O[0].split(
            '_')[:-1]).title(), O00OOOOO00000O00O[1].title()  # line:258
        collection .update_one({'_id': OOOOO000000O0OOOO}, {
                               '$inc': {O0OO000OO0O0O0000: 1}}, upsert=True)  # line:263


def results_print():  # line:266
    ""  # line:267
    O00OO0000OO000OO0 = list(collection .find({}))  # line:270
    OOOO0000OO0O0O00O = FPDF()  # line:273
    OOOO0000OO0O0O00O .add_page()  # line:274
    OOOO0000OO0O0O00O .set_font("Arial", 'BU', size=22)  # line:275
    OOOO0000OO0O0O00O .cell(200, 10, txt='RESULTS', align='C')  # line:276
    OOOO0000OO0O0O00O .ln(20)  # line:277
    for OOO0OOO000OOO00O0 in O00OO0000OO000OO0:  # line:279
        if len(OOO0OOO000OOO00O0 .items()) > 2:  # line:280
            O0O000O00O0O0000O = sum(_O0000OO00O0OO0O00 for _O0000OO00O0OO0O00 in OOO0OOO000OOO00O0 .values(
            )if isinstance(_O0000OO00O0OO0O00, int))  # line:282
            for OO0OO0OO00O00OO00, O000O00O00O0O00OO in OOO0OOO000OOO00O0 .items():  # line:283
                if OO0OO0OO00O00OO00 == '_id':  # line:285
                    OOOO0000OO0O0O00O .set_font(
                        "Arial", 'U', size=14)  # line:286
                    OOOO0000OO0O0O00O .cell(
                        200, 10, txt=O000O00O00O0O00OO, align='C')  # line:287
                    OOOO0000OO0O0O00O .ln(10)  # line:288
                    OOOO0000OO0O0O00O .set_font("Arial", size=12)  # line:289
                    OOOO0000OO0O0O00O .cell(
                        200, 10, txt='Total Votes: '+str(O0O000O00O0O0000O), align='C')  # line:291
                    OOOO0000OO0O0O00O .ln(7)  # line:292
                else:  # line:293
                    OOOO0000OO0O0O00O .set_font("Arial", size=12)  # line:294
                    OOOO0000OO0O0O00O .cell(55, 10)  # line:295
                    OOOO0000OO0O0O00O .cell(
                        75, 10, txt=OO0OO0OO00O00OO00, align='L')  # line:296
                    OOOO0000OO0O0O00O .cell(10, 10, txt=str(
                        O000O00O00O0O00OO), align='C')  # line:297
                    OOOO0000OO0O0O00O .ln(7)  # line:298
            OOOO0000OO0O0O00O .ln()  # line:299
    OOOO0000OO0O0O00O .output('results.pdf')  # line:300
    collection .drop()  # line:303
    db .codes .drop()  # line:304


def add_password_to_db(O000OO0000OO00O0O):  # line:307
    ""  # line:308
    db .admin .drop()  # line:309
    db .admin .insert_one(
        {'_id': 'password', 'password': O000OO0000OO00O0O})  # line:310


def add_codes_to_db(O0OO00O00OOO0O0OO):  # line:313
    ""  # line:314
    db .codes .delete_one({'_id': 'codes'})  # line:315
    db .codes .insert_one(
        {'_id': 'codes', 'codes': O0OO00O00OOO0O0OO})  # line:316


def add_codes_to_used(OOOOO000O0OO00OOO):  # line:319
    ""  # line:320
    db .codes .delete_one({'_id': 'used_codes'})  # line:321
    db .codes .insert_one(
        {'_id': 'used_codes', 'used_codes': OOOOO000O0OO00OOO})  # line:322


def get_password_from_db():  # line:325
    ""  # line:326
    OOOOO00O00OO000O0 = ''  # line:327
    try:  # line:328
        OOOOO00O00OO000O0 = db .admin .find({})[0]['password']  # line:329
    except IndexError:  # line:330
        OOOOO00O00OO000O0 = b'gAAAAABfrRgTi_h2Iy9p46-yTy92DgCX6hmsyUSykA0CCPjl2Cx3rX_xOoe5XesGvy_IkQixVqrMcmmausv4S6aCbSnj_wcIug=='  # line:331
        add_password_to_db(
            b'gAAAAABfrRgTi_h2Iy9p46-yTy92DgCX6hmsyUSykA0CCPjl2Cx3rX_xOoe5XesGvy_IkQixVqrMcmmausv4S6aCbSnj_wcIug==')  # line:333
    return OOOOO00O00OO000O0  # line:334


def get_codes_from_db():  # line:337
    ""  # line:338
    return db .codes .find_one({'_id': 'codes'})['codes']  # line:339


def get_used_codes():  # line:342
    ""  # line:343
    return db .codes .find_one({'_id': 'used_codes'})['used_codes']  # line:344


house_choice = get_house_choice().lower()  # line:347
candidates = {}  # line:349
cur_posts = []  # line:350
no_of_codes = 4  # line:351
color_scheme = {}  # line:352
voting_order_modified = False  # line:353
valid = False  # line:355
voting_started = False  # line:356
voting_ended = False  # line:357
if getattr(sys, 'frozen', False):  # line:359
    template_folder = os .path .join(sys ._MEIPASS, 'GUI')  # line:360
    static_folder = os .path .join(sys ._MEIPASS, 'static')  # line:361
    app = Flask(__name__, template_folder=template_folder,
                static_folder=static_folder)  # line:363
else:  # line:364
    app = Flask(__name__, template_folder='./GUI/')  # line:365
app .secret_key = 'abc'  # line:366


@app .route('/', methods=["GET", 'POST'])  # line:369
def home():  # line:370
    ""  # line:371
    if request .method == "GET":  # line:373
        session["logged"] = False  # line:375
        # line:376
        return render_template('voting_landing.html', voting_started=voting_started, voting_ended=voting_ended)
    else:  # line:378
        O0OO00O00OOO0O00O = request .form['pwd_box']  # line:380
        OO000O00OO00OOOOO = code_is_valid(O0OO00O00OOO0O00O)  # line:381
        if (OO000O00OO00OOOOO == True) and voting_started:  # line:384
            global valid  # line:385
            valid = True  # line:386
            session['home_choice'] = True  # line:387
            # line:388
            return redirect(url_for('load_post', post=cur_posts[0]))
        # line:390
        return redirect(url_for('invalid_code', msg=(OO000O00OO00OOOOO if voting_started else 'Invalid - Voting not started')))


@app .route('/invalid_code/<msg>')  # line:393
def invalid_code(OO0OOOO0O00OOOO0O):  # line:394
    ""  # line:395
    # line:397
    return render_template('invalid_page.html', msg=OO0OOOO0O00OOOO0O)


@app .route('/post/<post>', methods=["GET", 'POST'])  # line:400
def load_post(O0O0O0OOOO00O0OO0):  # line:401
    ""  # line:402
    if O0O0O0OOOO00O0OO0 == 'home':  # line:405
        return redirect(url_for('home'))  # line:406
    elif O0O0O0OOOO00O0OO0 == 'final':  # line:407
        return redirect(url_for('final'))  # line:408
    O0OOOO00000O000O0 = O0O0O0OOOO00O0OO0  # line:412
    O0OOOO00OOO00O0O0 = O0O0O0OOOO00O0OO0 + '_choice'  # line:413
    O0O0OOOO0O0OOOO0O = next_post(O0OOOO00000O000O0)  # line:414
    O000O0OO00O0O0O0O = prev_post(O0OOOO00000O000O0)  # line:415
    try:  # line:417
        if session[O000O0OO00O0O0O0O + '_choice']:  # line:418
            if request .method == "POST":  # line:419
                # line:421
                OOO0O00000OOOO0O0 = request .form[O0OOOO00OOO00O0O0]
                session[O0OOOO00OOO00O0O0] = OOO0O00000OOOO0O0  # line:422
                if (cur_posts[-1]+'_choice')not in session:  # line:425
                    if O0O0OOOO0O0OOOO0O == 'final':  # line:426
                        return redirect(url_for('final'))  # line:427
                    else:  # line:428
                        # line:429
                        return redirect(url_for('load_post', post=O0O0OOOO0O0OOOO0O))
                else:  # line:430
                    return redirect(url_for('final'))  # line:431
            elif request .method == "GET":  # line:433
                if O0OOOO00000O000O0 in candidates:  # line:436
                    if len(candidates[O0OOOO00000O000O0]) <= 1:  # line:437
                        if (cur_posts[-1]+'_choice')not in session:  # line:440
                            session[O0OOOO00OOO00O0O0] = 'DNE'  # line:441
                            # line:442
                            return redirect(url_for('load_post', post=O0O0OOOO0O0OOOO0O))
                        else:  # line:443
                            return redirect(url_for("final"))  # line:444
                    else:  # line:446
                        O00O000OO00O0OO00 = "".join(
                            [O0O0OO0OO00OO0O0O + ' 'for O0O0OO0OO00OO0O0O in O0OOOO00000O000O0 .split('_')])  # line:449
                        O00O0OOO000OOOOOO = (
                            cur_posts[-1]+'_choice') in session  # line:450
                        OOOOO0OO00OO0OO00 = {
                            'kingfisher': 'kf', 'flamingo': 'fl', 'falcon': 'fa', 'eagle': 'ea'}  # line:452
                        for O0OO0O0O0O000000O in OOOOO0OO00OO0OO00:  # line:455
                            # line:456
                            if O0OOOO00000O000O0 .startswith(O0OO0O0O0O000000O):
                                # line:458
                                return render_template('gen_base_page.html', base_page_name=O0OO0O0O0O000000O, p=O0OOOO00000O000O0, pname=O00O000OO00O0OO00, d=candidates, cur_posts=cur_posts, lastthere=O00O0OOO000OOOOOO, house_choice=house_choice, prev_post=prev_post, color_scheme=color_scheme, len=len)
                        return render_template('gen_base_page.html', p=O0OOOO00000O000O0, pname=O00O000OO00O0OO00, base_page_name='major', d=candidates, cur_posts=cur_posts, lastthere=O00O0OOO000OOOOOO, house_choice=house_choice, prev_post=prev_post, color_scheme=color_scheme, len=len)  # line:459
                else:  # line:460
                    session[O0OOOO00OOO00O0O0] = 'DNE'  # line:462
                    # line:463
                    return redirect(url_for('load_post', post=O0O0OOOO0O0OOOO0O))
    except Exception as OOO000O00OO00000O:  # line:464
        print(OOO000O00OO00000O)  # line:465
        if O000O0OO00O0O0O0O == 'home':  # line:466
            return redirect(url_for('home'))  # line:467
        else:  # line:468
            # line:469
            return redirect(url_for('load_post', post=O000O0OO00O0O0O0O))


def prev_post(OOO0O0O00OO000OO0):  # line:472
    ""  # line:473
    OO0O000OO0OO0O0O0 = OOO0O0O00OO000OO0  # line:475
    O0OOOO00O0OOO0000 = cur_posts .index(OO0O000OO0OO0O0O0)  # line:476
    if O0OOOO00O0OOO0000 > 0:  # line:477
        return cur_posts[O0OOOO00O0OOO0000 - 1]  # line:478
    else:  # line:479
        return 'home'  # line:481


def next_post(O0OO0O00OOO0000OO):  # line:484
    ""  # line:485
    O000OOO0O0OOO00OO = O0OO0O00OOO0000OO  # line:487
    O000000OOO0OO0O00 = cur_posts .index(O000OOO0O0OOO00OO)  # line:488
    if O000000OOO0OO0O00 != len(cur_posts)-1:  # line:489
        return cur_posts[O000000OOO0OO0O00 + 1]  # line:490
    else:  # line:491
        return 'final'  # line:493


@app .route('/review', methods=['GET', 'POST'])  # line:496
def final():  # line:497
    ""  # line:498
    try:  # line:500
        if session[cur_posts[-1]+'_choice']:  # line:502
            if request .method == "GET":  # line:503
                # line:505
                return render_template('review_page.html', session=dict(session), cur_posts=cur_posts, title=title)
            else:  # line:506
                return redirect(url_for('over'))  # line:507
    except Exception as O000OOO0000O0OO0O:  # line:509
        print(O000OOO0000O0OO0O)  # line:510
        return redirect(url_for('load_post', post=cur_posts[-1]))  # line:511


@app .route('/done')  # line:514
def over():  # line:515
    ""  # line:520
    store_result(dict(session))  # line:522
    session .clear()  # line:524
    global valid  # line:526
    valid = False  # line:527
    return render_template('thank_you.html')  # line:529


@app .route('/admin', methods=['GET', 'POST'])  # line:535
def admin_page():  # line:536
    ""  # line:537
    if request .method == 'GET':  # line:539
        return render_template('admin_landing.html')  # line:540
    elif request .method == "POST":  # line:541
        OOOOOOOO0OO0OOOOO = request .form['pwd_box']  # line:544
        if pass_is_valid(OOOOOOOO0OO0OOOOO):  # line:545
            session['logged'] = True  # line:546
            return redirect(url_for('dashboard'))  # line:547
        else:  # line:548
            return redirect(url_for('admin_page'))  # line:549


@app .route('/dashboard')  # line:552
def dashboard():  # line:553
    ""  # line:554
    try:  # line:556
        if session['logged'] == True:  # line:557
            return render_template('dashboard.html', voting_started=voting_started, voting_ended=voting_ended, no_of_codes=no_of_codes, house_choice=house_choice, color_scheme=color_scheme, makeupper=makeupper)  # line:559
        else:  # line:560
            return redirect(url_for('admin_page'))  # line:561
    except Exception as OO0OO00OOO0O000OO:  # line:562
        print(OO0OO00OOO0O000OO)  # line:563
        return redirect(url_for('admin_page'))  # line:564


@app .route('/show_candidate', methods=['GET', 'POST'])  # line:567
def show_candidate():  # line:568
    ""  # line:569
    try:  # line:571
        if session['logged'] == True:  # line:572
            global candidates  # line:573
            if request .method == "GET":  # line:574
                O0OO0O0O00O0OO000 = [['Head Boy', 'Head Girl', 'Sports Captain', 'Cultural Captain'], ['Assistant Head Boy', 'Assistant Head Girl', 'Sports Vice Captain', 'Cultural Vice Captain'], [
                    'Kingfisher Captain', 'Flamingo Captain', 'Falcon Captain', 'Eagle Captain'], ['Kingfisher Vice Captain', 'Flamingo Vice Captain', 'Falcon Vice Captain', 'Eagle Vice Captain']]  # line:580
                OOOO0O000OO00O0OO = get_custom_post_load_list()  # line:581
                return render_template('show_candidates.html', candidates=candidates, str=str, voting_started=voting_started, voting_ended=voting_ended, getcolor=getcolor, load_list=O0OO0O0O00O0OO000, title=title, startswith=startswith, custom_posts=OOOO0O000OO00O0OO, len=len)  # line:582
            else:  # line:584
                O0OO000OO00O00O0O = request .form['candvalue']  # line:586
                O0OO000OO00O00O0O = eval(O0OO000OO00O00O0O)  # line:587
                for O0OOO0OO0000OOO0O in O0OO000OO00O00O0O:  # line:590
                    # line:591
                    OOOOO00OO0000O00O = O0OO000OO00O00O0O[O0OOO0OO0000OOO0O]
                    O00OO00O0OO0O00OO = []  # line:592
                    for OO000OOO00O0OO00O in OOOOO00OO0000O00O:  # line:593
                        OO000OOO00O0OO00O = OO000OOO00O0OO00O .strip()  # line:594
                        if OO000OOO00O0OO00O != '':  # line:595
                            O00OO00O0OO0O00OO .append(
                                OO000OOO00O0OO00O)  # line:596
                    # line:597
                    O0OO000OO00O00O0O[O0OOO0OO0000OOO0O] = O00OO00O0OO0O00OO
                candidates = O0OO000OO00O00O0O  # line:600
                if not voting_order_modified:  # line:603
                    add_to_cur_posts()  # line:604
                initializing(candidates)  # line:607
                return redirect(url_for('show_candidate'))  # line:609
        else:  # line:610
            return redirect(url_for('admin_page'))  # line:611
    except Exception as O00O00OO0OOOOO00O:  # line:612
        print(O00O00OO0OOOOO00O)  # line:613
        return redirect(url_for('admin_page'))  # line:614


@app .route('/add_custom_post', methods=['GET', 'POST'])  # line:617
def add_custom_post():  # line:618
    ""  # line:619
    try:  # line:621
        if session['logged'] == True:  # line:622
            global cur_posts, candidates, voting_order_modified  # line:623
            if request .method == 'GET':  # line:625
                OOOO00O0O0OOOOO0O = request .host  # line:626
                # line:627
                return render_template('add_custom_post.html', str=str, cur_post=cur_posts, u=underscore_remove, replace_house_name=replace_house_name, site=OOOO00O0O0OOOOO0O)
            else:  # line:629
                OOOOOO00OO0OOOOOO = request .get_json()  # line:631
                # line:632
                OOOO0O000O00OO0O0 = OOOOOO00OO0OOOOOO['post_name'].lower(
                ).strip()
                O0000OO0OOOO0000O = []  # line:635
                if OOOO0O000O00OO0O0 != '':  # line:636
                    if not OOOOOO00OO0OOOOOO['for_house']:  # line:638
                        O0000OO0OOOO0000O = [OOOO0O000O00OO0O0 .replace(
                            ' ', '_')if OO000O000OO0O0OOO == 'new_post'else OO000O000OO0O0OOO for OO000O000OO0O0OOO in OOOOOO00OO0OOOOOO['cur_posts_order']]  # line:640
                        # line:643
                        if OOOO0O000O00OO0O0 .replace(' ', '_') in cur_posts:
                            # line:644
                            return redirect(url_for('show_candidate'))
                        candidates[OOOO0O000O00OO0O0 .replace(' ', '_')] = [
                        ]  # line:646
                    else:  # line:649
                        O0000OO0OOOO0000O = [house_choice + '_'+OOOO0O000O00OO0O0 .replace(
                            ' ', '_')if O0OO00O0O0OO0000O == 'new_post'else O0OO00O0O0OO0000O for O0OO00O0O0OO0000O in OOOOOO00OO0OOOOOO['cur_posts_order']]  # line:651
                        # line:654
                        if house_choice + '_'+OOOO0O000O00OO0O0 .replace(' ', '_') in cur_posts:
                            # line:655
                            return redirect(url_for('show_candidate'))
                        # line:657
                        for OOOO0O0OO0O000O0O in ['kingfisher', 'falcon', 'flamingo', 'eagle']:
                            # line:659
                            candidates[OOOO0O0OO0O000O0O + '_' +
                                       OOOO0O000O00OO0O0 .replace(' ', '_')] = []
                        OOOO0O000O00OO0O0 = house_choice + '_' + \
                            OOOO0O000O00OO0O0 .replace(' ', '_')  # line:661
                    O0000OO0OOOO0000O = [O000OO0OO0O0OO00O .replace('house', house_choice)if O000OO0OO0O0OO00O .startswith(
                        'house')else O000OO0OO0O0OO00O for O000OO0OO0O0OO00O in O0000OO0OOOO0000O]  # line:664
                    initializing(candidates)  # line:667
                    cur_posts = O0000OO0OOOO0000O  # line:668
                    voting_order_modified = True  # line:669
                else:  # line:670
                    # line:672
                    O0000OO0OOOO0000O = OOOOOO00OO0OOOOOO['cur_posts_order']
                    O0000OO0OOOO0000O .remove('new_post')  # line:673
                    cur_posts = [(O000OO0000O00O0OO .replace('house', house_choice)if O000OO0000O00O0OO .startswith(
                        'house')else O000OO0000O00O0OO)for O000OO0000O00O0OO in O0000OO0OOOO0000O]  # line:675
                    return redirect(url_for('add_custom_post'))  # line:677
        else:  # line:678
            return redirect(url_for('admin_page'))  # line:679
    except Exception as OOOOOO00O0O000000:  # line:680
        print(OOOOOO00O0O000000)  # line:681
        return redirect(url_for('admin_page'))  # line:682


@app .route('/delete_post', methods=['GET', 'POST'])  # line:685
def delete_post():  # line:686
    ""  # line:687
    try:  # line:689
        global cur_posts, candidates  # line:690
        if session['logged'] == True:  # line:691
            if request .method == 'GET':  # line:692
                OOOOO00OO00O0OO00 = request .host  # line:693
                # line:694
                return render_template('delete_post.html', cur_post=cur_posts, u=underscore_remove, replace_house_name=replace_house_name, site=OOOOO00OO00O0OO00)
            else:  # line:696
                O000OOO00O0O000O0 = request .get_json()  # line:698
                # line:699
                O000OO00O00O00OOO = O000OOO00O0O000O0['post_to_delete'].strip()
                O000OO00O00O00OOO = O000OO00O00O00OOO .replace(
                    ' ', '_').lower()  # line:700
                if O000OO00O00O00OOO .startswith('house'):  # line:702
                    O000OO00O00O00OOO = O000OO00O00O00OOO .replace(
                        'house', house_choice)  # line:704
                try:  # line:706
                    cur_posts .remove(O000OO00O00O00OOO)  # line:707
                    for O0OOO0O000OO0OO00 in list(candidates .keys()):  # line:709
                        # line:711
                        if O000OO00O00O00OOO .startswith(house_choice):
                            # line:712
                            if O0OOO0O000OO0OO00 .endswith("".join(["_"+OOO0O00O0OO00OO0O for OOO0O00O0OO00OO0O in O000OO00O00O00OOO .split('_')[1:]])):
                                del candidates[O0OOO0O000OO0OO00]  # line:713
                        else:  # line:716
                            if O0OOO0O000OO0OO00 == O000OO00O00O00OOO:  # line:717
                                del candidates[O0OOO0O000OO0OO00]  # line:718
                    initializing(candidates)  # line:720
                except Exception as OOO00O00O000O0O0O:  # line:721
                    print(OOO00O00O000O0O0O)  # line:722
                    pass  # line:723
        else:  # line:725
            return redirect(url_for('admin_page'))  # line:726
    except:  # line:727
        return redirect(url_for('admin_page'))  # line:728


@app .route('/voting_settings')  # line:731
def voting_settings():  # line:732
    ""  # line:733
    try:  # line:735
        if session['logged'] == True:  # line:736
            OO0OO0O0OO0OOO0OO = all_photo_check(set_photos_path())  # line:737
            return render_template('voting_settings.html', d=candidates, valid=voting_started, no_of_codes=no_of_codes, not_there=OO0OO0O0OO0OOO0OO, makeupper=makeupper, len=len, underscore_remove=underscore_remove)  # line:738
        else:  # line:739
            return redirect(url_for('admin_page'))  # line:740
    except Exception as O00OOO00OOO0O00O0:  # line:741
        print(O00OOO00OOO0O00O0)  # line:742
        return redirect(url_for('admin_page'))  # line:743


@app .route('/settings', methods=['GET', 'POST'])  # line:746
def settings():  # line:747
    ""  # line:748
    try:  # line:750
        if session['logged'] == True:  # line:751
            global house_choice, no_of_codes  # line:752
            if request .method == "GET":  # line:754
                # line:755
                return render_template('settings.html', house_choice=house_choice, no_of_codes=no_of_codes)
            elif request .method == "POST":  # line:757
                global cur_posts  # line:759
                O0OOO0OO00OO0O0O0 = house_choice  # line:760
                house_choice = request .form['hc']  # line:761
                house_choice = house_choice .lower()  # line:762
                store_house_choice(house_choice)  # line:763
                update_cur_post(O0OOO0OO00OO0O0O0, house_choice)  # line:764
                O0O000O0OOOOO0OO0 = request .form['changed_pwd']  # line:767
                if not pass_is_valid(O0O000O0OOOOO0OO0) and O0O000O0OOOOO0OO0 != '':  # line:768
                    pass_set(O0O000O0OOOOO0OO0)  # line:769
                # line:772
                O0OO00000O0O0O000 = request .form['changed_no_of_codes']
                OO000O0OOO0OOOOOO = eval(
                    O0OO00000O0O0O000 .split()[0])  # line:773
                if type(OO000O0OOO0OOOOOO) is int:  # line:774
                    if OO000O0OOO0OOOOOO > 0:  # line:775
                        no_of_codes = OO000O0OOO0OOOOOO  # line:776
                return redirect(url_for('settings'))  # line:778
    except Exception as OOO00000000000O00:  # line:780
        print(OOO00000000000O00)  # line:781
        return redirect(url_for('admin_page'))  # line:782


@app .route('/logout')  # line:785
def logout():  # line:786
    ""  # line:787
    session .clear()  # line:789
    return redirect(url_for("home"))  # line:790


@app .route('/start_voting')  # line:795
def start_voting():  # line:796
    ""  # line:797
    global voting_started, voting_ended  # line:799
    voting_started = True  # line:800
    voting_ended = False  # line:801
    code_print(no_of_codes)  # line:804
    return redirect(url_for("voting_settings"))  # line:806


@app .route('/stop_voting')  # line:809
def stop_voting():  # line:810
    ""  # line:811
    global voting_started, voting_ended  # line:813
    voting_started = False  # line:814
    voting_ended = True  # line:815
    results_print()  # line:818
    return redirect(url_for('result'))  # line:820


@app .route('/results')  # line:823
def result():  # line:824
    ""  # line:825
    return render_template('results.html')  # line:827


@app .route('/download_results')  # line:830
def download_results():  # line:831
    ""  # line:832
    O000OO0O00OO0OO0O = "".join(
        [OO0OOOO00OOO00O00 + '\\'for OO0OOOO00OOO00O00 in app .config['CANDIDATE_PHOTOS'].split('\\')[:-1]])  # line:835
    try:  # line:837
        # line:838
        return send_from_directory(O000OO0O00OO0OO0O, filename='results.pdf')
    except Exception as OOOO00O0O00OO0O00:  # line:839
        print(OOOO00O0O00OO0O00)  # line:840
        return str(OOOO00O0O00OO0O00)  # line:841


@app .route('/uploads/<path:filename>')  # line:844
def download_file(OO0OO000000OO0OOO):  # line:845
    ""  # line:846
    try:  # line:848
        O000O00O0OOOOOOOO = get_image_folder_path(
            app .config['CANDIDATE_PHOTOS'], OO0OO000000OO0OOO)  # line:849
        OOOO0OOOO0O0OO000 = "".join(
            [OOOO00O00O0000OOO + '/'for OOOO00O00O0000OOO in O000O00O0OOOOOOOO .split('/')[:-1]])  # line:850
        OO0OO000000OO0OOO = O000O00O0OOOOOOOO .split('/')[-1]  # line:851
        # line:852
        return send_from_directory(OOOO0OOOO0O0OO000, OO0OO000000OO0OOO, as_attachment=True)
    except:  # line:853
        pass  # line:854


def get_image_folder_path(O0O0000O0OOOO0O00, OOOOOO0O0OO00O000):  # line:857
    ""  # line:858
    for OO000O0OO0OOOO000 in os .walk(O0O0000O0OOOO0O00):  # line:860
        for OOOO00O0OOOOOO000 in OO000O0OO0OOOO000[2]:  # line:861
            # line:862
            if OOOO00O0OOOOOO000 .lower()[:len(OOOO00O0OOOOOO000)-OOOO00O0OOOOOO000[::-1].index('.')-1] == OOOOOO0O0OO00O000 .lower():
                if not OOOO00O0OOOOOO000 .lower().startswith('default'):  # line:863
                    # line:864
                    return OO000O0OO0OOOO000[0].replace('\\', '/')+'/'+OOOO00O0OOOOOO000


def all_photo_check(O000OO0OOOO00OO0O):  # line:867
    ""  # line:868
    OOO0O0000O0OOOO0O = {}  # line:871
    for OOOOO0O00000O0O0O, OOO00O0OO0O0000O0 in get_cands_from_db().items():  # line:873
        for O000000O0OO0OOO0O in OOO00O0OO0O0000O0:  # line:874
            for OO00O00OO000OO0OO in os .walk(O000OO0OOOO00OO0O):  # line:875
                OO0O0OOO0OO0O0000 = False  # line:876
                for OOO0O000O00OO0000 in OO00O00OO000OO0OO[2]:  # line:877
                    # line:878
                    if OOO0O000O00OO0000 .lower()[:len(OOO0O000O00OO0000)-OOO0O000O00OO0000[::-1].index('.')-1] == O000000O0OO0OOO0O .lower():
                        OO0O0OOO0OO0O0000 = True  # line:879
                else:  # line:880
                    if not OO0O0OOO0OO0O0000:  # line:881
                        try:  # line:882
                            OOO0O0000O0OOOO0O[OOOOO0O00000O0O0O] = OOO0O0000O0OOOO0O[OOOOO0O00000O0O0O]+[
                                O000000O0OO0OOO0O]  # line:883
                        except KeyError:  # line:884
                            OOO0O0000O0OOOO0O[OOOOO0O00000O0O0O] = [
                                O000000O0OO0OOO0O]  # line:885
    for OOOOO0O00000O0O0O in OOO0O0000O0OOOO0O:  # line:888
        O0OOO0000O0O000O0 = ",".join(
            OOO0O0000O0OOOO0O[OOOOO0O00000O0O0O])  # line:889
        OOO0O0000O0OOOO0O[OOOOO0O00000O0O0O] = O0OOO0000O0O000O0  # line:890
    return OOO0O0000O0OOOO0O  # line:892


def add_to_cur_posts():  # line:899
    ""  # line:900
    global cur_posts, candidates  # line:902
    cur_posts = []  # line:904
    OOO0O00000O00O00O = ['kingfisher',
                         'flamingo', 'falcon', 'eagle']  # line:905
    O0O0OO00000OO0000 = []  # line:906
    OO000O0OO00O0O0OO = []  # line:907
    OOOO00000O0OOO0O0 = ['head_boy', 'head_girl', 'assistant_head_boy', 'assistant_head_girl',
                         'cultural_captain', 'cultural_vice_captain', 'sports_captain', 'sports_vice_captain']  # line:909
    OOO0OO00O0O000000 = [house_choice + '_captain',
                         house_choice + '_vice_captain']  # line:911
    for OOOOOO0O0O00O000O in candidates:  # line:914
        O000O00OOO00000OO = False  # line:915
        for OOOO00OOOOOOO0OO0 in OOO0O00000O00O00O:  # line:916
            if OOOOOO0O0O00O000O .startswith(OOOO00OOOOOOO0OO0):  # line:917
                O000O00OOO00000OO = True  # line:918
        if O000O00OOO00000OO:  # line:920
            if OOOOOO0O0O00O000O .startswith(house_choice):  # line:921
                OO000O0OO00O0O0OO .append(OOOOOO0O0O00O000O)  # line:922
        else:  # line:923
            if len(candidates[OOOOOO0O0O00O000O]) > 1 or OOOOOO0O0O00O000O not in OOOO00000O0OOO0O0:  # line:924
                O0O0OO00000OO0000 .append(OOOOOO0O0O00O000O)  # line:925
    for OOOOOO0O0O00O000O in OOOO00000O0OOO0O0:  # line:928
        if OOOOOO0O0O00O000O in O0O0OO00000OO0000:  # line:930
            cur_posts .append(OOOOOO0O0O00O000O)  # line:931
            O0O0OO00000OO0000 .remove(OOOOOO0O0O00O000O)  # line:932
    for OOOOOO0O0O00O000O in O0O0OO00000OO0000:  # line:933
        cur_posts .append(OOOOOO0O0O00O000O)  # line:935
    for OOOOOO0O0O00O000O in OOO0OO00O0O000000:  # line:938
        if OOOOOO0O0O00O000O in OO000O0OO00O0O0OO:  # line:940
            cur_posts .append(OOOOOO0O0O00O000O)  # line:941
            OO000O0OO00O0O0OO .remove(OOOOOO0O0O00O000O)  # line:942
    for OOOOOO0O0O00O000O in OO000O0OO00O0O0OO:  # line:943
        cur_posts .append(OOOOOO0O0O00O000O)  # line:945


def set_photos_path():  # line:948
    ""  # line:949
    try:  # line:951
        if getattr(sys, 'frozen', False):  # line:952
            OOOOOOOO0OOO00OO0 = os .path .dirname(sys .executable)  # line:953
        else:  # line:954
            OOOOOOOO0OOO00OO0 = os .path .dirname(__file__)  # line:955
        O00O00OO00O00OO00 = 'candidate_photos'  # line:956
        OO0OOO00000O0O00O = OOOOOOOO0OOO00OO0 + '\\'+O00O00OO00O00OO00  # line:957
        app .config['CANDIDATE_PHOTOS'] = OO0OOO00000O0O00O  # line:958
    except FileNotFoundError:  # line:959
        # line:961
        OOO00OOOOOO000000 = "/".join(os .path .dirname(__file__).split('/'))
        os .mkdir(OOO00OOOOOO000000 + '/candidate_photos')  # line:962
        set_photos_path()  # line:963
    return OO0OOO00000O0O00O  # line:965


def colors_set():  # line:968
    ""  # line:969
    global color_scheme  # line:971
    color_scheme['kingfisher'] = ('#30a4e2', '#036f96', '#ffffff')  # line:973
    color_scheme['flamingo'] = ('#E05707', '#A63A0F', '#ffffff')  # line:974
    color_scheme['falcon'] = ('#7E58BF', '#432A73', '#ffffff')  # line:975
    color_scheme['eagle'] = ('#B81A1C', '#750407', '#ffffff')  # line:976
    color_scheme['major'] = ('#161616', '#212121', '#FCED47')  # line:977


def store_result(OOOOO00OO0OO00000):  # line:982
    ""  # line:983
    if 'logged' in OOOOO00OO0OO00000:  # line:986
        del OOOOO00OO0OO00000['logged']  # line:987
    if 'home_choice' in OOOOO00OO0OO00000:  # line:988
        del OOOOO00OO0OO00000['home_choice']  # line:989
    OOOOO00O0O00OOO00 = {}  # line:992
    for OO0000O0O0OO0OOO0 in OOOOO00OO0OO00000:  # line:993
        if OOOOO00OO0OO00000[OO0000O0O0OO0OOO0] != 'DNE':  # line:994
            # line:995
            OOOOO00O0O00OOO00[OO0000O0O0OO0OOO0] = OOOOO00OO0OO00000[OO0000O0O0OO0OOO0]
    add_votes_to_db(dict(OOOOO00O0O00OOO00))  # line:997


def get_custom_post_load_list():  # line:1000
    ""  # line:1001
    OOOOO000OO00O0OO0 = ['Head Boy', 'Head Girl', 'Sports Captain', 'Cultural Captain', 'Kingfisher Captain', 'Flamingo Captain', 'Falcon Captain', 'Eagle Captain', 'Assistant Head Boy',
                         'Assistant Head Girl', 'Sports Vice Captain', 'Cultural Vice Captain', 'Kingfisher Vice Captain', 'Flamingo Vice Captain', 'Falcon Vice Captain', 'Eagle Vice Captain']  # line:1005
    OOOOO000OO00O0OO0 = [O0OO000OOOO0OOOO0 .lower().replace(
        ' ', "_")for O0OO000OOOO0OOOO0 in OOOOO000OO00O0OO0]  # line:1006
    O0OOO000OOO0OOOOO = candidates .keys()  # line:1009
    OO0O00O0O0O0OOOOO = list(set(OOOOO000OO00O0OO0) ^
                             set(O0OOO000OOO0OOOOO))  # line:1012
    OOO00OOOO00OO0OOO = []  # line:1013
    for OO0OOO00OO0OOOOOO in OO0O00O0O0O0OOOOO:  # line:1016
        if OO0OOO00OO0OOOOOO not in OOOOO000OO00O0OO0:  # line:1017
            OOO00OOOO00OO0OOO .append(OO0OOO00OO0OOOOOO)  # line:1018
    OO0O00O0O0O0OOOOO = OOO00OOOO00OO0OOO  # line:1019
    OO0O0000O0OOOO00O = []  # line:1021
    OOO000OO0O000O0OO = []  # line:1022
    OOOO00OOOOO00O00O = []  # line:1023
    for OO0OOO00OO0OOOOOO in OO0O00O0O0O0OOOOO:  # line:1026
        if is_house_post(OO0OOO00OO0OOOOOO):  # line:1027
            if OO0OOO00OO0OOOOOO .startswith('kingfisher'):  # line:1028
                OOOO00OOOOO00O00O .append(OO0OOO00OO0OOOOOO)  # line:1029
        else:  # line:1030
            OOO000OO0O000O0OO .append(OO0OOO00OO0OOOOOO)  # line:1031
    for OO0OOO00OO0OOOOOO in OOOO00OOOOO00O00O:  # line:1034
        OO0OOO00OO0OOOOOO = OO0OOO00OO0OOOOOO .split('_')[1:]  # line:1035
        for OO0000O00O000OO0O in ["kingfisher", 'flamingo', 'falcon', 'eagle']:  # line:1036
            OO0O0000O0OOOO00O .append(OO0000O00O000OO0O + "".join(
                ['_'+OO0O000O000O0OOO0 for OO0O000O000O0OOO0 in OO0OOO00OO0OOOOOO]))  # line:1037
    OO0O0000O0OOOO00O .extend(OOO000OO0O000O0OO)  # line:1039
    return OO0O0000O0OOOO00O  # line:1041


def update_cur_post(O0O000000O0O00000, O00OOO00OOO00OO00):  # line:1044
    ""  # line:1045
    global cur_posts  # line:1047
    O00O00OO000O0OOO0 = []  # line:1048
    for O0OO00O00O0O0O00O in cur_posts:  # line:1049
        O0000O00000O00000 = O0OO00O00O0O0O00O .split('_')  # line:1050
        if O0000O00000O00000[0] == O0O000000O0O00000:  # line:1051
            O00O00OO000O0OOO0 .append(O00OOO00OOO00OO00 + ''.join(
                ['_'+OOOOO0O0O0O00OO00 for OOOOO0O0O0O00OO00 in O0000O00000O00000[1:]]))  # line:1052
        else:  # line:1053
            O00O00OO000O0OOO0 .append(O0OO00O00O0O0O00O)  # line:1054
    cur_posts = O00O00OO000O0OOO0  # line:1056


def underscore_remove(O00O00OOOO00OO000):  # line:1061
    return O00O00OOOO00OO000 .replace('_', ' ').upper()  # line:1062


def makeupper(OO00000O000O0OOOO):  # line:1065
    return OO00000O000O0OOOO .upper()  # line:1066


def title(OO0O0O0000O00O0O0):  # line:1069
    return OO0O0O0000O00O0O0 .title().replace('_', ' ')  # line:1070


def startswith(O00OOO00O0OOOO00O, O0OO0O00O0OO0O00O):  # line:1073
    return O00OOO00O0OOOO00O .startswith(O0OO0O00O0OO0O00O)  # line:1074


def getcolor(O00O00O00OO000OOO):  # line:1077
    O00O00O00OO000OOO = O00O00O00OO000OOO .split()[0].lower()  # line:1078
    OO0OOO0O00OOO0O00 = {'kingfisher': 'kf', 'flamingo': 'fl',
                         'falcon': 'fa', 'eagle': 'ea', 'major': 'ma'}  # line:1080
    for OO0000OO0OO000000 in OO0OOO0O00OOO0O00:  # line:1081
        if OO0000OO0OO000000 == O00O00O00OO000OOO:  # line:1082
            return OO0OOO0O00OOO0O00[O00O00O00OO000OOO]  # line:1083
    return OO0OOO0O00OOO0O00['major']  # line:1084


def is_house_post(O0OO0OOOO0OOO00O0):  # line:1087
    for O0000000000OOO0O0 in ["kingfisher", 'falcon', 'flamingo', 'eagle']:  # line:1088
        if O0OO0OOOO0OOO00O0 .lower().startswith(O0000000000OOO0O0):  # line:1089
            return True  # line:1090
    return False  # line:1091


def replace_house_name(O0O0OOO0O000000OO):  # line:1094
    # line:1095
    return [O0O0O0O0OOO0OOOO0 .replace(house_choice, 'house')if O0O0O0O0OOO0OOOO0 .startswith(house_choice)else O0O0O0O0OOO0OOOO0 for O0O0O0O0OOO0OOOO0 in O0O0OOO0O000000OO]


def start():  # line:1098
    ""  # line:1099
    global candidates  # line:1101
    candidates = get_cands_from_db()  # line:1102
    add_to_cur_posts()  # line:1104
    resize_images_in_folder(set_photos_path())  # line:1105
    colors_set()  # line:1106
    app .run(debug=False)  # line:1108


start()  # line:1111
