
from picamera import PiCamera
import smtplib
import time
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import RPi.GPIO as GPIO

toaddr = 'To Email'
me = 'From Email'
Subject='security alert'

GPIO.setmode(GPIO.BCM)

P=PiCamera()
P.resolution= (1024,768)
P.start_preview()

GPIO.setup(23, GPIO.IN)
while True:
    if GPIO.input(23):
        print("Motion...")
        #camera warm-up time
        time.sleep(2)
        P.capture('movement.jpg')
        time.sleep(10)
        subject='Security allert!!'
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = toaddr

        fp= open('movement.jpg','rb')
        img = MIMEImage(fp.read())
        fp.close()
        msg.attach(img)

        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(user = 'From Email',password='Password')
        server.send_message(msg)
        server.quit()

