DROP TABLE IF EXISTS "Films";
DROP TABLE IF EXISTS "People";
DROP TABLE IF EXISTS "Planets";
DROP TABLE IF EXISTS "Species";
DROP TABLE IF EXISTS "Starships";
DROP TABLE IF EXISTS "Vehicles";
DROP TABLE IF EXISTS "films_planets";
DROP TABLE IF EXISTS "films_species";
DROP TABLE IF EXISTS "films_starships";
DROP TABLE IF EXISTS "films_vehicles";
DROP TABLE IF EXISTS "films_people";
DROP TABLE IF EXISTS "people_vehicles";
DROP TABLE IF EXISTS "people_starships";

CREATE TABLE "Films" (
	"id"	INTEGER,
	"title"	TEXT,
	"episode_id"	INTEGER,
	"opening_crawl"	TEXT,
	"director"	TEXT,
	"producer"	TEXT,
	"release_date"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "People" (
	"id"	INTEGER,
	"name"	TEXT UNIQUE,
	"height"	TEXT,
	"mass"	TEXT,
	"hair_color"	TEXT,
	"skin_color"	TEXT,
	"eye_color"	TEXT,
	"birth_year"	TEXT,
	"gender"	TEXT,
	"homeworld"	INTEGER,
	"species"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("species") REFERENCES "Species"("id"),
	FOREIGN KEY("homeworld") REFERENCES "Planets"("id")
);

CREATE TABLE "Planets" (
	"id"	INTEGER,
	"name"	TEXT,
	"rotation_period"	TEXT,
	"orbital_period"	TEXT,
	"diameter"	TEXT,
	"climate"	TEXT,
	"gravity"	TEXT,
	"terrain"	TEXT,
	"surface_water"	TEXT,
	"population"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "Species" (
	"id"	INTEGER,
	"name"	TEXT,
	"classification"	TEXT,
	"designation"	TEXT,
	"average_height"	TEXT,
	"skin_colors"	TEXT,
	"hair_colors"	TEXT,
	"eye_colors"	TEXT,
	"average_lifespan"	TEXT,
	"homeworld"	INTEGER,
	"language"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("homeworld") REFERENCES "Planets"("id")
);

CREATE TABLE "Starships" (
	"id"	INTEGER,
	"name"	TEXT,
	"model"	TEXT,
	"manufacturer"	TEXT,
	"cost_in_credits"	TEXT,
	"length"	TEXT,
	"max_atmosphering_speed"	TEXT,
	"crew"	TEXT,
	"passengers"	TEXT,
	"cargo_capacity"	TEXT,
	"consumables"	TEXT,
	"hyperdrive_rating"	TEXT,
	"MGLT"	TEXT,
	"starship_class"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "Vehicles" (
	"id"	INTEGER,
	"name"	TEXT,
	"model"	TEXT,
	"manufacturer"	TEXT,
	"cost_in_credits"	TEXT,
	"length"	TEXT,
	"max_atmosphering_speed"	TEXT,
	"crew"	TEXT,
	"passengers"	TEXT,
	"cargo_capacity"	TEXT,
	"consumables"	TEXT,
	"vehicle_class"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "films_planets" (
	"id"	INTEGER,
	"id_films"	INTEGER,
	"id_planets"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_planets") REFERENCES "Planets"("id"),
	FOREIGN KEY("id_films") REFERENCES "Films"("id")
);

CREATE TABLE "films_species" (
	"id"	INTEGER,
	"id_films"	INTEGER,
	"id_species"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_films") REFERENCES "Films"("id"),
	FOREIGN KEY("id_species") REFERENCES "Species"("id")
);

CREATE TABLE "films_starships" (
	"id"	INTEGER,
	"id_films"	INTEGER,
	"id_starships"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_starships") REFERENCES "Starships"("id"),
	FOREIGN KEY("id_films") REFERENCES "Films"("id")
);

CREATE TABLE "films_vehicles" (
	"id"	INTEGER,
	"id_films"	INTEGER,
	"id_vehicles"	INTEGER,
	FOREIGN KEY("id_films") REFERENCES "Films"("id"),
	FOREIGN KEY("id_vehicles") REFERENCES "Vehicles"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "films_people" (
	"id"	INTEGER,
	"id_films"	INTEGER,
	"id_people"	INTEGER,
	FOREIGN KEY("id_films") REFERENCES "Films"("id"),
	FOREIGN KEY("id_people") REFERENCES "People"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "people_starships" (
	"id"	INTEGER,
	"id_people"	INTEGER,
	"id_starships"	INTEGER,
	FOREIGN KEY("id_people") REFERENCES "People"("id"),
	FOREIGN KEY("id_starships") REFERENCES "Starships"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "people_vehicles" (
	"id"	INTEGER,
	"id_people"	INTEGER,
	"id_vehicles"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_people") REFERENCES "People"("id"),
	FOREIGN KEY("id_vehicles") REFERENCES "Vehicles"("id")
);