create table if not exists users (
       id serial primary key,
       name text,
       email text unique,
       password text
       );

create table if not exists polls(
    poll_id serial primary key,
    u_id serial references users(id),
    question text,
    end_date date,
    end_time time
 );
 create table if not exists options(
    p_id serial references polls(poll_id),
    options text,
    votes int
 );
