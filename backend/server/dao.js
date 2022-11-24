const mysql = require("mysql2/promise");
const db = async () => {
    try {
        // db connection
        let connection = await mysql.createConnection({
            host: "localhost",
            user: "root",
            password: "1q2w3e4r!@",
            database: "sample",
        });
    }
    catch (err) {

    }
};
