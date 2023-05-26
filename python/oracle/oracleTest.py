# oracleTest.py

import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir="/Users/Lune/Oracle/instantclient_19_8")

# Connect as user "hr" with password "welcome" to the "orclpdb1" service running on this computer.
connection = cx_Oracle.connect(user="hr", password="1234",
                               dsn="localhost/xe")

cursor = connection.cursor()
cursor.execute("""
        SELECT first_name, last_name
        FROM employees
        WHERE department_id = :did AND employee_id > :eid""",
        did = 50,
        eid = 190)
for fname, lname in cursor:
    print("Values:", fname, lname)