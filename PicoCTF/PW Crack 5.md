## Name: PW Crack 5 // Difficulty: Medium // Topic: General Skills (python)

#### By: Kyle Zimmer  
 
**Overview: Building on the previous two PW Crack challenges, this one gave us a text document with a newline separated list of over sixty-five thousand passwords to guess. We utilized the readlines python function coupled with the replace function to take in every guess and neatly organize them into a list that we could use to try brute forcing the program.**  
  
<img width="853" height="529" alt="image" src="https://github.com/user-attachments/assets/ab8ad5ce-9cd7-46d3-ad2c-b6a66e983b7b" />  
  
Looking at the description on this challenge, it gives us four files including the password checker program, the encrypted flag file, the hashed binary of the flag, and a new dictionary file. Let’s look closer.
   
<img width="675" height="79" alt="image" src="https://github.com/user-attachments/assets/9175b84a-9753-495f-b785-c9fc7efa0f43" />   
    
Just as before in PW Crack 3 and 4, the .enc and .bin files are just dependencies for the checker program to compare against the user’s input.   
    
<img width="847" height="691" alt="image" src="https://github.com/user-attachments/assets/0dab8ebf-53fa-42b9-b4ca-ee10a63d2f0c" />  
   
Just as before, this script is the exact same. Ignoring the basic XOR function at the top, the program reads the binary data from the .enc and .bin files and stores them to global variables. It then defines two additional functions that hash the password and gather user input that gets hashed and compared to the correct_pw_hash variable defined earlier in order to authenticate the user and produce the flag… only this time it doesn’t give us a predefined list of passwords to try. Lets take a look at that dictionary file.   
   
<img width="518" height="245" alt="image" src="https://github.com/user-attachments/assets/c61f898c-7e10-4d68-9765-6a811bc7b973" />   
   
Using the `head` utility, I was able to get a quick glimpse at what this seems to be and it’s exactly what I thought it was; It’s a brute forcing list of ascending four-digit hexadecimal numbers. Being that there was one password guess per line, I was able to count all lines in the file using the handy `wc -l dictionary.txt` command. OVER SIXTY FIVE THOUSAND GUESSES! That’d take me a lifetime to enter in by hand.   
    
I see what this challenge is needing from me though. I have to take this file and iterate through each line and add each guess to a list that I can easily iterate through in my previous test.py script from PW Crack  3 and 4. I’ve used the readlines() function before; Lets create a script to get these into a list and print it as a proof of concept.    
   
<img width="398" height="142" alt="image" src="https://github.com/user-attachments/assets/7268e56e-22b7-4ead-b653-007372a62949" />   
    
Essentially, this script will open the dictionary.txt file with read permissions and then use the readlines function to add each line to the `lines` variable. I was then able to take that variable containing every line (ending in a newline) and begin to process it into the list `pw_list`. I was able to condense this to one line, making it a little cleaner. Noting some problems with the newline, I just used the replace function on every iteration of the lines variable to swap the character for nothing (“”) and then add it to pw_list = []. The print statements should list the first 20 items and how long the entire list is.     
   
<img width="1304" height="130" alt="image" src="https://github.com/user-attachments/assets/ed2b73c3-877c-4a0a-9f03-a4f7e38e7e2f" />   
   
Perfect. Now lets remove those print statements and add our brute forcing script that we used in the previous two PW Crack challenges. I removed the STDERR output, because the Popen pipe wasn’t receiving any data from the checker programs… Less statements to execute over the course of sixty five thousand guesses.   
   
<img width="521" height="436" alt="image" src="https://github.com/user-attachments/assets/2b528f9b-3861-4397-ab86-4046088613fa" />   
  
Only thing left to do is give it a try and see if it can detect a picoCTF{} flag….

<img width="518" height="198" alt="image" src="https://github.com/user-attachments/assets/934de16b-e261-4359-ac6e-f824b8db8b7c" />  
  
<img width="651" height="95" alt="image" src="https://github.com/user-attachments/assets/7224a217-fcff-41a8-bd35-e4a2eb4a717c" />  

Woops… forgot to add `import subprocess` at the top.    
    
<img width="766" height="689" alt="image" src="https://github.com/user-attachments/assets/a2cf33ea-9bd2-47f3-8940-d662de88d6a5" />    
    
And it’s off!  
  
<img width="668" height="331" alt="image" src="https://github.com/user-attachments/assets/f3b95b4d-1b83-4f1b-ae8e-18d9c437dad9" />  
  
Just like that… worked flawlessly. We retrieved the flag after tens of thousands of guesses. In total, this program found the flag in about two and a half minutes.  


Note: Don’t submit the flag that appeared on my screen. It is unique to my account and will cause your account to be flagged for cheating.
