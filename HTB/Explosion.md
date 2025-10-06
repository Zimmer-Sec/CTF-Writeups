## Name: Explosion   //   Difficulty: Very Easy   //   Topic: RDP    
#### By: Kyle Zimmer    
       
**Overview: In this challenge, we discovered a domain-joined machine that had an Administrator account without a password set and RDP open. We were able to enumerate the domain information and guess our way into a desktop GUI.**     
 
<img width="254" height="119" alt="image" src="https://github.com/user-attachments/assets/fea8e011-daeb-4d66-9366-4b9012822e83" />  

Let's jump into this challenge with a basic nmap scan against all TCP ports using my go-to:    
`nmap -sS -sV -T4 -sC -Pn --disable-arp-ping -n [target ip]`    
Results:   
<img width="769" height="585" alt="image" src="https://github.com/user-attachments/assets/67d8959f-4700-44f1-a76a-430d52323137" />   

Though, I know this Windows device challenge is going to be tailored towards the RDP service, I want to quickly check out the SMB service to see if there's any data stored on it that might help us with this challenge.    

First step: I'll try and use smbmap to list out any shares and permissions granted to my user WORKGROUP\kali: `smbclient -h [target ip] -u kali`    

<img width="764" height="388" alt="image" src="https://github.com/user-attachments/assets/76359cd6-1ee7-4d9a-9dad-572e78cf2f23" />     

And just to prove that there's nothing of use in the IPC$ share:   

<img width="451" height="188" alt="image" src="https://github.com/user-attachments/assets/8918eaab-5380-41e6-8f2a-8363745afc4c" />    

Now we can move onto the RDP service. I first want to go back and make sure I ran all possible RDP scripts in the Nmap Scripting Engine. To do so, I use `locate script/rdp` and then run all with `--script=rdp*:    

<img width="780" height="606" alt="image" src="https://github.com/user-attachments/assets/f085bd38-df59-4036-b8fd-ec1b46023df5" />    

With this information, let's begin to play with the most popular linux rdp client: xfreerdp3. We can use `xfreerdp3 /u:Administrator /v:10.129.1.13 /dynamic-resolution +clipboard` to attempt to use the usual "Administrator" username.     

<img width="1255" height="763" alt="image" src="https://github.com/user-attachments/assets/854dc267-9723-4f4a-8f06-9a6cf7bf9771" />     
<img width="500" height="102" alt="image" src="https://github.com/user-attachments/assets/5bde97cf-68ad-4584-a647-ac21e94aba55" />    

Using the data from the NMAP script, I guessed the domain name to be "EXPLOSION" like we saw in the NTLM data.

<img width="1027" height="802" alt="image" src="https://github.com/user-attachments/assets/6339c0fd-affd-451a-b075-42807125fee6" />   

Money! Let me make this full screen thanks to the `/dynamic-resolution`. Also, what's this? A text file called "flag.txt" on the desktop?    
<img width="290" height="275" alt="image" src="https://github.com/user-attachments/assets/26e3c90b-ad4a-4dc1-9fb6-ce9058934a6f" />       
<img width="510" height="169" alt="image" src="https://github.com/user-attachments/assets/fd427cf4-d8df-43d7-bc5f-4399183ea093" />    
<img width="512" height="498" alt="image" src="https://github.com/user-attachments/assets/6c63ce62-7a38-41d1-a42d-f408319030b8" />     
Note: Don’t submit the flag that appeared on my screen. It is unique to my account and will cause your account to be flagged for cheating.     



