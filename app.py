from flask import Flask, request, render_template
from icrawler.builtin import GoogleImageCrawler
import os
import shutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

# Function to download images and ensure unique numbering
def download_images(keyword, num_images):
    output_dir = f'./downloads/{keyword}'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Initialize GoogleImageCrawler
    google_crawler = GoogleImageCrawler(storage={'root_dir': output_dir})
    
    # Crawl for the images
    google_crawler.crawl(
        keyword=keyword,
        max_num=num_images
    )

    # Rename files to ensure unique numbering
    for index, filename in enumerate(os.listdir(output_dir)):
        if filename.endswith('.jpg'):  # You can adjust this based on the file type
            new_filename = f"{keyword}_{index + 1}.jpg"  # Start numbering from 1
            os.rename(os.path.join(output_dir, filename), os.path.join(output_dir, new_filename))

    # Zip the folder after renaming
    zip_file_path = shutil.make_archive(output_dir, 'zip', output_dir)
    
    # Return the absolute path of the zip file
    return os.path.abspath(zip_file_path)

# Function to send an email with the zip file attached
def send_email(recipient_email, keyword, zip_file_path):
    sender_email = "tjain1_be@thapar.edu"  # Replace with your email
    sender_password = "Tanisha@123"  # Replace with your email password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = f"Download Images for {keyword}"

    body = f"Please find the images for '{keyword}' attached."
    msg.attach(MIMEText(body, 'plain'))

    # Attach the zip file
    with open(zip_file_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(zip_file_path)}",
        )
        msg.attach(part)

    # Send the email via SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, recipient_email, text)
    server.quit()

@app.route('/')
def home():
    return render_template('front_end.html')

# Route to trigger image download and zip file creation
@app.route('/download_images', methods=['POST'])
def download_images_route():
    # Extract form data from the request
    keyword = request.form['keyword']
    num_images = int(request.form['num_images'])
    email = request.form['email']

    # Download images and get the path to the zip file
    zip_file_path = download_images(keyword, num_images)

    # Send email with the zip file attached
    send_email(email, keyword, zip_file_path)

    return f"Images for '{keyword}' downloaded and sent to {email} as a zip file."

if __name__ == '__main__':
    app.run(debug=True)
