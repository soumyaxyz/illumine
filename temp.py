#Surrogator: Tool to identify open access surrogates of access-restricted scholarly articles.
#Version: 2.3
#Written by TYSS Santosh, NDLI, IIT Kharagpur, India

#This software may be used for non-commercial purposes only.

#We request you to cite the following references in any article that is based on work that uses this tool.

# T. Y. S. S. Santosh, Debarshi Kumar Sanyal, Plaban Kumar Bhowmick, and Partha Pratim Das. 2018. Surrogator: A Tool to Enrich a Digital Library with Open Access Surrogate Resources. In Proceedings of ACM/IEEE Joint Conference on Digital Libraries, Poster Track (JCDL’18).
# T. Y. S. S. Santosh, Debarshi Kumar Sanyal, and Plaban Kumar Bhowmick. 2018. Surrogator: Enriching a Digital Library with Open Access Surrogate Resources. In ACM India Joint International Conference on Data Sciences and Management of Data, Demo Track (CoDS-COMAD’18).

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#N.B. This software has been developed as part of a research project and is likely to contain bugs. We will be delighted to receive your feedback on the software including bug reports and bug fixes.
#N.B. Tested on CentOS Linux release 7.3.1611 (Core), Python 3.6 only 


from importlib import reload
import sys
import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import requests
from bs4 import BeautifulSoup
from collections import Counter
import math
import numpy as np
import re
import webbrowser
import time
from nltk.corpus import stopwords
from nltk import download
from nltk import PorterStemmer
import gensim.models.keyedvectors as word2vec
from gensim.models.wrappers.fasttext import FastText
#from gensim.models import Word2Vec
from selenium import webdriver
from urllib.request import urlopen
import pandas as pd
import numpy as np
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from numpy import linalg as LA



class combodemo(QWidget):
    
    def __init__(self, parent = None):
      super(combodemo, self).__init__(parent)
      
      layout = QVBoxLayout()
      layout1 = QHBoxLayout()
      layout2 = QHBoxLayout()
      layout3=QHBoxLayout()
      layout4=QHBoxLayout()
      self.cb = QComboBox()
      #self.label = QLabel('\t\t\t\t\t\t\t\t\t\t     Select Source')
      #self.label.show()
      #self.label2 = QLabel('\t   Select Pages')
      #self.label2.show()
      #self.label1 = QLabel('\t                             Select Years')
      #self.label1.show()
      #self.label3 = QLabel('\tUse')
      #self.label3.show()
      #self.label4 = QLabel('\t\t\t     Select Criteria')
      #self.label4.show()
      #self.label5 = QLabel('\t Display Results')
      #self.label5.show()
      #self.label6 = QLabel('\tSimilarity measure')
      #self.label6.show()
      self.cb.addItem("Select Source")
      self.cb.addItem("Google Scholar")
      self.cb.addItems(["NDLI"])
      self.cb1 = QComboBox()
      self.cb1.addItem("Select Years")
      self.cb1.addItem("3")
      self.cb1.addItems(["5","10"])
      self.cb2 = QComboBox()
      self.cb2.addItem("Select Pages")
      self.cb2.addItem("1")
      self.cb2.addItems(["2","3"])
      self.cb3 = QComboBox()
      self.cb3.addItem("Select Metadata")
      self.cb3.addItem("Author & Title")
      self.cb3.addItems(["Author, Title & Abstract"])
      self.cb4 = QComboBox()
      self.cb4.addItem("Select Criteria")
      self.cb4.addItem("Exact match")
      self.cb4.addItems(["Near Match"])
      self.cb6 = QComboBox()
      self.cb6.addItem("Select Similarity (for abstract)")
      self.cb6.addItem("Word Mover's Distance")
      self.cb6.addItems(["Cosine Similarity (BoW)","Cosine Similarity (fastText)"])
      self.cb5 = QComboBox()
      self.cb5.addItem("Select Display Count")
      self.cb5.addItem("Top 1")
      self.cb5.addItems(["Top 2","Top 3"])
      #self.label.setFont(QFont('SansSerif', 8))
      #self.label1.setFont(QFont('SansSerif', 8)) 
      #self.label2.setFont(QFont('SansSerif', 8)) 
      #self.label3.setFont(QFont('SansSerif', 8)) 
      #self.label4.setFont(QFont('SansSerif', 8)) 
      #self.label5.setFont(QFont('SansSerif', 8)) 
      #self.label6.setFont(QFont('SansSerif', 8)) 
      self.e1 = QLineEdit()
      self.e1.setAlignment(Qt.AlignLeft)
      self.e1.setFont(QFont("Arial",20))
      self.b1 = QPushButton("Go")
      self.b1.setCheckable(True)
      self.str=str(0)
      self.b1.clicked.connect(self.btnstate)
      layout.addWidget(self.e1)
      layout1.addStretch()
      #layout3.addWidget(self.label)
      #layout3.addStretch()
      layout1.addWidget(self.cb)
      layout1.addStretch()
      layout1.addWidget(self.b1)
      layout.addLayout(layout3)
      layout.addLayout(layout1)
      layout2.addStretch()
      #layout4.addWidget(self.label4)
      #layout4.addWidget(self.label3)
      #layout4.addWidget(self.label1)
      #layout4.addWidget(self.label2)
      #layout4.addWidget(self.label5)
      #layout4.addWidget(self.label6)
      #layout4.addStretch()
      #layout.addLayout(layout4)
      layout2.addWidget(self.cb4)
      layout2.addWidget(self.cb3)
      layout2.addWidget(self.cb1)
      layout2.addWidget(self.cb2)
      layout2.addWidget(self.cb6)
      layout2.addWidget(self.cb5)
      layout2.addStretch()
      layout2.addWidget(self.b1)
      layout.addLayout(layout2)
      self.listWidget = QListWidget()
      self.listWidget.setVisible(True)
      layout.addWidget(self.listWidget)
      self.b2 = QPushButton("Next")
      self.b2.setCheckable(True)
      self.b2.clicked.connect(self.btn2state)
      layout.addWidget(self.b2)
      
      
      self.setLayout(layout)
      self.setWindowTitle("Surrogator v2.6")
      #self.setWindowTitle("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tSurrogator")
   
    def Clicked(self,item):
        index=self.listWidget.currentRow()
        #print(index)
        giv_years=self.cb1.currentText()
        giv_pages=self.cb2.currentText()
        giv_usage=self.cb3.currentText()
        giv_crit=self.cb4.currentText()
        giv_disp=self.cb5.currentText()
        giv_sim=self.cb6.currentText()
        
        paper=self.listWidget.currentItem().text()
        paper=str(paper).replace("\t","").strip()
        if(giv_years=="Select Years"):
                    giv_years="3"
        if(giv_pages=="Select Pages"):
                    giv_pages="1"
        if(giv_usage=="Select Metadata"):
                    giv_usage="Author & Title"
        if(giv_crit=="Select Criteria"):
                    giv_crit="Near Match"
        if(giv_disp=="Select Display Count"):
                    giv_disp="Top 3"
        if(giv_sim=="Select Similarity (for abstract)"):
                    giv_sim="Cosine Similarity (BoW)"
        if (index%4 == 0 ):
           
            try:
                new_dict=self.obtained_dict[paper]
                url=new_dict[str(paper)]
                webbrowser.open(url)
            except:
                
                pass
        
        if (index%4 == 2 ):
            
            if(paper=="CLICK HERE FOR NEAR MATCH" ):
                    
                    new_index=index-2
                    new_paper=self.listWidget.item(new_index).text()
                    start_time = time.time()
                    newlist,newdict=collect_authoridlink(new_paper,giv_pages,giv_years,giv_usage,giv_crit,giv_disp, giv_sim)
                    timecal=time.time()-start_time
                    timecal="%.2f" % (timecal)
                    #print (newlist)
                    print (newdict)
                    print (timecal)
                    if(newdict!={}):
                        self.obtained_dict.update(newdict)
                    
                    self.listWidget.takeItem(index)
                    

                    if(len(newlist)>0):
                        tempdum =QListWidgetItem("Surrogate :   ( time = "+ timecal +" seconds )")
                        tempdum.setFont(QFont('SansSerif', 8))
                        self.listWidget.insertItem(index,tempdum)
                        i=0
                        while(i<len(newlist)):
                            temp4 =QListWidgetItem('\t\t\t\t\t\t\t\t\t\t\t'+"Upvote :-)    Downvote :-(")
                            #temp4.setIcon(QIcon(r"/home/santosh/tick.jpg"))
                            #temp4.setIconSize(QSize(10, 20))
                            #temp4.setTextAlignment(Qt.AlignRight)
                            temp4.setFont(QFont('SansSerif', 20))
                            temp4.setForeground(QColor('#000000')) 
                            temp4.setFont(QFont('SansSerif',8)) 
                            self.listWidget.insertItem(index+i*4+1,temp4)

                            temp1 =QListWidgetItem('\t'+newlist[i][0])
                            temp1.setForeground(QColor('#1a0dab'))
                            temp1.setFont(QFont('SansSerif', 14)) 
                            self.listWidget.insertItem(index+2+4*i,temp1)
              
                            temp2 =QListWidgetItem('\t'+newlist[i][1])
                            temp2.setForeground(QColor('#006621')) 
                            temp2.setFont(QFont('SansSerif', 10))
                            self.listWidget.insertItem(index+3+4*i,temp2)
              
                            temp3 =QListWidgetItem('\t'+newlist[i][2])
                            temp3.setForeground(QColor('#1a0dab')) 
                            temp3.setFont(QFont('SansSerif', 8))
                            self.listWidget.insertItem(index+4+4*i,temp3)
                            
                               
                            
                            i+=1
                        
                    else:
                         temp1 =QListWidgetItem("No article found.   ( time ="+timecal+" seconds )" )
                   
                         temp1.setFont(QFont('SansSerif', 8)) 
                         self.listWidget.insertItem(index,temp1)
            elif(paper=="CLICK HERE FOR SURROGATES"):
                    new_index=index-2
                    new_paper=self.listWidget.item(new_index).text()
                    new_index2=index-1
                    new_paper1=self.listWidget.item(new_index2).text()
                    start_time = time.time()
                    newlist,newdict=collect_authoridlinkndl(new_paper,new_paper1,giv_pages,giv_years,giv_usage,giv_crit,giv_disp, giv_sim)
                    timecal=time.time()-start_time
                    timecal="%.2f" % (timecal)
                    #print (newlist)
                    print (newdict)
                    print (timecal)
                    if(newdict!={}):
                        self.obtained_dict.update(newdict)
                    
                    self.listWidget.takeItem(index)
                    

                    if(len(newlist)>0):
                        tempdum =QListWidgetItem("Surrogate :   ( time = "+ timecal +" seconds )")
                        tempdum.setFont(QFont('SansSerif', 8))
                        self.listWidget.insertItem(index,tempdum)
                        i=0
                        while(i<len(newlist)):
                            temp4 =QListWidgetItem('\t\t\t\t\t\t\t\t\t\t\t'+"Upvote :-)    Downvote :-(")
                            #temp4.setIcon(QIcon(r"/home/santosh/tick.jpg"))
                            #temp4.setIconSize(QSize(10, 20))
                            #temp4.setTextAlignment(Qt.AlignRight)
                            temp4.setFont(QFont('SansSerif',8)) 
                            self.listWidget.insertItem(index+i*4+1,temp4)

                            temp1 =QListWidgetItem('\t'+newlist[i][0])
                            temp1.setForeground(QColor('#1a0dab'))
                            temp1.setFont(QFont('SansSerif', 14)) 
                            self.listWidget.insertItem(index+2+4*i,temp1)
              
                            temp2 =QListWidgetItem('\t'+newlist[i][1])
                            temp2.setForeground(QColor('#006621')) 
                            temp2.setFont(QFont('SansSerif', 10))
                            self.listWidget.insertItem(index+3+4*i,temp2)
              
                            temp3 =QListWidgetItem('\t'+newlist[i][2])
                            temp3.setForeground(QColor('#1a0dab')) 
                            temp3.setFont(QFont('SansSerif', 8))
                            self.listWidget.insertItem(index+4+4*i,temp3)
                            
                               
                            
                            i+=1
                        
                    else:
                         tempdum =QListWidgetItem("No article found.   ( time = "+ timecal +" seconds )")
                         tempdum.setFont(QFont('SansSerif', 8))
                         self.listWidget.insertItem(index,tempdum)
                   
                 
               
              
            else:
                try:
                    new_index=index-2
                    new_paper=self.listWidget.item(new_index).text()
                    new_paper=str(new_paper).replace("\t","").strip()
                    new_dict=self.obtained_dict[new_paper]
                    url=new_dict[str(paper)]
                    webbrowser.open(url)
                except:
                    pass
         
            
          
          
     
      
 
    def btnstate(self):
        if self.b1.isChecked():
            self.listWidget.clear()
            paper=self.e1.text()
            source=self.cb.currentText()
            giv_years=self.cb1.currentText()
            giv_pages=self.cb2.currentText()
            giv_usage=self.cb3.currentText()
            giv_crit=self.cb4.currentText()
            giv_disp=self.cb5.currentText()
            giv_sim=self.cb6.currentText()
            pageno=self.str
            self.b1.toggle()
            if(len(paper)!=0):
                if(giv_years=="Select Years"):
                    giv_years="3"
                if(giv_pages=="Select Pages"):
                    giv_pages="1"
                if(giv_usage=="Select Metadata"):
                    giv_usage="Author & Title"
                if(giv_crit=="Select Criteria"):
                    giv_crit="Near Match"
                if(giv_disp=="Select Display Count"):
                    giv_disp="Top 3"
                if(source== "Select Source"):
                    showdialog2()
                elif(source== "Google Scholar"):
                    self.listWidget.setVisible(True)
                    pageno=0
                    self.obtained_list,self.obtained_dict=googlequery(paper,pageno)
                    pageno=int(pageno)+10
                    self.str=str(pageno)
                            
                    j=1
                    i=0
                    while(i<len(self.obtained_list)):
                        if("CITATION" in self.obtained_list[i][0]):
                            temp1 =QListWidgetItem(str(self.obtained_list[i][0]))
                            temp1.setForeground(QColor('#000000'))
                            temp1.setFont(QFont('SansSerif', 14)) 
                        else:
                            temp1 =QListWidgetItem(str(self.obtained_list[i][0]))
                            temp1.setForeground(QColor('#1a0dab'))
                            temp1.setFont(QFont('SansSerif', 14)) 
                        
                        self.listWidget.addItem(temp1)
                        temp2 =QListWidgetItem(str(self.obtained_list[i][1]))
                        temp2.setForeground(QColor('#006621')) 
                        temp2.setFont(QFont('SansSerif', 10))
                        self.listWidget.addItem(temp2)
                        
                        if("CITATION" in self.obtained_list[i][0]):
                            temp4 =QListWidgetItem("")
                            temp4.setFont(QFont('SansSerif',12 ))

                        else:
                            if(self.obtained_list[i][2] !=""):
                                temp4 =QListWidgetItem(self.obtained_list[i][2])
                                temp4.setFont(QFont('SansSerif',12 ))
                            else:
                                temp4 =QListWidgetItem("CLICK HERE FOR NEAR MATCH")
                                temp4.setFont(QFont('SansSerif',8 ))
                    
                        temp4.setForeground(QColor('#FF4500')) 
                        
                        self.listWidget.addItem(temp4)
                        
                        temp5 =QListWidgetItem("")
                        temp5.setFont(QFont('SansSerif',5)) 
                        self.listWidget.addItem(temp5)
                        i+=1
                    self.showMaximized()
                    self.listWidget.itemClicked.connect(self.Clicked)
                    
                    
                        
   
                else:
                    self.listWidget.setVisible(True)
                    
                    self.obtained_list,self.obtained_dict=ndlquery(paper,pageno)
                    
                    j=1
                    i=0
                    while(i<len(self.obtained_list)):
                        temp1 =QListWidgetItem(str(self.obtained_list[i][0]))
                        temp1.setForeground(QColor('#1a0dab'))
                        temp1.setFont(QFont('SansSerif', 14)) 
                        self.listWidget.addItem(temp1)

                        temp2 =QListWidgetItem(str(self.obtained_list[i][1]))
                        temp2.setForeground(QColor('#006621')) 
                        temp2.setFont(QFont('SansSerif', 10))
                        self.listWidget.addItem(temp2)
                        
                        temp3 =QListWidgetItem(self.obtained_list[i][2])
                        temp3.setFont(QFont('SansSerif',8 ))
                        temp3.setForeground(QColor('#FF4500')) 
                        self.listWidget.addItem(temp3)

                        temp4 =QListWidgetItem("")
                        temp4.setFont(QFont('SansSerif',5 ))
                        self.listWidget.addItem(temp4)
                        i+=1
                    self.showMaximized()
                    self.listWidget.itemClicked.connect(self.Clicked)


    def btn2state(self):
        if self.b2.isChecked():
            self.listWidget.clear()
            paper=self.e1.text()
            source=self.cb.currentText()
            giv_years=self.cb1.currentText()
            giv_pages=self.cb2.currentText()
            giv_usage=self.cb3.currentText()
            giv_crit=self.cb4.currentText()
            giv_disp=self.cb5.currentText()
            giv_sim=self.cb6.currentText()
            pageno=self.str
            self.b2.toggle()
            if(len(paper)!=0):
                if(giv_years=="Select Years"):
                    giv_years="3"
                if(giv_pages=="Select Pages"):
                    giv_pages="1"
                if(giv_usage=="Select Metadata"):
                    giv_usage="Author & Title"
                if(giv_crit=="Select Criteria"):
                    giv_crit="Near Match"
                if(giv_disp=="Select Display Count"):
                    giv_disp="Top 3"
                if(source== "Select Source"):
                    showdialog2() 
                elif(source== "Google Scholar"):
                    self.listWidget.setVisible(True)
                    
                    self.obtained_list,self.obtained_dict=googlequery(paper,pageno)
                    pageno=int(pageno)+10
                    self.str=str(pageno)
                            
                    j=1
                    i=0
                    while(i<len(self.obtained_list)):
                        if("CITATION" in self.obtained_list[i][0]):
                            temp1 =QListWidgetItem(str(self.obtained_list[i][0]))
                            temp1.setForeground(QColor('#000000'))
                            temp1.setFont(QFont('SansSerif', 14)) 
                        else:
                            temp1 =QListWidgetItem(str(self.obtained_list[i][0]))
                            temp1.setForeground(QColor('#1a0dab'))
                            temp1.setFont(QFont('SansSerif', 14)) 
                        
                        self.listWidget.addItem(temp1)
                        temp2 =QListWidgetItem(str(self.obtained_list[i][1]))
                        temp2.setForeground(QColor('#006621')) 
                        temp2.setFont(QFont('SansSerif', 10))
                        self.listWidget.addItem(temp2)
                        
                        if("CITATION" in self.obtained_list[i][0]):
                            temp4 =QListWidgetItem("")
                            temp4.setFont(QFont('SansSerif',12 ))

                        else:
                            if(self.obtained_list[i][2] !=""):
                                temp4 =QListWidgetItem(self.obtained_list[i][2])
                                temp4.setFont(QFont('SansSerif',12 ))
                            else:
                                temp4 =QListWidgetItem("CLICK HERE FOR NEAR MATCH")
                                temp4.setFont(QFont('SansSerif',8 ))
                    
                        temp4.setForeground(QColor('#FF4500')) 
                        
                        self.listWidget.addItem(temp4)
                        
                        temp5 =QListWidgetItem("")
                        temp5.setFont(QFont('SansSerif',5)) 
                        self.listWidget.addItem(temp5)
                        i+=1
                    self.showMaximized()
                    self.listWidget.itemClicked.connect(self.Clicked)
                    
                else:
                    self.listWidget.setVisible(True)
                    
                    self.obtained_list,self.obtained_dict=ndlquery(paper,pageno)
                   
                            
                    j=1
                    i=0
                    while(i<len(self.obtained_list)):
                        temp1 =QListWidgetItem(str(self.obtained_list[i][0]))
                        temp1.setForeground(QColor('#1a0dab'))
                        temp1.setFont(QFont('SansSerif', 14)) 
                        self.listWidget.addItem(temp1)

                        temp2 =QListWidgetItem(str(self.obtained_list[i][1]))
                        temp2.setForeground(QColor('#006621')) 
                        temp2.setFont(QFont('SansSerif', 10))
                        self.listWidget.addItem(temp2)
                        
                        temp3 =QListWidgetItem(self.obtained_list[i][2])
                        temp3.setFont(QFont('SansSerif',8 ))
                        temp3.setForeground(QColor('#FF4500')) 
                        self.listWidget.addItem(temp3)

                        temp4 =QListWidgetItem("")
                        temp4.setFont(QFont('SansSerif',5 ))
                        self.listWidget.addItem(temp4)
                        i+=1
                    self.showMaximized()
                    self.listWidget.itemClicked.connect(self.Clicked)       
	        

def ndlquery(name,pageno):
           
    url="https://ndl.iitkgp.ac.in/result?q={%22t%22:%22search%22,%22k%22:%22"+name+"%22,%22s%22:[%22type=\%22text\%22%22],%22b%22:{%22filters%22:[]}}"
    
    #(url)
    source_code = requests.get(url, verify=False, proxies = {"http": None, "https": None}) #DKS: verify=False
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text,"html.parser")
    data = soup.find_all("div",{"id":"search-result-group","class":"list-group"})
    obtained_list =[]
    obtained_dict={}
    if(len(data)>0):
        everylink=data[0].find_all("div",{"class":"list-group-item rows"})
        if(len(everylink)>0):
            for i in range(0,len(everylink)):
                eachone_list=[]
                eachone_dict={}
                everyblock=everylink[i].find_all("div",{"class":"col-md-11 col-sm-12"})
                unit_link=""
                unit_name=""
                details=""
                access=""
                if(len(everyblock)>0):
                    heading=everyblock[0].find_all("h4",{"class":"list-group-item-heading overflow-off"})
                    if(len(heading)>0):
                        unitlinklist=heading[0].find_all("a")
                        if(len(unitlinklist)>0):
                            unit_link=unitlinklist[0].get("href")
                            unit_name=unitlinklist[0].contents[0]
                    infoblock=everyblock[0].find_all("div",{"class":"col-sm-5"})
                    if(len(infoblock)>0):
                        authorsinfo=infoblock[0].find_all("div",{"class":"doc-author overflow-off"})
                        if(len(authorsinfo)>0):
                            authorsnames=authorsinfo[0].text
                            details=details+""+authorsnames
                            sourceinfo=infoblock[0].find_all("div",{"class":"text-primary doc-source overflow-off"}) 
                        if(len(sourceinfo)>0):
                            sourcenames=sourceinfo[0].text
                            sourcenames=sourcenames.replace('\n', '')
                            details=details+"::"+sourcenames
                        accessblock= infoblock[0].find_all("div",{"class":"icons"})
                        if(len(accessblock)>0):
                            accessinfo=accessblock[0].find_all("i")
                            if(len(accessinfo)>0):
                                access=accessinfo[0].get("title").replace("/n","")
                        if(access=="Subscribed"):
                            access="CLICK HERE FOR SURROGATES"
                        else:
                            access="Content free in NDLI"
                if(unit_link !=""):
                    eachone_dict[unit_name]=unit_link
                    if(access!="CLICK HERE FOR SURROGATES"):
                        eachone_dict[access]=unit_link
                eachone_list.append(unit_name)
                eachone_list.append(details)
                eachone_list.append(access)
                
                obtained_list.append(eachone_list)
                
                
                if(eachone_dict != {}):
                    obtained_dict[unit_name]=eachone_dict       
    
    return (obtained_list,obtained_dict)  

def googlequery(paper,pageno):
    split_array=str(paper).split() 
    text=''
    #print(paper)
    text=split_array[0]
    for i in range(1,len(split_array)):
        text=text+'+'+split_array[i].replace('"', '').replace("'", '')
    #print (text)
    url="https://scholar.google.co.in/scholar?start="+str(pageno)+"&hl=en&q="+text+"&as_sdt=0,5"
	
    #print(url)
    source_code = requests.get(url)#,verify=False) #DKS: verify=False
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text,"html.parser")
    data = soup.find_all("div",{"class":"gs_r"})
        
    obtained_list =[]
    obtained_dict={}
    
    if(len(data)>0):
        for i in range(0,len(data)) :
            eachone_list=[]
            eachone_dict={}
            data1 = data[i].find_all("div",{"class":"gs_ggs gs_fl"})
            pdflink=""
            pdftext=""
            if(len(data1)>0):
                pdf=data1[0].find_all("a")
                pdftext=data1[0].text
                if(len(pdf)>0):
                    pdflink=pdf[0].get("href")
            unit_name=""
            unit_link=""    
            
            link = data[i].find_all("div",{"class":"gs_ri"})  
            unit_namelink =  link[0].find_all("h3",{"class":"gs_rt"})  
            if(len(unit_namelink[0].find_all("span",{"class":"gs_ctu"}))>0):
                unit_name=unit_namelink[0].find_all("span",{"class":"gs_ct1"})[0].text
                for i in range(1,len(unit_namelink[0].contents)):
                    try:
                        unit_name=unit_name +unit_namelink[0].contents[i].text
                    except:
                        unit_name=unit_name +unit_namelink[0].contents[i]

                              
            elif(len(unit_namelink[0].find_all("span",{"class":"gs_ctc"}))>0):
                unit_name=unit_namelink[0].find_all("span",{"class":"gs_ct1"})[0].text
                unit_links=unit_namelink[0].find_all("a")
                if(len(unit_links)>0):
                    unit_name=unit_name+unit_links[0].text
            else:
                unit_links=unit_namelink[0].find_all("a")
                if(len(unit_links)>0):
                    unit_name=unit_name+unit_links[0].text
                       
            if(len(unit_namelink)>0):
                 unit_links=unit_namelink[0].find_all("a")
                 if(len(unit_links)>0):
                     unit_link=unit_links[0].get("href")
            #print unit_name
            #print unit_link
        # if(isinstance(unit_name,str)):
        #     unit_name=unit_name.encode('utf8') 
        # if(isinstance(unit_link,str)):
        #     unit_link=unit_link.encode('utf8')
            details=""
            detailslink =  link[0].find_all("div",{"class":"gs_a"})
            if(len(detailslink)>0):
                 details =  detailslink[0].text



            if(unit_link !=""):
                eachone_dict[unit_name]=unit_link
            eachone_list.append(unit_name)
            eachone_list.append(details)
            if(pdflink !=""):
                eachone_dict[pdftext]=pdflink
            eachone_list.append(pdftext)


            #print eachone_dict
            #print eachone_list
            obtained_list.append(eachone_list)
            
                
            if(eachone_dict != {}):
                obtained_dict[unit_name]=eachone_dict
            #print obtained_dict    
       
        
       
        # # if(isinstance(details,str)):
        # #      details=details.encode('utf8') 
        # eachone_list.append(details)
        # citlink =  link[0].find_all("a",{"class":"gs_nph"})
       
        # if(len(citlink)>1):
        #        cited=citlink[-1].text
               
        #        citation="https://scholar.google.co.in/"+citlink[-1].get("href")
        # if(len(citlink)==1):
        #        cited=citlink[0].text
               
        #        citation="https://scholar.google.co.in/"+citlink[0].get("href")
        # # if(isinstance(cited,str)):
        # #     cited=cited.encode('utf8') 
        # # if(isinstance(citation,str)):
        # #     citation=citation.encode('utf8') 
        # if cited.lower().find("cite") != -1:
        #      eachone_dict[cited]=citation
        #      eachone_list.append(cited)
        # else:
            
        #     eachone_list.append("")
          
        # if(isinstance(pdflink,str)):
        #     pdflink=pdflink.encode('utf8') 
        # if(isinstance(pdftext,str)):
        #     pdftext=pdftext.encode('utf8') 
        
            
        
    return (obtained_list,obtained_dict)

   
def showdialog():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Please enter some text")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()

def showdialog2():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Please 'Select Source'")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()

def showdialog3():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Please 'Select Years'")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()

def showdialog5():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Please 'Select Metadata'")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()

def showdialog6():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Please 'Select Criteria'")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()

def showdialog7():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Please 'Select Display Count'")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()
		
def showdialog4():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Please 'Select Pages'")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()

def main():
   app = QApplication(sys.argv)
   ex = combodemo()
   ex.show()
   sys.exit(app.exec_())
   

def collect_authoridlink(paper,giv_pages,giv_years,giv_usage,giv_crit,giv_disp, giv_sim):
    split=str(paper).split() 
    text=""
    #print(paper)

    for i in range(0,len(split)):
        text=text+"+"+split[i].replace('\"','')
    
    surrogates_list=[] 
    surrogates_dict={}  
    url="https://scholar.google.co.in/scholar?hl=en&q="+text+"&btnG="
    driver.get(url)
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
     
    dataset = soup.find_all("div",{"class":"gs_r"})
    bottom = soup.find_all("div",{"id":"gs_res_ccl_bot"})
    found=0
     
    if(len(dataset)>0):
        for i in range(0,len(dataset)) :
           
            data1 = dataset[i].find_all("div",{"class":"gs_ggs gs_fl"})
            pdflink=""
            pdftext=""
            if(len(data1)>0):
                pdf=data1[0].find_all("a")
                pdftext=data1[0].text
                if(len(pdf)>0):
                    pdflink=pdf[0].get("href")

            
            unit_name=""
            unit_link=""    
            link = dataset[i].find_all("div",{"class":"gs_ri"}) 
            #print(link[0].text)
            unit_namelink =  link[0].find_all("h3",{"class":"gs_rt"})  
            if(len(unit_namelink[0].find_all("span",{"class":"gs_ctu"}))>0):
                unit_name=unit_namelink[0].find_all("span",{"class":"gs_ct1"})[0].text
                add_name=""
                for i in range(1,len(unit_namelink[0].contents)):
                    try:
                        add_name=add_name +unit_namelink[0].contents[i].text
                    except:
                        add_name=add_name +unit_namelink[0].contents[i]
                unit_name=unit_name+add_name
                              
            elif(len(unit_namelink[0].find_all("span",{"class":"gs_ctc"}))>0):
                unit_name=unit_namelink[0].find_all("span",{"class":"gs_ct1"})[0].text
                unit_links=unit_namelink[0].find_all("a")
                add_name=""
                if(len(unit_links)>0):
                     add_name=add_name+unit_links[0].text

                unit_name=unit_name+add_name
                
            else:
                unit_links=unit_namelink[0].find_all("a")
                add_name=""
                if(len(unit_links)>0):
                    add_name=add_name+unit_links[0].text
            
                unit_name=unit_name+add_name

            if(len(unit_namelink)>0):
                unit_links=unit_namelink[0].find_all("a")
                if(len(unit_links)>0):
                     unit_link=unit_links[0].get("href")
            #print (paper)
            #print (add_name)
            
            if(str(add_name).lower() == str(paper).lower()) :
                data = link[0].find_all("a",{"class":"gs_nta gs_nph"})
                year=''
                authors=[]
                if(len(data)>0):
                      if data[-1].text.find("BibTeX")!=-1:
                          biblink=data[-1].get("href")
                          source_code = requests.get(biblink)
                          plain_text = source_code.text
                          titlesoup = BeautifulSoup(plain_text,"html.parser")
                          year=''
                          try:
                               yearindex=str(titlesoup).index('year={')
                               year=str(titlesoup)[yearindex+6:yearindex+10]
                          except:
                               pass
                          aut=''
                          try:
                               autindex=str(titlesoup).index('author={')
                               endautindex=str(titlesoup).index('},',autindex)
                               aut=str(titlesoup)[autindex+8:endautindex]
                          except:
                               pass
                          authors=[]
                          if(aut!=""):
                               authors=aut.split('and')
                               for i in range(0,len(authors)):
                                        bucket=authors[i].split()
                                        mainname=bucket[0].replace(',','')
                                        authors[i]=''
                                        if(len(bucket)>1):
                                                for j in range(1,len(bucket)):
                                                         authors[i]=authors[i]+bucket[j][0]
                                        authors[i]=(authors[i]+" "+mainname).strip()
                #print(authors)
                abstract=""
                
                
                item= link[0].find_all("div",{"class":"gs_fl"})
                if(len(item)>0):
                     citetext=item[0].find_all("a")
                if(len(citetext)>2):
                    citetext=item[0].find_all("a")[2].text
                    citing_link=item[0].find_all("a")[2].get("href")
                    citing_link=citing_link.replace("/scholar?","")
                    #print((giv_pages))
                    for i in range(0,int(giv_pages)):
                    	citation="https://scholar.google.co.in/scholar?start="+str(i*10)+"&"+citing_link
                    	#print ("cite"+str(i))
                    	if citetext.lower().find("cited") != -1 or citetext.lower().find("related")!=-1 :
                        	 #print (citetext)
                        	 #print (citation)
                        	 surrogates_list,surrogates_dict=findincit(citation,paper,authors,year,abstract,giv_years,giv_usage,giv_crit,giv_disp, giv_sim,surrogates_list,surrogates_dict)

                
                item= link[0].find_all("div",{"class":"gs_fl"})
                if(len(item)>0):
                    citetext=item[0].find_all("a")
                    if(len(citetext)>3):
                         relatedtext=item[0].find_all("a")[3].text
                         relating_link=item[0].find_all("a")[3].get("href")
                         relating_link=relating_link.replace("/scholar?","")
                         for i in range(0,int(giv_pages)):
                                 #print ("relate"+str(i))
                                 relatelink="https://scholar.google.co.in/scholar?start="+str(i*10)+"&"+relating_link
                                 if relatedtext.lower().find("related") != -1 or relatedtext.lower().find("cited")!=-1:
                          	 	#print relatedtext
                          	 	#print relatelink
                                        surrogates_list,surrogates_dict=findincit(relatelink,paper,authors,year,abstract,giv_years,giv_usage,giv_crit,giv_disp,  giv_sim,surrogates_list,surrogates_dict)
		
                
                if(len(bottom)>0):
                        bottext=bottom[0].find_all("a")
                        if(len(bottext)>0):
                            botlink="https://scholar.google.co.in/"+bottom[0].find_all("a")[0].get("href")
                            surrogates_list,surrogates_dict=findincit(botlink,paper,authors,year,abstract,giv_years,giv_usage,giv_crit,giv_disp, giv_sim, surrogates_list,surrogates_dict)
    surrogates_list=refine(surrogates_list,giv_disp)	
    print(surrogates_list)              
    return (surrogates_list,surrogates_dict)     

def refine(surrogates_list,giv_disp):
    surrogates_list = sorted(surrogates_list, key=lambda x: x[-1], reverse=True)
    df = pd.DataFrame(surrogates_list)
    try:
         df = df.drop_duplicates()
    except:
         pass
    surrogates_list = df.values.tolist()
    number=int(giv_disp.replace("Top","").strip())
    
    if(number<len(surrogates_list)):
            a = np.array(surrogates_list)
            surrogates_list=a[:number,:].tolist()
    return(surrogates_list)



def collect_authoridlinkndl(paper,paper2,giv_pages,giv_years,giv_usage,giv_crit,giv_disp,giv_sim):
    split=str(paper).split() 
    text=split[0]
    if(len(split)>1):
        for i in range(1,len(split)):
            text=text+"+"+split[i]
    authors=str(paper2).split("::")
    authorstr=""
    if(len(authors)>0):
        dum="Author:"
        if(dum in authors[0]):
            authorsstr=authors[0].replace(dum,"")
    authornames=[]
    abb_authornames=[]
    authornames=authorsstr.split("|")
    
    if(len(authornames)>0):
        for i in range(0,len(authornames)):
            authornames[i]=authornames[i].strip()
            everyname=authornames[i].split(",")
            if(len(everyname)>1):
                authornames[i]=everyname[1].strip()+" "+everyname[0].strip()
    
    if(len(authornames)>0):
        for i in range(0,len(authornames)):
            everyname=re.split('[. -]',authornames[i])
            
            authornames[i]=""
            for j in range(0,len(everyname)):
                authornames[i]=authornames[i].strip()+" "+ everyname[j].strip()
            authornames[i]=authornames[i].strip()
    
    if(len(authornames)>0):
        for i in range(0,len(authornames)):
            abb_authornames.append(authornames[i])          
    if(len(abb_authornames)>0):
        for i in range(0,len(abb_authornames)):
            eachname=abb_authornames[i].split()
            abb_authornames[i]=""
            if(len(eachname)>0):
                for j in range(0,len(eachname)-1):
                    abb_authornames[i]=abb_authornames[i]+eachname[j][0]
            abb_authornames[i]=abb_authornames[i]+" "+eachname[-1]
            abb_authornames[i]=abb_authornames[i].strip()
    #print (authornames)
    #print (abb_authornames)
    text2=""
    if(len(abb_authornames)>0):
        text2=abb_authornames[0]
        # if(len(abb_authornames)>1):
        #     for i in range(1,len(abb_authornames)):
        #         text2=text2+"+"+abb_authornames[i]
    
    surrogates_list=[] 
    surrogates_dict={}  
    url="https://scholar.google.co.in/scholar?as_q="+text+"&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors="+text2+"&as_publication=&as_ylo=&as_yhi=&hl=en&as_sdt=0%2C5"
    #print(url)
    driver.get(url)
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
     
    dataset = soup.find_all("div",{"class":"gs_r"})
    bottom = soup.find_all("div",{"id":"gs_res_ccl_bot"})

    
       
    if(len(dataset)>0):
         for i in range(0,len(dataset)) :
           
            data1 = dataset[i].find_all("div",{"class":"gs_ggs gs_fl"})
            pdflink=""
            pdftext=""
            if(len(data1)>0):
                pdf=data1[0].find_all("a")
                pdftext=data1[0].text
                if(len(pdf)>0):
                    pdflink=pdf[0].get("href")

            
            unit_name=""
            unit_link=""    
            link = dataset[i].find_all("div",{"class":"gs_ri"})  
            unit_namelink =  link[0].find_all("h3",{"class":"gs_rt"})  
            if(len(unit_namelink[0].find_all("span",{"class":"gs_ctu"}))>0):
                unit_name=unit_namelink[0].find_all("span",{"class":"gs_ct1"})[0].text
                add_name=""
                for i in range(1,len(unit_namelink[0].contents)):
                    try:
                        add_name=add_name +unit_namelink[0].contents[i].text
                    except:
                        add_name=add_name +unit_namelink[0].contents[i]
                unit_name=unit_name+add_name
                              
            elif(len(unit_namelink[0].find_all("span",{"class":"gs_ctc"}))>0):
                unit_name=unit_namelink[0].find_all("span",{"class":"gs_ct1"})[0].text
                unit_links=unit_namelink[0].find_all("a")
                add_name=""
                if(len(unit_links)>0):
                     add_name=add_name+unit_links[0].text

                unit_name=unit_name+add_name
                
            else:
                unit_links=unit_namelink[0].find_all("a")
                add_name=""
                if(len(unit_links)>0):
                    add_name=add_name+unit_links[0].text
            
                unit_name=unit_name+add_name

            if(len(unit_namelink)>0):
                unit_links=unit_namelink[0].find_all("a")
                if(len(unit_links)>0):
                     unit_link=unit_links[0].get("href")
            #print (paper)
            #print (add_name)
            if(str(add_name).lower() == str(paper).lower()) :
                data = link[0].find_all("a",{"class":"gs_nta gs_nph"})
                year=''
                authors=[]
                if(len(data)>0):
                      if data[-1].text.find("BibTeX")!=-1:
                          biblink=data[-1].get("href")
                          source_code = requests.get(biblink)
                          plain_text = source_code.text
                          titlesoup = BeautifulSoup(plain_text,"html.parser")
                          year=''
                          try:
                               yearindex=str(titlesoup).index('year={')
                               year=str(titlesoup)[yearindex+6:yearindex+10]
                          except:
                               pass
                          aut=''
                          try:
                               autindex=str(titlesoup).index('author={')
                               endautindex=str(titlesoup).index('},',autindex)
                               aut=str(titlesoup)[autindex+8:endautindex]
                          except:
                               pass
                          authors=[]
                          if(aut!=""):
                               authors=aut.split('and')
                               for i in range(0,len(authors)):
                                        bucket=authors[i].split()
                                        mainname=bucket[0].replace(',','')
                                        authors[i]=''
                                        if(len(bucket)>1):
                                                for j in range(1,len(bucket)):
                                                         authors[i]=authors[i]+bucket[j][0]
                                        authors[i]=(authors[i]+" "+mainname).strip()
                #print(authors)
                abstract=""
                  
                
                item= link[0].find_all("div",{"class":"gs_fl"})
                if(len(item)>0):
                     citetext=item[0].find_all("a")
                if(len(citetext)>2):
                    citetext=item[0].find_all("a")[2].text
                    citing_link=item[0].find_all("a")[2].get("href")
                    citing_link=citing_link.replace("/scholar?","")
                    for i in range(0,int(giv_pages)):
                    	citation="https://scholar.google.co.in/scholar?start="+str(i*10)+"&"+citing_link
                    	#print ("cite"+str(i))
                    	if citetext.lower().find("cited") != -1 or citetext.lower().find("related"):
                        	 #print (citetext)
                        	 #print (citation)
                        	 surrogates_list,surrogates_dict=findincit(citation,paper,abb_authornames,year,abstract,giv_years,giv_usage,giv_crit,giv_disp, giv_sim,surrogates_list,surrogates_dict)

                
                item= link[0].find_all("div",{"class":"gs_fl"})
                if(len(item)>0):
                    citetext=item[0].find_all("a")
                    if(len(citetext)>3):
                         relatedtext=item[0].find_all("a")[3].text
                         relating_link=item[0].find_all("a")[3].get("href")
                         relating_link=relating_link.replace("/scholar?","")
                         for i in range(0,int(giv_pages)):
                                #print ("relate"+str(i))
                                relatelink="https://scholar.google.co.in/scholar?start="+str(i*10)+"&"+relating_link
                                if relatedtext.lower().find("related") != -1 or relatedtext.lower().find("cited")!=-1:
                                        #print (relatedtext)
                                        #print (relatelink)
                                        surrogates_list,surrogates_dict=findincit(relatelink,paper,abb_authornames,year,abstract,giv_years,giv_usage,giv_crit,giv_disp, giv_sim,surrogates_list,surrogates_dict)
               
                if(len(bottom)>0):
                        bottext=bottom[0].find_all("a")
                        if(len(bottext)>0):
                            botlink="https://scholar.google.co.in/"+bottom[0].find_all("a")[0].get("href")
                            surrogates_list,surrogates_dict=findincit(botlink,paper,abb_authornames,year,abstract,giv_years,giv_usage,giv_crit,giv_disp, giv_sim,surrogates_list,surrogates_dict)
    
    if(len(surrogates_list)==0):
        text2=abb_authornames[0]
        if(len(abb_authornames)>1):
            text2=abb_authornames[1]
        # if(len(abb_authornames)>1):
        #     for i in range(1,len(abb_authornames)):
        #         text2=text2+"+"+abb_authornames[i]
    
        surrogates_list=[] 
        surrogates_dict={}  
        url="https://scholar.google.co.in/scholar?as_q="+text+"&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors="+text2+"&as_publication=&as_ylo=&as_yhi=&hl=en&as_sdt=0%2C5"
        #print(url)
        driver.get(url)
        source = driver.page_source
        soup = BeautifulSoup(source, "html.parser")
     
        dataset = soup.find_all("div",{"class":"gs_r"})
        bottom = soup.find_all("div",{"id":"gs_res_ccl_bot"})
    
       
        if(len(dataset)>0):
             for i in range(0,len(dataset)) :
           
                data1 = dataset[i].find_all("div",{"class":"gs_ggs gs_fl"})
                pdflink=""
                pdftext=""
                if(len(data1)>0):
                    pdf=data1[0].find_all("a")
                    pdftext=data1[0].text
                    if(len(pdf)>0):
                        pdflink=pdf[0].get("href")

            
                unit_name=""
                unit_link=""    
                link = dataset[i].find_all("div",{"class":"gs_ri"})  
                unit_namelink =  link[0].find_all("h3",{"class":"gs_rt"})  
                if(len(unit_namelink[0].find_all("span",{"class":"gs_ctu"}))>0):
                    unit_name=unit_namelink[0].find_all("span",{"class":"gs_ct1"})[0].text
                    add_name=""
                    for i in range(1,len(unit_namelink[0].contents)):
                        try:
                            add_name=add_name +unit_namelink[0].contents[i].text
                        except:
                            add_name=add_name +unit_namelink[0].contents[i]
                    unit_name=unit_name+add_name
                              
                elif(len(unit_namelink[0].find_all("span",{"class":"gs_ctc"}))>0):
                    unit_name=unit_namelink[0].find_all("span",{"class":"gs_ct1"})[0].text
                    unit_links=unit_namelink[0].find_all("a")
                    add_name=""
                    if(len(unit_links)>0):
                         add_name=add_name+unit_links[0].text

                    unit_name=unit_name+add_name
                
                else:
                    unit_links=unit_namelink[0].find_all("a")
                    add_name=""
                    if(len(unit_links)>0):
                        add_name=add_name+unit_links[0].text
            
                    unit_name=unit_name+add_name

                if(len(unit_namelink)>0):
                    unit_links=unit_namelink[0].find_all("a")
                    if(len(unit_links)>0):
                         unit_link=unit_links[0].get("href")
                #print (paper)
                #print (add_name)
                if(str(add_name).lower() == str(paper).lower()) :
                    data = link[0].find_all("a",{"class":"gs_nta gs_nph"})
                    year=''
                    authors=[]
                    if(len(data)>0):
                       if data[-1].text.find("BibTeX")!=-1:
                          biblink=data[-1].get("href")
                          source_code = requests.get(biblink)
                          plain_text = source_code.text
                          titlesoup = BeautifulSoup(plain_text,"html.parser")
                          year=''
                          try:
                               yearindex=str(titlesoup).index('year={')
                               year=str(titlesoup)[yearindex+6:yearindex+10]
                          except:
                               pass
                          aut=''
                          try:
                               autindex=str(titlesoup).index('author={')
                               endautindex=str(titlesoup).index('},',autindex)
                               aut=str(titlesoup)[autindex+8:endautindex]
                          except:
                               pass
                          authors=[]
                          if(aut!=""):
                               authors=aut.split('and')
                               for i in range(0,len(authors)):
                                        bucket=authors[i].split()
                                        mainname=bucket[0].replace(',','')
                                        authors[i]=''
                                        if(len(bucket)>1):
                                                for j in range(1,len(bucket)):
                                                         authors[i]=authors[i]+bucket[j][0]
                                        authors[i]=(authors[i]+" "+mainname).strip()
                    #print(authors)
                    abstract=""
                    item= link[0].find_all("div",{"class":"gs_fl"})
                    if(len(item)>0):
                         citetext=item[0].find_all("a")
                    if(len(citetext)>2):
                        citetext=item[0].find_all("a")[2].text
                        citing_link=item[0].find_all("a")[2].get("href")
                        citing_link=citing_link.replace("/scholar?","")
                        for i in range(0,int(giv_pages)):
                                citation="https://scholar.google.co.in/scholar?start="+str(i*10)+"&"+citing_link
                                #print ("cite"+str(i))
                       	        if citetext.lower().find("cited") != -1 or citetext.lower().find("related"):
                                        #print (citetext)
                                        #print (citation)
                                        surrogates_list,surrogates_dict=findincit(citation,paper,abb_authornames,year,abstract,giv_years,giv_usage,giv_crit,giv_disp, giv_sim,surrogates_list,surrogates_dict)

                    item= link[0].find_all("div",{"class":"gs_fl"})
                    if(len(item)>0):
                        citetext=item[0].find_all("a")
                        if(len(citetext)>3):
                            relatedtext=item[0].find_all("a")[3].text
                            relating_link=item[0].find_all("a")[3].get("href")
                            relating_link=relating_link.replace("/scholar?","")
                            for i in range(0,int(giv_pages)):
                                 #print ("relate"+str(i))
                                 relatelink="https://scholar.google.co.in/scholar?start="+str(i*10)+"&"+relating_link
                                 if relatedtext.lower().find("related") != -1 or relatedtext.lower().find("cited"):
                                        #print (relatedtext)
                                        #print (relatelink)
                                        surrogates_list,surrogates_dict=findincit(relatelink,paper,abb_authornames,year,abstract,giv_years,giv_usage,giv_crit,giv_disp, giv_sim,surrogates_list,surrogates_dict)
                       
                    if(len(bottom)>0):
                            bottext=bottom[0].find_all("a")
                            if(len(bottext)>0):
                              botlink="https://scholar.google.co.in/"+bottom[0].find_all("a")[0].get("href")
                              surrogates_list,surrogates_dict=findincit(botlink,paper,abb_authornames,year,abstract,giv_years,giv_usage,giv_crit,giv_disp, giv_sim,surrogates_list,surrogates_dict)
    surrogates_list=refine(surrogates_list,giv_disp)
    print(surrogates_list)
    return (surrogates_list,surrogates_dict)
       


def fetch_abstract(paper):
    url2 = 'https://www.semanticscholar.org/'
    driver2.get(url2)  
    driver2.find_element_by_xpath("//input[@class='input form-input']").clear()
    driver2.find_element_by_xpath("//input[@class='input form-input']").send_keys(paper)
    driver2.find_element_by_xpath("//input[@class='input form-input']").send_keys(Keys.ENTER)
    time.sleep(3)
    source = driver2.page_source
    soup = BeautifulSoup(source, "html.parser")
    data = soup.find_all("article",{"class":"search-result"})
    if(len(data)>0):
       for i in range(0,len(data)):
           titlelink=data[i].find_all("a",{"data-selenium-selector":"title-link"})
           if(len(titlelink)>0):
                  titleurl="https://www.semanticscholar.org"+titlelink[0].get("href")
                  driver2.get(titleurl)
                  time.sleep(3)
                  title=driver2.find_element_by_xpath("//h1[@data-selenium-selector='paper-detail-title']").text
                  #print(title)
                  author=driver2.find_element_by_xpath("//span[@class='author-list']").text
                  #print(author)
                  try:
                     year=driver2.find_element_by_xpath("//span[@data-selenium-selector='paper-year']").text
                     #print(year)
                  except:
                     pass
                  try:
                     driver2.find_element_by_xpath("//span[@class='mod-clickable more']").click()
                  except:
                     pass
                  abstract=driver2.find_element_by_xpath("//div[@class='text-truncator text--preline']").text[:-7]
                  #print(abstract)
                  if(str(title).lower() == str(paper).lower()):
                            break
                  else:
                            abstract=""

    return abstract 



   
def findincit(url,paper,authors,year,abstract,giv_years,giv_usage,giv_crit,giv_disp, giv_sim,surrogates_list,surrogates_dict):
    driver.get(url)
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    dataset = soup.find_all("div",{"class":"gs_r"})
    ans=0
    cityear=""
    if(len(dataset)>0):
        for i in range(0,len(dataset)) :
           
            data1 = dataset[i].find_all("div",{"class":"gs_ggs gs_fl"})
            pdflink=""
            pdftext=""
            if(len(data1)>0):
                pdf=data1[0].find_all("a")
                pdftext=data1[0].text
                if(len(pdf)>0):
                    pdflink=pdf[0].get("href")

            if(pdflink!=""):
                unit_name=""
                unit_link=""    
                link = dataset[i].find_all("div",{"class":"gs_ri"})  
                unit_namelink =  link[0].find_all("h3",{"class":"gs_rt"})  
                if(len(unit_namelink[0].find_all("span",{"class":"gs_ctu"}))>0):
                    unit_name=unit_namelink[0].find_all("span",{"class":"gs_ct1"})[0].text
                    add_name=""
                    for i in range(1,len(unit_namelink[0].contents)):
                        try:
                            add_name=add_name +unit_namelink[0].contents[i].text
                        except:
                            add_name=add_name +unit_namelink[0].contents[i]
                    unit_name=unit_name+add_name
                              
                elif(len(unit_namelink[0].find_all("span",{"class":"gs_ctc"}))>0):
                    unit_name=unit_namelink[0].find_all("span",{"class":"gs_ct1"})[0].text
                    unit_links=unit_namelink[0].find_all("a")
                    add_name=""
                    if(len(unit_links)>0):
                         add_name=add_name+unit_links[0].text

                    unit_name=unit_name+add_name
                    
                else:
                    unit_links=unit_namelink[0].find_all("a")
                    add_name=""
                    if(len(unit_links)>0):
                        add_name=add_name+unit_links[0].text
            
                    unit_name=unit_name+add_name

                if(len(unit_namelink)>0):
                    unit_links=unit_namelink[0].find_all("a")
                    if(len(unit_links)>0):
                         unit_link=unit_links[0].get("href")
                details=""
                detailslink =  link[0].find_all("div",{"class":"gs_a"})
                if(len(detailslink)>0):
                    details =  detailslink[0].text
                cit_abstract=""
                cityear=""
                citauthors=[]
                data = link[0].find_all("a",{"class":"gs_nta gs_nph"})
                if(len(data)>0):
                      if data[-1].text.find("BibTeX")!=-1:
                          biblink=data[-1].get("href")
                          source_code = requests.get(biblink)
                          plain_text = source_code.text
                          titlesoup = BeautifulSoup(plain_text,"html.parser")
                          
                          year=''
                          try:
                               yearindex=str(titlesoup).index('year={')
                               cityear=str(titlesoup)[yearindex+6:yearindex+10]
                          except:
                               pass
                          aut=''
                          try:
                               autindex=str(titlesoup).index('author={')
                               endautindex=str(titlesoup).index('},',autindex)
                               aut=str(titlesoup)[autindex+8:endautindex]
                          except:
                               pass
                          
                          if(aut!=""):
                               citauthors=aut.split('and')
                               for i in range(0,len(citauthors)):
                                     bucket=citauthors[i].split()
                                     #print(bucket)
                                     if(len(bucket)>0):   
                                        mainname=bucket[0].replace(',','')
                                        citauthors[i]=''
                                        if(len(bucket)>1):
                                                for j in range(1,len(bucket)):
                                                         citauthors[i]=citauthors[i]+bucket[j][0]
                                        citauthors[i]=(citauthors[i]+" "+mainname).strip()
                paper=''.join(i for i in str(paper) if ord(i)<128)
                add_name= ''.join(i for i in str(add_name) if ord(i)<128)
                #print (authors)
                #print (citauthors)
                res=compareaut(authors,citauthors)
                #print("authors = "+ str(res))
                #print(cityear)
                if(giv_crit=="Exact match"):
                       if(str(add_name).lower() == str(paper).lower()):
                             tit_res=comparetit(paper,add_name)
                             eachone_dict={}
                             eachone_list=[]
                             if(unit_link !=""):
                                        eachone_dict[unit_name]=unit_link
                                        eachone_list.append(unit_name)
                                        eachone_list.append(details)
                                        eachone_dict[pdftext]=pdflink
                                        eachone_list.append(pdftext)
                                        eachone_list.append(0.6*res+0.4*tit_res)
                                        surrogates_list.append(eachone_list)
                                        surrogates_dict[unit_name]=eachone_dict
                else:
                       if(giv_usage=="Author & Title"):
                             if(year=="" or cityear==""):
                                    if(res>0):
                                        tit_res=comparetit(paper,add_name)
                                        #print (paper)
                                        #print (add_name)
                                        #print("tit_res ="+ str(tit_res))
                                        if(tit_res> 0):
                                              eachone_dict={}
                                              eachone_list=[]
                                              if(unit_link !=""):
                                                     eachone_dict[unit_name]=unit_link
                                                     eachone_list.append(unit_name)
                                                     eachone_list.append(details)
                                                     eachone_dict[pdftext]=pdflink
                                                     eachone_list.append(pdftext)
                                                     eachone_list.append(0.6*res+0.4*tit_res)
                                                     surrogates_list.append(eachone_list)
                                                     surrogates_dict[unit_name]=eachone_dict
                       


                             elif(compareyear(year,cityear,giv_years)==1):
                                    if(res>0):
                                        tit_res=comparetit(paper,add_name)
                                        #print (paper)
                                        #print (add_name)
                                        #print("tit_res ="+ str(tit_res))
                                        if(tit_res> 0):
                                              eachone_dict={}
                                              eachone_list=[]
                                              if(unit_link !=""):
                                                     eachone_dict[unit_name]=unit_link
                                                     eachone_list.append(unit_name)
                                                     eachone_list.append(details)
                                                     eachone_dict[pdftext]=pdflink
                                                     eachone_list.append(pdftext)
                                                     eachone_list.append(0.6*res+0.4*tit_res)
                                                     surrogates_list.append(eachone_list)
                                                     surrogates_dict[unit_name]=eachone_dict


                       elif(giv_usage=="Author, Title & Abstract"):
                             if(year=="" or cityear==""):
                                    if(res>0):
                                        tit_res=comparetit(paper,add_name)
                                        #print (paper)
                                        #print (add_name)
                                        #print("tit_res ="+ str(tit_res))
                                        if(tit_res> 0):
                                              pap_abs=fetch_abstract(paper)
                                              cit_abs=fetch_abstract(add_name)
                                              if(pap_abs=="" or cit_abs==""):
                                                   eachone_dict={}
                                                   eachone_list=[]
                                                   if(unit_link !=""):
                                                      eachone_dict[unit_name]=unit_link
                                                      eachone_list.append(unit_name)
                                                      eachone_list.append(details)
                                                      eachone_dict[pdftext]=pdflink
                                                      eachone_list.append(pdftext)
                                                      eachone_list.append(0.6*res+0.4*tit_res)
                                                      surrogates_list.append(eachone_list)
                                                      surrogates_dict[unit_name]=eachone_dict
                                              else:
                                                   eachone_dict={}
                                                   eachone_list=[]
                                                   abs_res=compareabs(pap_abs,cit_abs, giv_sim)
                                                   if(unit_link !=""):
                                                      eachone_dict[unit_name]=unit_link
                                                      eachone_list.append(unit_name)
                                                      eachone_list.append(details)
                                                      eachone_dict[pdftext]=pdflink
                                                      eachone_list.append(pdftext)
                                                      eachone_list.append(0.5*res+0.4*tit_res+0.1*abs_res)
                                                      surrogates_list.append(eachone_list)
                                                      surrogates_dict[unit_name]=eachone_dict
                       


                             elif(compareyear(year,cityear,giv_years)==1):
                                    if(res>0):
                                        tit_res=comparetit(paper,add_name)
                                        #print (paper)
                                        #print (add_name)
                                        #print("tit_res ="+ str(tit_res))
                                        if(tit_res> 0):
                                              pap_abs=fetch_abstract(paper)
                                              cit_abs=fetch_abstract(add_name)
                                              if(pap_abs=="" or cit_abs==""):
                                                   eachone_dict={}
                                                   eachone_list=[]
                                                   if(unit_link !=""):
                                                      eachone_dict[unit_name]=unit_link
                                                      eachone_list.append(unit_name)
                                                      eachone_list.append(details)
                                                      eachone_dict[pdftext]=pdflink
                                                      eachone_list.append(pdftext)
                                                      eachone_list.append(0.6*res+0.4*tit_res)
                                                      surrogates_list.append(eachone_list)
                                                      surrogates_dict[unit_name]=eachone_dict
                                              else:
                                                   eachone_dict={}
                                                   eachone_list=[]
                                                   abs_res=compareabs(pap_abs,cit_abs, giv_sim)
                                                   if(unit_link !=""):
                                                      eachone_dict[unit_name]=unit_link
                                                      eachone_list.append(unit_name)
                                                      eachone_list.append(details)
                                                      eachone_dict[pdftext]=pdflink
                                                      eachone_list.append(pdftext)
                                                      eachone_list.append(0.5*res+0.4*tit_res+0.1*abs_res)
                                                      surrogates_list.append(eachone_list)
                                                      surrogates_dict[unit_name]=eachone_dict                                       
                        
                                     
                         
    return (surrogates_list,surrogates_dict)       
       
 
def comparetit(paper,cit_unit_name):
    paperlist=re.split('[  -/]',paper)
    cit_unit_namelist=re.split('[  -/]',cit_unit_name)
    pun={'~':'', '`':'', '!':'', '@':'', '#':'', '(':'', '*':'', '^':'', '!':'', ')':'', '_':'', '-':'', '{':'', '}':'', '[':'', ']':'', '|':'', '.':'', ',':'', '?':'', '\"':'', '\'':'',';':'',':':'','\\':'','/':''}

    for i in range(0,len(paperlist)):
        paperlist[i]=paperlist[i].strip()
        paperlist[i]=paperlist[i].lower()
    for i in range(0,len(paperlist)):
             for j,k in pun.items():
                     paperlist[i]=paperlist[i].replace(j,k)
        #print(type( paperlist[i]))
    for i in range(0,len(cit_unit_namelist)):
        cit_unit_namelist[i]=cit_unit_namelist[i].strip()
        cit_unit_namelist[i]=cit_unit_namelist[i].lower()
        #print(type(cit_unit_namelist[i]))
    for i in range(0,len(cit_unit_namelist)):
             for j,k in pun.items():
                     cit_unit_namelist[i]=cit_unit_namelist[i].replace(j,k)
    paperlist=remove_stopwords(paperlist)
    
    cit_unit_namelist=remove_stopwords(cit_unit_namelist)  
    paperlist=stem(paperlist)
    paperlist=list(set(paperlist))
    cit_unit_namelist=stem(cit_unit_namelist)
    cit_unit_namelist=list(set(cit_unit_namelist))
    #print(paperlist)
    #print(cit_unit_namelist)
    v1, v2 = build_vector(paperlist, cit_unit_namelist)  
    return calculate_cosim(v1, v2)
    


def getft_sentence_vector(modelft, sentence):
        wordcount = len(sentence)
        ft_sumvec = [0]*300  #Fast Text pretrained vectors are 300-dimensional
        validWordcount = 0
        for i in range(0, wordcount):
                try:
                        ft_wordvec = modelft[sentence[i]]
                        norm = LA.norm(ft_wordvec)
                        if(norm > 0.0):
                                ft_wordvec = np.divide(ft_wordvec, norm)
                                ft_sumvec = ft_sumvec + ft_wordvec
                        validWordcount = validWordcount + 1
                except:
                        pass
        if(wordcount>0):
                np.divide(ft_sumvec, validWordcount)
        return ft_sumvec

def getft_similarity(modelft, paperlist, cit_unit_namelist):
        ftsim = 0

        sentence_vec1 = getft_sentence_vector(modelft, paperlist)
        sentence_vec2 = getft_sentence_vector(modelft, cit_unit_namelist)
        n1 = LA.norm(sentence_vec1)
        n2 = LA.norm(sentence_vec2)

        if(n1 > 0 and n2 > 0):
                ftsim = np.dot(sentence_vec1, sentence_vec2)/ n1 / n2
        else:
                ftsim = 0  #Zero similarity if any sentence vector is null

        return ftsim


def compareabs(paper,cit_unit_name,giv_sim):
    
          paperlist=re.split('[  -/]',paper)
          cit_unit_namelist=re.split('[  -/]',cit_unit_name)
          pun={'~':'', '`':'', '!':'', '@':'', '#':'', '(':'', '*':'', '^':'', '!':'', ')':'', '_':'', '-':'', '{':'', '}':'', '[':'', ']':'', '|':'', '.':'', ',':'', '?':'', '\"':'', '\'':'',';':'',':':'','\\':'','/':'', '0':'', '1':'', '2':'', '3':'', '4':'', '5':'', '6':'', '7':'', '8':'', '9':''}

          for i in range(0,len(paperlist)):
              paperlist[i]=paperlist[i].strip()
              paperlist[i]=paperlist[i].lower()
          for i in range(0,len(paperlist)):
             for j,k in pun.items():
                     paperlist[i]=paperlist[i].replace(j,k)
          #print(type( paperlist[i]))
          for i in range(0,len(cit_unit_namelist)):
              cit_unit_namelist[i]=cit_unit_namelist[i].strip()
              cit_unit_namelist[i]=cit_unit_namelist[i].lower()
          #print(type(cit_unit_namelist[i]))
          for i in range(0,len(cit_unit_namelist)):
             for j,k in pun.items():
                     cit_unit_namelist[i]=cit_unit_namelist[i].replace(j,k)
          paperlist=remove_stopwords(paperlist)
          cit_unit_namelist=remove_stopwords(cit_unit_namelist)  
          if(giv_sim=="Cosine Similarity (BoW)"):      
               paperlist=stem(paperlist)
               paperlist=list(set(paperlist))
               cit_unit_namelist=stem(cit_unit_namelist)
               cit_unit_namelist=list(set(cit_unit_namelist))
               #print(paperlist)
               #print(cit_unit_namelist)
               v1, v2 = build_vector(paperlist, cit_unit_namelist)  
               return calculate_cosim(v1, v2)
          elif(giv_sim=="Cosine Similarity (fastText)"):
               #try:
        	#return model2.n_similarity(paperlist, cit_unit_namelist)
               return getft_similarity(model2, paperlist, cit_unit_namelist)
               #except:
               #  return 0
          else:
               #distance = model.wmdistance(paperlist,cit_unit_namelist)
               #return 5-distance
               distance = model.wmdistance(paperlist,cit_unit_namelist)
               return 1/(1.+ distance)
               
   

def compareyear(year,cityear,giv_years):
    if(isinstance(year,str)):
        year=year.encode('utf8') 
    if(isinstance(cityear,str)):
        cityear=cityear.encode('utf8')
    #print(year)
    #print (cityear)
    #print(giv_years)
    if((((int(year)-int(cityear))<=int(giv_years) and (int(year)-int(cityear))>=0)) or ((int(cityear)-int(year))<=int(giv_years) and (int(cityear)- int(year))>=0)):
        return 1
    else:
        return 0
    

def remove_stopwords(word_list):
    for i in range(0,len(word_list)):
        if(isinstance(word_list[i],bytes)):
              word_list[i]=word_list[i].decode() 
    #print(word_list)  
    resultwords  =[word for word in word_list if word not in stopwords.words('english')]
    #print(resultwords)
    return resultwords

def stem(wordlist):
    resultwords=[]
    for i in range(0,len(wordlist)):
        if(isinstance(wordlist[i],bytes)):
             wordlist[i]=wordlist[i].decode ()
    for i in range(0,len(wordlist)):
        resultwords.append(PorterStemmer().stem(wordlist[i]))
    return resultwords

def compareaut(authors,citauthors):
    for i in range(0,len(authors)):
        authors[i]=authors[i].strip()
        authors[i]=authors[i].lower()
        
    for i in range(0,len(citauthors)):
        citauthors[i]=citauthors[i].strip()
        citauthors[i]=citauthors[i].lower()
    
    #print(jaccard(authors,citauthors)) 
    return jaccard(authors,citauthors)
     
   
                     
def build_vector(iterable1, iterable2):
    counter1 = Counter(iterable1)
    counter2 = Counter(iterable2)
    all_items = set(counter1.keys()).union(set(counter2.keys()))
    vector1 = [counter1[k] for k in all_items]
    vector2 = [counter2[k] for k in all_items]
    return vector1, vector2
 
def calculate_cosim(v1, v2):
    dot_product = sum(n1 * n2 for n1, n2 in zip(v1, v2) )
    magnitude1 = math.sqrt(sum(n ** 2 for n in v1))
    magnitude2 = math.sqrt(sum(n ** 2 for n in v2))
    return round(dot_product / (magnitude1 * magnitude2),1) 

def jaccard(x,y):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    if(union_cardinality!=0):
        return round(intersection_cardinality/float(union_cardinality),1)
    else:
        return 0  
def process(bibtext):
    title=''
    aut=''
    try:
      titleindex=str(bibtext).index('title={')
      endtitleindex=str(bibtext).index('},',titleindex)
      title=str(bibtext)[titleindex+7:endtitleindex]
        
      autindex=str(bibtext).index('author={')
      endautindex=str(bibtext).index('},',autindex)
      aut=str(bibtext)[autindex+8:endautindex].replace("and","|")
      aut="Author:"+aut+"::"
      return title,aut
    except:
      print("Error in Bibtex format")
      print("""Example of bibtex format is:
             "@article{wickramarathne2011cofids,title={CoFiDS: A belief-theoretic approach for automated collaborative filtering},author={Wickramarathne, Thanuka L and Premaratne, Kamal and Kubat, Miroslav and Jayaweera, Dushyantha},journal={IEEE Transactions on Knowledge and Data Engineering},volume={23},number={2},pages={175--189},year={2011},publisher={IEEE}}" """)
      return title,aut



if __name__ == '__main__':

    if(len(sys.argv)!=1 and len(sys.argv)!=3):
             print("""Error in input""") 
             print("      Use:    <pythoncmd> <thisfilename.py> ")
             print("  or, use:    <pythoncmd> <thisfilename.py> <bibtex_citation> <source(\"Google Scholar\"|\"NDLI\")>")
             exit(-1)

    if not os.path.exists('./GoogleNews-vectors-negative300.bin.gz'):
               raise ValueError("SKIP: You need to download the Google News word vectors")
    print("Loading Google News word vectors. This may take a while...")
    model = word2vec.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin.gz', binary=True, limit=500000)
    model.init_sims(replace=True)
    print("Loading fastText word vectors. This may take a while...")
    model2 = FastText.load_fasttext_format('./wiki.simple/wiki.simple.bin')


    print("Starting internal browser. This may take a while and even fail!...")
    options = Options()
    options.add_argument("--headless")


    driver = webdriver.Firefox(firefox_options=options,executable_path=r'./geckodriver')
    url = 'https://scholar.google.co.in/'
    driver.get(url)
    time.sleep(5)
    driver.find_element_by_id("gs_hdr_mnu").click()
    driver.find_element_by_id("gs_hdr_drw_bs").click()
    driver.find_element_by_id("gs_settings_import_some").click()
    driver.find_element_by_xpath("//button[@class=' gs_btn_act gs_btn_lsb']").click()
    driver2 = webdriver.Firefox(firefox_options=options,executable_path=r'./geckodriver')
    reload(sys)
    print("Starting main application...")
    print("""*********** Default Options for Surrogator v2 *******************************
             "Select Years"                     : 3
             "Select Pages"                     : 1
             "Select Metadata"                  : "Author & Title"
             "Select Criteria"                  : "Near Match"
             "Select Similarity (for abstract)" : "Cosine Similarity (BoW)" 
             "Select Display Count"             : "Top 3"
*****************************************************************************""")
    #print(len(sys.argv))
    print("Arguments: ", sys.argv)
    if(len(sys.argv)==1):
              main()
    else:
              if(len(sys.argv)==3):
                              paper,excerpt=process(sys.argv[1])
                              source=sys.argv[2]
                              if(source != "Google Scholar" and source != "NDLI"):
                                  print("Source can be only \"Google Scholar\" or \"NDLI\"")
                                  exit(-1)
                              #print (paper,excerpt)
                              giv_crit="Near Match"  
                              giv_years="3"
                              giv_pages="1"
                              giv_usage="Author & Title"
                              giv_disp="Top 3"
                              giv_sim="Cosine Similarity (BoW)"
                              if(paper!="" and source=="NDLI"):
                                 collect_authoridlinkndl(paper,excerpt,giv_pages,giv_years,giv_usage,giv_crit,giv_disp,giv_sim)
                              elif(paper!="" and source=="Google Scholar"):
                                 paper=paper+excerpt
                                 collect_authoridlink(paper,giv_pages,giv_years,giv_usage,giv_crit,giv_disp,giv_sim)

              else:            
                              pass 





