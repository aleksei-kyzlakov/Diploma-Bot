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


def subscribe_user(db, user_data):
    if not user_data.get('subscribed'):
        db.users.update_one(
            {'_id': user_data['_id']},
            {'$set': {'subscribed': True}}
        )


def unsubscribe_user(db, user_data):
    db.users.update_one(
        {'_id': user_data['_id']},
        {'$set': {'subscribed': False}}
    )


def get_subscribed(db):
    return db.users.find({"subscribed": True})


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
    