USE Poly
GO


--2
DECLARE @n int
SET @n = 1

SELECT *
FROM Полином
WHERE Полином_id = @n and Коэф != 0
ORDER BY Степень_id

--3
SELECT distinct Полином_id
FROM Полином
WHERE Коэф = 0

--4
SET @n = 1

/*SELECT CASE WHEN MAX(Степень_id) > 2 THEN 'Полином не является полиномом второй степени' ELSE 'OK' END
FROM Полином
WHERE Полином_id = @n*/

IF (SELECT MAX(Степень_id)
	FROM Полином
	WHERE Полином_id = @n) != 2
	PRINT 'Полином не является полиномом второй степени'
ELSE
BEGIN
	DECLARE @a float, @b float, @c float, @d float, @x1 float, @x2 float
	SET @a = isNULL((SELECT Коэф
		FROM Полином
		WHERE Полином_id = @n and Степень_id = 2), 0)
	SET @b = isNULL((SELECT Коэф
		FROM Полином
		WHERE Полином_id = @n and Степень_id = 1), 0)
	SET @c = isNULL((SELECT Коэф
		FROM Полином
		WHERE Полином_id = @n and Степень_id = 0), 0)
	SET @d = @b * @b - 4 * @a * @c
	IF @d < 0
		PRINT 'Нет корней'
	ELSE IF @d = 1
	BEGIN
		PRINT '1 корень'
		SET @x1 = -@b / (2 * @a)
		PRINT @x1
	END
	ELSE
	BEGIN
		PRINT '2 корня'
		SET @x1 = -@b - SQRT(@d) / (2 * @a)
		PRINT @x1
		SET @x2 = -@b + SQRT(@d) / (2 * @a)
		PRINT @x2
	END
END

--5
SET @n = 1

SELECT Степень_id, Коэф
FROM Полином
WHERE Полином_id = @n and Степень_id % 2 = 0 and Коэф != 0
ORDER BY Степень_id


--6
DECLARE @p as float
SET @n = 1
SET @p = 3

SELECT Степень_id, Коэф * @p
FROM Полином
WHERE Полином_id = @n and Коэф != 0
ORDER BY Степень_id

--7
DECLARE @m int
SET @n = 1 --Полином_id
SET @m = 1 --power

SELECT CASE WHEN MAX(Степень_id) = @m THEN 'Да' ELSE 'Нет' END
FROM Полином
WHERE Полином_id = @n and Коэф != 0

--8
DECLARE @p1 int, @p2 int
SET @p1 = 1
SET @p2 = 2


SELECT isNull(П1.Степень_id, П2.Степень_id), isNull(П1.Коэф, 0) + isNull(П2.Коэф, 0)
FROM (SELECT Степень_id, Коэф
	FROM Полином 
	WHERE Полином_id = @p1) as П1 
	full join 
	(SELECT Степень_id, Коэф
	FROM Полином 
	WHERE Полином_id = @p2) as П2 
	on П1.Степень_id = П2.Степень_id

--9
SET @p1 = 1
SET @p2 = 2

SELECT П1.Степень_id + П2.Степень_id, SUM(П1.Коэф * П2.Коэф)
FROM (SELECT Степень_id, Коэф
	FROM Полином
	WHERE Полином_id = @p1) as П1 
	,
	(SELECT Степень_id, Коэф
	FROM Полином
	WHERE Полином_id = @p2) as П2
GROUP BY П1.Степень_id + П2.Степень_id

--10
DECLARE @x float
SET @n = 1 
SET @x = 1

SELECT SUM(power(@x, Степень_id) * Коэф)
FROM Полином
WHERE Полином_id = @n

--11
SET @n = 4

IF (SELECT MAX(Степень_id)
	FROM Полином
	WHERE Полином_id = @n) != 2
	PRINT 'Нет'
ELSE
BEGIN
	--DECLARE @a float, @b float, @c float
	SET @a = isNULL((SELECT Коэф
		FROM Полином
		WHERE Полином_id = @n and Степень_id = 2), 0)
	SET @b = isNULL((SELECT Коэф
		FROM Полином
		WHERE Полином_id = @n and Степень_id = 1), 0)
	SET @c = isNULL((SELECT Коэф
		FROM Полином
		WHERE Полином_id = @n and Степень_id = 0), 0)
	IF @b * @b - 4 * @a * @c = 0
		PRINT 'Да'
	ELSE
		PRINT 'Нет'
END


--12
SET @n = 1

SELECT A, count(*)
FROM (SELECT CASE WHEN Коэф > 0 THEN 'Positive' ELSE CASE WHEN Коэф = 0 THEN 'Zero' ELSE 'Negative' END END as A
	FROM Полином
	WHERE Полином_id = @n) as T
GROUP BY A

--13
SET @n = 1

IF (SELECT COUNT(*)
	FROM Полином
	WHERE Коэф != cast(Коэф as int)) != 0
PRINT 'Нет'
ELSE
PRINT 'Да' 
