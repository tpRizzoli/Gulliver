package com.example.gulliver.Fragment;

import static com.example.gulliver.MyApiEndpointInterface.urlServer;

import android.content.Context;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.GridView;
import android.widget.Toast;

import com.example.gulliver.Activity.MainActivity;
import com.example.gulliver.MyApiEndpointInterface;
import com.example.gulliver.R;
import com.example.gulliver.ClassiModello.Tipologia;
import com.example.gulliver.Adapter.TipologieAdapter;

import java.util.ArrayList;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class TipologieFragment extends Fragment {
    public static final String BASE_URL = urlServer;

    Retrofit retrofit = new Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build();

    Context context;
    GridView gridView = null;
    TipologieAdapter tAdapter = null;

    ArrayList<Tipologia> listaTipologie = new ArrayList<>();

    @Override
    public void onAttach(@NonNull Context context) {
        super.onAttach(context);
        this.context = context;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_tipologie, container, false);
        MyApiEndpointInterface apiService = retrofit.create(MyApiEndpointInterface.class);

        tAdapter = new TipologieAdapter(context, R.layout.tipologie_grid_item, listaTipologie);
        gridView = view.findViewById(R.id.tabellaTipologie);
        gridView.setAdapter(tAdapter);

        Button pulsanteAvanti = view.findViewById(R.id.confermaTipologie);

        String nomeLuogo = getArguments().getString("nomeLuogo");

        pulsanteAvanti.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ArrayList<Boolean> checkedList = tAdapter.getCheckedStates();
                ArrayList<Tipologia> objectsList = tAdapter.getAdapterList();

                Bundle tipSelezionate = new Bundle();
                ArrayList<Integer> idTipologieSelezionate = new ArrayList<>();


                for(int i = 0; i < checkedList.size(); i++){
                    if(checkedList.get(i) == true)
                        idTipologieSelezionate.add(objectsList.get(i).id);
                }

                tipSelezionate.putIntegerArrayList("idTipologie", idTipologieSelezionate);
                tipSelezionate.putString("nomeLuogo", nomeLuogo);

                AttivitaFragment attivitaFragment = new AttivitaFragment();
                ((MainActivity) context).changeFragment(attivitaFragment, tipSelezionate);
            }
        });


        Call<ArrayList<Tipologia>> call = apiService.findTipologie(nomeLuogo);
        call.enqueue(new Callback<ArrayList<Tipologia>>(){
            @Override
            public void onResponse(Call<ArrayList<Tipologia>> call, Response<ArrayList<Tipologia>> response) {
                if(response.isSuccessful()){
                    ArrayList<Tipologia> listaTipologie = response.body();
                    tAdapter.addAll(listaTipologie);
                    tAdapter.notifyDataSetChanged();
                    gridView.invalidate();

                }else{
                    Toast.makeText(context, "Query Error", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<ArrayList<Tipologia>> call, Throwable t) {
                Toast.makeText(context, "Errore di rete", Toast.LENGTH_SHORT).show();
            }
        });



        return view;
    }
}