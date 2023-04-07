/*  DB Info */
module.exports =
{
    user: process.env.NODE_ORACLEDB_USER || "hr",
    password: process.env.NODE_ORACLEDB_PASSWOR || "1234",
    connectString: process.env.NODE_ORACLEDB_CONNECTIONSTRING || "192.168.1.200:1521/xe"
}