from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import session
from functools import wraps

app = Flask(__name__)
app.secret_key = 'fghf'

@app.route('/')
def index():
    listdic = [
        {"id": 1, "name": "alice", "category": "A", "sub_category": "X"},
        {"id": 2, "name": "Bob", "category": "B", "sub_category": "Y"},
        {"id": 3, "name": "Charlie", "category": "A", "sub_category": "Z"},
        {"id": 4, "name": "David", "category": "B", "sub_category": "X"}]

    return render_template('index.html')

@app.route('/parsing', methods=['POST'])
def parsing():
    # Mendapatkan data dari POST request
    data = request.get_json()
    
    if not data:
        return {"error": "No data provided"}, 400
    
    # Mengelompokkan data berdasarkan kategori 
    categories = {}
    for item in data:
        category = item["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append(item)
        
    listdic = categories
    return render_template('index.html', dic=listdic)

app.run(debug=True)