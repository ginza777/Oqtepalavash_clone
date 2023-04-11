import sqlite3

conn = sqlite3.connect('example.db')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users (
	id integer PRIMARY KEY,
	telegram_id INTEGER, 
	first_name CHAR(56),
	last_name CHAR(56),
	phone_number CHAR (56)
);""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS mahsulotlar (
    id integer PRIMARY KEY , 
    name CHAR (100)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS mahsulot_tulari(
    id integer PRIMARY  KEY , 
    mah_id integer , 
    name CHAR (100), 
    image CHAR (100), 
    price INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS savatcha(
    id integer PRIMARY  KEY , 
    mah_id integer , 
    user_id integer , 
    soni INTEGER
)
""")


def user_check(telegram_id):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    cursor.execute(f"""
    SELECT * from users where telegram_id = {telegram_id}
    """)
    rows = cursor.fetchall()
    if len(rows) == 0:
        return False
    else:
        return True


def create_users(first_name, last_name, phone, telegram_id):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    INSERT INTO users (telegram_id,first_name, last_name, phone_number)
    VALUES({telegram_id}, '{first_name}', '{last_name}','{phone}');
    """)
    conn.commit()


def mahsulot_add(mahsulot_nomi):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO mahsulotlar (name)
        VALUES('{mahsulot_nomi}');
        """)
    conn.commit()


def mahsulotlar():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT * from mahsulotlar
        """)
    rows = cursor.fetchall()
    return rows


def mahsulot_turlari_dat(mah_id):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    cursor.execute(f"""
            SELECT * FROM mahsulot_tulari WHERE mah_id = {mah_id}
            """)
    rows = cursor.fetchall()
    return rows


def one_mahsulot_dat(mahsulot_id):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    cursor.execute(f"""
            SELECT id,name , price , image FROM mahsulot_tulari WHERE id = {mahsulot_id}
            """)
    rows = cursor.fetchall()
    return rows


def add_savatcha(mahsulot_id, user_id, soni):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO savatcha (mah_id, user_id, soni)
        VALUES({mahsulot_id}, {user_id}, {soni});
        """)
    conn.commit()


def ret_user_id(tel_id):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    cursor.execute(f"""
                SELECT id FROM users WHERE telegram_id = {tel_id}
                """)
    rows = cursor.fetchone()
    print(rows)
    return rows

def savatcha_user_data(user_id):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    cursor.execute(f"""
                    SELECT * FROM savatcha WHERE user_id = {user_id} and status = 'savatcha'
                    """)
    rows = cursor.fetchall()
    return rows
def savatcha_user_remove(user_id):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    cursor.execute(f"""
                        DELETE FROM savatcha WHERE user_id = {user_id} and status = 'savatcha'
                        """)
    conn.commit()