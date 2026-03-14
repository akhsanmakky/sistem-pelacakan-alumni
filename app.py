from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-for-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class Alumni(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    program_studi = db.Column(db.String(100), nullable=False)
    tahun_lulus = db.Column(db.Integer, nullable=False)
    kata_kunci = db.Column(db.String(200), nullable=False)

class HasilPelacakan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alumni_id = db.Column(db.Integer, db.ForeignKey('alumni.id'), nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    jabatan = db.Column(db.String(100), nullable=False)
    perusahaan = db.Column(db.String(100), nullable=False)
    lokasi = db.Column(db.String(100), nullable=False)
    sumber = db.Column(db.String(50), nullable=False)
    tanggal_pelacakan = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        admin = Admin.query.filter_by(email=email).first()
        if admin and check_password_hash(admin.password_hash, password):
            session['admin_id'] = admin.id
            flash('Login berhasil!', 'success')
            return redirect(url_for('dashboard'))
        flash('Email atau password salah!', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin_id', None)
    flash('Logout berhasil!', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    
    total_alumni = Alumni.query.count()
    total_pelacakan = HasilPelacakan.query.count()
    total_admin = Admin.query.count()
    recent_alumni = Alumni.query.order_by(Alumni.id.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                          total_alumni=total_alumni, 
                          total_pelacakan=total_pelacakan, 
                          total_admin=total_admin,
                          recent_alumni=recent_alumni)

@app.route('/alumni')
def alumni():
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    
    search = request.args.get('search')
    alumni_list = Alumni.query
    if search:
        alumni_list = alumni_list.filter(Alumni.nama.contains(search))
    alumni_list = alumni_list.all()
    
    return render_template('alumni.html', alumni=alumni_list)

@app.route('/tambah_alumni', methods=['GET', 'POST'])
def tambah_alumni():
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nama = request.form.get('nama', '').strip()
        program_studi = request.form.get('program_studi', '').strip()
        kata_kunci = request.form.get('kata_kunci', '').strip()
        tahun_lulus_str = request.form.get('tahun_lulus', '')
        
        # Validation
        if not all([nama, program_studi, kata_kunci, tahun_lulus_str]):
            flash('Semua field harus diisi!', 'danger')
            return render_template('tambah_alumni.html', current_year=datetime.now().year)
        
        try:
            tahun_lulus = int(tahun_lulus_str)
            if tahun_lulus < 1900 or tahun_lulus > datetime.now().year + 1:
                raise ValueError("Tahun lulus tidak valid")
        except ValueError:
            flash('Tahun lulus harus berupa angka tahun yang valid (1900-sekarang)!', 'danger')
            return render_template('tambah_alumni.html', current_year=datetime.now().year)
        
        new_alumni = Alumni(
            nama=nama,
            program_studi=program_studi,
            tahun_lulus=tahun_lulus,
            kata_kunci=kata_kunci
        )
        db.session.add(new_alumni)
        db.session.commit()
        flash('Alumni berhasil ditambahkan!', 'success')
        return redirect(url_for('alumni'))
    else:
        db.session.rollback()
        flash('Error menambah alumni: Database error', 'danger')
        return render_template('tambah_alumni.html', current_year=datetime.now().year)
    
    return render_template('tambah_alumni.html', current_year=datetime.now().year)

@app.route('/edit_alumni/<int:id>', methods=['GET', 'POST'])
def edit_alumni(id):
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    
    alumni = Alumni.query.get_or_404(id)
    
    if request.method == 'POST':
        alumni.nama = request.form.get('nama', '').strip()
        alumni.program_studi = request.form.get('program_studi', '').strip()
        alumni.kata_kunci = request.form.get('kata_kunci', '').strip()
        tahun_lulus_str = request.form.get('tahun_lulus', '')
        
        # Validation
        if not all([alumni.nama, alumni.program_studi, alumni.kata_kunci, tahun_lulus_str]):
            flash('Semua field harus diisi!', 'danger')
            return render_template('edit_alumni.html', alumni=alumni, current_year=datetime.now().year)
        
        try:
            tahun_lulus = int(tahun_lulus_str)
            if tahun_lulus < 1900 or tahun_lulus > datetime.now().year + 1:
                raise ValueError("Tahun lulus tidak valid")
            alumni.tahun_lulus = tahun_lulus
        except ValueError:
            flash('Tahun lulus harus berupa angka tahun yang valid (1900-sekarang)!', 'danger')
            return render_template('edit_alumni.html', alumni=alumni, current_year=datetime.now().year)
        
        db.session.commit()
        flash('Data alumni berhasil diupdate!', 'success')
        return redirect(url_for('alumni'))
    else:
        db.session.rollback()
        flash('Error mengupdate alumni: Database error', 'danger')
        return render_template('edit_alumni.html', alumni=alumni, current_year=datetime.now().year)
    
    return render_template('edit_alumni.html', alumni=alumni, current_year=datetime.now().year)

@app.route('/hapus_alumni/<int:id>')
def hapus_alumni(id):
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    
    alumni = Alumni.query.get_or_404(id)
    db.session.delete(alumni)
    db.session.commit()
    flash('Alumni berhasil dihapus!', 'success')
    return redirect(url_for('alumni'))

@app.route('/lacak_alumni/<int:id>')
def lacak_alumni(id):
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    
    alumni = Alumni.query.get_or_404(id)
    
    # Simulasi hasil pelacakan
    hasil = {
        'nama': alumni.nama,
        'jabatan': 'Software Engineer',
        'perusahaan': 'Gojek',
        'lokasi': 'Jakarta',
        'sumber': 'LinkedIn'
    }
    
    return render_template('hasil_pelacakan.html', alumni=alumni, hasil=hasil, alumni_id=id)

@app.route('/simpan_pelacakan/<int:alumni_id>')
def simpan_pelacakan(alumni_id):
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    
    alumni = Alumni.query.get_or_404(alumni_id)
    
    # Simulasi data hasil pelacakan
    new_hasil = HasilPelacakan(
        alumni_id=alumni_id,
        nama=alumni.nama,
        jabatan='Software Engineer',
        perusahaan='Gojek',
        lokasi='Jakarta',
        sumber='LinkedIn'
    )
    db.session.add(new_hasil)
    db.session.commit()
    flash('Hasil pelacakan berhasil disimpan!', 'success')
    return redirect(url_for('riwayat_pelacakan'))

@app.route('/riwayat_pelacakan')
def riwayat_pelacakan():
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    
    hasil_list = db.session.query(HasilPelacakan, Alumni).join(Alumni).all()
    return render_template('riwayat_pelacakan.html', hasil=hasil_list)

if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()
            # Buat admin default jika belum ada
            if not Admin.query.filter_by(email='admin@kampus.ac.id').first():
                admin = Admin(
                    email='admin@kampus.ac.id',
                    password_hash=generate_password_hash('admin123')
                )
                db.session.add(admin)
                db.session.commit()
                print("✓ Admin default dibuat: email=admin@kampus.ac.id, password=admin123")
            else:
                print("✓ Admin default sudah ada")
            print("✓ Database tables created successfully")
    except Exception as e:
        print(f"✗ Database initialization error: {e}")
    
    app.run(debug=True)
