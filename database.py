# data -information
# database-resource

# 2 types
# relational database -
#    * stored as tables
#    *uses sql
#    *structured query language
#     *MySQL ,PostgreSQL,SQLite


# non relational database -

# *templates,records,document
# *NoSQL
# *Mongodb

import sqlite3

conn = sqlite3.connect("first.db")  # to establish a connection

cursor = conn.cursor()  # to interact with db

conn.close()
