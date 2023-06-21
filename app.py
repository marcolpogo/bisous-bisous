from database import Database
from flask import Flask
from flask import render_template,  request, g, redirect, url_for, session
from flask_session import Session
from datetime import timedelta

# Instanciation de l'app
app = Flask(__name__, static_url_path="", static_folder="static")

app.secret_key = "like-me-like-me-not"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 10)
Session(app)

cookie_name = 'bisous-session-id'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()

  
# Page de connexion du username
@app.route('/', methods=['GET'])
def login():
    error = request.args.get('error')
    return render_template('login.html', error=error)


@app.route('/validate', methods=['POST'])
def validate():
    # If these field aren't there : error 400
    username = request.form['username']
    password = request.form['password']
    
    # Check for invalid char (only in username)
    blacklist = [";"]
    for char in blacklist:
        if char in username: 
            msg = "Invalid character...? 🥲"
            return redirect(url_for('login', error=msg))

    # Invalid username
    if len(get_db().get_user(username)) == 0:
        return redirect(url_for('login', error='Wrong username baby 🙃'))

    # Valid password and username
    if get_db().is_valid_password(username, password):
        # Initialize session
        session[cookie_name] = username # Change for automatic randomized value?
        return redirect(url_for('two_factor_auth'))

    # Invalid password
    return redirect(url_for('login', error='Oops... Forgot your password? 🤨'))


# Page de 2-Factor-Authentification
@app.route('/two-factor-auth', methods=['GET'])
def two_factor_auth():
    # Check if user is logged in
    if cookie_name not in session:
        return redirect(url_for('login'))

    # Check for user-agent
    user_agent = request.headers.get('User-Agent')
    device = 'Intel Mac OS X 45.55'
    if device in user_agent:
        return 'UQAM{1_H0P3_2FA_1SNT_R34LLY_L1K3_TH4T}'
    else:
        return render_template('two-factor-auth.html')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop(cookie_name, None)
    return redirect("/")
    