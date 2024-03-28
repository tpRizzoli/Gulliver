package com.example.gulliver.ClassiModello;

import com.google.gson.annotations.SerializedName;

public class User {
    @SerializedName("id")
    public Integer id;
    @SerializedName("username")
    public String username;
    @SerializedName("email")
    public String email;
    @SerializedName("password")
    public String password;

    public User(Integer id, String username, String email, String password) {
        this.id = id;
        this.username = username;
        this.email = email;
        this.password = password;
    }
}

