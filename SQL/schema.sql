create table if not exists users (
       id serial primary key,
       name text,
       email text unique,
       password text
       );

create table if not exists polls(
    u_id serial references users(id),
    question text,
    options text[]
 );