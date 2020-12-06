import uuid
import random
import time
import math

DEGREE = 90
order_stat = ["issued","delivering", "received"]
enum_order_stat = list(enumerate(order_stat))
payment_type = ["credit card", "debit card", "cash on delivery", "UPI", "gift coupon"]
payment_stat = ["failed","success"]
enum_payment_stat = list(enumerate(payment_stat))
coupons = ["Swiggy20","Swiggy40","FirstTime","Weekender","Birthday","Anniversary","First5"]
foodList = []
restaurantList = []

def load_food_list(fileLoc = "./food.txt"):
    file = open(fileLoc,'r')
    for line in file:
        Name,isVeg,price = line.split(",")
        isVeg = bool(int(isVeg))
        price = int(price)
        gst = gen_gst_rate(price)
        item = {"name":Name, "isVeg":isVeg, "price":price, "GST":gst}
        foodList.append(item)
    file.close()

def gen_lat_long():
    lat = (random.random() * 2 * DEGREE) - DEGREE
    long = (random.random() * 4 * DEGREE) - 2*DEGREE
    return str.format("{},{}",lat,long)

def create_restaurant_list(net):    
    for i in range(0,net):        
        num = int(random.random() * 10e5)
        shop = int(random.random() * 10e3)
        avenue = int(random.random() * 10e3)
        ll = gen_lat_long()
        res = {"name": str.format("restaurant #{}",num), "addr" : str.format("Shop {} - Avenue {}",shop,avenue), "LatLong": ll}
        restaurantList.append(res)
        
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
    selectedItems = []
    total_items = int(random.random() * len(foodList)) + 1
    for i in range(0,total_items):
        index = int(random.random() * len(foodList))
        selectedItems.append(foodList[index])
    return selectedItems

def create_order(userLatLong,userAddr,deliveryPricePerKm = 10):
    #userLatLong, userAddr, DeliveryCharge + Gst, couponCode, itemList, restaurantDetails, PaymentDetails
    _lat,_long = list(map(float,userLatLong.split(',')))
    orderMap = dict()
    _itemlist = gen_items()
    netGST = 0
    netAmt = 0
    for i in range(0,len(_itemlist)):
        netGST += _itemlist[i]["GST"]
        netAmt += _itemlist[i]["price"]
        
    restaurant = gen_restaurantInfo()
    _latres,_longres = list(map(float,restaurant["LatLong"].split(',')))
    
    orderMap["UserLatLong"] = userLatLong
    orderMap["userAddr"] = userAddr
    orderMap["DeliveryCharge"] = distance(_lat,_long,_latres,_longres) * deliveryPricePerKm
    orderMap["GST"] = netGST
    orderMap["CouponCode"] = gen_coupon()
    orderMap["ItemsList"] = gen_items()
    orderMap["RestaurantDetails"] = restaurant
    #amt needs to be recalculated
    orderMap["PaymentDetails"] = gen_payment(netAmt)

    return orderMap

def gen_restaurantInfo():
    index = (int)(random.random() * len(restaurantList))
    return restaurantList[index]

def transact_status():
    if (random.random() <0.01):
        return enum_payment_stat[0][0]
    else:
        return enum_payment_stat[1][0]
    
def gen_payment(amount):
    PaymentMethod = payment_type[int(random.random() * len(payment_type))]
    PaymentTransactionStatus = transact_status()
    TransactionID = gen_uuid()
    PaymentAmount = amount
    return {"PaymentMethod" : PaymentMethod, "PaymentTransactionStatus" : PaymentTransactionStatus, "TransactionID": TransactionID, "PaymentAmount": PaymentAmount }

def create_pre_post(user_uuids,orders = 10):
    pre = []
    post = []
    user_uuids_keys = list(user_uuids.keys())
    for i in range(0,orders):
        #pre data
        #order_id, user_id,place_time,order_stat,order_json
        order_id = gen_uuid()
        user_id = get_user_id(user_uuids_keys)
        start_t,assigned_t,delivered_t = time_triplet()
        current_order_status = get_order_status(start_t,assigned_t,delivered_t)
        
        #order_json        
        order_json = create_order(user_uuids[user_id][0],user_uuids[user_id][1])
        preValue = {"order_id": order_id, "user_id": user_id, "order_placed_at": start_t, "order_status": current_order_status,"order_json": order_json}
        
        #post data
        #order_id, del_id,assigned_time,delivered_time
        de_id = gen_uuid()
        postValue = {"order_id": order_id, "de_id": de_id, "de_assigned_at": assigned_t,"order_delivered_at": delivered_t}

        pre.append(preValue)
        post.append(postValue)

    return pre,post
