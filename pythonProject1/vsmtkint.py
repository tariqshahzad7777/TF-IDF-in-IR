from tkinter import *
from main import *
import json
import os

if os.path.exists(r"C:\Users\Tariq Shahzad\PycharmProjects\pythonProject1\finaldict.json"):
    with open('finaldict.json','r') as openfile:
        # Reading from json file
        finaldict=json.load(openfile)
    with open('idfscore.json','r') as openfile:
        # Reading from json file
        idfscore=json.load(openfile)
    with open('docvecs.json','r') as openfile:
        # Reading from json file
        docvecs=json.load(openfile)
else:
    finaldict=preproc()
    json_object=json.dumps(finaldict)
    with open("finaldict.json", "w") as fileobj:
        fileobj.write(json_object)

    idfscore=createidf(finaldict)
    json_object=json.dumps(idfscore)
    with open("idfscore.json", "w") as fileobj:
        fileobj.write(json_object)

    docvecs=tfidfgenerator(finaldict, idfscore)
    json_object=json.dumps(docvecs)
    with open("docvecs.json", "w") as fileobj:
        fileobj.write(json_object)

root = Tk()
root.title("Vector Space Model")
root.geometry("695x800")
root.configure(bg='aquamarine2')
userquery= StringVar()
usercutoff= StringVar()
output= IntVar()
Label(text="Vector Space Model for Information Retrieval",font="Helvetica 24 bold underline",bg='aquamarine2',pady=15).grid(row=0,column=0,columnspan=5)

def searching():
    userthresh=float(usercutent.get())
    userqueryinp=userqueryent.get()
    userqueryinp.lower()
    querylist = userqueryinp.split(' ')
    queryvect = queryvector(finaldict, querylist, idfscore)
    result = cosinesimilarity(docvecs, queryvect,userthresh)
    rankedresult = list(result.items())
    rankedresult.sort(reverse=True)
    resultlist = []
    for i in range(len(rankedresult)):
        resultlist.append(rankedresult[i][1])
    t1.insert(INSERT,resultlist)
    t1.insert(INSERT,"\n")
    t1.insert(INSERT,len(resultlist))

def refreshall(event):
    usercutent.delete("0","end")
    userqueryent.delete("0","end")
    t1.delete("1.0", "end")

def refreshuserquery(event):
    userqueryent.delete("0", "end")
    t1.delete("1.0", "end")


photo= PhotoImage(file="nat.png")
Label(image=photo,bg='aquamarine2').grid(row=1,column=0,columnspan=5)

Label(text="Prepared By: K18-0229",font="Helvetica 18 bold underline",pady=15,bg='aquamarine2').grid(row=2,ipady=5,column=0,columnspan=5)

Label(text="Enter alpha value:", font="Helvetica 14 bold",bg='aquamarine2').grid(row=3,column=0,columnspan=2,sticky="W")
usercutent= Entry(root,textvariable="usercutoff",width="10",font=("Calibri",14))
usercutent.grid(row=3,column=2,ipadx=5,ipady=5,pady=15,sticky=W)
b1 = Button(root, text ="Refresh",font="Helvetica 11 bold",bg="black",fg="azure",relief=RAISED)
b1.grid(row=3,column=3,ipadx=10,ipady=5)
b2 = Button(root, text ="Search",command=searching,font="Helvetica 11 bold",bg="black",fg="azure",relief=RAISED)
b2.grid(row=3,column=4,ipadx=10,ipady=5)

b1.bind('<Button-1>',refreshuserquery)
b1.bind('<Double-1>',refreshall)

Label(text="Enter your query here:", font="Helvetica 14 bold",bg='aquamarine2').grid(row=4,column=0,columnspan=2)
userqueryent= Entry(root,textvariable="userquery",width="39",font=("Calibri",14))
userqueryent.grid(row=4,column=2,columnspan=3,sticky=W,ipadx=5,ipady=5,pady=15)

Label(text="Retrieved documents:(Ranked)",font="Helvetica 14 bold",bg='aquamarine2').grid(row=5,column=0,columnspan=3,sticky=W)
t1=Text(root,height=5,width=56 ,font="Helvetica 14")
t1.grid(row=6,column=0,columnspan=5,pady=10,padx=10)
root.mainloop()
