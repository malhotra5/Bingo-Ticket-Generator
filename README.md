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
    
    def readData():
        data = pd.read_excel('Songs.xlsx')
        return data

Now that we have the data, we need a database to store it in. We make the database by making a connection.
    
    conn = sqlite3.connect("shrunkSongs.db")
    c = conn.cursor()
We create a table named songs using the following function.

    def createTable():
        c.execute('CREATE TABLE IF NOT EXISTS songs(ind INTEGER, name TEXT, kind TEXT)')

The function only makes a table if it does not exist. This is good practise to make sure that you don't accidently loose all the data you had in a table with the same name. The columns are the following - 

* ind - Index number of a song
* name - The name of a song
* kind - The genre of a song

We create a function to put data into the database - 

    def putData(name, index, kind):
        c.execute("INSERT INTO songs (ind, name, kind) VALUES(?,?,?)",
                (index,name, kind))
        conn.commit()

Now we call the functions we have and run the following - 
    
    data =readData() #Gets data
    createTable() #Makes a table
    for i, row in enumerate(data['Songs']): #Gets every songs name
        putData(i, row, data['Kind'][i]) #This gets every row from the excel file and puts it into the database

A lot of the time, we get extremely messy data. In the real world, we have to spend quite some time to preprocess data. In our case, it's pretty much done for use. But, we are going to clean some of it, by making sure that every song's name and song's kind are starting with captial letters. The following function will do it for us. 


### Making the tickets 
Now that we are done getting the data




