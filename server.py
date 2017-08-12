from flask import Flask, redirect, render_template, request
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app, 'friendsdb')
print(mysql)
friendsG = mysql.query_db("SELECT * FROM friends")
print(dir(mysql))
print(friendsG)
print(dir(friendsG))

@app.route('/')
def index():
    #testing flask part works & practice formatting extended data entries; pylint finds fault.
    # if True:
    #     return render_template('index.html', 
    #                             all_friends = [{'first_name':'bob', 
    #                                             'last_name':'brownhat',
    #                                             'id':1,
    #                                             'occupation':'malware UX optimizer'},
    #                                             {'first_name':'alice', 
    #                                             'last_name':'ecila',
    #                                             'id':2,
    #                                             'occupation':'data exfiltration engineer'}])
    friends = mysql.query_db("SELECT * FROM friends")
    print(friends)
    print(type(friends))
    return render_template('index.html', all_friends=friends)


@app.route('/friends', methods=['POST'])
def create():
    print request.form['first_name']
    print request.form['last_name']
    print request.form['occupation']
    # add a friend to the database!
    return redirect('/')

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



if __name__ == '__main__':
  app.run(port=8000, debug=True)
 