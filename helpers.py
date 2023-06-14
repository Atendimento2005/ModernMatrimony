'''
Get user by ID
Returns dict with keys as props

db => mysql.connector DB element
id => id of User to fetch
props => tuple of properties to fetch for given user
'''
def fetchUserByID(db, id :int, props : tuple):
    cur = db.cursor()
    cur.execute(f' SELECT {", ".join(props)} FROM Users WHERE id = {id};')
    user_data = cur.fetchone()

    return dict(zip(props, user_data))

def fetchReccomendations(db, id :int):
    cur = db.cursor()
    cur.execute(f'SELECT first_id, second_id, score FROM Relations WHERE first_id = {id} OR second_id = {id};')
    
    relations = {}
    for x in cur.fetchall():
        relID = x[0] if x[1] == id else x[1]
        relations[relID] = x[2]


    query = 'SELECT id, name, age, bio, interests FROM Users WHERE'
    for relID in relations.keys():
        query += f' id = {relID} OR'
    query = query[:-2]
    query += ';'
    cur.execute(query)
    reccs = cur.fetchall()
    
    reccomendedUsers = []
    for recc in reccs:
        User = {'id': recc[0],
                'name': recc[1],
                'age': recc[2],
                'bio': recc[3],
                'interests': recc[4],
                'score': relations[recc[0]]}
        reccomendedUsers.append(User)
    reccomendedUsers.sort(key = lambda x: x['score'])
    return reccomendedUsers