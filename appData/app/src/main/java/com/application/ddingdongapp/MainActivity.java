package com.application.ddingdongapp;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Spinner;
import android.widget.TextView;

import com.application.ddingdongapp.databinding.ActivityMainBinding;

public class MainActivity extends AppCompatActivity {

    TextView textView1;
    TextView textView2;
    TextView textView3;
    String[] items = {"과목0", "과목1", "과목2", "과목3", "과목4"};

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        ActivityMainBinding binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());
        setContentView(R.layout.activity_main);

        textView1 = findViewById(R.id.swStartTime);
        textView2 = findViewById(R.id.swSubmit);
        textView3 = findViewById(R.id.swVideo);
        Spinner spinner = findViewById(R.id.spinner);
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(
                this, android.R.layout.simple_spinner_item, items);
        adapter.setDropDownViewResource(
                android.R.layout.simple_spinner_dropdown_item);
        spinner.setAdapter(adapter);
        spinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                textView1.setText(items[position]);
                textView2.setText(items[position]);
                textView3.setText(items[position]);}
            @Override
            public void onNothingSelected(AdapterView<?> parent) {
                textView1.setText("");
                textView2.setText("");
                textView3.setText("");}});

    }
}