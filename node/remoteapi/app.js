const express = require('express');
const morgan = require('morgan'); // 디버깅을 위해서 사용한다
const path = require('path');
const bodyParser = require('body-parser') // get , post request 꺼내 올려면 필요한것이다.
const cookieParser = require('cookie-parser');
const router = express.Router();

const app = express();

app.set('port', process.env.PORT || 8000);
app.use(morgan('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

var main = require('./routes/main.js');
app.use('/', main);

app.listen(app.get('port'), () => {
    console.log('8000 Port : Server Started...')
});