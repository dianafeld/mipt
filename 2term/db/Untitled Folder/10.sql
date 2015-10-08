USE CONTR 
GO

DECLARE @step int

SET @step = 10

DECLARE @T table(Товар_ID int, Цена_от int, Цена_до int)

INSERT INTO @T
SELECT Товар_ID, Цена - cast(Цена as int) % @step, Цена + @step - cast(Цена as int) % @step
FROM Номенклатура

SELECT Цена_от, Цена_до, COUNT(*)
FROM @T
GROUP BY Цена_от, Цена_до
