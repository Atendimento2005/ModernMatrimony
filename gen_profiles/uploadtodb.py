from dotenv import load_dotenv
import mysql.connector
import os
import json
import time

with open('profiles.json', 'r') as f:
    data = json.load(f)['profiles']

load_dotenv()

db = mysql.connector.connect(
        host=os.getenv("HOST"),
        database=os.getenv("DATABASE"),
        user=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD"),
        ssl_ca=os.getenv("SSL_CERT")
    )

probs = [5,6,7,17,19]

for i in probs:
    user = tuple(data[i].values())[:-1]
    try:
        cur = db.cursor()
        cur.execute(f'''INSERT INTO Users(
                            name, 
                            age, 
                            sex, 
                            religion, 
                            caste, 
                            education, 
                            city, 
                            dating, 
                            marriage, 
                            interests, 
                            bio, 
                            email, 
                            ph, 
                            occupation, 
                            alma,
                            password
                )
                VALUES {user};''')
        db.commit()
        print(f"Uploaded {i}th user to DB successfully!")
        time.sleep(1)
    except Exception as e:
        print(e)
        print(f"Could not upload {i}th user to DB!")
# cur.execute('SELECT * FROM Users where id=3')
# print(cur.fetchone())
