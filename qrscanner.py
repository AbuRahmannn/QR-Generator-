from flask import Flask, render_template, request, send_file, jsonify
import qrcode
import qrcode.image.svg as svg
from PIL import Image
import io
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/preview', methods=['POST'])
def preview():
    try:
        link = request.form.get('link')
        fill_color = request.form.get('fill_color', '#000000')
        back_color = request.form.get('back_color', '#ffffff')

        if not link:
            return jsonify({"error": "Please enter a valid link"}), 400

        qr = qrcode.QRCode(
            version=None,
            box_size=10,
            border=4
        )

        qr.add_data(link)
        qr.make(fit=True)

        img = qr.make_image(
            fill_color=fill_color,
            back_color=back_color
        ).convert("RGB")

        # Handle Logo Upload Safely
        logo_file = request.files.get('logo')
        if logo_file and logo_file.filename != '':
            logo = Image.open(logo_file)
            logo = logo.resize((80, 80))
            pos = (
                (img.size[0] - 80) // 2,
                (img.size[1] - 80) // 2
            )
            img.paste(logo, pos)

        img_io = io.BytesIO()
        img.save(img_io, format="PNG")
        img_io.seek(0)

        encoded = base64.b64encode(img_io.getvalue()).decode()

        return jsonify({"image": encoded})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/download_png', methods=['POST'])
def download_png():
    link = request.form.get('link')

    if not link:
        return "Invalid Link", 400

    qr = qrcode.make(link)
    img_io = io.BytesIO()
    qr.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(
        img_io,
        mimetype="image/png",
        as_attachment=True,
        download_name="qr_code.png"
    )


@app.route('/download_svg', methods=['POST'])
def download_svg():
    link = request.form.get('link')

    if not link:
        return "Invalid Link", 400

    factory = svg.SvgImage
    img = qrcode.make(link, image_factory=factory)

    img_io = io.BytesIO()
    img.save(img_io)
    img_io.seek(0)

    return send_file(
        img_io,
        mimetype="image/svg+xml",
        as_attachment=True,
        download_name="qr_code.svg"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

