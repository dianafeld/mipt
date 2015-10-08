USE CONTR
GO

SELECT О.Код_склада, SUM(Дд.Цена * Дд.Колво)
FROM Остатки as О inner join Документы_данные as Дд on О.Код_склада = Дд.Код_склада and О.Товар_ID = Дд.Товар_ID inner join Номенклатура as Н on Н.Товар_ID = Дд.Товар_ID 
WHERE Н.Цена between 10 and 30
GROUP BY О.Код_склада
HAVING О.Код_склада in (SELECT top 1 with ties О.Код_склада
						FROM Остатки as О inner join Номенклатура as Н on О.Товар_ID = Н.Товар_ID
						GROUP BY О.Код_склада, О.Товар_ID
						ORDER BY SUM(О.Остаток * Н.Цена))
