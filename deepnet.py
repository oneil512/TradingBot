
from keras.layers import Input, Dense
from keras.models import Model
from keras.utils.vis_utils import *
from ingestData import *
import random
import numpy as np
from keras.utils.np_utils import to_categorical


(price, vol, weightedprice) = getPriceAndVolumeByTime()
(higher, lower) = partitionData(8, weightedprice, vol)

data = zip(higher, lower)
random.shuffle(data)

train_data = []
train_class = []

for record in data:
    F, T = record
    F_data, F_class = F
    T_data, T_class = T

    train_data.append(F_data)
    train_data.append(T_data)
    train_class.append([F_class])
    train_class.append([T_class])

train_class = to_categorical(train_class)

print train_data.shape
print train_class.shape


input_img = Input(shape=(16,))

encoded = Dense(12, activation='relu')(input_img)
encoded = Dense(6, activation='relu')(encoded)
encoded = Dense(2, activation='sigmoid')(encoded)

encoder = Model(input_img, encoded)


encoder.compile(optimizer='adadelta', loss='categorical_crossentropy', metrics=['accuracy'])

encoder.fit(train_data, train_class,
                    epochs=50,
                    batch_size=128,
                    shuffle=True,
                    verbosity=2,
                    validation_split=20.0)

encoded_imgs = encoder.predict(test_data)


plot_model(encoder, show_shapes=True, to_file='model.png')

