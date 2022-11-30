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
import android.widget.Toast;

import com.application.ddingdongapp.databinding.ActivityMainBinding;
import com.application.ddingdongapp.roomDataBase.SubjectDao;
import com.application.ddingdongapp.roomDataBase.TotalDataBase;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {
    ActivityMainBinding binding;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());
        UserInfo userInfo = getIntent().getParcelableExtra("userInfo"); //로그인 한 사용자 정보
        setUI(userInfo);
    }

    private void setUI(UserInfo userInfo){
        ArrayList<String> classNameList = new ArrayList<>();
        ArrayList<ClassData> dataList = new ArrayList(userInfo.getClassDataList());
        for(ClassData a : userInfo.getClassDataList()){
            classNameList.add(a.getName());
        }
        ArrayAdapter<String> adapter = new ArrayAdapter(
                this, android.R.layout.simple_spinner_item, classNameList); //
        adapter.setDropDownViewResource(
                android.R.layout.simple_spinner_dropdown_item);
        binding.spinner.setAdapter(adapter);
        binding.tvName.setText(userInfo.getName());
        binding.tvDept.setText(userInfo.getDept());
        binding.btnLogout.setOnClickListener(v->{
            new AlertDialog.Builder(this)
                    .setTitle("로그아웃 하시겠습니까?")
                    .setPositiveButton("네", (dialog1, which) -> {
                        dialog1.dismiss();
                        Intent intent = new Intent(MainActivity.this,LoginActivity.class);
                        startActivity(intent);
                        Toast.makeText(MainActivity.this,"정상적으로 로그아웃 되었습니다.",Toast.LENGTH_SHORT).show();
                        finish();
                    }).setNegativeButton("아니오", ((dialog1, which) ->
                    {
                        dialog1.dismiss();
                    })).show();
        });



        binding.spinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            String title;
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                title= classNameList.get(position);
                binding.swStartTime.setText(String.format("%s 수업 시작 시간 알림",title));
                binding.swStartTime.setChecked(dataList.get(position).getAlarm().get(1));
                binding.swVideo.setText(String.format("%s 영상 강의 알림", title));
                binding.swVideo.setChecked(dataList.get(position).getAlarm().get(1));
                binding.swSubmit.setText(String.format("%s 과제 제출 알림", title));
                binding.swSubmit.setChecked(dataList.get(position).getAlarm().get(2));
                binding.swSubmit.setOnCheckedChangeListener((buttonView, isChecked) -> {
                    dataList.get(position).setAlarmByType(position,isChecked);
                });
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
                title = "";
                binding.swStartTime.setText(String.format("%s 수업 시작 시간 알림",title));
                binding.swVideo.setText(String.format("%s 영상 강의 알림", title));
                binding.swSubmit.setText(String.format("%s 과제 제출 알림", title));
            }
        });

    }
    @Override
    public void onBackPressed() {
        close();
    }
    private void close(){
        new AlertDialog.Builder(this)
                .setTitle("앱을 종료하시겠습니까?")
                .setPositiveButton("네", (dialog1, which) -> {
                    dialog1.dismiss();
                    finish();
                }).setNegativeButton("아니오", ((dialog1, which) ->
                {
                    dialog1.dismiss();
                })).show();
    }
}