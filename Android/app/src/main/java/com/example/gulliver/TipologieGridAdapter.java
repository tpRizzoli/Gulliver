package com.example.gulliver;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CheckBox;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;

public class TipologieGridAdapter extends RecyclerView.Adapter<TipologieGridAdapter.TipologieViewHolder> {

    private ArrayList<Tipologia> listaTipologie;

    public TipologieGridAdapter(ArrayList<Tipologia> listaTipologie) {
        this.listaTipologie = listaTipologie;
    }

    public class TipologieViewHolder extends RecyclerView.ViewHolder{

        private CheckBox checkBox;
        private TextView testoCheckbox;
        public TipologieViewHolder(@NonNull View itemView) {
            super(itemView);

            checkBox = itemView.findViewById(R.id.checkboxTipologia);
            testoCheckbox = itemView.findViewById(R.id.checkboxTipologia);
        }
    }

    @NonNull
    @Override
    public TipologieGridAdapter.TipologieViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {

        View itemView = LayoutInflater.from(parent.getContext()).inflate(R.layout.tipologie_grid_item, parent, false);
        return new TipologieViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull TipologieGridAdapter.TipologieViewHolder holder, int position) {

        String nome = listaTipologie.get(position).nome;
        holder.testoCheckbox.setText(nome);
    }

    @Override
    public int getItemCount() {
        return listaTipologie.size();
    }


}