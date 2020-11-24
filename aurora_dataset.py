import tensorflow as tf
import glob
import numpy
import h5py
import imageio
import re
import os
import numpy as n
import matplotlib.pyplot as plt

class aurora_basic_classes(tf.keras.utils.Sequence):
    def __init__(self,dirname="/data0/aurora/",batch_size=32):
        self.dirname=dirname
        self.par_fl=glob.glob("%s/*/jpgs/*_par.h5"%(dirname))
        self.n_im = len(self.par_fl)
        self.tn_fl=[]
        self.prefixes=[]
        self.batch_size=batch_size
        for f in self.par_fl:
            prefix=re.search("(.*)_par.h5",f).group(1)
            self.prefixes.append(prefix)
            tn_fname="%s.64.jpg"%(prefix)
            if not os.path.exists(tn_fname):
                print("warning thumbnail doesn't exits. we may need to generate it first")
            if not os.path.exists(prefix):
                print("warning high res image doesn't exist. aborting")
            self.tn_fl.append(tn_fname)
        im=imageio.imread(self.tn_fl[0])
        self.tn_shape=im.shape
        print(len(self.tn_fl))
        print(len(self.prefixes))
        print(self.tn_shape)

        self.data_idx=n.arange(self.n_im,dtype=n.int)
        n.random.shuffle(self.data_idx)
        
    def __len__(self):
        return(int(n.floor(self.n_im/float(self.batch_size))))
    def __getitem__(self,idx):

        idxs=n.arange(self.batch_size,dtype=n.int)+idx*self.batch_size
        imgs=n.zeros([self.batch_size,self.tn_shape[0],self.tn_shape[1],self.tn_shape[2],1],dtype=n.float32)
        classes=n.zeros([self.batch_size,5],dtype=n.float32)
        for ii,i in enumerate(idxs):
            fi=self.data_idx[i]
            h=h5py.File(self.par_fl[fi],"r")
            a=[n.copy(h[("clouds")]),n.copy(h[("aurora")]),n.copy(h[("snow")]),n.copy(h[("moon")]),n.copy(h[("sunlight")])]
            classes[ii,:]=a
            h.close()
            im = n.array(imageio.imread(self.tn_fl[fi]),dtype=n.float32)/255.0
            imgs[ii,:,:,:,0]=im
        return(imgs,classes)


        

if __name__ == "__main__":
    a=aurora_basic_classes()
    imgs,classes=a.__getitem__(0)
    for i in range(imgs.shape[0]):
        im=imgs[i,:,:,:,0]
        plt.imshow(im)
        plt.title(classes[i,:])
        plt.show()
