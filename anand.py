
print(                                                                                                                                               
"########################################################################## "                                                                                                                                         
"#                                                                        # "
"#                    A Psycometric Testing Program based by MBTI         # "                    
"#                                                                        # "                                                                                                                                                                                          #
"########################################################################## "
)
import os
import csv
import time
print("        Now Your Psycometric Test Has Been Started ")
print('  ')
while True:
    name = input('Enter your name :- ').strip()
    if name.isalpha() and len(name)>=3:
        name=name.upper()
        break
    else:
        print("invalid name, use alphabet only(min 3 letters)")

from datetime import datetime, date

def validate_dob(dob_str):
    try:
        dob = datetime.strptime(dob_str, "%d-%m-%Y").date()
        if dob > date.today():
            return False, "DOB cannot be in the future"
        if dob.year < 1900:
            return False, "Year is too old"
        
        return True, dob

    except ValueError:
        return False, "Invalid format or invalid date"

while True :
    dob: str= input("Enter DOB (DD-MM-YYYY): ")
    valid, result = validate_dob(dob)
    if valid :
        dob=result.strftime("%d-%m-%y")
        break
    else:
        print("Error:", result)

def validate_gender(gender):
    valid_genders = ["male", "female", "other"]
    if gender.lower() in valid_genders:
        return True, gender.capitalize()
    else:
        return False, "Invalid gender"
while True:    
    gender = input("Enter Gender (Male/Female/Other): ")
    valid, result = validate_gender(gender)
    if valid:
        gender=result
        break
    else:
        print("Error:")
    
total_time = time.time() 

def save_result_to_csv(name, pcode, confidence_score, timestamp):
    file_exists = os.path.isfile("mbti_results.csv")
    with open("mbti_results.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Name", "MBTI", "Confidence", "DateTime"])
        writer.writerow([
            name,
            pcode,
            confidence_score,
            timestamp
        ])

#--------------------------------------------------------------------------------------------------------------------#
qno = 0
pcode=''
questions1 = [("At a party do you", "interact with many, including strangers", "interact with a few, known  to you"),
    ("At parties do you", "Stay late, with increasing energy", "Leave early, with decreasing energy"),
    ("In your social groups do you", "Keep abreast of others happenings", "Get behind on the news"),
    ("Are you usually rather", "Quick to agree to a time", "Reluctant to agree to a time"),
    ("In company do you", "Start conversations", "Wait to be approached"),
    ("Does new interaction with others", "Stimulate and energize you", "Tax your reserves"),
    ("Do you prefer", "Many friends with brief contact", "A few friends with longer contact"),
    ("Do you", "Speak easily and at length with strangers", "Find little to say to strangers"),
    ("When the phone rings do you", "Quickly get to it first", "Hope someone else will answer"),
    ("At networking functions you are", "Easy to approach", "A little reserved")]


counter_a, counter_b = 0, 0


for question in questions1:
    qno += 1      #count question no
    question_string = "%s:\n\tA. %s\n\tB. %s\n[a/b]:  " % (question[0], question[1], question[2])
    answer = input(str(qno)+'.  '+question_string).lower()
    print('')
    while answer not in ("a", "b"):
        print("Please choose A or B")
        answer = input(question_string).lower()
    if answer == "a":
        counter_a += 1
    else:
        counter_b += 1
print("      ")

if counter_a > counter_b:
    print ('Your first personality code is: E')
    pcode=pcode+'E'
else:
    print ('Your first personality code is: I')
    pcode=pcode+'I'
print("      ")

##############################################################################

questions2 = [("Are you more", "Realistic", "Philosophically inclined "),
("Are you a more", "Sensible person", "Reflective person "),
("Are you usually more interested in", "Specifics", "Concepts "),
("Facts", "Speak for themselves", "Usually require interpretation "),
("Traditional common sense is", "Usually trustworthy", "often misleading "),
("Are you more frequently", "A practical sort of person", "An abstract sort of person "),
("Are you more drawn to", "Substantial information", "Credible assumptions "),
("Are you usually more interested in the", "Particular instance", "General case "),
("Do you prize more in yourself a", "Good sense of reality", "Good imagination "),
("Do you have more fun with", "Hands-on experience", "Blue-sky fantasy "),]


counter2_a, counter2_b = 0, 0


for question in questions2:
    qno += 1   #count question no
    question_string = "%s:\n\tA. %s\n\tB. %s\n[a/b]:  " % (question[0], question[1], question[2])
    answer = input(str(qno) + '.   ' + question_string).lower()
    print('')
    while answer not in ("a", "b"):
        print("Please choose A or B")
        answer = input(question_string).lower()
    if answer == "a":
        counter2_a += 1
    else:
        counter2_b += 1



##############################################################################

questions3 = [("Are you usually more", "Fair minded", "Kind hearted"),
("Is it more natural to be", "Fair to others", "Nice to others"),
("Are you more naturally", "Impartial", "Compassionate"),
("Are you inclined to be more", "Cool headed", "Warm hearted"),
("Are you usually more", "Tough minded", "Tender hearted"),
("Which is more satisfying", "To discuss an issue throughly", "To arrive at agreement on an issue"),
("Are you more comfortable when you are", "Objective", "Personal"),
("Are you typically more a person of", "Clear reason", "Strong feeling"),
("In judging are you usually more", "Neutral", "Charitable"),
("Are you usually more", "Unbiased", "compassionate")]

counter3_a, counter3_b = 0, 0


for question in questions3:
    qno += 1
    question_string = "%s:\n\tA. %s\n\tB. %s\n[a/b]:  " % (question[0], question[1], question[2])
    answer = input(str(qno) + '.   ' + question_string).lower()
    print('')
    while answer not in ("a", "b"):
        print("Please choose A or B")
        answer = input(question_string).lower()
    if answer == "a":
        counter3_a += 1
    else:
        counter3_b += 1

plus1a3 = counter3_a + counter2_a
plus2b3 = counter3_b + counter2_b

print("      ")


if plus1a3 > plus2b3:
    print ('Your second personality code is: S')
    pcode=pcode+'S'
else:
    print ('Your second personality code is: N')
    pcode=pcode+'N'
print("      ")

##############################################################################

questions4 = [("Do you tend to be more", "Dispassionate", "Sympathetic"),
("In first approaching others are you more", "Impersonal and detached", "Personal and engaging"),
("In judging are you more likely to be", "Impersonal", "Sentimental"),
("Would you rather be", "More just than merciful", "More merciful than just"),
("Are you usually more", "Tough minded", "Tender hearted"),
("Which rules you more", "Your head", "Your heart"),
("Do you value in yourself more that you are", "Unwavering", "Devoted"),
("Are you inclined more to be", "Fair-minded", "Sympathetic"),
("Are you convinced by?", "Evidence", "Someone you trust"),
("Are you typically more", "Just than lenient", "Lenient than just")]

counter4_a, counter4_b = 0, 0


for question in questions4:
    qno += 1  # count question no
    question_string = "%s:\n\tA. %s\n\tB. %s\n[a/b]:  " % (question[0], question[1], question[2])
    answer = input(str(qno) + '.   ' + question_string).lower()
    print('')
    while answer not in ("a", "b"):
        print("Please choose A or B")
        answer = input(question_string).lower()
    if answer == "a":
        counter4_a += 1
    else:
        counter4_b += 1

plus1a4 = counter4_a + counter3_a
plus2b4 = counter4_b + counter3_b



##############################################################################

questions5 = [("Do you prefer to work", "To deadlines", "Just whenever"),
("Are you usually more", "Punctual", "Leisurely"),
("Do you usually", "Settle things", "Keep options open"),
("Are you more comfortable", "Setting a schedule", "Putting things off"),
("Are you more prone to keep things", "well organized", "Open-ended"),
("Are you more comfortable with work", "Contracted", "Done on a casual basis"),
("Are you more comfortable with", "Final statements", "Tentative statements"),
("Is it preferable mostly to", "Make sure things are arranged", "Just let things happen"),
("Do you prefer?", "Getting something done", "Having the option to go back"),
("Is it more like you to", "Make snap judgements", "Delay making judgements")]

counter5_a, counter5_b = 0, 0


for question in questions5:
    qno += 1
    question_string = "%s:\n\tA. %s\n\tB. %s\n[a/b]:  " % (question[0], question[1], question[2])
    answer = input(str(qno) + '.  ' + question_string).lower()
    print('')
    while answer not in ("a", "b"):
        print("Please choose A or B")
        answer = input(question_string).lower()
    if answer == "a":
        counter5_a += 1
    else:
        counter5_b += 1

plus1a5 = counter5_a + counter4_a
plus2b5 = counter5_b + counter4_b

print("      ")

if plus1a5 > plus2b5:
    print ('Your third personality code is: T')
    pcode=pcode+'T'
else:
    print ('Your third personality code is: F')
    pcode=pcode+'F'

print("      ")

##############################################################################

questions6 = [("Do you tend to choose", "Rather carefully", "Somewhat impulsively"),
("Does it bother you more having things", "Incomplete", "Completed"),
("Are you usually rather", "Quick to agree to a time", "Reluctant to agree to a time"),
("Are you more comfortable with", "Written agreements", "Handshake agreements"),
("Do you put more value on the", "Definite", "Variable"),
("Do you prefer things to be", "Neat and orderly", "Optional"),
("Are you more comfortable", "After a decision", "Before a decision"),
("Is it your way more to", "Get things settled", "Put off settlement"),
("Do you prefer to?", "Set things up perfectly", "Allow things to come together"),
("Do you tend to be more", "Deliberate than spontaneous", "Spontaneous than deliberate")]

counter6_a, counter6_b = 0, 0


for question in questions6:
    qno += 1
    question_string = "%s:\n\tA. %s\n\tB. %s\n[a/b]:  " % (question[0], question[1], question[2])
    answer = input(str(qno) + '.  ' + question_string).lower()
    print('')
    while answer not in ("a", "b"):
        print("Please choose A or B")
        answer = input(question_string).lower()
    if answer == "a":
        counter6_a += 1
    else:
        counter6_b += 1

plus1a6 = counter6_a + counter5_a
plus2b6 = counter6_b + counter5_b

print("      ")
if plus1a6 > plus2b6:
    pcode=pcode+'J'
    print ('Your fourth personality code is: J')
else:
    print ('Your fourth personality code is: P')
    pcode=pcode+'P'
counterA = 0
counterB = 0


print ('')


def question(x):
    input('')


def answer(x):
    if question == 'a' or question == 'A':
        counterA = counterA + 1
    else:
        counterB = counterB + 1 


print(" ")
def calculate_confidence(scores):
    """
    scores = list of (a_count, b_count)
    returns confidence percentage
    """
    total_diff = 0
    total_questions = 0
    for a, b in scores:
        total_diff += abs(a - b)
        total_questions += (a + b)
    confidence = (total_diff / total_questions) * 100
    return round(confidence, 2)

dimension_scores = [
    (counter_a, counter_b),
    (counter2_a, counter2_b),
    (counter3_a, counter3_b),
    (counter5_a, counter5_b),    
]
confidence_score = calculate_confidence(dimension_scores)

print(" ")

print ("Thanks for attempting the test!")
print("Your personality Type as per MBTI is :",pcode)
print("Please refer the attached document or Search your personality type code on google for detailed career recomondations as per your personality type")


            ############           MBTI CHART          ############


print('On the basis of your presonality according to MBTI chart your carrier option is :-')

if pcode == 'ISTJ' :
    a = '\n\tManagement \n\tAdministration Law enforcement \n\tAccounting'
    carear = a
    print(a)
elif  pcode ==  'ISTP ':
    b = '\n\tSkilled trades \n\tTechnical fields \n\tAgriculture \n\tlaw enforcement \n\tMilitary'
    carear = b
    print(b)
elif pcode == 'ESTP' :
    c = '\n\tMarketing\n\t Skilled trades Business\n\tLaw enforcement \n\tApplied technology'
    carear = c
    print(c)
elif pcode == 'ESTJ' :
    d = '\n\tManagement\n\t Administration \n\tLaw enforcement'
    carear  = d
    print(d)
elif  pcode == 'ISFJ' :
    e = '\n\tEducation \n\tHealth Care\n\t Religous setting'
    carear = e
    print(e)
elif pcode == 'ISFP'  :
    f = '\n\tHealthcare \n\tBusiness \n\tLaw enforcement'
    carear = f
    print(f)
elif pcode == 'ESFP' :
    g = '\n\tHealth care \n\t Teaching coaching \n\t childcare \n\t  worker \n\t skilled trades'
    carear = g 
    print(g)
elif  pcode ==  'ESFJ'  :
    h = '\n\tEducation \n\t Health care \n\tReligion'
    carear = h
    print(h)
elif  pcode == 'INFJ'  :
    i = '\n\tReligon counseling \n\t Teaching Arts'
    carear = i
    print(i)
elif pcode == 'INFP' :
    j = '\n\tCounselling \n\t Writing \n\t Arts'
    carear = j
    print(j)
elif pcode == 'ENFP' :
    k = '\n\tCounseling \n\t Teacjing \n\t Religion \n\t Atrs'
    carear = k 
    print(k)
elif pcode == 'ENFJ' :
    l = '\n\tReligion \n\t Arts \n\t Teaching '
    carear = l
    print(l)
elif  pcode ==  'INTJ'  :
    m = '\n\tScientific or teaching feilds\n\t Computers\n\t Law'
    carear = m
    print(m)
elif  pcode == 'INTP' :
    n = '\n\tScientific or teachnical fields'
    carear = n
    print(n)
elif pcode ==  'ENTP':
    o = '\n\tScience \n\tManagement\n\t Teachnology\n\t Arts'
    carear = o
    print(o)
else :
    
    p = '\n\tManagement Leadership'
    carear = p
    print(p)

#######################################################

# time calculation     
remaint = time.time()  -  total_time
time_tuple = time.localtime()
tame = time.strftime('%d/%m/%Y , %H:%M:%S' , time_tuple)
print(tame)

# function for make report and save it
with open('testreport.txt', "w") as cr:
    cr.write(f"Name :- {name}\n")
    cr.write(f"Date of Birth :- {dob}\n")
    cr.write(f"Gender :- {gender}\n")
    cr.write(f"Time of report :- {tame}\n")
    cr.write(f"\nPersonality = {pcode}\n")
    cr.write(f"\nConfidence Score :- {confidence_score}%\n")
    cr.write(f"\nCareer Option :- {carear}\n")
    ttk = (int(remaint) // 60) + 1
    cr.write(f"\nTotal time taken :- {ttk} min")
    cr.write("\nserial no.")
    cr.write("\ngeberated by ")
    
    
    cr.write(f"\n****DISCLAIMER:-THIS IS NOT OFFICIALLY GENERATED BY MBTI .SO, WE DOES NOT TAKE ANY RESPONSIBILITY****")

    print("Report saved at:",cr)

save_result_to_csv(name, pcode, confidence_score, tame)

######################################################
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch


def convert_report_to_pdf(name, dob, gender, pcode, carear, tame, remaint):
    file_name = f"{name}_MBTI_Report.pdf"

    pdf = SimpleDocTemplate(
        file_name,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=60,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    story = []

    # ---------------- HEADER  ----------------
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(BASE_DIR, "anand.jpg")

    logo=None
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=0.8*inch, height=0.8*inch)



    header_table = Table(
        [[
            Paragraph("<b>MBTI Personality Report</b>", styles["Title"]),
            logo if logo else " "
        ]],
        colWidths=[4.5*inch, 1.5*inch]
    )

    header_table.setStyle(TableStyle([
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))

    story.append(header_table)
    story.append(Spacer(1, 20))

    # ---------------- SECTION STYLE ----------------
    section_title = ParagraphStyle(
        "section",
        fontSize=10,
        textColor=colors.white,
        backColor=colors.darkblue,
        padding=8
    )

    normal = styles["Normal"]

    # ---------------- PERSONAL DETAILS ----------------
    story.append(Paragraph("Personal Details", section_title))
    story.append(Spacer(1, 8))

    details_table = Table([
        ["Name", name],
        ["Date of Birth", dob],
        ["Gender", gender],
        ["Report Time", tame],
    ], colWidths=[2*inch, 4*inch])

    details_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))

    story.append(details_table)
    story.append(Spacer(1, 20))

    # ---------------- PERSONALITY SUMMARY ----------------
    story.append(Paragraph("Personality Summary", section_title))
    story.append(Spacer(1, 8))
    story.append(Paragraph(f"<b>Personality Type:</b> {pcode}", normal))
    story.append(Spacer(1, 16))
    story.append(
    Paragraph(f"<b>Confidence Score:</b> {confidence_score}%", normal))
    story.append(Spacer(1, 10))

    # ---------------- CAREER RECOMMENDATIONS ----------------
    story.append(Paragraph("Career Recommendations", section_title))
    story.append(Spacer(1, 8))

    for line in carear.split("\n"):
        if line.strip():
            story.append(Paragraph("• " + line.strip(), normal))

    story.append(Spacer(1, 20))

    # ---------------- TIME  ----------------
    minutes = (int(remaint) // 60) + 1
    story.append(Paragraph(f"<b>Total Time Taken:</b> {minutes} minutes", normal))
    story.append(Spacer(1, 10))

    

    

    def personality_explanation(pcode):
        explanations = {
            "ISTJ": "You are practical, logical, and highly responsible. You value structure, rules, and reliability, making you excellent at planning and execution.",
            "ISFJ": "You are caring, loyal, and detail-oriented. You prefer helping others behind the scenes and value stability and harmony.",
            "INFJ": "You are insightful, empathetic, and driven by strong values. You often seek deep meaning and purpose in your actions.",
            "INTJ": "You are strategic, independent, and analytical. You enjoy solving complex problems and thinking long-term.",
            "ISTP": "You are adaptable, practical, and action-oriented. You learn best through hands-on experience.",
            "ISFP": "You are sensitive, artistic, and values-driven. You prefer personal freedom and creative expression.",
            "INFP": "You are idealistic, thoughtful, and empathetic. You are guided by strong inner values and creativity.",
            "INTP": "You are curious, logical, and innovative. You enjoy analyzing ideas and exploring possibilities.",
            "ESTP": "You are energetic, bold, and action-focused. You thrive in dynamic environments and enjoy challenges.",
            "ESFP": "You are outgoing, spontaneous, and enthusiastic. You enjoy engaging with people and living in the moment.",
            "ENFP": "You are imaginative, energetic, and people-oriented. You excel at motivating others and generating new ideas.",
            "ENTP": "You are innovative, outspoken, and intellectually curious. You enjoy debates and exploring new concepts.",
            "ESTJ": "You are organized, practical, and leadership-oriented. You value efficiency and clear structures.",
            "ESFJ": "You are warm, responsible, and cooperative. You prioritize relationships and social harmony.",
            "ENFJ": "You are charismatic, empathetic, and inspiring. You naturally guide and support others.",
            "ENTJ": "You are confident, strategic, and decisive. You excel in leadership and goal-oriented environments."
        }
        return explanations.get(pcode,"You have a unique personality blend that reflects adaptability and individual strengths.")
    
    # ---------------- GENERATED PERSONALITY EXPLANATION ----------------
    text = personality_explanation(pcode)
    story.append(Paragraph("Generated Personality Insight", section_title))
    story.append(Spacer(1, 8))
    story.append(Paragraph(text, normal))
    story.append(Spacer(1, 20))
    
    # ---------------- DISCLAIMER (RED WITH PADDING) ----------------
    story.append(Paragraph(f"<b>NOTE:-</b>please refer the attached document or search your personality type code on googlefor detailed career recomondation as per your personality type",normal))
    story.append(Spacer(1,16))
    
    
    
    disclaimer_para = Paragraph(
    "<b>DISCLAIMER:</b> This report is auto-generated and is NOT an official "
    "MBTI® assessment. The creators do not take any responsibility for decisions "
    "made based on this report.",styles["Normal"]
    )

    disclaimer_box = Table(
    [[disclaimer_para]],
    colWidths=[6 * inch])
    

    disclaimer_box.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFE6E6")),
    ("TEXTCOLOR", (0, 0), (-1, -1), colors.red),
    ("BOX", (0, 0), (-1, -1), 1, colors.red),

    # PADDING 
    ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ("TOPPADDING", (0, 0), (-1, -1), 10),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    
    story.append(Spacer(1, 25))
    story.append(disclaimer_box)

    # ---------------- FOOTER ----------------
    def footer(canvas, doc):
        canvas.setFont("Helvetica", 9)
        canvas.drawRightString(
            200 * mm if False else 550, 20,
            f"Page {doc.page} | Generated by Project"
        )

    pdf.build(story, onFirstPage=footer, onLaterPages=footer)

    print("Professional PDF created:", file_name)

convert_report_to_pdf(name, dob, gender, pcode, carear, tame, remaint)
