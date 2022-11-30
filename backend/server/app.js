const express = require('express');
const app = express();
const port = 8000;
const cron = require('./jobScheduling');
const dataManager = require("./manageData");
const pythonJob = require('./getFromPython');

app.use(express.urlencoded({extended: false}));
//처음 로그인 시도
app.get('/',(req,res)=>{
	console.log("hello");
	res.send("hi");
})
app.post('/login', async (req, response) => {
	const id = req.body.uid;
	const pw = req.body.upw;
	const token = req.body.token;
	console.log(req.body);

	//학교 서버에서 정상 로그인 여부 확인
	pythonJob.getUserData(id,pw,(res,err)=>{ 
		if(err!=0){
			response.send(err);
			console.log("에러출력",err);
		}
		else {
			const resData = res.toString().slice(0, -1);
			const userJson =JSON.parse(resData);
			userJson.usertoken = token;
			userJson.userId = id;
			userJson.userPw =pw;
			dataManager.createUser(userJson,(res,err)=>{
				if(err == null) { //정상적인 출력을 받은 경우
					 response.status(200).send(resData);
					 console.log("정상 출력",resData);
				}
				else if (err == 1) { 
					console.log("정상 출력",resData);
					response.status(200).send(resData); }
				else {
					response.status(err);
					console.log("에러출력",err);
				}
			});
		}
	});
});

app.post('/signOut',(req,res)=>{
  //
})

//포트에서 응답 받음
app.listen(port, () => {
	console.log(`server is listening at localhost:${port}`);
});
