package com.example.gulliver;

import android.os.Bundle;
import android.view.MenuItem;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;

import com.google.android.material.bottomnavigation.BottomNavigationView;

public class MainActivity extends AppCompatActivity implements BottomNavigationView.OnNavigationItemSelectedListener {

    BottomNavigationView bottomNavigationView;
    HomePageFragment homePageFragment = new HomePageFragment();
    ItinerariFragment itinerariFragment = new ItinerariFragment();
    ProfileShowFragment profileShowFragment = new ProfileShowFragment();
    ProfileShowFragment profileEditFragment = new ProfileShowFragment();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        bottomNavigationView = findViewById(R.id.bottomNavigationView);
        bottomNavigationView.setOnNavigationItemSelectedListener(this);
        bottomNavigationView.setSelectedItemId(R.id.homePage);
    }

    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        Fragment frag = null;
        int id = item.getItemId();

        if (id == R.id.homePage)
            frag = homePageFragment;

        if (id == R.id.itinerari)
            frag = itinerariFragment;

        if (id == R.id.profilo)
            frag = profileShowFragment;

        if (id == R.id.btnModificaProfilo)
            frag = profileEditFragment;

        // Cambia il fragment in base alla selezione dell'utente
        changeFragment(frag);
        return true;
    }

    // Metodo per cambiare il fragment
    public void changeFragment(Fragment frag) {
        getSupportFragmentManager()
                .beginTransaction()
                .replace(R.id.flFragment, frag)
                .addToBackStack(null) // Aggiungi il fragment allo stack all'interno del back stack
                .commit();
    }

    // Sovrascrivi il metodo onBackPressed per gestire correttamente la gesture "indietro"
    @Override
    public void onBackPressed() {
        FragmentManager fragmentManager = getSupportFragmentManager();
        int count = fragmentManager.getBackStackEntryCount();

        if (count == 0) {
            super.onBackPressed();
        } else {
            // Se siamo nel fragment degli itinerari, torna al fragment dell'home page
            Fragment homeFragment = fragmentManager.findFragmentByTag("homePage");
            if (homeFragment != null && homeFragment.isVisible()) {
                super.onBackPressed();
            } else {
                // Torna al fragment dell'home page
                fragmentManager.popBackStack("homePage", FragmentManager.POP_BACK_STACK_INCLUSIVE);
                bottomNavigationView.setSelectedItemId(R.id.main); // Seleziona l'elemento corrispondente nel BottomNavigationView
            }
        }
    }
}
