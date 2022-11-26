package com.application.ddingdongapp;

import com.google.gson.annotations.SerializedName;

public class UserInfo {
    @SerializedName("stNID") //학번
    private String sid;
    @SerializedName("stName") //사용자 이름
    private String name;
    @SerializedName("stEmail")//사용자 이메일 주소
    private String email;
    @SerializedName("stDept")//학과
    private String dept;
//    @SerializedName("classList") //강의목록

    public String getDept() {
        return dept;
    }

    public String getName() {
        return name;
    }

    public String getEmail() {
        return email;
    }

    public String getSid() {
        return sid;
    }
}
