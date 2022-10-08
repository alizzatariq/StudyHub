from flask import request, Response, jsonify,session
from flask_restful import Resource
from Classes import TodoList,User
import json


from DBHandler import DataBaseHandler
handler=DataBaseHandler("localhost", "root", '', "studyplanner")


class TodoListApi(Resource):
    def get(self):
        #body = request.get_json()
        todoList1=handler.getTodoList("usr_20010")
        jsonTodo = json.dumps(todoList1)
        print("json is :: ",jsonTodo)
        return Response(jsonTodo, mimetype="application/json", status=200)

    def post(self):
        body = request.get_json()
        #print(body,"   ",body["title"],body["desc"])
        tdList=TodoList("",body["userId"],"",body["title"],body["desc"],body["userName"])
        handler.addTodoList(tdList)
        return True




class TodoListApiCRUD(Resource):

    #FOR SPECIFIC USER DATA
    def get(self,id):
        todoList1=handler.getTodoList(id)
        jsonTodo = json.dumps(todoList1)
        print("json uId is :: ",jsonTodo)
        return Response(jsonTodo, mimetype="application/json", status=200)


    def delete(self,id):
        print("In delete specific Todo")
        handler.deleteTodo(id)
        print("Deleted")
        return True

