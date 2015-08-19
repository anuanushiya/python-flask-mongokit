from flask import Flask, request, render_template, redirect, url_for
from flask.ext.mongokit import MongoKit
from bson.objectid import ObjectId

from models import Task

app = Flask(__name__)

db = MongoKit(app)
db.register([Task])

@app.route('/')
def show_all():
    tasks = db.Task.find()
    return render_template('index.html', tasks=tasks)

@app.route('/create', methods=['POST'])
def add_task():
	body = request.form['body']

	title = request.form['title']
	task = db.Task()
	task.title = title
	task.body = body
	task.save()

	tasks = db.Task.find()
	return redirect(url_for('show_all'))

@app.route('/delete/<string:task_id>')
def delete_task(task_id):
	task = db.Task.find_one({'_id': ObjectId(task_id)})
	task.delete()

	return redirect(url_for('show_all'))

@app.route('/save', methods=['POST'])
def update_task():
	body = request.form['body']
	title = request.form['title']
	
	myid = request.form['id']
	task = db.Task.find_one({'_id': ObjectId(myid)})
	
	task.title = title
	task.body = body
	task.save()
	
	return redirect(url_for('show_all'))

if __name__ == '__main__':
	print "INIT FLASK"
	
	use_debugger = True
	app.run(use_debugger=use_debugger, debug=use_debugger)