package com.example.gulliver.Activity;
import static com.example.gulliver.Activity.LoginActivity.EMAIL;
import static com.example.gulliver.Activity.LoginActivity.ID;
import static com.example.gulliver.Activity.LoginActivity.MY_PREFERENCES;
import static com.example.gulliver.Activity.LoginActivity.PASSWORD;
import static com.example.gulliver.Activity.LoginActivity.USERNAME;
import static com.example.gulliver.MyApiEndpointInterface.urlServer;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.gulliver.MyApiEndpointInterface;
import com.example.gulliver.R;
import com.example.gulliver.ClassiModello.User;

import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
import retrofit2.Call;

public class RegisterActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        final String BASE_URL = urlServer;
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl(BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        MyApiEndpointInterface apiService = retrofit.create(MyApiEndpointInterface.class);

        EditText casellaUsername = findViewById(R.id.cUsername);
        EditText casellaEmail = findViewById(R.id.cEmail);
        EditText casellaPassword = findViewById(R.id.cPassword);
        EditText casellaConfermaPassword = findViewById(R.id.cConfermaPassword);

        Button registrationButton = findViewById(R.id.btnRegistrazione);

        registrationButton.setOnClickListener(v ->{
            String username = casellaUsername.getText().toString().trim();
            String email = casellaEmail.getText().toString().trim();
            String password = casellaPassword.getText().toString().trim();
            String confermaPassword = casellaConfermaPassword.getText().toString().trim();

            if(username.equals("")){
                Toast.makeText(this, "È necessario compilare tutti i campi di testo!", Toast.LENGTH_SHORT).show();
            } else if(email.equals("")) {
                Toast.makeText(this, "È necessario compilare tutti i campi di testo!", Toast.LENGTH_SHORT).show();
            } else if(password.equals("")) {
                Toast.makeText(this, "È necessario compilare tutti i campi di testo!", Toast.LENGTH_SHORT).show();
            } else if(confermaPassword.equals("")) {
                Toast.makeText(this, "È necessario compilare tutti i campi di testo!", Toast.LENGTH_SHORT).show();
            } else if(!password.equals(confermaPassword)) {
                Toast.makeText(this, "Le password inserite non corrispondono!", Toast.LENGTH_SHORT).show();
            } else {

                Call<User> call = apiService.createUser(username, email, password);

                call.enqueue(new Callback<User>() {
                    @Override
                    public void onResponse(Call<User> call, Response<User> response) {
                        if(response.isSuccessful()){
                            User utenteCreato = response.body();
                            savePreferencesData(utenteCreato);

                            Intent i = new Intent(RegisterActivity.this, MainActivity.class);
                            startActivity(i);
                            Toast.makeText(RegisterActivity.this, "Registrazione completata!", Toast.LENGTH_SHORT).show();
                        } else {
                            Toast.makeText(RegisterActivity.this, "Registrazione fallita!", Toast.LENGTH_SHORT).show();
                        }
                    }

                    @Override
                    public void onFailure(Call<User> call, Throwable t) {
                        Toast.makeText(RegisterActivity.this, "Errore di Rete!", Toast.LENGTH_SHORT).show();
                    }
                });
            }
        });

    }

    public void savePreferencesData(User utente) {
        SharedPreferences prefs = getSharedPreferences(MY_PREFERENCES, Context.MODE_PRIVATE);
        SharedPreferences.Editor editor = prefs.edit();

        if(utente != null){
            editor.putInt(ID, utente.id);
            editor.putString(USERNAME, utente.username);
            editor.putString(EMAIL, utente.email);
            editor.putString(PASSWORD, utente.password); // Valutare di non salvare la password quì

            editor.apply();
        }
    }

}
