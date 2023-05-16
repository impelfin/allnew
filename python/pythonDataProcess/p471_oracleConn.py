import cx_Oracle

# cx_Oracle.init_oracle_client(lib_dir="/Users/Lune/OracleXE/instantclient_19_8")
cx_Oracle.init_oracle_client(lib_dir="/usr/local/OracleXE/instantclient_19_19")

conn = None  # 접속 객체
cur = None  # 커서 객체

try:
    # 아이디/비번@hostname:port_number/sid
    loginfo = 'hr/1234@192.168.1.200:1521/xe'
    conn = cx_Oracle.connect(loginfo)
    print(type(conn))

    cur = conn.cursor()
    print(type(cur))

    sql = 'select power(2, 10) from dual'
    # sql = 'select * from USERTBL'
    cur.execute(sql)

    for item in cur:
        print(item)

except Exception as err:
    print(err)

finally:
    if cur != None:
        cur.close()

    if conn != None:
        conn.close()

print('finished')
