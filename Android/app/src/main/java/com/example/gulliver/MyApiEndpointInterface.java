package com.example.gulliver;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.PUT;
import retrofit2.http.Path;
import retrofit2.http.Query;
import java.util.ArrayList;

public interface MyApiEndpointInterface {

    // GET http://api.myservice.com/users/francesca
    @GET("/getUser")
    Call<ArrayList<User>> getUser(@Query("utente") String username, @Query("password") String password);

    @PUT("/modificaProfilo/{id}")
    Call<Void> modificaUsername(
            @Query("id") int id,
            @Query("username") String newUsername
    );

    @GET("/allusers")
    Call<ArrayList<User>> getAllUsers();

    // GET http://www.sito.it/group/103/users?sort=asc
    @GET("/group/{id}/users")
    Call<ArrayList<User>> groupList(@Path("id") int groupId, @Query("sort") String sort);

    @POST("/users/new")
    Call<User> createUser(@Body User user);
}
