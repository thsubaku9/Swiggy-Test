import uuid
import random

DEGREE = 90

#["user_id","user_name","user_address","user_lat_long"])

def load_names(file_path):
    names = []
    with open(file_path,'r') as file:
        for line in file:
            names.append(line.split("\n")[0])
    return names
    
def gen_uuid():
    return uuid.uuid4().int

def gen_addr():
    street = int(random.random() * 100)
    house =int(random.random() * 1000)
    return str.format("Street #{}, House #{}",street,house)

def gen_user_name(user_list):
    index = int(random.random() * len(user_list))
    return user_list[index]
    

#utilizing the DD format (range from (-90,90) for N and E)
def gen_lat_long():
    lat = (random.random() * 2 * DEGREE) - DEGREE
    long = (random.random() * 4 * DEGREE) - 2*DEGREE
    return str.format("{},{}",lat,long)

def create_user_table(lim,file_path = "./Names.csv"):
    names = load_names(file_path)
    res = []
    user_uuids = dict()
    for i in range(0,lim):        
        generated_uuid = gen_uuid()
        ll = gen_lat_long()
        name = gen_user_name(names)        
        addr = gen_addr()
        user_uuids[generated_uuid] = (ll,addr)
        user = {"user_id":generated_uuid, "user_name": name, "user_address": addr, "user_lat_lng": ll}
        res.append(user)
        
    return res,user_uuids
