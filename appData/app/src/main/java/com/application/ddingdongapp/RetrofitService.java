package com.application.ddingdongapp;


import java.util.Map;

import retrofit2.Call;
import retrofit2.http.Body;

import retrofit2.http.FieldMap;
import retrofit2.http.FormUrlEncoded;
import retrofit2.http.POST;

public interface RetrofitService {
    //로그인 시
    @FormUrlEncoded
    @POST("login")
    Call<UserInfo> login(
            @FieldMap Map<String, String> map
            );
}
