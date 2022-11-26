/*작업 스케줄링
1. 매일 9시에 사용자에게 해당 요일에 수업이 있는지 알려준다.
2. 매일 오후 12시에 3일 안으로 듣거나 수행해야 하는 과제와 영상 강의가 있다면 알려준다.
*/

const crontab = require("node-cron");
const admin = require("firebase-admin");
const messaging = require("firebase-admin/messaging")
const serviceAccount = require("./filebaseAdmin.json");
admin.initializeApp({
    credential:admin.credential.cert(serviceAccount)
})
class CloudMessage{
    message;
    setData(title,text,token){
      this.message ={
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


// const msg = new CloudMessage();
// msg.setData("나이","aasdasd",'dv_Hw2D2SFew7tzGO8jl99:APA91bErbpoeWeCa5hiltiOGiNOA9T2_w3sXJOnT6saoo1iNz0UuzRYfN9YXxBjR3Vb3ZEGd-K4vGA8WVapNgQHXdbeQvw9L9gMBHLLIcPMaisViCJk8pRWAeaJvHutYmF1k9hwn5F8X');
// msg.sendMessage();
// msg.setData("asdsadas","ww2",'dv_Hw2D2SFew7tzGO8jl99:APA91bErbpoeWeCa5hiltiOGiNOA9T2_w3sXJOnT6saoo1iNz0UuzRYfN9YXxBjR3Vb3ZEGd-K4vGA8WVapNgQHXdbeQvw9L9gMBHLLIcPMaisViCJk8pRWAeaJvHutYmF1k9hwn5F8X');
// msg.sendMessage();







// function scheduling() {
    
//     crontab.schedule("0 0 9 * * *", () => console.log("hello"), {
//         scheduled: true,
//         timezone: "Asia/Seoul"
//     }); //매일 9시에 수행(시간 차이를 위한 1분 전 수행) (매일 수업 알림)

// }
// function dailyLesson(){
//     const result = spawn('python3',['./crawl/ccCrawler.py']);
//     //mysql을 통해 정보 조회 (해당 요일에 맞는 수업을 찾고 해당 수업을 수강하는 사용자를 찾음)
//     //
//     result.stdout.on('data',(data)=>{
//         //결과값을 받음 
//         const resultData = data.toString(); 
//         //
        
//     });
// }

// dailyLesson();
// module.exports = { scheduling };