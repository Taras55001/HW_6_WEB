SELECT gr.name, ROUND(AVG(g.grade), 2) as avg_grade
FROM groups gr
JOIN students s ON gr.id = s.group_id 
JOIN grades g ON s.id = g.student_id
JOIN subjects sub ON g.subject_id = sub.id
WHERE sub.id = 4
GROUP BY gr.id