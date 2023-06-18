SELECT t.fullname, ROUND(AVG(g.grade), 2), sub.name AS average_grade
FROM teachers AS t
JOIN subjects AS sub ON t.id = sub.teacher_id
JOIN grades AS g ON sub.id = g.subject_id
WHERE t.id = 2
GROUP BY sub.id;
