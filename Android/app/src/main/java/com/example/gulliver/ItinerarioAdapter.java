package com.example.gulliver;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;

public class ItinerarioAdapter extends RecyclerView.Adapter<ItinerarioAdapter.ItinerarioViewHolder> {

    private ArrayList<Itinerario> itinerariList;
    private Context context;

    public ItinerarioAdapter(ArrayList<Itinerario> itinerariList, Context context) {
        this.itinerariList = itinerariList;
        this.context = context;
    }

    @NonNull
    @Override
    public ItinerarioViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.lista_itinerari, parent, false);
        return new ItinerarioViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ItinerarioViewHolder holder, int position) {
        Itinerario itinerario = itinerariList.get(position);
        holder.nomeTextView.setText(itinerario.getNome());
    }

    @Override
    public int getItemCount() {
        return itinerariList.size();
    }

    public static class ItinerarioViewHolder extends RecyclerView.ViewHolder {
        TextView nomeTextView;

        public ItinerarioViewHolder(@NonNull View itemView) {
            super(itemView);
            nomeTextView = itemView.findViewById(R.id.nomeTextView);
        }
    }
}
