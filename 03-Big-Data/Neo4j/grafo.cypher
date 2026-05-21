":begin
CREATE CONSTRAINT UNIQUE_IMPORT_NAME FOR (node:`UNIQUE IMPORT LABEL`) REQUIRE (node.`UNIQUE IMPORT ID`) IS UNIQUE;
:commit
CALL db.awaitIndexes(300);
:begin
UNWIND [{_id:0, properties:{name:"JoaquinSabina"}}, {_id:1, properties:{name:"Rusia2018"}}, {_id:2, properties:{name:"Argentina"}}, {_id:3, properties:{name:"Feliz Domingo"}}, {_id:4, properties:{name:"Messi"}}] AS row
CREATE (n:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row._id}) SET n += row.properties SET n:Trending;
:commit
:begin
UNWIND [{start: {_id:0}, end: {_id:3}, properties:{ntweet:52}}, {start: {_id:1}, end: {_id:2}, properties:{ntweet:73}}, {start: {_id:1}, end: {_id:3}, properties:{ntweet:183}}, {start: {_id:1}, end: {_id:4}, properties:{ntweet:65}}, {start: {_id:2}, end: {_id:1}, properties:{ntweet:73}}, {start: {_id:2}, end: {_id:4}, properties:{ntweet:112}}, {start: {_id:3}, end: {_id:0}, properties:{ntweet:52}}, {start: {_id:3}, end: {_id:1}, properties:{ntweet:183}}, {start: {_id:3}, end: {_id:4}, properties:{ntweet:81}}, {start: {_id:4}, end: {_id:1}, properties:{ntweet:65}}, {start: {_id:4}, end: {_id:2}, properties:{ntweet:112}}, {start: {_id:4}, end: {_id:3}, properties:{ntweet:81}}] AS row
MATCH (start:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.start._id})
MATCH (end:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.end._id})
CREATE (start)-[r:RELACION]->(end) SET r += row.properties;
:commit
:begin
MATCH (n:`UNIQUE IMPORT LABEL`)  WITH n LIMIT 20000 REMOVE n:`UNIQUE IMPORT LABEL` REMOVE n.`UNIQUE IMPORT ID`;
:commit
:begin
DROP CONSTRAINT UNIQUE_IMPORT_NAME;
:commit
"