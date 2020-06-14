const path = require('path');

// const dotenv = require("dotenv");
// dotenv.config();

const express = require("express");
const app = express();
const port = 3001;

const cors = require("cors");
app.use(cors());

const bodyParser = require("body-parser");
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.use(express.static(__dirname));

app.get('/', function (req, res) {
    res.sendFile(path.resolve('client/views/index.html'))
})

const server = app.listen(port, () => {
  console.log(`running on localhost: ${port}`);
});

app.get('/success', function (req, res) {
    // res.sendFile(path.resolve('client/views/success.html'))
    res.sendFile(path.resolve('../../templates/success.html'))
})



