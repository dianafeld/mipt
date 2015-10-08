USE Книжный_магазин
GO

CREATE TABLE Заказы
	(нДок int primary key, Дата date, Покупатель_ID int, Сумма_RUR int, Оплата_RUR int)

INSERT INTO Заказы VALUES
(1, '20130313', 1, 100, 100)

CREATE TABLE Заказы_данные
	(нДок int, нПоз int, Книга_ID int, Колво int, Отпущено int, Цена_RUR int, primary key (нДок, нПоз))

INSERT INTO Заказы_данные VALUES
(1, 1, 1, 2, 2, 150)

CREATE TABLE Остатки
	(Книга_ID int primary key, Остаток int, Резерв int)

INSERT INTO Остатки VALUES
(1, 3, 1)

CREATE TABLE Книги
	(Книга_ID int primary key, Название varchar(50), Автор_ID int, Год_выпуска int, Цена_RUR int, Раздел_ID int)

INSERT INTO Книги VALUES
(1, 'Дюна', 1, 1998, 150, 1)

CREATE TABLE Разделы
	(Раздел_ID int primary key, Раздел varchar(50))

INSERT INTO Разделы VALUES
(1, 'Научная фантастика')

CREATE TABLE Авторы
	(Автор_ID int primary key, Фамилия varchar(50), Имя varchar(50), Отчество varchar(50))

INSERT INTO Авторы VALUES
(1, 'Герберт', 'Фрэнк', NULL)

CREATE TABLE Покупатели
	(Покупатель_ID int primary key, Название varchar(50), Баланс int)

INSERT INTO Покупатели VALUES
(1, 'А', 200)

SELECT SUM(), SUM()
FROM 