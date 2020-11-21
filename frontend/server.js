const express = require("express");
const path = require("path");

const app = express();

app.use("/static", express.static(path.resolve(__dirname, "frontend", "static")));

app.get("/*", (req, res) => {
    res.sendFile(path.resolve(__dirname, "frontend", "index.html"));
});

//This is "listening" for the port number 5061 on my local device
//You may be able to access the webpage by typing in localhost:5061 into your browser as well
//This will eventually be "listening" for memphisbizapp.com once we figure out how to connect them
app.listen(process.env.PORT || 5061, () => console.log("Server is running..."));