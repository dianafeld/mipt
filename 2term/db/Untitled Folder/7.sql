/*SELECT *
FROM Номенклатура as Н left join Остатки as О on Н.Товар_ID = О.Товар_ID

SELECT Н.Товар_ID, SUM(О.Остаток)
FROM Номенклатура as Н left join Остатки as О on Н.Товар_ID = О.Товар_ID
GROUP BY Н.Товар_ID */

SELECT Н.Товар_ID 
FROM Номенклатура as Н left join Остатки as О on Н.Товар_ID = О.Товар_ID
GROUP BY Н.Товар_ID
HAVING isNULL(SUM(О.Остаток),0) < 5

