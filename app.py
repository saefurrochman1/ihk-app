from flask import Flask
from routes.data_routes import data_bp
from routes.forecast_routes import forecast_bp
from routes.grafik_routes import grafik_bp

app = Flask(__name__)

# Register blueprint
app.register_blueprint(data_bp)
app.register_blueprint(forecast_bp)
app.register_blueprint(grafik_bp)

# Default redirect ke /data
@app.route("/")
def index():
    from flask import redirect, url_for
    return redirect(url_for("data_page.index"))

if __name__ == "__main__":
    app.run(debug=True)
