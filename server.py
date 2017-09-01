from flask import Flask, redirect, render_template, request, url_for
from mysqlconnection import MySQLConnection
app = Flask(__name__)
mysql = MySQLConnection(app, 'friendsdb')


@app.route('/')
def index():
    return redirect(url_for('viewfriends'))


@app.route('/friends', methods=['GET'])
def viewfriends():
    return render_template('index.html', all_friends=mysql.query_db("SELECT * FROM friends"))


@app.route('/friends', methods=['POST'])
def addFriend():
    print('addFriend')
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    occupation = request.form['occupation']
    print(first_name, last_name, occupation)
    # str_sql_insert = "USE friendsdb; INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES ({}, {}, {}, NOW(), NOW());".format(first_name, last_name, occupation)
    str_sql_insert = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (:first_name, :last_name, :occupation, NOW(), NOW());"
    data = {
            'first_name': first_name,
            'last_name': last_name, 
            'occupation': occupation,
            }
    print str_sql_insert
    mysql.query_db(str_sql_insert, data)
    return redirect(url_for('viewfriends'))

@app.route('/friends/<friend_id>')
def show(friend_id):
    # Write query to select specific user by id. At every point where
    # we want to insert data, we write ":" and variable name.
    query = "SELECT * FROM friends WHERE id = :specific_id"
    # Then define a dictionary with key that matches :variable_name in query.
    data = {'specific_id': friend_id}
    # Run query with inserted data.
    friends = mysql.query_db(query, data)
    # Friends should be a list with a single object,
    # so we pass the value at [0] to our template under alias one_friend.
    return render_template('index.html', one_friend=friends[0])

fake_friends = [{'first_name':'bob', 
             'last_name':'brownhat',
             'id':1,
             'occupation':'malware UX optimizer'},
             {'first_name':'alice', 
             'last_name':'ecila',
             'id':2,
             'occupation':'data exfiltration engineer'}]
#to double check flask part works, ie if True:\n    return render_template("index.html", all_friends=fake_friends)
if __name__ == '__main__':
  app.run(port=8000, debug=True)