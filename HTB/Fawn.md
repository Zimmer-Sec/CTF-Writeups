## Name: Fawn   //   Difficulty: Very Easy   //   Topic: FTP    
#### By: Kyle Zimmer    
       
**Overview: After a basic scan, we noticed the server host FTP with a configuration that allowed for anonymous logins, allowing us to pull the file of interest.**     

<img width="260" height="109" alt="image" src="https://github.com/user-attachments/assets/7f0852dd-ddc6-45ba-b0dd-a21080b9e15b" />     

Let's get into this. I'll choose to connect to the VPN server using `sudo openssl [vpn file]`   

<img width="1246" height="263" alt="image" src="https://github.com/user-attachments/assets/50526e78-1026-4760-873c-5cd11f875080" />   

Let's now test reachability with the `ping` utility.   

<img width="544" height="179" alt="image" src="https://github.com/user-attachments/assets/35232ca0-a538-4679-a0fa-41d18e0a1896" />   

And now a basic service version scan using `nmap -sV [target IP]`   
  
<img width="753" height="204" alt="image" src="https://github.com/user-attachments/assets/eb110b3e-9bc2-4a01-bbd2-e605fa997a40" />     

Looks like we found a singular service open. I'll note the specific version of FTP found (vsftpd 3.0.3) and the box being Unix. I'll do a quick search to see if there are any obvious public CVEs with `searchsploit vsftpd 3.0.3`:    

<img width="375" height="142" alt="image" src="https://github.com/user-attachments/assets/edf845a9-e2dc-4b87-b015-152ae03c6c72" />    

Denial of service doesn't really interest me here. I'll move onto the most basic features of insecure FTP... anoonymous authentication! Simply attempting to login with username "anonymous" and an empty password could give us an easy win!    
  
<img width="343" height="189" alt="image" src="https://github.com/user-attachments/assets/7bed5a1d-1fb1-4602-9a63-0628129c9e17" />    

The command `ftp> help` will show us a listing of commands that we can use within the ftp service. I want to see where we're operating and what's within it, so i'll use the `pwd` and `dir` (or `ls`) commands.   

<img width="557" height="136" alt="image" src="https://github.com/user-attachments/assets/2ee19191-0d9d-4ca0-8bfd-585257d0db31" />    

Now that we see we have a file of interest in front of us, we can use FTP's `get [filename]` command to download it to our current directory on Kali.   

<img width="1253" height="115" alt="image" src="https://github.com/user-attachments/assets/3824ef32-a496-470f-8416-03aa0515d1d5" />   

Now all that's left is to print out the contents with `cat flag.txt`.   

<img width="513" height="339" alt="image" src="https://github.com/user-attachments/assets/a2cb3317-6649-42e1-b0ae-e9f719723513" />    
    
<img width="569" height="499" alt="image" src="https://github.com/user-attachments/assets/46cb416a-94cb-453d-a459-4eb63e79dce9" />  
  
Note: Don’t submit the flag that appeared on my screen. It is unique to my account and will cause your account to be flagged for cheating.  
