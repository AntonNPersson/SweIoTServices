from ToolModule import executeQuery, GetModel, jsonify, GetTable, request, GetSession, HTTPException, abort, json, datetime
import json
from datetime import datetime
from sqlalchemy.exc import IntegrityError, ProgrammingError
from sqlalchemy import text

def InsertToTable(table, values):
    def queryFunc(session, base, values):
        # Get table model and columns
        name = "public." + table
        tableModel = base.metadata.tables.get(name)
        # Check if table exists
        if tableModel is None:
            return False, 'Error: Table not found'
        columnsModel = tableModel.columns.keys()
        newValues = {}
        # Ensure that values are provided
        assert values is not None, "Error: No values provided"
        # Loop through the columns in the table and create a dictionary
        # with column names and values to insert
        for column in columnsModel:
            if column in values:
                colType = str(tableModel.columns[column].type)
                colValue = values[column]
                if colType.startswith('VARCHAR') or colType.startswith('TEXT'):
                    newValues[column] = colValue
                elif colType.startswith('INTEGER'):
                    newValues[column] = int(colValue)
                elif colType.startswith('BOOLEAN'):
                    newValues[column] = colValue.lower() == 'true'
                elif colType.startswith('NUMERIC'):
                    newValues[column] = float(colValue)
                elif colType.startswith('DATE'):
                    newValues[column] = datetime.strptime(colValue, '%Y-%m-%d').date()
                elif colType.startswith('TIME'):
                    newValues[column] = datetime.strptime(colValue, '%H:%M:%S').time()
                elif colType.startswith('TIMESTAMP'):
                    newValues[column] = datetime.strptime(colValue, '%Y-%m-%d %H:%M:%S')
                elif colType.startswith('JSON'):
                    newValues[column] = json.loads(colValue)
                elif colType.startswith('ARRAY'):
                    newValues[column] = colValue.split(',')
            elif column == 'id':
                # Generate a new id value using the default sequence
                query = text(f"SELECT nextval('{table}_id_seq')")
                result = session.execute(query)
                newValues[column] = result.scalar()
            else:
                newValues[column] = None  # Use default value for missing columns
        # Insert the new object into the table
        newObject = tableModel.insert().values(**newValues)
        session.execute(newObject)
        session.commit()
        # Return success
        return True
    return executeQuery(queryFunc, values)



def RemoveFromTable(table, id):
    def queryFunc(session, base, table, id):
        # Get the table model from the metadata based on the provided table name
        name = "public." + table
        tableModel = base.metadata.tables.get(name)
        # Check if the table exists in the metadata
        if tableModel is None:
            return False, 'Error: Table not found'
        # Ensure that an ID is provided
        assert id is not None, "Error: No ID provided"
        # Create a query to remove a row with the given ID from the table
        query = tableModel.delete().where(tableModel.c.id == id)
        try:
            # Execute the query and commit the transaction
            session.execute(query)
            session.commit()
            return True, None
        except Exception as e:
            return False, str(e)
    return executeQuery(queryFunc, table, id)


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

def UpdateTable(table_name):
    session, base = GetSession()
    table = table_name
    if table != table_name:
        return abort(400, "Invalid table name.")
    
    updated_values = request.get_json()
    if not updated_values:
        return abort(404, "No data provided.")

    # Collect all the item IDs that need to be updated
    item_ids = [item.get("id") for item in updated_values]
    if not item_ids:
        return abort(404, "No items to update.")

    theTable = GetModel(table)
    name = "public." + table
    tableModel = base.metadata.tables.get(name)
    columnsModel = tableModel.columns.keys()
    for column in columnsModel:
        colType = str(tableModel.columns[column].type)

    # Get the columns of the table and their corresponding data types
    columns = theTable.__table__.columns
    column_types = {str(col.name): col.type for col in columns}

    # Update the rows in the database
    for updated_row in updated_values:
        item_id = updated_row.get("id")
        # Query the database for the row to update
        row = session.query(theTable).filter_by(id=item_id).first()
        if not row:
            return abort(404, f"Cannot update id: {item_id}.")
        # Update the row with the new values
        for key, value in updated_row.items():
            if key != "id" or not isinstance(value, str):
                # Convert the value to the correct data type
                if colType:
                    try:
                        if colType.startswith('VARCHAR') or colType.startswith('TEXT'):
                            newValues = value
                        elif colType.startswith('INTEGER'):
                            newValues = int(value)
                        elif colType.startswith('BOOLEAN'):
                            newValues = value.lower() == 'true'
                        elif colType.startswith('NUMERIC'):
                            newValues = float(value)
                        elif colType.startswith('DATE') or colType.startswith('date'):
                            newValues = datetime.strptime(value, '%Y-%m-%d').date()
                        elif colType.startswith('TIME'):
                            newValues = datetime.strptime(value, '%H:%M:%S').time()
                        elif colType.startswith('TIMESTAMP'):
                            newValues = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                        elif colType.startswith('JSON'):
                            newValues = json.loads(value)
                        elif colType.startswith('ARRAY'):
                            newValues = value.split(',')
                        setattr(row, key, newValues)
                    except ValueError:
                            return abort(400, f"Invalid value '{value}' for column '{key}'")
        # Mark the row as dirty so that it will be updated in the database
        session.add(row)

    # Commit the changes to the database
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        error_message = str(e.orig)
        error_explanation = error_message.split("DETAIL:")[0]
        return abort(400, error_explanation)
    except ValueError as e:
        session.rollback()
        return abort(400, f"Invalid format: '{key}'")
    except ProgrammingError as e:
        return abort(400, f"Invalid format: '{key}'")
    except Exception as e:
        session.rollback()
        return abort(400, f"Invalid format: '{key}'")
    else:
        return jsonify({"message": "Table values updated successfully."}), 200







