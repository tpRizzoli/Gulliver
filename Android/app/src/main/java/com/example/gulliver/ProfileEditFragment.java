// ProfileEditFragment.java

package com.example.gulliver;

import static com.example.gulliver.LoginActivity.MY_PREFERENCES;
import static com.example.gulliver.MyApiEndpointInterface.urlServer;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import androidx.fragment.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class ProfileEditFragment extends Fragment {

    public static final String BASE_URL = urlServer;
    Retrofit retrofit = new Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build();

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_modificaprofilo, container, false);

        EditText inputDataUsername = view.findViewById(R.id.cUsername);
        EditText inputDataEmail = view.findViewById(R.id.cEmail);
        EditText inputDataPassword = view.findViewById(R.id.cPassword);
        Button btnSalvaModifiche = view.findViewById(R.id.btnSalvaModfiche);

        btnSalvaModifiche.setOnClickListener(v -> {;
            String new_username = inputDataUsername.getText().toString();
            String new_email = inputDataEmail.getText().toString();
            String new_pwd = inputDataPassword.getText().toString();

            updateUserInfo(new_username, new_email, new_pwd);
        });

        return view;
    }

    private void updateUserInfo(String new_username, String new_email, String new_pwd) {
        MyApiEndpointInterface apiService = retrofit.create(MyApiEndpointInterface.class);

       Integer idUtente = 1; // Integer.parseInt(getUserIdFromSharedPreferences()); // Prende l'id dalla SharedPreferences salvata

        Call<Void> call = apiService.modificaUsername(idUtente, new_username, new_email, new_pwd);
        call.enqueue(new Callback<Void>() {
            @Override
            public void onResponse(Call<Void> call, Response<Void> response) {
                if (response.isSuccessful()) {
                    Toast.makeText(getActivity(), "Username aggiornato con successo", Toast.LENGTH_SHORT).show();
                } else {
                    Toast.makeText(getActivity(), "Errore durante l'aggiornamento dell'username", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<Void> call, Throwable t) {
                Toast.makeText(getActivity(), "Errore di rete", Toast.LENGTH_SHORT).show();
            }
        });
    }

    private String getUserIdFromSharedPreferences() {
        SharedPreferences prefs = getActivity().getSharedPreferences(MY_PREFERENCES, Context.MODE_PRIVATE);
        return prefs.getString("userId", ""); // Ritorna un valore di default
    }
}
