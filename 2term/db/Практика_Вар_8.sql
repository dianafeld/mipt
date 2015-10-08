SET dateformat dmy

DECLARE @Сотрудники TABLE
(Сотрудник_ID int primary key, ФИО varchar(50))

INSERT INTO @Сотрудники
VALUES (1, 'А'), (2, 'Б'), (3, 'В'), (4, 'Г')

DECLARE @Проекты TABLE
(Проект_ID int primary key, Название varchar(50))

INSERT INTO @Проекты
VALUES (1, 'москва1'), (2, 'москва'), (3, 'Москва'), (4, 'Париж'), (5, 'Проект')

DECLARE @Работы TABLE
(Проект_ID int, Сотрудник_ID int, Начало date, Конец date)

INSERT INTO @Работы
VALUES (1, 1, '01.04.2013', NULL), (1, 2, '01.04.2013', '04.04.2013'), (2, 2, '01.04.2013', '04.04.2013'), (1, 2, '02.04.2013', '04.04.2013'), (3, 2, '02.04.2012', '04.04.2012'), (4, 1, '01.04.2012', '04.04.2012')

--1 
SELECT COUNT(*)
FROM @Проекты
WHERE Название not like '%москва%'

--2
SELECT П.*, Р.Начало, COUNT(distinct Р.Сотрудник_ID)
FROM @Проекты as П inner join @Работы as Р on П.Проект_ID = Р.Проект_ID
GROUP BY П.Проект_ID, П.Название, Р.Начало
ORDER BY П.Проект_ID, Р.Начало

--3

SELECT П.*, COUNT(distinct Р.Сотрудник_ID) as S
FROM @Проекты as П
left join @Работы as Р
on П.Проект_ID = Р.Проект_ID
GROUP BY П.Проект_ID, П.Название


SELECT TOP 1 WITH TIES *
FROM (SELECT П.Проект_ID as ID, П.Название, COUNT(distinct Р.Сотрудник_ID) as S
	FROM @Проекты as П
	left join @Работы as Р
	on П.Проект_ID = Р.Проект_ID
	GROUP BY П.Проект_ID, П.Название) as A
ORDER BY A.S desc

--4
SELECT П.*
FROM @Проекты as П
WHERE П.Проект_ID not in (SELECT Р.Проект_ID 
				FROM @Работы as Р
				WHERE Р.Начало > '01.03.13')
--5
SELECT П.*
FROM @Проекты as П
WHERE П.Проект_ID not in (SELECT Р.Проект_ID 
				FROM @Работы as Р
				WHERE Р.Начало > '01.03.13' and Р.Сотрудник_ID = 1)

