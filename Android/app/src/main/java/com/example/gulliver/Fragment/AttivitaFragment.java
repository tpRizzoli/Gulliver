package com.example.gulliver.Fragment;

import static com.example.gulliver.MyApiEndpointInterface.urlServer;

import android.content.Context;
import android.os.Bundle;
import com.example.gulliver.R;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ListView;

import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class AttivitaFragment extends Fragment {
    public static final String BASE_URL = urlServer;
    Retrofit retrofit= new Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build();

    Context context;
    ListView listView;
    Button button;

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



        return view;
    }
}