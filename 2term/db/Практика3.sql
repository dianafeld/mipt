SET dateformat dmy

USE Магазин
GO

--1
CREATE TABLE Товары(Товар_ID int primary key, Название nvarchar(max), Цена int)
CREATE TABLE Покупатели(Покупатель_ID int primary key, Покупатель nvarchar(max))
CREATE TABLE Чеки(нДок int primary key, Дата date, Покупатель_ID int, Сумма int)
CREATE TABLE Чеки_данные(нДок int, Товар_ID int, Цена int, Колво int, primary key(нДок, Товар_ID))

--2
INSERT INTO Покупатели
VALUES (1, 'Иванов'), (2, 'Петров'), (3, 'Smith')

INSERT INTO Товары
VALUES (1, 'Молоко', 50), (2, 'Масло', 20), (3, 'Хлеб', 17)

--3
INSERT INTO Чеки_данные
SELECT П.Покупатель_ID, Т.Товар_ID, Т.Цена, ABS(CHECKSUM(NEWID())) % 5 + 1
FROM Покупатели as П, Товары as Т


--4
INSERT INTO Чеки
SELECT Чд.нДок, GETDATE(), Чд.нДок, SUM(Чд.Цена * Чд.Колво)
FROM Чеки_данные as Чд
GROUP BY Чд.нДок

--5

UPDATE Чеки_данные
SET Цена = 1.5 * Цена
WHERE Товар_ID = (SELECT MIN(Товар_ID)
			FROM Чеки_данные)


SELECT *
FROM Чеки_данные
SELECT *
FROM Чеки

--6
UPDATE Чеки
SET Сумма = А.Сумма
FROM (SELECT Ч.нДок, SUM(Чд.Цена * Чд.Колво) as Сумма
	FROM Чеки as Ч inner join Чеки_данные as Чд on Ч.нДок = Чд.нДок
	GROUP BY Ч.нДок) as А
WHERE Чеки.нДок = А.нДок

SELECT *
FROM Чеки


--7
SELECT distinct П.Покупатель
FROM Покупатели as П inner join Чеки as Ч on П.Покупатель_ID = Ч.Покупатель_ID
WHERE Ч.Сумма > (SELECT AVG(Ч.Сумма)
				FROM Чеки as Ч
				WHERE MONTH(Ч.Дата) = '05' and YEAR(Ч.Дата) = '2013')

--8

INSERT INTO Покупатели
VALUES (4, 'Ford'), (5, 'Bellman')

INSERT INTO Чеки
VALUES (100, '12.05.13', 4, 600), (101, '12.05.13', 5, 600) 

DECLARE @T table(Покупатель_ID int, Покупатель nvarchar(max), Сумма int)

INSERT INTO @T
SELECT П.Покупатель_ID, П.Покупатель, SUM(Ч.Сумма)
FROM Покупатели as П inner join Чеки as Ч on П.Покупатель_ID = Ч.Покупатель_ID
WHERE MONTH(Ч.Дата) = '05' and YEAR(Ч.Дата) = '2013'
GROUP BY П.Покупатель_ID, П.Покупатель

SELECT *
FROM @T

SELECT T1.Покупатель_ID, T1.Покупатель, COUNT(*)
FROM @T as T1 inner join @T as T2 on T1.Сумма <= T2.Сумма
GROUP BY T1.Покупатель_ID, T1.Покупатель


DROP TABLE Товары
DROP TABLE Покупатели
DROP TABLE Чеки
DROP TABLE Чеки_данные