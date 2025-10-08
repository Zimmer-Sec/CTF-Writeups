## Name: Synced   //   Difficulty: Very Easy   //   Topic: RSync    
#### By: Kyle Zimmer    
       
**Overview: After noticing an open Rsync service without any authentication modules present, I was able to list shared folders and incrementally (fully) download files to my local system.**     

<img width="367" height="189" alt="image" src="https://github.com/user-attachments/assets/66a21d05-c325-42bb-ab34-d4a74b1e2a5f" />   

Let's get this started with a quick syn-scan without dns resolution and ICMP/ARP pings. I'll then add on deeper (service version and script scans when I narrow down the open ports.     

For this, I'll use `nmap -sS -Pn --disable-arp-ping -n [target ip]` -- followed by adding the `-sV -sC`     

<img width="786" height="369" alt="image" src="https://github.com/user-attachments/assets/9dafb049-3e20-4d1b-9407-f5e0c0b710c8" />      

It looks like the "Sync" box is hosting RSync on it's default port, 873. We see that it's version 31. We can begin looking for vulnerabilities in that release.     

Rsync is a free software and is used for transferring incremental filesystem/file updates between remote systems. We can use the `rsync` command utlity to interact with this server. Being that we have no indication of credentials, we can begin with seeing if the good ol' anonymous login is allowed on this device.      

Being that the -sC script: `--script rsync-list-modules` didn't show any results... there's a good chance that there's no authentication required.   

We can list files using `rsync -av --list-only rsync://[target ip]/` and hopefully it doesn't prompt for creds (Thanks [HackTricks](https://book.hacktricks.wiki/en/network-services-pentesting/873-pentesting-rsync.html#manual-rsync-usage))      

<img width="420" height="64" alt="image" src="https://github.com/user-attachments/assets/29d8a2f5-c1c6-479c-9f63-22ddab18c3d6" />    

So we see that there are two shares. Let's begin by poking our nose inside public with `rsync -av --list-only rsync://10.129.228.37/public`    

<img width="493" height="143" alt="image" src="https://github.com/user-attachments/assets/85eda4ec-620e-4f7e-af54-a43280e6dea1" />    

And just like that, it acts just like an `ls -l`, presenting us with a file called flag.txt. Removing the --list-only option and adding a local directory to incrementally update to will download the file to our system: `rsync -av rsync://10.129.228.37/public .`    

<img width="421" height="272" alt="image" src="https://github.com/user-attachments/assets/84b44f00-df61-4478-87d4-96713bcde785" />     

<img width="687" height="597" alt="image" src="https://github.com/user-attachments/assets/97742d6c-dbec-44d3-bcae-6d9815138997" />    

Note: Don’t submit the flag that appeared on my screen. It is unique to my account and will cause your account to be flagged for cheating.  
