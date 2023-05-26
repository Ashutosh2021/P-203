import socket 
from threading import Thread
import random

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000


server.bind((ip_address, port))
server.listen()

list_of_clients = []
nicknames=[]

print("Server has started...")

questions=[
    "What is the Italian word for PIE ?\na.Mozarella\nb.Pasty\nc.Patty\nd.Pizza",
    "Water boils at 212 units at which scale ?\nFahrenheit\nb.Celsius\nc.Rankine\nd.Kelvin",
    "How many wonders are there in the world ?\na.4\nb.7\nc.9\nd.3",
    "What element does not exist ?\na.Xf\nb.Ra\nc.Si\nd.Pa"
    "How many states are there in india ?\na.24\nb.30\nc.29\nd.31",
    "Hg stands for ?\na.Mercury\nb.Argenine\nc.Calcium\nd.Halfinum",
    "What is the smallest continent ?\na.Antarctica\nb.Australia\nc.Africa\nd.America"
    "Which planet is closest to the Sun ?\na.Venus\nb.Earth\nc.Pluto\nd.Mercury"
    "Who gifted the statue of liberty to the US ?\na.France\nb.Germany\nc.Africa\nd.Russia"
    "How many bones does a human body have ?\na.205\nb.200\nc.206\nd.210"
]

answers=["d","a","b","a","c","a","b","d","a","c"]

def get_random_qna(conn):
    random_index=random.randint(0,len(questions)-1)
    random_question=questions[random_index]
    random_answer=answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index,random_question,random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)


def clientthread(conn,nickname):
    score=0
    conn.send("Welcome to this quiz game!".encode('utf-8'))
    conn.send("You will receive a question. The answer to the question should be one of a,b,c and d".encode('utf-8'))
    conn.send("Good Luck!\n\n".encode('utf-8'))
    index,question,answer=get_random_qna(conn)
    
    while True:
        try:
            message=conn.recv(2048).decode('utf-8')
            if message:
                if message.lower() == answer:
                    score+=1
                    conn.send(f"Bravo! your score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect Answer! Better luck next time!")
                remove_question(index)
                index,question,answer=get_random_qna(conn)
            else:
                remove(conn)
        except:
            continue

while True:
    conn, addr = server.accept()
    conn.send("NICKNAME".encode("utf-8"))
    nickname = conn.recv(2048).decode("utf-8")
    list_of_clients.append(conn)
    nicknames.append(nickname)
    print (nickname + " connected")
    new_thread = Thread(target= clientthread,args=(conn,nickname))
    new_thread.start()
