// UserUpdateRequest.java

package com.example.gulliver.ClassiModello;

import com.google.gson.annotations.SerializedName;

public class UserUpdateRequest {

    @SerializedName("username")
    public String new_username;
    @SerializedName("email")
    public String new_email;

    @SerializedName("password")
    public String new_pwd;

    public UserUpdateRequest(String new_username, String  new_email, String  new_pwd) {
        this.new_username = new_username;
        this.new_email = new_email;
        this.new_pwd = new_pwd;
    }
}