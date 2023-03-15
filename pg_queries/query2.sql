-- 5 комнат, где самый маленький средний возраст студентов
SELECT rooms.id AS room, AVG(students.age) AS avg_age
FROM students INNER JOIN rooms
ON students.id_room = rooms.id
GROUP BY rooms.id
ORDER BY avg_age
LIMIT 5;
