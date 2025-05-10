// server.js
const express = require("express");
const { usersCollection, resetTokensCollection } = require("./collections");

const app = express();
app.use(express.json());

app.get("/", async (req, res) => {
  const users = await usersCollection.find().toArray();
  res.json(users);
});

const PORT = 5500;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
