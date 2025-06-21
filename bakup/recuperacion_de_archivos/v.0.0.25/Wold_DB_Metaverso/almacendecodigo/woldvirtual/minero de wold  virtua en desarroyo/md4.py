from flask import Flask, render_template_string

app = Flask(__name__)

# Global variable for registered providers
registered_providers = []

@app.route('/')
def get_server_status():
    """Route to get backend status and display shared resources interface."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .resource-box {
                width: 80%;
                max-width: 600px;
                margin: 20px auto;
                padding: 20px;
                border: 2px solid #ccc;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            .status-info {
                margin-bottom: 20px;
                padding: 10px;
                background-color: #e8f5e9;
                border-radius: 4px;
            }
            .share-form {
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            .share-form input, .share-form textarea {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            .share-button {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="resource-box">
            <h2>Backend Status</h2>
            <div class="status-info">
                <p>Server Status: <span id="server-status">Up</span></p>
                <p>Database Status: <span id="database-status">Up</span></p>
                <p>Cache Status: <span id="cache-status">Up</span></p>
                <p>Registered Providers: {{ providers }}</p>
            </div>
            <form class="share-form" action="/share" method="POST">
                <h3>Share Resources</h3>
                <input type="text" placeholder="Resource Title" required>
                <textarea placeholder="Resource Description" required></textarea>
                <input type="url" placeholder="Resource URL" required>
                <button type="submit" class="share-button">Share Resource</button>
            </form>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_content, providers=len(registered_providers))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
