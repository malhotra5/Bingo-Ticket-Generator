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
We are using reportlab to create a pdf of tickets. If we can create just one PDF with all the tickets, then we can print it all at once. To make the PDF's, we can use reportlab. Here are the steps to make the ticket generator - 
* Getting the data
  * Take the data (songs) from an excel file, and make a database
  * Format and clean all the data in the database
* Making the tickets
  * Get random data for a ticket
  * Make a table out of it (this is the final ticket)
* Keep repeating the second step until you get the number of tickets you want
