import sys 
import requests 

base_url = "https://api.trello.com/1/{}" 
auth_params = {    
    'key': "d44c6c4f30f9c6983495600d361cc4e4",    
    'token': "1f4d473fe314d61e895c681b10d51a714dbf96a911d0246bed570e09c4153aa0", }
board_id = "FxLJ80qx"    
    
def read():      
    # Получим данные всех колонок на доске:      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()          
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:          
        # Получим данные всех задач в колонке и перечислим все названия      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print("\n", column['name'], len(task_data), "\n")      
        if not task_data:      
            print('\t' + 'Нет задач!')      
            continue      
        ind = 0
        for task in task_data:
            ind += 1      
            print( '\t {i}. {n}, id: {id}'.format(i=ind, n=task['name'], id=task['id']) )    
    
def create(name, column_name):      
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна
    print(column_name)      
    for column in column_data:      
        if column['name'] == column_name:
            print(column['id'])      
            # Создадим задачу с именем _name_ в найденной колонке      
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            print("Задача {name} добавлена в {column_name}".format(name = name, column_name = column_name))      
            break  
    
def move(name, column_name):    
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
        
    # Среди всех колонок нужно найти задачу по имени и получить её id    
    task_id = None 
    list_tasks = []
    i = 0   
    for column in column_data:    
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:    
            if task['name'] == name:
                i += 1
                list_tasks.append({"Номер": i, "Имя": task['name'], "Колонка":column['name'], "id":task['id']})
                continue
    if len(list_tasks) == 1:    
        print(list_tasks)
        task_id = list_tasks[0]["id"]
    elif len(list_tasks) > 1:
        print(list_tasks)
        x = int(input("Выберите номер необходимой задачи: "))
        task_id = list_tasks[x-1]["id"]
    else:
        print("Не обнаружено задачи: {}".format(name))

       
    # Теперь, когда у нас есть id задачи, которую мы хотим переместить    
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу    
    for column in column_data:    
        if column['name'] == column_name:    
            # И выполним запрос к API для перемещения задачи в нужную колонку    
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})    
            print("Задача {name} перемещена в колонку {column_name}".format(name = name, column_name = column_name))
            break 

def create_column(column_name):
    # Реализация создания колонок
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    possibility_to_create = True
    for column in column_data:
        if column_name in column['name']:
            print("Колонка с названием {} уже существует".format(column_name))
            possibility_to_create = False
            break

    if possibility_to_create == True:
        requests.post(base_url.format('lists'), data={'name': column_name, 'idBoard': column_data[0]['idBoard'], **auth_params})
        print('Список "{}" создан!'.format(column_name))

if __name__ == "__main__":    
    if len(sys.argv) <= 2:   
        read()    
    elif sys.argv[1] == 'create':    
        create(sys.argv[2], sys.argv[3])    
    elif sys.argv[1] == 'move':    
        move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'create_column':
        create_column(sys.argv[2])  