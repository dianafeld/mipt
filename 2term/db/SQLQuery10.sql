
DECLARE @M TABLE (id int, kol int)
INSERT INTO @M 
Values (1,2), (2,1), (3,3), (4,8), (5,4)

SELECT *
FROM @M
ORDER BY kol

Select M1.id, Count(M1.id)
From @M M1 INNER JOIN @M M2 ON
    M1.kol >= M2.kol
Group BY M1.id, M1.kol