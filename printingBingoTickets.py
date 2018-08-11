from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import random
import sqlite3

#Make document
doc = SimpleDocTemplate("PDF results.pdf", pagesize=letter)
#Make element holder
elements = []


#Connect to database of songs
conn = sqlite3.connect("Bingo Songs.db")
#Make a cursor
c = conn.cursor()


#Get all the data from database
def getData():
    c.execute('SELECT * FROM songs')
    data = c.fetchall()
    return data

#Get random data in a list. None of the elements are repeated
def getRandom(data):
    copy = data
    #List for the songs chosen for a ticket
    chosen = []

    for _ in range(3*5): #Number of songs required
        randEl = random.choice(copy) #Choose random song
        copy.remove(randEl) #Remove the song from our options so that we don't repeat it
        chosen.append(randEl[1]) #Choose only the song name from the random choice
    return chosen

#Make 2 dimensional lists to represent table in reportlab
def createDataForm(chosen):
    #This makes lists of lists
    #Its in the following format
    #[   [" ", Songs Bingo!, " " ], ###This is the header of the table
    #    [name1, name2, name3],
    #    [name4, name5, name6],
    #    [name7, name8, name9],
    #    [name10, name11, name12],
    #    [name13, name14, name15]]
    
    finalData = []
    newList = []
    #Append the header of the table
    finalData.append([" ", 'Songs Bingo!'])
    #Choose data 3 at a time and make a row of the table out of it
    for i in range(int(len(chosen)/3)):
        finalData.append(chosen[i*3:i*3 + 3: 1])

    #Returns list for the table of 1 ticket
    return finalData

#Make a table and align it to the left or right
def createTables(data, align):

    #Pre-process data
    data = textWrap(data)

    #Align it to the left or to the right
    if(align == 0):
        t=Table(data,3*[1.2*inch], 6*[0.5*inch], hAlign = 'LEFT') #Make table element
    else:
        t=Table(data,3*[1.2*inch], 6*[0.5*inch], hAlign = 'RIGHT') #Make table element

    #Set table style for rows
    t.setStyle(TableStyle([('INNERGRID', (0,1), (-1,-1), 0.25, colors.black),
                           ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                           ('BOX', (0,1), (-1,-1), 0.25, colors.black),
                           ]))
    #Set table style for headers
    t.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 0.25, colors.black),
                           ('BACKGROUND',(0,0), (3,0), colors.lightgrey)
                            ]))

    #Return final table
    return t

#Text wrap. This is to make sure that a very long sentence moves to the next line to adjust the cell length in a table.
def textWrap(data):
    for i in data:
        for j in range(len(i)):
            lens = []
            words = i[j].split(" ")
            for z in words:
                lens.append(len(z))
            num = 0
            allIndex = []
            for index, val in enumerate(lens):
                num = num + val
                if (num > 12):
                    num = val
                    allIndex.append(index)
            for ind, val in enumerate(allIndex):
                words.insert(val+ind, '\n')
            newSentence = ""
            for word in words:
                newSentence = newSentence + " " + word

            i[j] = newSentence
    return data
    

#Table of tables
TEMP = [[]]


for i in range(100):
    data = getData() #Gets data
    ticketData = getRandom(data) #Gets random data for ticket
    formatedData = createDataForm(ticketData)   #Creates a list for the table
    if(i%2 == 0):
        align = 0
    else:
        align = 1
    TEMP[0].append(createTables(formatedData, align))   #Makes a table which holds 2 tables (the 2 tables are the tickets)
    if(len(TEMP[0]) == 2):
        #Adds the table of 2 tables to elements
        elements.append(Table(TEMP))
        TEMP = [[]]
        #Adds space between a row of 2 tickets
        elements.append(Spacer(1,20))

#Build the elements
doc.build(elements)

#Close database connections
c.close()
conn.close()

