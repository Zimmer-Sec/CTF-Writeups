## Name: Responder   //   Difficulty: Very Easy   //   Topic: NTLM    
#### By: Kyle Zimmer    
       
**Overview: **     

<img width="309" height="110" alt="image" src="https://github.com/user-attachments/assets/608006ee-f7d1-427c-a4b4-2c11ce922b20" />       

Let's begin by running a quick TCP Syn and UDP scan against the top 10,000 ports with no regard for staying silent: `sudo nmap -sS --disable-arp-ping -Pn -p- -sU [target ip] -T5 --top-ports 10000`   

<img width="780" height="212" alt="image" src="https://github.com/user-attachments/assets/8055705c-0a12-4ce8-8f08-1da98ad52004" />   

Now, let's focus our more intensive version and script scans at those three TCP ports with: `sudo nmap -sT -p 80,5985,7680 -sC -sV -O [target IP]`   

<img width="1039" height="368" alt="image" src="https://github.com/user-attachments/assets/be29e5b7-91fe-4b91-9a50-3120b6056ef2" />      

No title on that web server... hmm... Let's try and grab the headers with `curl -i -v [url]`    

<img width="568" height="445" alt="image" src="https://github.com/user-attachments/assets/1877630f-e9d8-478a-afe3-fb2663588124" />    

Weird. It's wanting to refresh our page with a "unika.htb" domain that doesn't seem to exist. My next idea is to let gobuster run to try and find directories behind this web server. I'll start with `gudo gobuster dir --url [target ip] --wordlist /usr/share/dirbuster/wordlists/directory-list-2.3-small.txt --ne -r` (ne = no errors, -r = follow redirects (recursive))    

<img width="796" height="462" alt="image" src="https://github.com/user-attachments/assets/5fb68628-0634-4ad2-98fa-2df060215376" />    

Taking a look at the good results. HTTP status 403 = Forbidden. HTTP status 503 = Maintenance. HTTP status 200 = STATUS OK!   

<img width="834" height="720" alt="image" src="https://github.com/user-attachments/assets/5bcb147a-ae06-4f43-ab94-7a5f953561eb" />   

Not much to see, but I'll take note of `Apache/2.4.52 (Win64) OpenSSL/1.1.1m PHP/8.1.1 Server`. We may be able to use this information later. Also, I found a Thumbs.db composite document File V2 that I don't currently understand, but we can also come back to this after I look at the other directories.

<img width="518" height="214" alt="image" src="https://github.com/user-attachments/assets/ff6ead74-833e-499c-8d30-8a30d354922c" />   

<img width="812" height="349" alt="image" src="https://github.com/user-attachments/assets/c087fa50-b9b6-4ad8-8442-b2e0acba85a8" />   

Theme.js didn't show us much besides the javascript functionality to animated page features.

<img width="943" height="463" alt="image" src="https://github.com/user-attachments/assets/2b3203c1-f22b-4bd5-a565-ed6fb3dc338e" />

Nothing out of the ordinary here. Styling sheets for css.  

<img width="943" height="626" alt="image" src="https://github.com/user-attachments/assets/1535d9b5-f71d-42f0-b43f-3783d1eb1c0f" /> 

/inc/ included nothing besides some jquery and font libraries.




Note: Don’t submit the flag that appeared on my screen. It is unique to my account and will cause your account to be flagged for cheating.       
