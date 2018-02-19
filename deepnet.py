
from keras.layers import Input, Dense
from keras.models import Model
from keras.utils.vis_utils import *
from ingestData import *
import random
import numpy as np
from keras.utils.np_utils import to_categorical

# Get Data
(price, vol, weightedprice) = getPriceAndVolumeByTime()
(higher, lower) = partitionData(8, weightedprice, vol)
(train_data, train_class) = shapeData(higher, lower)

# Create Net
input_img = Input(shape=(16,))

encoded = Dense(12, activation='relu')(input_img)
encoded = Dense(6, activation='relu')(encoded)
encoded = Dense(2, activation='sigmoid')(encoded)

encoder = Model(input_img, encoded)


encoder.compile(optimizer='adadelta', loss='categorical_crossentropy', metrics=['accuracy'])


# Train Net
encoder.fit(train_data, train_class,
                    epochs=50,
                    batch_size=128,
                    shuffle=True,
                    verbosity=2,
                    validation_split=20.0)

encoded_imgs = encoder.predict(test_data)


plot_model(encoder, show_shapes=True, to_file='model.png')

