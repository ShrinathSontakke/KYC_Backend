from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb+srv://shrisontakke:shri123@pratyaksha-kyc.32uio.mongodb.net/?retryWrites=true&w=majority&appName=Pratyaksha-kyc')

# Select a database and collection
db = client.get_database('KYC')
collection = db['Users']
