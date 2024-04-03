package com.example.gulliver.Adapter;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.example.gulliver.ClassiModello.Attivita;
import com.example.gulliver.ClassiModello.AttivitaConLuogo;
import com.example.gulliver.R;

import java.util.ArrayList;

public class AttivitaConLuogoAdapter extends ArrayAdapter<AttivitaConLuogo>{

    Context context;
    int resource;
    private ArrayList<AttivitaConLuogo> lista;

    public AttivitaConLuogoAdapter(@NonNull Context context, int resource, ArrayList<AttivitaConLuogo> lista) {
        super(context, resource, lista);
        this.context = context;
        this.resource = resource;
        this.lista = lista;
    }

    public static class ViewHolder {
        TextView nome;
        TextView descrizione;
        TextView difficolta;
        TextView luogo;
    }

    public ArrayList<AttivitaConLuogo> getAdapterList() {
        return lista;
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        View viewContent = convertView;

        if(convertView == null){
            LayoutInflater inflater = (LayoutInflater) context.getSystemService(context.LAYOUT_INFLATER_SERVICE);
            viewContent = inflater.inflate(resource, null);

            ViewHolder holder = new ViewHolder();

            holder.nome = viewContent.findViewById(R.id.nomeAttivita);
            holder.descrizione = viewContent.findViewById(R.id.descrizioneAttivita);
            holder.difficolta = viewContent.findViewById(R.id.difficoltaValore);
            holder.luogo = viewContent.findViewById(R.id.luogoValore);

            viewContent.setTag(holder);
        }

        AttivitaConLuogoAdapter.ViewHolder holder = (ViewHolder) viewContent.getTag();
        AttivitaConLuogo item = getItem(position);

        holder.nome.setText(String.valueOf(item.nomeAttivita));
        holder.descrizione.setText(String.valueOf(item.descrizioneAttivita));
        holder.difficolta.setText(String.valueOf(item.difficoltaAttivita));
        holder.luogo.setText(String.valueOf(item.nomeLuogo));

        return viewContent;
    }
}
