## Name: Three   //   Difficulty: Very Easy   //   Topic: S3 Reverse Shell    
#### By: Kyle Zimmer    
       
**Overview: **     

<img width="267" height="103" alt="image" src="https://github.com/user-attachments/assets/604ce017-f0f4-4e51-a528-cabe5b2a6566" />    

Getting started, let's start with our usual port scan, followed by a more in-depth version and script scan against the identified ports:  
- `sudo nmap -sS -Pn -n --disable-arp-ping --top-ports 10000 [target ip] -oG`   
- `sudo nmap -sT -Pn -n --disable-arp-ping -O -sV -sC -p [port1,port2] [target ip]`   
- If we suspect UDP and we have the time: `sudo nmap -sU -Pn -n --disable-arp-ping [target ip]`   

Being that we know this box is likely to be a Linux web server with a back-end S3 bucket storage utility, I'll move forward confidently with just the top 1500 ports and then looking at those TCP ports closely...     
   
<img width="686" height="197" alt="image" src="https://github.com/user-attachments/assets/b4800901-6be1-4f16-87f2-9956ff138348" />    

<img width="868" height="417" alt="image" src="https://github.com/user-attachments/assets/d2e569ba-586a-43a8-932d-f3eb0ec5a6aa" />   

Let's look at the HTTP headers and response we get from this web server using curl:    
- `curl -v [target ip]`

<img width="937" height="605" alt="image" src="https://github.com/user-attachments/assets/6a4d240a-2ae8-4433-ac7a-9e51cd345ecd" />   

Everything seems to load correctly. Looks like a music group's band page with contact information and tour data. Let's see how this renders in our browser.  

<img width="1388" height="984" alt="image" src="https://github.com/user-attachments/assets/62ddcfb1-e3dd-4b18-a12d-6c645e206546" />   

<img width="984" height="822" alt="image" src="https://github.com/user-attachments/assets/46f24992-e5d0-4519-b878-e06cab5329e5" />   

The "Buy Tickets" section doesn't really work.   

The contact section seems to have some functionality with its backend being made-up by PHP code. It's sends your inputted data to **action_page**.php?Name=...&Email=...&Message=... 

<img width="1175" height="290" alt="image" src="https://github.com/user-attachments/assets/e7be8294-b61e-4fc8-b164-e8a57de3475a" />   

I don't entirely know what this means, but we will note it as a data point. Wildcards, file paths, and remote urls give the same results.  Other than that, all the buttons at the top are just redirectors to sections of the static page. The search feature at the top also doesn't work. Let's look for some hidden directories on this server with gobuster:

One other thing I noticed in the contact section was the email domain they're using. It's different than the IP we used to access their sites. Let's try and resolve the domain: thetoppers.htb on both HTTP and HTTPS.
  
<img width="1181" height="757" alt="image" src="https://github.com/user-attachments/assets/769b40c1-87ab-4ba7-8164-2c38fc3fd480" />  

Hmm... Let's just add it as the domain pointing to the IPv4 address we just visited by adding it to our /etc/hosts file. `sudo vim /etc/hosts`

<img width="499" height="224" alt="image" src="https://github.com/user-attachments/assets/2e40e684-bc7a-4130-b970-ee9122d695fd" />  

And now to test it...   

<img width="1388" height="697" alt="image" src="https://github.com/user-attachments/assets/205e0d12-0530-4fe9-8a77-8304f5d68dbe" />   

Like a charm. Okay. We have a domain pointing to an IP address... We know it's SSH accesssible (no creds)... let's quickly test passwordless logins for SSH.   

<img width="680" height="779" alt="image" src="https://github.com/user-attachments/assets/99652136-400f-4126-b970-59869df13dc9" />   

Worth the shot, but didn't work. Let's go after hidden directories (+ robots.txt) and then subdomains using gobuster!  
- `sudo gobuster dir --url thetoppers.htb --wordlist /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt --ne`  
- `sudo gobuster dns --domain thetoppers.htb -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt`  
- `sudo gobuster vhost -u http://thetoppers.htb -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt -r --ad`   

<img width="1020" height="369" alt="image" src="https://github.com/user-attachments/assets/1277a568-2fa1-4c86-b814-302ad70910b9" />

No interesting resources in the subdirectories that I could find...   

<img width="1035" height="415" alt="image" src="https://github.com/user-attachments/assets/5f45b517-c919-41db-b68e-7978f6b12a6e" />

Even after changing `--resolver /etc/hosts`, I still couldn't get it to validate the base domain or find any subdomains of the main site.  

<img width="1040" height="391" alt="image" src="https://github.com/user-attachments/assets/7d361120-3af5-4962-97c7-94a716b6b6c5" />   

Looks like Virtual Hosts (VHost) scanning is what I was looking to find behind the domain. Let's try and resolve it in our /etc/hosts.




Note: Don’t submit the flag that appeared on my screen. It is unique to my account and will cause your account to be flagged for cheating.       
