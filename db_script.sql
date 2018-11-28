create table contact
(
  id      integer,
  subject text not null,
  email   text not null,
  message text not null,
  primary key (id autoincrement)
);

create table items
(
  id                  integer,
  product_upc         int   default 0000000000 not null,
  product_name        text not null,
  cost                float default 0.00 not null,
  product_description text,
  primary key (id autoincrement)
);

create table promo_codes
(
  id         integer,
  value      float default 0.0 not null,
  value_type text  default 'dollars' not null,
  start_date datetime not null,
  end_date   datetime not null,
  code_name  text     not null,
  primary key (id autoincrement)
);

create unique index promo_codes_code_name_uindex
  on promo_codes (code_name);

create table users
(
  username text,
  password text,
  email    text,
  id       int,
  primary key (username)
);

create table cart
(
  id            integer,
  user_id       int not null,
  item_id       int not null,
  quantity      int      default 0 not null,
  promo_id      int      default 0 not null,
  created_time  datetime default '1970-01-01T00:00:00+0000' not null,
  modified_time datetime default '1970-01-01T00:00:00+0000' not null,
  primary key (id autoincrement),
  constraint cart_items_id_fk
  foreign key (item_id) references items,
  constraint cart_promo_codes_id_fk
  foreign key (promo_id) references promo_codes,
  constraint cart_users_id_fk
  foreign key (user_id) references users (id)
    on delete cascade
);

CREATE TRIGGER update_modified_time
  AFTER UPDATE
  ON cart
  FOR EACH ROW
BEGIN
  UPDATE cart
  SET modified_time = strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
  WHERE id = old.id;
end;

CREATE TRIGGER create_created_time
    AFTER INSERT
    ON cart
    FOR EACH ROW
BEGIN
    UPDATE cart
    SET created_time = strftime('%Y-%m-%dT%H:%M:%fZ','now')
    WHERE id = new.id;
end;

create unique index users_email_uindex
  on users (email);

create unique index users_id_uindex
  on users (id);


REPLACE INTO promo_codes SET value = 0, value_type = 'items', start_date = '1970-01-01T00:00:00+0000', end_date = '1970-01-01T00:00:00+0000', code_name = 'ITEM' WHERE id = 0;
REPLACE INTO items SET product_upc = 0, product_name = 'PROMO_CODE', cost = 0, product_description = 'promo code' WHERE id = 0;
INSERT INTO cart (id, user_id, item_id, quantity, promo_id, created_time, modified_time) VALUES (1, 1, 2, 2, 0, '2018-11-22T03:15:02.672Z', '2018-11-22T03:18:50.497Z');
INSERT INTO cart (id, user_id, item_id, quantity, promo_id, created_time, modified_time) VALUES (2, 2, 1, 3, 0, '2018-11-22T01:51:40.930Z', '2018-11-22T03:18:50.504Z');
INSERT INTO cart (id, user_id, item_id, quantity, promo_id, created_time, modified_time) VALUES (3, 1, 1, 3, 0, '2018-11-22T01:57:09.466Z', '2018-11-22T02:12:30.092Z');
INSERT INTO users (username, password, email, id) VALUES ('chris', 'P@ssw0rd', 'chris@cfedun.com', 1);
INSERT INTO users (username, password, email, id) VALUES ('frit', 'p4ssw0rd', 'matt@frit.me', 2);
INSERT INTO items (id, product_upc, product_name, cost, product_description) VALUES (0, 0, 'PROMO_CODE', 0, 'promo code');
INSERT INTO items (id, product_upc, product_name, cost, product_description) VALUES (1, 0, 'Item 1', 5, 'first item');
INSERT INTO items (id, product_upc, product_name, cost, product_description) VALUES (2, 0, 'Item 2', 10, 'Second item');
INSERT INTO promo_codes (id, value, value_type, start_date, end_date, code_name) VALUES (0, 0, 'items', '1970-01-01T00:00:00+0000', '1970-01-01T00:00:00+0000', 'ITEM');
INSERT INTO promo_codes (id, value, value_type, start_date, end_date, code_name) VALUES (1, 5, 'dollars', '2018-11-22T01:51:40.930Z', '2018-11-22T01:51:40.930Z', 'EXAMPLECODE');