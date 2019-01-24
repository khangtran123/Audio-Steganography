# Audio-Steganography
This will be my Final Year Project that focuses on steganography in the form of audio files that includes using either MP3 or WAV files as the carriers. 


# Here’s the list of features that would be included in this software are:

  •	Data Encryption using AES 256-bit Standards – All compressed datafiles that are converted into bit characters will have to be             encrypted using AES 256-bit standards to provide extra security measures during the transfer of the embedded audio file to another         third-party person. 
  
  •	Public and Private Keys – All embedded audio carrier files must follow the public and private key schematics where only the               authenticated person receiving the file can decode the file to get the hidden content. This is implemented to add extra security           measures as a precaution, in-case the file gets into the wrong hands.
  
  •	Steganography Encoding Process – This feature allows the user to compress, encrypt, embed the data file into the audio carrier file       that is protected with a private without distorting the audio quality. 
  
  •	Steganography Decoding Process – This feature allows the third-party person to validate their identity via the shared private key and     decode the embedded audio file to retrieve the hidden contents the sender hid. 


# This GUI application will allow any user to easily embed data files of their choice into an audio file that can be covertly transmitted to another third-party user. The GUI will include the following frames:

  •	Main Menu --> a) Encode
              --> b) Decode

  •	Encoding Setup --> a) Datafile: Browse File Dialog for data file to hide
                   --> b) AudioCarrier: Browse File Dialog for audio file to be the carrier
                   --> c) Directory: Browse Folder Dialog for saved audio output destination
                   --> d) Passphrase: User enters passphrase that will be used as Assymetric Key to lock the file
                   --> e) Begin: User clicks button that will save all entries and directs them to next page (Begin Encoding)
              
  •	Begin Encoding --> a) Begin Embedding: User clicks this button to being the embeddement process. The user is presented with a                                 progress bar that shows the percent completed and will be notified when the file has been embedded.
                   --> b) Main Menu: Option will appear only after the process has been completed. 
                   
  • Decoding Setup --> a) Datafile: Browse File Dialog for embedded audio file
                   --> b) Passphrase: User enters passphrase that will be used (Private Key) to unlock the file. The user will be                                 notified if the passphrase does not match to the shared key and will not be able to retrieve the data file to                           ensure protection of sensitive data.
                   --> c) Begin: User clicks button that will save all entries and directs them to next page (Begin Decoding)
              
  •	Begin Decoding --> a) Begin File Retrieval: User clicks this button to being the decoding process. The user is presented with a                               progress bar that shows the percent completed and will be notified when the file has been retrieved from the                             audio carrier file.
                   --> b) Main Menu: Option will appear only after the process has been completed. 
           

