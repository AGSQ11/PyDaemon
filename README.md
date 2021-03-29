# PyDaemon
A simple Python daemon listening for commands to execute

Baiscally it listens to your server's port and address defined in daemon.py line 18 and 19 and executes to local machine all commands received via POST in the "data" input.

The "data" value should be base64_encoded. 

Also an authorisation key should be send in the "key" input, plaintext. 

For experimenting purposes and to reduce accidental posts, I've placed an IP restriction as well, which can be changed from config.cfg.


I'm not really familiar with Python, so, if you have any suggestion for improving this little daemon script, feel free to submit your ideea. :)
