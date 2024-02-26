from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
import openpyxl

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///Std.db"
db=SQLAlchemy(app)

class Std(db.Model):
    id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    name=db.Column(db.String(100), nullable=False)
    age=db.Column(db.Integer(), nullable=False)


@app.route('/fileparser',methods=['POST'])
def fileparser():
    data=request.files['file']
    workbook=openpyxl.load_workbook(data)

    print(workbook)
    sheet=workbook.active

    for row in sheet.iter_rows(min_row=2, values_only=True):
        print(row)
        name,age=row
        data2=Std(name=name,age=age)
        db.session.add(data2)

        db.session.commit()
    

    return 'msg: file uploaded Successfully '


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # db.drop_all()

    app.run(debug=True, port=8000)
