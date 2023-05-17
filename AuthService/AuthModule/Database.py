from AuthModule import GetModel, executeQuery

def GetObjectFromTable(value, table, column):
    def queryFunc(session, base, value, table, column):
        # Check if value is provided
        assert value is not None, "Error: No value provided"
        # Get all rows from the specified table and column
        theTable = session.query(GetModel(table)).filter_by(**{column: value}).first()
        # Check if an error occurred during retrieval
        if theTable is None:
            print('Error: No table exist with provided values')
            return None, 404
        # If no error, query the row that matches the provided value
        else:
            return theTable
    return executeQuery(queryFunc, value, table, column)

def GetPasswordFromUsername(username):
    def queryFunc(session, base, username):
        # Query the database for the user with the provided username
        user = session.query(GetModel('users')).filter_by(username=username).first()
        # Check if an error occurred during retrieval
        if user is None:
            print('Error: No user exist with provided username')
            return None, 404
        # If no error, return the user's password
        else:
            return user.password
    return executeQuery(queryFunc, username)
