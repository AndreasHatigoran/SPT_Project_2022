from flask import Flask, flash, redirect, render_template, request, send_file, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from io import BytesIO


app = Flask(__name__)
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spt.db'
db = SQLAlchemy(app)
db_connect = create_engine('sqlite:///spt.db')


class mytask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)
    topik = db.Column(db.String)
    tanggal = db.Column(db.String)
    deskripsi = db.Column(db.Text)
    
@app.route('/')
def mytask_index():
    conn = db_connect.connect()
    query = conn.execute("select * from mytask")

    return render_template('mytaskIndex.html', submission_data = query.cursor.fetchall())

@app.route('/submit')
def index():
    return render_template('index.html')

@app.route('/upload', methods= ['POST'])
def upload():
    file = request.files['inputFile']
    submission_topik = request.form['topik']
    submission_tanggal = request.form['tanggal']
    submission_deskripsi = request.form['deskripsi']
    
    newFile = mytask(name=file.filename, data=file.read(), topik=submission_topik, tanggal=submission_tanggal, deskripsi=submission_deskripsi)
    db.session.add(newFile)
    db.session.commit()
    return 'File ' +  file.filename +  ' Berhasil disimpan. ' + ' <a href="/">Silahkan klik untuk kembali</a>'

@app.route('/delete/<int:id>')
def delete(id):
    record= mytask.query.get_or_404(id)
   
    try:
        db.session.delete(record)
        db.session.commit()
        submission_data = mytask.query.filter_by(id)
        flash("Sukses Didelete")
        return redirect(url_for('mytask_index'),row = submission_data)
    
    except:
        flash("Tidak bisa di delete")
        return render_template('mytaskIndex.html')
    

@app.route('/download/<int:data_id>')
def download(data_id):
    file_data = mytask.query.filter_by(id=data_id).first()
    return send_file(BytesIO(file_data.data), attachment_filename=file_data.name, as_attachment=True)

if __name__ == '__main__':
   app.run(debug=True)