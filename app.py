from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
# import urllib3

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/forex-news")
def kompas_food():
    # Dapatkan halaman web
    url = "https://www.forexfactory.com/news"
    response = requests.get(url, verify=False)

    # Periksa apakah permintaan berhasil
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Temukan elemen dengan class "body flexposts" yang berisi berita-berita
        large = soup.find(attrs={'class': 'pagearrange__layout-row full'})
        if large:
            return 'ada'
        else:
            return 'tidak ada'
        medium = large.find(attrs={'class': 'flexBox news'})
        
        area_latest_story = medium.find('div', id_='flexBox_flex_news_newsLeft1')

        # Temukan semua elemen berita
        if area_latest_story:
            news_items = area_latest_story.find_all('li', class_='flexposts__item')
            # Lanjutkan pemrosesan berita
            news = []

            for item in news_items:
                title = item.find('div', class_='flexposts__story-title').find('a').text.strip()
                link = item.find('div', class_='flexposts__story-title').find('a')['href']
                source = item.find('span', class_='flexposts__caption').find('a').text.strip()
                time = item.find('span', class_='flexposts__time').text.strip()

                news.append({
                    'title': title,
                    'link': link,
                    'source': source,
                    'time': time
                })

            return render_template("a_berita1.html", news=news)
        else:
            return 'file kosong'
    else:
            # Tindakan jika elemen tidak ditemukan
        # Siapkan daftar berita untuk ditampilkan di template
       
        # Jika permintaan tidak berhasil, Anda dapat menangani kesalahan di sini
        return "Gagal mengambil data berita."
@app.route("/travel-antara")
def tempo_nasional():
    html_doc = requests.get("https://www.antaranews.com/lifestyle/travel")
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    popular_area = soup.find(attrs={'class': 'main-content mag-content clearfix'})

    texts = popular_area.findAll(attrs={'class': 'text-card'})
    images = popular_area.findAll(attrs={'class': 'simple-post simple-big clearfix'})

    return render_template("a_berita2.html", images=images, texts=texts)

@app.route("/travel-kompas")
def grid_tekno():
    html_doc = requests.get("https://travel.kompas.com/jalan-jalan")
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    popular_area = soup.find(attrs={'class': 'col-bs10-7'})

    texts = popular_area.findAll(attrs={'class': 'news-list__details'})
    images = popular_area.findAll(attrs={'class': 'article__list clearfix'})

    return render_template("a_berita3.html", images=images, texts=texts)


app.run(debug=True)

