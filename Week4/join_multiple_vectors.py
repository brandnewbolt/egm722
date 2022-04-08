#drop the index_right column in order to do second join (python wont allow multiply columns by same name)
join_a.drop('index_right', axis=1, inplace=True)
