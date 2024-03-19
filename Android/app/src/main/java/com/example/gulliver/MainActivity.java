package com.example.gulliver;

import android.os.Bundle;
import android.view.MenuItem;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.fragment.app.Fragment;

import com.google.android.material.bottomnavigation.BottomNavigationView;

public class MainActivity extends AppCompatActivity
        implements BottomNavigationView
        .OnNavigationItemSelectedListener {

    BottomNavigationView bottomNavigationView;
    FirstFragment firstFragment = new FirstFragment();
    SecondFragment secondFragment = new SecondFragment();
    ThirdFragment thirdFragment = new ThirdFragment();


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        bottomNavigationView
                = findViewById(R.id.bottomNavigationView);

        bottomNavigationView
                .setOnNavigationItemSelectedListener(this);
        bottomNavigationView.setSelectedItemId(R.id.homePage);
    }

    @Override
    public boolean
    onNavigationItemSelected(MenuItem item) {
        Fragment frag = null;
        int id = item.getItemId();

        if (id == R.id.homePage)
            frag = firstFragment;

        if (id == R.id.itinerari)
            frag = secondFragment;

        if (id == R.id.profilo)
            frag = thirdFragment;

        assert frag != null;
        getSupportFragmentManager()
                .beginTransaction()
                .replace(R.id.flFragment, frag)
                .commit();
        return true;
    }
}
