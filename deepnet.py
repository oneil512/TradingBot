
from keras.layers import Input, Dense
from keras.models import Model
from keras.utils.vis_utils import *
from ingestData import *
import random
import numpy as np
from keras.utils.np_utils import to_categorical


(price, vol, weightedprice) = getPriceAndVolumeByTime()
(higher, lower) = partitionData(8, price, vol)

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

split = int(.75 * len(train_data))
x = np.arange(len(train_data))
np.random.shuffle(x)

train_data = np.array(train_data)
train_class = np.array(train_class)

train_data = train_data[x]
train_class = train_class[x]

test_class = train_class[split::]
test_data = train_data[split::]

np.delete(test_data, np.s_[split::], 0)
np.delete(test_class, np.s_[split::], 0)

print train_data.shape
print train_class.shape


#input_img = Input(shape=(28,28,1))

#x = Conv2D(16, (3, 3), activation='relu', padding='same')(input_img)
#x = MaxPooling2D((2,2), padding='same')(x)
#x = Conv2D(8, (3,3), activation='relu', padding='same')(x)
#x = MaxPooling2D((2,2), padding='same')(x)
#x = Conv2D(8, (3,3), activation='relu', padding='same')(x)
#encoded = MaxPooling2D((2,2), padding='same')(x)

input_img = Input(shape=(16,))

encoded = Dense(12, activation='relu')(input_img)
encoded = Dense(6, activation='relu')(encoded)
encoded = Dense(2, activation='sigmoid')(encoded)

encoder = Model(input_img, encoded)

#encoded_input = Input(shape=(encoding_dim,))
#decoder_layer = autoencoder.layers[-1]
#decoder = Model(encoded_input, decoder_layer(encoded_input))

encoder.compile(optimizer='adadelta', loss='categorical_crossentropy', metrics=['accuracy'])

encoder.fit(train_data, train_class,
                    epochs=50,
                    batch_size=128,
                    shuffle=True,
                    validation_data=(test_data, test_class))

encoded_imgs = encoder.predict(test_data)


plot_model(encoder, show_shapes=True, to_file='model.png')

