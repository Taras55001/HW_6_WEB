SELECT sub.name, s.fullname AS subject_name
FROM students AS s
JOIN grades AS g ON s.id = g.student_id
JOIN subjects AS sub ON g.subject_id = sub.id
WHERE s.id = 40;
