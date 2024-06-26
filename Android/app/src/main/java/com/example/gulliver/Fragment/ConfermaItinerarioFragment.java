package com.example.gulliver.Fragment;


import static com.example.gulliver.MyApiEndpointInterface.urlServer;

import android.app.Activity;
import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;

import androidx.annotation.IntegerRes;
import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
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
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapFragment;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.model.CameraPosition;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;

import java.util.ArrayList;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class ConfermaItinerarioFragment extends Fragment implements OnMapReadyCallback {
    public static final String BASE_URL = urlServer;
    Retrofit retrofit= new Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build();

    MyApiEndpointInterface apiService = retrofit.create(MyApiEndpointInterface.class);

    static View view = null;
    Context context;

    EditText inserimentoNome;
    ListView listaAttivita;
    Button pulsanteConferma;
    Button pulsanteAnnulla;

    GoogleMap googleMap;

    String nomeItinerario;

    LatLng marker;

    ArrayList<AttivitaConLuogo> dettagliAttivita = new ArrayList<>();

    @Override
    public void onAttach(@NonNull Context context) {
        super.onAttach(context);
        this.context = context;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {

        //if(view == null)
            view = inflater.inflate(R.layout.fragment_conferma_itinerario, container, false);

        inserimentoNome = view.findViewById(R.id.inserimentoNomeItinerario);
        listaAttivita = view.findViewById(R.id.listaAttivita);
        pulsanteConferma = view.findViewById(R.id.btnConferma);
        pulsanteAnnulla = view.findViewById(R.id.btnAnnulla);

        AttivitaConLuogoAdapter adapter = new AttivitaConLuogoAdapter(context, R.layout.attivita_list_item_nocheckbox, dettagliAttivita);
        listaAttivita.setAdapter(adapter);

        Bundle extra = getArguments();

        ArrayList<Integer> idAttivitaScelte = extra.getIntegerArrayList("idAttivita");
        Integer idItinerario = extra.getInt("idItinerario");
        nomeItinerario = extra.getString("nomeItinerario");

        Call recuperoDettagli = null;

        if (idAttivitaScelte != null) {
            inserimentoNome.setEnabled(true);
            inserimentoNome.setText("");
            recuperoDettagli = apiService.findDettagliAttivita(idAttivitaScelte);
        }else {
            inserimentoNome.setEnabled(false);
            inserimentoNome.setText(nomeItinerario);
            recuperoDettagli = apiService.findDettagliItinerario(idItinerario);
        }

        recuperoDettagli.enqueue(new Callback<ArrayList<AttivitaConLuogo>>() {
            @Override
            public void onResponse(Call<ArrayList<AttivitaConLuogo>> call, Response<ArrayList<AttivitaConLuogo>> response) {
                dettagliAttivita.clear();
                dettagliAttivita.addAll(response.body());
                adapter.notifyDataSetChanged();
                listaAttivita.invalidate();

                changeMarker(0);
            }

            @Override
            public void onFailure(Call<ArrayList<AttivitaConLuogo>> call, Throwable t) {
                Toast.makeText(context, "Impossibile caricare i dettagli", Toast.LENGTH_SHORT).show();
            }
        });

        listaAttivita.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                int p = position;
                changeMarker(position);
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

                if(nomeItinerario == null || nomeItinerario.equals("")){
                    nomeItinerario = inserimentoNome.getText().toString();
                }

                if(nomeItinerario.equals("")){
                    Toast.makeText(context, "Inserire un nome!", Toast.LENGTH_SHORT).show();

                } else if (idAttivitaScelte != null) {
                    creaNuovoItinerario(idUtente, nomeItinerario, idAttivitaScelte);

                }else {
                    associaItinerarioEsistente(idUtente, idItinerario);

                }

            }
        });


        return view;
    }

    private void creaNuovoItinerario(Integer idUtente, String nomeItinerario, ArrayList<Integer> idAttivita){
        if(idUtente != -1){
            Call<Itinerario> creaItinerario = apiService.creaItinerario(idUtente, nomeItinerario, idAttivita);
            creaItinerario.enqueue(new Callback<Itinerario>() {
                @Override
                public void onResponse(Call<Itinerario> call, Response<Itinerario> response) {

                    if(response.isSuccessful()){
                        ItinerariUtenteFragment riepilogoItinerari = new ItinerariUtenteFragment();
                        ((MainActivity) context).changeFragment(riepilogoItinerari);
                        Toast.makeText(context, "Itinerario creato con successo!", Toast.LENGTH_SHORT).show();

                    }
                }

                @Override
                public void onFailure(Call<Itinerario> call, Throwable t) {
                    Toast.makeText(context, "Impossibile creare l'itinerario", Toast.LENGTH_SHORT).show();
                }
            });
        }
    }

    private void associaItinerarioEsistente(Integer idUtente, Integer idItinerario){

        if(idUtente != -1){
            Call<Itinerario> associaItinerario = apiService.associaItinerario(idUtente, idItinerario);
            associaItinerario.enqueue(new Callback<Itinerario>() {
                @Override
                public void onResponse(Call<Itinerario> call, Response<Itinerario> response) {
                    if(response.isSuccessful()){
                        ItinerariUtenteFragment riepilogoItinerari = new ItinerariUtenteFragment();
                        ((MainActivity) context).changeFragment(riepilogoItinerari);
                        Toast.makeText(context, "Itinerario creato con successo!", Toast.LENGTH_SHORT).show();
                    }
                }

                @Override
                public void onFailure(Call<Itinerario> call, Throwable t) {
                    Toast.makeText(context, "Impossibile registrare l'itinerario", Toast.LENGTH_SHORT).show();
                }
            });
        }
    }

    private void initilizeMap() {
        MapFragment mapFragment = null;

        if (googleMap == null) {
            mapFragment = ((MapFragment) ((Activity)context).getFragmentManager().findFragmentById(R.id.mapConferma));
            mapFragment.getMapAsync(this);
        }
    }

    @Override
    public void onResume() {
        super.onResume();

        initilizeMap();
    }
    @Override
    public  void  onMapReady(GoogleMap  googleMap)  {
        this.googleMap  =  googleMap;

        googleMap.setMapType(GoogleMap.MAP_TYPE_HYBRID);

    }

    private void changeMarker(Integer position) {
        if (googleMap != null) {
            googleMap.clear();
            AttivitaConLuogo attivita = dettagliAttivita.get(position);

            marker = new LatLng(attivita.latitudine, attivita.longitudine);
            googleMap.addMarker(new MarkerOptions().position(marker).title(attivita.nomeAttivita));

            CameraPosition cameraPosition = new CameraPosition.Builder().target(marker).zoom(17).build();
            googleMap.animateCamera(CameraUpdateFactory.newCameraPosition(cameraPosition));
        }
    }

}