var oracledb = require('oracledb');
var dbConfig = require('./dbConfig');
// Express 기본 모듈 불러오기
var express = require('express')
    , http = require('http')
    , path = require('path');

// 익스프레스 객체 생성
var app = express();

// 기본 속성 설정
app.set('port', process.env.PORT || 3000);

// body-parser
var bodyParser = require('body-parser');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Oracle Auto Commit 설정
oracledb.autoCommit = true;

app.get('/', (req, res) => {
    res.send('Web Server Started~!!')
});


// 데이터 조회 처리
app.get('/dbTestSelect', function (request, response) {
    oracledb.getConnection({
        user: dbConfig.user,
        password: dbConfig.password,
        connectString: dbConfig.connectString
    },
        function (err, connection) {
            if (err) {
                console.error(err.message);
                return;
            }

            let query =
                'select * ' +
                '   from usertbl';

            connection.execute(query, [], function (err, result) {
                if (err) {
                    console.error(err.message);
                    doRelease(connection);
                    return;
                }
                console.log(result.rows);                   // 데이터
                doRelease(connection, result.rows);         // Connection 해제
            });
        });

    // DB 연결 해제
    function doRelease(connection, rowList) {
        connection.release(function (err) {
            if (err) {
                console.error(err.message);
            }

            // DB종료까지 모두 완료되었을 시 응답 데이터 반환
            console.log('list size: ' + rowList.length);

            response.send(rowList);
        });
    }
});

// 데이터 입력 처리
app.get('/dbTestInsert', function (request, response) {

    oracledb.getConnection({
        user: dbConfig.user,
        password: dbConfig.password,
        connectString: dbConfig.connectString
    },
        function (err, connection) {
            if (err) {
                console.error(err.message);
                return;
            }

            // PrepareStatement 구조
            let query =
                'INSERT INTO EMP( EMPNO ,ENAME, JOB, MGR, HIREDATE, SAL, COMM, DEPTNO) ' +
                'VALUES( :EMPNO ,:ENAME, :JOB, :MGR, SYSDATE, :SAL, :COMM, :DEPTNO )';

            let binddata = [
                Number(request.body.empno),
                request.body.ename,
                request.body.job,
                request.body.mgr,
                Number(request.body.sal),
                Number(request.body.comm),
                Number(request.body.deptno)
            ];

            connection.execute(query, binddata, function (err, result) {
                if (err) {
                    console.error(err.message);
                    doRelease(connection);
                    return;
                }
                console.log('Row Insert: ' + result.rowsAffected);

                doRelease(connection, result.rowsAffected);         // Connection 해제
            });
        });

    // DB 연결 해제
    function doRelease(connection, result) {
        connection.release(function (err) {
            if (err) {
                console.error(err.message);
            }

            // DB종료까지 모두 완료되었을 시 응답 데이터 반환
            response.send('' + result);
        });
    }
});

// 등록되지 않은 패스에 대해 페이지 오류 응답
app.all('*', function (req, res) {
    res.status(404).send('<h1>ERROR - 페이지를 찾을 수 없습니다.</h1>');
});

// Express 서버 시작
app.listen(app.get('port'), function () {
    console.log('Express server listening on port ' + app.get('port'));
});