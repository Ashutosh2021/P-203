import socket
from threading import Thread
from tkinter import *

# nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))

class GUI:

    def __init__(self):
        self.window=Tk()
        self.window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")

        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=400)
        
        self.pls = Label(self.login,
					text = "Please login to continue",
					justify = CENTER,
					font = "Helvetica 14 bold")
        self.pls.place( relheight = 0.15,
                        relx = 0.2,
                        rely = 0.07)
        
        self.labelName = Label(self.login,
							text = "Name: ",
							font = "Helvetica 12")
        self.labelName.place(relheight = 0.2,
							relx = 0.1,
							rely = 0.2)
        
        self.entryName = Entry(self.login,
							font = "Helvetica 14")
        self.entryName.place(relwidth = 0.4,
							relheight = 0.12,
							relx = 0.35,
							rely = 0.2)
        self.entryName.focus()

        self.go=Button(self.login,text="CONTINUE",font="Helvetica 14 bold",command=lambda: self.goAhead(self.entryName.get()))
        self.go.place(relx=0.4,rely=0.55)
        self.window.mainloop()

    def goAhead(self,nickname) :
        self.login.destroy()
        self.name=nickname

        receive_thread = Thread(target=self.receive)
        receive_thread.start()
        self.layout(self.name)
    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    self.showMsg(message)
            except:
                print("An error occured!")
                client.close()
                break

    def write(self):
        self.textCons.config(state=DISABLED)
        while True:
            message =input('')
            client.send(message.encode('utf-8'))
            self.showmsg(message)
            break

    def layout(self,name):
        #self.name = name
        self.window.deiconify()
        self.window.title("CHATROOM")
        self.window.resizable(width = False,
							height = False)
        self.window.configure(width = 470,
							height = 550,
							bg = "#17202A")

        self.labelHead = Label(self.window,
							bg = "#17202A",
							fg = "#EAECEE",
							text = self.name ,
							font = "Helvetica 13 bold",
							pady = 5)
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.window,
						width = 450,
						bg = "#ABB2B9")
        self.line.place(relwidth = 1,
						rely = 0.07,
						relheight = 0.012)
        self.textCons = Text(self.window,
							width = 20,
							height = 2,
							bg = "#17202A",
							fg = "#ffffff",
							font = "Helvetica 14",
							padx = 5,
							pady = 5)
        self.textCons.place(relheight = 0.745,
							relwidth = 1,
							rely = 0.08)
        
        self.labelBottom = Label(self.window,
			   					bg="#ABB2B9",
								height=80)
        self.labelBottom.place(relwidth=1,rely=0.825)
        self.entryMessage = Entry(self.labelBottom,
			    				bg="#2C3E50",
								fg="#EAECEE",
								font="Helvetica 13")
        self.entryMessage.place(relwidth=0.74,
			  					relheight=0.06,
								rely=0.008,
								relx=0.011)
        self.entryMessage.focus()
        self.buttonMessage = Button(self.labelBottom,
			      					text="Send",
									font="Helvetica 10 bold",
									width=20,
									bg="#ABB2B9",
									command=lambda : self.sendButton(self.entryMessage.get()))
        self.buttonMessage.place(relx=0.77,
			   					rely=0.008,
								relheight=0.06,
								relwidth=0.22)
        self.textCons.config(cursor="arrow")
        self.scrollBar = Scrollbar(self.textCons)
        self.scrollBar.place(relheight=1,relx=0.974)
        self.scrollBar.config(command=self.textCons.yview)
		
    def sendButton(self,msg) :
        self.textCons.config(state=DISABLED)
        self.msg=msg
        self.entryMessage.delete(0,END)
        
        send=Thread(target=self.write)
        send.start()

    def showmsg(self,msg) :
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END,msg+"\n\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

		


g=GUI()