package com.example.gulliver.ClassiModello;

import com.google.gson.annotations.SerializedName;

public class Tipologia {
    @SerializedName("id")
    public Integer id;
    @SerializedName("nome")
    public String nome;

    public Tipologia(Integer id, String nome) {
        this.id = id;
        this.nome = nome;
    }
}
