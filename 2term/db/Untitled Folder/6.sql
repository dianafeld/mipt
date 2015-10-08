USE CONTR
GO

SET DATEFORMAT DMY

DECLARE @p int
SET @p = 1

SELECT distinct П.Покупатель_ID, О.Код_склада 
FROM Покупатели as П, Остатки as О
WHERE EXISTS(SELECT T.Остаток
		FROM Остатки as T
		WHERE T.Код_склада = О.Код_склада and T.Товар_ID = @p)
		and
		П.Покупатель_ID not in
		(SELECT T.Покупатель_ID
		FROM Покупатели as T left join Документы as Д on T.Покупатель_ID = Д.Покупатель_ID inner join Документы_данные as Дд on Д.ндок = Дд.ндок
		WHERE Дд.Товар_ID = @p and Д.Дата >= '01.04.12' and Дд.Код_склада = О.Код_склада)