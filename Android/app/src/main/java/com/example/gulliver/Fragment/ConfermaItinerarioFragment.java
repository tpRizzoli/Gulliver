package com.example.gulliver.Fragment;

import static com.example.gulliver.MyApiEndpointInterface.urlServer;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;

import com.example.gulliver.Activity.LoginActivity;
import com.example.gulliver.Activity.MainActivity;
import com.example.gulliver.Adapter.AttivitaConLuogoAdapter;
import com.example.gulliver.ClassiModello.AttivitaConLuogo;
import com.example.gulliver.ClassiModello.Itinerario;
import com.example.gulliver.MyApiEndpointInterface;
import com.example.gulliver.R;
import com.google.android.gms.maps.MapFragment;
import com.google.android.gms.maps.SupportMapFragment;

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

    FragmentManager fragmentManager;
    FragmentTransaction fragmentTransaction;
    SupportMapFragment mappa;

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

        fragmentManager = getChildFragmentManager();
        fragmentTransaction = fragmentManager.beginTransaction();
        mappa = SupportMapFragment.newInstance();

        fragmentTransaction.replace(R.id.map, mappa);
        fragmentTransaction.commit();


        AttivitaConLuogoAdapter adapter = new AttivitaConLuogoAdapter(context, R.layout.attivita_list_item_nocheckbox, dettagliAttivita);
        listaAttivita.setAdapter(adapter);

        Bundle extra = getArguments();

        ArrayList<Integer> idAttivitaScelte = extra.getIntegerArrayList("idAttivita");
        Integer idItinerario = extra.getInt("idItinerario");
        String nomeItinerario = extra.getString("nomeItinerario");

        if(idAttivitaScelte != null){
            // Creazione nuovo itinerario e collegamento con l'utente

            inserimentoNome.setEnabled(true);
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


            pulsanteAnnulla.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    HomePageFragment homePage = new HomePageFragment();
                    ((MainActivity) context).changeFragment(homePage);
                }
            });

            pulsanteConferma.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    String nomeItinerario = inserimentoNome.getText().toString();

                    if(nomeItinerario.equals("")){
                        Toast.makeText(context, "Devi prima scegliere un nome", Toast.LENGTH_SHORT).show();
                    }else{
                        SharedPreferences sp = getActivity().getSharedPreferences(LoginActivity.MY_PREFERENCES, Context.MODE_PRIVATE);
                        Integer idUtente = sp.getInt(LoginActivity.ID, -1);

                        if(idUtente != -1){
                            Call<Itinerario> creaItinerario = apiService.creaItinerario(idUtente, nomeItinerario, idAttivitaScelte);
                            creaItinerario.enqueue(new Callback<Itinerario>() {
                                @Override
                                public void onResponse(Call<Itinerario> call, Response<Itinerario> response) {
                                    Itinerario itinerarioCreato = response.body();

                                    ItinerariUtenteFragment riepilogoItinerari = new ItinerariUtenteFragment();
                                    ((MainActivity) context).changeFragment(riepilogoItinerari);
                                    Toast.makeText(context, "Itinerario creato con successo!", Toast.LENGTH_SHORT).show();
                                }

                                @Override
                                public void onFailure(Call<Itinerario> call, Throwable t) {
                                    Toast.makeText(context, "Impossibile creare l'itinerario", Toast.LENGTH_SHORT).show();
                                }
                            });
                        }
                    }
                }
            });
        } else {
            // Collegamento di un Itinerario con l'utente

            inserimentoNome.setEnabled(false);
            inserimentoNome.setText(nomeItinerario);

            Call recuperoDettagliItinerario = apiService.findDettagliItinerario(idItinerario);
            recuperoDettagliItinerario.enqueue(new Callback<ArrayList<AttivitaConLuogo>>() {
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


            pulsanteAnnulla.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    HomePageFragment homePage = new HomePageFragment();
                    ((MainActivity) context).changeFragment(homePage);
                }
            });

            pulsanteConferma.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    SharedPreferences sp = getActivity().getSharedPreferences(LoginActivity.MY_PREFERENCES, Context.MODE_PRIVATE);
                    Integer idUtente = sp.getInt(LoginActivity.ID, -1);

                    if(idUtente != -1){
                        Call<Itinerario> associaItinerario = apiService.associaItinerario(idUtente, idItinerario);
                        associaItinerario.enqueue(new Callback<Itinerario>() {
                            @Override
                            public void onResponse(Call<Itinerario> call, Response<Itinerario> response) {
                                Itinerario itinerarioCreato = response.body();

                                ItinerariUtenteFragment riepilogoItinerari = new ItinerariUtenteFragment();
                                ((MainActivity) context).changeFragment(riepilogoItinerari);
                                Toast.makeText(context, "Itinerario creato con successo!", Toast.LENGTH_SHORT).show();
                            }

                            @Override
                            public void onFailure(Call<Itinerario> call, Throwable t) {
                                Toast.makeText(context, "Impossibile creare l'itinerario", Toast.LENGTH_SHORT).show();
                            }
                        });
                    }

                }
            });
        }

        return view;
    }
}