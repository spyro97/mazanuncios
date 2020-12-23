from utils.db import fetch, execute

async def db_check_token_user(user):
    query = """select * from users where username = :username"""
    values = {"username": user.username}
    result = await fetch(query, True, values)
    if result is None:
        return None
    else:
        return result


async def db_check_jwt_username(username):
    query = """select * from users where username = :username"""
    values = {"username": username}

    result = await fetch(query, True, values)
    if result is None:
        return False
    else:
        return True

async def db_insert_user(user):
    try:
        user_query = """select * from users where username=:username"""
        user_values = {"username": user.username}
        user_data = await fetch(user_query, True, user_values)
        
        if user_data != None:
            return False
        
        query = """insert into users(username, password, email, role)
                values(:username, :password, :email, :role)"""
        values = dict(user)
        created_user = await execute(query, False, values)
        print(created_user)
        return True
    except:
        return False
    

async def retrieve_user(username):
    try:
        query = """select * from users where username=:username"""
        values = {"username": username}
        user = await fetch(query, True, values)
        return user
    except:
        return None
    
async def delete_users():
    try:
        query = """delete from users"""
        await fetch(query, False)
        return True
    except:
        return False