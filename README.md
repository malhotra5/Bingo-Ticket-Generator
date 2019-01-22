# Bingo-Ticket-Generator
This is a small python project using sqlite3 and reportlab to automate a real world task. It creates bingo tickets using song names. 
## Inspiration 
One day, my mother told me to create bingo tickets. She said we would play bingo during a get together with friends. In the game, we would play a song. We would have to recognize the song's name. If the name of the song was on the ticket, we would scratch it out. We would keep doing so until someone has a bingo. 
## Getting Started
Clone the repository to get started.
### Prerequisites
* Pandas (data manipulation and analysis)
* sqlite3 (database management system)
* reportlab (PDF and Graphics generator)

I will explain the code for reportlab and pandas. For sqlite3, check out my tutorial here - 
https://github.com/malhotra5/Database-functionalities

### Installing
Sqlite comes pre-installed. To get the rest, you can find python wheels at this website - https://www.lfd.uci.edu/~gohlke/pythonlibs/

Download the wheel files for the required modules. To install wheels, run the following commands on the terminal. Make sure that your terminal is in the directory your wheel files have been downloaded. Run - 

    pip install wheelFileName.whl #Run for all wheel files
    
An alternate would be to run the following - 

    pip install pandas
    pip install reportlab
    
    
## How it's made
We are going to create a pdf of tickets. If we can create just one PDF with all the tickets, then we can print it all at once. To make the PDF's, we can use reportlab. I got all the songs for the tickets from my mother in an excel sheet. We will use pandas to read data from there. Here are the steps to make the ticket generator - 
* Getting the data
  * Take the data (songs) from an excel file, and make a database
  * Format and clean all the data in the database
* Making the tickets
  * Get random data for a ticket
  * Make a table out of it (this is the final ticket)
* Keep repeating the second step until you get the number of tickets you want

### Getting the data: Making the database
We need to get the data from an excel file, and make a database out of it. We will use pandas for it. In my repository, I made a whole other file in order to do this. Its called excelToDatabase.py. The excel file is the following format

Songs|Kind
-----|-----
High Hopes| Rock
Back in Black| Rock

This function only reads all the raw data from the excel file. 
```python    
    def readData():
        data = pd.read_excel('Songs.xlsx')
        return data
```
Now that we have the data, we need a database to store it in. We make the database by making a connection.
```python    
    conn = sqlite3.connect("shrunkSongs.db")
    c = conn.cursor()
```
We create a table named songs using the following function.
```python
    def createTable():
        c.execute('CREATE TABLE IF NOT EXISTS songs(ind INTEGER, name TEXT, kind TEXT)')
```
The function only makes a table if it does not exist. This is good practise to make sure that you don't accidently loose all the data you had in a table with the same name. The columns are the following - 

* ind - Index number of a song
* name - The name of a song
* kind - The genre of a song

We create a function to put data into the database - 
```python
    def putData(name, index, kind):
        c.execute("INSERT INTO songs (ind, name, kind) VALUES(?,?,?)",
                (index,name, kind))
        conn.commit()
```        
A lot of the time, we get extremely messy data. In the real world, we have to spend quite some time to preprocess data. In our case, it's pretty much done for use. But, we are going to clean some of it, by making sure that every song's name and song's kind are starting with captial letters. The following function will do it for us. 
```python
    def updateValDataBase(data, typ):
        #All the rows in our data
        for row in data:
            #Checking if the first letter is lower case
            if(row[0].islower()):
                #Storing all the letters from row except for the first letter
                old = row[1:len(row)]
                #Making only the first letter uppercase
                newLet = row[0].upper()
                
                #Making the new string with first letter capital 
                newData = newLet+old
                
                #Checking whether to update name or kind, then updating it
                if(typ == 'Songs'):
                    c.execute('UPDATE songs SET name=(?) WHERE name=(?)', (newData, row))
                    conn.commit()
                else:
                    c.execute('UPDATE songs SET kind=(?) WHERE kind=(?)', (newData, row))
                    conn.commit()
```
This function will take any kind of text data in the database, and capitalize the first letter. We will use this function on the songs names and kinds. 

Now we call the functions we have and run the following - 
 ```python   
    data =readData() #Gets data
    createTable() #Makes a table
    for i, row in enumerate(data['Songs']): #Gets every songs name
        putData(i, row, data['Kind'][i]) #This gets every row from the excel file and puts it into the database
    
    updateValDataBase(data['Songs'], 'Songs') #Cleans data 
    updateValDataBase(data['Kind'], 'Kind')

```

### Making the tickets 
Now that we are done getting the data, we need to use it to create a PDF of tickets. I decided to have 15 songs on the list in a 5 x 3 table. Our first step will be to get random song names from the database, for every ticket we want. We can get the data by doing the following - 
```python
    #Get all the data from database
    def getData():
        c.execute('SELECT * FROM songs')
        data = c.fetchall()
        return data
```
We can now get random song names for a ticket by doing the following - 
```python
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
```        
Note that we added code to make sure that none of the song names repeat on the ticket. The function above returns a list of songs that we can use for one ticket.

Now that we have our list of song names we want to use for a ticket, we need to format the data. Reportlab has a function that can make a table for us. However, it takes a two dimensional list. It takes one list, that has multiple lists within it. Each list within it, represents a row of the table. We can make that data format by using the following function - 
```python   
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
```    
The function above returns the data in the format we want. Now we can get to the good part. We can finally make the table out it. But, reportlab has a problem. If the song name it too large, the text will run out of the it's cell in the table, and go into another cell. This will cause the text to overlap. This following picture a table with the text overlapping. 

![GitHub Logo](/images/over.jpg)

We have to make our own text wrap function. Honestly, my code is very long and hard to explain. I show the function and briefly tell what it is doing. 
```python
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
```
This taking a sentence, and adding the word **\n** where ever its needed. Reportlab, will automatically shift a sentence into the next line, if it every encounters **\n (this stands for new line)**. So, the function above, splits a sentence it its words. Then it makes a list for the length of every word. Then, the algorithm figures out where to add the word **\n**, given the length of the words in the original sentence. The function takes the formatted data, and text wraps it. 

Now, we can finally make out table. The following function makes a table for one ticket. 

#Make a table and align it to the left or right
```python   
    def createTables(data, align):

        #Text wrap data
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
```
The function *table* from reportlab used above, takes the number of columns and rows as a parameter. We used the size *inch* to define how big of a cell we want. We then used halign to make the table go to the left or right of the PDF. We set the style of the table using *setStyle*. This gave everythin except for the header a border. It also gave the header a different background color. To know more about the parameters for the reportlab methods above, visit this documentation - https://www.reportlab.com/docs/reportlab-userguide.pdf

Great! We finally have a table. We are not done yet though. Based on the size of the table, we want to fit multiple tables on one page. We want to fit to tables next to each other. So, we can make a table of 1 row and 2 columns, that will hold 2 tickets. After that, we can tie it all together using the functions we made. 

```python
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
```
The data above, makes a a PDF for a hundred tickets. Notice doc.build, takes a list of elements. These elements, hold out tables. At the end, we build the tables

## Results 

![GitHub Logo](/images/results.jpg)

## Things to take away
* Real world problems can be solved by programming
* A lot of times, modules or code that has been provided for you won't have everything. You have to create your own functionalities sometimes. You saw this during the **textWrap()** function
* You saw how to use multiple modules in Python, and implement it for a full fledged application
## Things to improve
Even though we are randomly picking songs for the tickets, there might be a slight chance in which there might be two identical tickets. The order of the songs might be different or even the same, but there is definetely a high chance of having the same songs if there are too few of songs to choose from. 
## Built with
Python3
## Acknowledgments
* My mother for the inspiration to make this repository
