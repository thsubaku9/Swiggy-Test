var userFile = "./user_table.json"
var preFile =  "./pre_table.json"
var postFile = "./post_table.json"

val users = spark.read.option("multiLine", true).json(userFile)
val pre_table = spark.read.option("multiLine", true).json(preFile)
val post_table = spark.read.option("multiLine", true).json(postFile)

print("Displaying Schema View")
users.printSchema()
pre_table.printSchema()
post_table.printSchema()


print("Joining data frames")
val flow_table = pre_table.join(post_table,"order_id")
val order_fact = flow_table.join(users,"user_id")
print("Order Fact has been created")

order_fact.coalesce(1).write.format("json").save("./result/order_json.json")