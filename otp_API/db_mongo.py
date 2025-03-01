from pymongo import MongoClient

def get_otp_collection():
    client = MongoClient('mongodb+srv://shrisontakke:shri123@pratyaksha-kyc.32uio.mongodb.net/?retryWrites=true&w=majority&appName=Pratyaksha-kyc')
    db = client["KYC"]  # Replace with your database name
    return db["otp_collection"]  # Replace with your collection name
