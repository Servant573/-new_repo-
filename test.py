from trello import TrelloApi
api_key = "d44c6c4f30f9c6983495600d361cc4e4"
token = "1f4d473fe314d61e895c681b10d51a714dbf96a911d0246bed570e09c4153aa0"
trello = TrelloApi(api_key, token)
response = trello.boards.new("Learn Python")
board_id = response['id']
for column in trello.boards.get_list(board_id):
	if "Нужно" in column['name']:
		list_id = column['id']
card = trello.cards.new("Научиться использовать Trello", list_id)