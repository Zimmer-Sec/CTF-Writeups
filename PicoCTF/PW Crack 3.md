## Name: PW Crack 3 // Difficulty: Medium // Topic: General Skills (python)

#### By: Kyle Zimmer  
 
**Overview: This challenge required me to analyze a python script that uses multiple functions to read in encoded and encrypted data only accessible by a valid password. I chose to write a program to iterate through the given passwords and output the flag.**  
  
<img width="855" height="550" alt="image" src="https://github.com/user-attachments/assets/6e5ad9ef-dbbb-4019-a2fd-b226d1b59f1c" />   
    
Starting with the hint, we know that there are seven passwords in the checker script and only one is correct. I'll start by reviewing that python script.   
   
<img width="850" height="771" alt="image" src="https://github.com/user-attachments/assets/a85efe70-2de1-4fc2-bf19-ff475cf952be" />    
     
Analyzing this python script, we have three functions declared, one of which is a generic string object XOR function that the author tells us won't even help. At the bottom, we see a list containing the passwords clear as day (insecure).     
     
Though there's may not be much cracking to do, I can enter these passwords by hand or via script to get the flag. With this little of passwords, It'd be faster to do it by hand compared to writing out the an entire script, but I'll still do it, because it may prove useful in bruteforcing future passwords.       
    
<img width="666" height="267" alt="image" src="https://github.com/user-attachments/assets/5950b42a-a9b8-49d1-832d-7b9edad217ed" />    
   
I included this photo because I wanted to show that the binary and encrypted files are unreadable. It also shows the functionality of the checker script. The checker shows that the hash.bin file is a binary hash of the password used to compare against the user's input. The encrypted file is another encrypted binary text file that is read into the checker to compare.   
   
<img width="598" height="432" alt="image" src="https://github.com/user-attachments/assets/d1c72866-65ad-439e-b850-27bd76bab6fe" />   
   
Using the subprocess library, I was able to create this test script to open the program with `proc = subprocess.Popen([“python3 lvl3_checker.py”]` and then send the standard in, standard out, and standard error to their own respective pipes while telling the process that it’s handling ordinary text (opposed to raw binary data).  
   
I then used `proc.communicate(input=var)` to send my iterated password guess to stdin of the opened program. **I had some problems getting it to relay the enter key to submit the password, but I remedied this by sending a newline appended to the guess.**    
   
The program then begins printing the stdout and stderr (I had to use .strip() because the output always contained a trailing newline character). If the program notices the word “pico” (flag) in the output, it’ll stop the program because we will have found our flag (cracked the password).    
    
<img width="523" height="232" alt="image" src="https://github.com/user-attachments/assets/ef74c38d-77bd-4f4e-9bb2-2ed9f9d4cc9b" />    
   
After modifying the program's execution bit, I'm now able to run it!     
    
<img width="670" height="323" alt="image" src="https://github.com/user-attachments/assets/24605997-cd9c-41d7-b0c4-7f270a4094db" />     
   
And after just three password attempts, we see that the script executed flawlessly! I'll link my code [HERE](https://github.com/Zimmer-Sec/CTF-Writeups/blob/main/PicoCTF/PWcrack3.py) if you'd like to copy and modify it to your needs.    
    
Note: Don’t submit the flag that appeared on my screen. It is unique to my account and will cause your account to be flagged for cheating.   
