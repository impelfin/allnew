const https = require('https');

app.get('/', (req, res) => {
    res.send("Web Sever started...");
})

app.get('/hello', (req, res) => {
    res.send("Hello World - Moon");
})

let option = "http://192.168.1.158:8000/hello"
app.get("/rhello", function (req, res) {
    request(option, { json: true }, (err, result, body) => {
        if (err) { return console.log(err) }
        res.send(CircularJSON.stringify(body))
    })
})

const data = JSON.stringify({ todo: 'Buy the milk - Moon' })
app.get("/data", function (req, res) {
    res.send(data);
})

option = "http://192.168.1.158:8000/data"
app.get("/rdata", function (req, res) {
    request(option, { json: true }, (err, result, body) => {
        if (err) { return console.log(err) }
        res.send(CircularJSON.stringify(body))
    })
})

app.listen(8000, function () {
    console.log('8000 Port : Server Started....');
})