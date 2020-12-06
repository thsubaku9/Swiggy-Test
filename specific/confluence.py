import gen_user_table as gut
import gen_order_flow as gof

LIM = 10
ORDERS = 30

#First generate the user data
userTables,userID_map = create_user_table(LIM)

#Next create the order data
create_pre_post(userID_map,ORDERS)
