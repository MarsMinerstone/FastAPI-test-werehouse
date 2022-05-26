import motor.motor_asyncio

# Insert Your link of DateBase to ''
MONGODB_URL = 'link to your database'

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

# connection to db, Insert Your Name of DateBase to "Your_DB_Name"
database = client.Your_DB_Name