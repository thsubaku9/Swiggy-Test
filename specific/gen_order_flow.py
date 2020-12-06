import uuid
import random
import time
import math

order_stat = ["issued","delivering", "received"]
enum_order_stat = list(enumerate(order_stat))
payment_stat = ["failed","success"]
enum_payment_stat = list(enumerate(payment_stat))
coupons = ["Swiggy20","Swiggy40","FirstTime","Weekender","Birthday","Anniversary","First5"]
foodList = []

def load_food_list(fileLoc = "./food.txt"):
    file = open(fileLoc,'r')
    for line in file:
        Name,isVeg,price = line.split(",")
        isVeg = bool(int(isVeg))
        price = int(price)
        gst = gen_gst_rate(price)
        item = [Name,isVeg,price,gst]
        foodList.append(item)
    file.close()

def gen_uuid():
    return uuid.uuid4().int

def gen_coupon():
    isCoup = random.random()
    if(isCoup >0.3):
        loc = int(random.random() * len(coupons))
        return coupons[loc]
    else:
        return ""

def get_user_id(uid_list):
    index = (int)(random.random() * len(uid_list))
    return uid_list[index]

def time_triplet():
    start_t = 0
    assigned_t = 0
    delivered_t = 0

    base_val_time = 10e8 + 10e7 * 5
    current_time = time.time()

    start_t = base_val_time + (random.random() * (current_time - base_val_time))

    #probability wise drop certain orders
    if(random.random() < 0.05):
        return start_t,assigned_t,delivered_t
    else:
        #assuming at minimum 2 minutes and at most 20 minutes before it is assigned to a person
        assigned_t = start_t + (random.random() * 60 *(20 -2)) + (60*2)
        if(random.random() < 0.1):            
            return start_t,assigned_t,delivered_t
        else:
        #assuming at minimum 20 minutes and at most 60 minutes before it is assigned to a person
            delivered_t = assigned_t + (random.random() * 60 *(60 -20)) + (60*20)

    return start_t,assigned_t,delivered_t
            
def get_order_status(start_t,assigned_t,delivered_t):
    if (assigned_t == 0):
        return enum_order_stat[0][0]
    elif (delivered_t == 0):
        return enum_order_stat[1][0]
    else:
        return enum_order_stat[2][0]
    

def gen_gst_rate(order_price ,base = 0.05,cap = 0.20):
    gst_created = (random.random() * (cap - base)) + base
    return order_price * gst_created

def distance(startLat,startLong,endLat,endLong):
    #haversine formula - distance in km
    lat1 = math.radians(startLat)
    lat2 = math.radians(endLat)
    lon1 = math.radians(startLong)
    lon2 = math.radians(endLong)

    a = math.sin((lat2 - lat1)/2)**2 + math.cos(lat1)* math.cos(lat2) * math.sin((lon2 - lon1)/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371
    return ( c*r)

def gen_items():
    return 0

def create_order(userLatLong,userAddr,):    
    #userLatLong, userAddr, DeliveryCharge + Gst, couponCode, itemList, restaurantDetails, PaymentDetails
    _lat,_long = list(map(float,userLatLong.split(',')))
    orderMap = dict()
    orderMap["UserLatLong"] = userLatLong
    orderMap["userAddr"] = userAddr
    orderMap["DeliveryCharge"] = distance(''' Locations''') * 20
    orderMap["GST"]
    orderMap["CouponCode"] = gen_coupon()
    orderMap["ItemsList"],amt,gst = gen_items()
    orderMap["RestaurantDetails"] = gen_restaurantInfo()
    #amt needs to be recalculated
    orderMap["PaymentDetails"] = gen_payment(amt)

    return orderMap

def gen_restaurantInfo():
    #map of resta info
    return 0
    
def gen_payment(amount):
    #returns a map of data
    return 0

def create_pre_post(user_uuids,orders = 10):
    pre = []
    post = []
    user_uuids_keys = list(user_uuids.keys())
    for i in range(0,orders):
        pre_tab = []
        post_tab = []
        #pre data
        #order_id, user_id,place_time,order_stat,order_json
        order_id = gen_uuid()
        user_id = get_user_id(user_uuids_keys)
        start_t,assigned_t,delivered_t = time_triplet()
        order_status = get_order_status(start_t,assigned_t,delivered_t)
        
        #order_json        
        order_json = create_order(user_uuids[user_id][0],user_uuids[user_id][1])
        #create_order(userLatLong,userAddr,)
        pre_tab.append(order_id)
        pre_tab.append(user_id)
        pre_tab.append(start_t)
        pre_tab.append(order_stat)
        pre_tab.append(order_json)
        
        #post data
        #order_id, del_id,assigned_time,delivered_time
        del_id = gen_uuid()
        post_tab.append(order_id)
        post_tab.append(del_id)
        post_tab.append(assigned_t)
        post_tab.append(delivered_t)

        pre.append(pre_tab)
        post.append(post_tab)

    return pre,post
