package com.application.ddingdongapp;

import androidx.appcompat.app.AppCompatActivity;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.util.Log;

import com.application.ddingdongapp.databinding.ActivityLoginBinding;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class LoginActivity extends AppCompatActivity {
    private ActivityLoginBinding binding;
    private boolean isDone = false;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityLoginBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());
        binding.button.setOnClickListener(v -> {
            Intent fcm = new Intent(LoginActivity.this, FcmService.class);
            startService(fcm);
            LocalBroadcastManager.getInstance(this).registerReceiver(mAlertReceiver, new IntentFilter("AlertServiceFilter"));
        });

    }

    @Override
    protected void onDestroy() {
        binding = null;
        super.onDestroy();
    }

    private BroadcastReceiver mAlertReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            //토큰을 받음 -> 서버에
            if(!isDone) {
                String token = intent.getStringExtra("token");
                Login(token);
            }
        }
    };

    //로그인 진행
    private void Login(String token) {
        String id = binding.edtID.getText().toString();
        String pw = binding.edtPW.getText().toString();
        ApiCall call = new ApiCall();
        Callback<UserInfo> callback = new Callback<UserInfo>() {
            @Override
            public void onResponse(Call<UserInfo> call, Response<UserInfo> response) {
                //정상적으로 데이터가 수신되는 경우
                if (response.code() == 200) {
                    Intent intent = new Intent(LoginActivity.this, MainActivity.class);
                    startActivity(intent);
                    assert response.body() != null;
                    Log.d("data",response.body().getDept());
                    //ROOM에 데이터 저장
                    isDone = true;
                }

            }

            @Override
            public void onFailure(Call<UserInfo> call, Throwable t) {
                Log.d("data", "gg");
            }
        };
        call.login(id, pw, token, callback);
    }
}