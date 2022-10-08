from .resources import TodoListApi,TodoListApiCRUD

def initialize_routes(api):
    api.add_resource(TodoListApi, '/api/tdlist')
    api.add_resource(TodoListApiCRUD, '/api/todolistuser/<id>')



    #api.add_resource(Hello, '/api/')
    #api.add_resource(Square, '/square/<int:num>')