CREATE TABLE birds (
  `id` int(11) not null auto_increment,
  `common_name` text,
  `birdweb_url` text,
  `family_id` int,
  primary key (`id`)
);

insert into birds (`common_name`, `birdweb_url`, `family_id`) VALUES
  ('foo', 'bar', 1);

CREATE TABLE bird_images (
  id integer primary key auto_increment,
  contributor_name text,
  contributor_url text,
  src text
);

CREATE TABLE families (
  id integer primary key auto_increment,
  name text,
  short_name text
);

CREATE TABLE calls (
  id integer primary key auto_increment,
  bird_id int,
  url text
);