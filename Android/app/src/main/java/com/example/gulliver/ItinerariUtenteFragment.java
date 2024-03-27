package com.example.gulliver;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class ItinerariUtenteFragment extends Fragment {

    protected final static String MY_PREFERENCES = "loginUtente";
    protected final static String ID = "idData";
    Retrofit retrofit;
    RecyclerView recyclerView;
    ItinerarioAdapter adapter;

    @SuppressLint("WrongViewCast")
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_itinerari_utente, container, false);

        retrofit = new Retrofit.Builder()
                .baseUrl(MyApiEndpointInterface.urlServer)
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        MyApiEndpointInterface apiService = retrofit.create(MyApiEndpointInterface.class);

        recyclerView = view.findViewById(R.id.container_itinerari);
        recyclerView.setLayoutManager(new LinearLayoutManager(getContext()));

        SharedPreferences sharedPreferences = getContext().getSharedPreferences(MY_PREFERENCES, Context.MODE_PRIVATE);
        Integer id = sharedPreferences.getInt(ID, -1);

        Call<ArrayList<Itinerario>> call = apiService.findItinerariUtente(id);

        call.enqueue(new Callback<ArrayList<Itinerario>>() {
            @Override
            public void onResponse(Call<ArrayList<Itinerario>> call, Response<ArrayList<Itinerario>> response) {
                if (response.isSuccessful()) {
                    ArrayList<Itinerario> itinerari = response.body();
                    adapter = new ItinerarioAdapter(itinerari, getContext());
                    recyclerView.setAdapter(adapter);
                } else {
                    Toast.makeText(getActivity(), "Impossibile vedere", Toast.LENGTH_SHORT).show();
                }
            }

            public void onFailure(Call<ArrayList<Itinerario>> call, Throwable t) {
                // Gestisci eventuali errori di comunicazione qui
                Toast.makeText(getActivity(), "errore...", Toast.LENGTH_SHORT).show();
            }
        });
        return view;
    }
}
