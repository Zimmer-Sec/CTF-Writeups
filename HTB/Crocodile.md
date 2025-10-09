## Name: Crocodile   //   Difficulty: Very Easy   //   Topic: FTP & HTTP    
#### By: Kyle Zimmer    
       
**Overview: In this challenge, we finally were able to utilize operational data from one machine to pivot into another. Our target was seen running a vulnerable version of FTP which led us to credentials to log into the web server's admin account.**     

<img width="329" height="111" alt="image" src="https://github.com/user-attachments/assets/78aef3ad-8e43-44f5-a036-93a6cb0bf2fc" />   

Let's conduct a broad syn scan and then narrow our scan to just the ports we identify in the original scan. I'll use the following syntax:  
* `nmap -sS -Pn --disable-arp-ping -n [target ip]`   
* `nmap -sT -sV -sC -p [ports] [target ip]`   

<img width="858" height="709" alt="image" src="https://github.com/user-attachments/assets/2a60db7e-1bea-48b2-806f-5aab186448d1" />   

We found vsftpd 3.0.3 open along with an apache 2.4.41 server running on an Ubuntu distribution. The useful scripts option informs us that the FTP service actually allows anonymous logins.    

Using the ftp (tnftp) client, we can attempt to login with the anaonymous option: `tnftp -a [target]`   
* I have a note from the last FTP ctf stating that if my connect looks to be hung, try adding `anonymous@` along with the port at the end.   

<img width="324" height="147" alt="image" src="https://github.com/user-attachments/assets/4f197c31-b0b3-4a52-8539-fc7909e4563d" />   

Now that we have an FTP shell, let's look around and see what's available to the anonymous (public) user account.   

<img width="1411" height="498" alt="image" src="https://github.com/user-attachments/assets/c0563b32-e9b5-47e5-9990-d0d8e0328749" />   

After using the `pwd` + `ls` + `get` commands, we've found and collected a few files appearing to be user credentials that we might be able to escalate with.   

<img width="311" height="224" alt="image" src="https://github.com/user-attachments/assets/c6e35295-e8ea-46a6-b41a-2a2f3fe557d5" />   

We can try logging back into FTP for more information, but first, let's take a look at that web server that was running on 80.    

<img width="1273" height="1117" alt="image" src="https://github.com/user-attachments/assets/b3825764-a5df-4ab8-85bc-d29c1e5c284e" />   

<img width="1180" height="542" alt="image" src="https://github.com/user-attachments/assets/95a4dff8-df02-4fbc-81f0-3a611f9dc420" />     

This is a static website that has broken buttons and a feedback form at the bottom that doesn't actually send your information anywhere. This site also doesn't appear to have any login page visibly accessible. Let's run our good ol' directory fuzzing tool to confirm this: `gobuster dir --url [target ip] -w /usr/share/wordlists/directory-list-2.3-small.txt`    

<img width="940" height="368" alt="image" src="https://github.com/user-attachments/assets/1fd34332-e180-4a8c-b16d-e3d25e35685b" />      

Very quickly, we discovered a dashboard directory. Let's see what's on it.     
 
<img width="1275" height="1119" alt="image" src="https://github.com/user-attachments/assets/fed88f1f-cae2-4bc8-b3d6-f893107d3a70" />     

Interesting... before it'd let me get to the dashboard (probaby administrative dashboard, it is requiring me to fill out an login.php form.    

<img width="467" height="329" alt="image" src="https://github.com/user-attachments/assets/4466f77d-bccf-408a-8123-bb34670ac723" />     

We remember that PHP uses a `#` for a comment. This type of input should be validated and not allowed within usernames, but it's not. To begin, we can attempt to login with just credentials and if those combinations don't work, we can attempt to use SQL injection.    

Let's begin with the username `admin` and the passwords from top to bottom `root -> Supersecretpassword1 -> @BaASD^9032123sASD -> rKXM59ESxesUFHAd`   

<img width="414" height="329" alt="image" src="https://github.com/user-attachments/assets/7b9fb3a9-53aa-4c04-8dda-4a07d154af5c" />   

Failed.     

<img width="467" height="368" alt="image" src="https://github.com/user-attachments/assets/ea25f4fd-24c3-4e24-8a1e-03b74c9b7e57" />      

Failed.   

<img width="362" height="340" alt="image" src="https://github.com/user-attachments/assets/307b506a-eaa3-434b-8a63-bd651b69b039" />   

Failed.   

<img width="444" height="354" alt="image" src="https://github.com/user-attachments/assets/259ae456-6365-4594-8378-69f319b1aa19" />   

Worked!: `rKXM59ESxesUFHAd`  ---- I knew I should've just used what lined up in the files... oh well! We still got to the same destination.    

<img width="1779" height="1169" alt="image" src="https://github.com/user-attachments/assets/dd7c12cc-8157-4565-b3d1-209e7bca80f6" />    

We're presented with a fake server management page that could've led us to uncover some very valuable information and potential lateral movement... but they instantly provided us the flag for this event. Let's go ahead and enter it on the HTB challenge.    

<img width="535" height="501" alt="image" src="https://github.com/user-attachments/assets/714c8083-f737-4c80-b619-7b65642c1d54" />    


Note: Don’t submit the flag that appeared on my screen. It is unique to my account and will cause your account to be flagged for cheating.     
