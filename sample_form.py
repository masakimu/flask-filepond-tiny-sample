from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm as Form
from flask_wtf.csrf import CSRFProtect
from wtforms import HiddenField, TextField, SubmitField
from wtforms.validators import Required
from werkzeug import secure_filename
import os
import json


app = Flask(__name__)
app.secret_key = 'MRS'

csrf=CSRFProtect()
csrf.init_app(app)

class SampleForm(Form):
    dammy_hidden=HiddenField('dammy_hidden') # required to print csrf token into hidden field by FlaskForm
    name=TextField('Name', validators=[Required()]) # just a dammy
    submit= SubmitField('Submit')

def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')

# uploaded data processing server for filepond javascript
@app.route('/upload', methods=['POST'])
def upload():
    form = SampleForm()
    
    upload_dir = 'upload_files'
    fn=""
    file_names=[]
    for i,f in enumerate(request.files):
        file = request.files.get(f)
        fn = secure_filename(file.filename)
        file_names.append(fn)
        print('filename: ', fn)
        try:
            file.save(os.path.join(upload_dir,  fn))
        except:
            print('save fail: ' + os.path.join(upload_dir,  fn))
    
    return json.dumps({'filename':[f for f in file_names]})

# front end of this sample web application
@app.route('/', methods=['POST','GET'])
def home():
    form = SampleForm()
    if form.validate_on_submit():
        upload_dir = 'upload_files'
        if 'selected_file' in request.form:
            print('Uploaded File Name: ', request.form['selected_file'])
        else:
            flash('No Uploaded File')
            print('No Uploaded File')
        print('Inputed String in Text Form: ' + form.name.data)
    else:
        flash_errors(form)
        print('no operation hogehoge')
        
    return render_template('sample_form.html', form=form)
#    return render_template('sample_form_jquery.html', form=form)
        
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)
