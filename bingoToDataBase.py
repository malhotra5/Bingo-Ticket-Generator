import sqlite3
import pandas as pd


#Connections to database
conn = sqlite3.connect("Bingo Songs.db")
c = conn.cursor()

#File with songs
fileName = 'SongsListBingo.xlsx'

#Makes table if it doesn't exist
def createTable():
    c.execute('CREATE TABLE IF NOT EXISTS songs(ind INTEGER, name TEXT, kind TEXT)')

#Puts data in database
def putData(index, name, kind):
    c.execute("INSERT INTO songs (ind, name, kind) VALUES(?,?,?)",
              (index,name, kind))
    conn.commit()

#Gets the data from excel file in the form of a dictionary
def readData(fileName):
    data = pd.read_excel(fileName)
    return data

#Pre-processes data
def updateValDataBase(data, typ):
    for row in data:
        print(row)
        if(row[0].islower()):
            old = row[1:len(row)]
            newLet = row[0].upper()
            
            newData = newLet+old

            if(typ == 'Songs'):
                c.execute('UPDATE songs SET name=(?) WHERE name=(?)', (newData, row))
                conn.commit()
            else:
                c.execute('UPDATE songs SET kind=(?) WHERE kind=(?)', (newData, row))
                conn.commit()


data =readData(fileName) #Gets data
createTable() #Makes a table if it exists
for i, row in enumerate(data['Songs']): #Gets songs names from every row in excel file
    putData(i, row, data['Kind'][i]) # Puts every row of excel file in database
    
updateValDataBase(data['Songs'], 'Songs') #Pre-processes data
updateValDataBase(data['Kind'], 'Kind')

#Close connections
c.close()
conn.close()
