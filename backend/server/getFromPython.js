const spawn = require('child_process').spawn;

function getUserData(data,cb){
    try{
        const result = spawn('python3',['./crawl/ccCrawler.py',data.id,data.pw]);
        result.stdout.on('data',(res,err)=>{
            cb(res,err);
        });
    }
    catch(err){
        const result = spawn('python',['./crawl/ccCrawler.py',data.id,data.pw]);
        result.stdout.on('data',(res)=>{
            cb(res,err);
        });
    }
}
//     //mysql을 통해 정보 조회 (해당 요일에 맞는 수업을 찾고 해당 수업을 수강하는 사용자를 찾음)
//     //
//     result.stdout.on('data',(data)=>{
//         //결과값을 받음 
//         const resultData = data.toString(); 
//         //
        
module.exports= {getUserData};