def is_list(query):
	""" Given a string return true if it is formatted as a list, and False otherwise """
	try:
		return type(eval(query)) == list 
	except: 
		return False