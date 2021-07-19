from flask import Flask, render_template

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
        return render_template('auth/register.html')
    return app