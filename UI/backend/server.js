// server.js
const express = require("express");
const connectDB = require("./db");

const app = express();
app.use(express.json());

app.get("/", async (req, res) => {
  const db = await connectDB();
  const users = await db.collection("users").find().toArray();
  res.json(users);
});

const PORT = 5500;
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${5500}`);
});
