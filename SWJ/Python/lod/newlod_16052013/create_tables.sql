-- this table is a simplified 
create table temp as select su.naming as lemma, su.idusem, su.pos, st.template from usem su, usemtemplates sut, templates st  where su.idusem = sut.idusem and st.idtemplate=sut.idtemplate and su.naming is not null order by 1 asc 
-- main table
create table simple as SELECT s.lemma as source_lemma,s.idusem as source_usem, s.pos as source_pos,s.template as source_template,r.relation as relation, r.class as relation_type,t.lemma as target_lemma,t.idusem as target_usem, t.pos as target_pos,t.template as target_template FROM temp s, usemrel ur, relations r, temp t  where ur.idusem=s.idusem and r.idRsem=ur.idrsem and ur.idusemtarget=t.idusem 

--semantic vs lexical relations
CREATE TABLE simple_lexrelations as SELECT * FROM simple where relation_type in ('Polysemy','Metaphor','Synonym','Derivational','Antonym')
CREATE TABLE simple_semrelations as SELECT * FROM simple where relation_type not in ('Polysemy','Metaphor','Synonym','Derivational','Antonym')

-- lemmas which have both relation
create table common_lemmas as SELECT distinct lr.source_lemma FROM simple_lexrelations lr, simple_semrelations sr where lr.source_lemma=sr.source_lemma  order by 1 asc

-- onlylex
create table simple_onlylexrelations as SELECT lr.* FROM simple_lexrelations lr left outer join common_lemmas c on c.source_lemma = lr.source_lemma where c.source_lemma is  null;
--onlysem
create table simple_onlysemrelations as SELECT lr.* FROM simple_semrelations lr left outer join common_lemmas c on c.source_lemma = lr.source_lemma where c.source_lemma is  null;
--both
create table simple_bothrelations as SELECT lr.*, 'type' FROM simple_lexrelations lr,common_lemmas c where c.source_lemma = lr.source_lemma and 1=2;
-- insert values
insert into simple_bothrelations SELECT lr.*,'lex' FROM simple_lexrelations lr,common_lemmas c where c.source_lemma = lr.source_lemma 
union 
SELECT sr.*,'sem' FROM simple_semrelations sr,common_lemmas c where c.source_lemma = sr.source_lemma

-------
-- SELECT TO EXTRACT VALUES
------

--
--list of lemmas/usems used to map usems to lemma_sense#
--

-- create a file
SELECT distinct source_lemma as lemma, source_usem as idusem FROM simple 
UNION SELECT distinct target_lemma as lemma, target_usem as idusem FROM simple order by 1 asc
