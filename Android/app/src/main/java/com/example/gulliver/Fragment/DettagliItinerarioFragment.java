package com.example.gulliver.Fragment;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;

import com.example.gulliver.Activity.MainActivity;
import com.example.gulliver.Adapter.AttivitaConLuogoAdapter;
import com.example.gulliver.ClassiModello.Attivita;
import com.example.gulliver.ClassiModello.AttivitaConLuogo;
import com.example.gulliver.ClassiModello.Itinerario;
import com.example.gulliver.MyApiEndpointInterface;
import com.example.gulliver.R;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
import retrofit2.converter.scalars.ScalarsConverterFactory;

public class DettagliItinerarioFragment extends Fragment {

    TextView nomeItinerario;
    ListView elencoAttivita;
    Button pulsanteElimina;

    Context context;

    AttivitaConLuogoAdapter adapter;

    protected final static String MY_PREFERENCES = "loginUtente";
    protected final static String ID = "idData";
    Retrofit retrofit;

    @Override
    public void onAttach(@NonNull Context context) {
        super.onAttach(context);
        this.context = context;
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_dettagli_itinerario, container, false);

        retrofit = new Retrofit.Builder()
                .baseUrl(MyApiEndpointInterface.urlServer)
                .addConverterFactory(ScalarsConverterFactory.create())
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        MyApiEndpointInterface apiService = retrofit.create(MyApiEndpointInterface.class);

        ArrayList<AttivitaConLuogo> listaAttivita = new ArrayList<>();

        nomeItinerario = view.findViewById(R.id.nomeItinerario);
        elencoAttivita = view.findViewById(R.id.listaAttivita);
        pulsanteElimina = view.findViewById(R.id.btnEliminaItinerario);


        adapter = new AttivitaConLuogoAdapter(context, R.layout.attivita_list_item_nocheckbox, listaAttivita);
        elencoAttivita.setAdapter(adapter);


        Bundle extra = getArguments();
        Integer idItinerario = extra.getInt("idItinerario");

        nomeItinerario.setText(extra.getString("nomeItinerario"));

        Call<ArrayList<AttivitaConLuogo>> call = apiService.findDettagliItinerario(idItinerario);

        call.enqueue(new Callback<ArrayList<AttivitaConLuogo>>() {
            @Override
            public void onResponse(Call<ArrayList<AttivitaConLuogo>> call, Response<ArrayList<AttivitaConLuogo>> response) {
                if (response.isSuccessful()) {
                    listaAttivita.clear();
                    listaAttivita.addAll(response.body());
                    adapter.notifyDataSetChanged();
                    elencoAttivita.invalidate();
                } else {
                    Toast.makeText(getActivity(), "Query Error", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<ArrayList<AttivitaConLuogo>> call, Throwable t) {
                Toast.makeText(getActivity(), "Connection error", Toast.LENGTH_SHORT).show();
            }
        });

        pulsanteElimina.setOnClickListener(new View.OnClickListener() {

            SharedPreferences sharedPreferences = getContext().getSharedPreferences(MY_PREFERENCES, Context.MODE_PRIVATE);
            Integer idUtente = sharedPreferences.getInt(ID, -1);

            @Override
            public void onClick(View v) {
                Call<String> eliminaItinerario = apiService.eliminaItinerario(idUtente, idItinerario);

                eliminaItinerario.enqueue(new Callback<String>() {
                    @Override
                    public void onResponse(Call<String> call, Response<String> response) {
                        if (response.isSuccessful()) {
                            String res = response.body().toString();
                            if (res.equals("Itinerario eliminato!")) {
                                Toast.makeText(context, "Itinerario eliminato", Toast.LENGTH_SHORT).show();
                                ItinerariUtenteFragment iuFrag = new ItinerariUtenteFragment();
                                ((MainActivity) context).changeFragment(iuFrag);
                            }
                        } else {
                            try {
                                String errorBody = response.errorBody().string();
                                Toast.makeText(context, errorBody, Toast.LENGTH_SHORT).show();
                            } catch (Exception e) {
                                e.printStackTrace();
                            }
                        }
                    }

                    @Override
                    public void onFailure(Call<String> call, Throwable t) {
                        Toast.makeText(getActivity(), "Connection error", Toast.LENGTH_SHORT).show();
                    }
                });
            }
        });

        return view;
    }
}

