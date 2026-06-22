from flask import Flask, render_template, request, jsonify, send_from_directory
from datetime import datetime
import os
import csv
import uuid
import qrcode
import io
import json
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch, mm

app = Flask(__name__, static_folder='static', template_folder='templates')


# --- Questions copied from original script ---
questions1 = [
    ("At a party do you", "interact with many, including strangers", "interact with a few, known  to you"),
    ("At parties do you", "Stay late, with increasing energy", "Leave early, with decreasing energy"),
    ("In your social groups do you", "Keep abreast of others happenings", "Get behind on the news"),
    ("Are you usually rather", "Quick to agree to a time", "Reluctant to agree to a time"),
    ("In company do you", "Start conversations", "Wait to be approached"),
    ("Does new interaction with others", "Stimulate and energize you", "Tax your reserves"),
    ("Do you prefer", "Many friends with brief contact", "A few friends with longer contact"),
    ("Do you", "Speak easily and at length with strangers", "Find little to say to strangers"),
    ("When the phone rings do you", "Quickly get to it first", "Hope someone else will answer"),
    ("At networking functions you are", "Easy to approach", "A little reserved")
]

questions2 = [
    ("Are you more", "Realistic", "Philosophically inclined "),
    ("Are you a more", "Sensible person", "Reflective person "),
    ("Are you usually more interested in", "Specifics", "Concepts "),
    ("Facts", "Speak for themselves", "Usually require interpretation "),
    ("Traditional common sense is", "Usually trustworthy", "often misleading "),
    ("Are you more frequently", "A practical sort of person", "An abstract sort of person "),
    ("Are you more drawn to", "Substantial information", "Credible assumptions "),
    ("Are you usually more interested in the", "Particular instance", "General case "),
    ("Do you prize more in yourself a", "Good sense of reality", "Good imagination "),
    ("Do you have more fun with", "Hands-on experience", "Blue-sky fantasy "),
]

questions3 = [
    ("Are you usually more", "Fair minded", "Kind hearted"),
    ("Is it more natural to be", "Fair to others", "Nice to others"),
    ("Are you more naturally", "Impartial", "Compassionate"),
    ("Are you inclined to be more", "Cool headed", "Warm hearted"),
    ("Are you usually more", "Tough minded", "Tender hearted"),
    ("Which is more satisfying", "To discuss an issue throughly", "To arrive at agreement on an issue"),
    ("Are you more comfortable when you are", "Objective", "Personal"),
    ("Are you typically more a person of", "Clear reason", "Strong feeling"),
    ("In judging are you usually more", "Neutral", "Charitable"),
    ("Are you usually more", "Unbiased", "compassionate"),
]

questions4 = [
    ("Do you tend to be more", "Dispassionate", "Sympathetic"),
    ("In first approaching others are you more", "Impersonal and detached", "Personal and engaging"),
    ("In judging are you more likely to be", "Impersonal", "Sentimental"),
    ("Would you rather be", "More just than merciful", "More merciful than just"),
    ("Are you usually more", "Tough minded", "Tender hearted"),
    ("Which rules you more", "Your head", "Your heart"),
    ("Do you value in yourself more that you are", "Unwavering", "Devoted"),
    ("Are you inclined more to be", "Fair-minded", "Sympathetic"),
    ("Are you convinced by?", "Evidence", "Someone you trust"),
    ("Are you typically more", "Just than lenient", "Lenient than just"),
]

questions5 = [
    ("Do you prefer to work", "To deadlines", "Just whenever"),
    ("Are you usually more", "Punctual", "Leisurely"),
    ("Do you usually", "Settle things", "Keep options open"),
    ("Are you more comfortable", "Setting a schedule", "Putting things off"),
    ("Are you more prone to keep things", "well organized", "Open-ended"),
    ("Are you more comfortable with work", "Contracted", "Done on a casual basis"),
    ("Are you more comfortable with", "Final statements", "Tentative statements"),
    ("Is it preferable mostly to", "Make sure things are arranged", "Just let things happen"),
    ("Do you prefer?", "Getting something done", "Having the option to go back"),
    ("Is it more like you to", "Make snap judgements", "Delay making judgements"),
]

questions6 = [
    ("Do you tend to choose", "Rather carefully", "Somewhat impulsively"),
    ("Does it bother you more having things", "Incomplete", "Completed"),
    ("Are you usually rather", "Quick to agree to a time", "Reluctant to agree to a time"),
    ("Are you more comfortable with", "Written agreements", "Handshake agreements"),
    ("Do you put more value on the", "Definite", "Variable"),
    ("Do you prefer things to be", "Neat and orderly", "Optional"),
    ("Are you more comfortable", "After a decision", "Before a decision"),
    ("Is it your way more to", "Get things settled", "Put off settlement"),
    ("Do you prefer to?", "Set things up perfectly", "Allow things to come together"),
    ("Do you tend to be more", "Deliberate than spontaneous", "Spontaneous than deliberate"),
]


def calculate_confidence(scores):
    total_diff = 0
    total_questions = 0
    for a, b in scores:
        total_diff += abs(a - b)
        total_questions += (a + b)
    if total_questions == 0:
        return 0.0
    confidence = (total_diff / total_questions) * 100
    return round(confidence, 2)


def compute_mbti_from_answers(answers):
    # answers: list of 'a' or 'b', expected length 60
    def count_slice(start, length):
        a = b = 0
        for ch in answers[start:start+length]:
            if str(ch).lower() == 'a':
                a += 1
            else:
                b += 1
        return a, b

    counter_a, counter_b = count_slice(0, 10)
    counter2_a, counter2_b = count_slice(10, 10)
    counter3_a, counter3_b = count_slice(20, 10)
    counter4_a, counter4_b = count_slice(30, 10)
    counter5_a, counter5_b = count_slice(40, 10)
    counter6_a, counter6_b = count_slice(50, 10)

    pcode = ''
    if counter_a > counter_b:
        pcode += 'E'
    else:
        pcode += 'I'

    plus1a3 = counter3_a + counter2_a
    plus2b3 = counter3_b + counter2_b
    if plus1a3 > plus2b3:
        pcode += 'S'
    else:
        pcode += 'N'

    plus1a5 = counter5_a + counter4_a
    plus2b5 = counter5_b + counter4_b
    if plus1a5 > plus2b5:
        pcode += 'T'
    else:
        pcode += 'F'

    plus1a6 = counter6_a + counter5_a
    plus2b6 = counter6_b + counter5_b
    if plus1a6 > plus2b6:
        pcode += 'J'
    else:
        pcode += 'P'

    dimension_scores = [
        (counter_a, counter_b),
        (counter2_a, counter2_b),
        (counter3_a, counter3_b),
        (counter5_a, counter5_b),
    ]
    confidence_score = calculate_confidence(dimension_scores)

    # Simple career mapping (subset)
    careers = {
        'ISTJ': 'Management, Administration, Accounting',
        'ISTP': 'Skilled trades, Technical fields, Agriculture',
        'ESTP': 'Marketing, Applied technology',
        'ESTJ': 'Management, Administration',
        'ISFJ': 'Education, Health Care',
        'ISFP': 'Healthcare, Business',
        'ESFP': 'Health care, Teaching, Skilled trades',
        'ESFJ': 'Education, Health care',
        'INFJ': 'Counseling, Teaching, Arts',
        'INFP': 'Counselling, Writing, Arts',
        'ENFP': 'Counseling, Teaching, Arts',
        'ENFJ': 'Religion, Arts, Teaching',
        'INTJ': 'Scientific fields, Computers, Law',
        'INTP': 'Scientific or technical fields',
        'ENTP': 'Science, Management, Technology, Arts',
        'ENTJ': 'Management, Leadership'
    }
    carear = careers.get(pcode, 'Management, Leadership')

    return {
        'pcode': pcode,
        'confidence': confidence_score,
        'career': carear,
        'scores': {
            'q1': (counter_a, counter_b),
            'q2': (counter2_a, counter2_b),
            'q3': (counter3_a, counter3_b),
            'q4': (counter4_a, counter4_b),
            'q5': (counter5_a, counter5_b),
            'q6': (counter6_a, counter6_b),
        }
    }


def save_result_to_csv(name, pcode, confidence_score, timestamp, serial, generated_by):
    file_path = os.path.join(os.path.dirname(__file__), 'mbti_results.csv')
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Name', 'MBTI', 'Confidence', 'DateTime', 'Serial', 'GeneratedBy'])
        writer.writerow([name, pcode, confidence_score, timestamp, serial, generated_by])




def generate_pdf_report(name, dob, gender, pcode, career, confidence_score, serial, generated_by, qr_url=None):
    reports_dir = os.path.join(os.path.dirname(__file__), 'static', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    safe_name = ''.join(c for c in name if c.isalnum() or c in (' ', '_')).rstrip()
    filename = f"{safe_name}_{serial}_MBTI_Report.pdf"
    file_path = os.path.join(reports_dir, filename)

    styles = getSampleStyleSheet()
    normal = styles['Normal']

    story = []

    # Header with optional logo
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(BASE_DIR, 'anand.jpg')
    logo = None
    if os.path.exists(logo_path):
        try:
            logo = Image(logo_path, width=0.8*inch, height=0.8*inch)
        except Exception:
            logo = None

    header_table = Table(
        [[Paragraph('<b>MBTI Personality Report</b>', styles['Title']), logo if logo else ' ']],
        colWidths=[4.5*inch, 1.5*inch]
    )
    header_table.setStyle(TableStyle([
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 12))
    # Serial number displayed at top-right below header
    try:
        serial_para = Paragraph(f"<b>Serial:</b> {serial}", ParagraphStyle('serial', parent=styles['Normal'], fontSize=9, alignment=2))
        serial_table = Table([["", serial_para]], colWidths=[4.5*inch, 1.5*inch])
        serial_table.setStyle(TableStyle([("ALIGN", (1, 0), (1, 0), "RIGHT")]))
        story.append(serial_table)
        story.append(Spacer(1, 8))
    except Exception:
        pass

    # Prepare QR image file (we will draw it in the footer at bottom-right)
    qr_path = None
    if qr_url:
        try:
            qr = qrcode.QRCode(box_size=6, border=2)
            qr.add_data(qr_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            # ensure RGB and save
            try:
                img = img.convert('RGB')
            except Exception:
                pass
            qr_path = os.path.join(reports_dir, f"{serial}_qr.png")
            img.save(qr_path)
        except Exception:
            qr_path = None

    # Section title style
    section_title = ParagraphStyle(
        'section',
        fontSize=10,
        textColor=colors.white,
        backColor=colors.darkblue,
        leading=12,
    )

    # Personal details table
    story.append(Paragraph('Personal Details', section_title))
    story.append(Spacer(1, 8))

    details_table = Table([
        ['Name', name],
        ['Date of Birth', dob],
        ['Gender', gender],
        ['Report Time', datetime.now().strftime('%d/%m/%Y , %H:%M:%S')],
    ], colWidths=[2*inch, 4*inch])
    details_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(details_table)
    story.append(Spacer(1, 16))

    # Personality summary
    story.append(Paragraph('Personality Summary', section_title))
    story.append(Spacer(1, 8))
    story.append(Paragraph(f'<b>Personality Type:</b> {pcode}', normal))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f'<b>Confidence Score:</b> {confidence_score}%', normal))
    story.append(Spacer(1, 12))

    # Career recommendations
    story.append(Paragraph('Career Recommendations', section_title))
    story.append(Spacer(1, 8))
    for line in str(career).split(','):
        if line.strip():
            story.append(Paragraph('• ' + line.strip(), normal))

    story.append(Spacer(1, 16))

    # Generated explanation mapping
    def personality_explanation(code):
        explanations = {
            "ISTJ": "You are practical, logical, and highly responsible. You value structure, rules, and reliability.",
            "ISFJ": "You are caring, loyal, and detail-oriented. You prefer helping others behind the scenes.",
            "INFJ": "You are insightful, empathetic, and driven by strong values.",
            "INTJ": "You are strategic, independent, and analytical.",
            "ISTP": "You are adaptable, practical, and action-oriented.",
            "ISFP": "You are sensitive, artistic, and values-driven.",
            "INFP": "You are idealistic, thoughtful, and empathetic.",
            "INTP": "You are curious, logical, and innovative.",
            "ESTP": "You are energetic, bold, and action-focused.",
            "ESFP": "You are outgoing, spontaneous, and enthusiastic.",
            "ENFP": "You are imaginative, energetic, and people-oriented.",
            "ENTP": "You are innovative, outspoken, and intellectually curious.",
            "ESTJ": "You are organized, practical, and leadership-oriented.",
            "ESFJ": "You are warm, responsible, and cooperative.",
            "ENFJ": "You are charismatic, empathetic, and inspiring.",
            "ENTJ": "You are confident, strategic, and decisive."
        }
        return explanations.get(code, "You have a unique personality blend that reflects adaptability and individual strengths.")

    story.append(Paragraph('Generated Personality Insight', section_title))
    story.append(Spacer(1, 8))
    story.append(Paragraph(personality_explanation(pcode), normal))
    story.append(Spacer(1, 14))

    # Disclaimer 
    story.append(Paragraph(f"<b>NOTE:-</b>please refer the attached document or search your personality type code on google for detailed career recommendation as per your personality type",normal))
    story.append(Spacer(1,16))

    disclaimer_para = Paragraph(
        "<b>DISCLAIMER:</b> This report is auto-generated and is NOT an official MBTI® assessment. The creators do not take any responsibility for decisions made based on this report.",
        normal
    )
    disclaimer_box = Table([[disclaimer_para]], colWidths=[6 * inch])
    disclaimer_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFE6E6")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.red),
        ("BOX", (0, 0), (-1, -1), 1, colors.red),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(disclaimer_box)

    # Place QR code 3mm below the disclaimer, aligned to the right
    if qr_path and os.path.exists(qr_path):
        try:
            story.append(Spacer(1, 3 * mm))
            qr_img = Image(qr_path, width=1 * inch, height=1 * inch)
            qr_table = Table([["", qr_img]], colWidths=[4.5 * inch, 1 * inch])
            qr_table.setStyle(TableStyle([
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ]))
            story.append(qr_table)
            story.append(Spacer(1, 6 * mm))
        except Exception:
            pass

    # Footer: draw generated_by (no QR in footer now)
    def footer(canvas, doc):
        canvas.setFont("Helvetica", 9)
        canvas.drawRightString(550, 30, f"Page {doc.page} | Generated by {generated_by}")

    doc = SimpleDocTemplate(file_path, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=40)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return filename


@app.route('/')
def index():
    # pass questions to template for client-side rendering
    all_questions = [q for q in (questions1 + questions2 + questions3 + questions4 + questions5 + questions6)]
    return render_template('index.html', questions=all_questions)


@app.route('/language')
def language():
    return render_template('language.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')





@app.route('/report/<serial>')
def report_view(serial):
    # load metadata JSON for this serial
    reports_dir = os.path.join(os.path.dirname(__file__), 'static', 'reports')
    meta_path = os.path.join(reports_dir, f"{serial}.json")
    if not os.path.isfile(meta_path):
        return "Report not found", 404
    with open(meta_path, 'r', encoding='utf-8') as mf:
        meta = json.load(mf)
    return render_template('report.html', serial=meta.get('serial'), name=meta.get('name'), dob=meta.get('dob'), gender=meta.get('gender'), pcode=meta.get('pcode'), confidence=meta.get('confidence'), career=meta.get('career'), generated_by=meta.get('generated_by'), pdf_filename=meta.get('pdf_filename'))


@app.route('/api/assess', methods=['POST'])
def assess():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    name = data.get('name', 'Anonymous')
    dob = data.get('dob', '')
    gender = data.get('gender', '')
    answers = data.get('answers', [])
    if not isinstance(answers, list) or len(answers) < 60:
        return jsonify({'error': 'Answers must be a list of 60 items (a/b)'}), 400

    result = compute_mbti_from_answers(answers)
    timestamp = datetime.now().isoformat()
    result.update({'name': name, 'dob': dob, 'gender': gender, 'generated_at': timestamp})

    # create serial and metadata
    serial = uuid.uuid4().hex[:10]
    generated_by = 'MBTI REPORT Anand'

    # save csv
    try:
        save_result_to_csv(name, result['pcode'], result['confidence'], timestamp, serial, generated_by)
        result['csv_saved'] = True
    except Exception as e:
        result['csv_saved'] = False
        result['csv_error'] = str(e)



    # generate pdf (include QR linking to report page)
    try:
        # build a small payload that will be embedded in the QR (so scanners see report data offline)
        qr_payload = json.dumps({
            'name': name,
            'pcode': result['pcode'],
            'confidence': result['confidence'],
            'career': result['career'],
            'serial': serial,
            'generated_by': generated_by,
        })

        # still provide the local report URL in the response for convenience
        base = request.host_url.rstrip('/')
        local_report_url = f"{base}/report/{serial}"

        pdf_filename = generate_pdf_report(name, dob, gender, result['pcode'], result['career'], result['confidence'], serial, generated_by, qr_url=qr_payload)
        result['pdf'] = f"/static/reports/{pdf_filename}"
        result['serial'] = serial
        result['generated_by'] = generated_by
        result['report_url'] = local_report_url

        # save metadata JSON for public report page
        try:
            reports_dir = os.path.join(os.path.dirname(__file__), 'static', 'reports')
            meta = {
                'name': name,
                'dob': dob,
                'gender': gender,
                'pcode': result['pcode'],
                'confidence': result['confidence'],
                'career': result['career'],
                'serial': serial,
                'generated_by': generated_by,
                'pdf_filename': pdf_filename,
                'timestamp': timestamp,
            }
            meta_path = os.path.join(reports_dir, f"{serial}.json")
            with open(meta_path, 'w', encoding='utf-8') as mf:
                json.dump(meta, mf, ensure_ascii=False, indent=2)
            result['metadata_saved'] = True
        except Exception as e:
            result['metadata_saved'] = False
            result['metadata_error'] = str(e)
    except Exception as e:
        result['pdf'] = None
        result['pdf_error'] = str(e)

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
