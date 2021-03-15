import csv
import os
from tkinter import filedialog

def readCsv():
    path=filedialog.askopenfilename(initialdir="./resource",filetypes=[("CSV Files", "*.csv")],title="select [ KAKAO TALK CHAT ] file")
    with open(path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            print(', '.join(row))


if __name__=="__main__":
    readCsv()
    