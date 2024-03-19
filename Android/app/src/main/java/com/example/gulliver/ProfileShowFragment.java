package com.example.gulliver;

import android.os.Bundle;
import androidx.fragment.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;


public class ProfileShowFragment extends Fragment {

    public ProfileShowFragment() {
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_profiloutente, container, false);

        Button btnModificaProfilo = view.findViewById(R.id.btnModificaProfilo);
        btnModificaProfilo.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ProfileEditFragment profileEditFragment = new ProfileEditFragment();
                getParentFragmentManager().beginTransaction()
                        .replace(R.id.flFragment, profileEditFragment)
                        .addToBackStack(null) // Se desideri aggiungere al backstack
                        .commit();
            }
        });

        return view;
    }
}
