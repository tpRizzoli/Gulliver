package com.example.gulliver.Fragment;

import static com.example.gulliver.MyApiEndpointInterface.urlServer;

import android.content.Context;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.gulliver.Activity.MainActivity;
import com.example.gulliver.Adapter.AttivitaAdapter;
import com.example.gulliver.Adapter.ItinerarioAdapter;
import com.example.gulliver.ClassiModello.Itinerario;
import com.example.gulliver.MyApiEndpointInterface;
import com.example.gulliver.R;

import java.util.ArrayList;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class ItinerariSuggeritiFragment extends Fragment {

    Context context;

    TextView testoCategoria;
    ListView elencoItinerari;

    public static final String BASE_URL = urlServer;
    Retrofit retrofit= new Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build();

    MyApiEndpointInterface apiService = retrofit.create(MyApiEndpointInterface.class);

    ItinerarioAdapter adapter;
    ArrayList<Itinerario> itinerariSuggeriti = new ArrayList<>();

    @Override
    public void onAttach(@NonNull Context context) {
        super.onAttach(context);
        this.context = context;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_itinerari_suggeriti, container, false);

        testoCategoria = view.findViewById(R.id.nomeCategoria);
        elencoItinerari = view.findViewById(R.id.listaItinerari);

        adapter = new ItinerarioAdapter(context, R.layout.itinerari_list_item, itinerariSuggeriti);
        elencoItinerari.setAdapter(adapter);

        String nomeCategoria = getArguments().getString("nomeCategoria");

        testoCategoria.setText(nomeCategoria);

        Call<ArrayList<Itinerario>> call = apiService.findItinerariSuggeriti(nomeCategoria);
        call.enqueue(new Callback<ArrayList<Itinerario>>() {
            @Override
            public void onResponse(Call<ArrayList<Itinerario>> call, Response<ArrayList<Itinerario>> response) {
                if (response.isSuccessful()){
                    itinerariSuggeriti = response.body();

                    adapter.clear();
                    adapter.addAll(itinerariSuggeriti);

                    adapter.notifyDataSetChanged();
                    elencoItinerari.invalidate();

                } else {
                    Toast.makeText(context, "Query Error", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<ArrayList<Itinerario>> call, Throwable t) {
                Toast.makeText(context, "Connection Error", Toast.LENGTH_SHORT).show();
            }
        });

        elencoItinerari.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                Bundle extra = new Bundle();

                Itinerario i = itinerariSuggeriti.get(position);

                extra.putInt("idItinerario", i.id);
                extra.putString("nomeItinerario", i.nome);

                ConfermaItinerarioFragment confermaItinerario = new ConfermaItinerarioFragment();
                ((MainActivity)context).changeFragment(confermaItinerario, extra);
            }
        });

        return view;
    }
}