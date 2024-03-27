package com.example.gulliver;

import static com.example.gulliver.LoginActivity.MY_PREFERENCES;
import static com.example.gulliver.MyApiEndpointInterface.urlServer;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.GridView;

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

    Context ctx;
    GridView grigliaTipologie = null;
    TipologieGridAdapter tga = null;

    ArrayList<Tipologia> listaTipologie = new ArrayList<>();

    @Override
    public void onAttach(@NonNull Context context) {
        super.onAttach(context);
        ctx = context;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_tipologie, container, false);
        MyApiEndpointInterface apiService = retrofit.create(MyApiEndpointInterface.class);

        tga = new TipologieGridAdapter(ctx, R.layout.tipologie_grid_item, listaTipologie);
        grigliaTipologie = view.findViewById(R.id.tabellaTipologie);
        grigliaTipologie.setAdapter(tga);

        Button pulsanteAvanti = view.findViewById(R.id.confermaTipologie);

        String nomeLuogo = getArguments().getString("nomeLuogo");

        Call<ArrayList<Tipologia>> call = apiService.findTipologie(nomeLuogo);
        call.enqueue(new Callback<ArrayList<Tipologia>>(){

            @Override
            public void onResponse(Call<ArrayList<Tipologia>> call, Response<ArrayList<Tipologia>> response) {
                if(response.isSuccessful()){
                    ArrayList<Tipologia> listaTipologie = response.body();
                    tga.addAll(listaTipologie);
                    tga.notifyDataSetChanged();
                    grigliaTipologie.invalidate();



                }else{

                }
            }

            @Override
            public void onFailure(Call<ArrayList<Tipologia>> call, Throwable t) {

            }
        });



        return view;
    }
}