import os
import sys
import json
import uuid

#os.chdir("F:\Swiggy Test\schema")

def load_schema(path = "./schema"):
    #acquire path to schema
    curr_path = os.getcwd()
    os.chdir(path)

    #files = 

    #load the schemas
    schema_map = {}
    
    #switch back to original path
    os.chdir(curr_path)

def load_rules(path = "./rules"):
    curr_path = os.getcwd()

    os.chdir(curr_path)

#have to perform schema cohesiveness given a schema map

