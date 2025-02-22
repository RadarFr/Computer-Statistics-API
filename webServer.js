const express = require("express");
const path = require("path");

const app = express();
const port = 8080;

// Serve static files (HTML, CSS, JS)
app.use(express.static(path.join(__dirname, "public")));

app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.listen(port, '0.0.0.0', () => {
    console.log(`Website Server running on http://45.90.175.151:${port}`);
});
