# Welcome to Teleolx!
Hi, I'm very proud that you found my piece of code in gitHub. You met here my bot for telegram messenger called **`teleolx`**. It has a wide range of uses cases from collectors hunting for rare items to scalpers trying to quickly buy rare things from market or just for handyman looking for specific spare parts.

The principle of operation is that every specified time, bot downloads json from the olx portal set to a specific phrase - in this example we are looking for the phrase "xperia". He saves the data in the database and if the new ad is unique, it sends you a telegram notification.

For proper operation, it needs a file with the configuration of your previously created telegram bot and your own chat id. The file must be named "teleolx.cred" and placed in the directory from which `main.py` will be running. The content of the file should be json style:

>**{**  
**"TOKEN": "your bot token here",**   
**"CHAT_ID": "your chat id here"**  
**}**

### Complications:
If you have a problem with any aspect of using the bot, e.g. you can't prepare a json request for a specific phrase, you don't have a server where you could run it, or you encounter any other problems feel free to contact me via telegram at https://cyberwron.t.me/