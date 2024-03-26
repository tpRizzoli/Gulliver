// ProfileEditFragment.java

package com.example.gulliver;

import static com.example.gulliver.LoginActivity.EMAIL;
import static com.example.gulliver.LoginActivity.ID;
import static com.example.gulliver.LoginActivity.MY_PREFERENCES;
import static com.example.gulliver.LoginActivity.PASSWORD;
import static com.example.gulliver.LoginActivity.USERNAME;
import static com.example.gulliver.MyApiEndpointInterface.urlServer;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;

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

        SharedPreferences sp = getActivity().getSharedPreferences(MY_PREFERENCES, Context.MODE_PRIVATE);
        inputDataUsername.setText(sp.getString(LoginActivity.USERNAME, null));
        inputDataEmail.setText(sp.getString(LoginActivity.EMAIL, null));
        inputDataPassword.setText(sp.getString(LoginActivity.PASSWORD, null));

        btnSalvaModifiche.setOnClickListener(v -> {;
            ProfileShowFragment profileShowFragment = new ProfileShowFragment();
            FragmentManager fragmentManager = requireActivity().getSupportFragmentManager();

            String new_username = inputDataUsername.getText().toString();
            String new_email = inputDataEmail.getText().toString();
            String new_pwd = inputDataPassword.getText().toString();

            updateUserInfo(new_username, new_email, new_pwd);

            fragmentManager.beginTransaction()
                    .replace(R.id.flFragment, profileShowFragment)
                    .addToBackStack(null)
                    .commit();
        });

        // -------------------------- \\

        Button btnAnnullaModifiche = view.findViewById(R.id.btnAnnullaModifiche);
        btnAnnullaModifiche.setOnClickListener(v -> {
            // Creare l'istanza del fragment ProfileShowFragment
            ProfileShowFragment profileShowFragment = new ProfileShowFragment();

            // Ottenere il FragmentManager
            FragmentManager fragmentManager = requireActivity().getSupportFragmentManager();

            // Iniziare una transazione per sostituire il fragment corrente con il ProfileShowFragment
            fragmentManager.beginTransaction()
                    .replace(R.id.flFragment, profileShowFragment) // R.id.fragment_container è l'ID del contenitore dei frammenti nell'activity
                    .addToBackStack(null) // Aggiungi questa transazione allo stack indietro, in modo che l'utente possa tornare al fragment precedente premendo il pulsante indietro
                    .commit();
        });

        return view;
    }

    private void updateUserInfo(String new_username, String new_email, String new_pwd) {
        SharedPreferences sp = getActivity().getSharedPreferences(MY_PREFERENCES, Context.MODE_PRIVATE);

        MyApiEndpointInterface apiService = retrofit.create(MyApiEndpointInterface.class);

       Integer idUtente = sp.getInt(LoginActivity.ID, -1); // Integer.parseInt(getUserIdFromSharedPreferences()); // Prende l'id dalla SharedPreferences salvata

        Call<User> call = apiService.modificaProfilo(idUtente, new_username, new_email, new_pwd);
        call.enqueue(new Callback<User>() {
            @Override
            public void onResponse(Call<User> call, Response<User> response) {
                if (response.isSuccessful()) {
                    User utenteModificato = response.body();
                    savePreferencesData(utenteModificato);

                    Toast.makeText(getActivity(), "Profilo aggiornato con successo", Toast.LENGTH_SHORT).show();
                } else {
                    Toast.makeText(getActivity(), "Errore durante l'aggiornamento del Profilo", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call < User > call, Throwable t){
                Toast.makeText(getActivity(), "Errore di rete", Toast.LENGTH_SHORT).show();
            }
        });
    }



    private String getUserIdFromSharedPreferences() {
        SharedPreferences prefs = getActivity().getSharedPreferences(MY_PREFERENCES, Context.MODE_PRIVATE);
        return prefs.getString("userId", ""); // Ritorna un valore di default
    }

    public void savePreferencesData(User utente) {
        SharedPreferences prefs = getActivity().getSharedPreferences(MY_PREFERENCES, Context.MODE_PRIVATE);
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
