package com.application.ddingdongapp.roomDataBase;

import androidx.annotation.NonNull;
import androidx.room.ColumnInfo;
import androidx.room.Entity;
import androidx.room.PrimaryKey;

@Entity
public class Subject {
    @PrimaryKey @NonNull
    public String SubId; //과목 코드
    @ColumnInfo(name = "SubjectName")
    public String SubName; //과목 이름
    @ColumnInfo(name = "vidAlarm")
    public boolean vidAlarm; //영상 시청 알림 여부
    @ColumnInfo(name = "smAlarm")
    public boolean smAlarm; //제출 알림여부
}
