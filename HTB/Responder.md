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

/inc/ included nothing besides some jquery and font libraries. So what... we have an IP redirecting us to a domain that we can't resolve while also hosting a backend full of webpage resources? This smells like there's an issue with the `unika.htb` domain. If it's supposed to resolve, maybe our system just doesn't know how to. Let's document it in our /etc/hosts file so that the domain will resolve to the Responder box's IP address and load those backend resources.  

<img width="506" height="143" alt="image" src="https://github.com/user-attachments/assets/0cda8836-1387-4515-9cc8-f3e95e65e9a2" />  

<img width="1272" height="972" alt="image" src="https://github.com/user-attachments/assets/d3966914-a652-455b-b7d7-5c84859ad021" />  

Just as expected. It loaded the images from the /img directory and contains all the javascript functionality outlined in the /js and /inc directories! Now, let's poke around and see what this site offers.
<img width="1276" height="1161" alt="image" src="https://github.com/user-attachments/assets/1ad99f16-6425-4567-afdd-fe7f476f62a5" />  
 
The site is a pretty static page with beautifully scrolling photos and designs. There's a customer feedback form that appears to do nothing at the bottom. All the buttons at the top drop us down to sections of the main scrolling page... except one.

The EN button gives a little pop-out box, allowing you to select French (FR) or German (DE) language packs to translate the page.

<img width="1274" height="825" alt="image" src="https://github.com/user-attachments/assets/7e29ff79-61d5-4a18-96ea-ec7e764f13a8" />   

Whats interesting about that is the url. I see that it changes to include a `?page=[new page file.html]` at the end. Lets try monkeying with this file name. I'll trying throwing in flag.txt for shits and giggles.

<img width="1132" height="229" alt="image" src="https://github.com/user-attachments/assets/5bd11131-3d9b-4660-8eb8-3ddbdec0b22d" />   

included([FILE NAME])... `C:\xampp\htdocs\index.php` Does this service just let us search/navigate the windows file system? 

So what do we know? 
* This server is letting us attempt to include files on the page based on the url parameter `?page=`
* We're located in C:\xampp\htdocs\ [index.php]
* This web server is an Apache / PHP server.
* The underlying OS is Windows.

Let's google for some common xampp apache file paths of interest. After some searching, I found a wordlist already prepped that contained the C:\xampp\apache\) directory: 

<img width="977" height="575" alt="image" src="https://github.com/user-attachments/assets/018a1f04-3564-4955-82d1-f06d857cf091" />  

Let's begin throwing these after the `?page=..` entry...

<img width="1272" height="822" alt="image" src="https://github.com/user-attachments/assets/a84d27b8-9b00-4e11-a4fa-2766a2b5328f" />     

`..\apache\conf\httpd.conf` worked! This gives us the server configuration file. Lots to take in here. Let's see if we can go back past the C:\xampp\ folder... to C:\

<img width="999" height="222" alt="image" src="https://github.com/user-attachments/assets/1a7768d7-f4aa-44bb-a6cf-7a6d8e0d30c9" />  

Oh we can try searching anywhere on the NTFS and maybe more.









Note: Don’t submit the flag that appeared on my screen. It is unique to my account and will cause your account to be flagged for cheating.       
