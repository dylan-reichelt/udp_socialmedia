# udp_socialmedia
A small social media service made with UDP, created for my Computer Networks Class CSE434 at ASU. This was made 
to be a small Twitter like application. You are able to subscribe, login, etc.

## Installation

Make sure to have my python_aes.py application setup. As this program uses that for encryption and decryption of 
the data sent back and forth between the server and the client (Instruction on how to install that in that readme).

On the server side simply cd to /server
```bash
python3 main.py
```

On the client side simply cd to /client
```bash
python3 main.py
```

## Usage
Built in users and passwords (They are read from the users.txt file but the passwords are hashed):

dylan&programmer,
max&gamer,
sina&backwoods,
rob&friend,
alex&loser

Commands for the client (server side is all handled on its own, there is nothing to interface with)
```python
login#dylan&programmer
subscribe#max
unsubscribe#max
post#this is a post
retrieve#1
logout#
```

All the above command are things you can do once logged in.

Note: You can have multiple connections at a time, as well as get real time messages when online.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. 
This is for a class so there won't be too many changes once the assignment is done.

## License
[MIT](https://choosealicense.com/licenses/mit/)
