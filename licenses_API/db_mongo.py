from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb+srv://shrisontakke:shri123@pratyaksha-kyc.32uio.mongodb.net/?retryWrites=true&w=majority&appName=Pratyaksha-kyc')

# Select the database
db = client.get_database('KYC')

# Define collections for Licenses and License Assignments
licenses_collection = db['Licenses']
license_assignments_collection = db['LicenseAssignments']
