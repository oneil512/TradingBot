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


# Create Net, work in progess

model = Sequential()
model.add(Embedding(vocabulary, hidden_size, input_length=num_steps))
model.add(LSTM(hidden_size, return_sequences=True))
model.add(LSTM(hidden_size, return_sequences=True))
model.add(Dropout(0.5))
model.add(TimeDistributed(Dense(vocabulary)))
model.add(Activation('softmax'))
encoder = Model(input_img, encoded)


encoder.compile(optimizer='adadelta', loss='categorical_crossentropy', metrics=['accuracy'])

# Train Net
encoder.fit(train_data, train_class,
                    epochs=50,
                    batch_size=128,
                    validation_split=.2)


plot_model(encoder, show_shapes=True, to_file='model.png')
