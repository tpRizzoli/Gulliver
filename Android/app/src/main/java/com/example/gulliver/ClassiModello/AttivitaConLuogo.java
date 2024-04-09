package com.example.gulliver.ClassiModello;

import com.google.gson.annotations.SerializedName;

public class AttivitaConLuogo {
    @SerializedName("idAttivita")
    public Integer idAttivita;
    @SerializedName("nomeAttivita")
    public String nomeAttivita;
    @SerializedName("descrizioneAttivita")
    public String descrizioneAttivita;
    @SerializedName("difficoltaAttivita")
    public Integer difficoltaAttivita;
    @SerializedName("idLuogo")
    public Integer idLuogo;
    @SerializedName("nomeLuogo")
    public String nomeLuogo;
    @SerializedName("statoLuogo")
    public String statoLuogo;
    @SerializedName("latitudine")
    public Float latitudine;
    @SerializedName("longitudine")
    public Float longitudine;

    public AttivitaConLuogo(Integer idAttivita, String nomeAttivita, String descrizioneAttivita, Integer difficoltaAttivita, Integer idLuogo, String nomeLuogo, String statoLuogo, Float latitudine, Float longitudine) {
        this.idAttivita = idAttivita;
        this.nomeAttivita = nomeAttivita;
        this.descrizioneAttivita = descrizioneAttivita;
        this.difficoltaAttivita = difficoltaAttivita;
        this.idLuogo = idLuogo;
        this.nomeLuogo = nomeLuogo;
        this.statoLuogo = statoLuogo;
        this.latitudine = latitudine;
        this.longitudine = longitudine;
    }
}
