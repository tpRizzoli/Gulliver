package com.example.gulliver.Fragment;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.content.*;
import androidx.fragment.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;
import com.example.gulliver.Activity.LoginActivity;
import com.example.gulliver.Activity.MainActivity;
import com.example.gulliver.R;

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
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_profiloutente, container, false);

        TextView usernameText = view.findViewById(R.id.cUsername);
        TextView emailText = view.findViewById(R.id.cEmail);

        SharedPreferences sp = getActivity().getSharedPreferences(LoginActivity.MY_PREFERENCES, Context.MODE_PRIVATE);

        usernameText.setText(sp.getString(LoginActivity.USERNAME, null));
        emailText.setText(sp.getString(LoginActivity.EMAIL, null));

        Button btnModificaProfilo = view.findViewById(R.id.btnModificaProfilo);
        btnModificaProfilo.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ProfileEditFragment profileEditFragment = new ProfileEditFragment();
                ((MainActivity)ctx).changeFragment(profileEditFragment);
            }
        });

        Button btnLogout = view.findViewById(R.id.btnLogout);
        btnLogout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Crea un Intent per avviare l'Activity LoginActivity
                Intent intent = new Intent(getActivity(), LoginActivity.class);

                // Imposta i flag per terminare tutte le altre attività
                intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK | Intent.FLAG_ACTIVITY_NEW_TASK);

                SharedPreferences settings = requireContext().getSharedPreferences("loginUtente", Context.MODE_PRIVATE);
                settings.edit().clear().commit();

                // Avvia l'Activity utilizzando l'Intent
                startActivity(intent);
            }
        });
        return view;
    }
}
