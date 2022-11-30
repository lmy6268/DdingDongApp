package com.application.ddingdongapp;

import androidx.appcompat.app.AppCompatActivity;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;

import android.app.ProgressDialog;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;

import com.application.ddingdongapp.databinding.ActivityLoginBinding;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class LoginActivity extends AppCompatActivity {
    private ActivityLoginBinding binding;
    private boolean isDone = false;
    private boolean isWait = false;
    private Context context = this;
    ProgressDialog progressDialog;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityLoginBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());
        progressDialog = new ProgressDialog(this);
        progressDialog.setMessage("로그인 중입니다...");
        progressDialog.setCancelable(true);
        progressDialog.setProgressStyle(android.R.style.Widget_ProgressBar_Horizontal);

        binding.button.setOnClickListener(v -> {
            String id = binding.edtID.getText().toString();
            String pw = binding.edtPW.getText().toString();
            //아이디 or 비밀번호에 공백이 포함된 경우
            if (id.contains(" ") || pw.contains(" "))
                Toast.makeText(context, "아이디 혹은 비밀번호에 공백이 포함되어있습니다.", Toast.LENGTH_SHORT).show();
            else if (!id.equals("") && !pw.equals("")) {
                Intent fcm = new Intent(LoginActivity.this, FcmService.class);
                startService(fcm);
                LocalBroadcastManager.getInstance(this).registerReceiver(mAlertReceiver, new IntentFilter("AlertServiceFilter"));
            }
            //아이디 or 비밀번호가 입력이 되지 않은 경우
            else Toast.makeText(context, "아이디와 비밀번호를 모두 입력 후 진행해 주세요.", Toast.LENGTH_SHORT).show();
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
            //토큰을 받음 -> 서버에 전달
            if (!isDone) {
                String token = intent.getStringExtra("token");
                Login(token);
            }
        }
    };

    //로그인 진행
    private void Login(String token) {
        String id = binding.edtID.getText().toString();
        String pw = binding.edtPW.getText().toString();
        ApiCall call = ApiCall.getInstance();
        progressDialog.show();
        Callback<UserInfo> callback = new Callback<UserInfo>() {

            @Override
            public void onResponse(Call<UserInfo> call, Response<UserInfo> response) {
                isWait = false;
                progressDialog.cancel();
                //정상적으로 데이터가 수신되는 경우 -> 로그인 성공
                if (response.code() == 200) {
                    Intent intent = new Intent(LoginActivity.this, MainActivity.class);
                    intent.putExtra("userInfo", response.body());
                    startActivity(intent);
                    finish();
                    assert response.body() != null;
                    Log.d("data", response.body().getClassDataList().get(0).getName());
                    //ROOM에 데이터 저장
                    isDone = true; //
                } else if (response.code() == 400) {
                    Toast.makeText(context, "사이버캠퍼스 생체인증 혹은 메일 인증을 수행 후 진행해 주세요.", Toast.LENGTH_SHORT).show();
                } else {
                    Toast.makeText(context, "올바르지 않은 정보를 입력하였습니다.", Toast.LENGTH_SHORT).show();
                }

            }

            @Override
            public void onFailure(Call<UserInfo> call, Throwable t) {
                isWait = false;
                progressDialog.cancel();
                Toast.makeText(context, "서버와 접속하는데 실패하였습니다.", Toast.LENGTH_SHORT).show();
            } //실패했을 떄
        };
        if (!isWait) {
            call.login(id, pw, token, callback);
            isWait = true;
        }
    }
}