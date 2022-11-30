/*작업 스케줄링
1. 매일 9시에 사용자에게 해당 요일에 수업이 있는지 알려준다.
2. 매일 오후 12시에 3일 안으로 듣거나 수행해야 하는 과제와 영상 강의가 있다면 알려준다.
*/

const fs = require("fs");
const Path = require('path');
const crontab = require("node-schedule");
const admin = require("firebase-admin");
const messaging = require("firebase-admin/messaging")
const serviceAccount = require("./filebaseAdmin.json");
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
})
const today = new Date();
const dailyArray = ['일', '월', '화', '수', '목', '금', '토', '일'];

//메시지 보내기
class CloudMessage {
  constructor(){
    this.message="";
  }
  setData(title, text, token) {
    this.message = {
      data: {
        title: title,
        body: text
      },
      token: token
    };
  }
  sendMessage() {
    messaging.getMessaging().send(this.message)
      .then((response) => {
        // Response is a message ID string.
        console.log('Successfully sent message:', response);
      })
      .catch((error) => {
        console.log('Error sending message:', error);
      });
  }
}


//작업 스케줄링

const dailyLessonJob = () => {
  let rule = new crontab.RecurrenceRule();
  rule.hour = 9;
  rule.minute = 0;
  rule.tz = 'Asia/Seoul'
  crontab.scheduleJob(rule, () => {
    dailyLesson();
  })
};



//과제 체크 작업 스케줄링
const homeworkCheckJob = () => {
  let rule = new crontab.RecurrenceRule();
  rule.hour = 9;
  rule.minute = 0;
  rule.tz = 'Asia/Seoul'
  crontab.scheduleJob(rule, () => {
    dailyLesson();
  })
}

//영상 강의 체크 작업 스케줄링


//출석 체크 작업 스케줄링


//실행 
const dailyLesson = () => {
  const path = Path.join(__dirname, '/userData');
  fs.readdir(path, { withFileTypes: true }, (err, files) => {
    if (err == null) {
      files.forEach((file) => {
        const filePath = Path.join(__dirname, `/userData/${file.name}`);
        fs.readFile(filePath, (err, data) => {
          if (err == null) {
            const jsonData = JSON.parse(data);
            var messageData = [];
            for (var i = 0; i < jsonData.classList.length; i++) {
              var nowData = jsonData.classList[i];
              if (nowData.day == dailyArray[today.getDay()]) messageData.push(`${nowData.startTime} ${nowData.name}`);
            }
            if (messageData.length != 0) {
              var message = new CloudMessage();
              message.setData("오늘의 강의", messageData.sort().join('\n'), jsonData.usertoken);
              message.sendMessage();
            }
          }
          else console.error(err);
        })
      });
    }
  });
};



function startSchedule() {
  dailyLessonJob();

}
