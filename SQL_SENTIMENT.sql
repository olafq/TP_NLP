USE NLP 
CREATE TABLE Posts_twetter (
author nvarchar(255),
selftext nvarchar(255),
sentiment decimal(18,4),
analisis nvarchar(255),
)
create table Algo (
n nvarchar(255),
)
drop table Algo
select * from Algo
CREATE TABLE Posts_reddit (
title nvarchar(1000),
author nvarchar(255),
selftext nvarchar(1000),
sentiment decimal(18,4),
analisis nvarchar(255),
)
drop table Posts_reddit
GO
select * from Posts_reddit