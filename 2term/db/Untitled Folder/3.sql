USE CONTR
GO



SELECT Н.Товар_ID, SUM(Дд.Колво), SUM(Дд.Колво) * MIN(Н.Объем), SUM(Дд.Колво) * MIN(Н.Масса), SUM(Дд.Цена)
FROM Номенклатура as Н inner join Документы_данные as Дд on Н.Товар_ID = Дд.Товар_ID 
GROUP BY Н.Товар_ID
