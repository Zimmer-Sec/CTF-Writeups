## Name: Meow   //   Difficulty: Very Easy   //   Topic: Telnet    
#### By: Kyle Zimmer    
   
<img width="268" height="99" alt="Screenshot 2025-10-05 230858" src="https://github.com/user-attachments/assets/134b9389-2911-44d1-a7d2-02f702837d50" />    
    
**Overview: Utilizing some core functionalities of Kali linux, we exploited the box's use of passwordless Telnet authentication to gain a root shell.**   
  
<img width="1258" height="205" alt="image" src="https://github.com/user-attachments/assets/58d77d11-d2b8-48ab-96a8-b1b58694a1d1" />    

Using my own Kali linux VM, I used the openvpn binary to connect to HackTheBox's VIP VPN Server in order to establish a tunnel interface to the victim box. To get our first picture of this device, we can use a basic nmap scan to get an idea using the Syn Stealth (default) and version scan option:     

<img width="786" height="216" alt="image" src="https://github.com/user-attachments/assets/1b55f35f-246b-4c46-9bf3-9f79eb82ed75" />     

Knowing that telnet is the obvious port that this CTF is wanting us to look at, I can start using nmap's scripting engine (NSE) to look closer. Also knowing that telnet is inherently insecure, transmitting data in plain-text, I want to see if it has encryption enabled.     

<img width="523" height="182" alt="image" src="https://github.com/user-attachments/assets/05e75e7a-5d64-46d2-8e82-d24318c26338" />      

Looks like `nmap -p 23 --script telnet-encryption 10.129.1.17` provided little info. Knowing this is a linux box (as seen in the first nmap scan), there's no need to look for NTLM data using `--script telnet-ntlm-info`. Let's try to banner this with netcat and retrieve some basic information.     

<img width="367" height="81" alt="image" src="https://github.com/user-attachments/assets/6c35de2b-d9ae-4cb1-9d3a-054218a2297f" />      

Nothing... Let's move onto testing for the basic anonymous (no username and no password) and passwordless (username and no password) logins used by admins to host public files.  Syntax: `telnet 10.129.1.17 23`        

<img width="482" height="249" alt="image" src="https://github.com/user-attachments/assets/76be4088-4513-4ebc-9b0c-bcbe1a83d399" />   

Knowing this is a linux box, we can test root, user, test, and maybe admin/administrator.      

<img width="627" height="767" alt="image" src="https://github.com/user-attachments/assets/2d8c33c5-3f4a-4690-afe8-f8b22fcbedbd" />      

Before I could even try to enter a blank password, the passwordless feature gave us a shell as root on the host machine "Meow"!      

We can now begin to look around for something of interest.    

<img width="563" height="296" alt="image" src="https://github.com/user-attachments/assets/d5a2a2f2-d8a4-4a21-9c55-6ee547142d56" />      
   
<img width="582" height="280" alt="image" src="https://github.com/user-attachments/assets/d385b411-fcdd-41b5-88bf-ebbe9f9891ea" />   

<img width="549" height="492" alt="image" src="https://github.com/user-attachments/assets/e467e973-316a-4b80-bb21-7a3ab7fb2750" />    
    
Note: Don’t submit the flag that appeared on my screen. It is unique to my account and will cause your account to be flagged for cheating.
