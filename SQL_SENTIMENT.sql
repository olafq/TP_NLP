USE NLP 
CREATE TABLE Sentimientos_Relacionados (
	fecha_de_analisis nvarchar(50),
	precio decimal(18,4),
	analisis nvarchar(255),
	fecha_a_predecir nvarchar(50),
	precio_cierre decimal(18,4),
)
create procedure cargar_tabla 
as begin 
select distinct * from Sentimientos_Relacionados
end 
go


declare @cargar_tabla int
exec @cargar_tabla = cargar_tabla
go

