SELECT s.fullname, gr.name
FROM students AS s
JOIN groups AS gr ON s.group_id = gr.id
WHERE gr.id = 1;
