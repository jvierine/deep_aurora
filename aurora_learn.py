import tensorflow as tf

# "hot dog" vs "not hot dog" for aurora
from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras import Model
import h5py
import numpy as n
import matplotlib.pyplot as plt

import aurora_dataset as ad

a=ad.aurora_basic_classes(dirname="/scratch/data/juha/aurora/",batch_size=32)
im,sc=a[0]
print(im)
print(sc)

#ms=tf.distribute.MirroredStrategy()
#with ms.scope():
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu', input_shape=(128,128,3)),
    tf.keras.layers.MaxPooling2D((2,2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2,2)),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2,2)),    
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2,2)),    
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(1024,activation="relu"),
    tf.keras.layers.Dense(1024,activation="relu"),
    tf.keras.layers.Dense(5,activation="relu")
])

#loss='mean_squared_logarithmic_error',
#mean_squared_logarithmic_error',
model.compile(loss='mse',
              optimizer=tf.keras.optimizers.Adam(0.0001))
model.summary()

history = model.fit(a,
                    batch_size=32,
                    epochs=20)



for i in range(len(a)):
    imgs,sc=a[i]
    pr=model.predict(imgs)
    for imi in range(imgs.shape[0]):
        plt.imshow(imgs[imi,:,:,:])
        print(pr[imi,:])
        labelstr=""
        if pr[imi,0]>0.5:
            labelstr+="clouds "
        if pr[imi,1]>0.5:
            labelstr+="aurora "
        if pr[imi,2]>0.5:
            labelstr+="snow/rain "
        if pr[imi,3]>0.5:
            labelstr+="moon "
        if pr[imi,4]>0.5:
            labelstr+="sunlight "
        plt.title(labelstr)
        plt.show()



