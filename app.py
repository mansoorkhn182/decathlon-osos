from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from os.path import join, dirname, realpath
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import decathlon
import decathlon_get_results
import json

app = Flask(__name__)

## setup database for storing username and filename. Later on can use for authentication
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///decathlon.db'
db = SQLAlchemy(app)

## User table in database which store username and file
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    file = db.Column(db.String(80))
# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = '/DECATHLONTEST/static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

# Root URL
@app.route('/')
def index():
     # Set The upload HTML template '\templates\index.html'
    return render_template('index.html')


# Get the uploaded files, this post method will upload the files to folder and get the results
@app.route("/", methods=['POST'])
def uploadFiles():
      # get the uploaded file
      uploaded_file = request.files['file']
      username = request.form.get('username')
      #print(username)
      if uploaded_file.filename != '':
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
          # set the file path
           uploaded_file.save(file_path)
          # save the file
      user = User(username=username, file=uploaded_file.filename)
      db.session.add(user)
      db.session.commit()
      db.session.close()
      return redirect(url_for('.procdata', username=username))

### this method will get the data from database and load the csv file from the server and do the data operations
@app.route("/dataproc")
def procdata():
    
    username = request.args['username'] 
    user_data = User.query.filter_by(username=username).first()
    filename = user_data.file
    file_path = '/DECATHLONTEST/static/files/'+filename
    data_file = pd.read_csv(file_path,sep=";",header=None)  # load data
    
    ## Data Preparation (add columns to the data)
    data_file.columns = ["Athlets", "100m", "Long.jump", "Shot.put",	"High.jump", "400m",	"110m.hurdle", "Discus", "Pole.vault", "Javeline", "1500m"]
    #print(data_file.head())
    
    #send data file to dacthlon get result method to calculate total scores of each athelits and add the total scores in scores column
    get_scores = decathlon_get_results.scores(data_file)
    
    ## create and save final json file on the server
    json_file_name = '/DECATHLONTEST/static/files/'+username+'-'+filename.split('.csv')[0]+'.json'
    with open(json_file_name, 'w') as f:
        json.dump(get_scores, f)

    ### send data to UI for presentation
    final_data_presentation = {'username': username,'data': get_scores, 'filepath': json_file_name}
    db.session.commit()
    db.session.close()
    
    return render_template("dataproc.html", fdp = final_data_presentation)

## download file
@app.route('/download/<path:username>')
def downloadFile (username):
    user_data = User.query.filter_by(username=username).first()
    filename = user_data.file
    json_file_name = '/DECATHLONTEST/static/files/'+username+'-'+filename.split('.csv')[0]+'.json'
    
    return send_file(json_file_name, as_attachment=True)

if (__name__ == "__main__"):
     db.create_all()
     port = int(os.environ.get('PORT', 5000))
     app.run(host = '0.0.0.0', port = port)