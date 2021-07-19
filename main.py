from flask import Flask, render_template,request

def create_app():
    app = Flask("new")
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
            return render_template('index.html',name=name)
        else:
            return render_template('auth/register.html')
    return app