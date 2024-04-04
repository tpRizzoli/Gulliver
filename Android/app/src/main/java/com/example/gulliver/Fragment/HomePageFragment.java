package com.example.gulliver.Fragment;

import android.content.Context;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.GridView;
import android.widget.Toast;

import androidx.fragment.app.Fragment;

import com.example.gulliver.Activity.MainActivity;
import com.example.gulliver.R;
import com.example.gulliver.ClassiModello.Tipologia;
import com.example.gulliver.Adapter.TipologieAdapter;

import java.util.ArrayList;

public class HomePageFragment extends Fragment {

    Context ctx = null;
    GridView grigliaTipologie = null;
    TipologieAdapter tga = null;

    ArrayList<Tipologia> listaTipologie = new ArrayList<>();


    public HomePageFragment() {
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
        ctx = context;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {

        View view = inflater.inflate(R.layout.fragment_homepage, container, false);

        EditText nomePosto = view.findViewById(R.id.cNomeItinerario);
        Button btnCercaItinerario = view.findViewById(R.id.btnCercaItinerario);

        btnCercaItinerario.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String nomePostoText = nomePosto.getText().toString().trim();
                if (nomePostoText.isEmpty()) {
                    Toast.makeText(getActivity(), "Devi inserire il nome del posto", Toast.LENGTH_SHORT).show();
                } else if (nomePostoText.matches(".*\\d+.*")) {
                    // Il campo contiene numeri, mostra un messaggio di errore
                    Toast.makeText(getActivity(), "Inserisci il nome, non i numeri", Toast.LENGTH_SHORT).show();
                } else {
                    // Il campo non contiene numeri, puoi procedere con il cambio del fragment
                    Bundle extra = new Bundle();
                    extra.putString("nomeLuogo", nomePosto.getText().toString());

                    TipologieFragment tipologieFragment = new TipologieFragment();
                    ((MainActivity) ctx).changeFragment(tipologieFragment, extra);
                }
            }
        });


        Button btnMare = view.findViewById(R.id.imageMare);
        btnMare.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ItinerariSuggeritiFragment itinerariSuggeriti = new ItinerariSuggeritiFragment();

                Bundle extra = new Bundle();
                extra.putString("nomeCategoria", "Mare");

                ((MainActivity) ctx).changeFragment(itinerariSuggeriti, extra);
            }
        });

        Button btnMontagna = view.findViewById(R.id.imageMontagna);
        btnMontagna.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ItinerariSuggeritiFragment itinerariSuggeriti = new ItinerariSuggeritiFragment();

                Bundle extra = new Bundle();
                extra.putString("nomeCategoria", "Montagna");

                ((MainActivity) ctx).changeFragment(itinerariSuggeriti, extra);
            }
        });

        Button btnCitta = view.findViewById(R.id.imageCitta);
        btnCitta.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ItinerariSuggeritiFragment itinerariSuggeriti = new ItinerariSuggeritiFragment();

                Bundle extra = new Bundle();
                extra.putString("nomeCategoria", "Citta");

                ((MainActivity) ctx).changeFragment(itinerariSuggeriti, extra);
            }
        });

        return view;
    }
}
