drop database gulliver;

create database if not exists Gulliver;
use Gulliver;

create table utenti (
	ID int primary key auto_increment,
    username varchar(50),
    email varchar(50),
    pwd varchar(50)
) engine InnoDB;

create table itinerari (
	ID int primary key auto_increment,
    nome varchar(100),
    sysDefault int default 0
) engine InnoDB;

create table tipologie (
	ID int primary key auto_increment,
    nome varchar(100)
) engine InnoDB;    

create table attivita (
	ID int primary key auto_increment,
    nome varchar(100),
    difficolta int,
    id_tipologia int,
    constraint fk_attivita_tipologie
    foreign key (id_tipologia)
    references tipologie(ID),
    descrizione varchar(254)
) engine InnoDB;

create table categorie (
	ID int primary key auto_increment,
    nome varchar(100)
) engine InnoDB;    

create table luoghi (
	ID int primary key auto_increment,
    nome varchar(100),
    stato varchar(50),
    longitudine float,
    latitudine float
) engine InnoDB;


create table utenti_itinerari (
	ID int primary key auto_increment,
	id_utente int,
    id_itinerario int,
	constraint fk_utenti_itinerari_utenti
    foreign key (id_utente)
    references utenti(ID), 
    constraint fk_utenti_itinerari_itinerari
    foreign key (id_itinerario)
    references itinerari(ID)
) engine InnoDB;    

create table attivita_itinerari (
	ID int primary key auto_increment,
	id_attivita int,
    id_itinerario int,
	constraint fk_attivita_itinerari_attivita
    foreign key (id_attivita)
    references attivita(ID), 
    constraint fk_attivita_itinerari_itinerari
    foreign key (id_itinerario)
    references itinerari(ID)
) engine InnoDB;

create table attivita_luoghi (
	ID int primary key auto_increment,
	id_attivita int,
    id_luogo int,
	constraint fk_attivita_luoghi_attivita
    foreign key (id_attivita)
    references attivita(ID), 
    constraint fk_attivita_luoghi_luoghi
    foreign key (id_luogo)
    references luoghi(ID)
) engine InnoDB;  

 create table luoghi_categorie (
	ID int primary key auto_increment,
	id_luogo int,
    id_categoria int,
	constraint fk_luoghi_categorie_luoghi
    foreign key (id_luogo)
    references luoghi(ID), 
    constraint fk_luoghi_categorie_categorie
    foreign key (id_categoria)
    references categorie(ID)
) engine InnoDB;  
    