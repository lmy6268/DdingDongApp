package com.application.ddingdongapp.roomDataBase;

import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.Query;
import androidx.room.Update;

import java.util.List;
@Dao
public interface SubjectDao {
    @Query("SELECT * FROM subject")
    List<Subject> getAll();
    @Insert //과목 추가
    void insert(Subject... subjects);
    @Update
    void update(Subject subject);
    @Query("DELETE FROM subject")
    void deleteAll();
}
