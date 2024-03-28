package com.example.gulliver;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.CheckBox;
import android.widget.CompoundButton;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import java.util.ArrayList;
import java.util.Collections;

public class TipologieAdapter extends ArrayAdapter<Tipologia> {

    Context context;
    int resource;
    private ArrayList<Tipologia> lista;
    private ArrayList<Boolean> checkedStates;


    public TipologieAdapter(@NonNull Context context, int resource, ArrayList<Tipologia> lista) {
        super(context, resource, lista);
        this.context = context;
        this.resource = resource;
        this.lista = lista;

        checkedStates = new ArrayList<>(Collections.nCopies(lista.size(), false));
    }

    static class TipologiaGridViewHolder {
        CheckBox checkBox;
    }

    public ArrayList<Tipologia> getAdapterList() {
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

            TipologiaGridViewHolder holder = new TipologiaGridViewHolder();
            holder.checkBox = viewContent.findViewById(R.id.checkboxTipologia);

            holder.checkBox.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
                @Override
                public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                    checkedStates.set(position, isChecked);
                }
            });

            viewContent.setTag(holder);
        }

        TipologiaGridViewHolder holder = (TipologiaGridViewHolder) viewContent.getTag();
        Tipologia item = getItem(position);


        holder.checkBox.setText(String.valueOf(item.nome));

        return viewContent;
    }
}