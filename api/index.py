from flask import Flask

app = Flask(__name__)

# 函式的裝飾器 (Decorator)：函釋為基礎提供的附加功能
@app.route("/") 
def home():
    return "Hello Flask"

@app.route("/aaa")
def test():
    return "Hello route is aaa"

@app.route("/train")
def test():
    return "train"
    
if __name__ == "__main__":
    app.run()