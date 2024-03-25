package com.example.gulliver;

import android.content.Context;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import androidx.fragment.app.Fragment;

public class HomePageFragment extends Fragment {

    Context ctx = null;

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

        Button btnCercaItinerario = view.findViewById(R.id.btnCercaItinerario);
        btnCercaItinerario.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ItinerariFragment itinerariFragment = new ItinerariFragment();
                ((MainActivity) ctx).changeFragment(itinerariFragment);
            }
        });

        Button btnmare = view.findViewById(R.id.imageMare);
        btnmare.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ItMareFragment itMareFragment = new ItMareFragment();
                ((MainActivity) ctx).changeFragment(itMareFragment);
            }
        });

        Button btnmontagna = view.findViewById(R.id.imageMontagna);
        btnmontagna.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ItMontagnaFragment ItMontagnaFragment = new ItMontagnaFragment();
                ((MainActivity) ctx).changeFragment(ItMontagnaFragment);
            }
        });

        Button btncitta = view.findViewById(R.id.imageCitta);
        btncitta.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ItCittaFragment ItCittaFragment = new ItCittaFragment();
                ((MainActivity) ctx).changeFragment(ItCittaFragment);
            }
        });

        /*
        RecyclerView recyclerView = view.findViewById(R.id.recycler);
        ArrayList<String> arrayList = new ArrayList<>();

        // Add multiple images to arraylist.
        arrayList.add("");
        arrayList.add("");
        arrayList.add("");
        arrayList.add("");

        ImageAdapter adapter = new ImageAdapter(HomePageFragment.this, arrayList);
        recyclerView.setAdapter(adapter);

        adapter.setOnItemClickListener(new ImageAdapter.OnItemClickListener() {
            @Override
            public void onClick(ImageView imageView, String path) {
                // Do something like opening the image in new activity or showing it in full screen or something else.
            }
        });
        */

        return view;
    }
}
