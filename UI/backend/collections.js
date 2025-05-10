const connectDB = require("./db");

let usersCollection;
let resetTokensCollection;

(async () => {
  const db = await connectDB();
  usersCollection = db.collection("users");
  resetTokensCollection = db.collection("password_reset_tokens");
})();

module.exports = { usersCollection, resetTokensCollection };