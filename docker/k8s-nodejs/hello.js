var express = require('express')
var app = express()

app.get('/', function (req, res) {
    res.send("Hello Node JS~!!\n")
})

app.listen(8000, function () {
    console.log("8000 Port : Server Started~!!")
})
