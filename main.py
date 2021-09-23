#from tkinter import *
from tkinter import *
#from Tkinter import messagebox
from tkinter import messagebox as tkMessageBox
#from Tkinter.filedialog import askopenfilename
from tkinter import filedialog as tkFileDialog
from reduction import Reduction
from nltk.stem import PorterStemmer
import wikipedia
import shortForm
import time
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import modelVC,cosine
import requests #for reading web data
import random
import os
import pdf2text

'''pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"'''
opTA=""
opPA=""
endTime1=0
endTime2=0
heavyWords=""

def freshWindow(): #clear GUI
	ipEntry.delete(1.0, END)
	ipEntry.pack_forget()
	ipLabel.pack_forget()
	opLabel.pack_forget()
	buttonSummary.pack_forget()
	buttonSave.pack_forget()
	buttonSave.pack_forget()
	wordCountEntry.pack_forget()
	wordCountEntry.config(text='-')
	opEntry.pack_forget()
	redRatio.pack_forget()
	buttonupdateRR.pack_forget()
	wikiQLabel.pack_forget()
	wSearchEntry.pack_forget()
	buttonWiki.pack_forget()
	buttonWeb.pack_forget()
	opEntry.delete(1.0,END)
	logLabel.pack_forget()
	buttonClear.pack_forget()
	impWords.pack_forget()
	impWordsLabel.pack_forget()
	buttonImpWords.pack_forget()
	


def packIP(): #pack input area
	ipLabel.pack()
	ipEntry.pack()
	ipEntry.delete(1.0, END)
	buttonSummary.pack()
	#wordCountEntry.pack()
	opLabel.pack()
	opEntry.pack()
	buttonClear.pack()
	opEntry.insert(INSERT, "Enter input first.")
	opEntry.config(state='disabled', fg='#404247', bg='#c8cace')

def newWin():
	freshWindow()
	packIP()	

def openLog(): #display Log
		freshWindow()
		logLabel.pack()
		ipEntry.pack()
		ipEntry.delete(1.0,END)
		with open("log.txt") as f:
			ipEntry.insert(INSERT,f.read())
			
			
def evaluate(): 
	
	count = 0
	stop_words=0
	swFile=open("stopWords.txt").read()
	global opPA,opTA
	
	if len(opPA)<len(opTA):
		for word in opPA:
			#if word not in swFile:
			if word in opTA:
				count+=1
			else:
				stop_words+=1
				
	else:
		for word in opTA:
			#if word not in swFile:
			if word in opPA:
				count+=1
			else:
				stop_words+=1

	den=float(len(opPA)+len(opTA))/2
	value = ((count)/den)*100.0

	tkMessageBox.showinfo("Closeness","Similarity of PA and Text Rank is: %.2f percent\n" %(value))
	
	text = ipEntry.get("1.0", END)
	lenText=len(text)
	with open("perfLog.text", "a+") as f:
		f.write("\n\nInput length: %d" %lenText)
		f.write("\nReduction Ratio: %d" %redRatio.get() )
		f.write("\nSimilarity: %.2f" %value)
		f.write("\nTime(for TR): %.2f " %endTime1)
		f.write("\nTime(for PA): %.2f " %endTime2)
		
	return 1

def close(): #exit
	res=tkMessageBox.askquestion("Exit", "Are you sure to exit?")
	if res == 'yes':
		exit()
	else:
		freshWindow()

def getFile(): #import text file
	freshWindow()
	packIP()
	filename = tkFileDialog.askopenfilename()
	text1 = open(filename, encoding='UTF-8').read()
	ipEntry.insert(INSERT, text1.rstrip(''))

def wikiSearch(): #search wiki
	freshWindow()
	buttonSummary.pack_forget()
	searchTerm = wSearchEntry.get("1.0", END)
	result = wikipedia.page(searchTerm)
	packIP()
	ipEntry.insert(INSERT, result.summary)
	buttonWiki.pack_forget()
	buttonClear.pack_forget()

def getInput2(): #wikipedia search entry
	freshWindow()
	wikiQLabel.pack()
	wSearchEntry.delete(1.0,END)
	wSearchEntry.pack()
	buttonWiki.pack()

def getPdf():
	freshWindow()
	packIP()
	filename = tkFileDialog.askopenfilename()
	text=pdf2text.convert(filename,pages=None)
	ipEntry.insert(INSERT, text)

def getPText(): #paste text
	freshWindow()
	packIP()

def getImage(): #open image file
	freshWindow()
	packIP()
	ipEntry.insert(INSERT,"Loading text from image...")
	filename = tkFileDialog.askopenfilename()	
	
	im = Image.open(filename) 
	im = im.filter(ImageFilter.MedianFilter())
	enhancer = ImageEnhance.Contrast(im)	
	im = enhancer.enhance(2)
	im = im.convert('1')
	im.save('temp2.jpeg')

	pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
	

	text = pytesseract.image_to_string(Image.open('temp2.jpeg'))
	text=processText(text)

	ipEntry.delete(1.0, END)
	ipEntry.insert(INSERT, text)

def processText(text):
		text=text.lower()
		text=text.replace("(","c")
		text=text.replace("8","b")
		text=text.replace("0","o")
		return text

def getInput5(): #web search
	freshWindow()
	wikiQLabel.pack()
	wSearchEntry.delete(1.0,END)
	wSearchEntry.pack()
	buttonWeb.pack()
	
def displayWeb(): #paste web search to ip box
	buttonClear.pack_forget()
	packIP()
	searchTerm = wSearchEntry.get("1.0", END)
	text = requests.get(searchTerm.strip()).text
	#print text	
	ipEntry.insert(INSERT,"Loading...")
	ipEntry.delete(1.0, END)
	ipEntry.insert(INSERT, text.rstrip(' '))
	wikiQLabel.pack_forget()
	wSearchEntry.pack_forget()
	buttonWiki.pack_forget()
	buttonWeb.pack_forget()
	buttonClear.pack()

def impWordsRoutine():
	global heavyWords
	heavyWords = impWords.get("1.0", END)
	newWin()
	#print heavyWords

def updateImpWords():
	freshWindow()
	impWordsLabel.pack()
	impWords.pack()
	buttonImpWords.pack()
	

def getSummary(): #actually calculate summary
	opLabel.pack_forget()
	opEntry.pack_forget()
	buttonSummary.pack_forget()
	wordCountEntry.pack()
	buttonClear.pack_forget()
	buttonSummary.pack()
	opLabel.pack()
	opEntry.pack()
	buttonClear.pack()
	opEntry.config(state='normal' , bg="white" , fg="black")
	opEntry.delete(1.0,END)
	opEntry.insert(INSERT,"Generating Summary...")

	global endTime1,endTime2	
	
	
	startTime = time.time()
	text = ipEntry.get("1.0", END)
	
	temp = str(len(text))
	temp=temp+' characters'
	#print temp
	wordCountEntry.config(text=temp)
	wordCountEntry.config(state='disabled')

	ps = PorterStemmer()
	red_ra=redRatio.get()/100.00
	
	if var1.get():
		words = text.split()
		for w in words:
			text += ps.stem(w)
			text += " "
	
	if var6.get()==1:
		r = Reduction() #object of class Red..
		reduced_text = r.reduce(text, red_ra)
		op=' '.join(reduced_text)
		global opTA
		opTA=op
	elif var6.get()==2:
		m = modelVC.summary()
		global heavyWords
		op = m.summarize(text,red_ra,heavyWords)
		global opPA
		opPA=op


	if var2.get()==1:
		op=shortForm.shortF(op)

	opEntry.delete(1.0,END)
	opEntry.insert(INSERT, op)
	
	if var6.get()==1: 
		endTime1 = time.time() - startTime
		print("Time taken: %f secs" %endTime1)
		if var4.get():
			tkMessageBox.showinfo("Statistics", "Time taken to complete: %f secs" %endTime1)
	
	if var6.get()==2: 
		endTime2 = time.time() - startTime
		print("Time taken: %f secs" %endTime2)
		if var4.get():
			tkMessageBox.showinfo("Statistics", "Time taken to complete: %f secs" %endTime2)

	if var3.get() == 1:
		file_f = open("log.txt", "a")
		lenText=len(text)
		file_f.write("\nInput length: %d" %lenText)
		lenText = len(op)
		file_f.write("\tSummary length: %d" % lenText)
		file_f.write('\nStemming: %d' %var1.get())
		file_f.write('\tShort Forms: %d' %var2.get())
		file_f.write('\tReduction Ratio: %d percent' % redRatio.get())
		file_f.write('\tModel: %d ' % var6.get())
		if var6.get()==1: 
			file_f.write("\nTime taken: %f secs\n" %endTime1)
		if var6.get()==2: 
			file_f.write("\nTime taken: %f secs\n" %endTime2)

		file_f.close()

def getRR(): #set RR
	freshWindow()
	redRatio.pack()
	buttonupdateRR.pack()

def updateSW(): #stopWords.txt editing
	with open("stopWords.txt", 'w+') as f:
		text=ipEntry.get("1.0", END)
		f.write(text)
		f.close()

def showSW(): #display Stop Words in ip box
	buttonSummary.pack_forget()
	ipEntry.pack()
	opLabel.pack_forget()
	opEntry.pack_forget()
	buttonClear.pack_forget()
	with open("stopWords.txt") as f:
		ipEntry.delete(1.0, END)
		text=f.read()
		text=text.strip('/n')
		ipEntry.insert(INSERT,text)
		buttonSave.pack()
		f.close()

def showSF(): #to be done
	tkMessageBox.showinfo("Short Forms", "Instructions:\n"
								"1. Open file /shortForm.py \n\n2. Define needed short form as key value pair, eg. Industry Grade : IG" 									"\n\n3.Save and close the file")
							
	return 1

def showHelp():
	tkMessageBox.showinfo("Help", "Instructions:\n"
								"1. Select suitable input method. \n\n2. Select reduction ratio(size of summary)\n\n3."
								"Select preferences\n\n4."
								"Generate Summary.")

def about():
	tkMessageBox.showinfo("About us", "Version: 13.0.2\n"
									"The Personalized Content Summary Generator"
									"\n\nDeveloped by:\n"
									"Aniket Singh\nZaifa Khan")

def feedback():
	tkMessageBox.showinfo("Feedback", "All rights reserved\n"
									"\nInfo and updates at: https://github.com/khanzaifa37")
def clear():
	ipEntry.delete(1.0, END)
	opEntry.delete(1.0, END)
	wSearchEntry.delete(1.0,END)



#Main GUI begins
root = Tk()

root.title("Content Summary Generator")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
x = (width / 2) - (800 / 2)
y = (height / 2) - (650 / 2)
root.resizable(width=True, height=True)
root.geometry('%dx%d+%d+%d' % (800, 600, x, y))

#Menu Bar with all its elements
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=newWin)
filemenu.add_command(label="Open Log", command=openLog)
filemenu.add_command(label="Evaluation", command=evaluate)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=close)

sourceMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Input", menu=sourceMenu)
sourceMenu.add_command(label="Import text file", command=getFile)
wSearchEntry=Text(root)
sourceMenu.add_separator()
sourceMenu.add_command(label="Web Search", command=getInput5)
sourceMenu.add_command(label="Wikipedia Search", command=getInput2)
sourceMenu.add_separator()
sourceMenu.add_command(label="Paste Text", command=getPText)
sourceMenu.add_command(label="Read text from PDF*", command=getPdf)
sourceMenu.add_command(label="Read text from image(JPG/JPEG)*", command=getImage)

var1 = IntVar() #stem
var2 = IntVar() #SF
var3 = IntVar(value=1) #log
var4 = IntVar() #time display
#var5 = IntVar() #conc
var6 = IntVar(value=2) #textRank #personal algo
prefMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Preferences", menu=prefMenu)
prefMenu.add_radiobutton(label="Text Rank Algorithm", var=var6, value=1)
prefMenu.add_radiobutton(label="Proposed Algorithm", var=var6, value=2)
#prefMenu.add_radiobutton(label="Algorithm 3", var=var6, value=3)
prefMenu.add_separator()
prefMenu.add_command(label="Set Reduction ratio", command=getRR)
prefMenu.add_command(label="Define important words", command=updateImpWords)
prefMenu.add_separator()
#prefMenu.add_checkbutton(label="Concurrency*", var=var5)
prefMenu.add_checkbutton(label="Use Stemming", var=var1)
prefMenu.add_checkbutton(label="Use Short Forms", var=var2)
prefMenu.add_separator()
prefMenu.add_checkbutton(label="Display time stats", var=var4)
prefMenu.add_checkbutton(label="Write to file", var=var3)


editmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Personalize", menu=editmenu)
editmenu.add_command(label="Edit Stop Words", command=showSW)
editmenu.add_command(label="Edit Short Forms", command=showSF)


helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="Help", command=showHelp)
helpmenu.add_command(label="About", command=about)
helpmenu.add_separator()
helpmenu.add_command(label="Feedback", command=feedback)
#Menu Bar ends

#define elements
redRatio = Scale(root, from_=1, to=99, length=300, orient=HORIZONTAL)

redRatio.set(random.randint(5,65))
logLabel = Label(root, text="Log: ")
ipLabel = Label(root, text="Input Text: ")
ipEntry = Text(root, wrap=WORD, width=80, height=15)
opLabel = Label(root, text="Summary: ")
opEntry = Text(root, wrap=WORD, width=80, height=15, fg='#404247', bg='#c8cace')
wordCountEntry = Label(root, width=18, height=1, fg="#56313a")
wSearchEntry= Text(root, width=80, height=1)
wikiQLabel = Label(root, text="Enter Search Query")
buttonWiki = Button(root, text="Search", command=wikiSearch)
buttonWeb = Button(root, text="Search", command=displayWeb)
buttonSummary = Button(root, height=2, width=15, text="Generate Summary", font=(10), command=getSummary, relief="groove")
buttonSummary.config()
buttonSave = Button(root,text="Save to File", command= updateSW)
buttonClear = Button(root, text="Clear", command=clear, relief='groove')
buttonupdateRR = Button(root, text="Update Reduction Ratio", command=newWin)

impWordsLabel = Label(root, text="Important Words (that should carry more weight)")
impWords = Text(root,wrap=WORD, fg='#2ab72c')
buttonImpWords = Button(root, text="Update List", command=impWordsRoutine)

#end of definitions

freshWindow()
packIP()

root.config(menu=menubar)

img = PhotoImage(file='favicon2.png')
root.tk.call('wm', 'iconphoto', root._w, img) 

#root.iconbitmap(r'/home/death/Desktop/favicon.ico')
root.mainloop()
