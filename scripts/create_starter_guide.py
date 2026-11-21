from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/jaynova-digital-product-starter-guide.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
FONT = '/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('Guide', FONT + 'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('GuideBold', FONT + 'DejaVuSans-Bold.ttf'))
BLUE, INK, LIME, GRAY, PAPER = map(HexColor, ['#243de8','#171b25','#d6f34b','#5d6471','#f8f9fc'])
W, H = 612, 792
c = canvas.Canvas(str(OUT), pagesize=(W,H))
c.setTitle('The Digital Product Starter Guide for Beginners')
c.setAuthor('JayNova Brands')
c.setSubject('A free practical workbook for making and sharing your first useful digital product')
body = ParagraphStyle('body',fontName='Guide',fontSize=11,leading=18,textColor=INK,spaceAfter=10)
small = ParagraphStyle('small',parent=body,fontSize=9,leading=14,textColor=GRAY)
head = ParagraphStyle('head',fontName='GuideBold',fontSize=16,leading=21,textColor=BLUE)

def para(text, y, style=body, x=48, width=516):
    p=Paragraph(text,style); _,h=p.wrap(width,H)
    assert y-h>67, f'Page overflow: {text[:55]}'
    p.drawOn(c,x,y-h)
    return y-h-12

def page(title,kicker='MAKE SOMETHING USEFUL'):
    c.setFillColor(PAPER);c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(BLUE);c.rect(0,H-11,W,11,fill=1,stroke=0)
    c.setFont('GuideBold',9);c.drawString(48,751,'JAYNOVA BRANDS / FREE STARTER GUIDE')
    c.setFillColor(GRAY);c.setFont('Guide',8);c.drawRightString(564,751,'BEGINNER EDITION / NOVEMBER 2026')
    y=para(kicker,714,small)
    y=para(title,y,ParagraphStyle('title',fontName='GuideBold',fontSize=30,leading=36,textColor=INK))
    return y-5

def finish(n):
    c.setStrokeColor(HexColor('#d8dde6'));c.line(48,53,564,53)
    c.setFillColor(GRAY);c.setFont('Guide',8)
    c.drawString(48,35,'jaynovabrands.com / Big ideas. Useful files. Honest claims.')
    c.drawRightString(564,35,f'{n:02d} / 12')
    c.showPage()

def bullet(text,y): return para('<b>+ </b>'+text,y)
def block(label,text,y):
    y=para(label,y,head)
    return para(text,y)

c.setFillColor(BLUE);c.rect(0,0,W,H,fill=1,stroke=0)
c.setFillColor(LIME);c.setFont('GuideBold',11);c.drawString(48,737,'JAYNOVA BRANDS / THE FREE DIGITAL DROP')
cover=ParagraphStyle('cover',fontName='GuideBold',fontSize=44,leading=48,textColor=white)
y=para('The Digital<br/>Product<br/>Starter Guide<br/>for Beginners',630,cover)
y=para('Make your first useful file.<br/>Give it a clear purpose.<br/>Share it without the hype.',y-25,ParagraphStyle('sub',fontName='Guide',fontSize=16,leading=25,textColor=white))
c.setFillColor(LIME);c.rect(48,145,516,54,fill=1,stroke=0)
c.setFillColor(INK);c.setFont('GuideBold',12);c.drawString(66,168,'12 PAGES. ZERO COST. NO INCOME PROMISES.')
c.setFillColor(white);c.setFont('Guide',9);c.drawString(48,76,'An original practical workbook, with a little JayNova attitude.')
c.drawString(48,59,'No account, email address, or payment is required to download.')
c.showPage()

y=page('Start small. Finish one thing.','YOUR ROUTE FROM IDEA TO DOWNLOAD')
y=para('A digital product is a reusable file or tool that helps someone do something. A useful checklist is a product. So is a worksheet, template, short guide, design asset, or small calculator. It does not need to be a course or an app.',y)
for label,text in [('Choose a person','Who is this for, and what are they trying to do?'),('Choose one result','Make one task easier, clearer, or faster.'),('Build the smallest useful version','A focused two-page worksheet can be more useful than an unfinished 100-page ebook.'),('Test the file','Ask someone to use it without your explanation.'),('Package and share','Use a clear filename, readable description, and working download.'),('Improve from real feedback','Track what people get stuck on, rather than inventing success statistics.')]:
    y=block(label,text,y)
finish(2)

y=page('Pick a format you can finish.','IDEA MENU')
for label,text in [('Checklist','For someone who needs to remember a sequence. Example: a first client-call preparation checklist.'),('Worksheet','For someone who needs to make a decision. Example: a one-page project scope planner.'),('Template','For someone who repeats a task. Example: an editable weekly content calendar.'),('Short guide','For someone who needs a clear explanation. Example: how to organize a simple client handoff.'),('Creative asset','For someone who needs a starting point. Example: original icon shapes, caption prompts, or presentation layouts.')]: y=block(label,text,y)
y=para('<b>Choose your first idea:</b> I will make a __________ for __________ so they can __________.',y)
y=para('Avoid starting with a giant bundle. Pick the format that solves your chosen task with the fewest moving parts.',y,small)
finish(3)

y=page('Find a problem worth solving.','LISTEN BEFORE YOU DESIGN')
y=para('Start with a task you understand from study, work, a hobby, or everyday life. Talk to a few people who actually do that task. A few conversations can improve an idea, but they are not proof of market demand.',y)
for text in ['What is the hardest or most repetitive part of this task?','How do you handle it now?','What do you repeatedly forget, rewrite, or look up?','What would a useful finished result look like?','Would you try this draft and tell me where it is confusing?']: y=bullet(text,y)
y=block('Write down the actual words','Keep a short list of the problems people describe. Do not invent reviews or turn a casual compliment into a customer testimonial.',y)
y=block('Choose a narrow promise','Try: "Plan one client project before you start." Avoid: "Build a six-figure empire with this PDF."',y)
y=para('<b>My audience:</b> _________________________________<br/><br/><b>Their task:</b> ___________________________________<br/><br/><b>The useful result:</b> ______________________________',y)
finish(4)

y=page('Write your one-page brief.','MAKE THE IDEA SPECIFIC')
for label,text in [('Working title','Use a plain name that tells the reader what the file helps them do.'),('Audience and situation','Describe one person using it at one moment: "A freelance designer preparing for a first client call."'),('Outcome','State what they will have or understand after using it.'),('Contents','List only what is needed: a short explanation, a worksheet, a worked example, and a checklist.'),('Boundaries','State what the file does not cover. A project planner is not a legal contract or a guarantee of paid work.')]: y=block(label,text,y)
y=para('<b>Done means:</b> a reader can open the file, understand the instructions, complete the task, and save their result.',y)
y=para('Set a realistic finish date: __________________________<br/><br/>The one feature I will leave out for now: _______________',y)
finish(5)

y=page('Build an actually useful draft.','EXAMPLE: A FIRST CLIENT-CALL CHECKLIST')
y=para('Use this structure as an example, then adapt it to your own topic. Keep each instruction concrete enough that someone can act on it.',y)
for label,text in [('Before the call','Write the client\'s main goal, the current problem, three questions, and any information you still need.'),('During the call','Capture the desired result, audience, timing, constraints, and the person who will make decisions.'),('After the call','Summarize what you heard, list open questions, and state the agreed next step. Mark estimates as estimates.'),('At the end of your product','Include one filled example and one blank worksheet. Label the example as fictional or illustrative.')]: y=block(label,text,y)
y=para('<b>Your draft outline:</b><br/><br/>1. ______________________________________________<br/><br/>2. ______________________________________________<br/><br/>3. ______________________________________________<br/><br/>4. ______________________________________________',y)
finish(6)

y=page('Use AI as a drafting assistant.','YOU ARE STILL THE EDITOR')
y=para('AI can help organize an outline, simplify an instruction, or suggest test cases. Review every claim and example yourself. Do not upload private client, patient, student, or account information into a prompt.',y)
y=block('Outline prompt','"Create a short outline for a [format] that helps [audience] do [one task]. Include a worked example and a blank worksheet. Keep it beginner-friendly. Flag facts that need checking. Do not invent credentials, testimonials, statistics, or income claims."',y)
y=block('Clarity prompt','"Review these instructions for ambiguity. Identify missing steps and unfamiliar terms. Suggest plain-language revisions. Keep the scope unchanged."',y)
y=block('Test prompt','"Pretend you are a first-time reader. List the places where this worksheet may be confusing. Give me five practical things to test with a real person."',y)
y=para('<b>Human review:</b> verify facts, remove filler, check examples, and make the final instructions your own. Check the terms and permissions for any assets or tools you use.',y)
finish(7)

y=page('Design for someone using it.','CLEAR BEATS COMPLICATED')
for text in ['Use a readable body font and strong contrast. Do not hide essential instructions in tiny type.','Keep headings consistent and leave enough space to write or type.','Use meaningful headings and an obvious reading order. Keep text selectable in exported PDFs.','Explain any symbols or colors used to indicate an action or status.','Check the document on a phone and a larger screen. Test at a higher zoom level.','For editable products, test the actual editing experience. For print products, test a plain black-and-white printout.']: y=bullet(text,y)
y=block('A simple design recipe','One main typeface, one heading style, one accent color, and consistent margins are enough for a first version.',y)
y=para('<b>Before export:</b> check spelling, links, page breaks, writing space, and whether the file still makes sense without you talking someone through it.',y)
finish(8)

y=page('Package it like you care.','THE FILE IS PART OF THE EXPERIENCE')
for label,text in [('Name the file clearly','Try first-client-call-checklist-v1.pdf. Avoid final-final-actually-final.pdf.'),('Include short instructions','Say what is included, how to open it, whether it is editable, and how the reader can use it.'),('Explain usage permissions','Use assets you created or have permission to distribute. State what recipients may do with your original material. Do not assume a paid tool grants resale rights to every included asset.'),('Test delivery','Download the exact uploaded file in a fresh browser session. Open it and check the pages, images, links, and any included attachments.'),('Keep an original','Save the editable source and a copy of the exact version you publish. Use a version number when you revise it.')]: y=block(label,text,y)
y=para('For this guide, you may use the worksheets and ideas for your own projects. The JayNova logos and branding do not become your business identity.',y,small)
finish(9)

y=page('Launch with a clear description.','NO MAKE-BELIEVE SUCCESS REQUIRED')
y=para('Your product page should answer four questions: who is it for, what does it help them do, what exactly is included, and how do they get it?',y)
y=block('Illustrative product description','"First Client-Call Checklist: a free, three-page PDF for new freelance designers. Prepare questions, capture project requirements, and record next steps. Includes a filled example and a blank worksheet. Download instantly; no email required."',y)
y=block('If you offer a product free','Call it free, explain any conditions, and make the download work. Do not show a made-up original price to suggest a discount.',y)
y=block('If you later charge for a product','Explain the format, compatibility, support, delivery, and applicable purchase terms before someone pays. Research any platform rules and obligations that apply to your actual business.',y)
y=para('A free product can help you learn what people find useful. Download counts are a signal, not a claim about unique customers, satisfaction, revenue, or future results.',y)
finish(10)

y=page('Collect less. Explain more.','DELIVERY, PRIVACY, AND SUPPORT')
y=para('A basic file download can work without a name, email address, or account. Add forms, analytics, or marketing tools only when you have a clear purpose for them.',y)
for text in ['Describe the information your actual site collects, why it collects it, who processes it, and how long it is kept.','Give visitors usable choices for optional tracking. A notice should match the code; a banner by itself does not create legal compliance.','Keep a free download separate from optional marketing signup. If you later send marketing, establish a working opt-out process.','Do not collect passwords, payment details, health information, or other sensitive data for a simple download.','Provide a support or privacy contact that you actually monitor. Do not invent a support mailbox.']: y=bullet(text,y)
y=para('This guide is general education, not legal, tax, or financial advice. Requirements depend on what you do, where you operate, and whom you serve. Get qualified advice for your situation when needed.',y,small)
finish(11)

y=page('Your first-week action plan.','LESS PLANNING THE EMPIRE. MORE FINISHING THE FILE.')
for label,text in [('Day 1 / Choose','Pick one audience, one task, and one format.'),('Day 2 / Listen','Talk with a few people and write a one-page brief.'),('Day 3 / Draft','Create the smallest useful version and a worked example.'),('Day 4 / Design','Improve layout, readability, and instructions.'),('Day 5 / Test','Ask someone to use the exact file without your help.'),('Day 6 / Package','Fix confusing parts, name files, and check usage permissions.'),('Day 7 / Share','Publish an honest description and a working download. Record what to improve next.')]: y=block(label,text,y)
y=para('<b>My first useful product:</b> __________________________<br/><br/><b>My finish date:</b> __________________________________',y)
finish(12)
c.save()
print(OUT)
