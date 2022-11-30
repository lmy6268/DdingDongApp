const spawn = require('child_process').spawn;

//로그인 시 사용자 데이터를 불러오거나 갱신하는 함수 
function getUserData(id,pw,cb){
    try{
        const result = spawn('python3',['../crawl/ccCrawler.py',id,pw,1]);
        result.stdout.on('data',(res)=>{
            let rst = res.toString();
            var err =  rst.includes('ValueError') ? 400 : rst.includes('NameError') ?300: 0;
            cb(rst,err);
        });
    }
    catch(err){
        const result = spawn('python',['../crawl/ccCrawler.py',id,pw,1]);
        result.stdout.on('data',(res)=>{
            let rst = res.toString();
            var err =  rst.includes('ValueError') ? 400 : rst.includes('NameError') ?300: 0;
            cb(rst,err);
        });
    }
}

//
function getUserAtdc(userData,cb){
    try{

    }catch(err){

    }
}


module.exports= {getUserData};