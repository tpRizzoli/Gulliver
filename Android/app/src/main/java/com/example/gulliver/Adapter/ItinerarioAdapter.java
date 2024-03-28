package com.example.gulliver.Adapter;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.example.gulliver.ClassiModello.Itinerario;
import com.example.gulliver.R;

import java.util.ArrayList;

public class ItinerarioAdapter extends ArrayAdapter<Itinerario> {

    Context context;
    int resource;

    public ItinerarioAdapter(@NonNull Context context, int resource, ArrayList<Itinerario> lista) {
        super(context, resource, lista);
        this.context = context;
        this.resource = resource;
    }


    static class ItinerarioGridViewHolder {
        TextView textView;
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        View viewContent = convertView;

        if(convertView == null){
            LayoutInflater inflater = (LayoutInflater) context.getSystemService(context.LAYOUT_INFLATER_SERVICE);
            viewContent = inflater.inflate(resource, null);

            ItinerarioGridViewHolder holder = new ItinerarioGridViewHolder();
            holder.textView = viewContent.findViewById(R.id.nomeTextView);

            viewContent.setTag(holder);
        }

        ItinerarioGridViewHolder holder = (ItinerarioGridViewHolder) viewContent.getTag();
        Itinerario item = getItem(position);


        holder.textView.setText(String.valueOf(item.nome));

        return viewContent;
    }
}