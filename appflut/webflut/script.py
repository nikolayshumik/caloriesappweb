import sqlite3
import pandas as pd
import numpy as np

# Загрузите данные
df = pd.read_excel(r'D:\КОЛЯМБА\25.03_проверка\caloriesappweb\МЕТы_для_БГУиР.xlsx')

df['Категория'] = df['Категория'].fillna(method='ffill')
# Fill NaN values with an arbitrary number
df['№'] = df['№'].fillna(0)

# Convert numbers to integer safely
df['№'] = df['№'].apply(lambda x: int(x) if x == x else "")

# Fill NaN values with an empty string for other columns
df = df.replace(np.nan, "", regex=True)

# Подключитесь к БД
conn = sqlite3.connect(r'D:\КОЛЯМБА\25.03_проверка\caloriesappweb\appflut\db.sqlite3')
cur = conn.cursor()

# Итерируйте по данным и создайте экземпляры Activity
for index, row in df.iterrows():
    try:
        met_value = float(row['МЕТ'])
    except ValueError:
        met_value = 0.0

    data = (str(row['Категория']), str(row['Вид активности']), met_value)
    print(data)  # Add this line
    cur.execute("INSERT INTO webflut_activity (category, activity_type, met) VALUES (?, ?, ?)", data)



# Закройте соединение
conn.commit()
conn.close()

# import sqlite3
#
# # Подключитесь к базе данных
# conn = sqlite3.connect(r'D:\flutappweb\appflut\db.sqlite3')
# cur = conn.cursor()
#
# # Удалите все записи из таблицы
# cur.execute("DELETE FROM webflut_activity")
#
# # Закройте соединение
# conn.commit()
# conn.close()