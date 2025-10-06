## Name: Dancing   //   Difficulty: Very Easy   //   Topic: SMB    
#### By: Kyle Zimmer    
       
**Overview: This challenge presented us with a good introduction to interacting with SMB servers and exploiting their guest logins to access files that were a little _too_ valuable to other workgrouped systems.**     
 
<img width="286" height="112" alt="image" src="https://github.com/user-attachments/assets/7fb07e00-a090-461b-8659-c9092d063764" />   

After connecting our Kali linux VM to the HTB VPN, I started off by performing a basic connectivity test and basic syn-stealth version scan using `nmap -sV [target ip]`   

<img width="762" height="432" alt="image" src="https://github.com/user-attachments/assets/ba3d9259-dae2-44e2-9ff7-cb1e702f8acb" />    

These scan results reveal that it's a Windows box running SMB coupled with RPC, Netbios Sessions Service, and an HTTP API service. Here's a quick overview of each service's purpose:    
* TCP Port 135: Remote Procedure Call (RPC) Endpoint Mapper/Locator: enables clients to query the server to locate RPC-based services. The Endpoint Mapper responds with the dynamic port number where the requested RPC service is running. The client then connects to that dynamic port to execute remote procedures, allowing the server to process the request and return the results.    
* TCP Port 139: NetBIOS Session Service (NetBIOS-SSN): Legacy protocol for file and printer sharing, as well as other network services, by establishing sessions for data exchange between devices using the NetBIOS protocol. Should be disabled on interfaces if legacy (SMBv1) systems aren't in use (heavily targeted by vulnerabilities like WannaCry).    
* TCP Port 445: Server Message Block (SMB): Used to mount network shares for remote access. Historically (SMB v1.0), this service operated using Netbios Over TCP's (NBT) port TCP 139 for session services, port TCP/UDP 137 for name services, and port UDP 138 for datagram services. On modern day systems, NetBios may still be open to support older OS versions, but can expose mounted shares. We can interact with both of these ports to understand the full attack surface.    
* TCP Port 5985: Windows HTTP API: Used for admins to execute remote management tasks, such as executing PowerShell commands, managing system configurations, and monitoring servers via WinRM.    

So, what should we look at first? NSE Scripts are always a good starting point. I'll try out a -sC to throw common scripts, including `--script=smb-os-discovery.nse`     

<img width="830" height="429" alt="image" src="https://github.com/user-attachments/assets/3a093cbe-28ef-439d-8460-5d19a0529d56" />      

It looks like we can only get some data from the HTTP API service. Let's try basic interaction with the utility for talking to an SMB server, smbclinet.     

<img width="1237" height="175" alt="image" src="https://github.com/user-attachments/assets/bbadf45d-9061-476f-9ce5-8b53416f61e2" />   

From the usage output, we see that all the uses in brackets are optional. Some of the more useful looking options are:   
* [-I|--ip-address=IP]   
* [-p|--port=PORT]   
* [-U|--user=[DOMAIN/]USERNAME%[PASSWORD]]   
* [-N|--no-pass] AND/OR [--password=STRING]   
* (from man page) -L|--list allows you to look at what services are available on a server.   
* (from man page) -B|--browse Browse SMB servers using DNS   
  
I'll start by just simply trying to list the services with `smbclinet -L [target ip]` and seeing what its use is.   

<img width="752" height="431" alt="image" src="https://github.com/user-attachments/assets/d0bdd346-2653-4e8b-a843-e40a2b65642e" />    

I went back and modified the syntax to include `smbclient -N`, which removed that kali login prompt. As we see in the photo, we are successfully able to view four shares on the system. ADMIN$, C$, IPC$, and "WorkShares"! We also see that it tries to fallback to requesting SMBv1 (legacy), but fails because this device has it disabled (also seen in the smb-protocols script output).      

<img width="515" height="313" alt="image" src="https://github.com/user-attachments/assets/a116ada7-dafe-43e8-8e38-51cce965c593" />    

  
Before we try and connect to any shares, let's see if we can enumerate any user accounts with a common nmap scrit: `nmap -p 445 --script smb-enum-users.nse [target ip]`  

<img width="530" height="173" alt="image" src="https://github.com/user-attachments/assets/b6255284-8ca1-4e4c-afe3-523512604916" />     

Nothing... Let's try interacting with every one of the shares to see if any anonymous/guest logins are allowed. For that I'll have escape the \\IP and \sharename: `smbclient \\\\[target ip]\\ADMIN$`   

<img width="378" height="81" alt="image" src="https://github.com/user-attachments/assets/48134f39-9947-4f98-8a2a-0d0b9d24e83d" />   

Let's move on and try the other three shares with the same syntax.   

<img width="641" height="454" alt="image" src="https://github.com/user-attachments/assets/56a15d9b-d033-4c8e-8927-2ec825801350" />     

The C$ default share yields no access. The Remote $IPC share gives us read access, but there are no files to be found at the root of the directory structure. Lastly, the WorkShares gives us access with just our personal workgroup credentials!   

I'll leave a table at the bottom for SMB commands. They're very similar to linux/ftp! Now, I'll use `ls`, `cd`, and `get` to move around the filesystem and pull what looks interesting to me (flag).    

<img width="894" height="421" alt="image" src="https://github.com/user-attachments/assets/fbbbcf51-82cc-421f-83a7-b8d5652790c6" />    
    
<img width="381" height="218" alt="image" src="https://github.com/user-attachments/assets/aeb990cf-daac-4d68-985f-7ba95ea9539e" />    

Clear as day! Now let's enter it into the system.     
   
<img width="527" height="499" alt="image" src="https://github.com/user-attachments/assets/3fdd0f30-ff70-40f1-968f-e95cc4aac2ac" />      
    
Note: Don’t submit the flag that appeared on my screen. It is unique to my account and will cause your account to be flagged for cheating.     
