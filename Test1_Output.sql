/* Table T1 */ 

/* Checking FK referential integrity */ 


SELECT t1.k2, t2.k2
FROM t1
LEFT JOIN t2 ON t1.k2 = t2.k2
WHERE t2.k2 IS NULL;


/* Checking columns for key candiate */ 


SELECT COUNT(k1), COUNT(DISTINCT(k1))
FROM T1;



SELECT COUNT(k2), COUNT(DISTINCT(k2))
FROM T1;



SELECT COUNT(A), COUNT(DISTINCT(A))
FROM T1;



SELECT COUNT(B), COUNT(DISTINCT(B))
FROM T1;


/* Checking non-key data dependent */ 


SELECT a.k1, a.k2, b.k2 
FROM T1 a
JOIN T1 b ON a.k2 = b.k2
WHERE a.k2<>b.k2;



SELECT a.k1, a.A, b.A 
FROM T1 a
JOIN T1 b ON a.A = b.A
WHERE a.A<>b.A;



SELECT a.k1, a.B, b.B 
FROM T1 a
JOIN T1 b ON a.B = b.B
WHERE a.B<>b.B;



SELECT a.k2, a.k1, b.k1 
FROM T1 a
JOIN T1 b ON a.k1 = b.k1
WHERE a.k1<>b.k1;



SELECT a.k2, a.A, b.A 
FROM T1 a
JOIN T1 b ON a.A = b.A
WHERE a.A<>b.A;



SELECT a.k2, a.B, b.B 
FROM T1 a
JOIN T1 b ON a.B = b.B
WHERE a.B<>b.B;



SELECT a.A, a.k1, b.k1 
FROM T1 a
JOIN T1 b ON a.k1 = b.k1
WHERE a.k1<>b.k1;



SELECT a.A, a.k2, b.k2 
FROM T1 a
JOIN T1 b ON a.k2 = b.k2
WHERE a.k2<>b.k2;



SELECT a.A, a.B, b.B 
FROM T1 a
JOIN T1 b ON a.B = b.B
WHERE a.B<>b.B;



SELECT a.B, a.k1, b.k1 
FROM T1 a
JOIN T1 b ON a.k1 = b.k1
WHERE a.k1<>b.k1;



SELECT a.B, a.k2, b.k2 
FROM T1 a
JOIN T1 b ON a.k2 = b.k2
WHERE a.k2<>b.k2;



SELECT a.B, a.A, b.A 
FROM T1 a
JOIN T1 b ON a.A = b.A
WHERE a.A<>b.A;


/* Table T2 */ 

/* Checking FK referential integrity */ 


SELECT t2.k3, t3.k3
FROM t2
LEFT JOIN t3 ON t2.k3 = t3.k3
WHERE t3.k3 IS NULL;


/* Checking columns for key candiate */ 


SELECT COUNT(k2), COUNT(DISTINCT(k2))
FROM T2;



SELECT COUNT(k3), COUNT(DISTINCT(k3))
FROM T2;



SELECT COUNT(C), COUNT(DISTINCT(C))
FROM T2;


/* Checking non-key data dependent */ 


SELECT a.k2, a.k3, b.k3 
FROM T2 a
JOIN T2 b ON a.k3 = b.k3
WHERE a.k3<>b.k3;



SELECT a.k2, a.C, b.C 
FROM T2 a
JOIN T2 b ON a.C = b.C
WHERE a.C<>b.C;



SELECT a.k3, a.k2, b.k2 
FROM T2 a
JOIN T2 b ON a.k2 = b.k2
WHERE a.k2<>b.k2;



SELECT a.k3, a.C, b.C 
FROM T2 a
JOIN T2 b ON a.C = b.C
WHERE a.C<>b.C;



SELECT a.C, a.k2, b.k2 
FROM T2 a
JOIN T2 b ON a.k2 = b.k2
WHERE a.k2<>b.k2;



SELECT a.C, a.k3, b.k3 
FROM T2 a
JOIN T2 b ON a.k3 = b.k3
WHERE a.k3<>b.k3;


/* Table T3 */ 

/* Checking FK referential integrity */ 

/* Checking columns for key candiate */ 


SELECT COUNT(k3), COUNT(DISTINCT(k3))
FROM T3;



SELECT COUNT(D), COUNT(DISTINCT(D))
FROM T3;


/* Checking non-key data dependent */ 


SELECT a.k3, a.D, b.D 
FROM T3 a
JOIN T3 b ON a.D = b.D
WHERE a.D<>b.D;



SELECT a.D, a.k3, b.k3 
FROM T3 a
JOIN T3 b ON a.k3 = b.k3
WHERE a.k3<>b.k3;


