## Name: Appointment   //   Difficulty: Very Easy   //   Topic: SQLi    
#### By: Kyle Zimmer    
       
**Overview: Though I may have went down the rabbit hole on this box, I finally came around to finding out that the login form of a web page doesn't throw errors when special characters are entered. After enumerating the backend and identifying MySQL was being used, I manipulated data entry to bypass password validation and access user data (flag).**     

<img width="363" height="183" alt="image" src="https://github.com/user-attachments/assets/cc813934-ae54-4a06-a967-6fd5a6031b88" />     

Let's begin with our usual quick syn scan against the most common ports with `nmap -sS -Pn --disable-arp-ping -n [target ip]`   

<img width="585" height="184" alt="image" src="https://github.com/user-attachments/assets/72cd2695-0026-417c-87b0-10637edd4e32" />   

And now we can narrow in our query with version and script scans against this target's open port by adding `-sT -sV -sC -p 80`    
* As a reminder, I use -Pn to disable ICMP pings, arp layer 2 pings, and dns resolution on scans to speed things up.   
  
<img width="797" height="228" alt="image" src="https://github.com/user-attachments/assets/24f3a8c5-9be6-4512-b3ad-de79b9863ee2" />     

We quickly notice that this HTTP port is running an apache web server with version 2.4.38 on a debian Linux distribution.     

HackTheBox's question lists asks about the 2021 OWASP Top 10 along with some SQL questions. I assume that this web server's going to have some form of SQL vulnerability, namely SQL injection. Let's take a look at this web server by browsing to it.    

<img width="1260" height="1070" alt="image" src="https://github.com/user-attachments/assets/67e5f703-79ec-41d9-b55f-9f3c0ca243cd" />    


Data point: Taking a look at [CVEDetails](https://www.cvedetails.com/version/613554/Apache-Http-Server-2.4.38.html), we can see that this version of Apache's HTTP Server Daemon has a few vulnerabilities we can look out for as well.    

<img width="1055" height="385" alt="image" src="https://github.com/user-attachments/assets/cbc95a38-0f3d-47c6-a012-e2f92cb313e4" />    

Let's also take a look at searchsploit.    

<img width="513" height="140" alt="Screenshot 2025-10-08 224258" src="https://github.com/user-attachments/assets/a6b8e545-6462-4730-bafa-42bab88db3ee" />

Nothing really of interest here... While we're in the enumeration phase, let's begin looking for hidden directories that we can potentially leverage. I'll use gobuster like in one of my last write-ups: `gobuster dir -u [target ip] -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -x ".html" --timeout 20s`    

<img width="978" height="370" alt="image" src="https://github.com/user-attachments/assets/4dd1a21a-af8e-485f-8c70-35a605e4a545" />     

I'm interested in that javascript directory. The vendor directory is my second up. Let's check them out in our browser and look for clues.    

<img width="717" height="332" alt="image" src="https://github.com/user-attachments/assets/2382369f-bdef-4623-9e72-7f006715d2b3" />   

<img width="1264" height="973" alt="image" src="https://github.com/user-attachments/assets/1e93f628-d902-4e28-bcae-6c6f50acd985" />   

<img width="851" height="347" alt="image" src="https://github.com/user-attachments/assets/d20e9c02-11fe-40f8-9fa3-c568516835c4" />   
 
<img width="677" height="306" alt="image" src="https://github.com/user-attachments/assets/e8a36c67-b3fa-4f65-9664-913c426929d4" />   

main.js doesn't seem to have anything out of the ordinary.     

<img width="902" height="606" alt="image" src="https://github.com/user-attachments/assets/00aa942e-71dc-41bf-8dba-3836cff4e457" />    

Vendor seems to be a bunch of web page css and javascript to add web dynamics to scxroll bars, buttons, and other miscellaneous functions.   

<img width="757" height="388" alt="image" src="https://github.com/user-attachments/assets/c26d79e1-bbbc-4cb3-8fa3-25d3e186f050" />   

Nothing to see here... I think we're down a rabbithole. While the rest of the gobuster runs, I will take a look at another method of web enumeration... web request proxy interception with Burpsuite. This tool will allow us to catch the HTTP request to the site so that we can analyze what it looks like and how we can manipulate it before passing it on to the web server.    

<img width="2414" height="1218" alt="image" src="https://github.com/user-attachments/assets/9624c22c-7082-4f8e-a32e-170b0d6f3170" />    
 
Now that we have the BurpSuite web browser open with the client waiting to intercept our HTTP requests to the server, let's go ahead and input some random creds to see what it looks like on the wire.   

<img width="2040" height="904" alt="image" src="https://github.com/user-attachments/assets/2a1978fd-2352-4c90-ac17-1dba31f3ba29" />     

Also, in the history tab you can see that the site loaded all those vendor, js, and font directories to build our front-end:    

<img width="541" height="210" alt="image" src="https://github.com/user-attachments/assets/5ce7fd28-9c9b-4ccc-a3fc-02af93fd23be" />    

Sadly, the response to our request didn't lead to anything telling.. just a HTTP 200 response with the web page re-loaded.   

<img width="1190" height="635" alt="image" src="https://github.com/user-attachments/assets/59177b83-d49e-44b6-be64-22551bf73d73" />    

With the information we obtained in our packet interception (`--data="username=admin&password=123"`), we can enumerate the backend through automated inputs using a SQL injection tool called SQLMap.

<img width="1258" height="579" alt="image" src="https://github.com/user-attachments/assets/4a5d7467-c823-45d6-bcca-dc10e6b84daf" />     

* `.29-MariaDB-0+deb10u1`
* `web server operating system: Linux Debian 10 (buster)`
* `web application technology: Apache 2.4.38`
* `back-end DBMS: MySQL >= 5.0.12 (MariaDB fork)`
* `banner: '10.3.29-MariaDB-0+deb10u1'`

Assuming that this PHP (most popular with Apache) server is running MySQL in the background, we can try using some MySQL commenting to try and mess with the login process. To begin with this, let's see if the login form allows us to enter special characters without error:    
 
<img width="455" height="491" alt="image" src="https://github.com/user-attachments/assets/df2cff05-efae-4bf4-86aa-b4194e167990" />     
 
Doing this just returned us back to the same login.html page... BUT it didn't give us any errors. Let's think deeper about this.      

A basic statement in MySQL will resemble: `SELECT * FROM 'database_name' WHERE variable='xxx'`. I also want to note that MySQL allows for the `#` and `--` character sequences to denote comments in source code.     

With that in mind, let's assume that at some point, this database server is going to be queried for our stored credentials or other information about our account like `SELECT * FROM accounts WHERE username='entered_username' AND ...validate password...`     

If I wanted to terminate the SQL Statement before it could validate the password, I'd simply want to end a valid username entry with a symbol to comment out the rest of the line.    
* `SELECT * FROM accounts WHERE usernam='administrator'#' AND ... validate password commented out ...`    
Pay close attention to the end of the username. Let's go ahead and try a couple usernames like this in the login forum with "123" as the password (because it'll be commented out regardless.)    

Let's try some basic usernames (root, user, guest, admin, administrator) but tailor them to end like we described above, i.e. (u: root'# // p: 123)   

<img width="457" height="531" alt="image" src="https://github.com/user-attachments/assets/9dd615e5-cda7-42f4-ba27-b4f6a2f299e9" />     

Nothing... returned to the login page... onto the next.   

<img width="447" height="518" alt="image" src="https://github.com/user-attachments/assets/a1366e92-18e5-429d-9cd1-a2fa81c0103f" />     

Nope. Next.   

<img width="446" height="509" alt="image" src="https://github.com/user-attachments/assets/32120a5b-1f3e-4e28-8c5e-541874ec25be" />     

Nada.   

<img width="417" height="521" alt="image" src="https://github.com/user-attachments/assets/0ed7b122-697b-47d1-b624-2f55723ddb51" />   

Bingo!   

<img width="708" height="177" alt="image" src="https://github.com/user-attachments/assets/ec5dcf6f-d97f-4b85-9517-1a17c66ace0a" />  

<img width="687" height="594" alt="image" src="https://github.com/user-attachments/assets/3b145448-afbb-4daf-b3e7-dd59a92199bb" />    
  


Note: Don’t submit the flag that appeared on my screen. It is unique to my account and will cause your account to be flagged for cheating.       
