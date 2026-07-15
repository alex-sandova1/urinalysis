--Number of urinalysis tests by gender
SELECT Gender, COUNT(*) AS NumberOfTests
FROM urinalysis_tests
GROUP BY Gender;

--Number of urinalysis tests by age group
SELECT 
  CASE 
    WHEN Age < 18 THEN 'Under 18'
    WHEN Age BETWEEN 18 AND 25 THEN 'Young Adult (18-25)'
    WHEN Age BETWEEN 26 AND 64 THEN 'Adult (26-64)'
    ELSE 'Seniors (Over 65)'
  END AS AgeGroup,
  COUNT(*) AS NumberOfTests
FROM urinalysis_tests
GROUP BY AgeGroup
ORDER BY CASE 
  WHEN Age < 18 THEN 1
  WHEN Age BETWEEN 18 AND 25 THEN 2
  WHEN Age BETWEEN 26 AND 64 THEN 3
  ELSE 4
END;

--Number of urinalysis tests by diagnosis
SELECT Diagnosis, COUNT(*) AS NumberOfTests
FROM urinalysis_tests
GROUP BY Diagnosis;