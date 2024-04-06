import psycopg2
import re


def extract_categories(text):
    all_results = []
    sections = text.strip().split('\n\n')

    for section in sections:
        categories = {}
        lines = section.strip().split('\n')
        current_category = None

        for line in lines:
            if ":" in line:
                category, content = re.split(r'\s*:\s*', line, maxsplit=1)
                category = category.lower().replace(" ",
                                                    "_")  # Convert category to lowercase and replace spaces with underscores
                categories[category] = content.strip()
                current_category = category
            elif current_category:
                categories[current_category] += ' ' + line.strip()

        all_results.append(categories)

    return all_results


def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wine_description (
        id SERIAL PRIMARY KEY,
        name TEXT,
        type TEXT,
        notes TEXT,
        barrel TEXT,
        time_barrel TEXT,
        sugar TEXT,
        grapes TEXT
    )
    """)
    conn.commit()


def insert_data(conn, data):
    cursor = conn.cursor()
    for entry in data:
        print(entry.get('time', ''))
        cursor.execute("""
        INSERT INTO wine_description (name, type, notes, barrel, time_barrel, sugar, grapes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (entry.get('name', ''), entry.get('type', ''), entry.get('notes', ''), entry.get('barrel', ''),
              entry.get('time', ''), entry.get('sugar', ''), entry.get('grapes', '')))
    conn.commit()


def main():
    with open('wines.txt', 'r') as file:
        text = file.read()

    conn = psycopg2.connect(dbname='wine_bot', user='benjacruz', password='bcruz123', host='localhost',
                            port='5432')

    create_table(conn)
    data = extract_categories(text)
    insert_data(conn, data)

    conn.close()


if __name__ == "__main__":
    main()
