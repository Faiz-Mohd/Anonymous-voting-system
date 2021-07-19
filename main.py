from flask import Flask, render_template,request

def create_app():
    app = Flask("new")
    app.config.from_mapping(
        DATABASE="mydb"
    )
    from . import db
    db.init_app(app)

    @app.route("/")
    def index():
        return render_template('index.html')
    @app.route("/login")
    def login():
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
                return "Account already Exists!"
            else:
                curs.execute("insert into users(name,email,password) values (%s, %s, %s)", (name, email, password))
                conn.commit()
                return render_template('index.html',name=name)
        else:
            return render_template('auth/register.html')
    return app