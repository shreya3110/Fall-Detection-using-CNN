import tkinter as tk
from PIL import Image, ImageTk
import time
import numpy as np
import cv2
import os
import shutil
import threading
import simpleaudio as sa
import smtplib
from email.mime.text import MIMEText
from tkinter.filedialog import askopenfilename
import Train_FDD_cnn as TrainM
from session import current_user

# ======================= Email Configuration =======================
YOUR_GMAIL =  current_user # 🔁 Replace with your Gmail
APP_PASSWORD = "Enter APP Password"  # 🔐 Your Gmail App Password

def send_email_notification():
    subject = "🚨 Fall Detected!"
    body = "A fall has been detected by the Fall Detection System. Immediate attention required."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "System Mail"
    msg["To"] = YOUR_GMAIL  # Sending to self

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("System mail", APP_PASSWORD)
        server.sendmail("System mail", YOUR_GMAIL, msg.as_string())
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print("❌ Failed to send email:", e)

# ======================= GUI Setup =======================
root = tk.Tk()
root.state('zoomed')
root.title("Fall-No Fall Detection System")

current_path = str(os.path.dirname(os.path.realpath('__file__')))
basepath = current_path + "\\"

img = Image.open("f3.jpg")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
bg = img.resize((w, h), Image.LANCZOS)
bg_img = ImageTk.PhotoImage(bg)
bg_lbl = tk.Label(root, image=bg_img)
bg_lbl.place(x=0, y=0)

heading = tk.Label(root, text="Fall Detection System", width=25,
                   font=("Times New Roman", 45, 'bold'), bg="#192841", fg="white")
heading.place(x=240, y=0)

# ======================= Helper Functions =======================
def CLOSE():
    root.destroy()

def update_label(str_T):
    result_label = tk.Label(root, text=str_T, width=50,
                            font=("bold", 25), bg='cyan', fg='black')
    result_label.place(x=400, y=400)

def train_model():
    update_label("Model Training Start...............")
    start = time.time()
    X = TrainM.main()
    end = time.time()
    ET = "Execution Time: {0:.4} seconds \n".format(end - start)
    msg = "Model Training Completed.." + '\n' + X + '\n' + ET
    update_label(msg)

# ======================= Main Fall Detection Logic =======================
def show_FDD_video(video_path):
    from keras.models import load_model

    img_cols, img_rows = 64, 64
    FALLModel = load_model('FALLModel_cleaned.keras')
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print(f"{video_path} cannot be opened")
        return

    font = cv2.FONT_HERSHEY_SIMPLEX
    green = (0, 255, 0)
    red = (0, 0, 255)
    line_type = cv2.LINE_AA
    i = 1
    alarm_playing = False
    email_sent = False
    stop_alarm = threading.Event()

    def play_alarm():
        try:
            wave_obj = sa.WaveObject.from_wave_file("alarm.wav")
            play_obj = wave_obj.play()
            while not stop_alarm.is_set() and play_obj.is_playing():
                time.sleep(0.1)
            play_obj.stop()
        except Exception as e:
            print("[ERROR] Alarm sound failed:", e)

    alarm_thread = None

    while True:
        ret, frame = video.read()
        if not ret:
            break

        img = cv2.resize(frame, (img_cols, img_rows), interpolation=cv2.INTER_CUBIC)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        X_img = img.reshape(-1, img_cols, img_rows, 1).astype('float32') / 255

        predicted = FALLModel.predict(X_img)
        label = 1 if predicted[0][0] < 0.5 else 0
        label_text = "Fell" if label == 1 else "Walking"
        color = red if label == 1 else green

        # Draw on frame
        cv2.putText(frame, f"Frame: {i}", (20, 30), font, 0.8, color, 2, line_type)
        cv2.putText(frame, f"Label: {label_text}", (20, 60), font, 0.8, color, 2, line_type)

        cv2.imshow('FDD', frame)

        if label == 1:
            # Start alarm only once
            if not alarm_playing:
                alarm_playing = True
                stop_alarm.clear()
                alarm_thread = threading.Thread(target=play_alarm, daemon=True)
                alarm_thread.start()

            # Send email once
            if not email_sent:
                email_sent = True
                threading.Thread(target=send_email_notification, daemon=True).start()

            time.sleep(0.5)  # 20ms delay for fall frame
        i += 1

        if cv2.waitKey(30) & 0xFF == 27:
            break

    stop_alarm.set()
    if alarm_thread:
        alarm_thread.join()
    video.release()
    cv2.destroyAllWindows()

# ======================= Video Verify =======================
def Video_Verify():
    global fn
    fn = askopenfilename(initialdir='/dataset', title='Select image',
                         filetypes=[("all files", "*.*")])
    if not fn.lower().endswith('.mp4'):
        print("Select Video File!!!!!!")
    else:
        show_FDD_video(fn)

# ======================= Buttons =======================
button5 = tk.Button(root, command=Video_Verify, text="Fall Detection", width=20,
                    font=("Times new roman", 25, "bold"), bg="cyan", fg="black")
button5.place(x=100, y=150)

close = tk.Button(root, command=CLOSE, text="Exit", width=20,
                  font=("Times new roman", 25, "bold"), bg="red", fg="black")
close.place(x=100, y=300)

root.mainloop()
