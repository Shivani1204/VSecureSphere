// db.js
const { MongoClient } = require("mongodb");

const uri = "mongodb://localhost:27017"; // Default MongoDB URI
const client = new MongoClient(uri);

async function connectDB() {
  try {
    await client.connect();
    console.log("✅ Connected to MongoDB");
    const db = client.db("vsecuresphere"); // you can rename the DB as needed
    return db;
  } catch (error) {
    console.error("❌ MongoDB connection failed:", error);
  }
}

module.exports = connectDB;
