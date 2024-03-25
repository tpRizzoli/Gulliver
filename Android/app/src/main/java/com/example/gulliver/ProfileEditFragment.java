// ProfileEditFragment.java

package com.example.gulliver;

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

    public static final String BASE_URL = "http://192.168.0.110:5000";
    Retrofit retrofit = new Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build();

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_modificaprofilo, container, false);

        EditText inputDataUsername = view.findViewById(R.id.cUsername);
        Button btnSalvaModifiche = view.findViewById(R.id.btnSalvaModfiche);

        btnSalvaModifiche.setOnClickListener(v -> {
            String newUsername = inputDataUsername.getText().toString();
            updateUsername(newUsername);
        });

        return view;
    }

    private void updateUsername(String newUsername) {
        MyApiEndpointInterface apiService = retrofit.create(MyApiEndpointInterface.class);

        String idUtente = "1"; //getUserIdFromSharedPreferences(); // Prende l'id dalla SharedPreferences salvata

        UserUpdateRequest userUpdateRequest = new UserUpdateRequest(newUsername, null, null);

        Call<Void> call = apiService.modificaUsername(Integer.parseInt(idUtente), userUpdateRequest);
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
        SharedPreferences prefs = getActivity().getSharedPreferences("Autenticazione", Context.MODE_PRIVATE);
        return prefs.getString("userId", ""); // Ritorna un valore di default
    }
}
