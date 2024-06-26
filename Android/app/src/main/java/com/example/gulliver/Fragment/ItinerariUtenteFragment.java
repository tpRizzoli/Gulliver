package com.example.gulliver.Fragment;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import com.example.gulliver.Activity.MainActivity;
import com.example.gulliver.ClassiModello.Itinerario;
import com.example.gulliver.Adapter.ItinerarioAdapter;
import com.example.gulliver.MyApiEndpointInterface;
import com.example.gulliver.R;

import java.util.ArrayList;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class ItinerariUtenteFragment extends Fragment {

    Context context;

    protected final static String MY_PREFERENCES = "loginUtente";
    protected final static String ID = "idData";
    Retrofit retrofit;
    ListView listView;
    ItinerarioAdapter adapter;

    ArrayList<Itinerario> listaItinerari = new ArrayList<>();

    @Override
    public void onAttach(@NonNull Context context) {
        super.onAttach(context);
        this.context = context;
    }

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

        listView = view.findViewById(R.id.listaItinerari);
        adapter = new ItinerarioAdapter(context, R.layout.itinerari_list_item, listaItinerari);
        listView.setAdapter(adapter);


        SharedPreferences sharedPreferences = getContext().getSharedPreferences(MY_PREFERENCES, Context.MODE_PRIVATE);
        Integer id = sharedPreferences.getInt(ID, -1);

        Call<ArrayList<Itinerario>> call = apiService.findItinerariUtente(id);

        call.enqueue(new Callback<ArrayList<Itinerario>>() {
            @Override
            public void onResponse(Call<ArrayList<Itinerario>> call, Response<ArrayList<Itinerario>> response) {
                if (response.isSuccessful()) {
                    listaItinerari.clear();

                    listaItinerari.addAll(response.body());

                    adapter.notifyDataSetChanged();
                    listView.invalidate();

                } else {
                    Toast.makeText(getActivity(), "Query Error", Toast.LENGTH_SHORT).show();
                }
            }

            public void onFailure(Call<ArrayList<Itinerario>> call, Throwable t) {
                Toast.makeText(getActivity(), "Errore di rete", Toast.LENGTH_SHORT).show();
            }
        });


        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                Bundle extra = new Bundle();

                Itinerario i = listaItinerari.get(position);

                extra.putInt("idItinerario", i.id);
                extra.putString("nomeItinerario", i.nome);

                DettagliItinerarioFragment dettagliItinerario = new DettagliItinerarioFragment();
                ((MainActivity)context).changeFragment(dettagliItinerario, extra);
            }
        });


        return view;
    }
}
