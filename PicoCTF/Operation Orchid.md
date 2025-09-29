## Name: Operation Orchid // Difficulty: Medium // Topic: Forensics
#### By: Kyle Zimmer


**Overview: This challenge requires the use of a disk image analyzer to query through directories to discover hidden encrypted files. I had to identify the decryption cipher, credentials, and options while circumnavigating roadblocks and rabbit-holes in order to uncover the flag.**  

<img width="858" height="534" alt="image" src="https://github.com/user-attachments/assets/226c3b72-a576-4e62-9073-4092a5a604aa" />  
  
Jumping into this challenge, we’re provided with a disk.flag.img.gz file.	 
  
<img width="1259" height="222" alt="image" src="https://github.com/user-attachments/assets/f804000b-7b90-4672-b60d-10bfc2fc3e32" />  
  
I confirm that this file is compressed with gzip (obvious from the file extension), but I just like to double-check. I then go along to decompress it with `gunzip disk.flag.img.gz`. This leaves us with an uncompressed disk image file to begin analyzing.  
  
Just like in my, “Disk, disk, sleuth! II” writeup, we’re going to begin looking at this image file’s partitioning from the media layer using [The Sleuth Kit (TSK)](https://wiki.sleuthkit.org/index.php?title=The_Sleuth_Kit) to get a higher level overview of the system’s layout.   
  
<img width="717" height="208" alt="image" src="https://github.com/user-attachments/assets/58058247-6d45-4f91-bf0d-2be66a726211" />  
  
The output from our `mmls disk.flag.img` command revealed that this drive is nix-like, has 512-byte blocks, and has multiple different partitions. The first partition we see (001) is an empty 2048 bytes. The second (002) is a 204800-byte partition that could be a primary file system. The third (003) looks to be a swap partition (dedicated virtual memory space used for performance when the system’s RAM is at full capacity). The fourth and last (004) partition is the largest at 407552-bytes, likely acting as the main file system.  
  
We can begin to look into these closer by just quickly browsing each memory offset’s filename layer using TSK’s fls utility.  
  
<img width="610" height="684" alt="image" src="https://github.com/user-attachments/assets/0c365b6e-beec-49b0-b337-27fc08593c75" />  
  
`fls -o [offset] disk.flag.img` gives us a clear printout of the file name layer of each partition. The first (002) partition’s offset (00002048) revealed files related to the syslinux bootloader. I don’t think we need to be looking in that direction. The second (003) partition’s offset (206848) revealed that it doesn’t have an ordinary file structure as expected. The last partition (004) showed us a very readable ext4 file structure.  
  
Without a real direction to follow on trying to find this flag, I’m going to use a previous trick to just skim the file name layer for the keyword “flag” using `fls -a -r -o 411648 disk.flag.img | grep flag`  
  
<img width="695" height="76" alt="image" src="https://github.com/user-attachments/assets/250fd472-a020-4e17-a1cb-c0ef4a0990fa" />  
  
Well that as easy! The command showed us that there is a flag.txt, but what’s interesting is that it says (realloc) next to the inode number. This means that this file was removed and the memory that it had taken up has likely been overwritten, but we may be able to recover and read some of it! The other file’s name likely implies that it is encrypted in some form.  
  
Lets go ahead and read the data with `icat -o 411648 disk.flag.img 1876` and `icat -o 411648 disk.flag.img 1782`  
  
<img width="691" height="162" alt="image" src="https://github.com/user-attachments/assets/cc43b0b2-c4e8-4df3-9417-90dfbe8103e7" />  
  
The initial assumption we had about the flag.txt.enc file was right, but the flag.txt file outputted what appears to be a pair of… coordinates? I guess I can throw those in Google Maps to try and find some hint or clue.  
<img width="765" height="641" alt="image" src="https://github.com/user-attachments/assets/7c15a5d4-b889-47da-81d7-74ad1cff4bc1" />  
<img width="1075" height="519" alt="image" src="https://github.com/user-attachments/assets/dcbd6cdf-208b-4944-8685-916def1f7e19" />  
  
After spending about an hour cycling through the surrounding area and switching around the coordinates, I’ve come up with nothing. I’ve hit a road block and I think I should dedicate time to other parts of this disk.  
  
Looking back at that encrypted file, I can export it to my local system and run file against it to try and get a further clue using `icat -o 411648 disk.flag.img 1782 > flag.txt.enc`  
  
<img width="840" height="174" alt="image" src="https://github.com/user-attachments/assets/cedb6c89-76b8-4ed9-bf83-4b79d571942d" />  
  
Looks like the user of this file system had encrypted the file.txt with openssl and a salted password (also see in the file’s contents “Salted_…”  
  
I could try putting together some form of password list that I’d brute force against the file to try and decrypt it, but that could take some time… Maybe there are some other artifacts that could give me a clue.  
  
After piping the output of `fls -r -a -o 411648 disk.flag.img > fls_out` and tracking where the flag files came from, I see that it was /root.   
<img width="361" height="193" alt="image" src="https://github.com/user-attachments/assets/4a8a89e2-c53f-41cc-9600-b686d01bc50f" />  
  
Weirdly enough, there’s only one other file in the same directory as the flag files… coincidence?  
This appears to be a simple history file for the Almquist Shell. Hopefully the inode reveals some data that pushes us in the direction that we need for this decryption.  
<img width="668" height="230" alt="image" src="https://github.com/user-attachments/assets/650e8ba0-c7a6-4982-aba3-1aa8f22d74cf" />  
  
The admin broke a big rule that openssl themselves even warn you about… entering your passwords in plain text on the command-line! We see that from this history file, the user/admin created the flag, opened thefile for editing (writing the flag), encrypted it, and then deleted and overwrote the memory with `shred -u flag.txt` Using this information, we can reverse the openssl command to decrypt the file using the supplied password. `openssl enc -d -aes256 -salt -in flag.txt.enc -out flag.txt.dec -k unbreakablepassword1234567`  
  
<img width="1184" height="128" alt="image" src="https://github.com/user-attachments/assets/d34011e6-b4c6-41ae-806b-d927e5302850" />  
  
We see that the command threw a “bad decrypt” error, but also produced the flag.txt.dec file. We might as well open it up and see if it’s still ciphertext.  
  
<img width="586" height="43" alt="image" src="https://github.com/user-attachments/assets/a1b80b17-8f26-4cf3-b734-4d67bde28cb2" />  
  
Regardless of the error, we still were able to print uncover the PicoCTF{} flag!  
  
Note: Don’t submit the flag that appeared on my screen. It is unique to my account and will cause your account to be flagged for cheating.  
