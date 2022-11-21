package com.application.ddingdongapp;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.TextView;

import com.application.ddingdongapp.databinding.ActivityMainBinding;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        ActivityMainBinding binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());
        binding.tvName.setText("이다함");
        binding.swStartTime.setText("");
        String items[] = {"아이템0", "아이템1", "아이템2", "아이템3", "아이템4"};

    }
}