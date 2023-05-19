const express = require('express');
const bodyParser = require('body-parser');
const XMLHttpRequest = require('xhr2');

const app = express()

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get('/hello', (req, res) => {
    res.send('hello world~!!')
})

app.get('/getPostData', (req, res) => {
    const xhr = new XMLHttpRequest();

    xhr.open("GET", "http://localhost:5000/users");
    xhr.setRequestHeader("content-type", "application/json");
    xhr.send();

    xhr.onload = () => {
        if (xhr.status === 200) {
            const res = JSON.parse(xhr.response);
            console.log(res);
        } else {
            console.log(xhr.status, xhr.statusText);
        }
        res.send(xhr.response)
    }
})

app.get('/PostData', (req, res) => {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:5000/users");
    xhr.setRequestHeader("content-type", "application/json; charset=UTF-8")

    const data = { title: 'JavaScript', author: 'John Doe' };
    xhr.send(JSON.stringify(data));

    xhr.onload = () => {
        if (xhr.status === 201) {
            const res = JSON.parse(xhr.response);
            console.log(res);
        } else {
            console.log(xhr.status, xhr.statusText);
        }
        res.send(xhr.response)
    }
})

app.get('/addData', (req, res) => {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:5000/users");
    xhr.setRequestHeader("content-type", "application/json; charset=UTF-8");
    const data = { id: 2 };
    xhr.send(JSON.stringify(data));

    xhr.onload = () => {
        if (xhr.status === 200) {
            const res = JSON.parse(xhr.response);
            console.log(res);
        } else {
            console.log(xhr.status, xhr.statusText);
        }
        res.send(xhr.response)
    }
})

app.get('/putData', (req, res) => {
    const xhr = new XMLHttpRequest();
    xhr.open("PUT", "http://localhost:5000/users/2");
    xhr.setRequestHeader("content-type", "application/json; charset=UTF-8");
    const data = { title: "HTML", author: "Heung Min SON" };
    xhr.send(JSON.stringify(data));

    xhr.onload = () => {
        if (xhr.status === 200) {
            const res = JSON.parse(xhr.response);
            console.log(res);
        } else {
            console.log(xhr.status, xhr.statusText);
        }
        res.send(xhr.response)
    }
})

app.get('/deleteData', (req, res) => {
    const xhr = new XMLHttpRequest();

    xhr.open("DELETE", "http://localhost:5000/users/2");
    xhr.getResponseHeader("content-type", "application/json; charset=UTF-8")
    xhr.send();

    xhr.onload = () => {
        if (xhr.status === 200) {
            const res = JSON.parse(xhr.response);
            console.log(res);
        } else {
            console.log(xhr.status, xhr.statusText);
        }
        res.send(xhr.response)
    }
})

module.exports = app;
