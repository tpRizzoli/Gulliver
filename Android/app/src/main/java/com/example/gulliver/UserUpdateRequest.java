// UserUpdateRequest.java

package com.example.gulliver;

public class UserUpdateRequest {
    private String userName;
    private String userEmail;
    private String userPassword;

    public UserUpdateRequest(String userName, String userEmail, String userPassword) {
        this.userName = userName;
        this.userEmail = userEmail;
        this.userPassword = userPassword;
    }

    // Aggiungi getter e setter se necessario
}
