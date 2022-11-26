package com.application.ddingdongapp;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.room.Room;

import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Spinner;
import android.widget.TextView;

import com.application.ddingdongapp.databinding.ActivityMainBinding;
import com.application.ddingdongapp.roomDataBase.SubjectDao;
import com.application.ddingdongapp.roomDataBase.TotalDataBase;

public class MainActivity extends AppCompatActivity {

    String[] items = {"과목0", "과목1", "과목2", "과목3", "과목4"};


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        ActivityMainBinding binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        //데이터 베이스 생성
        TotalDataBase db = Room.databaseBuilder(getApplicationContext(),
                TotalDataBase.class, "DdingDongDb").build();
        SubjectDao subjectDao = db.subjectDao();


        //데이터 베이스에서 데이터 불러오기
        // 데이터 세팅


        ArrayAdapter<String> adapter = new ArrayAdapter<String>(
                this, android.R.layout.simple_spinner_item, items);
        adapter.setDropDownViewResource(
                android.R.layout.simple_spinner_dropdown_item);
        binding.spinner.setAdapter(adapter);


        binding.spinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                binding.swStartTime.setText(items[position]);
                binding.swVideo.setText(items[position]);
                binding.swSubmit.setText(items[position]);
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
                binding.swStartTime.setText("");
                binding.swSubmit.setText("");
                binding.swVideo.setText("");
            }
        });

    }


    @Override
    public void onBackPressed() {
        new AlertDialog.Builder(this)
                .setTitle("앱을 종료하시겠습니까?")
                .setPositiveButton("네", (dialog1, which) -> {
                    dialog1.dismiss();
                    ActivityCompat.finishAffinity(this);
                    System.exit(0);
                }).setNegativeButton("아니오", ((dialog1, which) ->
                {
                    dialog1.dismiss();
                })).show();
    }
}