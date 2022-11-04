USE NLP 
CREATE TABLE Sentimiento_Relacionado (
	fecha_de_analisis nvarchar(50),
	analisis nvarchar(255),
	fecha_a_predecir nvarchar(50),
	precio_open decimal(18,4),
)
create procedure cargar_tabla 
as begin 
select distinct * from Sentimiento_Relacionado
end 
go
--Migra los compra producto (devuelve 0 si esta todo ok)
declare @cargar_tabla int
exec @cargar_tabla = cargar_tabla
go

