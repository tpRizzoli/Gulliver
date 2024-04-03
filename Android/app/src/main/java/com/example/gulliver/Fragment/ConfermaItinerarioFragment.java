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
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;

import com.example.gulliver.Adapter.AttivitaConLuogoAdapter;
import com.example.gulliver.ClassiModello.AttivitaConLuogo;
import com.example.gulliver.MyApiEndpointInterface;
import com.example.gulliver.R;

import java.util.ArrayList;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class ConfermaItinerarioFragment extends Fragment {
    public static final String BASE_URL = urlServer;
    Retrofit retrofit= new Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build();

    MyApiEndpointInterface apiService = retrofit.create(MyApiEndpointInterface.class);

    Context context;

    EditText inserimentoNome;
    ListView listaAttivita;
    Button pulsanteConferma;
    Button pulsanteAnnulla;

    ArrayList<AttivitaConLuogo> dettagliAttivita = new ArrayList<>();

    @Override
    public void onAttach(@NonNull Context context) {
        super.onAttach(context);
        this.context = context;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_conferma_itinerario, container, false);

        inserimentoNome = view.findViewById(R.id.inserimentoNomeItinerario);
        listaAttivita = view.findViewById(R.id.listaAttivita);
        pulsanteConferma = view.findViewById(R.id.btnConferma);
        pulsanteAnnulla = view.findViewById(R.id.btnAnnulla);

        AttivitaConLuogoAdapter adapter = new AttivitaConLuogoAdapter(context, R.layout.attivita_list_item_nocheckbox, dettagliAttivita);
        listaAttivita.setAdapter(adapter);

        Bundle extra = getArguments();
        ArrayList<Integer> idAttivitaScelte = extra.getIntegerArrayList("idAttivita");

        Call recuperoDettagliAttivita = apiService.findDettagliAttivita(idAttivitaScelte);
        recuperoDettagliAttivita.enqueue(new Callback<ArrayList<AttivitaConLuogo>>() {

            @Override
            public void onResponse(Call<ArrayList<AttivitaConLuogo>> call, Response<ArrayList<AttivitaConLuogo>> response) {
                dettagliAttivita.clear();
                dettagliAttivita.addAll(response.body());
                adapter.notifyDataSetChanged();
                listaAttivita.invalidate();
            }

            @Override
            public void onFailure(Call<ArrayList<AttivitaConLuogo>> call, Throwable t) {
                Toast.makeText(context, "Impossibile caricare i dettagli", Toast.LENGTH_SHORT).show();
            }
        });


        return view;
    }
}