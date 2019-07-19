import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import stream_with_context
from flask import jsonify
from flask_cors import CORS, cross_origin

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = ['.pdf','.docx','.png']

app = Flask(__name__)
cors=CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024


def allowed_file(filename):
   ext=os.path.splitext(filename)[1]
   if not ext.lower() in ALLOWED_EXTENSIONS:
     return False
   else:
       return True

@app.route('/upload', methods=['POST'])
@cross_origin(allow_headers=['Content-Type','Authorization'])
def upload_file():
   if request.method == 'POST':
       # check if the post request has the file part
       if 'file' not in request.files:
            res={'Response': None,
            'Error': 'No file Part'}

       file = request.files['file']
       if file.filename == '':
            res={'Response': None,
            'Error': 'No file Selected'}
           



       if file and allowed_file(file.filename):
         filename = secure_filename(file.filename)
         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
         ch=50
         ext=os.path.splitext(filename)[1]
         path="uploads/user_id"+ext.lower()

         with open(path, "wb") as f:
            chunk_size = 10
            while True:
                  chunk = file.stream.read(chunk_size)
                  if len(chunk)==0:
                     res={'Response': 'Saved',
                        'Error': None}
                     return jsonify(res)
                  else:
                     f.write(chunk)
        #            # if len(chunk) == 0:
        #            #     res = {'Error':'No file'}
        #            #     return jsonify(res)
        #            # f.write(chunk)
         # with open(path, "wb") as f:
         #    f.write(file.stream.read())

           res={'Response': 'Saved',
           'Error': None}
    return jsonify(res)

@app.errorhandler(413)
def request_entity_too_large(error):
   return "File is too large to upload"

if __name__=="__main__":
   app.run(debug=True,host="127.0.0.1", port='8080')