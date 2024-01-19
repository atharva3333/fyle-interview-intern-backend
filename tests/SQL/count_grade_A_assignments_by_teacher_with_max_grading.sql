-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH MaxGradedTeacher AS (
  SELECT teacher_id
  FROM assignments
  WHERE state = 'GRADED'
  GROUP BY teacher_id
  ORDER BY COUNT(*) DESC
  LIMIT 1
)

SELECT COUNT(*) AS grade_a_count
FROM assignments
WHERE grade = 'A'
  AND teacher_id = (SELECT teacher_id FROM MaxGradedTeacher);

