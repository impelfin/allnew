const express = require('express')
const bodyParser = require('body-parser')
const mysql = require("sync-mysql")
const env = require("dotenv").config({ path: "../../.env" });

var connection = new mysql({
    host: process.env.host,
    user: process.env.user,
    password: process.env.password,
    database: process.env.database
});

const app = express()

app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }))
app.use(express.json())
app.use(express.urlencoded({ extended: true }))

app.get("/Hello", (req, res) => {
    res.send("Hello World")
})

// Select all rows from st_info table
app.get("/select", (req, res) => {
    const result = connection.query("SELECT * FROM st_info");
    console.log(result);
    res.writeHead(200);
    var template = `
  <!doctype html>
  <html>
  <head>
    <title>Result</title>
    <meta charset="utf-8">
  </head>
  <body>
   <table border="1" margin:auto; text-align:center;>
     <tr>
       <th>ST_ID</th>
       <th>NAME</th>
       <th>DEPT</th>
     </tr>
   `;
    for (var i = 0; i < result.length; i++) {
        template += `
     <tr>
       <th>${result[i]['ST_ID']}</th>
       <th>${result[i]['NAME']}</th>
       <th>${result[i]['DEPT']}</th>
     </tr>
    `
    }
    template += `
     </table>
  </body>
  </html>
 `;
    res.end(template);
})


// insert data into st_info table
app.get("/insert", (req, res) => {
    const { ST_ID, NAME, DEPT } = req.query
    const result = connection.query(
        "INSERT INTO st_info values (?, ?, ?)", [
        ST_ID,
        NAME,
        DEPT
    ]);

    res.redirect('/select');
})

// update row from st_info table
app.get("/update", (req, res) => {
    const { ST_ID, NAME, DEPT } = req.query
    const result = connection.query("UPDATE st_info SET NAME=?, DEPT=? WHERE ST_ID=?", [
        NAME,
        DEPT,
        ST_ID
    ]);

    res.redirect('/select');
})

// delete row from st_info table
app.get("/delete", (req, res) => {
    const ST_ID = req.query.ST_ID
    result = connection.query("DELETE FROM st_info WHERE ST_ID=?", [
        ST_ID
    ]);

    res.redirect('/select');
})

module.exports = app;
