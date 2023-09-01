# Oracle database connection settings
db_user = "HR"
db_password = "HR"
db_dsn = "localhost:1521/TEST.tayyipaltunoz.com"  # örn: "localhost:1521/XE"

# Bağlantı havuzu (connection pool) ayarları
pool_min = 2  # Minimum bağlantı sayısı
pool_max = 5  # Maksimum bağlantı sayısı
pool_increment = 1  # Bağlantıların artırılma miktarı
pool_threaded = True  # Thread desteği etkinleştir