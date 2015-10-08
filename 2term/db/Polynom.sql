USE Poly
GO

DROP TABLE Полином
CREATE TABLE Полином (Полином_id int, Степень_id int, Коэф float, primary key(Полином_id, Степень_id))

INSERT INTO Полином
VALUES (1, 0, 5), (1, 1, 4), (1, 2, 0), (1, 3, -1), (1, 4, 0.5), (2, 2, 100), (2, 3, 4), (3, 0, 1), (4, 0, 1), (4, 1, 2), (4, 2, 1)
