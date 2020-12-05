import uuid
import random
DEGREE = 90

#["user_id","user_name","user_address","user_lat_long"])

def load_names(file_path):
    names = []
    with open(file_path) as file:
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
    global DEGREE
    lat = (random.random() * 2 * DEGREE) - DEGREE
    long = (random.random() * 2 * DEGREE) - DEGREE
    return str.format("{},{}",lat,long)

def create_user_table(lim,file_path = "F:/Swiggy Test/specific/Names.csv"):
    names = load_names(file_path)
    res = []
    user_uuids = set()
    for i in range(0,lim):
        a1 = []
        generated_uuid = gen_uuid()
        user_uuids.update({generated_uuid})
        a1.append(generated_uuid)
        a1.append(gen_user_name(names))
        a1.append(gen_addr())
        a1.append(gen_lat_long())
        res.append(a1)
    return res,user_uuids

