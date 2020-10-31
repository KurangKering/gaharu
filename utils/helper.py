def get_second_value(list_of_tuples, first_value):
	return next((y for x,y in list_of_tuples if x == first_value), None)