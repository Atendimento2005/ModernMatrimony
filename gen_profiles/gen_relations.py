from dotenv import load_dotenv
import mysql.connector
import os
import json
import time

load_dotenv()

db = mysql.connector.connect(
        host=os.getenv("HOST"),
        database=os.getenv("DATABASE"),
        user=os.getenv("USER_NAME"),
        password=os.getenv("PASSWORD"),
        ssl_ca=os.getenv("SSL_CERT")
    )

cur = db.cursor()
cur.execute('SELECT * FROM Users')
data = cur.fetchall()
'''
id,
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
'''


for User in data:
    cur = db.cursor()
    cur.execute(f'SELECT * FROM Users WHERE (age > {User[2]-6} AND age < {User[2]+6}) AND (dating = {User[8]} OR marriage = {User[9]}) AND id != {User[0]};')
    relUsers = cur.fetchall()
    cur = db.cursor()
    cur.execute(f'SELECT first_id, second_id FROM Relations WHERE first_id = {User[0]} OR second_id = {User[0]};')
    relatedIDs = [x[0] if x[1] == User[0] else x[1] for x in cur.fetchall()]
    queries = []
    for relUser in relUsers:
        if relUser[0] in relatedIDs: continue
        score = 0
        score += (6 - abs(relUser[2] - User[2]))*(10/6)
        for i in range(4, 14):
            if i == 10:
                for j in range(15):
                    if User[10][i] == relUser[10][i]:
                        score += 1
            elif i not in [8, 9, 10, 11, 12, 13]:
                score += 3 if User[i].lower() == relUser[i].lower() else 0
        queries.append((User[0], relUser[0], score))
    if len(queries):
        cur = db.cursor()
        cur.execute(f'INSERT INTO Relations(first_id, second_id, score) VALUES {str(queries)[1:-1]};')
        db.commit()

