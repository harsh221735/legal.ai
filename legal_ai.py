# -*- coding: utf-8 -*-
"""legal_ai.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iKk5RIiSkxqRvlq_ngRA2pNwq722-zXe

# **EXTRACTION PROCESS**
"""

!pip install easyocr

!pip install language_tool_python

import easyocr
import cv2
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from google.colab.patches import cv2_imshow

img = cv2.imread('/content/sample1.jpeg')
img = cv2.resize(img, (900,900))
cv2_imshow(img)

# Apply adaptive thresholding
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
threshold_img = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 10)
cv2_imshow(threshold_img)

reader = easyocr.Reader(['en'],gpu = False)
result = reader.readtext(threshold_img)

df = pd.DataFrame(result)
data = ' '.join(df[1].astype(str))
print(data)

# dividing text to get n words in each part in order to feed in the model
#text = 'hi i am harsh . ia m 18 yers old i am a gib byo so i'
words = data.split()
per_text = []
n = 12
i = 0
j = n
x = 0
while x<= len(words):
  temp_text = words[i:j]
  per_text.append(temp_text)
  i = j
  j = j+n
  x = i
print(per_text)
print(len(words))

#post processing
from transformers import pipeline

corrector = pipeline('text2text-generation', model='prithivida/grammar_error_correcter_v1')
fi_result = []
for i in per_text:
  div_words = ' '.join(i)
  result = corrector(div_words)
  fi_result.append(result[0]['generated_text'].split())
fi_result = [word for sublist in fi_result for word in sublist]
fi_result = ' '.join(fi_result)
print(fi_result)
word = fi_result.split()
print(len(word))

"""## **END OF EXTRACTION PROCESS**

# **START OF SUMMARIZATION**
"""

for (bbox, text, prob) in result:
  (tl, tr, br, bl) = bbox
  tl = (int(tl[0]), int(tl[1]))
  tr = (int(tr[0]), int(tr[1]))
  br = (int(br[0]), int(br[1]))
  bl = (int(bl[0]), int(bl[1]))
  cv2.rectangle(img, tr, bl, (0, 255, 0), 2)
cv2_imshow(img)

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load the model and tokenizer
model_name = "sshleifer/distilbart-cnn-12-6"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Your long text
text = """
The 2024 Summer Olympics will be held in Paris, France.
The event is expected to bring together athletes from around the world to compete in a wide range of sports.
Preparations are underway, with new infrastructure projects being developed across the city.
"""

# Tokenize input
inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)

# Generate summary
summary_ids = model.generate(inputs["input_ids"], max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)

# Decode and print the summary
summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
print(summary)

