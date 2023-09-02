from flask import Flask, request, render_template,redirect,url_for,session
import requests
import pandas as pd
# import json
import cx_Oracle
from cx_Oracle import Connection, SessionPool
from flask_sqlalchemy import SQLAlchemy
import config as conf

app = Flask(__name__, static_folder='static', static_url_path='/')
app.secret_key = 'some_secret_key_tayyip_is_should_know'

#login controller
@app.before_request
def check_login():
    allowed_routes = ["login", "static"]  # Giriş yapmadan erişime izin verilen sayfalar
    if request.endpoint not in allowed_routes and "username" not in session:
        return redirect(url_for("login"))

#home and page func...    
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

#login
@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if verify_user(username, password):
            session["username"] = username
            return redirect(url_for("home"))
        else:
            error = "Kullanıcı adı veya şifre hatalı."
            return render_template("login.html", error=error)
    
    return render_template("login.html")


# Connection pooling
def create_connection_pool():
    try:
        pool = SessionPool(
            user=conf.db_user,
            password=conf.db_password,
            dsn=conf.db_dsn,
            min=conf.pool_min,
            max=conf.pool_max,
            increment=conf.pool_increment,
            threaded=conf.pool_threaded,
        )
        return pool
    except Exception as e:
        print("Bağlantı havuzu oluşturulurken hata oluştu:", e)
        return None

# Connection pooling
connection_pool = create_connection_pool()

def verify_user(username, password):
    try:
        conn = connection_pool.acquire()
        cursor = conn.cursor()

        query = "SELECT username FROM users WHERE username = :username AND password = :password"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        cursor.close()
        connection_pool.release(conn)
        
        if result:
            return True
        else:
            return False
    except Exception as e:
        print("Veritabanına bağlanırken hata oluştu:", e)
        return False

def verify_db_connection():
    if connection_pool:
        print ("Bağlantı havuzu başarıyla oluşturuldu.")
    else:
        print ("Bağlantı havuzu oluşturulurken hata oluştu.")

# Send username to layout
@app.context_processor
def inject_user():
    username = session.get("username")
    return dict(username=username)

#logout
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

#error handler
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html") # veya başka bir sayfa


conn = connection_pool.acquire()
@app.route("/history", methods=["GET","POST"])
def history():
    if request.method =="POST":  
        user_input = request.form.get("user_input")
        sql = "SELECT * FROM employees WHERE department_id = :user_input ORDER BY hire_date DESC FETCH FIRST 10 ROWS ONLY"
        
        try:
            # Parametreleri kullanarak SQL sorgusunu çalıştırın
            data = pd.read_sql(sql, conn, params={"user_input": user_input})
            data_html = data.to_html(classes="table table-bordered table-striped table-hover", index=False)
            return render_template("history.html", data_html=data_html)
        
        except Exception as e:
            # Hata durumunu ele al
            return render_template("error.html", error_message=str(e))
    
    return render_template("history.html")






if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
    

