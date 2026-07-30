from flask import Flask, render_template_string, jsonify
from markupsafe import Markup
import redis
from datetime import datetime

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask App</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
            max-width: 600px;
            width: 100%;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }
        
        .content {
            padding: 40px;
            text-align: center;
        }
        
        .counter-display {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 30px;
            margin: 20px 0;
        }
        
        .counter-label {
            color: #666;
            font-size: 1em;
            margin-bottom: 10px;
        }
        
        .counter-number {
            font-size: 4em;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .timestamp {
            color: #999;
            font-size: 0.9em;
            margin-top: 10px;
        }
        
        .stats {
            background: #e8f0fe;
            border-left: 4px solid #667eea;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            text-align: left;
        }
        
        .stats p {
            margin: 8px 0;
            color: #333;
        }
        
        .stats strong {
            color: #667eea;
        }
        
        .button-group {
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 30px;
        }
        
        a.btn {
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
            font-weight: 600;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }
        
        .btn-secondary {
            background: #e8f0fe;
            color: #667eea;
            border: 2px solid #667eea;
        }
        
        .btn-secondary:hover {
            background: #667eea;
            color: white;
        }
        
        .alert {
            background: #fff3cd;
            border: 1px solid #ffc107;
            color: #856404;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome</h1>
        </div>
        
        <div class="content">
            {{ content | safe }}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def welcome():
    visits = r.get('visits') or '0'
    content = Markup(f"""
        <h2>Welcome! 👋</h2>
        <p>This is a containerized Flask application demonstrating Docker and Redis integration.</p>
        
        <div class="counter-display">
            <div class="counter-label">Total Visits</div>
            <div class="counter-number">{visits}</div>
        </div>
        
        <div class="stats">
            <p><strong>📊 Statistics:</strong></p>
            <p>Total page visits: <strong>{visits}</strong></p>
            <p>Application running in Docker ✓</p>
            <p>Redis cache connected ✓</p>
        </div>
        
        <div class="button-group">
            <a href="/count" class="btn btn-primary">📈 View Counter</a>
            <a href="/stats" class="btn btn-secondary">📊 View Stats</a>
        </div>
    """)
    return render_template_string(HTML_TEMPLATE, content=content)

@app.route('/count')
def count():
    count = int(r.incr('visits'))
    r.set('last_visit', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    content = Markup(f"""
        <h2>Visit Counter 📈</h2>
        
        <div class="counter-display">
            <div class="counter-label">Page Views</div>
            <div class="counter-number">{count}</div>
            <div class="timestamp">Last visit: {r.get('last_visit')}</div>
        </div>
        
        <div class="alert">
            ✨ This page has been visited <strong>{count}</strong> times!
        </div>
        
        <p style="margin: 20px 0; color: #666;">Each time you visit this page, the counter increments thanks to Redis persistence.</p>
        
        <div class="button-group">
            <a href="/" class="btn btn-secondary">← Back Home</a>
        </div>
    """)
    return render_template_string(HTML_TEMPLATE, content=content)

@app.route('/stats')
def stats():
    visits = r.get('visits') or '0'
    last_visit = r.get('last_visit') or 'Never'
    
    content = Markup(f"""
        <h2>Statistics 📊</h2>
        
        <div class="stats">
            <p><strong>📈 Total Visits:</strong> {visits}</p>
            <p><strong>🕐 Last Visit:</strong> {last_visit}</p>
            <p><strong>🐳 Deployment:</strong> Docker Container</p>
            <p><strong>💾 Cache System:</strong> Redis</p>
            <p><strong>🔗 Framework:</strong> Flask</p>
        </div>
        
        <p style="margin: 20px 0; color: #666;">All data is persisted in Redis database for reliability.</p>
        
        <div class="button-group">
            <a href="/" class="btn btn-secondary">← Home</a>
            <a href="/count" class="btn btn-primary">📈 Counter</a>
        </div>
    """)
    return render_template_string(HTML_TEMPLATE, content=content)

@app.route('/api/visits')
def api_visits():
    return jsonify({
        'visits': int(r.get('visits') or 0),
        'last_visit': r.get('last_visit') or None
    })

@app.errorhandler(404)
def not_found(error):
    content = Markup("""
        <h2>404 - Page Not Found 🔍</h2>
        <p>The page you're looking for doesn't exist.</p>
        <div class="button-group">
            <a href="/" class="btn btn-primary">← Back Home</a>
        </div>
    """)
    return render_template_string(HTML_TEMPLATE, content=content), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
    # HTML added 