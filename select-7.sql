SELECT s.fullname, g.grade, gr.name
FROM students AS s
JOIN grades AS g ON s.id = g.student_id
JOIN subjects AS sub ON g.subject_id = sub.id
JOIN groups AS gr ON s.group_id = gr.id
WHERE sub.id = 4 AND gr.id = 3;
