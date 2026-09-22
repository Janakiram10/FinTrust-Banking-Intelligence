from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"portfolio"/"resume"; OUT.mkdir(parents=True,exist_ok=True)
DOCX=OUT/"Palla_Janakiram_Data_Analyst_Resume.docx"

def hyperlink(p,text,url):
    part=p.part; rel=part.relate_to(url,"http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",is_external=True)
    h=OxmlElement("w:hyperlink"); h.set(qn("r:id"),rel); r=OxmlElement("w:r"); pr=OxmlElement("w:rPr")
    color=OxmlElement("w:color"); color.set(qn("w:val"),"0B5E75"); pr.append(color)
    u=OxmlElement("w:u"); u.set(qn("w:val"),"single"); pr.append(u); r.append(pr)
    t=OxmlElement("w:t"); t.text=text; r.append(t); h.append(r); p._p.append(h)

def heading(doc,text):
    p=doc.add_paragraph(); p.paragraph_format.space_before=Pt(4); p.paragraph_format.space_after=Pt(2)
    r=p.add_run(text.upper()); r.bold=True; r.font.size=Pt(9.5); r.font.color.rgb=RGBColor(0x0B,0x3A,0x53)
    b=OxmlElement("w:pBdr"); bottom=OxmlElement("w:bottom"); bottom.set(qn("w:val"),"single"); bottom.set(qn("w:sz"),"4"); bottom.set(qn("w:color"),"8DB4C2"); b.append(bottom); p._p.get_or_add_pPr().append(b)

def bullet(doc,text):
    p=doc.add_paragraph(style="List Bullet"); p.paragraph_format.left_indent=Inches(.16); p.paragraph_format.first_line_indent=Inches(-.12)
    p.paragraph_format.space_after=Pt(.7); p.paragraph_format.line_spacing=1.0
    r=p.add_run(text); r.font.size=Pt(8.55); return p

def role(doc,title,org,dates):
    t=doc.add_table(rows=1,cols=2); t.autofit=False; t.columns[0].width=Inches(5.5); t.columns[1].width=Inches(1.45)
    t.cell(0,0).width=Inches(5.5); t.cell(0,1).width=Inches(1.45)
    for c in t.row_cells(0): c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p=t.cell(0,0).paragraphs[0]; p.paragraph_format.space_after=Pt(0); r=p.add_run(title); r.bold=True; r.font.size=Pt(9); p.add_run(f" | {org}").font.size=Pt(9)
    p=t.cell(0,1).paragraphs[0]; p.alignment=WD_ALIGN_PARAGRAPH.RIGHT; p.paragraph_format.space_after=Pt(0); r=p.add_run(dates); r.bold=True; r.font.size=Pt(8.6)
    for cell in t.row_cells(0):
        tcPr=cell._tc.get_or_add_tcPr(); mar=OxmlElement("w:tcMar")
        for side in ("top","left","bottom","right"):
            x=OxmlElement(f"w:{side}"); x.set(qn("w:w"),"0"); x.set(qn("w:type"),"dxa"); mar.append(x)
        tcPr.append(mar)

doc=Document(); sec=doc.sections[0]; sec.top_margin=Inches(.42); sec.bottom_margin=Inches(.42); sec.left_margin=Inches(.55); sec.right_margin=Inches(.55)
styles=doc.styles; styles["Normal"].font.name="Arial"; styles["Normal"].font.size=Pt(8.4)
styles["Title"].font.name="Arial"; styles["Title"].font.color.rgb=RGBColor(0,0,0)

p=doc.add_paragraph(style="Title"); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after=Pt(0)
r=p.add_run("PALLA JANAKIRAM"); r.bold=True; r.font.size=Pt(18); r.font.color.rgb=RGBColor(0,0,0)
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after=Pt(1)
r=p.add_run("DATA ANALYST"); r.bold=True; r.font.size=Pt(10); r.font.color.rgb=RGBColor(0x0B,0x5E,0x75)
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after=Pt(2)
p.add_run("Hyderabad, Telangana  |  +91 9866804339  |  janakiram.palla01@gmail.com  |  ").font.size=Pt(8)
hyperlink(p,"GitHub","https://github.com/Janakiram10")

heading(doc,"Professional Summary")
p=doc.add_paragraph("Data Analyst candidate with 2+ years of experience in technical operations, structured-data validation, quality checks, reporting, and issue analysis. Uses SQL, Python, Pandas, Excel, PostgreSQL, Power BI and DAX to clean data, validate KPIs, build dimensional models and create decision-focused dashboards. Portfolio work covers banking and healthcare analytics, including locally executed PySpark, Delta Lake and dbt pipelines.")
p.paragraph_format.space_after=Pt(1); p.paragraph_format.line_spacing=1.04; p.runs[0].font.size=Pt(8.6)

heading(doc,"Technical Skills")
p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(1); p.paragraph_format.line_spacing=1.0
items=[("Analytics","SQL, Python, Pandas, NumPy, Excel, data cleaning, validation, EDA, KPI reporting, business analysis"),("BI and databases","Power BI, DAX, Power Query, dimensional modeling, PostgreSQL, DuckDB, data visualization"),("Modern analytics","PySpark, Apache Spark, Delta Lake, dbt, medallion architecture, Airflow DAG design"),("Tools","Git, GitHub, ArcGIS Pro, Google Earth Pro, KML/KMZ, Microsoft 365")]
for i,(a,b) in enumerate(items):
    rr=p.add_run(f"{a}: "); rr.bold=True; rr.font.size=Pt(8.35); rr=p.add_run(b+("  |  " if i<len(items)-1 else "")); rr.font.size=Pt(8.35)

heading(doc,"Professional Experience")
role(doc,"Sr. Associate - Customer Support","Tech Mahindra","Mar 2026 - Present")
bullet(doc,"Validate structured mapping and operational records against defined business rules, document discrepancies, and maintain accurate service records within SLA timelines.")
bullet(doc,"Investigate recurring data and service issues, coordinate escalations, and communicate resolution status clearly to internal stakeholders.")
role(doc,"Technical Support Engineer","Blue Dome Technologies","Jan 2024 - Dec 2025")
bullet(doc,"Performed data extraction, validation and quality checks for road-infrastructure, mapping and asset-analysis workflows using Excel, GIS tools and structured datasets.")
bullet(doc,"Reconciled asset attributes, GPS/KML information and source imagery; identified missing, duplicate and inconsistent records for correction and reporting.")
bullet(doc,"Maintained analytical deliverables, issue records and SOPs while coordinating with technical, GIS and operations teams to resolve data-quality problems.")

heading(doc,"Selected Projects")
role(doc,"FinTrust Banking Intelligence","Portfolio Project","2026")
bullet(doc,"Built a six-page Power BI banking dashboard covering executive performance, deposits, transactions, credit risk, fraud, customers and branches; validated 108 report elements and ten headline KPIs.")
bullet(doc,"Implemented a local Bronze-Silver-Gold lakehouse across 257,969 records using PySpark and Delta Lake, with checksum-based incremental ingestion and partitioned transaction processing.")
bullet(doc,"Built 11 dbt models with 12 passing tests, DuckDB serving tables, quality gates, monitoring and an eight-task Airflow DAG design; 8 automated repository tests passed.")
p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(1); p.add_run("Repository: ").bold=True; hyperlink(p,"github.com/Janakiram10/FinTrust-Banking-Intelligence","https://github.com/Janakiram10/FinTrust-Banking-Intelligence")
role(doc,"MediCore Healthcare Analytics","Portfolio Project","2026")
bullet(doc,"Analyzed synthetic multi-hospital operations covering 500,000 appointments and 300,000 encounters using PostgreSQL, SQL, Python and Pandas.")
bullet(doc,"Built validated Power BI and Plotly Dash reporting for revenue, collections, patient flow, no-shows, satisfaction, wait times and readmission monitoring.")
p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(1); p.add_run("Repository: ").bold=True; hyperlink(p,"github.com/Janakiram10/MediCore-Healthcare-Analytics","https://github.com/Janakiram10/MediCore-Healthcare-Analytics")

heading(doc,"Education and Certifications")
p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(0); p.paragraph_format.line_spacing=1.0
r=p.add_run("Bachelor of Technology in Mechanical Engineering"); r.bold=True; r.font.size=Pt(8.6)
p.add_run(" | WISTM, Andhra University | 2020 - 2023 | 72%\n").font.size=Pt(8.5)
p.add_run("Certifications: ").bold=True; p.add_run("SQL for Data Analytics | Python for Data Analysis | Microsoft Power BI | Microsoft Excel for Data Analysis").font.size=Pt(8.5)

for table in doc.tables:
    table.allow_autofit=False
doc.save(DOCX); print(DOCX)
