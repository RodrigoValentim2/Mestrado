from tkinter import *
from  movimento import Movimento as mv
 
class Application:
	def __init__(self, master=None):
	    self.fonte = ("Verdana", "20")
	 
	    self.container1 = Frame(master)
	    self.container1["pady"] = 10
	    self.container1.pack()
	    self.container2 = Frame(master)
	    self.container2["padx"] = 200
	    self.container2["pady"] = 5
	    self.container2.pack()
	    self.container3 = Frame(master)
	    self.container3["padx"] = 200
	    self.container3["pady"] = 5
	    self.container3.pack()
	    self.container4 = Frame(master)
	    self.container4["padx"] = 20
	    self.container4["pady"] = 5
	    self.container4.pack()
	    self.container5 = Frame(master)
	    self.container5["padx"] = 20
	    self.container5["pady"] = 5
	    self.container5.pack()
	    self.container6 = Frame(master)
	    self.container6["padx"] = 20
	    self.container6["pady"] = 5
	    self.container6.pack()
	    self.container7 = Frame(master)
	    self.container7["padx"] = 20
	    self.container7["pady"] = 5
	    self.container7.pack()
	    self.container8 = Frame(master)
	    self.container8["padx"] = 20
	    self.container8["pady"] = 10
	    self.container8.pack()
	    self.container9 = Frame(master)
	    self.container9["pady"] = 150
	    self.container9.pack()
	 
	    self.titulo = Label(self.container1, text="Informe os dados :")
	    self.titulo["font"] = ("Calibri", "25", "bold")
	    self.titulo.pack ()
	 
	    self.number_palheta = Label(self.container2, 
	    text="Núemro da palheta:", font=self.fonte, width=30)
	    self.number_palheta.pack(side=LEFT)
	 
	    self.txtnumber_palheta = Entry(self.container2)
	    self.txtnumber_palheta["width"] = 20
	    self.txtnumber_palheta["font"] = self.fonte
	    self.txtnumber_palheta.pack(side=LEFT)
	 
	   
	    self.lblnumber_amostra= Label(self.container3, text="Número da amostra:", 
	    font=self.fonte, width=30)
	    self.lblnumber_amostra.pack(side=LEFT)
	 
	    self.txtnumber_amostra = Entry(self.container3)
	    self.txtnumber_amostra["width"] = 20
	    self.txtnumber_amostra["font"] = self.fonte
	    self.txtnumber_amostra.pack(side=LEFT)
	 
	   
	 
	    self.bntAlterar = Button(self.container8, text="Run", 
	    font=self.fonte, width=12)
	    self.bntAlterar["command"] = self.run
	    self.bntAlterar.pack (side=LEFT)

	def run(self):
	    mv.run(self.txtnumber_palheta.get() ,self.txtnumber_amostra.get())
	



	   
	 
	 
	 
	 
	 
	
 
 
root = Tk()
Application(root)
root.mainloop()
