import sqlite3
import pandas as pd

# Загрузите данные из Excel
df = pd.read_excel(r'D:\КОЛЯМБА\25.03_проверка\caloriesappweb\МЕТы_детские.xlsx', header=None, skiprows=2)

# Заполните пропущенные значения второго столбца (категории)
df[1].fillna(method='ffill', inplace=True)

# Подключитесь к базе данных SQLite
conn = sqlite3.connect(r'D:\КОЛЯМБА\25.03_проверка\caloriesappweb\appflut\db.sqlite3')
cur = conn.cursor()

# Итерируйте по данным и вставьте их в таблицу SQLite
for index, row in df.iterrows():
    code = str(row[0])
    category = str(row[1])
    subcategory = str(row[2])
    code_6_9 = str(row[3])
    code_10_12 = str(row[4])
    code_13_15 = str(row[5])
    code_16_18 = str(row[6])

    # Вставьте данные в таблицу SQLite
    cur.execute("INSERT INTO webflut_activity_for_children (code, category, subcategory, code_6_9, code_10_12, code_13_15, code_16_18) VALUES (?,?,?,?,?,?,?)",
                (code, category, subcategory, code_6_9, code_10_12, code_13_15, code_16_18))

# Закройте соединение с базой данных
conn.commit()
conn.close()

print("Импорт данных из Excel в базу данных SQLite завершен.")
