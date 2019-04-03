from flask_wtf import FlaskForm as Form
from wtforms import FormField, FieldList, IntegerField, Form as nonCSRFForm, SelectMultipleField, validators, SubmitField, HiddenField, TextField
from wtforms.widgets import ListWidget, TableWidget, CheckboxInput
from wtforms.validators import (Required, InputRequired)
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug import secure_filename
from flask import Flask, render_template, flash, request
import os
import json

from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = 'MRS'

csrf=CSRFProtect()
csrf.init_app(app)

class SampleForm(Form):
    dammy_hidden=HiddenField('dammy_hidden')
    #file_upload=FileField('sample File')
    name=TextField('Name', validators=[Required()])
    submit= SubmitField('Submit')

def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')
@app.route('/upload', methods=['POST'])
def upload():
    form = SampleForm()
    
    upload_dir = 'upload_files'
    fn=""
    ## with open('hoge.csv', 'w') as f:
    ##     csvwriter = csv.writer(f, lineterminator='\n')
    file_names=[]
    for i,f in enumerate(request.files):
        file = request.files.get(f)
        fn = secure_filename(file.filename)
        file_names.append(fn)
        print('filename: ', fn)
        #            csvwriter.writerow([str(i), fn])
        try:
            file.save(os.path.join(upload_dir,  fn))
        except:
            print('save fail: ' + os.path.join(upload_dir,  fn))
    
    return json.dumps({'filename':[f for f in file_names]})


@app.route('/', methods=['POST','GET'])
def home():
    form = SampleForm()
    fn = ""
    if form.validate_on_submit():
        upload_dir = 'upload_files'
        if 'selected_file' in request.form:
            print(request.form['selected_file'])
        else:
            flash('Upload Data File')
                    
    else:
        flash_errors(form)
        print('no operation hogehoge')
        
    return render_template('sample_form.html', form=form, fn=fn)
        
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)
    
