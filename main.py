import sqlite3
from datetime import datetime, date, timedelta
from random import randint
from typing import List

from faker import Faker

fake = Faker('uk-UA')

subjects = [
    "Основи програмування",
    "Математичний аналіз",
    "Численні методи",
    "Культурологія",
    "Філософія",
    "Теорія ймовірності",
    "Web програмування",
    "Механіка рідини і газу",
    "Фізика"
]

task_dict = {"select-1.sql":"1.Знайти 5 студентів із найбільшим середнім балом з усіх предметів.",
             "select-2.sql":"2.Знайти студента із найвищим середнім балом з певного предмета.",
             "select-3.sql":"3.Знайти середній бал у групах з певного предмета.",
             "select-4.sql":"4.Знайти середній бал на потоці (по всій таблиці оцінок).",
             "select-5.sql":"5.Знайти, які курси читає певний викладач.",
             "select-6.sql":"6.Знайти список студентів у певній групі.",
             "select-7.sql":"7.Знайти оцінки студентів в окремій групі з певного предмета.",
             "select-8.sql":"8.Знайти середній бал, який ставить певний викладач зі своїх предметів.",
             "select-9.sql":"9.Знайти список курсів, які відвідує студент.",
             "select-10.sql":"10.Список курсів, які певному студенту читає певний викладач."}

groups = ["ФФ-11", "GoIt-12", "ЕМ-10"]

NUMBERS_TEACHERS = 5
NUMBERS_STUDENTS = 50

connect = sqlite3.connect('hw06.db')
cursor = connect.cursor()

def create():
    cursor.execute("""DROP TABLE IF EXISTS [groups];""")
    cursor.execute("""CREATE TABLE [groups] (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name STRING UNIQUE
    );""")
    cursor.execute("""DROP TABLE IF EXISTS teachers;""")
    cursor.execute("""
    CREATE TABLE teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname STRING
    );""")

    cursor.execute("""DROP TABLE IF EXISTS students;""")
    cursor.execute("""
    CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname STRING,
    group_id REFERENCES [groups] (id)
    );""")

    cursor.execute("""DROP TABLE IF EXISTS subjects;""")
    cursor.execute("""
    CREATE TABLE subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name STRING UNIQUE,
    teacher_id REFERENCES teachers (id)
    );""")

    cursor.execute("""DROP TABLE IF EXISTS grades;""")
    cursor.execute("""
    CREATE TABLE grades (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id REFERENCES students(id),
    subject_id REFERENCES subjects(id),
    grade INTEGER NOT NULL,
    date_of DATE
    );""")

def seed_teacher():
    teachers = [fake.name() for _ in range(NUMBERS_TEACHERS)]
    sql = "INSERT INTO teachers(fullname) VALUES (?);"
    cursor.executemany(sql, zip(teachers,))


def seed_groups():
    sql = "INSERT INTO groups(name) VALUES (?);"
    cursor.executemany(sql, zip(groups,))


def seed_students():
    students = [fake.name() for _ in range(NUMBERS_STUDENTS)]
    list_group_id = [randint(1, len(groups)) for _ in range(NUMBERS_STUDENTS)]
    sql = "INSERT INTO students(fullname, group_id) VALUES (?, ?);"
    cursor.executemany(sql, zip(students, list_group_id))


def seed_subjects():
    list_teacher_id = [randint(1, NUMBERS_TEACHERS) for _ in range(len(subjects))]
    sql = "INSERT INTO subjects(name, teacher_id) VALUES (?, ?);"
    cursor.executemany(sql, zip(subjects, list_teacher_id))


def seed_grades():
    start_date = datetime.strptime("2022-09-01", "%Y-%m-%d")
    finish_date = datetime.strptime("2023-05-31", "%Y-%m-%d")
    sql = "INSERT INTO grades(student_id, subject_id, grade, date_of) VALUES (?, ?, ?, ?);"

    def get_list_date(start_date, finish_date) -> List[date]:
        result = []
        current_day: date = start_date
        while current_day < finish_date:
            if current_day.isoweekday() < 6:
                result.append(current_day)
            current_day += timedelta(1)
        return result

    list_date = get_list_date(start_date, finish_date)

    grades = []
    for day in list_date:
        random_subject = randint(1, len(subjects))
        random_students = [randint(1, NUMBERS_STUDENTS) for _ in range(5)]
        for student in random_students:
            grades.append((student, random_subject, randint(1, 12), day.date()))

    cursor.executemany(sql, grades)
def task(file,task):
    with open(file,"r") as file:
        print(task)
        cursor.execute(file.read())
        five_students_with_the_highest =cursor.fetchall()
        for student in five_students_with_the_highest:
            print(student)
def select():
    for key,value in task_dict.items():
        task(key,value)
        print("-" * 50)
    

if __name__ == '__main__':
    create()
    seed_teacher()
    seed_groups()
    seed_students()
    seed_subjects()
    seed_grades()
    select()
    connect.commit()
    connect.close()
