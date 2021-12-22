create table GROUP_TAG_EN (
    ID bigserial primary key,
    NAME text unique not null
);

create table PATTERN_EN (
    ID bigserial primary key,
    TEXT text not null,
    GROUP_TAG_ID bigint not null,
    constraint PATTERN_GROUP_TAG_ID foreign key (GROUP_TAG_ID) references GROUP_TAG(ID)
);

create table RESPONSE_EN (
    ID bigserial primary key,
    TEXT text not null,
    TYPE text not null,
    GROUP_TAG_ID bigint not null,
    constraint RESPONSE_GROUP_TAG_ID foreign key (GROUP_TAG_ID) references GROUP_TAG(ID)
);