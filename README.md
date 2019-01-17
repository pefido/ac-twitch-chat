# ac-twitch-chat
### Assetto Corsa twitch chat app  
<br/>

**What does the app do ?**  
It provides to a streamer the ability to have the online twitch chat of his channel in the in-game app.

**How does it work ?**  
It uses IRC api and URL api of twitch.

**What are the features ?**  
* Chat message from stream channel
* Color lines by nickname ( 13 different colors)
* hide chat if there are no new messages in the last 2 minutes
* minimum interface for vr users

**How i can install it ?**  
Download latest Archive zip file.
Extract it on the app folder (default is : C:\Program Files (x86)\Steam\steamapps\common\assettocorsa\apps\python )
go into the twitch folder extracted and edit the ini file following the comment instruction.

```
Code:
host = irc.chat.twitch.tv  ;irc host for twitch api
port = 6667  ;Port of twitch irc(6667 or 443 for ssl)
nick = youre_username   ; username in lowercase
pass = youre_oauthkey ; in example : oauth:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx generate from here : https://twitchapps.com/tmi/
chan = #youre_username;  in lower case with # before channel name 
Don't leave these lines commented on ini file
```  
To generate your oauth key go here : https://twitchapps.com/tmi/

the chan name is basically the streamer username prefix by a #  

<br/>

Support the original creator:  
### Original app page:
https://www.racedepartment.com/downloads/twitch-chat.13076/
