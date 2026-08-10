import psycopg2

connection = psycopg2.connect(
    host="localhost",
    database="FAULT_TOLERANT_AGENT",
    user="postgres",
    password="REMOVED_SECRET",
    port="5432"
)

print("Database Connected Successfully!")

connection.close()
print("Connection Closed!")