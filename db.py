from pymongo import MongoClient
import settings


client = MongoClient(settings.MONGO_LINK)
db = client[settings.MONGO_DB]


def get_or_create_user(db, effective_user, chat_id):
    user = db.users.find_one({"user_id": effective_user.id})
    if not user:
        user = {
            "user_id": effective_user.id,
            "first_name": effective_user.first_name,
            "last_name": effective_user.last_name,
            "username": effective_user.username,
            "chat_id": chat_id,
            "default_currency": 'EUR'
        }
        db.users.insert_one(user)
    return user


def sub_currency_db(db, user_data, symbol):
    sub = user_data.get('sub_currency')
    if not sub:
        db.users.update_one(
            {'_id': user_data['_id']},
            {'$set': {'sub_currency': symbol}})
        return True
    else:
        sub = sub.split('|')
        if symbol in sub:
            sub.remove(symbol)
            action = False
        else:
            sub.append(symbol)
            action = True
        sub = '|'.join(sub)
    if sub:
        db.users.update_one(
            {'_id': user_data['_id']},
            {'$set': {'sub_currency': sub}})
    else:
        db.users.update_one(
            {'_id': user_data['_id']},
            {'$unset': {'sub_currency': ''}})
    return action


def sub_crypto_db(db, user_data, symbol):
    sub = user_data.get('sub_crypto')
    if not sub:
        db.users.update_one(
            {'_id': user_data['_id']},
            {'$set': {'sub_crypto': symbol}})
        return True
    else:
        sub = sub.split('|')
        if symbol in sub:
            sub.remove(symbol)
            action = False
        else:
            sub.append(symbol)
            action = True
        sub = '|'.join(sub)
    if sub:
        db.users.update_one(
            {'_id': user_data['_id']},
            {'$set': {'sub_crypto': sub}})
    else:
        db.users.update_one(
            {'_id': user_data['_id']},
            {'$unset': {'sub_crypto': ''}})
    return action


def sub_stocks_db(db, user_data, symbol):
    sub = user_data.get('sub_stocks')
    if not sub:
        db.users.update_one(
            {'_id': user_data['_id']},
            {'$set': {'sub_stocks': symbol}})
        return True
    else:
        sub = sub.split('|')
        if symbol in sub:
            sub.remove(symbol)
            action = False
        else:
            sub.append(symbol)
            action = True
        sub = '|'.join(sub)
    if sub:
        db.users.update_one(
            {'_id': user_data['_id']},
            {'$set': {'sub_stocks': sub}})
    else:
        db.users.update_one(
            {'_id': user_data['_id']},
            {'$unset': {'sub_stocks': ''}})
    return action


def default_currency_db(db, user_data, symbol):
    db.users.update_one(
        {'_id': user_data['_id']},
        {'$set': {'default_currency': symbol}}
    )


def set_recent_rates(db, data):
    db.rates.insert_one(data)

def get_recent_rates(db):
    recent_rates = db.rates.aggregate([{'$sort': {'datetime': -1}}])
    recent_rates = next(recent_rates, None)
    return recent_rates
    