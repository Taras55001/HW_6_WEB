SELECT sub.name, t.fullname
FROM subjects sub
JOIN teachers t ON sub.teacher_id = t.id
WHERE t.id = 3
;
