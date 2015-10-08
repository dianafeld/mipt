DECLARE @Города TABLE
(Город_ID int primary key, Название nvarchar(max), Область_ID int)

INSERT INTO @Города
VALUES (1, 'Москва', 1), (2, 'Калуга', 2), (3, 'Долгопрудный', 3), (4, 'Лобня', 3), (5, 'Химки', 3), (6, 'Обнинск', 2)

DECLARE @Области TABLE
(Область_ID int primary key, Область nvarchar(max))

INSERT INTO @Области
VALUES (1, 'Москва'), (2, 'Калужская область'), (3, 'Московская область')

DECLARE @Маршруты TABLE
(Город_ID_1 int, Город_ID_2 int, Расстояние int, primary key(Город_ID_1, Город_ID_2), check(Город_ID_1 < Город_ID_2))

INSERT INTO @Маршруты
VALUES (1, 2, 100), (1, 3, 20), (1, 4, 130), (1, 5, 10), (3, 4, 100), (3, 5, 200), (2, 6, 100), (3, 6, 10), (5, 6, 1), (4, 5, 40), (4, 6, 10)


--1
SELECT TOP 1 WITH TIES Г1.Название, Г2.Название
FROM @Маршруты as М inner join @Города as Г1 on М.Город_ID_1 = Г1.Город_ID inner join @Города as Г2 on М.Город_ID_2 = Г2.Город_ID
ORDER BY М.Расстояние

--2
SELECT TOP 1 WITH TIES Г1.Название, Г2.Название
FROM @Маршруты as М inner join @Города as Г1 on М.Город_ID_1 = Г1.Город_ID inner join @Города as Г2 on М.Город_ID_2 = Г2.Город_ID
WHERE Г1.Область_ID = Г2.Область_ID
ORDER BY М.Расстояние

--3
SELECT Г1.Название, Г2.Название
FROM @Города as Г1 inner join @Города as Г2 on Г1.Город_ID < Г2.Город_ID
WHERE NOT EXISTS (SELECT * 
					FROM @Маршруты as М
					WHERE М.Город_ID_1 = Г1.Город_ID and М.Город_ID_2 = Г2.Город_ID)
--4
DECLARE @Маршруты2 TABLE
(Город_ID_1 int, Город_ID_2 int, Расстояние int, primary key(Город_ID_1, Город_ID_2))

INSERT INTO @Маршруты2
SELECT *
FROM @Маршруты
UNION
SELECT М.Город_ID_2, М.Город_ID_1, М.Расстояние
FROM @Маршруты as М

SELECT distinct T.Город_ID_1, T.Город_ID_2
FROM 
(SELECT М1.Город_ID_1, М1.Город_ID_2
FROM @Маршруты as М1 inner join @Маршруты2 as М2 on М2.Город_ID_1 = М1.Город_ID_1 and М2.Город_ID_2 != М1.Город_ID_2 inner join @Маршруты2 as М3 on М3.Город_ID_1 = М2.Город_ID_2 and М3.Город_ID_2 = М1.Город_ID_2
WHERE М1.Расстояние > М2.Расстояние + М3.Расстояние) as T


/*SELECT distinct T.Город_ID_1, T.Город_ID_2
FROM
(SELECT М1.Город_ID_1, М1.Город_ID_2
FROM @Маршруты as М1 inner join @Маршруты as М2 on М2.Город_ID_1 = М1.Город_ID_1 and М2.Город_ID_2 != М1.Город_ID_2 inner join @Маршруты as М3 on М3.Город_ID_1 = М2.Город_ID_2 and М3.Город_ID_2 = М1.Город_ID_2
WHERE М1.Расстояние > М2.Расстояние + М3.Расстояние
UNION
SELECT М1.Город_ID_1, М1.Город_ID_2
FROM @Маршруты as М1 inner join @Маршруты as М2 on М2.Город_ID_2 = М1.Город_ID_1 and М2.Город_ID_1 != М1.Город_ID_1 inner join @Маршруты as М3 on М3.Город_ID_1 = М2.Город_ID_1 and М3.Город_ID_2 = М1.Город_ID_2
WHERE М1.Расстояние > М2.Расстояние + М3.Расстояние
UNION
SELECT М1.Город_ID_1, М1.Город_ID_2
FROM @Маршруты as М1 inner join @Маршруты as М2 on М2.Город_ID_1 = М1.Город_ID_1 and М2.Город_ID_2 != М1.Город_ID_2 inner join @Маршруты as М3 on М3.Город_ID_2 = М2.Город_ID_2 and М3.Город_ID_1 = М1.Город_ID_2
WHERE М1.Расстояние > М2.Расстояние + М3.Расстояние) as T*/
--5

DECLARE @Расписание TABLE
(Номер int primary key, Город_ID int)

INSERT INTO @Расписание
VALUES (1, 1), (2, 3), (3, 5), (4, 4), (5, 6)

DECLARE @Г TABLE
(Расстояние int)

INSERT INTO @Г
SELECT М.Расстояние 
		FROM (SELECT Р1.Город_ID as Г1, Р2.Город_ID as Г2
				FROM @Расписание as Р1 inner join @Расписание as Р2 on Р1.Номер + 1 = Р2.Номер) as T 
			left join @Маршруты2 as М on T.Г1 = М.Город_ID_1 and T.Г2 = М.Город_ID_2

IF NOT EXISTS(SELECT *
			FROM @Г
			WHERE Расстояние is NULL)
BEGIN
SELECT SUM(D.Расстояние)
FROM (SELECT М.Расстояние 
		FROM (SELECT Р1.Город_ID as Г1, Р2.Город_ID as Г2
				FROM @Расписание as Р1 inner join @Расписание as Р2 on Р1.Номер + 1 = Р2.Номер) as T 
			left join @Маршруты2 as М on T.Г1 = М.Город_ID_1 and T.Г2 = М.Город_ID_2) as D
END