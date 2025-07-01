create table if not exists users(
    id integer primary key autoincrement,
    name  text not null,
    email text unique not null check(email like '%@%.%'),
    password blob not null,
    is_admin INTEGER DEFAULT 0
);

create table if not exists cars(
    id integer primary key autoincrement,
    brand text not null,
    model text not null,
    price_per_day real not null,
    available integer default 1
);

create table if not exists bookings(
    id integer primary key autoincrement,
    user_id integer,
    car_id integer,
    start_date text,
    end_date text,
    total_cost real,
    foreign key(user_id) references users(id),
    foreign key(car_id) references cars(id)

);