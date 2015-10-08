USE Library
GO


--1
SELECT Фамилия, Имя, Отчество
FROM Авторы
ORDER BY Фамилия, Имя, Отчество

--2
SELECT TOP 5 Название
FROM Издания
ORDER BY Название desc

--3
SELECT ISBN, Название
FROM Издания
WHERE Название like '%SQL%'

--4
SELECT Автор_ID, Фамилия, Имя, Отчество
FROM Авторы
WHERE Фамилия not like '%ова'

--5
SELECT COUNT(DISTINCT Иа.Автор_ID)
FROM Книги as К inner join Издания_авторы as Иа on К.ISBN = Иа.ISBN
WHERE К.Наличие = 1

--6
SELECT COUNT(DISTINCT К.ISBN)
FROM Книги as К
WHERE К.Наличие = 1

--7
SELECT COUNT(*)
FROM Книги as К
WHERE К.Наличие = 1

--8
SELECT И.ISBN, И.Название, isNULL(SUM(cast(К.Наличие as int)), 0)
FROM Издания as И left join Книги as К on И.ISBN = К.ISBN
GROUP BY И.ISBN, И.Название

--9
SELECT И.ISBN, И.Название, MAX(Иа.N_автора)
FROM Издания as И inner join Издания_авторы as Иа on И.ISBN = Иа.ISBN
GROUP BY И.ISBN, И.Название

--10 ,,
SELECT TOP 5 А.Фамилия, А.Имя, А.Отчество
FROM Авторы as А inner join Издания_авторы as Иа on А.Автор_ID = Иа.Автор_ID
GROUP BY А.Автор_ID, А.Фамилия, А.Имя, А.Отчество
ORDER BY COUNT(Иа.ISBN)


--11

--12
