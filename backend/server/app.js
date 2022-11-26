const express = require('express');
const app = express();
const port = 3000;
const cron = require('./jobScheduling')
const dao = require('./dao');
const pythonJob = require('./getFromPython');

app.use(express.urlencoded({extended: false}));
//처음 로그인 시도
app.post('/login', async (req, res) => {
	const id = req.body.uid;
	const pw = req.body.upw;
	const token = req.body.token;
	//데이터 베이스에서 정보 찾기 
	dao.findUser({
		id : id,
		pw:pw,
		token:token
	},(res,err)=>{
		if(err){
			//학교 서버에서 로그인하여 정보를 가져옴
			pythonJob.getUserData({
				id:id,
				pw:pw
			},(res,err)=>{
				//성공
				if(res){
					
				}
				//실패
				else {
					
				}
			});
		}
		else{
			
		}
	});

	// //서버에 정보가 있는 경우 -> 해당 정보를 사용자에게 알림
	// res.status(200).json(); //데이터를 json화 해서 전송
	res.status(200).json({
		stNID:"111",
		stName:"000",
		stEmail: "dd",
		stDept: "zx"
	});
	res.errored

});

//포트에서 응답 받음
app.listen(port, () => {
	console.log(`server is listening at localhost:${port}`);
});
