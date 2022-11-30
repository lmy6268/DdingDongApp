package com.application.ddingdongapp;

import android.os.Parcel;
import android.os.Parcelable;

import com.google.gson.annotations.SerializedName;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class ClassData implements Parcelable {
    @SerializedName("name") //강의명
    private String name;
    @SerializedName("link") //강의 링크
    private String link;
    @SerializedName("day")//요일
    private String day;
    @SerializedName("startTime")//시작시간
    private String startTime;
    private ArrayList<Boolean> alarm = new ArrayList<>(Arrays.asList(true,true,true));


    protected ClassData(Parcel in) {
        name = in.readString();
        link = in.readString();
        day = in.readString();
        startTime = in.readString();
    }

    public static final Creator<ClassData> CREATOR = new Creator<ClassData>() {
        @Override
        public ClassData createFromParcel(Parcel in) {
            return new ClassData(in);
        }

        @Override
        public ClassData[] newArray(int size) {
            return new ClassData[size];
        }
    };

    public String getName() {
        return name;
    }

    public String getDay() {
        return day;
    }

    public void setAlarm(ArrayList<Boolean> alarm) {
        this.alarm = alarm;
    }

    public void setAlarmByType(int position,boolean bool){
        this.alarm.set(position,bool);
    }
    public List<Boolean> getAlarm() {
        return alarm;
    }

    public String getLink() {
        return link;
    }

    public String getStartTime() {
        return startTime;
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeString(name);
        dest.writeString(link);
        dest.writeString(day);
        dest.writeString(startTime);
    }
}
