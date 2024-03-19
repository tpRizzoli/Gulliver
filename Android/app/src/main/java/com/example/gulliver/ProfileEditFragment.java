package com.example.gulliver;

import android.os.Bundle;
import androidx.fragment.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;


public class ProfileEditFragment extends Fragment {

    public ProfileEditFragment() {
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_modificaprofilo, container, false);

        Button btnModificaProfilo = view.findViewById(R.id.btnAnnullaModfiche);
        btnModificaProfilo.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ProfileShowFragment profileShowFragment = new ProfileShowFragment();
                getParentFragmentManager().beginTransaction()
                        .replace(R.id.flFragment, profileShowFragment)
                        .addToBackStack(null) // Se desideri aggiungere al backstack
                        .commit();
            }
        });
        return view;
    }
}
