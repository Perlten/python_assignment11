import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import cv2
from tensorflow.keras.models import Model
import glob



# example of progressively loading images from file
# create generator
# datagen = ImageDataGenerator(rescale=1./255,)
# train_it = datagen.flow_from_directory('dataset/train', class_mode='categorical', batch_size=32)
# test_it = datagen.flow_from_directory('dataset/test', class_mode='categorical', batch_size=32)
def resize(image, new_dim):
    dim = (new_dim, new_dim)
    resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized_image

def make_labels(label_list):
    y_train = []
    for x in label_list:
        if x == "apple":
            y_train.append(0)
        if x == "banana":
            y_train.append(1)
        if x == "orange":
            y_train.append(2)
    y_train = np.asarray(y_train)
    return y_train

def import_images(filelist):
    num_image = np.array([cv2.cvtColor(cv2.imread(fname), cv2.COLOR_BGR2RGB) for fname in filelist])
    return np.asarray([resize(image, 64) for image in num_image])

train_filelist = glob.glob('dataset2/train/*')
train_label_list = [name.split("_")[0].split("/")[-1] for name in train_filelist]
x_train = import_images(train_filelist)
y_train = make_labels(train_label_list)

test_filelist = glob.glob('dataset2/test1/*')
test_label_list = [name.split("_")[0].split("/")[-1] for name in test_filelist]
print(test_label_list)
x_test = import_images(test_filelist)
y_test = make_labels(test_label_list)

x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(3, activation=tf.nn.softmax))
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
 )
model.fit(x_train, y_train, epochs=22)
val_loss, val_acc = model.evaluate(x_test, y_test)
predictions = model.predict([x_test])


for x in range(len(test_label_list)):
    pred_label = np.argmax(predictions[x])
    print("The label was:", pred_label, "and was", test_label_list[x])