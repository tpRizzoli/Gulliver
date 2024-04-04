package com.example.gulliver.Fragment;

import static com.example.gulliver.Activity.LoginActivity.EMAIL;
import static com.example.gulliver.Activity.LoginActivity.ID;
import static com.example.gulliver.Activity.LoginActivity.MY_PREFERENCES;
import static com.example.gulliver.Activity.LoginActivity.PASSWORD;
import static com.example.gulliver.Activity.LoginActivity.USERNAME;
import static com.example.gulliver.MyApiEndpointInterface.urlServer;

import android.content.Context;
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

import com.example.gulliver.Activity.LoginActivity;
import com.example.gulliver.MyApiEndpointInterface;
import com.example.gulliver.R;
import com.example.gulliver.ClassiModello.User;

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
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_modificaprofilo, container, false);

        EditText inputDataUsername = view.findViewById(R.id.cUsername);
        EditText inputDataEmail = view.findViewById(R.id.cEmail);
        EditText inputDataPassword = view.findViewById(R.id.cPassword);
        Button btnSalvaModifiche = view.findViewById(R.id.btnSalvaModfiche);

        SharedPreferences sp = getActivity().getSharedPreferences(MY_PREFERENCES, Context.MODE_PRIVATE);
        inputDataUsername.setText(sp.getString(LoginActivity.USERNAME, null));
        inputDataEmail.setText(sp.getString(LoginActivity.EMAIL, null));
        inputDataPassword.setText(sp.getString(LoginActivity.PASSWORD, null));

        btnSalvaModifiche.setOnClickListener(v -> {
            String new_username = inputDataUsername.getText().toString();
            String new_email = inputDataEmail.getText().toString();
            String new_pwd = inputDataPassword.getText().toString();

            updateUserInfo(new_username, new_email, new_pwd);
        });

        return view;
    }

    private void updateUserInfo(String new_username, String new_email, String new_pwd) {
        SharedPreferences sp = getActivity().getSharedPreferences(MY_PREFERENCES, Context.MODE_PRIVATE);

        MyApiEndpointInterface apiService = retrofit.create(MyApiEndpointInterface.class);

        Integer idUtente = sp.getInt(LoginActivity.ID, -1);

        Call<User> call = apiService.modificaProfilo(idUtente, new_username, new_email, new_pwd);
        call.enqueue(new Callback<User>() {
            @Override
            public void onResponse(Call<User> call, Response<User> response) {
                if (response.isSuccessful()) {
                    User utenteModificato = response.body();
                    savePreferencesData(utenteModificato);

                    Toast.makeText(getActivity(), "Profilo aggiornato con successo", Toast.LENGTH_SHORT).show();

                    // Passa al fragment ProfileShowFragment
                    Fragment profileShowFragment = new ProfileShowFragment();
                    getParentFragmentManager().beginTransaction()
                            .replace(R.id.flFragment, profileShowFragment)
                            .commit();
                } else {
                    Toast.makeText(getActivity(), "Errore durante l'aggiornamento del Profilo", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<User> call, Throwable t) {
                Toast.makeText(getActivity(), "Errore di rete", Toast.LENGTH_SHORT).show();
            }
        });
    }

    public void savePreferencesData(User utente) {
        SharedPreferences prefs = getActivity().getSharedPreferences(MY_PREFERENCES, Context.MODE_PRIVATE);
        SharedPreferences.Editor editor = prefs.edit();

        if (utente != null) {
            editor.putInt(ID, utente.id);
            editor.putString(USERNAME, utente.username);
            editor.putString(EMAIL, utente.email);
            editor.putString(PASSWORD, utente.password);
            editor.apply();
        }
    }
}
