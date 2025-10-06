## Name: Redeemer   //   Difficulty: Very Easy   //   Topic: Redis    
#### By: Kyle Zimmer    
       
**Overview: In this challenge we got a chance to interact with the in-memory (RAM-managed) database service, Redis using the redis-cli interface to list keys and dump their values.**     
 
<img width="282" height="103" alt="image" src="https://github.com/user-attachments/assets/f7e6c131-b853-4a40-aabe-7cfb69e2ab7b" />     

Like all basic CTFs, let's run some scans against this box. Being that it's a beginner one, I doubt that there's be any scan limitations or firewall blocking. I'll be using the following commands to scan both TCP and UDP:    

`nmap -sS -p- -sV -T4 -sC 10.129.136.187 -Pn --disable-arp-ping -n`      
* -sS: (default with root) TCP Syn Stealth (S, SA, RST)     
* -p-: all ports     
* -sV: versions, service names, and details   
* -T4: [Speed](https://nmap.org/book/performance-timing-templates.html) of scanning (0-5) (0=paranoid, 3=normal, 5=insanely loud) CAUTION, THESE MAY LESSEN TIME, BUT MIGHT MISS HOSTS OR PORTS    
* -sC: helpful scripts    
* -Pn: Disable ping before scan. (time saver)     
* --disable-arp-ping: Disable layer two arp ping before scan (time saver)    
* -n: Disable dns resolution (time saver)     

`nmap -sU --top-ports=10000 -sV -sC -Pn -n -T4 10.129.136.187`     

<img width="764" height="191" alt="image" src="https://github.com/user-attachments/assets/2d7fb42c-442c-4784-886d-f56b0b1de166" />    

Good thing we let those run together. The `-p-` option was useful in identifying this server hosting Redis 5.0.7 on TCP port 6379. Let's see if there are any nmap scripts that exist for redis enumeration. I accomplish this regularly by using `locate scripts/[service_name]`    

<img width="382" height="78" alt="image" src="https://github.com/user-attachments/assets/c86f1bd0-6f49-4f0b-91ed-adce7035095e" />   

Let's try out the redis-info script with `nmap -sV --script=redis-info.nse -p 6379 10.129.136.187`    

<img width="763" height="475" alt="image" src="https://github.com/user-attachments/assets/90efe0de-f9c9-4e60-a823-286011e06593" />    

That's a lot of good information. Let's try banner grabbing for anything additional. We'll use good ol' netcat: `nc -nv [target ip] [r_port]`    

<img width="378" height="76" alt="image" src="https://github.com/user-attachments/assets/d50bca46-d3ad-4f4b-92c3-8a989a4815b8" />      

Well... we learned that it was open... again. Let's try interacting with it using the most popular utility: Redis CLI. We can aim this at our target machine (host) with the -h option: `redis-cli -h [target ip]`    

<img width="311" height="55" alt="image" src="https://github.com/user-attachments/assets/34de12a4-c800-4112-8e3c-534dd530f18c" />    

The [HackTricks](https://book.hacktricks.wiki/en/network-services-pentesting/6379-pentesting-redis.html#manual-enumeration) forum gave a good idea of first checking the system for interesting data by using the `info` redis command.   

<img width="457" height="548" alt="image" src="https://github.com/user-attachments/assets/e03ebd40-28c9-476b-9758-18b0bd78cdd5" />   

This data confirms what our NSE script already. Let's now take a look at who is all connected to this database with `client list` (not expecting anything other than myself, but still good to understand importance of this device.)    
We can also take a look at the full configuration key-value dump with `config get *`

<img width="1227" height="277" alt="image" src="https://github.com/user-attachments/assets/cdd9c096-5d13-45e3-8acd-ba196f0d139c" />    

This type of information is valuable to attackers, but for this situation we'll need to look the more simple features. Let's (risky) dump all the key names on this server with `keys *`.    

<img width="272" height="99" alt="image" src="https://github.com/user-attachments/assets/a6760432-c92d-458d-adac-379fbc0633a2" />   

Knowing that Redis stores data in the form Key:Value, we can use the `dump` command to extract the value of listed keys, more importantly the flag key: `dump flag`    

<img width="531" height="117" alt="image" src="https://github.com/user-attachments/assets/e1ab33b4-6de2-4411-adb8-cfc4cb5ee386" />   













Note: Don’t submit the flag that appeared on my screen. It is unique to my account and will cause your account to be flagged for cheating.     
