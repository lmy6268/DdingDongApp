package com.application.ddingdongapp;

import android.net.Uri;
import android.util.Log;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeUnit;

import okhttp3.OkHttpClient;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
import retrofit2.http.POST;

public class ApiCall {
    private static ApiCall instance = null;
    //레트로핏이 자꾸만 생성되서 call이 여러개로 생겨남
    private final RetrofitService service;
    String URL = "http://193.123.230.166:8000/"; //접속할 서버 주소
    final OkHttpClient okHttpClient = new OkHttpClient().newBuilder().readTimeout(10, TimeUnit.SECONDS)
            .connectTimeout(10, TimeUnit.SECONDS).build(); //1초동안 전달이 안되면 오류로 간주
    private ApiCall() {
        Retrofit retrofit = new Retrofit.Builder().baseUrl(URL).addConverterFactory(GsonConverterFactory.create()).client(okHttpClient).build();
        service = retrofit.create(RetrofitService.class);
    }
    //싱글톤 형식
    public static ApiCall getInstance(){
        if(instance == null) instance = new ApiCall();
        return instance;
    }
    //서버에 로그인
    public void login(String id, String pw, String token, Callback<UserInfo> callback) {
        Map<String, String> map = new HashMap();
        map.put("uid", id);
        map.put("upw", pw);
        map.put("token", token);
        Call<UserInfo> call = service.login(map);
        call.enqueue(callback);
    }
}
