package com.example.gulliver;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Response;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.PUT;
import retrofit2.http.Path;
import retrofit2.http.Query;
import java.util.ArrayList;

public interface MyApiEndpointInterface {

    String urlServer = "http://192.168.0.106:5000";

    // GET http://api.myservice.com/users/francesca
    @GET("/getUser")
    Call<ResponseBody> getUser(@Query("utente") String username, @Query("password") String password);
    Call<ResponseBody> getUser();

    @PUT("/modificaProfilo/{id}")
    Call<ResponseBody> modificaUsername(@Path("id")Integer id, @Query("username") String username, @Query("email") String email, @Query("password") String pwd);

    @GET("/allusers")
    Call<ArrayList<User>> getAllUsers();

    // GET http://www.sito.it/group/103/users?sort=asc
    @GET("/group/{id}/users")
    Call<ArrayList<User>> groupList(@Path("id") int groupId, @Query("sort") String sort);

    @POST("/users/new")
    Call<User> createUser(@Body User user);
}
