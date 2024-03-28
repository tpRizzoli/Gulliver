package com.example.gulliver.ClassiModello;

import com.google.gson.annotations.SerializedName;

public class Attivita {
    @SerializedName("id")
    public Integer id;
    @SerializedName("nome")
    public String nome;
    @SerializedName("descrizione")
    public String descrizione;
    @SerializedName("difficolta")
    public Integer difficolta;
    @SerializedName("nomeLuogo")
    public String nomeLuogo;

    public Attivita(Integer id, String nome, String descrizione, Integer difficolta, String nomeLuogo) {
        this.id = id;
        this.nome = nome;
        this.descrizione = descrizione;
        this.difficolta = difficolta;
        this.nomeLuogo = nomeLuogo;
    }
}
