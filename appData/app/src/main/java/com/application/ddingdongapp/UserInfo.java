package com.application.ddingdongapp;

import android.os.Parcel;
import android.os.Parcelable;

import com.google.gson.annotations.SerializedName;

import java.util.List;

public class UserInfo implements Parcelable {
    @SerializedName("stNID") //학번
    private final String sid;
    @SerializedName("stName") //사용자 이름
    private final String name;
    @SerializedName("stEmail")//사용자 이메일 주소
    private final String email;
    @SerializedName("stDept")//학과
    private final String dept;
    @SerializedName("classList") //강의목록
    private List<ClassData> classDataList;

    protected UserInfo(Parcel in) {
        sid = in.readString();
        name = in.readString();
        email = in.readString();
        dept = in.readString();
        classDataList = in.createTypedArrayList(ClassData.CREATOR);
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeString(sid);
        dest.writeString(name);
        dest.writeString(email);
        dest.writeString(dept);
        dest.writeTypedList(classDataList);
    }

    @Override
    public int describeContents() {
        return 0;
    }

    public static final Creator<UserInfo> CREATOR = new Creator<UserInfo>() {
        @Override
        public UserInfo createFromParcel(Parcel in) {
            return new UserInfo(in);
        }

        @Override
        public UserInfo[] newArray(int size) {
            return new UserInfo[size];
        }
    };

    public List<ClassData> getClassDataList() {
        return classDataList;
    }
    public void setClassDataList(List<ClassData> data){
        classDataList = data;
    }

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
