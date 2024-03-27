package com.example.gulliver;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.CheckBox;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import java.util.ArrayList;
import java.util.zip.Inflater;

public class TipologieGridAdapter extends ArrayAdapter<Tipologia> {

    Context context;
    int resource;

    public TipologieGridAdapter(@NonNull Context context, int resource, ArrayList<Tipologia> lista) {
        super(context, resource, lista);
        this.context = context;
        this.resource = resource;
    }


    static class TipologiaGridViewHolder {
        CheckBox checkBox;
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

            viewContent.setTag(holder);
        }

        TipologiaGridViewHolder holder = (TipologiaGridViewHolder) viewContent.getTag();
        Tipologia item = getItem(position);


        holder.checkBox.setText(String.valueOf(item.nome));

        return viewContent;
    }
}