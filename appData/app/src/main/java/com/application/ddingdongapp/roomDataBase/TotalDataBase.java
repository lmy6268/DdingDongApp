package com.application.ddingdongapp.roomDataBase;

import androidx.room.Database;
import androidx.room.RoomDatabase;

@Database(entities = {Subject.class},version = 1)
public abstract class TotalDataBase extends RoomDatabase {
    public abstract SubjectDao subjectDao();
}
