package com.example.gulliver.Adapter;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Checkable;
import android.widget.CompoundButton;
import android.widget.RelativeLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.example.gulliver.ClassiModello.Attivita;
import com.example.gulliver.ClassiModello.Tipologia;
import com.example.gulliver.R;

import java.util.ArrayList;
import java.util.Collections;

public class AttivitaAdapter extends ArrayAdapter<Attivita>{

    Context context;
    int resource;
    private ArrayList<Tipologia> lista;
    private ArrayList<Boolean> checkedStates;

    public AttivitaAdapter(@NonNull Context context, int resource) {
        super(context, resource);
        this.context = context;
        this.resource = resource;
        this.lista = lista;

        checkedStates = new ArrayList<>(Collections.nCopies(lista.size(), false));
    }

    /*static class TipologiaGridViewHolder {
        CheckBox checkBox;
    }

    public void notifyDataSetChanged() {
        super.notifyDataSetChanged();

        checkedStates.clear();
        checkedStates = new ArrayList<>(Collections.nCopies(lista.size(), false));
    }*/

    public ArrayList<Tipologia> getAdapterList() {
        return lista;
    }

    class AttivitaViewHolder extends RelativeLayout implements Checkable{

        LayoutInflater inflater = LayoutInflater.from(context);
        View v = inflater.inflate(R.layout.attivita_list_item, this, true);

        TextView nome;
        TextView descrizione;
        TextView difficolta;
        TextView luogo;

        RelativeLayout layout;

        private Boolean checked;

        public AttivitaViewHolder(Context context) {
            super(context);


            nome = v.findViewById(R.id.nomeAttivita);
            descrizione = v.findViewById(R.id.descrizioneAttivita);
            difficolta = v.findViewById(R.id.difficoltaValore);
            luogo = v.findViewById(R.id.luogoValore);

            layout = v.findViewById(R.id.corniceLayout);

            checked = false;
        }

        @Override
        public void setChecked(boolean checked) {
            this.checked = checked;

            if(isChecked()){
                layout.setBackgroundResource(R.drawable.shape_backgroud_checked);
            }
            else{
                layout.setBackgroundResource(R.drawable.shape_background);
            }
        }

        @Override
        public boolean isChecked() {
            return checked;
        }

        @Override
        public void toggle() {
            this.checked = !checked;
        }

    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        View viewContent = convertView;

        if(convertView == null){
            LayoutInflater inflater = (LayoutInflater) context.getSystemService(context.LAYOUT_INFLATER_SERVICE);
            viewContent = inflater.inflate(resource, null);

            AttivitaAdapter.AttivitaViewHolder holder = new TipologieAdapter.TipologiaGridViewHolder();


            holder.checkBox.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
                @Override
                public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                    checkedStates.set(position, isChecked);
                }
            });

            viewContent.setTag(holder);
        }

        TipologieAdapter.TipologiaGridViewHolder holder = (TipologieAdapter.TipologiaGridViewHolder) viewContent.getTag();
        Attivita item = getItem(position);


        holder.checkBox.setText(String.valueOf(item.nome));

        return viewContent;
    }


}
