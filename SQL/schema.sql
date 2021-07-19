create table if not exists users (
       id serial primary key,
       name text,
       email text unique,
       password text
       );