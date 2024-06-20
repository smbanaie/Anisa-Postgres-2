create table mvcctable 
(
idcol integer,
valcol char (255)
) with (autovacuum_enabled = off);

create index idx_mvcctable on mvcctable (idcol);
	