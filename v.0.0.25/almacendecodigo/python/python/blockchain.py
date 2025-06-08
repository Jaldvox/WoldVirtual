from flask import Flask, jsonify, request
import hashlib
import datetime
import random
import json
from flask import render_template, redirect, url_for

app = Flask(__name__)

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.usuarios = {}
        self.crear_bloque_genesis()
        # HTML templates stored as strings
        self.html_templates = {
            'index': '''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Blockchain App</title>
                    <style>
                        body { font-family: Arial; margin: 40px; }
                        .nav { background: #333; padding: 15px; }
                        .nav a { color: white; margin-right: 15px; }
                        .container { margin-top: 20px; }
                    </style>
                </head>
                <body>
                    <div class="nav">
                        <a href="/login">Login</a>
                        <a href="/register">Register</a>
                    </div>
                    <div class="container">
                        <h1>Welcome to Blockchain App</h1>
                    </div>
                </body>
                </html>
            ''',
            'login': '''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Login</title>
                    <style>
                        .login-form { max-width: 300px; margin: 50px auto; }
                        input { width: 100%; padding: 8px; margin: 10px 0; }
                        button { width: 100%; padding: 10px; background: #4CAF50; color: white; }
                    </style>
                </head>
                <body>
                    <div class="login-form">
                        <h2>Login</h2>
                        <form method="POST">
                            <input type="text" name="username" placeholder="Username">
                            <input type="password" name="password" placeholder="Password">
                            <button type="submit">Login</button>
                        </form>
                    </div>
                    <script>
                        // Add client-side validation
                        document.querySelector('form').onsubmit = function(e) {
                            const username = document.querySelector('[name="username"]').value;
                            const password = document.querySelector('[name="password"]').value;
                            if (!username || !password) {
                                e.preventDefault();
                                alert('Please fill all fields');
                            }
                        }
                    </script>
                </body>
                </html>
            '''
        }

class BlockchainWeb:
    def __init__(self):
        self.chain = []
        self.usuarios = {}
        self.template = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Blockchain Dashboard</title>
                <style>
                    body { font-family: Arial; margin: 20px; }
                    .container { max-width: 1200px; margin: 0 auto; }
                    .block { border: 1px solid #ddd; margin: 10px; padding: 15px; border-radius: 5px; }
                    .nav { background: #333; padding: 15px; margin-bottom: 20px; }
                    .nav a { color: white; margin-right: 15px; text-decoration: none; }
                    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                    .login-form { max-width: 300px; margin: 50px auto; }
                    input, textarea { width: 100%; padding: 8px; margin: 10px 0; }
                    button { padding: 10px; background: #4CAF50; color: white; border: none; cursor: pointer; }
                </style>
            </head>
            <body>
                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/dashboard">Dashboard</a>
                    <a href="/mine">Mine Block</a>
                    <a href="/monitor">Monitor</a>
                    <a href="/login">Login</a>
                </div>
                <div class="container">
                    {content}
                </div>
            </body>
            </html>
        '''
        
        # Initialize blockchain with genesis block
        genesis_block = {
            'index': 0,
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data': 'Genesis Block',
            'previous_hash': '0'
        }
        self.chain.append(genesis_block)

    def hash_block(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = {
            'index': len(self.chain),
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data': data,
            'previous_hash': self.hash_block(previous_block)
        }
        self.chain.append(new_block)
        return new_block

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            if self.chain[i]['previous_hash'] != self.hash_block(self.chain[i-1]):
                return False
        return True

    def register_user(self, username, password):
        if username not in self.usuarios:
            self.usuarios[username] = {
                'password': hashlib.sha256(password.encode()).hexdigest(),
                'recursos': {'cpu': 20, 'bandwidth': 20}
            }
            return True
        return False

    def verify_user(self, username, password):
        if username in self.usuarios:
            return self.usuarios[username]['password'] == hashlib.sha256(password.encode()).hexdigest()
        return False

    def monitor_resources(self):
        return {
            username: {
                'cpu_usage': round(random.uniform(0, 100), 2),
                'memory_usage': round(random.uniform(0, 1024), 2),
                'network_usage': round(random.uniform(0, 50), 2),
                'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            } for username in self.usuarios
        }

    def render_page(self, page_type, **kwargs):
        content = ""
        if page_type == 'dashboard':
            content = ''.join(f'<div class="block"><pre>{json.dumps(block, indent=2)}</pre></div>' 
                            for block in self.chain)
            content = f"<h1>Blockchain Dashboard</h1>{content}"
            
        elif page_type == 'monitor':
            monitoring_data = self.monitor_resources()
            rows = ''.join(
                f'<tr><td>{username}</td><td>{data["cpu_usage"]}%</td>'
                f'<td>{data["memory_usage"]} MB</td><td>{data["network_usage"]} Mbps</td>'
                f'<td>{data["timestamp"]}</td></tr>'
                for username, data in monitoring_data.items()
            )
            content = f'''
                <h1>Resource Monitoring</h1>
                <table>
                    <tr>
                        <th>Username</th>
                        <th>CPU Usage</th>
                        <th>Memory Usage</th>
                        <th>Network Usage</th>
                        <th>Timestamp</th>
                    </tr>
                    {rows}
                </table>
            '''
            
        elif page_type == 'mine':
            content = '''
                <h1>Mine New Block</h1>
                <form method="POST" action="/mine">
                    <textarea name="data" placeholder="Enter block data"></textarea>
                    <button type="submit">Mine Block</button>
                </form>
            '''
            
        elif page_type == 'login':
            content = '''
                <div class="login-form">
                    <h2>Login</h2>
                    <form method="POST" action="/login">
                        <input type="text" name="username" placeholder="Username" required>
                        <input type="password" name="password" placeholder="Password" required>
                        <button type="submit">Login</button>
                    </form>
                </div>
            '''
            
        return self.template.format(content=content)

# Initialize the blockchain web application
blockchain_web = BlockchainWeb()

@app.route('/')
def home():
    return blockchain_web.render_page('dashboard')

@app.route('/dashboard')
def dashboard():
    return blockchain_web.render_page('dashboard')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if blockchain_web.verify_user(request.form['username'], request.form['password']):
            return redirect(url_for('dashboard'))
        return blockchain_web.render_page('login') + '<script>alert("Invalid credentials");</script>'
    return blockchain_web.render_page('login')

@app.route('/mine', methods=['GET', 'POST'])
def mine():
    if request.method == 'POST':
        blockchain_web.add_block(request.form.get('data', ''))
        return redirect(url_for('dashboard'))
    return blockchain_web.render_page('mine')

@app.route('/monitor')
def monitor():
    return blockchain_web.render_page('monitor')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
