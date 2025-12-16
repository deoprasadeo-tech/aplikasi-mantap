from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Data antrean
current_queue = {
    "A": None,
    "B": None,
    "C": None,
    "D": None,
}
last_number = {
    "A": 0,
    "B": 0,
    "C": 0,
    "D": 0
}

# Simulasi user
users = {
    "kanimpati": {"username": "kanimpati", "password": "imipatiwbk"}
}

# Model user
class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    if username in users:
        return User(username)
    return None

@app.route('/')
def home():
    return render_template('home.html', current_queue=current_queue)

@app.route('/get_queue')
def get_queue():
    return jsonify(current_queue)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            flash('Login berhasil!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Username atau password salah!', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html', current_queue=current_queue)

@app.route('/call_queue/<jenis>/<queue_type>')
@login_required
def call_queue(jenis, queue_type):
    if jenis in current_queue and queue_type in last_number:
        last_number[queue_type] += 1
        current_queue[jenis] = f"{queue_type}-{last_number[queue_type]}"
    return redirect(url_for('admin'))

@app.route('/reset', methods=['POST'])
@login_required
def reset():
    for jenis in current_queue:
        current_queue[jenis] = None
    for key in last_number:
        last_number[key] = 0
    flash('Antrean berhasil direset!', 'success')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
