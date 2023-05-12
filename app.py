from flask import Flask, render_template, request, redirect, session
import os
from models import utility

app = Flask(__name__)
# SET secret key. The secret key is used when encripting the data stored in session (e.g. user_id)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def index():
    # entries will contain a list of dict
    entries = utility.get_all_entries()
    # print(entries)
    return render_template("summary.html", entries=entries)


@app.route("/forms/entry/add")
def add_entry_form():
    return render_template("add_entry_form.html")


# the add_entry function and the index function use the same route
# the first one uses POST method, second one uses GET. When a form passed to this route,
# Flask will scan all functions and match them with the function that uses the correct method.
@app.route("/api/creat_new", methods=["POST"])
# @app.route("/api/entry/add", methods=["POST"])
def add_entry():
    form = request.form
    utility.insert_entry(
        form.get("entry_type"),
        form.get("entry_amount"),
        form.get("entry_description"),
        form.get("entry_date"),
        form.get("entry_user_id"),
    )
    return redirect("/")


@app.route("/forms/entry/edit/<id>")
def edit_entry_form(id):
    print(id)
    entry = utility.sql_read("SELECT * FROM entries WHERE id=%s", [id])[0]
    print(entry)
    entry = utility.convert_to_dictionary(entry)
    print(entry)

    return render_template("edit_entry_form.html", entry=entry)


@app.route("/api/entry/edit", methods=["POST"])
def edit_entry():
    form = request.form
    print()
    print(form)
    # form data are all strings, need to convert them to relevant type before insert into db
    utility.update_entry(
        form.get("entry_id"),
        form.get("entry_type"),
        form.get("entry_amount"),
        form.get("entry_description"),
        form.get("entry_date"),
        form.get("entry_user_id"),
    )
    return redirect("/")


@app.route("/forms/entry/delete/<id>")
def delete_entry_form(id):
    entry = utility.get_entry(id)
    return render_template("delete_entry_form.html", entry=entry)


@app.route("/api/entry/delete", methods=["POST"])
def delete_entry():
    form = request.form
    utility.delete_entry(form.get("entry_id"))
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5500))
