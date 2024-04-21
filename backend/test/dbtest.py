import pymysql

try:
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='sarthak123',
                                 db='investedge',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print("Connection successful!")
except Exception as e:
    print(f"Connection error: {e}")
finally:
    if connection:
        connection.close()
