from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
# Set up database URI and configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "users.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    company_name = db.Column(db.String(120))
    hr_gender = db.Column(db.String(10))
    post = db.Column(db.String(50))
    country = db.Column(db.String(50))
    email_sent_count = db.Column(db.Integer, default=0)  # Track how many emails have been sent to the user

# Get Gmail credentials from environment variables for security
GMAIL_USER = 'ayusharya.personal@gmail.com'  # Set GMAIL_USER in your environment variables
APP_PASSWORD = 'uclx fhnh plxf jgjh'  # Set APP_PASSWORD in your environment variables

# Email sending function
def send_email(gmail_user, app_password, to_email, company_name, hr_name, specific_role):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Email content
    subject = " Interest in {} Opportunities at {}".format(specific_role, company_name)
    message_body = f"""
          <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title> Interest in AI/ML Opportunities at {company_name}")</title>
            <style>
                /* General Reset */
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f5f5f5;
                    color: #333;
                    padding: 20px;
                }}
                .email-container {{
                    max-width: 650px;
                    margin: auto;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                    overflow: hidden;
                    border: 1px solid #e0e0e0;
                }}

                /* Header */
                .header {{
                    background:  linear-gradient(135deg, #9b59b6, #e84393);
                    color: #ffffff;
                    padding: 30px;
                    text-align: center;
                    background-image: url('https://ayusharya.me/assets/header.png');
                   background-size: cover;
                   background-repeat: no-repeat;
                   background-position: center;
                   padding: 30px;
                   text-align: center;

                }}
                .header h1 {{
                    font-size: 24px;
                    font-weight: 700;
                    margin-bottom: 5px;
                }}
                .header p {{
                    font-size: 16px;
                    margin-top: 5px;
                }}
                /* Content */
                .content {{
                    padding: 25px 30px;
                    font-size: 16px;
                    line-height: 1.6;
                    color: #555;
                }}
                .content p {{
                    margin: 15px 0;
                }}
                .highlight {{
                    color: #9b59b6;
                    font-weight: 600;
                }}
                .cta-button {{
                    display: inline-block;
                    padding: 12px 24px;
                    margin-top: 20px;
                    background-color: #3498db; /* Solid background for desktop */
                    color: #ffffff;
                    text-decoration: none;
                    font-weight: 600;
                    border-radius: 5px;
                    transition: background-color 0.3s ease;
                }}
                .cta-button:hover {{
                    background-color: #2980b9; /* Darker shade on hover for desktop */
                }}

                /* Responsive styles */
                @media (max-width: 600px) {{
                    .cta-button {{
                        background-color: #e84393; /* Different color for mobile */
                        padding: 10px 18px;
                        font-size: 15px;
                        }}
                    .cta-button:hover {{
                        background-color: #d6336c; /* Darker shade on hover for mobile */}}
                        }}


                /* Footer */
                .footer {{
                    background-color: #e7e7e7;
                    padding: 20px;
                    text-align: center;
                    font-size: 14px;
                    color: #333;
                    border-top: 1px solid #e0e0e0;
                }}
                .footer a {{
                    color: black;
                    text-decoration: none;
                    font-weight: 500;
                    margin: 0 10px;
                }}
                .footer .icon {{
                    margin: 0 5px;
                    vertical-align: middle;
                }}
                .footer img {{
                    width: 20px; /* Size of the icons */
                    height: 20px;
                    vertical-align: middle;
                    margin-right: 5px;
                }}

                /* Media Queries for Mobile */
                @media (max-width: 600px) {{
                    .content {{
                        padding: 20px;
                    }}
                    .header h1 {{
                        font-size: 20px;
                    }}
                    .cta-button {{
                        padding: 10px 18px;
                        font-size: 15px;
                    }}
                    .footer {{
                        padding: 15px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <!-- Header Section -->
                <div class="header">
                    <h1> Application for {specific_role} Role at {company_name}</h1>
                    <p>An Enthusiastic Candidate Ready to Make an Impact</p>
                </div>

                <!-- Content Section -->
             <div class="content">
            <p>Dear <span class="highlight">{hr_name}</span>,</p>

             <p>I hope this email finds you well. My name is Ayush Arya, a final-year B.Tech student specializing in Computer Science and Engineering with a focus on Machine Learning. I am reaching out to express my strong interest in the <span class="highlight"> {specific_role}</span> position at <span class="highlight">{company_name}</span>.</p>

                <p>Having developed projects like a Image Classification  system using Open CV,CNN and a conversational AI tool, I have honed my technical expertise in full-stack development, cloud computing, and problem-solving. My recent internships at Astroverse and IIT BHU have further strengthened my ability to contribute effectively in collaborative and innovative environments.</p>

                <p>I am particularly impressed by your organization's</span> commitment to focus on fostering innovation and delivering impactful solutions that enhance user experiences and drive technological progress, and I would love the opportunity to bring my skills and enthusiasm to your team.</p>

                <p>I have attached my resume for your reference. I would greatly appreciate the chance to discuss how I can contribute to <span class="highlight"> {company_name}'s </span>goals. Please let me know if a convenient time is available for a conversation.</p>

                <p>Thank you for considering my application. I look forward to the possibility of contributing to your team.</p>
        <p>Warm regards,<br>
        Ayush Arya<br>
        </div>




                <!-- Footer Section -->
                <div class="footer">
                    <p>
                        <a href="https://ayusharya.me">
                            <img src="https://img.icons8.com/ios-filled/50/domain.png" class="icon" alt="Website">Website
                        </a> |
                        <a href="https://github.com/Ayush01arya">
                            <img src="https://img.icons8.com/ios-filled/50/000000/github.png" class="icon" alt="Phone">Ayush01arya
                        </a> |
                        <a href="https://linkedin.com/in/ayusharya25">
                            <img src="https://img.icons8.com/ios-filled/50/000000/linkedin.png" class="icon" alt="LinkedIn">LinkedIn
                        </a> |
                        <a href="https://ayusharya.me/assets/0Ayush_Arya_Resume.pdf">
                            <img src="https://img.icons8.com/ios-filled/50/resume.png" class="icon" alt="Resume">Resume
                        </a> 


                    </p>
                </div>
            </div>
        </body>
        </html>"""
    msg = MIMEMultipart()
    msg["From"] = gmail_user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message_body, "html"))

    try:
        # Send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(gmail_user, app_password)
        server.sendmail(gmail_user, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

# Route to get all users
@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        user_list = [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'company_name': user.company_name,
                'hr_gender': user.hr_gender,
                'post': user.post,
                'country': user.country,
                'email_sent_count': user.email_sent_count  # Correct column name here
            }
            for user in users
        ]
        return jsonify(user_list)
    except Exception as e:
        return jsonify({"message": f"Failed to retrieve users: {e}"}), 500

# Route to add a new user
@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if not all(data.get(field) for field in ['username', 'email', 'company_name', 'hr_gender', 'post', 'country']):
        return jsonify({"message": "Missing required fields!"}), 400

    try:
        new_user = User(
            username=data['username'],
            email=data['email'],
            company_name=data['company_name'],
            hr_gender=data['hr_gender'],
            post=data['post'],
            country=data['country']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "New user added successfully!"}), 201
    except Exception as e:
        return jsonify({"message": f"Failed to add user: {e}"}), 500

# Route to send an email (only POST method now)
@app.route('/api/send_email/<int:user_id>', methods=['POST'])
def send_email_route(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found!"}), 404

    data = request.get_json()
    specific_role = data.get('specific_role')
    if not specific_role:
        return jsonify({"message": "Missing specific role!"}), 400

    if send_email(
        GMAIL_USER, APP_PASSWORD, user.email, user.company_name,
        user.username, specific_role
    ):
        user.email_sent_count += 1  # Increment the email sent count
        db.session.commit()
        return jsonify({"message": f"Email sent successfully to {user.email}! User has sent {user.email_sent_count} emails."})
    else:
        return jsonify({"message": "Failed to send email!"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Make sure to create the database tables if they don't exist
    app.run(debug=True)
