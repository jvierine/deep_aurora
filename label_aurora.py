import imageio
import matplotlib.pyplot as plt
import glob
import sys
import h5py
import numpy as n
from PIL import Image
import os
import h5py
dir_name="/data0/aurora/2*/jpgs/"
fl=glob.glob("%s/*.JPG"%(dir_name))
fl.sort()

idx=n.arange(len(fl),dtype=n.int)
#n.random.seed(0)
#n.random.shuffle(idx)

clouds=False
aurora=False
moon=False
snow=False
sunlight=False

txt=None


fi=0
while True:
    if fi < 0:
        fi=0
    if fi > len(fl)-1:
        fi=len(fl)-1
    f=fl[fi]

    par_fname="%s_par.h5"%(fl[fi])
    if os.path.exists(par_fname):
        print("reading %s"%(par_fname))
        h=h5py.File(par_fname,"r")
        clouds=h["clouds"].value
        aurora=h["aurora"].value
        moon=h["moon"].value
        snow=h["snow"].value
        sunlight=h["sunlight"].value
        h.close()
    
    im = Image.open(f)
    im=im.rotate(-90)

    def draw_text():
        global clouds, txt
        global aurora
        global moon
        global snow
        global sunlight

        labels=""
        if clouds:
            labels+=" 1) clouds "
        else:
            labels+="           "
        if aurora:
            labels+=" 2) aurora "
        else:
            labels+="           "
        if snow:
            labels+=" 3) snow/rain "
        else:
            labels+="              "
        if moon:
            labels+=" 4) moon "
        else:
            labels+="         "
        if sunlight:
            labels+=" 5) sunlight "
        else:
            labels+="             "

        if txt != None:
            txt.remove()
        txt=ax.text(5,10,labels,color="white")
            
        fig.canvas.draw()
        
    def press(event):
        global par_fname
        global clouds, clouds_txt
        global aurora, aurora_txt
        global moon, moon_txt
        global snow, snow_txt
        global sunlight, sunlight_txt        
        global fi

        x, y = event.xdata, event.ydata
        if event.key == '1':
            clouds=not clouds
            print(clouds)
            draw_text()

        if event.key == '2':
            aurora=not aurora
            print(aurora)
            draw_text()

        if event.key == '3':
            snow=not snow
            print(snow)
            draw_text()
            
        if event.key == '4':
            moon=not moon
            print(moon)
            draw_text()
            
        if event.key == '5':
            sunlight=not sunlight
            print(sunlight)
            draw_text()

        if event.key == '6':
            fi=fi-1
            plt.close()
        if event.key == '7':
            fi=fi+1
            plt.close()
        if event.key == '0':
            fi = int(n.floor(n.random.rand(1)*len(fl)))
            plt.close()
        h=h5py.File(par_fname,"w")
        print("saving %s"%(par_fname))
        h["clouds"]=clouds
        h["aurora"]=aurora
        h["moon"]=moon
        h["snow"]=snow
        h["sunlight"]=sunlight
        h.close()


            
    fig, ax = plt.subplots(figsize=(15,15))
    fig.canvas.mpl_connect('key_press_event', press)
    ax.imshow(im)
    plt.title("file %d %s\n 1) clouds 2) aurora 3) snow/rain 4) moon 5) scattered sunlight 6) prev 7) next 0) jump"%(fi,fl[fi]))
    plt.tight_layout()
    draw_text()    
    plt.show()
