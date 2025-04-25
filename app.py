from flask import Flask
from routes.summarize_route import summarize_bp

app = Flask(__name__)
app.register_blueprint(summarize_bp)

if __name__ == '__main__':
    app.run(port=5000, debug=True)

