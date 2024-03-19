package com.example.gulliver;

import android.content.Intent;
import android.os.Bundle;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import com.google.android.material.bottomnavigation.BottomNavigationView;

public class MainActivity extends AppCompatActivity
        implements BottomNavigationView.OnNavigationItemSelectedListener {

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
    public boolean
    onNavigationItemSelected(MenuItem item) {
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


        assert frag != null;
        getSupportFragmentManager()
                .beginTransaction()
                .replace(R.id.flFragment, frag)
                .commit();
        return true;
    }
}
