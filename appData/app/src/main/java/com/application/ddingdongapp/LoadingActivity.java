package com.application.ddingdongapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;

import com.application.ddingdongapp.databinding.ActivityMainBinding;

import java.util.ArrayList;

public class LoadingActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        ActivityMainBinding binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(R.layout.activity_loading);
        new Handler().postDelayed(new Runnable() {
            public void run() {
                Intent intent = new Intent(LoadingActivity.this,LoginActivity.class);
                startActivity(intent);
            }
        }, 500);   //5 seconds
        String items[] = {"hello","hi","now"};



    }
}