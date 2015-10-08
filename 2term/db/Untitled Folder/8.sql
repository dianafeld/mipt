USE CONTR
GO

DECLARE @p int

SET @p = 1

UPDATE Остатки
SET Остаток = Остаток + 5
WHERE Код_склада = @p