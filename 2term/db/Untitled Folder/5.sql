USE CONTR
GO

SET DATEFORMAT DMY

DECLARE @p int
SET @p = 1

SELECT COUNT(П.Покупатель_ID)
FROM Покупатели as П
WHERE П.Покупатель_ID not in 
	(SELECT П.Покупатель_ID
	FROM Покупатели as П left join Документы as Д on П.Покупатель_ID = Д.Покупатель_ID inner join Документы_данные as Дд on Д.ндок = Дд.ндок
	WHERE Дд.Товар_ID = @p and Д.Дата >= '01.04.12')
								

