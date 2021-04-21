CREATE TABLE "user"(
	identifier numeric primary key,
	access_code text not null,
	recovery_code text not null,
	first_name text not null,
	last_name text not null,
	department text not null,
	location text not null
);

insert into "user" (identifier,access_code,recovery_code,first_name,last_name,department,location)values(9012,'12se74','rb9012','Rachel','Booker','Sales','Manchester');
insert into "user" (identifier,access_code,recovery_code,first_name,last_name,department,location)values(2070,'04ap67','lg2070','Laura','Grey','Depot','London');
insert into "user" (identifier,access_code,recovery_code,first_name,last_name,department,location)values(4081,'30no86','cj4081','Craig','Johnson','Depot','London');
insert into "user" (identifier,access_code,recovery_code,first_name,last_name,department,location)values(9346,'14ju73','mj9346','Mary','Jenkins','Engineering','Manchester');
insert into "user" (identifier,access_code,recovery_code,first_name,last_name,department,location)values(5079,'09ja61','js5079','Jamie','Smith','Engineering','Manchester');
