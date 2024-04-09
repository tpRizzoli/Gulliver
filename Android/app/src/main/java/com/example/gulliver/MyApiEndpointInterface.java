package com.example.gulliver;

import com.example.gulliver.ClassiModello.Attivita;

import com.example.gulliver.ClassiModello.AttivitaConLuogo;

import com.example.gulliver.ClassiModello.Itinerario;
import com.example.gulliver.ClassiModello.Tipologia;
import com.example.gulliver.ClassiModello.User;

import okhttp3.Response;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.DELETE;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.PUT;
import retrofit2.http.Path;
import retrofit2.http.Query;
import java.util.ArrayList;
import java.util.List;

public interface MyApiEndpointInterface {

    String urlServer = "http://192.168.0.137:5000";

    @GET("/api/getUser")
    Call<User> getUser(@Query("utente") String username, @Query("password") String password);

    @PUT("/api/modificaProfilo/{id}")
    Call<User> modificaProfilo(@Path("id")Integer id, @Query("username") String username, @Query("email") String email, @Query("password") String pwd);

    @POST("/api/createUser")
    Call<User> createUser(@Query("username") String username, @Query("email") String email, @Query("password") String password);

    @GET("/api/findTipologie")
    Call<ArrayList<Tipologia>> findTipologie(@Query("nomeLuogo") String nomeLuogo);

    @GET("/api/findItinerariUtente")
    Call<ArrayList<Itinerario>> findItinerariUtente(@Query("idUtente") Integer id);

    @GET("/api/findAttivitaTipologie")
    Call<ArrayList<Attivita>> findAttivitaFromTipologie(@Query("nomeLuogo") String nomeLuogo, @Query("idTipologia") List<Integer> idTipologia);

    @GET("/api/getDettagliAttivita")
    Call<ArrayList<AttivitaConLuogo>> findDettagliAttivita(@Query("idAttivita") ArrayList<Integer> idAttivita);

    @GET("/api/getDettagliItinerario")
    Call<ArrayList<AttivitaConLuogo>> findDettagliItinerario(@Query("idItinerario") Integer idItinerario);

    @POST("/api/createItinerario")
    Call<Itinerario> creaItinerario(@Query("idUtente") Integer idUtente, @Query("nomeItinerario") String nomeItinerario, @Query("idAttivita") ArrayList<Integer> idAttivita);

    @GET("/api/findItinerariSuggeriti")
    Call<ArrayList<Itinerario>> findItinerariSuggeriti(@Query("categoria") String nomeCategoria);

    @POST("/api/createItinerario")
    Call<Itinerario> associaItinerario(@Query("idUtente") Integer idUtente, @Query("idItinerario") Integer idItinerario);

    @DELETE("/api/eliminaItinerario")
    Call<String> eliminaItinerario(@Query("idUtente") Integer idUtente, @Query("idItinerario") Integer idItinerario);

}
