--Number of urinalysis tests by gender
SELECT Gender, COUNT(*) AS [Number of Tests]
FROM urinalysis_tests
GROUP BY Gender;

--Number of urinalysis tests by age group
SELECT 
  CASE 
    WHEN Age < 18 THEN 'Under 18'
    WHEN Age BETWEEN 18 AND 25 THEN 'Young Adult (18-25)'
    WHEN Age BETWEEN 26 AND 64 THEN 'Adult (26-64)'
    ELSE 'Seniors (Over 65)'
  END AS [Age Group],
  COUNT(*) AS [Number of Tests]
FROM urinalysis_tests
GROUP BY [Age Group]
ORDER BY CASE 
  WHEN Age < 18 THEN 1
  WHEN Age BETWEEN 18 AND 25 THEN 2
  WHEN Age BETWEEN 26 AND 64 THEN 3
  ELSE 4
END;

--Number of urinalysis tests by diagnosis
SELECT Diagnosis, COUNT(*) AS [Number of Tests]
FROM urinalysis_tests
GROUP BY Diagnosis;

--Group by urine color
SELECT Color, COUNT(*) AS [Number of Tests]
FROM urinalysis_tests
GROUP BY Color;

--Group by urine clarity
SELECT Transparency, COUNT(*) AS [Number of Tests]
FROM urinalysis_tests
GROUP BY Transparency;

--Group by Glucose
SELECT Glucose, COUNT(*) AS [Number of Tests]
FROM urinalysis_tests
GROUP BY Glucose;

--Group by Protein
SELECT Protein, COUNT(*) AS [Number of Tests]
FROM urinalysis_tests
GROUP BY Protein;

--Group by pH
SELECT pH, COUNT(*) AS [Number of Tests]
FROM urinalysis_tests
GROUP BY pH;

--Group by Specific Gravity
SELECT [Specific Gravity], COUNT(*) AS [Number of Tests]
FROM urinalysis_tests
GROUP BY [Specific Gravity];

--Group by WBC
SELECT WBC, COUNT(*) AS [Number of Tests]
FROM urinalysis_tests
GROUP BY WBC;

--Group by RBC
SELECT RBC, COUNT(*) AS [Number of Tests]
FROM urinalysis_tests
GROUP BY RBC;

--Group by Epithelial Cells
SELECT [Epithelial Cells], COUNT(*) AS [Number of Tests]
FROM urinalysis_tests
GROUP BY [Epithelial Cells];

--Group by Bacteria
SELECT Bacteria, COUNT(*) AS [Number of Tests]
FROM urinalysis_tests
GROUP BY Bacteria;

--Group by Mucous Threads
SELECT [Mucous Threads], COUNT(*) AS [Number of Tests]
FROM urinalysis_tests
GROUP BY [Mucous Threads];

--Group by Amorphous Urates
SELECT [Amorphous Urates], COUNT(*) AS [Number of Tests]
FROM urinalysis_tests
GROUP BY [Amorphous Urates];