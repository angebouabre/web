INSERT INTO moniteur_carte VALUES(8,'b8_27_eb_a8_40_20','b8_27_eb_a8_40_20','Raspberry','b8:27:eb:a8:40:20','None','1','Down');
                                                                                                                         CREATE TABLE "moniteur_capteur" (
    "id" integer NOT NULL PRIMARY KEY,
    "slug" varchar(30) NOT NULL UNIQUE,
    "localisation" varchar(10) NOT NULL,
    "type_mesure" varchar(12),
    "nom_capteur" varchar(30) NOT NULL UNIQUE,
    "marque" varchar(30),
    "date_activation" datetime,
    "date_achat" date,
    "carte_id" integer NOT NULL REFERENCES "moniteur_carte" ("id")
);
CREATE INDEX "moniteur_capteur_1aa9815d" ON "moniteur_capteur" ("carte_id");
