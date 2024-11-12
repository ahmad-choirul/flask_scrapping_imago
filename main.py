from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import session
from functools import wraps
from bs4 import BeautifulSoup
import requests
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'kunci'  # Diperlukan untuk session

@app.route('/')
def index():
    buah = ["apel", "jeruk", "mangga", "pisang", "durian"]
    listdic = [
        {"id": 1, "name": "alice", "category": "A", "sub_category": "X"},
        {"id": 2, "name": "Bob", "category": "B", "sub_category": "Y"},
        {"id": 3, "name": "Charlie", "category": "A", "sub_category": "Z"},
        {"id": 4, "name": "David", "category": "B", "sub_category": "X"}]

    categories = {}
    # Menggunakan listdic untuk mengelompokkan data
    for item in listdic:
        category = item["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append({"id": item["id"], "name": item["name"]})
    
    return render_template('index.html', dic=categories)

@app.route('/parsing', methods=['POST'])
def parsing():
    # Mendapatkan data dari POST request
    data = request.get_json()
    
    if not data:
        return {"error": "No data provided"}, 400
    
    # Mengelompokkan data berdasarkan kategori 
    categories = {}
    for item in data:  # Menggunakan data dari request
        category = item["category"]
        sub_category = item["sub_category"]
        if category not in categories:
            categories[category] = {}
        if sub_category not in categories[category]:
            categories[category][sub_category] = []
        categories[category][sub_category].append(item)
        
    return render_template('index.html', dic=categories)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # contoh password manual 
        if username == "admin" and password == "admin123":
            session['username'] = username
            return redirect('/')
        else:
            return render_template('login.html', error="Username atau password salah")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')
# Fungsi untuk mengambil data dari detik.com
def scrap_detik(search_term=None):
    # Setel URL pencarian dengan default 'jember'
    url = f"https://www.detik.com/search/searchall?query={search_term}" if search_term else "https://www.detik.com/search/searchall?query=jember"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        soup = BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.ConnectionError:
        return render_template('error.html', error="Tidak ada koneksi internet. Silakan coba lagi nanti.")
    except requests.exceptions.HTTPError:
        return render_template('error.html', error="Gagal mengambil data. Silakan coba lagi nanti.")
    
    # ambil seluruh data dan di masukan ke variabel articles
    articles = soup.find_all('article')
    data = []

    # Looping setiap artikel dan ekstrak informasi
    for article in articles:
        title = article.find('div', class_='dtr-ttl').text.strip() if article.find('div', class_='dtr-ttl') else ''
        sub_title = article.find('a', attrs={'dtr-ttl': True}).get('dtr-ttl') if article.find('a', attrs={'dtr-ttl': True}) else ''
        image_link = article.find('img')['src'] if article.find('img') else ''
        body_text = article.find('div', class_='media__desc').text.strip() if article.find('div', class_='media__desc') else ''
        tanggal_hari = article.find('div', class_='media__date').find('span')['title'] if article.find('div', class_='media__date') and article.find('div', class_='media__date').find('span') else ''
       

        # Tmemasukan kedalam array 
        data.append({
            'title': title,
            'sub_title': sub_title,
            'image_link': image_link,
            'body_text': body_text,
            'publication_time': tanggal_hari
        })

    # Paginasi data, 10 artikel per halaman
    paginated_data = [data[i:i+10] for i in range(0, len(data), 10)]

    return paginated_data

# route untuk melihat data yang diambil
@app.route('/scrap-detik', methods=['GET'])
def scrap_detik_view():
    #ambil data get dengan default jember jika kosong
    search_term = request.args.get('search_term', 'jember')
    data = scrap_detik(search_term)
    return render_template('scrap_detik.html', data=data, search_term=search_term)

# API untuk mendapatkan data yang diambil
@app.route('/scrap-detik-api', methods=['GET'])
def scrap_detik_api():
    search_term = request.args.get('search_term')
    data = scrap_detik(search_term)
    return jsonify(data)


app.run(debug=True)