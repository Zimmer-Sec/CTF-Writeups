## Name: Mongod   //   Difficulty: Very Easy   //   Topic: MongoDB    
#### By: Kyle Zimmer    
       
**Overview: This challenge led me to my first time interacting with a MongoDB instance. After troubleshooting some legecy client software, I was able to connect without credentials and collect the exposed flag!**     


<img width="356" height="121" alt="Screenshot 2025-10-07 113858" src="https://github.com/user-attachments/assets/445dcfad-b54d-4ab2-a333-533b6924c5f8" />   

Let's begin this challenge by testing connectivity to the remote target and then throwing a basic syn scan (-sS) with version scanning (-sV) and help scripts (-sC): `nmap -sS -sV -sC [target ip]`

<img width="776" height="431" alt="image" src="https://github.com/user-attachments/assets/484c69b5-64b3-4bed-a98f-f06a2922d471" />    

The only service open on the device seems to be OpenSSH 8.2p1. The scan also shows that this is an Ubuntu machine. Let's take a look for any specific vulnerabilities tied to this version:    

<img width="830" height="577" alt="image" src="https://github.com/user-attachments/assets/1a898968-cf59-45db-8251-7fef76065768" />    

Being that this doesn't seem like the entire picture I'm supposed to be seeing, I'm going to scan across all (TCP) ports with `-p-`. To speed it up a little, I removed the scripts and version scanning options unitl after I've narrowed down open ports.    

<img width="794" height="985" alt="image" src="https://github.com/user-attachments/assets/64720383-53a5-403e-b6b5-1e6d7438cceb" />     

The output of the mongodb scripts was a bit overwhelming, but there was transportation security, host, and database information. Interestingly, it shows us thast there are currently eleven active clients. The Javascript engine `mozjs` could also prove useful in finding vulnerabilities.    

In order to access the official MongoDB client, `mongosh`, I'll have to download it with curl: `curl -O https://downloads.mongodb.com/compass/mongodb-mongosh_2.5.8-linux-x64.tgz` followed by `gunzip mongosh-2.5.8-linux-x64.tgz` and `tar -xvf mongosh-2.5.8-linux-x64.tar`

That gives me access to the mongosh binary file found in `~/Downloads/mongosh-2.5.8-linux-x64/bin/`. Now we can finally start to interact with this device.

<img width="1064" height="523" alt="image" src="https://github.com/user-attachments/assets/392eedc0-e268-4e90-af11-4cd4f1f84b82" />   

<img width="634" height="76" alt="image" src="https://github.com/user-attachments/assets/291741f2-ced1-4a41-979d-f722d1c2c8a3" />    

I noticed that the documentation stated that the server's MongoDB version had to be higher than 4.2 to work with mongosh. While attempting to connect with the basic `mongosh mongodb://[target ip]:27017`, I received an error confirming this.   

<img width="1258" height="228" alt="image" src="https://github.com/user-attachments/assets/7128a421-6535-47af-8aeb-6ebfbcc458f1" />  

I found that if I went back to the GUI and downloaded the old 1.10.6 version and went through the same process, I was successful.    

<img width="610" height="793" alt="image" src="https://github.com/user-attachments/assets/cefa24e2-d895-4aa8-a389-0f7f80900ee0" />   

<img width="1181" height="525" alt="image" src="https://github.com/user-attachments/assets/e568e630-243b-4432-867a-e75b310b027f" />   

The `show dbs` function reaveals what we saw in our nmap scripts output. Database layers: "admin", "config", "local", "sensitive information", and "users". Let's jump right to he juicy stuff and do `use sensitive_information` to mount onto the database.   

<img width="343" height="37" alt="image" src="https://github.com/user-attachments/assets/ee7f5f1e-0e79-4ae3-be15-6cc2f222d561" />   

Remembering that the database uses a hierarchy of Database -> Collection -> Documents (JSON Data), let's look at the collections within this database with `show collections`:   

<img width="332" height="35" alt="image" src="https://github.com/user-attachments/assets/8121a0e9-ef1d-4e5c-9c56-673b473a416c" />      

and finally, we can denote that `flag` collection in our next command to list all documents within that collection with `db.flag.find()`:    

<img width="435" height="116" alt="image" src="https://github.com/user-attachments/assets/eaffc035-44da-41e5-bc84-cbbda60e1ffd" />    

<img width="680" height="587" alt="image" src="https://github.com/user-attachments/assets/18694636-7491-4697-aede-f0018a2dbb80" />    


Note: Don’t submit the flag that appeared on my screen. It is unique to my account and will cause your account to be flagged for cheating.     
