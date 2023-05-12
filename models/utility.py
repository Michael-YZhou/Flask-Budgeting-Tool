import psycopg2
import os


def sql_read(query, parameters=[]):
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
    )
    cursor = connection.cursor()
    cursor.execute(query, parameters)
    results = cursor.fetchall()
    connection.close()
    return results


def sql_write(query, parameters=[]):
    connection = psycopg2.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
    )
    cursor = connection.cursor()
    cursor.execute(query, parameters)
    connection.commit()
    connection.close()


def convert_to_dictionary(entry):
    return {
        "id": str(entry[0]),
        "type": entry[1],
        "amount": "{:.2f}".format(entry[2] / 100),
        "description": entry[3],
        "date": entry[4],
        "user_id": entry[5],
    }


def get_entry(id):
    # PSQL query returns a list of tuples even though there is only 1 result
    entry = sql_read("SELECT * FROM entries WHERE id=%s", [id])[0]
    # convert the PSQL result to from tuple to dict, so it can be passed to HTML
    return convert_to_dictionary(entry)


def get_all_entries():
    entries = sql_read("SELECT * FROM entries")
    return [convert_to_dictionary(entry) for entry in entries]


def insert_entry(
    entry_type, entry_amount, entry_description, entry_date, entry_user_id
):
    sql_write(
        "INSERT INTO entries(type, amount, description, date, user_id) VALUES(%s, %s, %s, %s, %s);",
        [
            entry_type,
            int(float(entry_amount) * 100),
            entry_description,
            entry_date,
            int(entry_user_id),
        ],
    )


def update_entry(
    entry_id, entry_type, entry_amount, entry_description, entry_date, entry_user_id
):
    sql_write(
        "UPDATE entries SET type=%s, amount=%s, description=%s, date=%s, user_id=%s WHERE id=%s",
        [
            entry_type,
            int(float(entry_amount) * 100),
            entry_description,
            entry_date,
            int(entry_user_id),
            int(entry_id),
        ],
    )


def delete_entry(entry_id):
    sql_write("DELETE FROM entries WHERE id=%s", [int(entry_id)])
