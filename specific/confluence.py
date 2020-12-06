import gen_user_table as gut
import gen_order_flow as gof
import json

USERS = 10
ORDERS = int(10e2)
RESTAURANTS = 400

print("GENERATING 1000 USERS AND 10K ORDERS TAKES 200ISH MBS\n")
print("Your patience is appreciated, in case you're utilizing a low RAM device, please use the load_table function to load the json back into python\n")

def save_table(user_data,filename):
    data = json.JSONEncoder().encode(user_data)
    with open(filename,"w+") as file:
        file.write(data)

def load_table(filename):
    with open(filename,"r") as file:
        data = json.JSONDecoder().decode(file.read())
    return data
    
#First generate the user data
userTables,userID_map = gut.create_user_table(USERS)

print("user values generated\n")
#load ItemList
gof.load_food_list()

#generate restaurants
gof.create_restaurant_list(RESTAURANTS)
print("pseudo restaurants created\n")

#Next create the order data
preTables,postTables = gof.create_pre_post(userID_map,ORDERS)
print("pre and post flow tables created !\n")
save_table(userTables,"user_table.json")
save_table(preTables,"pre_table.json")
save_table(postTables,"post_table.json")

