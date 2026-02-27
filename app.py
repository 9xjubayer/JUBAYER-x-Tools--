from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = "super_secret_key" # আপনার নিজের সিক্রেট কি দিন

# অ্যাডমিন পাসওয়ার্ড (পরিবর্তন করে নিন)
ADMIN_PASSWORD = "admin123"
DATA_FILE = "data.json"

# ডেটা লোড করার ফাংশন
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# ডেটা সেভ করার ফাংশন
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    links = load_data()
    return render_template('index.html', links=links)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin'))
    return '''
        <form method="post" style="text-align:center; margin-top:50px;">
            <input type="password" name="password" placeholder="Admin Password">
            <button type="submit">Login</button>
        </form>
    '''

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    links = load_data()
    if request.method == 'POST':
        new_entry = {
            "name": request.form.get('webname'),
            "url": request.form.get('url'),
            "image": request.form.get('pnglink')
        }
        links.append(new_entry)
        save_data(links)
        return redirect(url_for('admin'))
        
    return render_template('admin.html', links=links)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
