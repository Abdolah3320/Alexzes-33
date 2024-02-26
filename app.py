from flask import *
import os
import shutil
from ast import literal_eval
from random import choice
import apsw as sql
import smtplib as sm
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64


def create_icon(filename):
    extension = filename.rsplit('.', 1)[-1].lower()
    icon_class = "fa-file"

    extension_icon_mapping = {
        "txt": "fa-file-alt",
        "jpg": "fa-file-image",
        "jpeg": "fa-file-image",
        "png": "fa-file-image",
        "gif": "fa-file-image",
        "doc": "fa-file-word",
        "docx": "fa-file-word",
        "ppt": "fa-file-powerpoint",
        "pptx": "fa-file-powerpoint",
    }

    if extension in extension_icon_mapping:
        icon_class = extension_icon_mapping[extension]
    else:
        icon_class = "fa-file"

    return icon_class


def mk_num():
    lst = [str(i) for i in range(10)]
    x = ""
    last = ""
    for i in range(8):
        d = choice(lst)
        while d == last:
            d = choice(lst)
        x += d
        last = d

    return int(x)


def mk_code():
    mydb.execute("SELECT id FROM users")
    try:
        lst2 = mydb.fetchall()
        lst = []
        for i in lst2:
            lst.append(i[0])
    except:
        lst = []

    print(lst)
    letters1 = tuple([chr(i) for i in range(ord("a"), ord("z") + 1)])
    letters2 = tuple([chr(i) for i in range(ord("A"), ord("Z") + 1)])
    nums = tuple([str(i) for i in range(10)])
    ALL = (letters1, letters2, nums)
    x = ""
    last = ""
    used = []
    for i in range(30):
        tpl = choice(ALL)
        y = choice(tpl)
        while last == tpl or y in used:
            tpl = choice(ALL)
            y = choice(tpl)
        x += y
        last = tpl
        used.append(y)
    if x in lst:
        print(True)
        mk_code()
    else:
        return x


def encode(file_path: str):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
        base64_data = base64.b64encode(binary_data).decode('utf-8')
    return base64_data


def decode(code, file_path: str):
    with open(file_path, 'wb') as file:
        file.write(base64.b64decode(code))


def mk_code2():
    cmds = ["SELECT code FROM classes",
            "SELECT code FROM grades",
            "SELECT code FROM subjects",
            "SELECT code FROM posts",
            "SELECT code FROM files"]

    ids = []
    for i in cmds:
        try:
            temp = []
            mydb.execute(i)
            temp2 = mydb.fetchall()
            for i in temp2:
                temp.append(i[0])
        except Exception as x:
            print(x, i)
            temp = []
        ids.extend(temp)

    lst = [str(i) for i in range(10)]
    lst2 = [chr(i) for i in range(ord("a"), ord("z") + 1)]
    lst3 = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
    x = ""
    last = lst
    for i in range(10):
        tpl = choice([lst, lst2, lst3])
        while tpl == last:
            tpl = choice([lst, lst2, lst3])
        d = choice(tpl)
        x += d
        last = tpl
    if x in ids:
        mk_code2()
    else:
        return x


def send(email, name, num):
    em = MIMEMultipart()

    body = f"""
{name},

Thank you for choosing our study platform. As part of our security measures, we have generated a verification number for you.

Verification Number: {num}

Please use this number to complete the verification process and ensure the security of your account.

Best Regards,
Alexzes Team
    """
    em.attach(MIMEText(body, "plain"))
    em["From"] = "alexzesteam@gmail.com"
    em["To"] = email
    em["Subject"] = "Account Verification - School in your pocket"

    smtp = sm.SMTP_SSL("smtp.gmail.com", 465)
    smtp.login("alexzesteam@gmail.com", "wxbpywtxhiwqgdwc")
    smtp.sendmail("alexzesteam@gmail.com", email, em.as_string())
    smtp.quit()


def send2(email, name, num):
    em = MIMEMultipart()

    body = f"""
Dear {name},

We received a request to verify your account on our study platform.

Verification Code: {num}

Please use this code to complete the verification process and ensure the security of your account.


Best Regards,
Alexzes Team
    """
    em.attach(MIMEText(body, "plain"))
    em["From"] = "alexzesteam@gmail.com"
    em["To"] = email
    em["Subject"] = "Account Verification - School in your pocket"

    smtp = sm.SMTP("smtp.gmail.com", 587)
    smtp.starttls()
    smtp.login("alexzesteam@gmail.com", "wxbpywtxhiwqgdwc")
    smtp.sendmail("alexzesteam@gmail.com", email, em.as_string())
    smtp.quit()


def save_sc(id, address, email, password, name):
    mydb.execute("INSERT INTO users VALUES(?, ?, ?, ?)",
                 (id, email, password, "sc"))
    mydb.execute(
        "INSERT INTO schools VALUES(?, ?, ?, ?, ?)",
        (id, name, address, mk_code2(), "[]"),
    )


def save_st(id, c_code, email, password, name):
    mydb.execute("INSERT INTO users VALUES(?, ?, ?, ?)",
                 (id, email, password, "st"))
    mydb.execute("INSERT INTO students VALUES(?, ?, ?)", (id, name, c_code))


def save_t(id, email, password, name):
    mydb.execute("INSERT INTO users VALUES(?, ?, ?, ?)",
                 (id, email, password, "t"))
    mydb.execute("INSERT INTO teachers VALUES(?, ?, ?)",
                 (id, name, "[]"))


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")
temp_dir = os.path.join(BASE_DIR, "templates")
cont_dir = os.path.join(static_dir, "container")
db_dir = os.path.join(static_dir, "db")
imgs_dir = os.path.join(static_dir, "imgs")
subs_dir = os.path.join(static_dir, "subjects")
posts_dir = os.path.join(static_dir, "posts")
DIRS = (cont_dir, db_dir, imgs_dir, subs_dir, posts_dir)
for dir in DIRS:
    if not os.path.exists(dir):
        os.mkdir(dir)
db = sql.Connection(os.path.join(db_dir, "Data.db"))
mydb = db.cursor()
app = Flask(__name__, static_folder=static_dir, template_folder=temp_dir)
app.secret_key = 'SecKeyForWeb0000'

mydb.execute(
    "CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY_KEY, email TEXT, password TEXT, type TEXT)"
)
mydb.execute(
    "CREATE TABLE IF NOT EXISTS tosignup(id TEXT PRIMARY_KEY, ver_num TEXT, data TEXT)"
)
mydb.execute(
    "CREATE TABLE IF NOT EXISTS schools(id TEXT PRIMARY_KEY, name TEXT, address TEXT, code TEXT, grades TEXT)"
)
mydb.execute(
    "CREATE TABLE IF NOT EXISTS teachers(id TEXT PRIMARY_KEY, name TEXT, classes TEXT)"
)
mydb.execute(
    "CREATE TABLE IF NOT EXISTS students(id TEXT PRIMARY_KEY, name TEXT, class_code TEXT)"
)
mydb.execute(
    "CREATE TABLE IF NOT EXISTS grades(code TEXT, name TEXT, school_code TEXT, classes TEXT, subjects TEXT)"
)
mydb.execute(
    "CREATE TABLE IF NOT EXISTS classes(code TEXT, name TEXT, school_code TEXT, grade TEXT, students TEXT, teachers TEXT, posts TEXT)"
)
mydb.execute(
    "CREATE TABLE IF NOT EXISTS subjects(code TEXT, name TEXT, school_code TEXT, grade TEXT, files TEXT, folder TEXT)"
)
mydb.execute(
    "CREATE TABLE IF NOT EXISTS posts(code TEXT, class TEXT, content TEXT, files TEXT, folder TEXT, comments TEXT, owner TEXT)"
)
mydb.execute(
    "CREATE TABLE IF NOT EXISTS files(code TEXT, name TEXT, folder TEXT, backup_code TEXT)"
)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')

@app.route("/")
@app.route("/home")
@app.route("/welcome")
def home():
    id = session.get('schoolInPockID')
    if id:
        mydb.execute("SELECT * FROM users WHERE id = ?", (id,))
        try:
            data = mydb.fetchall()[0]
            tp = data[-1]
            id = data[0]
            if tp == "sc":
                return redirect(url_for("school"))
            elif tp == "st":
                return redirect(url_for("student"))
            elif tp == "t":
                return redirect(url_for("teacher"))
        except:
            session.clear()
            pass
    return render_template("welcome.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route("/get-vercode", methods=["POST", "GET"])
def getVerCode():
    num = request.form.get("v-num")
    id = request.form.get("v-error")
    print(num, id)
    mydb.execute("SELECT * FROM tosignup WHERE id = ?", (id,))
    result = mydb.fetchall()
    exist = 0
    print(result)
    for i in result:
        print(i)
        if num == i[1]:
            exist = 1
            data = dict(literal_eval(i[-1]))

    if exist:
        tp = data["t"]
        if tp == "sc":
            save_sc(id, data["a"], data["e"], data["p"], data["n"])
        elif tp == "st":
            save_st(id, data["c_c"], data["e"], data["p"], data["n"])
        elif tp == "t":
            save_t(id, data["e"], data["p"], data["n"])

    data = {"exist": exist}
    return jsonify(data)


@app.route("/sc/collectdata/signup", methods=["POST", "GET"])
def sc_signup():
    name = request.form.get("sc-name")
    address = request.form.get("sc-address")
    email = request.form.get("sc-email")
    password = request.form.get("sc-pass")
    mydb.execute("SELECT * FROM users WHERE email = ?", (email,))
    result = mydb.fetchall()
    if len(result) == 0:
        num = mk_num()
        per_data = {"n": name, "p": password,
                    "t": "sc", "e": email, "a": address}
        newId = mk_code()
        mydb.execute(
            "INSERT INTO tosignup(id, ver_num, data) VALUES(?, ?, ?)",
            (newId, num, str(per_data)),
        )
        data = {"exist": "0", "error": newId}
        send(email, name, num)
    else:
        data = {"exist": "1", "error": "Invalid E-mail"}
    return jsonify(data)


@app.route("/t/collectdata/signup", methods=["POST", "GET"])
def t_signup():
    name = request.form.get("t-name")
    email = request.form.get("t-email")
    password = request.form.get("t-pass")
    mydb.execute("SELECT * FROM users WHERE email = ?", (email,))
    result = mydb.fetchall()
    if len(result) == 0:
        num = mk_num()
        per_data = {"n": name, "p": password,
                    "t": "t", "e": email}
        newId = mk_code()
        mydb.execute(
            "INSERT INTO tosignup(id, ver_num, data) VALUES(?, ?, ?)",
            (newId, num, str(per_data)),
        )
        data = {"exist": "0", "error": newId}
        send(email, name, num)
    else:
        data = {"exist": "1", "error": "Invalid E-mail"}
    return jsonify(data)


@app.route("/st/collectdata/signup", methods=["POST", "GET"])
def st_signup():
    name = request.form.get("st-name")
    code = request.form.get("st-cls-code")
    email = request.form.get("st-email")
    password = request.form.get("st-pass")
    mydb.execute("SELECT * FROM users WHERE email = ?", (email,))
    result = mydb.fetchall()
    if len(result) == 0:
        mydb.execute("SELECT * FROM classes WHERE code = ?", (code,))
        result = mydb.fetchall()
        if len(result) == 0:
            num = mk_num()
            per_data = {"n": name, "p": password,
                        "t": "st", "e": email, "c_c": code}
            newId = mk_code()
            mydb.execute(
                "INSERT INTO tosignup(id, ver_num, data) VALUES(?, ?, ?)",
                (newId, num, str(per_data)),
            )
            data = {"exist": "0", "error": newId}
            send(email, name, num)
        else:
            data = {"exist": "1", "error": "Invalid Class code"}
    else:
        data = {"exist": "1", "error": "Invalid E-mail"}
    return jsonify(data)


@app.route("/collectdata/login", methods=["POST", "GET"])
def login():
    email = request.form.get("l-email")
    password = request.form.get("l-pass")
    mydb.execute("SELECT * FROM users WHERE email = ?", (email,))
    id = 0
    result = mydb.fetchall()
    for i in result:
        if password == i[2]:
            id = str(i[0])
            session['schoolInPockID'] = id
            id = 1
    data = {"id": id}
    return jsonify(data)


@app.route("/sc")
def school():
    id = session.get('schoolInPockID')
    if not id:
        return redirect(url_for('home'))
    mydb.execute("SELECT * FROM schools WHERE id = ?", (id,))
    try:
        data = mydb.fetchall()[0]
        print(data)
        grades = literal_eval(data[4])
        name = data[1]
        name = name.capitalize()
        spName = name.split()
        if not "School" in spName:
            name += " School"
        code = data[3]
        g_data = []
        total_classes = 0
        total_students = 0
        if len(grades) > 0:
            for i in grades:
                mydb.execute("SELECT * FROM grades WHERE code = ?", (i,))
                res = list(mydb.fetchall()[0])
                classes = literal_eval(res[3])
                c_count = len(classes)
                total_classes += c_count
                students = 0
                if c_count > 0:
                    for j in classes:
                        mydb.execute(
                            "SELECT id FROM students WHERE class_code = ?", (
                                j,)
                        )
                        res2 = mydb.fetchall()
                        print(res2)
                        st_count = len(res2)
                        students += st_count
                        total_students += st_count
                url = f"/sc/grade/{ i }/classes"
                res.append(c_count)
                res.append(students)
                res.append(url)
                g_data.append(res)
        print(g_data)
        lst = [
            ("Grades :", len(grades)),
            ("Classes :", total_classes),
            ("Students :", total_students),
            ("Code :", code),
            ("st", "Setting", f"/sc/settings"),
        ]

        return render_template(
            "sc_t_st.html",
            sc=True,
            name=name,
            cards=g_data,
            lst=lst,
            frm="Grade",
            url_new_g=f"/newGrade",
            frm_id="form",
        )

    except IndexError:
        return redirect(url_for('home'))


# @app.route("/sc/settings")
# def school_set():
#     id = session.get('schoolInPockID')
#     if not id:
#         return redirect(url_for('home'))
#     mydb.execute("SELECT * FROM schools WHERE id = ?", (id,))
#     try:
#         data = mydb.fetchall()[0]
#         print(data)
#         grades = literal_eval(data[4])
#         name = data[1]
#         name = name.capitalize()
#         spName = name.split()
#         if not "School" in spName:
#             name += " School"
#         address = data[2]
#         code = data[3]
#         g_data = []
#         total_classes = 0
#         total_students = 0
#         if len(grades) > 0:
#             for i in grades:
#                 mydb.execute("SELECT * FROM grades WHERE code = ?", (i,))
#                 res = list(mydb.fetchall()[0])
#                 classes = literal_eval(res[3])
#                 c_count = len(classes)
#                 total_classes += c_count
#                 students = 0
#                 if c_count > 0:
#                     for j in classes:
#                         mydb.execute(
#                             "SELECT id FROM students WHERE class_code = ?", (
#                                 j,)
#                         )
#                         res2 = mydb.fetchall()
#                         print(res2)
#                         st_count = len(res2)
#                         students += st_count
#                         total_students += st_count
#                 url = f"/sc/grade/{ i }/classes"
#                 res.append(c_count)
#                 res.append(students)
#                 res.append(url)
#                 g_data.append(res)
#         print(g_data)
#         path = [
#             (name, f"/sc"),
#             (">"),
#             ("Settings", f"/sc/settings"),
#         ]

#         return render_template(
#             "settings.html",
#             name=name,
#             address=address,
#             cards=g_data,
#             path=path,
#         )

#     except IndexError:
#         return redirect(url_for('home'))


@app.route("/newClass/grade/<gradeid>", methods=["POST"])
def newClass(gradeid):
    id = session.get('schoolInPockID')
    name = request.form.get("g_name")
    try:
        mydb.execute("SELECT * FROM schools WHERE id = ?", (id,))
        school = mydb.fetchall()[0]
        sc_code = school[3]
        sc_grades = literal_eval(school[4])
        if not gradeid in sc_grades:
            data = {"exist": "1", "error": "Not Found"}
            print(data)
            return jsonify(data)
        mydb.execute("SELECT * FROM grades WHERE code = ?", (gradeid,))
        grade = mydb.fetchall()[0]
        classes = list(literal_eval(grade[-2]))
        new = mk_code2()
        classes.append(str(new))
        mydb.execute(
            "UPDATE grades SET classes = ? WHERE code = ?", (str(
                classes), gradeid)
        )
        mydb.execute(
            "INSERT INTO classes VALUES(?, ?, ?, ?, ?, ?, ?)",
            (new, name, sc_code, gradeid, "[]", "[]", '[]'),
        )
        data = {"exist": "0"}
    except:
        data = {"exist": "1", "error": "Internal Server Error"}
    return jsonify(data)


@app.route("/newGrade", methods=["POST"])
def newGrade():
    name = request.form.get("g_name")
    id = session.get('schoolInPockID')
    mydb.execute("SELECT * FROM schools WHERE id = ?", (id,))
    try:
        sc = mydb.fetchall()[0]
        sc_code = sc[3]
        grades = list(literal_eval(sc[-1]))
        new = mk_code2()
        grades.append(str(new))
        mydb.execute(
            "UPDATE schools SET grades = ? WHERE code = ?", (str(
                grades), sc_code)
        )
        mydb.execute(
            "INSERT INTO grades VALUES(?, ?, ?, ?, ?)",
            (new, name, sc_code, "[]", "[]"),
        )
        data = {"exist": "0"}
    except:
        data = {"exist": "1", "error": "Internal Server Error"}
    return jsonify(data)


def get_data(id, gradeid, classid=False):
    try:
        mydb.execute("SELECT * FROM schools WHERE id = ?", (id,))
        s_data = mydb.fetchall()[0]
        mydb.execute("SELECT * FROM grades WHERE code = ?", (gradeid,))
        g_data = mydb.fetchall()[0]
        sc_grades = literal_eval(s_data[4])
        if gradeid not in sc_grades:
            return None, None
        students_data = []
        teachers_data = []
        classes = list(literal_eval(g_data[3]))
        total_s = 0
        c_data = []
        if len(classes) > 0:
            for i in classes:
                mydb.execute("SELECT * FROM classes WHERE code = ?", (i,))
                res = list(mydb.fetchall()[0])
                url = f"/sc/grade/{ gradeid }/class/{ i }"
                x = list(literal_eval(res[4]))
                students = len(x)
                total_s += students
                res.append(students)
                res.append(url)
                c_data.append(res)
                mydb.execute(
                    "SELECT * FROM students WHERE class_code = ?", (i,))
                st_data = mydb.fetchall()
                for i in st_data:
                    i_lst = list(i)
                    i_lst.append(res[1])
                    students_data.append(i_lst)
                x = list(literal_eval(res[4]))
                students = len(x)
                total_s += students
                teachers = list(literal_eval(res[5]))
                for i in teachers:
                    mydb.execute("SELECT * FROM teachers WHERE id = ?", (i,))
                    try:
                        y = mydb.fetchall()[0]
                        teachers_data.append(y)
                    except IndexError:
                        continue
        for i in teachers_data:
            if teachers_data.count(i) > 1:
                teachers_data.remove(i)
        subjects = list(literal_eval(g_data[-1]))
        subdata = []
        for i in subjects:
            mydb.execute('SELECT * FROM subjects WHERE code = ?', (i,))
            try:
                subdata.append(mydb.fetchall()[0])
            except Exception as x:
                print(x)
                pass
        sub = len(subjects)
        commom_url = f"/sc/grade/{ gradeid }/"
        lst = [
            ("Classes :", len(classes), commom_url + "classes"),
            ("Students :", total_s, commom_url + 'people'),
            ("Subjects :", sub, commom_url + "subjects"),
            ("Settings", "", commom_url + "settings"),
        ]
        sc_name = str(s_data[1])
        sc_name = sc_name.capitalize()
        spsc_name = sc_name.split()
        if not "School" in spsc_name:
            sc_name += " School"
        path = [
            (sc_name, f"/sc"),
            (">"),
            (g_data[1], f"/sc/grade/{ gradeid }"),
        ]
        return s_data, g_data, teachers_data, students_data, total_s, c_data, lst, path, subdata
    except:
        return None, None, None, None, None, None, None, None, None


@app.route("/sc/grade/<gradeid>")
@app.route("/sc/grade/<gradeid>/classes")
@app.route("/sc/grade/<gradeid>/settings")
def sc_grade_cls(gradeid):
    id = session.get('schoolInPockID')
    if not id:
        return redirect(url_for('home'))
    try:
        mydb.execute('select * from schools where id = ?', (id,))
        school_data = mydb.fetchall()[0]
        if not gradeid in list(literal_eval(school_data[4])):
            return redirect(url_for('home'))
    except Exception as x:
        print(x)
        return redirect(url_for('home'))
    s_data, g_data, teachers_data, students_data, total_s, c_data, lst, path, subdata = get_data(
        id, gradeid)
    if s_data is None or g_data is None:
        return redirect(url_for('home'))
    return render_template(
        "sc_t_st.html",
        frm="Class",
        path=path,
        name=g_data[1],
        lst=lst,
        cards=c_data,
        c=True,
        frm_id="form_class",
        url_new_g=f"/newClass/grade/{ gradeid }",
    )


@app.route("/sc/grade/<gradeid>/students")
@app.route("/sc/grade/<gradeid>/teachers")
@app.route("/sc/grade/<gradeid>/people")
def sc_grade_st(gradeid):
    id = session.get('schoolInPockID')
    if not id:
        return redirect(url_for('home'))
    try:
        mydb.execute('select * from schools where id = ?', (id,))
        school_data = mydb.fetchall()[0]
        if not gradeid in list(literal_eval(school_data[4])):
            return redirect(url_for('home'))
    except:
        return redirect(url_for('home'))
    s_data, g_data, teachers_data, students_data, total_s, c_data, lst, path, subdata = get_data(
        id, gradeid)
    if s_data is None or g_data is None:
        return redirect(url_for('home'))
    path.append(('>'))
    path.append(('People', f"/sc/grade/{ gradeid }/people"))
    return render_template(
        "students.html",
        path=path,
        lst=lst,
        c=True,
        data=students_data,
        tdata=teachers_data,
        gd=True,
        sc=True,
    )


@app.route("/addFile/<gradeid>/<subjectCode>", methods=["POST"])
def addFile(gradeid, subjectCode):
    id = session.get('schoolInPockID')
    if not id:
        return redirect(url_for('home'))
    try:
        mydb.execute('select * from schools where id = ?', (id,))
        school_data = mydb.fetchall()[0]
        if not gradeid in list(literal_eval(school_data[4])):
            return jsonify({'error': True})
        mydb.execute('select * from grades where code = ?', (gradeid,))
        grade_data = mydb.fetchall()[0]
        mydb.execute('select * from subjects where code = ?', (subjectCode,))
        sub_data = mydb.fetchall()[0]
        file = request.files.get('file')
        if not file:
            return jsonify({'error': True})
        folderName = sub_data[0]
        fileName = file.filename
        ex = fileName.rsplit('.', 1)[1]
        fileName = fileName.rsplit('.', 1)[0]
        path = os.path.join(subs_dir, folderName)
        if not os.path.exists(path):
            os.mkdir(path)
        name = fileName + '.' + ex
        file_path = os.path.join(path, name)
        i = 1
        while os.path.exists(file_path):
            i += 1
            name = fileName + str(i) + '.' + ex
            file_path = os.path.join(path, name)
        file.save(file_path)
        newId = mk_code2()
        mydb.execute('INSERT INTO files VALUES(?, ?, ?, ?)',
                     (newId, name, folderName, encode(file_path)))
        files = list(literal_eval(sub_data[4]))
        files.append(newId)
        mydb.execute('UPDATE subjects SET files = ? where code = ?',
                     (str(files), subjectCode))
        return jsonify({'error': False})
    except Exception as x:
        print(x)
        return jsonify({'error': True})


@app.route("/addSub/<gradeid>", methods=["POST"])
def addSub(gradeid):
    id = session.get('schoolInPockID')
    if not id:
        return jsonify({'error': True})
    name = request.form.get('name')
    if not name:
        return jsonify({'error': True})
    print(name)
    try:
        mydb.execute('select * from schools where id = ?', (id,))
        school_data = mydb.fetchall()[0]
        if not gradeid in list(literal_eval(school_data[4])):
            return jsonify({'error': True})
        mydb.execute('select * from grades where code = ?', (gradeid,))
        g_data = mydb.fetchall()[0]
        subList = list(literal_eval(g_data[4]))
        print(subList)
        newId = mk_code2()
        mydb.execute("INSERT INTO subjects VALUES(?, ?, ?, ?, ?, ?)",
                     (newId, name, id, g_data[0], '[]', newId))
        subList.append(newId)
        mydb.execute("UPDATE grades SET subjects = ? WHERE code = ?",
                     (str(subList), gradeid))
        return jsonify({'error': False})
    except Exception as x:
        print(x)
        return jsonify({'error': True})


@app.route('/removeFiles/<gradeid>/<subjectid>', methods=["POST", "GET"])
def removeFile(gradeid, subjectid):
    id = session.get('schoolInPockID')
    if not id:
        return redirect(url_for('home'))
    remData = request.form.get('ids')
    if not remData:
        return jsonify({'error': True})
    remData = remData.split(',')
    print(remData)
    try:
        mydb.execute('select * from schools where id = ?', (id,))
        school_data = mydb.fetchall()[0]
        if not gradeid in list(literal_eval(school_data[4])):
            return jsonify({'error': True})
        mydb.execute('SELECT * FROM subjects WHERE code = ?', (subjectid,))
        sub_data = mydb.fetchall()[0]
        mydb.execute('select * from grades where code = ?', (gradeid,))
        grade_data = mydb.fetchall()[0]
        files = list(literal_eval(sub_data[4]))
        for i in remData:
            print(i)
            try:
                mydb.execute('SELECT * FROM files WHERE code = ?', (i,))
                file_data = mydb.fetchall()[0]
                file_path = os.path.join(subs_dir, file_data[2], file_data[1])
                print(file_path)
                if os.path.exists(file_path):
                    os.remove(file_path)
                mydb.execute('DELETE FROM files WHERE code = ?', (i,))
                files.remove(i)
            except Exception as x:
                print(x)
                return jsonify({'error': True})
        mydb.execute('UPDATE subjects SET files = ? WHERE code = ?',
                     (str(files), subjectid))
    except Exception as x:
        print(x)
        return jsonify({'error': True})
    return jsonify({'error': False})


@app.route("/sc/grade/<gradeid>/subjects")
def sc_grade_subs(gradeid):
    id = session.get('schoolInPockID')
    if not id:
        return redirect(url_for('home'))
    try:
        mydb.execute('select * from schools where id = ?', (id,))
        school_data = mydb.fetchall()[0]
        if not gradeid in list(literal_eval(school_data[4])):
            return redirect(url_for('home'))
    except:
        return redirect(url_for('home'))
    s_data, g_data, teachers_data, students_data, total_s, c_data, lst, path, subdata = get_data(
        id, gradeid)
    if s_data is None:
        return render_template('404.html')
    path.append(('>'))
    path.append(('Subjects', f"/sc/grade/{ gradeid }/subjects"))
    for ind, i in enumerate(subdata):
        # print(i[4])
        i = list(i)
        i.append(f'/addFile/{gradeid}/{i[0]}')
        files = []
        if not literal_eval(i[4]):
            i[4] = []
        else:
            for j in literal_eval(i[4]):
                try:
                    mydb.execute('select * from files where code = ?', (j,))
                    res = mydb.fetchall()[0]
                    folder = str(res[2])
                    fileName = str(res[1])
                    ex = fileName.rsplit('.', 1)[-1]
                    shortName = fileName.rsplit('.', 1)[0]
                    if not os.path.exists(os.path.join(subs_dir, folder)):
                        os.mkdir(os.path.join(subs_dir, folder))
                    file_path = os.path.join(subs_dir, folder, fileName)
                    if not os.path.exists(file_path):
                        decode(i[3], file_path)
                    if len(shortName) > 10:
                        shortName = shortName[:6] + '..' + shortName[-2:]
                    files.append([shortName + '.' + ex, url_for(
                        'static', filename=f'subjects/{res[2]}/{res[1]}'), create_icon(fileName), fileName, j])
                except Exception as x:
                    print(x)
                    pass
                i[4] = files
                # print(i[0])
                i.append(f'/removeFiles/{gradeid}/{i[0]}')
        subdata[ind] = i
    # print(subdata)

    return render_template(
        'subjects.html',
        path=path,
        lst=lst,
        sdata=subdata,
        addSubRoute=f'/addSub/{gradeid}'
    )


# @app.route("/sc/grade/<gradeid>/settings")
# def sc_grade_set(gradeid):
#     id = session.get('schoolInPockID')
#     if not id:
#         return redirect(url_for('home'))
#     s_data, g_data, teachers_data, students_data, total_s, c_data, lst, path, subdata = get_data(
        # id, gradeid)
#     


@app.route("/addPost/<gradeid>/<classid>", methods=["POST"])
def addPost(gradeid, classid):
    id = session.get('schoolInPockID')
    if not id:
        return jsonify({'error': True})
    data = request.form.get('data')
    if not data:
        return jsonify({'error': True})
    print(data)
    try:
        mydb.execute('select * from users where id = ?', (id,))
        user_data = mydb.fetchall()[0]
        mydb.execute('select * from classes where code = ?', (classid,))
        class_data = mydb.fetchall()[0]
        # print(class_data)
        mydb.execute('select * from grades where code = ?', (gradeid,))
        g_data = mydb.fetchall()[0]
        postsList = list(literal_eval(class_data[6]))
        print(postsList)
        newId = mk_code2()
        mydb.execute("INSERT INTO posts VALUES(?, ?, ?, ?, ?, ?, ?)",
                        (newId, classid, data, '[]', '', '[]', str([id, user_data[-1]])))
        postsList.append(newId)
        mydb.execute("UPDATE classes SET posts = ? WHERE code = ?",
                        (str(postsList), classid))
        return jsonify({'error': False})
    except Exception as x:
        print(x)
        return jsonify({'error': True})



@app.route("/sc/grade/<gradeid>/class/<classid>")
def sc_class(gradeid, classid):
    id = session.get('schoolInPockID')
    if not id:
        return redirect(url_for('home'))
    try:
        mydb.execute('select * from schools where id = ?', (id,))
        school_data = mydb.fetchall()[0]
        if not gradeid in list(literal_eval(school_data[4])):
            return redirect(url_for('home'))
        mydb.execute('select * from classes where code = ?', (classid,))
        class_data = mydb.fetchall()[0]
        print(class_data)
    except:
        return redirect(url_for('home'))
    s_data, g_data, teachers_data, students_data, total_s, c_data, lst, path, subdata = get_data(
        id, gradeid, class_data)
    if s_data is None or g_data is None:
        return redirect(url_for('home'))
    path.append(('>'))
    path.append((class_data[1], f"/sc/grade/{ gradeid }/class/{classid}"))
    posts = reversed(list(literal_eval(class_data[6])))
    posts_data = []
    for i in posts:
        try:
            mydb.execute('SELECT * FROM posts WHERE code = ?', (i,))
            x = list(mydb.fetchall()[0])
            owner = list(literal_eval(x[-1]))
            tp = owner[1]
            if tp == 'st':
                tp = 'students'
            elif tp == 't':
                tp = 'teachers'
            elif tp == 'sc':
                tp = 'schools'
            mydb.execute(f'SELECT * FROM {tp} WHERE id = ?', (owner[0],))
            owner_data = mydb.fetchall()[0]
            nm = owner_data[1]
            owner_name = [nm[0].upper(), nm]
            x[-1] = owner_name
            posts_data.append(x)
        except Exception as x:
            print(x)
            pass
    for i in posts_data:
        files = []
        for j in literal_eval(i[3]):
            try:
                mydb.execute('select * from files where code = ?', (j,))
                res = mydb.fetchall()[0]
                folder = str(res[2])
                fileName = str(res[1])
                ex = fileName.rsplit('.', 1)[-1]
                shortName = fileName.rsplit('.', 1)[0]
                if not os.path.exists(os.path.join(subs_dir, folder)):
                    os.mkdir(os.path.join(subs_dir, folder))
                file_path = os.path.join(subs_dir, folder, fileName)
                if not os.path.exists(file_path):
                    decode(i[3], file_path)
                if len(shortName) > 10:
                    shortName = shortName[:6] + '..' + shortName[-2:]
                files.append([shortName + '.' + ex, url_for(
                    'static', filename=f'subjects/{res[2]}/{res[1]}'), create_icon(fileName), fileName, j])
            except Exception as x:
                print(x)
                pass
            i[4] = files
    return render_template("class.html", sc=True, lst=lst, c=True, path=path, subs=subdata, posts=posts_data, add_sub=f'/addPost/{ gradeid }/{ classid }')


@app.route("/t")
def teacher():
    id = session.get('schoolInPockID')
    if not id:
        return redirect(url_for('home'))
    try:
        mydb.execute("SELECT * FROM teachers WHERE id = ?", (id,))
        data = mydb.fetchall()[0]
        path = [[data[1]]]
        classes = list(literal_eval(data[3]))
        cls_data = []
        for i in classes:
            mydb.execute('select * from classes where code = ?', (i,))
            try:
                result = list(mydb.fetchall()[0])
                students = list(literal_eval(result[4]))
                result.append(len(students))
                cls_data.append(result)
                result.append(f'/t/c/{result[0]}')
            except Exception as x:
                print(x)
        
        lst = [
            ("Classes :", len(classes)),
            ("Settings", "", "/t/settings"),
        ]
        return render_template("sc_t_st.html", path=path, lst=lst, c=True, t=True, frm='Class', placeholder='Class Code', cards=cls_data, frm_id='form_class_code', url_new_g='/t/AddC')
    except Exception as x:
        print(x)
        return render_template("404.html")


@app.route("/st")
def student():
    id = session.get('schoolInPockID')
    if not id:
        return redirect(url_for('home'))
    try:
        mydb.execute("SELECT * FROM students WHERE id = ?", (id,))
        data = mydb.fetchall()[0]
        path = [[data[1]]]
        classid = data[2]
        mydb.execute('select * from classes where code = ?', (classid,))
        cls_data = list(mydb.fetchall()[0])
        lst = [
            ("Settings", "", "/st/settings"),
        ]
        gradeid = cls_data[3]
        mydb.execute('select * from grades where code = ?', (gradeid,))
        g_data = list(mydb.fetchall()[0])
        posts = reversed(list(literal_eval(cls_data[6])))
        posts_data = []
        for i in posts:
            try:
                mydb.execute('SELECT * FROM posts WHERE code = ?', (i,))
                x = list(mydb.fetchall()[0])
                owner = list(literal_eval(x[-1]))
                tp = owner[1]
                if tp == 'st':
                    tp = 'students'
                elif tp == 't':
                    tp = 'teachers'
                elif tp == 'sc':
                    tp = 'schools'
                mydb.execute(f'SELECT * FROM {tp} WHERE id = ?', (owner[0],))
                owner_data = mydb.fetchall()[0]
                nm = owner_data[1]
                owner_name = [nm[0].upper(), nm]
                x[-1] = owner_name
                posts_data.append(x)
            except Exception as x:
                print(x)
                pass
        return render_template("class.html", sc=True, lst=lst, c=True, path=path, posts=posts_data, add_sub=f'/addPost/{ gradeid }/{ classid }')
    except Exception as x:
        print(x)
        return render_template("404.html")


@app.route("/t/AddC", methods=['POST'])
def t_addC():
    id = session.get('schoolInPockID')
    classid = request.form.get('classCode')
    print(classid)
    if not id or not classid:
        return jsonify({'exists': True, 'error': 'Not Found'})
    try:
        mydb.execute("SELECT * FROM teachers WHERE id = ?", (id,))
        data = mydb.fetchall()[0]
        mydb.execute("SELECT * FROM classes WHERE code = ?", (classid,))
        cls_data = mydb.fetchall()[0]
        clsList = list(literal_eval(data[3]))
        if classid in clsList:
            return jsonify({'exists': True, 'error': 'Already exists'})
        tList = list(literal_eval(cls_data[5]))
        clsList.append(classid)
        tList.append(id)
        mydb.execute('update teachers set classes = ? where id = ?', (str(clsList), id))
        mydb.execute('update classes set teachers = ? where code = ?', (str(tList), classid))
        return jsonify({'exists': False})
    except Exception as x:
        print(x)
        return jsonify({'exists': True, 'error': 'Not Found'})


@app.route("/t/c/<classid>")
def t_class(classid):
    id = session.get('schoolInPockID')
    if not id:
        return redirect(url_for('home'))
    try:
        mydb.execute('select * from teachers where id = ?', (id,))
        data = mydb.fetchall()[0]
        mydb.execute('select * from classes where code = ?', (classid,))
        cls_data = mydb.fetchall()[0]
        gradeid = cls_data[3]
        mydb.execute('select * from classes where code = ?', (classid,))
        class_data = mydb.fetchall()[0]
        print(class_data)
    except:
        return redirect(url_for('home'))
    posts = reversed(list(literal_eval(class_data[6])))
    posts_data = []
    for i in posts:
        try:
            mydb.execute('SELECT * FROM posts WHERE code = ?', (i,))
            x = list(mydb.fetchall()[0])
            owner = list(literal_eval(x[-1]))
            tp = owner[1]
            if tp == 'st':
                tp = 'students'
            elif tp == 't':
                tp = 'teachers'
            elif tp == 'sc':
                tp = 'schools'
            mydb.execute(f'SELECT * FROM {tp} WHERE id = ?', (owner[0],))
            owner_data = mydb.fetchall()[0]
            nm = owner_data[1]
            owner_name = [nm[0].upper(), nm]
            x[-1] = owner_name
            posts_data.append(x)
        except Exception as x:
            print(x)
            pass
    for i in posts_data:
        files = []
        for j in literal_eval(i[3]):
            try:
                mydb.execute('select * from files where code = ?', (j,))
                res = mydb.fetchall()[0]
                folder = str(res[2])
                fileName = str(res[1])
                ex = fileName.rsplit('.', 1)[-1]
                shortName = fileName.rsplit('.', 1)[0]
                if not os.path.exists(os.path.join(subs_dir, folder)):
                    os.mkdir(os.path.join(subs_dir, folder))
                file_path = os.path.join(subs_dir, folder, fileName)
                if not os.path.exists(file_path):
                    decode(i[3], file_path)
                if len(shortName) > 10:
                    shortName = shortName[:6] + '..' + shortName[-2:]
                files.append([shortName + '.' + ex, url_for(
                    'static', filename=f'subjects/{res[2]}/{res[1]}'), create_icon(fileName), fileName, j])
            except Exception as x:
                print(x)
                pass
            i[4] = files
    classes = list(literal_eval(data[3]))
    path = [[data[1]]]
    lst = [
            ("Classes :", len(classes)),
            ("Settings", "", "/t/settings"),
        ]
    return render_template("class.html", sc=True, lst=lst, c=True, path=path, posts=posts_data, add_sub=f'/addPost/{ gradeid }/{ classid }')


if __name__ == "__main__":
    app.run(debug=1)
