import uuid
import random
import time

def gen_uuid():
    return uuid.uuid4().int


def create_pre_post(user_uuid_set):
    pre = []
    post = []
