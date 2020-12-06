import gen_user_table as gut
import gen_order_flow as gof
import json

LIM = 20
ORDERS = 2
RESTAURANTS = 40

def save_table(user_data,filename):
    data = json.JSONEncoder().encode(user_data)
    with open(filename,"w+") as file:
        file.write(data)

def load_table(filename):
    with open(filename,"r") as file:
        data = json.JSONDecoder().decode(file.read())
    return data
    
#First generate the user data
userTables,userID_map = gut.create_user_table(LIM)

#load ItemList
gof.load_food_list()

#generate restaurants
gof.create_restaurant_list(RESTAURANTS)

#Next create the order data
preTables,postTables = gof.create_pre_post(userID_map,ORDERS)

save_table(userTables,"user_table.json")
save_table(preTables,"pre_table.json")
save_table(postTables,"post_table.json")
