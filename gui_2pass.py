# import files

import tkinter as tk                            
from tkinter import filedialog                  # importing filedialog for getting filename of selected file



# Function for showing which file is selected (input file)
def uploadInputFile():
    global input_file_path
    input_file_path = filedialog.askopenfilename()

    # checking if file is selected
    if input_file_path:         
        label1.config(text=f"Selected File: {input_file_path}")


# Function for showing which file is selected (optab file)
def uploadOptabFile():
    global optab_file_path
    optab_file_path = filedialog.askopenfilename()

    # checking if file is selected
    if optab_file_path:         
        label2.config(text=f"Selected File: {optab_file_path}")

# pass 1 function
def pass1():
    global loctor,start,length,count
    count = 0
    # opening files                     
    f1 = open(input_file_path,"r")
    f3 = open("output_gui.txt","w")
    f4 = open("symtab_gui.txt","w")
    f5 = open("length_gui.txt","w")

    inp,inp2 = [], []                                  # list to store the values read from files
    lines = f1.readline()                             
    fields = lines.split(' ')                          # for taking each item sepearted by a space
    inp.extend(fields)

    # checking if opcode is START
    if inp[1] == "START":
        start = int(inp[2].rstrip())                    # rstrip function is used here to remove the \n from the end
        loctor = start
        f3.write(f"\t{inp[0]}\t{inp[1]}\t{inp[2]}")
        label3.config(text=f"\t{inp[0]}\t{inp[1]}\t{inp[2]}")
        inp = []                                        # list is made empty to enter the new values from file
        lines = f1.readline()
        fields = lines.split(' ')
        inp.extend(fields)
    else:
        loctor = 0

    # travesing till END is reached
    while inp[1] != "END":
        f3.write(f"{loctor}\t{inp[0]}\t{inp[1]}\t{inp[2]}")
        current_text1 = label3.cget("text")   
        label3.config(text=f"{current_text1}{loctor}\t{inp[0]}\t{inp[1]}\t{inp[2]}")

        if inp[0] == "**":
            count += 3
        # to check if it is a label and then write it to symtab file
        if inp[0] != "**":
            f4.write(f"{inp[0]}\t{loctor}\n")
            current_text2 = label4.cget("text")
            label4.config(text=f"{current_text2}{inp[0]}\t{loctor}\n")

        f2 = open(optab_file_path,"r")
        inp2 = []
        lines2 = f2.readline()
        fields2 = lines2.split(' ')
        inp2.extend(fields2)

        while inp2[0] != "END":
            if inp[1] == inp2[0]:
                loctor += 3
                break
            inp2 = []
            lines2 = f2.readline()
            fields2 = lines2.split(' ')
            inp2.extend(fields2)
            

        f2.close()                                         # file is closed here to ensure that the optab file is read from start in the next loop

        if inp[1] == "WORD":
            loctor += 3
            count += 3
        elif inp[1] == "RESW":
            loctor +=(3*(int(inp[2].rstrip())))
        elif inp[1] == "BYTE":
            loctor += 1
            count += 1
        elif inp[1] == "RESB":
            loctor += int(inp[2].rstrip())
        
        inp = []
        lines = f1.readline()
        fields = lines.split(' ')
        inp.extend(fields)

    f3.write(f"{loctor}\t{inp[0]}\t{inp[1]}\t{inp[2]}")
    current_text1 = label3.cget("text")
    label3.config(text=f"{current_text1}{loctor}\t{inp[0]}\t{inp[1]}\t{inp[2]}")
    

    # closing files
    f1.close()
    f3.close()
    f4.close()

    length = loctor - start                                 # calculating the length
    f5.write(str(length))
    f5.close()
       
# pass 2 function
def pass2():
    global prevaddr,finaddr,diff,start,leng,actual_len,ad,fields2
    mnemonic = ["LDA","STA","LDCH","STCH"]
    code = ["33","44","53","57"]
    j = 0

    # opening files
    f1 = open("final_output_gui.txt","w")
    f2 = open("symtab_gui.txt","r")
    f3 = open("output_gui.txt","r")
    f4 = open("object_gui.txt","w")
    
    inp = []
    lines = f3.readline()
    fields = lines.split('\t')
    inp.extend(fields)

    inp = []                                                # reading the second line since we need second line first
    lines = f3.readline()
    fields = lines.split('\t')                              # seperating each item in file using tab space as the delimiter   
    inp.extend(fields)

    while inp[2] != "END":
        prevaddr = int(inp[0])
        inp = []
        lines = f3.readline()
        fields = lines.split('\t')
        inp.extend(fields)
    finaddr = inp[0]
    f3.close()
    f3 = open("output_gui.txt","r")

    inp = []
    lines = f3.readline()
    fields = lines.split('\t')
    inp.extend(fields)

    if inp[2] == "START":
        f1.write(f"\t{inp[1]}\t{inp[2]}\t{inp[3]}")
        label3.config(text=f"\t{inp[1]}\t{inp[2]}\t{inp[3]}")
        f4.write(f"H^{inp[1]}^00{inp[3]}^00{finaddr}\n")
        label4.config(text=f"H^{inp[1]}^00{inp[3].rstrip()}^00{finaddr}\n")
        inp = []
        lines = f3.readline()
        fields = lines.split('\t')
        inp.extend(fields)
        start = int(inp[0])
        diff = count
        f4.write(f"T^00{inp[0]}^{hex(diff)[2:]}")
        current_text2 = label4.cget("text")   
        label4.config(text=f"{current_text2}T^00{inp[0]}^{hex(diff)[2:]}")
    while inp[2] != "END":
        if inp[2].rstrip() == "BYTE":                                           # rstrip is used to remove the \n at the end 
            f1.write(f"{inp[0]}\t{inp[1]}\t{inp[2]}\t{inp[3].rstrip()}\t")
            current_text1 = label3.cget("text")   
            label3.config(text=f"{current_text1}{inp[0]}\t{inp[1]}\t{inp[2]}\t{inp[3].rstrip()}\t")
            leng = len(inp[3])
            actual_len = leng - 3
            f4.write("^")
            current_text2 = label4.cget("text")   
            label4.config(text=f"{current_text2}^")
            for i in range(2,actual_len+1):
                ad = str(hex(ord(inp[3][i]))[2:])                               # hex used for hex conversion, ord for ascii value,[2:] is for removing the hex representaion of 0x which is generated when using the hex() function
                f1.write(ad)
                current_text1 = label3.cget("text")   
                label3.config(text=f"{current_text1}{ad}")
                f4.write(ad)
                current_text2 = label4.cget("text")   
                label4.config(text=f"{current_text2}{ad}")
            f1.write("\n")
            current_text1 = label3.cget("text")   
            label3.config(text=f"{current_text1}\n")
        elif inp[2] == "WORD":
            leng = len(inp[2])
            a = str(int(inp[3]))
            f1.write(f"{inp[0]}\t{inp[1]}\t{inp[2]}\t{inp[3].rstrip()}\t00000{a}\n")
            current_text1 = label3.cget("text")   
            label3.config(text=f"{current_text1}{inp[0]}\t{inp[1]}\t{inp[2]}\t{inp[3].rstrip()}\t00000{a}\n")
            f4.write(f"^00000{a}")
            current_text2 = label4.cget("text")   
            label4.config(text=f"{current_text2}^00000{a}")
        elif (inp[2] == "RESB" or inp[2] == "RESW"):
            f1.write(f"{inp[0]}\t{inp[1]}\t{inp[2]}\t{inp[3]}")
            current_text1 = label3.cget("text")   
            label3.config(text=f"{current_text1}{inp[0]}\t{inp[1]}\t{inp[2]}\t{inp[3]}")
        else:
            while inp[2] != mnemonic[j]:
                j += 1
            if inp[2] == "COPY":
                f1.write(f"{inp[0]}\t{inp[1]}\t{inp[2]}\t{inp[3].rstrip()}\t{code[j]}")
                current_text1 = label3.cget("text")   
                label3.config(text=f"{current_text1}{inp[0]}\t{inp[1]}\t{inp[2]}\t{inp[3].rstrip()}\t{code[j]}")
            else:
                f2.seek(0)                                                      # seek(0) is used to change the file pointer to start of file
                inp2 = []
                lines2 = f2.readline()
                fields2 = lines2.split('\t')
                inp2.extend(fields2)
                while inp[3].rstrip() != inp2[0]:
                    inp2 = []
                    lines2 = f2.readline()
                    fields2 = lines2.split('\t')
                    inp2.extend(fields2)
                    


                f1.write(f"{inp[0]}\t{inp[1]}\t{inp[2]}\t{inp[3].rstrip()}\t{code[j]}{inp2[1]}")
                current_text1 = label3.cget("text")   
                label3.config(text=f"{current_text1}{inp[0]}\t{inp[1]}\t{inp[2]}\t{inp[3].rstrip()}\t{code[j]}{inp2[1]}")
                f4.write(f"^{code[j]}{inp2[1].rstrip()}")
                current_text2 = label4.cget("text")   
                label4.config(text=f"{current_text2}^{code[j]}{inp2[1].rstrip()}")
                
        inp = []
        lines = f3.readline()
        fields = lines.split('\t')
        inp.extend(fields)        

    f1.write(f"{inp[0]}\t{inp[1]}\t{inp[2]}\t{inp[3]}")
    current_text1 = label3.cget("text")   
    label3.config(text=f"{current_text1}{inp[0]}\t{inp[1]}\t{inp[2]}\t{inp[3]}")
    f4.write(f"\nE^00{start}")
    current_text2 = label4.cget("text")   
    label4.config(text=f"{current_text2}\nE^00{start}")

    # closing files
    f1.close()
    f2.close()
    f3.close()
    f4.close()

    


# Creating the window
root = tk.Tk()
root.title("TWO PASS ASSEMBLER")                # Title for the Application
root.config(bg="#EAEAEA")                       # backgroundcolor for the window

#creating the Buttons and Labels
inputFileButton = tk.Button(root,text="upload input file",command=uploadInputFile)
label1 = tk.Label(root,text="No File Selected")
optabFileButton = tk.Button(root,text="upload optab file",command=uploadOptabFile)
label2 = tk.Label(root,text="No File Selected")
passbutton = tk.Button(root,text="PASS 1",command=pass1)
passbutton2 = tk.Button(root,text="PASS 2",command=pass2)
label3 = tk.Label(root,text="",justify="left")
label4 = tk.Label(root,text="",justify="left")

# Positioning the Buttons and Labels
inputFileButton.place(x=100,y=100)
optabFileButton.place(x=100,y=300)
passbutton.place(x=100,y=500)
passbutton2.place(x=400,y=500)
label1.place(x=100,y=200)
label2.place(x=100,y=400)
label3.place(x=700,y=100)
label4.place(x=700,y=300)

# setting the background and foreground colors for buttons and labels
inputFileButton.config(bg="#5B8DF1", fg="#FFFFFF")
optabFileButton.config(bg="#5B8DF1", fg="#FFFFFF")
passbutton.config(bg="#5B8DF1", fg="#FFFFFF")
passbutton2.config(bg="#5B8DF1", fg="#FFFFFF")
label1.config(bg="#2C3E50", fg="#ECF0F1")
label2.config(bg="#2C3E50", fg="#ECF0F1")
label3.config(bg="#EAEAEA", fg="#2C3E50")  
label4.config(bg="#EAEAEA", fg="#2C3E50")  


root.mainloop()                                 # starts the Tkinter event loop
