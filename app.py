from flask import Flask, request, render_template,redirect,url_for,session
import requests
# import pandas as pd
# import json

app = Flask(__name__, static_folder='static', static_url_path='/')
app.secret_key = 'some_secret_key_tayyip_is_should_know'

@app.before_request
def check_login():
    allowed_routes = ["login", "static"]  # Giriş yapmadan erişime izin verilen sayfalar
    if request.endpoint not in allowed_routes and "username" not in session:
        return redirect(url_for("login"))
    
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Kullanıcının girdiği değeri alalım
        query = request.form['query'].upper()
        
        if query == "" :
            pass
        else :
            # REST API'ye istek gönderelim
            # response = requests.get('https://fakestoreapi.com/products/' + query)
            response = requests.get('https://dummyjson.com/products/' + query)
            
            # API yanıtını bir değişkene ata
            try:
                result = response.json()

                # Sonucu bir Flask şablonunda kullanmak için değişkeni geri döndür
                return render_template('index.html', result=result)
            except Exception as ex:
                print(f'Sonuç bulunamadı. {ex}')
                error = (f'"{query}" için sonuç bulunamadı. {ex}')
                return render_template('index.html', error=error)
    
    return render_template("index.html")
    

users = {
    "tayyip": "1",
    "user2": "2"
}

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if username in users and users[username] == password:
            # Kullanıcı doğrulandı, ana sayfaya yönlendir
            session["username"] = username
            username = request.form["username"]
            return redirect(url_for('home'))
        else:
            error = "Kullanıcı adı veya şifre hatalı."
            return render_template("login.html", error=error)
    
    return render_template("login.html")


@app.context_processor
def inject_user():
    username = session.get("username")
    return dict(username=username)


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html") # veya başka bir sayfa


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
    

