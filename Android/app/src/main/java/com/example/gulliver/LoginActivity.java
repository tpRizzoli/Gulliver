package com.example.gulliver;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import java.util.ArrayList;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class LoginActivity extends AppCompatActivity {

    protected final static String MY_PREFERENCES = "Autenticazione";
    protected final static String USERNAME_DATA_KEY = "usernameData";
    protected final static String PASSWORD_DATA_KEY = "passwordData";

    public static final String BASE_URL = "http://192.168.0.111:5000 ";
    Retrofit retrofit = new Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build();

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        Button btnOpenActivity = findViewById(R.id.btnRegistrazione);
        btnOpenActivity.setOnClickListener(v -> {
            Intent activity = new Intent(LoginActivity.this, RegisterActivity.class);
            startActivity(activity);
        });

        MyApiEndpointInterface apiService = retrofit.create(MyApiEndpointInterface.class);

        Button btnLoginButton = findViewById(R.id.loginButton);
        btnLoginButton.setOnClickListener(v -> {
            EditText outputViewUsername = findViewById(R.id.inputDataUsername);
            EditText outputViewPassword = findViewById(R.id.inputDataPassword);
            String username = outputViewUsername.getText().toString();
            String password = outputViewPassword.getText().toString();

            Call<ArrayList<User>> call = apiService.getUser(username, password);
            call.enqueue(new Callback<ArrayList<User>>() {
                @Override
                public void onResponse(Call<ArrayList<User>> call, Response<ArrayList<User>> response) {
                    if (response.isSuccessful()) {
                        User user = ((ArrayList<User>) response.body()).get(0);
                        if (user != null && user.password.equals(password)) {
                            savePreferencesData();

                            Intent activity = new Intent(LoginActivity.this, MainActivity.class);
                            startActivity(activity);
                            Toast.makeText(LoginActivity.this, "Accesso eseguito con successo!", Toast.LENGTH_SHORT).show();

                        } else {
                            Toast.makeText(LoginActivity.this, "Credenziali errate", Toast.LENGTH_SHORT).show();
                        }
                    } else {
                        Toast.makeText(LoginActivity.this, "Errore di rete", Toast.LENGTH_SHORT).show();
                    }
                }

                private boolean isUserLoggedIn() {
                    SharedPreferences prefs = getSharedPreferences(MY_PREFERENCES, Context.MODE_PRIVATE);
                    return prefs.contains(USERNAME_DATA_KEY) && prefs.contains(PASSWORD_DATA_KEY);
                }

                @Override
                public void onFailure(Call<ArrayList<User>> call, Throwable t) {
                    Toast.makeText(LoginActivity.this, "Errore di rete", Toast.LENGTH_SHORT).show();
                }
            });
        });

        // updatePreferencesData();
    }

    public void savePreferencesData() {
        SharedPreferences prefs = getSharedPreferences(MY_PREFERENCES, Context.MODE_PRIVATE);
        SharedPreferences.Editor editor = prefs.edit();

        EditText outputViewUsername = findViewById(R.id.inputDataUsername);
        EditText outputViewPassword = findViewById(R.id.inputDataPassword);
        CharSequence textDataUsername = outputViewUsername.getText();
        CharSequence textDataPassword = outputViewPassword.getText();

        if (textDataUsername != null && textDataPassword != null) {
            editor.putString(USERNAME_DATA_KEY, textDataUsername.toString());
            editor.putString(PASSWORD_DATA_KEY, textDataPassword.toString());
            editor.apply();
        }
        //updatePreferencesData();
    }
}
