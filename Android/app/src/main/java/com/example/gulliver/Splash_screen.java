    package com.example.gulliver;

    import android.content.Context;
    import android.content.Intent;
    import android.content.SharedPreferences;
    import android.os.Bundle;
    import android.os.Handler;
    import android.view.WindowManager;
    import androidx.appcompat.app.AppCompatActivity;
    public class Splash_screen extends AppCompatActivity {
            private static final int SPLASH_DELAY = 2000; // Delay in milliseconds

            @Override
            protected void onCreate(Bundle savedInstanceState) {
                super.onCreate(savedInstanceState);
                getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
                setContentView(R.layout.splash_screen);

                new Handler().postDelayed(() -> {
                    Intent intent;
                    if (isUserLoggedIn()) {
                        intent = new Intent(Splash_screen.this, MainActivity.class);
                    } else {
                        intent = new Intent(Splash_screen.this, LoginActivity.class);
                    }
                    startActivity(intent);
                    finish();
                }, SPLASH_DELAY);
            }

            private boolean isUserLoggedIn() {
                SharedPreferences prefs = getSharedPreferences(LoginActivity.MY_PREFERENCES, Context.MODE_PRIVATE);
                return prefs.contains(LoginActivity.USERNAME_DATA_KEY) && prefs.contains(LoginActivity.PASSWORD_DATA_KEY);
            }
        }