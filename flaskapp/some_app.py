import net as neuronet
import os
import json
from io import BytesIO
from PIL import Image
import base64
from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
# модули валидации полей формы
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from flask import request
from flask import Response
import lxml.etree as ET


print("Hello world")
app = Flask(__name__)
bootstrap = Bootstrap(app)

SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
# используем капчу и полученные секретные ключи с сайта Google
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lf98BEnAAAAAE9oIv_oMeaKVagAqVzp00mv2jxB'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lf98BEnAAAAACFE6XeKwL3DOYiytp2oud8V_Ncp'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}


class NetForm(FlaskForm):
    openid = StringField('openid', validators=[DataRequired()])
    upload = FileField('Load image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    recaptcha = RecaptchaField()
    submit = SubmitField('send')


@app.route("/")
def hello():
    return " <html><head></head> <body> Hello World! </body></html>"


@app.route("/data_to")
def data_to():
    some_pars = {'user': 'Ivan', 'color': 'red'}

    some_str = 'Hello my dear friends!'
    some_value = 10
    return render_template('simple.html', some_str=some_str,
                           some_value=some_value, some_pars=some_pars)


@app.route("/net", methods=['GET', 'POST'])
def net():
    form = NetForm()
    filename = None
    neurodic = {}

    if form.validate_on_submit():
        filename = os.path.join(
            './static', secure_filename(form.upload.data.filename))
        fcount, fimage = neuronet.read_image_files(10, './static')

        decode = neuronet.getresult(fimage)

        for elem in decode:
            neurodic[elem[0][1]] = elem[0][2]

        form.upload.data.save(filename)

    return render_template('net.html', form=form, image_name=filename, neurodic=neurodic)


@app.route("/apinet", methods=['GET', 'POST'])
def apinet():
    neurodic = {}
    if request.mimetype == 'application/json':
        data = request.get_json()
        filebytes = data['imagebin'].encode('utf-8')
        cfile = base64.b64decode(filebytes)

        img = Image.open(BytesIO(cfile))
        decode = neuronet.getresult([img])
        neurodic = {}

        for elem in decode:
            neurodic[elem[0][1]] = str(elem[0][2])
            print(elem)

    ret = json.dumps(neurodic)
    resp = Response(response=ret,
                    status=200,
                    mimetype="application/json")

    return resp


@app.route("/apixml", methods=['GET', 'POST'])
def apixml():
    dom = ET.parse("./static/xml/file.xml")
    xslt = ET.parse("./static/xml/file.xslt")
    transform = ET.XSLT(xslt)
    newhtml = transform(dom)
    strfile = ET.tostring(newhtml)
    return strfile


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
