package com.application.ddingdongapp;

import android.net.Uri;
import android.util.Log;

import java.util.HashMap;
import java.util.Map;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
import retrofit2.http.POST;

public class ApiCall {
    Retrofit retrofit;
    RetrofitService service;
    String URL = "http://192.168.1.19:3000/";

    ApiCall() {
        retrofit = new Retrofit.Builder().baseUrl(URL).addConverterFactory(GsonConverterFactory.create()).build();
        service = retrofit.create(RetrofitService.class);
    }

    //서버에 로그인
    public void login(String id, String pw, String token, Callback<UserInfo> callback) {
        Map<String,String> map =new HashMap();
        map.put("uid",id);
        map.put("upw",pw);
        map.put("token",token);
        Call<UserInfo> call = service.login(map);
        call.enqueue(callback);
    }
}
