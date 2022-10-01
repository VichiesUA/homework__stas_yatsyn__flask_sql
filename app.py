from flask import Flask, Response
from webargs import fields
from webargs.flaskparser import use_args

from application.services.create_table import create_table
from application.services.db_connection import DBConnection

app = Flask(__name__)

@app.route("/")
def start_page():
    return '''
        <h1> ==> <a href = "/users/create"> create users (need write contact= and phone=) </a> <br></h1>
        <h1> ==> <a href = "/users/read-all"> show all users in phones data base </a> <br></h1>
        <h1> ==> <a href = "/users/read/"> READ user in primary key (need write primary key) </a></h1>
        <h1> ==> <a href = "/users/update/"> UPDATE user in primary key (need write primary key) </a></h1>
        <h1> ==> <a href = "/users/delete"> DELETE user in primary key (need write primary key) </a></h1>
        '''


@app.route("/users/create")
@use_args({"contact": fields.Str(required=True), "phone": fields.Int(required=True)}, location="query")
def users__create(args):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "INSERT INTO phones (contact, phone) VALUES (:contact, :phone);",
                {"contact": args["contact"], "phone": args["phone"]},
            )

    return "Ok"

@app.route("/users/read-all")
def users__read_all():
    with DBConnection() as connection:
        phones = connection.execute("SELECT * FROM phones;").fetchall()

    return "<br>".join([f'{contact["phone_ID"]}: {contact["contact"]} - {contact["phone"]}' for contact in phones])


@app.route("/users/read/<int:phone_ID>")
def users__read(phone_ID: int):
    with DBConnection() as connection:
        phones = connection.execute(
            "SELECT * " "FROM phones " "WHERE (phone_ID=:phone_ID);",
            {
                "phone_ID": phone_ID,
            },
        ).fetchone()

    return f'{phones["phone_ID"]}: {phones["contact"]} - {phones["phone"]}'


@app.route("/users/update/<int:phone_ID>")
@use_args({"phone": fields.Int(), "contact": fields.Str()}, location="query")
def users__update(
    args,
    phone_ID: int,
):
    with DBConnection() as connection:
        with connection:
            contact = args.get("contact")
            phone = args.get("phone")
            if contact is None and phone is None:
                return Response(
                    "Need to provide at least one argument",
                    status=400,
                )

            args_for_request = []
            if contact is not None:
                args_for_request.append("contact=:contact")
            if phone is not None:
                args_for_request.append("phone=:phone")

            args_2 = ", ".join(args_for_request)

            connection.execute(
                "UPDATE phones " f"SET {args_2} " "WHERE phone_ID=:phone_ID;",
                {
                    "phone_ID": phone_ID,
                    "phone": phone,
                    "contact": contact,
                },
            )

    return "Ok"


@app.route("/users/delete/<int:phone_ID>")
def users__delete(phone_ID):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "DELETE " "FROM phones " "WHERE (phone_ID=:phone_ID);",
                {
                    "phone_ID": phone_ID,
                },
            )

    return "Ok"


create_table()

if __name__ == '__main__':
    app.run()
