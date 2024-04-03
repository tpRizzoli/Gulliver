package com.example.gulliver.Fragment;

import static com.example.gulliver.MyApiEndpointInterface.urlServer;

import android.content.Context;
import android.os.Bundle;

import com.example.gulliver.Activity.LoginActivity;
import com.example.gulliver.Activity.MainActivity;
import com.example.gulliver.Adapter.AttivitaAdapter;
import com.example.gulliver.ClassiModello.Attivita;
import com.example.gulliver.MyApiEndpointInterface;
import com.example.gulliver.R;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;

import java.util.ArrayList;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class AttivitaFragment extends Fragment {
    public static final String BASE_URL = urlServer;
    Retrofit retrofit= new Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build();

    MyApiEndpointInterface apiService = retrofit.create(MyApiEndpointInterface.class);

    Context context;
    ListView listView;
    Button button;

    AttivitaAdapter aAdapter;

    @Override
    public void onAttach(@NonNull Context context) {
        super.onAttach(context);
        this.context = context;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_attivita, container, false);

        listView = view.findViewById(R.id.listaAttivita);
        button = view.findViewById(R.id.confermaAttivita);

        ArrayList<Attivita> listaAttivita = new ArrayList<>();

        aAdapter = new AttivitaAdapter(context, R.layout.attivita_list_item, listaAttivita);
        listView.setAdapter(aAdapter);

        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                AttivitaAdapter adapter = (AttivitaAdapter) listView.getAdapter();
                ArrayList<Boolean> checkedList = adapter.getCheckedStates();
                ArrayList<Attivita> objectsList = adapter.getAdapterList();

                Bundle extra = new Bundle();
                ArrayList<Integer> idAttivitaSelezionate = new ArrayList<>();

                for(int i = 0; i < checkedList.size(); i++){
                    if(checkedList.get(i) == true)
                        idAttivitaSelezionate.add(objectsList.get(i).id);
                }

                extra.putIntegerArrayList("idAttivita", idAttivitaSelezionate);

                ConfermaItinerarioFragment confermaItinerario = new ConfermaItinerarioFragment();
                ((MainActivity) context).changeFragment(confermaItinerario, extra);
            }
        });

        Bundle extra = getArguments();
        ArrayList<Integer> listaTipologie = extra.getIntegerArrayList("idTipologie");
        String nomeLuogo = extra.getString("nomeLuogo");

        Call<ArrayList<Attivita>> call = apiService.findAttivitaFromTipologie(nomeLuogo, listaTipologie);
        call.enqueue(new Callback<ArrayList<Attivita>>() {
            @Override
            public void onResponse(Call<ArrayList<Attivita>> call, Response<ArrayList<Attivita>> response) {
                if(response.isSuccessful()){
                    ArrayList<Attivita> listaAttivita = response.body();
                    aAdapter.addAll(listaAttivita);
                    aAdapter.notifyDataSetChanged();
                    listView.invalidate();

                }else{
                    Toast.makeText(context, "Query Error", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<ArrayList<Attivita>> call, Throwable t) {
                Toast.makeText(context, "Errore di rete", Toast.LENGTH_SHORT).show();
            }
        });
        return view;
    }
}


// Usare onItemClick per intercettare il checked