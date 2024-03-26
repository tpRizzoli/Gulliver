package com.example.gulliver;

import static com.example.gulliver.MyApiEndpointInterface.urlServer;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;

import java.io.IOException;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
import com.google.gson.Gson;

public class LoginActivity extends AppCompatActivity {

    protected final static String MY_PREFERENCES = "loginUtente";
    protected final static String ID = "idData";
    protected final static String USERNAME = "usernameData";
    protected final static String EMAIL = "emailData";
    protected final static String PASSWORD = "passwordData";

    public static final String BASE_URL = urlServer;
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

            Call<ResponseBody> call = apiService.getUser(username, password);
            call.enqueue(new Callback<ResponseBody>() {
                @Override
                public void onResponse(Call<ResponseBody> call, Response<ResponseBody> response) {

                    if (response.isSuccessful()) {
                        ResponseBody body = response.body();
                        try {
                            String jsonString = body.string();
                            if(!jsonString.equals("[]")) {
                                Gson gson = new Gson();

                                User utenteCreato = gson.fromJson(jsonString, User.class);

                                savePreferencesData(utenteCreato);

                                Intent activity = new Intent(LoginActivity.this, MainActivity.class);
                                startActivity(activity);
                                Toast.makeText(LoginActivity.this, "Accesso eseguito con successo!", Toast.LENGTH_SHORT).show();
                            }else{
                                Toast.makeText(LoginActivity.this, "Credenziali errate", Toast.LENGTH_SHORT).show();
                            }

                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    } else {
                        Toast.makeText(LoginActivity.this, "Errore di rete", Toast.LENGTH_SHORT).show();
                    }
                }

                private boolean isUserLoggedIn() {
                    SharedPreferences prefs = getSharedPreferences(MY_PREFERENCES, Context.MODE_PRIVATE);
                    return prefs.contains(ID) && prefs.contains(USERNAME) && prefs.contains(EMAIL) && prefs.contains(PASSWORD);
                }


                public void onFailure(Call<ResponseBody> call, Throwable t) {
                    Toast.makeText(LoginActivity.this, "Errore di rete", Toast.LENGTH_SHORT).show();
                }
            });
        });

        // updatePreferencesData();
    }

    public void savePreferencesData(User utente) {
        SharedPreferences prefs = getSharedPreferences(MY_PREFERENCES, Context.MODE_PRIVATE);
        SharedPreferences.Editor editor = prefs.edit();

        if(utente != null){
            editor.putInt(ID, utente.id);
            editor.putString(USERNAME, utente.username);
            editor.putString(EMAIL, utente.username);
            editor.putString(PASSWORD, utente.username); // Valutare di non salvare la password quì

            editor.apply();
        }
    }
}
