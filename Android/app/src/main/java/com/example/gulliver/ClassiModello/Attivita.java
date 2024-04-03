package com.example.gulliver.ClassiModello;

import com.google.gson.annotations.SerializedName;

public class Attivita {
    @SerializedName("id")
    public Integer id;
    @SerializedName("nome")
    public String nome;
    @SerializedName("luogo")
    public String nomeLuogo;
    @SerializedName("difficolta")
    public Integer difficolta;
    @SerializedName("descrizione")
    public String descrizione;


    public Attivita(Integer id, String nome, String nomeLuogo, Integer difficolta, String descrizione) {
        this.id = id;
        this.nome = nome;
        this.descrizione = descrizione;
        this.difficolta = difficolta;
        this.nomeLuogo = nomeLuogo;
    }
}
