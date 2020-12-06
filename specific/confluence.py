import gen_user_table as gut
import gen_order_flow as gof

LIM = 20
ORDERS = 2

#First generate the user data
userTables,userID_map = gut.create_user_table(LIM)

#load ItemList
gof.load_food_list()
#Next create the order data
#preTables,postTables = gof.create_pre_post(userID_map,ORDERS)
