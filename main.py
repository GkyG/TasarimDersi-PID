from flask import Flask, render_template, request, send_file
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__)

# Ana sayfa ve PID parametreleri alımı
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Kullanıcıdan gelen PID parametrelerini al
        Kp = float(request.form['Kp'])
        Ki = float(request.form['Ki'])
        Kd = float(request.form['Kd'])
        Ka = float(request.form['Ka'])

        # G(s) pay ve payda kısmını al
        G_num = [float(x) for x in request.form['G_num'].split()]
        G_den = [float(x) for x in request.form['G_den'].split()]

        # H(s) pay ve payda kısmını al
        H_num = [float(x) for x in request.form['H_num'].split()]
        H_den = [float(x) for x in request.form['H_den'].split()]

        # Zaman aralığı
        t = np.linspace(0, 5, 500)

        # Sistem Transfer Fonksiyonları
        G = ctrl.TransferFunction(G_num, G_den)  # G(s) = Pay / Payda
        H = ctrl.TransferFunction(H_num, H_den)  # H(s) = Pay / Payda

        # PID Denetleyicisi Transfer Fonksiyonu
        C = ctrl.TransferFunction([Ka, Kd, Kp, Ki], [1, 0])

        # Kapalı Çevrim Sistemi
        Gk = ctrl.feedback(C * G, H)

        # Step Yanıtı
        t, y = ctrl.step_response(Gk, t)

        # Grafik oluşturma
        fig, ax = plt.subplots()
        ax.plot(t, y)
        ax.set_title('PID Basamak Cevabı')
        ax.set_xlabel('Zaman (s)')
        ax.set_ylabel('Genlik')
        ax.grid(True)

        # Grafik için buffer oluşturma
        buf = io.BytesIO()
        canvas = FigureCanvas(fig)
        canvas.print_png(buf)
        buf.seek(0)

        return send_file(buf, mimetype='image/png')

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
