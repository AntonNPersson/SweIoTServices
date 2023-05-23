from ToolModule import session, GetAllObjectsInModel, GetModel, redirect, render_template, GetSession
from ToolModule import loginName
from flask import request

def GetList(name):
    if 'user_id' in session:
        dbsession, base = GetSession()
        # Get all items in the model with the specified name using the operation module
        try:
            items = GetAllObjectsInModel(name, dbsession, base)
        except:
            return 'Error: Cannot find table with name: ' + name
        # Create a list to store dictionaries representing the items
        itemsDict = []
        # Iterate through each item and convert it to a dictionary
        try:
            for item in items:
                itemDict = item.__dict__   # Convert the item to a dictionary
                itemDict.pop('_sa_instance_state', None)   # Remove the '_sa_instance_state' key from the dictionary
                itemsDict.append(itemDict)   # Append the dictionary to the itemsDict list
        except:
            return 'Error: Cannot convert items to dictionary'
        # Get the keys of the first dictionary in the itemsDict list, which represent the columns of the table
        columns = itemsDict[0].keys()
        # Get the model object for the specified name
        model = GetModel(name, dbsession, base)
        # Render the 'tableList2.html' template with the itemsDict list, columns, and model as arguments
        dbsession.close()
        return render_template('tableList2.html', items=itemsDict, columns=columns, orders=model)
    else:
        return redirect(loginName), 401