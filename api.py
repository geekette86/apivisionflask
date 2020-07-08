import flask 
from flask import request, jsonify
#for file manipulation 
import io
from werkzeug import secure_filename
 #coding=utf-8  
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#for  operating sustem env and process
import os

#google vison api 
from google.cloud import vision

#library for graph vis based on math like matlab (kind of )
from matplotlib import pyplot as plt
from matplotlib import patches as pch

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["imgdir"] = 'images' 
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
@app.route('/',methods=['GET']) 
def home():
    return "<h1>You are in the right place, add some params</>"

@app.route('/procr', methods = ['GET', 'POST'])
def procr():
    #load credential file of Vision API

 os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(os.curdir, '../credentials.json')

#returns detected entities from the images
 client = vision.ImageAnnotatorClient()

#load and read image

 wineimage= request.files["file"]
 filename = secure_filename(wineimage.filename)
 filepath = os.path.join(app.config['imgdir'], filename);
 wineimage.save(filepath)
 
#Opens a file for reading only in binary format.
 with io.open(str(filepath), "rb") as image:
     content = image.read()
 image = vision.types.Image(content = content)
#detect text as first step 
 response = client.document_text_detection(
    image = image,
    image_context={"language_hints": ["fr"]},  #french
) 
 data = []
#if response is ok oCR is done with haluliya
 for page in response.full_text_annotation.pages:
  for block in page.blocks:
            
            data.append('Block confidence: {}'.format(block.confidence))

            for paragraph in block.paragraphs:
                data.append('Paragraph confidence: {}'.format(
                    paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    data.append('Word text: {} (confidence: {})'.format(
                        word_text, word.confidence))

                    for symbol in word.symbols:
                        data.append('Symbol: {} (confidence: {})'.format(
                            symbol.text, symbol.confidence))
  return {"response": data}
  #return jsonify(data)
    

 if response.error.message:
     raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
#return render_template("index.html")
app.run(port= 8887, host= 'localhost')
