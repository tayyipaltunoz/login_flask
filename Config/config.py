# Oracle database connection settings
db_user = "HR"
db_password = "HR"
db_dsn = "localhost:1521/TEST.tayyipaltunoz.com"  # örn: "localhost:1521/XE"

# Bağlantı havuzu (connection pool) ayarları
pool_min = 2  # Minimum bağlantı sayısı
pool_max = 5  # Maksimum bağlantı sayısı
pool_increment = 1  # Bağlantıların artırılma miktarı
pool_threaded = True  # Thread desteği etkinleştir

#Search API
# response = requests.get('https://fakestoreapi.com/products/' + query)
search_api="https://dummyjson.com/products/" 

#Users query
user_sql="SELECT username FROM users WHERE username = :username AND password = :password"

#History query
history_sql="SELECT * FROM employees WHERE department_id = :user_input ORDER BY hire_date DESC FETCH FIRST 10 ROWS ONLY"