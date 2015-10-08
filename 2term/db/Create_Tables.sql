-- запустите запросы на создание/заполнение к базе, к которой Вы будете писать запросы

USE CONTR
GO

SET DATEFORMAT DMY

CREATE TABLE Документы (ндок int primary key, Дата datetime, Покупатель_ID int)
CREATE TABLE Документы_данные (ндок int, Товар_ID int, Код_склада int, Колво int, Цена float, primary key (ндок, Товар_ID))
CREATE TABLE Номенклатура (Товар_ID int primary key, Наименование nvarchar(max), Цена float, Масса float, Объем float)
CREATE TABLE Покупатели (Покупатель_ID int primary key, ФИО nvarchar(max))
CREATE TABLE Остатки (Код_склада int, Товар_ID int, Остаток int, primary key (Код_склада, Товар_ID))

INSERT INTO Документы VALUES (1, '15.02.12', 1)
INSERT INTO Документы VALUES (2, '25.04.12', 2)
INSERT INTO Документы VALUES (3, '16.10.12', 3)
INSERT INTO Документы VALUES (4, '16.11.12', 2)
INSERT INTO Документы VALUES (5, '10.12.12', 1)

INSERT INTO Документы_данные VALUES (1,1,1,15,15)
INSERT INTO Документы_данные VALUES (1,2,2,1,50)
INSERT INTO Документы_данные VALUES (2,1,2,13,10)
INSERT INTO Документы_данные VALUES (3,3,2,5,17)
INSERT INTO Документы_данные VALUES (3,4,1,5,15)
INSERT INTO Документы_данные VALUES (3,1,2,5,550)
INSERT INTO Документы_данные VALUES (4,4,2,1,7)
INSERT INTO Документы_данные VALUES (4,3,1,2,6)
INSERT INTO Документы_данные VALUES (5,1,2,3,5)

INSERT INTO Номенклатура VALUES (1, 'Мышка', 12, 0.2, 0.5)
INSERT INTO Номенклатура VALUES (2, 'Клавиатура', 15, 1.5, 3)
INSERT INTO Номенклатура VALUES (3, 'Монитор', 150, 6, 10)
INSERT INTO Номенклатура VALUES (4, 'Звуковая карта', 34, 0.5, 4)
INSERT INTO Номенклатура VALUES (5, 'Материнская плата', 76, 2.5, 7)

INSERT INTO Остатки VALUES (1,1,14)
INSERT INTO Остатки VALUES (1,2,13)
INSERT INTO Остатки VALUES (1,4,23)
INSERT INTO Остатки VALUES (2,5,1)
INSERT INTO Остатки VALUES (2,2,8)
INSERT INTO Остатки VALUES (2,1,3)

INSERT INTO Покупатели VALUES (1, 'Иванов Иван Иванович')
INSERT INTO Покупатели VALUES (2, 'Петрова Валентина Федоровна')
INSERT INTO Покупатели VALUES (3, 'Степанов Дмитрий Николаевич')
INSERT INTO Покупатели VALUES (4, 'Хомяков Андрей Викторович')

