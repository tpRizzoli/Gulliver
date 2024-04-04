package com.example.gulliver.ClassiModello;

import com.google.gson.annotations.SerializedName;

public class Itinerario {

    @SerializedName("id")
    public Integer id;
    @SerializedName("nome")
    public String nome;
    @SerializedName("default")
    public Integer sysDefault;

    public Itinerario(Integer id, String nome, Integer sysDefault) {
        this.id = id;
        this.nome = nome;
        this.sysDefault = sysDefault;
    }


}


