USE CONTR
GO

SELECT Код_склада, SUM(Остаток)
FROM Остатки
GROUP BY Код_склада