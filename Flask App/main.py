from flask import Flask, render_template,request, session,redirect,url_for
from datetime import datetime

def create_app():
    app = Flask("new")
    app.config.from_mapping(
        DATABASE="mydb"
    )
    app.secret_key = 'secret'

    from . import db
    db.init_app(app)

    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/login", methods =['GET', 'POST'])
    def login():
        msg=""
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            email = request.form['email']
            password = request.form['password']
            conn = db.get_db()
            curs = conn.cursor()
            curs.execute("select * from users where email = %s", (email, ))
            account = curs.fetchone()
            if account:
                if account[3]==password:
                    session['loggedin']=True
                    session['name']=account[1]
                    session['u_id'] = account[0]
                    return redirect(url_for("dashboard"))
                else:
                    return render_template('auth/login.html',msg="Wrong password")
            else:
                return render_template('auth/login.html',msg="Account doesn't Exist")
        else:
            if 'loggedin' in session:
                return redirect(url_for("dashboard"))
            return render_template('auth/login.html',msg=msg)

    @app.route("/register", methods =['GET', 'POST'])
    def register():
        if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'cpassword' in request.form and 'email' in request.form:
            name = request.form['name']
            password = request.form['password']
            email = request.form['email']
            conn = db.get_db()
            curs = conn.cursor()
            curs.execute("select * from users where email = %s", (email, ))
            account = curs.fetchone()
            if account:
                return render_template('auth/register.html',msg="Account already Exists")
            else:
                curs.execute("insert into users(name,email,password) values (%s, %s, %s)", (name, email, password, ))
                conn.commit()
                curs.execute("select * from users where email = %s", (email,))
                account = curs.fetchone()
                session['u_id']=account[0]
                session['loggedin'] = True
                session['name'] = name
                msg="Account created successfully"
                return render_template('dashboard.html',name=name,msg=msg)
        else:
            return render_template('auth/register.html')

    @app.route("/dashboard", methods =['GET', 'POST'])
    def dashboard():
        if request.method == 'POST' and 'u_id' in session:
            question=request.form['question']
            options = request.form.getlist('options[]')
            date=request.form['date']
            time=request.form['time']
            conn = db.get_db()
            curs = conn.cursor()
            u_id=session['u_id']
            name = session['name']
            curs.execute("insert into polls (u_id,question,end_date,end_time) values (%s,%s,%s,%s)",(u_id,question,date,time))
            conn.commit()
            curs.execute("select poll_id from polls where u_id= %s order by poll_id desc limit 1",(u_id, ))
            poll=curs.fetchone()[0]
            for op in options:
                curs.execute("insert into options (p_id,options,votes) values (%s,%s,%s)",(poll, op,0))
            conn.commit()
            return render_template('dashboard.html', msg="Poll Created Successfully",name=name)
        elif 'loggedin' in session:
            if 'msg' in request.args:
                msg = request.args['msg']
            else:
                msg=''
            name = session['name']
            return render_template('dashboard.html',name=name,msg=msg)
        else:
            return redirect(url_for("login"))

    @app.route("/dashboard/polls")
    def poll_list():
        if 'loggedin' in session:
            conn = db.get_db()
            curs = conn.cursor()
            u_id = session['u_id']
            name=session['name']
            curs.execute("select * from polls where u_id= %s order by poll_id desc", (u_id,))
            polls = curs.fetchall()
            return render_template('polls.html',polls=polls,name=name)
        else:
            return redirect(url_for("login"))

    @app.route("/dashboard/polls/<pid>")
    def poll_result(pid):
        if 'loggedin' in session:
            u_id=session['u_id']
            name = session['name']
            conn = db.get_db()
            curs = conn.cursor()
            curs.execute("select question from polls where u_id= %s and poll_id=%s", (u_id,pid))
            res=curs.fetchone()
            if res:
                question=res[0]
                curs.execute("select options,votes from options where p_id= %s", (pid,))
                result=curs.fetchall()
                a=[]
                b=[]
                for x in result:
                    a.append(x[0])
                    b.append(x[1])
                return render_template('poll_result.html', pid=pid, question=question,a=a,b=b,name=name)
            else:
                return redirect(url_for("poll_list"))
        else:
            return redirect(url_for("login"))

    @app.route("/polls/<pid>")
    def polling(pid):
        conn = db.get_db()
        curs = conn.cursor()
        curs.execute("select * from polls where poll_id=%s", (pid,))
        res = curs.fetchone()
        date=res[3]
        time=res[4]
        com=datetime.combine(date,time)
        curr=datetime.now()
        diff=(com-curr).total_seconds()
        if diff<1:
            return render_template('voting_page.html', msg="The Poll you are looking for is no longer accepting responses")
        question=res[2]
        curs.execute("select options from options where p_id=%s", (pid,))
        op = curs.fetchall()
        options=[]
        for x in op:
            options.append(x[0])
        return render_template('voting_page.html',question=question,options=options,pid=pid)

    @app.route("/polls/<pid>/vote", methods=['GET','POST'])
    def vote(pid):
        if request.method == 'POST' and 'radio' in request.form:
            value=request.form['radio']
            conn = db.get_db()
            curs = conn.cursor()
            curs.execute("update options set votes=votes+1 where p_id= %s and options= %s", (pid,value, ))
            conn.commit()
            return render_template('voting_page.html',msg="Your response have submitted successfully.")
        else:
            return redirect(url_for("polling",pid=pid))


    @app.route("/logout")
    def logout():
        session.pop('loggedin', None)
        session.pop('name', None)
        session.pop('u_id', None)
        return redirect(url_for('login'))


    return app