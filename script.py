import random
import psycopg2
import datetime

conn = psycopg2.connect(dbname='employees_db', user='postgres', password='bnFo4LKI3i', host='localhost')
cursor = conn.cursor()

cursor.execute("INSERT INTO api_job_title VALUES (0, 'Teamlead')")
cursor.execute("INSERT INTO api_job_title VALUES (1, 'Senior')")
cursor.execute("INSERT INTO api_job_title VALUES (2, 'Middle')")
cursor.execute("INSERT INTO api_job_title VALUES (3, 'Junior')")
cursor.execute("INSERT INTO api_job_title VALUES (4, 'Trainee')")
conn.commit


first_names = ['Вячеслав', 'Герман', 'Вадим', 'Юрий', 'Никон', 'Владислав', 'Эммануил', 'Василий', 'Богдан', 'Рюрик', 'Павел']
second_names = ['Смелоч', 'Веденин', 'Корниенко', 'Бабышев', 'Густокашин', 'Шапиро', 'Ивашев', 'Черепанов', 'Лебединцев', 'Чистяков']
middle_names = ['Федосиевич', 'Карлович', 'Тихонович', 'Иосифович', 'Прохорович', 'Давыдович', 'Глебович', 'Никифорович', 'Сократович', 'Эрнстович']
date = datetime.date.today()
salary_currency = 'USD' 
password = 'e10adc3949ba59abbe56e057f20f883e' #123456


i = -1
while True:
    i += 1
    command = str("INSERT INTO api_employee VALUES ({0}, '{1}', '{2}', '{3}', '{4}', '{5}', {6}, '{7}', '{8}', NULL, 0, NULL)").format(
    i, random.choice(first_names), random.choice(second_names), random.choice(middle_names), date, salary_currency, 
    random.randrange(500, 2000), 'username'+str(i), password)
    cursor.execute(command)

    i += 1
    command = str("INSERT INTO api_employee VALUES ({0}, '{1}', '{2}', '{3}', '{4}', '{5}', {6}, '{7}', '{8}', NULL, 1, {9})").format(
    i, random.choice(first_names), random.choice(second_names), random.choice(middle_names), date, salary_currency, 
    random.randrange(500, 2000), 'username'+str(i), password, i-1)
    cursor.execute(command)

    i += 1
    command = str("INSERT INTO api_employee VALUES ({0}, '{1}', '{2}', '{3}', '{4}', '{5}', {6}, '{7}', '{8}', NULL, 2, {9})").format(
    i, random.choice(first_names), random.choice(second_names), random.choice(middle_names), date, salary_currency, 
    random.randrange(500, 2000), 'username'+str(i), password, i-1)
    cursor.execute(command)

    i += 1
    command = str("INSERT INTO api_employee VALUES ({0}, '{1}', '{2}', '{3}', '{4}', '{5}', {6}, '{7}', '{8}', NULL, 2, {9})").format(
    i, random.choice(first_names), random.choice(second_names), random.choice(middle_names), date, salary_currency, 
    random.randrange(500, 2000), 'username'+str(i), password, i-2)
    cursor.execute(command)

    i += 1
    command = str("INSERT INTO api_employee VALUES ({0}, '{1}', '{2}', '{3}', '{4}', '{5}', {6}, '{7}', '{8}', NULL, 3, {9})").format(
    i, random.choice(first_names), random.choice(second_names), random.choice(middle_names), date, salary_currency, 
    random.randrange(500, 2000), 'username'+str(i), password, i-1)
    cursor.execute(command)

    i += 1
    command = str("INSERT INTO api_employee VALUES ({0}, '{1}', '{2}', '{3}', '{4}', '{5}', {6}, '{7}', '{8}', NULL, 4, {9})").format(
    i, random.choice(first_names), random.choice(second_names), random.choice(middle_names), date, salary_currency, 
    random.randrange(500, 2000), 'username'+str(i), password, i-1)
    cursor.execute(command)

    i += 1
    command = str("INSERT INTO api_employee VALUES ({0}, '{1}', '{2}', '{3}', '{4}', '{5}', {6}, '{7}', '{8}', NULL, 4, {9})").format(
    i, random.choice(first_names), random.choice(second_names), random.choice(middle_names), date, salary_currency, 
    random.randrange(500, 2000), 'username'+str(i), password, i-2)
    cursor.execute(command)

    if i >= 50000:
        break

conn.commit()
cursor.close()
conn.close()
