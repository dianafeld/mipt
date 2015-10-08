USE CONTR
GO

DECLARE @p float

SET @p = 0.5

SELECT distinct Масса
FROM Номенклатура
WHERE Объем > @p

