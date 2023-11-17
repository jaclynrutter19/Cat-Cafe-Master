# Sample Flask application for a Foster Cat Relationship database, snapshot of Foster_Cat_Relationships
# Citation: Original code is reformatted by the bsg_people example and flask tutorial https://github.com/osu-cs340-ecampus/flask-starter-app/tree/master/bsg_people_app

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os



app = Flask(__name__)

# database connection
# Template:
# app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
# app.config["MYSQL_USER"] = "cs340_OSUusername"
# app.config["MYSQL_PASSWORD"] = "XXXX" | last 4 digits of OSU id
# app.config["MYSQL_DB"] = "cs340_OSUusername"
# app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# database connection info
app.config["MYSQL_HOST"] = ""
app.config["MYSQL_USER"] = ""
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = ""
app.config["MYSQL_CURSORCLASS"] = ""

mysql = MySQL(app)

# Routes
# have homepage route to /main by default for convenience, generally this will be your home route with its own template
@app.route("/")
def home():
    return render_template("main.j2")


# route for foster cat relationships page
@app.route("/foster_cat", methods=["POST", "GET"])
def foster_cat_relationships():
    # Separate out the request methods, in this case this is for a POST
    # insert a foster cat relationship into the foster cat relationships entity
    if request.method == "POST":
        # fire off if user presses the Add foster cat relationship button
        if request.form.get("Add_Foster_Cat_Relationship"):
            # grab user form inputs
            cat_id = request.form["cat_id"]
            foster_parent_id = request.form["foster_parent_id"]

            # account for null cat_id AND foster_parent_id
            if cat_id == "" and foster_parent_id == "0":
                # mySQL query to insert a new foster cat relationship into Foster_Cat_Relationships with our form inputs
                query = "INSERT INTO Foster_Cat_Relationships (cat_id, foster_parent_id) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (cat_id, foster_parent_id))
                mysql.connection.commit()

            # account for null foster_parent_id
            elif foster_parent_id == "0":
                query = "INSERT INTO Foster_Cat_Relationships (cat_id, foster_parent_id) VALUES (%s, %s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (cat_id, foster_parent_id))
                mysql.connection.commit()

            # account for null cat_id
            elif cat_id == "":
                query = "INSERT INTO Foster_Cat_Relationships (cat_id, foster_parent_id) VALUES (%s, %s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (cat_id, foster_parent_id))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Foster_Cat_Relationships (cat_id, foster_parent_id) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (cat_id, foster_parent_id))
                mysql.connection.commit()

            # redirect back to foster cat relationships page
            return redirect("/foster_cat")

    # Grab Foster_Cat_Relationships data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the foster cat relationships in Foster_Cat_Relationships
        query = "SELECT Foster_Cat_Relationships.id, cat_id, foster_parent_id, Foster_Cat_Relationships.name AS foster_parent_id, cat_id FROM Foster_Cat_Relationships LEFT JOIN Foster_Cat_Relationships ON cat_id = Foster_Cat_Relationships.id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab planet id/name data for our dropdown
        query2 = "SELECT cat_id, foster_parent_id FROM Foster_Cat_Relationships"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        foster_parent_id_data = cur.fetchall()

        # render edit_foster_cats_relationship page passing our query data and foster parent data to the foster cat relationships template
        return render_template("foster_cat.j2", data=data)


# route for delete functionality, deleting a foster cat relationship from Foster_Cat_Relationships,
# we want to pass the 'id' value of that foster cat relationship on button click (see HTML) via the route
@app.route("/delete_foster_cat_relationship/<int:id>")
def delete_foster_cat_relationship(id):
    # mySQL query to delete the foster cat relationship with our passed id
    query = "DELETE FROM Foster_Cat_Relationships WHERE id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to foster cat relationships page
    return redirect("/foster_cat")


# route for edit functionality, updating the attributes of a foster cat relationship in Foster_Cat_Relationships
# similar to our delete route, we want to the pass the 'id' value of that foster cat relationship on button click (see HTML) via the route
@app.route("/edit_foster_cat_relationship/<int:id>", methods=["POST", "GET"])
def edit_foster_cat_relationship(id):
    if request.method == "GET":
        # mySQL query to grab the info of the foster cat relationship with our passed id
        query = "SELECT * FROM Foster_Cat_Relationships WHERE id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab cat & foster id/name data for our dropdown
        query2 = "SELECT cat_id, foster_parent_id FROM Foster_Cat_Relationships"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        foster_parent_data = cur.fetchall()

        # render edit_foster_cat_ page passing our query data and cat/foster data to the edit_foster_cat template
        return render_template("edit_foster_cat.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit foster cat relationship' button
        if request.form.get("Edit_Foster_Cat_Relationship"):
            # grab user form inputs
            id = request.form["fosterCatRelationshipID"]
            cat_id = request.form["cat_id"]
            foster_parent_id = request.form["foster_parent_id"]

            # account for null cat_id AND foster_cat_id
            if (cat_id == "" or cat_id == "None") and foster_parent_id == "0":
                # mySQL query to update the attributes of foster cat relationship with our passed id value
                query = "UPDATE Foster_Cat_Relationships SET Foster_Cat_Relationships.cat_id = %s, Foster_Cat_Relationships.foster_parent_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (cat_id, foster_parent_id))
                mysql.connection.commit()

            # account for null foster_parent_id
            elif foster_parent_id == "0":
                query = "UPDATE Foster_Cat_Relationships SET Foster_Cat_Relationships.cat_id = %s, Foster_Cat_Relationships.foster_parent_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (cat_id, foster_parent_id))
                mysql.connection.commit()

            # account for null cat_id
            elif cat_id == "" or cat_id == "None":
                query = "UPDATE Foster_Cat_Relationships SET Foster_Cat_Relationships.cat_id = %s, Foster_Cat_Relationships.foster_parent_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (cat_id, foster_parent_id))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "UPDATE Foster_Cat_Relationships SET Foster_Cat_Relationships.cat_id = %s, Foster_Cat_Relationships.foster_parent_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (cat_id, foster_parent_id))
                mysql.connection.commit()

            # redirect back to foster cat relationships page after we execute the update query
            return redirect("/foster_cat")


# Listener
# change the port number if deploying on the flip servers
if __name__ == "__main__":
    app.run(port=3054, debug=True)