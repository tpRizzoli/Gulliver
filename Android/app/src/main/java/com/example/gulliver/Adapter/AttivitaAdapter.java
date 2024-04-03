package com.example.gulliver.Adapter;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.CheckBox;
import android.widget.Checkable;
import android.widget.CompoundButton;
import android.widget.RelativeLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.example.gulliver.ClassiModello.Attivita;
import com.example.gulliver.R;

import java.util.ArrayList;
import java.util.Collections;

public class AttivitaAdapter extends ArrayAdapter<Attivita>{

    Context context;
    int resource;
    private ArrayList<Attivita> lista;
    private ArrayList<Boolean> checkedStates;

    public AttivitaAdapter(@NonNull Context context, int resource, ArrayList<Attivita> lista) {
        super(context, resource, lista);
        this.context = context;
        this.resource = resource;
        this.lista = lista;

        checkedStates = new ArrayList<>(Collections.nCopies(lista.size(), false));
    }

    public static class AttivitaCliccabileViewHolder{
        TextView nome;
        TextView descrizione;
        TextView difficolta;
        TextView luogo;

        CheckBox checkBox;
    }

    public ArrayList<Attivita> getAdapterList() {
        return lista;
    }

    public ArrayList<Boolean> getCheckedStates() {
        return checkedStates;
    }

    @Override
    public void notifyDataSetChanged() {
        super.notifyDataSetChanged();

        checkedStates.clear();
        checkedStates = new ArrayList<>(Collections.nCopies(lista.size(), false));
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        View viewContent = convertView;

        if(convertView == null){
            LayoutInflater inflater = (LayoutInflater) context.getSystemService(context.LAYOUT_INFLATER_SERVICE);
            viewContent = inflater.inflate(resource, null);

            AttivitaCliccabileViewHolder holder = new AttivitaCliccabileViewHolder();

            holder.nome = viewContent.findViewById(R.id.nomeAttivita);
            holder.descrizione = viewContent.findViewById(R.id.descrizioneAttivita);
            holder.difficolta = viewContent.findViewById(R.id.difficoltaValore);
            holder.luogo = viewContent.findViewById(R.id.luogoValore);
            holder.checkBox = viewContent.findViewById(R.id.checkboxAttivita);

            holder.checkBox.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
                @Override
                public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                    checkedStates.set(position, isChecked);
                }
            });

            viewContent.setTag(holder);
        }

        AttivitaAdapter.AttivitaCliccabileViewHolder holder = (AttivitaCliccabileViewHolder) viewContent.getTag();
        Attivita item = getItem(position);

        holder.nome.setText(String.valueOf(item.nome));
        holder.descrizione.setText(String.valueOf(item.descrizione));
        holder.difficolta.setText(String.valueOf(item.difficolta));
        holder.luogo.setText(String.valueOf(item.nomeLuogo));

        return viewContent;
    }
}
