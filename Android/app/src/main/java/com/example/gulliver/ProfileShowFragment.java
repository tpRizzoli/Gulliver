package com.example.gulliver;

import android.content.Context;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;


public class ProfileShowFragment extends Fragment {

    Context ctx = null;

    public ProfileShowFragment() {
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
        ctx = context;
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
                ((MainActivity)ctx).changeFragment(profileEditFragment);
            }
        });

        return view;
    }
}
