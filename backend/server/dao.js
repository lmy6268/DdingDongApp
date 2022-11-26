const mysql = require("mysql2/promise");
require('dotenv').config({ path: "./server/.env" });

//initialize
const { DB_HOST, DB_USER, DB_PASS } = process.env;
const pool = mysql.createPool({
	host: DB_HOST,
	user: DB_USER,
	password: DB_PASS,
	database: "DDINGDONGDB",
	port: '3306',
	connectionLimit: 10 //최대 10개의 connection 미리 생성
});

const addUserQuery = (data) => `INSERT INTO USERINFO VALUES('${data.id}','${data.name}','${data.sid}','${data.pw}','${data.dept}',${data.token})`;
const addClassQuery = (data) => `INSERT IGNORE INTO SUBJECT VALUES('${data.cId}','${data.cTitle}','${data.cTime}','${data.cDay}')`;
const addUserClassQuery = (data)=>`INSERT IGNORE INTO CLASS(SID,SUBID) VALUE('${data.sid}','${data.cId}')`;

const getConnection = async () => {
    try {
        const conn = await pool.getConnection();
        return conn;
    } catch (error) {
        console.error(`connection error : ${error.message}`);
        return null;
    }
};

const releaseConnection = async (conn) => {
    try {
        await conn.release();
    } catch (error) {
        console.error(`release error : ${error.message}`);
    }
};

//transaction 로직
const transaction = async (logic) => {
    let conn = null;
    try {
        conn = await getConnection();
        await conn.beginTransaction();
    	//connection만 넣어준다.
        const result = await logic(conn);
        await conn.commit();
        return result;
    } catch (err) {
        if (conn) {
            conn.rollback();
        }
        console.error(err);
        return null;
    } finally {
        if (conn) {
            releaseConnection(conn);
        }
    }
};

//사용자 등록
async function addUser(data, cb) {	
	const result =await transaction(
		(conn)=>{
			conn.query(addUserQuery(data));
			for(let i=0;i<data.classList.length;i++){
				conn.query(addClassQuery(data)); // 수업 정보 입력
				conn.query(addUserClassQuery({
					sid: data.sid,
					cId: data.classList[i].cId
				})); //사용자 수업 등록
			}});
	//오류 난 경우
	if(result == null){
		console.error("에러입니다.");
	}
	else console.log("정상적으로 처리되었습니다.");
}
//사용자 조회
function findUser(data, cb) {
	pool.getConnection((connErr, conn) => {
		if (connErr) console.error("에러입니다.");
		else conn.query(`SELECT * FROM USERINFO WHERE uId = '${data.id}' AND uPw='${data.pw}'`, (err, res) => {
			if (err || res.length == 0) {
				conn.release();
				cb(null, true);
			}
			else {
				conn.release();
				cb(res);
			}
		})
	})
}

//날짜에 대한 강의 목록 및 사용자 목록 조회(매일 강의 알림용)
function dailyAlertData() {

}

//날짜와 시간을 대입 -> 해당하는 강의 가져오기 (출석체크 알림용)
function findLesson() {

}

//각 사용자 별 강의 목록 가져오기 (동영상 강의 나 과제 알림용)
function findLessonList() {

}

module.exports = { addUser, findUser, dailyAlertData, findLesson, findLessonList };