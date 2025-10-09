## Name: Seequel   //   Difficulty: Very Easy   //   Topic: SQL    
#### By: Kyle Zimmer    
       
**Overview: After finding a MariaDB server with a default root account that doesn't require a password, I navigated around the databases, finding user and configuration data that led me to the flag.**       

<img width="279" height="106" alt="image" src="https://github.com/user-attachments/assets/f33cb244-0fec-4325-8dd2-0f8eb6b35c9e" />   

Let's conduct a broad syn scan and then narrow our scan to just the ports we identify in the original scan. I'll use the following syntax:   
* `nmap -sS -Pn --disable-arp-ping -n [target ip]`   
* `nmap -sT -sV -sC -p [ports] [target ip]`   

<img width="1263" height="536" alt="image" src="https://github.com/user-attachments/assets/83e00da8-4c1d-411b-9608-e057d1ddc768" />   

Quickly, we found that the server is running an instance of MariaDB (version 5.5.5-10.3.27). To interact with this, we need a software client. The software client we can use for this is mariadb
* -h, --host=name     Connect to host.
* -p, --password[=name] 
* -u, --username
* -P, --port=#        Port number to use for connection (0-3306 default).
* -t, --table         Output in table format.
* -v, --verbose       Write more. (-v -v -v gives the table output format).

`mariadb -h 10.129.95.232 -P 3306 -u [username] -t`     

After one quick google search for default credentials, we see that there is commonly a root account with unset passwords.    

<img width="1174" height="651" alt="image" src="https://github.com/user-attachments/assets/591e619d-6aee-4947-9d49-7a788b0886df" />     

Lets try using the mariadb syntax to log in with the root account.    

<img width="724" height="87" alt="image" src="https://github.com/user-attachments/assets/56876b29-508f-41e5-85bd-2a8ec3a08e98" />     

Let's look at trying to disable this SSL option to fix our connection.     

<img width="608" height="51" alt="image" src="https://github.com/user-attachments/assets/6976dcf6-eede-4684-bc30-389c65661832" />    

<img width="500" height="103" alt="image" src="https://github.com/user-attachments/assets/94450ada-0e78-429f-8d1a-35b87eb684e0" />     

* Let's add `--ssl=FALSE` and see if that helps.   

<img width="664" height="188" alt="image" src="https://github.com/user-attachments/assets/c0db1f65-1516-4070-b126-b13cc320cc21" />    

* SIDE NOTE: I noticed that I was using a lowercase `-p 3306` flag in the original authentication request. I was meaning to leave the password field blank and it was messing up the authentication. It works without the --sql=FALSE... but we still got there anyway.   

Now that we have an SQL shell on the database service of this server, let's try enumerating what tables we can see as the root user.   

Using the "HELP" option, we can see the following commands available to us as root:   

<img width="856" height="538" alt="image" src="https://github.com/user-attachments/assets/9f0f1eca-942f-4a84-afcd-80dd6f5dc53f" />   

Let's try looking around the underlying linux OS with `system`:   

<img width="958" height="823" alt="image" src="https://github.com/user-attachments/assets/01c60239-2387-4722-9209-9919eb0e1a6e" />  

This is one busy server. I guess it wants us to keep this within the SQL service bounds. But just out of curiosity, I want to try reading what they have in that file.    

<img width="858" height="182" alt="image" src="https://github.com/user-attachments/assets/36e1e713-5092-4a2b-97b6-41019c3f8700" />   

Must be for another FTP challenge. Let's try just inputting some SQL statements to begin enumerating this system from the top down. Starting with the overarching database schema names with: `SHOW DATABASES;`  

<img width="290" height="167" alt="image" src="https://github.com/user-attachments/assets/e77dc7b6-5f9a-4d38-b2ef-6910f3ba3bb2" />  

So, we have four databases stored on this service. The mysql, information_schema, and performance_schema all seem like built-in databases. The obvious outlier is "htb". Let's go ahead and select that database to begin looking through it with: `USE htb` 

<img width="563" height="83" alt="image" src="https://github.com/user-attachments/assets/5331652c-ae12-4299-b41f-29de622a37dd" />    

Now, we know databases consist of tables and those tables consist of columns and rows (like excel sheets). Let's begin analyzing which tables exist with: `SHOW TABLES;`   


<img width="319" height="140" alt="image" src="https://github.com/user-attachments/assets/847e257a-3023-4347-8506-68bbe6371e12" />    

Now, we know there are two tables. Let's look through users. We can use a select statement to choose all the data within this table using `SELECT * FROM users;`   

<img width="368" height="174" alt="image" src="https://github.com/user-attachments/assets/2f562fe6-b1c7-4a1c-adf9-7326be1c9e09" />    

Nothing too interesting here. In another life, we could use these creds to possibly brute-force a webmail server or domain (sequel.htb). For now, let's move onto config with the same type of statement: `SELECT * FROM config;`

<img width="586" height="224" alt="image" src="https://github.com/user-attachments/assets/1456eb0c-8f9d-4f11-a6d3-6489e3fe72e8" />   

This configuration data is very helpful, letting us know that it uses as RADIUS server for authentication, doesn't allow uploads, and has default security. More importantly though, we found our flag for this event... time to enter it!

<img width="620" height="579" alt="image" src="https://github.com/user-attachments/assets/3c2befa2-6727-4ffb-a8e6-7f9eb49ad5f6" />  


Note: Don’t submit the flag that appeared on my screen. It is unique to my account and will cause your account to be flagged for cheating.       
