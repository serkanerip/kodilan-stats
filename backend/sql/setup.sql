create database kodilan_stats;
use kodilan_stats;

create table kodilan_posts
(
    id          bigint auto_increment primary key,
    slug        varchar(256) null,
    position    varchar(256) null,
    tags        varchar(256) null,
    location    varchar(256) null,
    company     varchar(256) null,
    created_at  datetime     null,
    description text         null
);

create table kodilan_tags
(
    tag varchar(250) not null,
    constraint kodilan_tags_tag_uindex
        unique (tag)
);

alter table kodilan_tags
    add primary key (tag);
