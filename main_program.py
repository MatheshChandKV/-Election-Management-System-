import tkinter as tk
import pymysql as py


mode=None
voted_names=[]
irv_ballots=[]

DB_USER='root'
DB_PASSWORD='nimrutha12'
DB_HOST='localhost'
DB_DATABASE='election'

def update_winner_db(winner):
    try:
        db=py.connect(host=DB_HOST,user=DB_USER,password=DB_PASSWORD,database=DB_DATABASE)
        cursor=db.cursor()
        cursor.execute("UPDATE winners SET winner=%s WHERE election_id=1",(winner,))
        db.commit()
        cursor.close()
        db.close()
        print("Winner updated to database successfully.")
    except Exception as e:
        print(f"Error updating winner: {e}")

def fptp_vote():
    cnx=py.connect(user=DB_USER,password=DB_PASSWORD,host=DB_HOST,database=DB_DATABASE)
    cursor=cnx.cursor()
    cursor.execute("SELECT * FROM candidates")
    candidates=[row[0] for row in cursor.fetchall()]
    cursor.close()
    cnx.close()

    root3=tk.Toplevel(root)
    root3.title("Electoral Pad FPTP")
    root3.geometry('300x300+500+300')
    votes={candidate: 0 for candidate in candidates}

    def vote(candidate):
        votes[candidate] += 1
        root3.after(300,root3.destroy)
    for i,candidate in enumerate(candidates):
        label=tk.Label(root3,text=candidate)
        label.grid(row=i,column=0)
        button=tk.Button(root3,text="Vote",command=lambda c=candidate: vote(c))
        button.grid(row=i,column=1)
    root3.mainloop()
    winner=max(votes,key=votes.get)
    print("The winner is:",winner)
    update_winner_db(winner)

def approval_vote():
    db=py.connect(host=DB_HOST,user=DB_USER,password=DB_PASSWORD,database=DB_DATABASE)
    cursor=db.cursor()
    cursor.execute("SELECT * FROM candidates")
    candidates=[row[0] for row in cursor.fetchall()]
    cursor.close()
    db.close()

    root4=tk.Toplevel(root)
    root4.title("Electoral Pad APPROVAL")
    root4.geometry('300x300+500+300')
    votes={candidate: 0 for candidate in candidates}

    def toggle(candidate):
        votes[candidate] = 1 - votes[candidate]
        button=buttons[candidate]
        button.config(bg="#8FD3FF" if votes[candidate]==1 else "SystemButtonFace")
    def submit():
        winner=max(votes,key=votes.get)
        print("The winner is:",winner)
        update_winner_db(winner)
        root4.destroy()
    buttons={}
    for candidate in candidates:
        b=tk.Button(root4,text=candidate,command=lambda c=candidate: toggle(c))
        b.pack(pady=5)
        buttons[candidate]=b
    tk.Button(root4,text="Submit Votes",command=submit).pack(pady=20)
    root4.mainloop()

def irv_vote():
    cnx=py.connect(user=DB_USER,password=DB_PASSWORD,host=DB_HOST,database=DB_DATABASE)
    cursor=cnx.cursor()
    cursor.execute("SELECT * FROM candidates")
    candidates=[row[0] for row in cursor.fetchall()]
    cursor.close()
    cnx.close()

    root5=tk.Toplevel(root)
    root5.title("Electoral Pad IRV")
    root5.geometry('400x400+500+300')

    ballot=[]
    rank=1
    tk.Label(root5,text="Rank candidates (1 highest)",font=("Arial",11)).pack(pady=10)

    def pick(c):
        nonlocal rank
        if c not in ballot:
            ballot.append(c)
            btn[c].config(state="disabled",bg="#A4C8FF")
            rank+=1
        if len(ballot)==len(candidates):
            irv_ballots.append(ballot)
            root5.destroy()
            determine_irv_winner(candidates)
    btn={}
    for c in candidates:
        b=tk.Button(root5,text=c,width=20,command=lambda x=c: pick(x))
        b.pack(pady=4)
        btn[c]=b
    root5.mainloop()

def determine_irv_winner(candidates):
    remaining=candidates.copy()
    while True:
        counts={c:0 for c in remaining}
        for ballot in irv_ballots:
            for pref in ballot:
                if pref in remaining:
                    counts[pref]+=1
                    break
        total=sum(counts.values())
        for cand,v in counts.items():
            if v > total/2:
                print("IRV Winner:",cand)
                update_winner_db(cand)
                return
        loser=min(counts,key=counts.get)
        remaining.remove(loser)
        if len(remaining)==1:
            print("IRV Winner:",remaining[0])
            update_winner_db(remaining[0])
            return
    return

def admin():
    global pwd,pwd_win
    pwd_win=tk.Toplevel(root)
    pwd_win.title("Admin Login")
    pwd_win.geometry('200x200+500+300')
    pwd_label=tk.Label(pwd_win,text="Enter password:")
    pwd_label.pack()
    pwd=tk.StringVar()
    pwd_entry=tk.Entry(pwd_win,width=20,textvariable=pwd,show='*')
    pwd_entry.pack()
    pwd_entry.focus()
    pwd_entry.bind('<Return>',check_pwd)

def check_pwd(event=None):
    password=pwd.get()
    try:
        cnx=py.connect(user=DB_USER,password=DB_PASSWORD,host=DB_HOST,database=DB_DATABASE)
        cursor=cnx.cursor()
        cursor.execute("SELECT password FROM admin")
        row=cursor.fetchone()
        cursor.close()
        cnx.close()
        stored_pwd=row[0] if row else None
    except Exception:
        stored_pwd=None
    if stored_pwd and password==stored_pwd:
        pwd_win.destroy()
        admin_win()
    else:
        pass_label=tk.Label(root,text="Incorrect password",fg="red")
        pass_label.pack()
        pass_label.after(1000,pass_label.destroy)

def admin_win():
    root1=tk.Tk()
    root1.attributes('-fullscreen',True)
    root1.title("Admin Window")
    root1.config(bg='grey')
    label=tk.Label(root1,text="Welcome,Admin!\n Which mode?")
    label.place(relx=0.5,rely=0.2,anchor='center')
    global mode
    mode=' '
    tk.Button(root1,text='FPTP',command=lambda: set_mode('F')).place(relx=0.3,rely=0.5,anchor='center')
    tk.Button(root1,text='APPROVAL',command=lambda: set_mode('A')).place(relx=0.5,rely=0.5,anchor='center')
    tk.Button(root1,text='IRV',command=lambda: set_mode('I')).place(relx=0.7,rely=0.5,anchor='center')
    tk.Button(root1,text="GO BACK",command=root1.destroy).place(relx=0.5,rely=0.7,anchor='center')
    root1.mainloop()

def set_mode(m):
    global mode
    mode=m

def voter_win():
    global root2
    root2=tk.Toplevel(root)
    root2.title('VOTE WINDOW')
    root2.geometry('400x400+500+300')
    tk.Label(root2,text="VOTER NAME==>").place(relx=0.2,rely=0.2)
    tk.Label(root2,text="VOTER NUMBER==>").place(relx=0.2,rely=0.3)
    txt=tk.Entry(root2,width=20)
    txt.place(relx=0.5,rely=0.2)
    txt1=tk.Entry(root2,width=20)
    txt1.place(relx=0.5,rely=0.3)
    txt.focus()
    txt.bind('<Return>',lambda event: txt1.focus())
    txt1.bind('<Return>',lambda event: clicked(txt.get(),txt1.get()))

def clicked(name,number):
    if validate_voter(name,number):
        global mode
        if mode=='F':
            fptp_vote()
        elif mode=='A':
            approval_vote()
        elif mode=='I':
            irv_vote()
    else:
        at=tk.Label(root2,text='INCORRECT NAME OR NUMBER OR YOU WOULD HAVE ALREADY VOTED',fg='red')
        at.place(relx=0.3,rely=0.4)
        at.after(1000,at.destroy)

def validate_voter(name,number):
    global voted_names
    try:
        cnx=py.connect(user=DB_USER,password=DB_PASSWORD,host=DB_HOST,database=DB_DATABASE)
        cursor=cnx.cursor()
        cursor.execute("SELECT voter_number FROM voters WHERE name=%s",(name,))
        row=cursor.fetchone()
        cursor.close()
        cnx.close()
        db_num=str(row[0]) if row else None
    except Exception:
        db_num=None
    if db_num is not None and str(number)==db_num and name not in voted_names:
        voted_names.append(name)
        return True
    return False


root=tk.Tk()
root.attributes('-fullscreen',True)
root.title("Election")
root.geometry('1000x700+200+100')
canvas1=tk.Canvas(root,width=200,height=200,bg = "#95F1AF")
canvas1.pack(fill="both",expand=True)
btn1=tk.Button(root,text="ADMINISTRATOR",bg="#3B84C3",fg='#00FF00',font=("Segoe Print",15),relief="flat",width=15,height=1,command=admin)
btn2=tk.Button(root,text="VOTER",bg='#3B84C3',fg="#00FF00",font=("Segoe Print",15),relief="flat",width=15,height=1,command=voter_win)
button1_canvas=canvas1.create_window(451,500,anchor="center",window=btn1)
button2_canvas=canvas1.create_window(1085,500,anchor="center",window=btn2)
canvas1.create_text(775,400,anchor='center',fill='#007250',font=('Rockwell',60),text="ELECTION")
root.mainloop()