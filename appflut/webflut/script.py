import pandas as pd
from .models import Activity

# load the data
df = pd.read_excel('file.xlsx')

# iterate through the data and create Activity instances
for index, row in df.iterrows():
    Activity.objects.create(
        id=row['№'],
        category=row['Категория'],
        activity_type=row['Вид активности'],
        met=row['МЕТ']
    )

import sqlite3
import pandas as pd

# Загрузите данные
df = pd.read_excel('file.xlsx')

# Подключитесь к БД
conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()

# Итерируйте по данным и создайте экземпляры Activity
for index, row in df.iterrows():
    # Здесь формируется SQL запрос, который заменяет Django ORM
    query = f"""
    INSERT INTO your_app_activity (id, category, activity_type, met)
    VALUES ({row['№']}, "{row['Категория']}", "{row['Вид активности']}", "{row['МЕТ']}");
    """

    cur.execute(query)

# Закройте соединение
conn.commit()
conn.close()