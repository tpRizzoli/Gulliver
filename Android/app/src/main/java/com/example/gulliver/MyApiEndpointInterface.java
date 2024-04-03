package com.example.gulliver;

import com.example.gulliver.ClassiModello.Attivita;
import com.example.gulliver.ClassiModello.Itinerario;
import com.example.gulliver.ClassiModello.Tipologia;
import com.example.gulliver.ClassiModello.User;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.PUT;
import retrofit2.http.Path;
import retrofit2.http.Query;
import java.util.ArrayList;
import java.util.List;

public interface MyApiEndpointInterface {

    String urlServer = "http://192.168.0.137:5000";

    // GET http://api.myservice.com/users/francesca
    @GET("/getUser")
    Call<User> getUser(@Query("utente") String username, @Query("password") String password);

    @PUT("/modificaProfilo/{id}")
    Call<User> modificaProfilo(@Path("id")Integer id, @Query("username") String username, @Query("email") String email, @Query("password") String pwd);

    @POST("/createUser")
    Call<User> createUser(@Query("username") String username, @Query("email") String email, @Query("password") String password);

    @GET("/findTipologie")
    Call<ArrayList<Tipologia>> findTipologie(@Query("nomeLuogo") String nomeLuogo);

    @GET("/findItinerariUtente")
    Call<ArrayList<Itinerario>> findItinerariUtente(@Query("idUtente") Integer id);

    @GET("/findAttivitaTipologie")
    Call<ArrayList<Attivita>> findAttivitaFromTipologie(@Query("nomeLuogo") String nomeLuogo, @Query("idTipologia") List<Integer> idTipologia);
}
