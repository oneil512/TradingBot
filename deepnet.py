
from keras.layers import Input, Dense
from keras.models import Model
from keras.utils.vis_utils import *
from ingestData import *

# Get Data
(price, vol, weightedprice) = getPriceAndVolumeByTime()
(higher, lower) = partitionData(8, price, vol)
(train_data, train_class) = shapeData(higher, lower)

# Create Net
input_img = Input(shape=(16,))

encoded = Dense(12, activation='relu')(input_img)
encoded = Dense(6, activation='relu')(encoded)
encoded = Dense(2, activation='sigmoid')(encoded)

encoder = Model(input_img, encoded)


encoder.compile(optimizer='adadelta', loss='poisson', metrics=['accuracy'])


# Train Net
encoder.fit(train_data, train_class,
                    epochs=50,
                    batch_size=128,
                    shuffle=True,
                    validation_split=.2)


plot_model(encoder, show_shapes=True, to_file='model.png')

