from functools import wraps
import os

from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from sqlalchemy import or_
from werkzeug.utils import secure_filename

from database import db
from models import User


# Charger les variables du fichier .env
load_dotenv()

app = Flask(__name__)

# ==========================
# Security configuration
# ==========================
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# ==========================
# Database configuration
# ==========================
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:///users.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# ==========================
# Upload configuration
# ==========================
UPLOAD_IMAGE = os.path.join("static", "uploads", "images")
UPLOAD_VIDEO = os.path.join("static", "uploads", "videos")

os.makedirs(UPLOAD_IMAGE, exist_ok=True)
os.makedirs(UPLOAD_VIDEO, exist_ok=True)

with app.app_context():
    db.create_all()


# ==========================
# Login protection
# ==========================
def login_required(view_function):
    @wraps(view_function)
    def protected_view(*args, **kwargs):
        if not session.get("admin_logged_in"):
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login"))

        return view_function(*args, **kwargs)

    return protected_view


# ==========================
# Home page
# ==========================
@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# Admin login
# ==========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("admin_logged_in"):
        return redirect(url_for("users"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            session["admin_username"] = username

            flash("Login successful.", "success")
            return redirect(url_for("users"))

        flash("Invalid username or password.", "danger")

    return render_template("login.html")


# ==========================
# Admin logout
# ==========================
@app.route("/logout")
def logout():
    session.clear()

    flash("You have been logged out.", "info")

    return redirect(url_for("login"))


# ==========================
# Register user
# ==========================
@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("fullname", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()

    if not name or not email or not phone:
        flash("Name, email and phone are required.", "danger")
        return redirect(url_for("home"))

    photo = request.files.get("photo")
    video = request.files.get("video")

    photo_name = ""
    video_name = ""

    if photo and photo.filename:
        photo_name = secure_filename(photo.filename)

        photo.save(
            os.path.join(
                UPLOAD_IMAGE,
                photo_name,
            )
        )

    if video and video.filename:
        video_name = secure_filename(video.filename)

        video.save(
            os.path.join(
                UPLOAD_VIDEO,
                video_name,
            )
        )

    user = User(
        name=name,
        email=email,
        phone=phone,
        photo=photo_name,
        video=video_name,
    )

    db.session.add(user)
    db.session.commit()

    flash("User registered successfully.", "success")

    return redirect(url_for("users"))


# ==========================
# Display and search users
# ==========================
@app.route("/users")
@login_required
def users():
    search = request.args.get("search", "").strip()

    if search:
        all_users = User.query.filter(
            or_(
                User.name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
                User.phone.ilike(f"%{search}%"),
            )
        ).all()
    else:
        all_users = User.query.order_by(User.id.desc()).all()

    return render_template(
        "users.html",
        users=all_users,
        search=search,
    )


# ==========================
# Edit user
# ==========================
@app.route("/edit/<int:id>")
@login_required
def edit(id):
    user = User.query.get_or_404(id)

    return render_template(
        "edit.html",
        user=user,
    )


# ==========================
# Update user
# ==========================
@app.route("/update/<int:id>", methods=["POST"])
@login_required
def update(id):
    user = User.query.get_or_404(id)

    user.name = request.form.get("fullname", "").strip()
    user.email = request.form.get("email", "").strip()
    user.phone = request.form.get("phone", "").strip()

    db.session.commit()

    flash("User updated successfully.", "success")

    return redirect(url_for("users"))


# ==========================
# Delete user
# ==========================
@app.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    user = User.query.get_or_404(id)

    if user.photo:
        photo_path = os.path.join(
            UPLOAD_IMAGE,
            user.photo,
        )

        if os.path.exists(photo_path):
            os.remove(photo_path)

    if user.video:
        video_path = os.path.join(
            UPLOAD_VIDEO,
            user.video,
        )

        if os.path.exists(video_path):
            os.remove(video_path)

    db.session.delete(user)
    db.session.commit()

    flash("User deleted successfully.", "success")

    return redirect(url_for("users"))


# ==========================
# Run application
# ==========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )