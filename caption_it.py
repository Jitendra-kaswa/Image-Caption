#import pandas as pd
#import matplotlib.pyplot as plt
#import re
#import nltk
#from nltk.corpus import stopwords
#import string
#from time import time
#from keras.applications.vgg16 import VGG16
import pickle
import json
import keras
import numpy as np
from keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from keras.preprocessing import image
from keras.models import Model, load_model
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.layers import Input, Dense, Dropout, Embedding, LSTM
from keras.layers.merge import add

with open("model_weights/word_to_idx.pkl","rb") as w2i:
  word_to_idx=pickle.load(w2i)

with open("model_weights/idx_to_word.pkl","rb") as i2w:
  idx_to_word=pickle.load(i2w)


path ="model_weights/model_9.h5"
model=load_model(path)
#model._make_predict_function()

model_temp = ResNet50(weights="imagenet",input_shape=(224,224,3))
model_resnet = Model(model_temp.input,model_temp.layers[-2].output)
#model_resnet._make_predict_function()

def preprocess_img(img):
    img = image.load_img(img,target_size=(224,224))
    img = image.img_to_array(img)
    img = np.expand_dims(img,axis=0)
    # Normalisation
    img = preprocess_input(img) # resnet has it's own preprocess model
    return img

def encode_image(img):
    img = preprocess_img(img)
    feature_vector = model_resnet.predict(img)

    feature_vector = feature_vector.reshape(1,feature_vector.shape[1])
    #print(feature_vector.shape)
    return feature_vector

def predict_caption(photo):

    in_text = "startseq"
    max_len=35
    for i in range(max_len):
      #max_len was 35 in our model
        sequence = [word_to_idx[w] for w in in_text.split() if w in word_to_idx]
        sequence = pad_sequences([sequence],maxlen=max_len,padding='post')

        ypred = model.predict([photo,sequence])
        ypred = ypred.argmax() #WOrd with max prob always - Greedy Sampling
        word = idx_to_word[ypred]
        in_text += (' ' + word)

        if word == "endseq":
            break

    final_caption = in_text.split()[1:-1]
    final_caption = ' '.join(final_caption)
    return final_caption

def caption_this_image(image):
	enc = encode_image(image)
	caption = predict_caption(enc)

	return caption
