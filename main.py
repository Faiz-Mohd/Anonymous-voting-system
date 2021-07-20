from flask import Flask, render_template,request, session,redirect,url_for


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
                    return redirect(url_for("dashboard"))
                else:
                    return "Wrong password!"
            else:
                return "Account doesn't Exist"
        else:
            if 'loggedin' in session:
                return redirect(url_for("dashboard"))
            return render_template('auth/login.html')

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
                session['loggedin'] = True
                session['name'] = name
                return redirect(url_for("dashboard"))
        else:
            return render_template('auth/register.html')

    @app.route("/dashboard")
    def dashboard():
        if 'loggedin' in session:
            name = session['name']
            return render_template('dashboard.html',name=name)
        else:
            return redirect(url_for("login"))

    @app.route("/logout")
    def logout():
        session.pop('loggedin', None)
        session.pop('name', None)
        return redirect(url_for('login'))

    return app