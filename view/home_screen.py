from PIL import Image
from PIL import ImageTk
import tkinter as tki
import cv2
import datetime
import os
import time
import json
import sys
import requests
import numpy as np

def create_home_screen(obj):
    obj.lab_home = tki.Label(text="Bem Vindo")
    obj.btn_go_client = tki.Button(obj.root, text="Comprar",
            command=lambda: obj.event_manager("go_client"))
    obj.btn_go_admin = tki.Button(obj.root, text="admin",
            command=lambda: obj.event_manager("go_admin"))

def pack_home_screen(obj):
    obj.lab_home.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.btn_go_client.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.btn_go_admin.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)

def hide_home_screen(obj):
    obj.lab_home.pack_forget()
    obj.btn_go_client.pack_forget()
    obj.btn_go_admin.pack_forget()

def create_client_main(obj):
    obj.panel = tki.Label(image=None)
    obj.panel.image = None
    obj.btn_snapshot = tki.Button(obj.root, text="Snapshot!",
            command=lambda: obj.event_manager("snapshot"))
    obj.btn_go_home = tki.Button(obj.root, text="go home",
            command=lambda: obj.event_manager("go_home"))

def pack_client_main(obj):
    obj.panel.pack(side="left", padx=10, pady=10)
    obj.btn_snapshot.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.btn_go_home.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)


def hide_client_main(obj):
    obj.btn_snapshot.pack_forget()
    obj.btn_go_home.pack_forget()
    obj.panel.pack_forget()

def create_client_show(obj):
    obj.lab_checkout = tki.Label(text="Confirme seu pedido jndfnanlsnaka = 1000 reais")
    obj.btn_checkout = tki.Button(obj.root, text="checkout",
            command=lambda: obj.event_manager("checkout"))
    obj.btn_repeat = tki.Button(obj.root, text="repeat",
            command=lambda: obj.event_manager("repeat"))

def pack_client_show(obj):
    obj.panel.pack(side="left", padx=10, pady=10)
    obj.lab_checkout.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.btn_checkout.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.btn_repeat.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.btn_go_home.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)

def hide_client_show(obj):
    obj.lab_checkout.pack_forget()
    obj.btn_checkout.pack_forget()
    obj.btn_repeat.pack_forget()
    obj.btn_go_home.pack_forget()
    obj.panel.pack_forget()

def create_client_pay(obj):
    obj.btn_pay = tki.Button(obj.root, text="pagar",
            command=lambda: obj.event_manager("pay"))
    obj.btn_cancel = tki.Button(obj.root, text="cancel",
            command=lambda: obj.event_manager("cancel"))

def pack_client_pay(obj):
    obj.lab_checkout.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.btn_pay.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.btn_cancel.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)

def hide_client_pay(obj):
    obj.lab_checkout.pack_forget()
    obj.btn_pay.pack_forget()
    obj.btn_cancel.pack_forget()

def create_thanks(obj):
    obj.lab_thanks = tki.Label(text="Compra Efetivada!! Volte Sempre")

def pack_thanks(obj):
    obj.lab_thanks.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)

def hide_thanks(obj):
    obj.lab_thanks.pack_forget()

def action0(obj):
    create_home_screen(obj)
    pack_home_screen(obj)

def action1(obj):
    hide_home_screen(obj)
    create_client_main(obj)
    #create_panel(obj)
    pack_client_main(obj)
    #pack_panel(obj)

def action2(obj):
    hide_client_main(obj)
    create_client_show(obj)
    pack_client_show(obj)
    ts = datetime.datetime.now()
    filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
    p = os.path.sep.join((obj.outputPath, filename))
    frame = obj.frame.copy()
    cv2.imwrite(p, frame)
    obj.last_photo = p
    print("[INFO] saved {}".format(filename))

    # YOLO
    frame = cv2.resize(frame, None, fx=0.4, fy=0.4)
    frame = frame.tolist()
    data = json.dumps(frame)
    print(sys.getsizeof(data))
    res = requests.post('http://localhost:5000/api/prediction', json = data)
    #res = requests.post('http://aws-test.eba-gajbic4g.sa-east-1.elasticbeanstalk.com/api/prediction', json = data)
    if res.ok:
        print("res ok")
        res = res.json()
        print(res["qtd"])
        obj.price = res["qtd"]
        img = res["data"]
        img = cv2.UMat(np.array(img, dtype=np.uint8))
        cv2.imwrite(p, img)
        obj.last_photo = p

def action3(obj):
    hide_client_show(obj)
    create_client_pay(obj)
    pack_client_pay(obj)

def action4(obj):
    hide_client_show(obj)
    pack_client_main(obj)

def action5(obj):
    hide_client_main(obj)
    pack_home_screen(obj)

def action6(obj):
    hide_client_show(obj)
    pack_home_screen(obj)

def action7(obj):
    hide_client_pay(obj)
    pack_home_screen(obj)

def action8(obj):
    hide_thanks(obj)
    pack_home_screen(obj)

def action9(obj):
    hide_client_pay(obj)
    create_thanks(obj)
    pack_thanks(obj)

def state1(obj):
    obj.frame = obj.vs.read()

    # OpenCV represents images in BGR order; however PIL
    # represents images in RGB order, so we need to swap
    # the channels, then convert to PIL and ImageTk format
    obj.image = cv2.cvtColor(obj.frame, cv2.COLOR_BGR2RGB)
    obj.image = Image.fromarray(obj.image)
    obj.image = ImageTk.PhotoImage(obj.image)

    # if the panel is None, we need to initialize it
    #if obj.panel is None:
        #obj.panel = tki.Label(image=obj.image)
        #obj.panel.image = obj.image
        #obj.panel.pack(side="left", padx=10, pady=10)

    # otherwise, simply update the panel
    obj.panel.configure(image=obj.image)
    obj.panel.image = obj.image

def state2(obj):
    # aqui vai o yolo
    if obj.last_photo:
        obj.frame = cv2.imread(obj.last_photo)
        obj.last_photo = None
        
        # display yolo image 
        obj.image = cv2.cvtColor(obj.frame, cv2.COLOR_BGR2RGB)
        obj.image = Image.fromarray(obj.image)
        obj.image = ImageTk.PhotoImage(obj.image)
        obj.panel.configure(image=obj.image)
        obj.panel.image = obj.image
        obj.lab_checkout.configure(text="Quantidade comprada: %d"%obj.price[0])

def state4(obj):
    time0 = time.time()
    time1 = time.time()
    while time1 - time0 < 2: time1 = time.time()
    obj.event_manager()
