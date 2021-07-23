from api_requests import request_all

from db import db

from telegram.error import BadRequest

def hourly_db_repopulation(db):
    set_recent_rates(db, request_all())