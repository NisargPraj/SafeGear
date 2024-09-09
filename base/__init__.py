import warnings
from flask import Flask, Response, jsonify
from flask_sqlalchemy import SQLAlchemy


warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = 'qazwsxedcrfvtgbyhnujmikolp123456789'

app.config['SQLALCHEMY_ECHO'] = True

# Configure MySQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/safegear?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Path configuration
app.config['UPLOAD_FOLDER'] = r'static\upload'
app.config['OUTPUT_FOLDER'] = r'static\output'

# Database instance
db = SQLAlchemy(app)

from base.com import controller
