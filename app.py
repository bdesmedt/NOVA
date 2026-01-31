import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Page config
st.set_page_config(
    page_title="NOVA Platform Demo",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main { background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); }
    
    .stApp { font-family: 'Inter', sans-serif; }
    
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #0f172a;
    }
    
    .metric-label {
        font-size: 14px;
        color: #64748b;
        margin-bottom: 8px;
    }
    
    .metric-delta-positive { color: #10b981; font-size: 14px; }
    .metric-delta-negative { color: #ef4444; font-size: 14px; }
    
    .agent-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 8px 0;
        border-left: 4px solid;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .agent-aria { border-left-color: #14b8a6; }
    .agent-nova { border-left-color: #8b5cf6; }
    .agent-sage { border-left-color: #f59e0b; }
    .agent-luna { border-left-color: #3b82f6; }
    .agent-alex { border-left-color: #ec4899; }
    
    .status-active { 
        background: #dcfce7; 
        color: #166534; 
        padding: 4px 12px; 
        border-radius: 20px; 
        font-size: 12px;
        font-weight: 500;
    }
    
    .status-won { background: #dcfce7; color: #166534; }
    .status-negotiation { background: #fef3c7; color: #92400e; }
    .status-proposal { background: #dbeafe; color: #1e40af; }
    .status-qualified { background: #f3e8ff; color: #6b21a8; }
    .status-lead { background: #f1f5f9; color: #475569; }
    
    .pipeline-stage {
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 500;
        display: inline-block;
    }
    
    .invoice-row {
        background: white;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
        border: 1px solid #e2e8f0;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .invoice-row:hover {
        border-color: #14b8a6;
        box-shadow: 0 4px 12px rgba(20,184,166,0.15);
    }
    
    .rgs-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
        padding: 16px 24px;
        border-radius: 12px 12px 0 0;
        font-weight: 600;
    }
    
    .rgs-row {
        display: flex;
        justify-content: space-between;
        padding: 12px 24px;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .rgs-row:nth-child(even) { background: #f8fafc; }
    
    .rgs-total {
        background: #0f172a;
        color: white;
        font-weight: 600;
    }
    
    .odoo-badge {
        background: linear-gradient(135deg, #714B67 0%, #8F5C7A 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
    }
    
    .portal-toggle {
        background: white;
        border-radius: 12px;
        padding: 8px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .client-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid #e2e8f0;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .client-card:hover {
        border-color: #14b8a6;
        box-shadow: 0 4px 16px rgba(20,184,166,0.15);
        transform: translateY(-2px);
    }
    
    .client-status-green { border-left: 4px solid #10b981; }
    .client-status-yellow { border-left: 4px solid #f59e0b; }
    .client-status-red { border-left: 4px solid #ef4444; }
    
    .team-member {
        background: white;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        border: 1px solid #e2e8f0;
    }
    
    .alert-card {
        background: #fef3c7;
        border: 1px solid #f59e0b;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
    }
    
    .alert-card-red {
        background: #fee2e2;
        border: 1px solid #ef4444;
    }
    
    h1, h2, h3 { color: #0f172a; }
    
    .sidebar .sidebar-content { background: #0f172a; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'portal_mode' not in st.session_state:
    st.session_state.portal_mode = 'kantoor'  # 'kantoor' or 'klant'
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'dashboard'
if 'selected_client' not in st.session_state:
    st.session_state.selected_client = None
if 'selected_invoice' not in st.session_state:
    st.session_state.selected_invoice = None
if 'processed_invoices' not in st.session_state:
    st.session_state.processed_invoices = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'selected_deal' not in st.session_state:
    st.session_state.selected_deal = None

# ============================================
# DEMO DATA - KANTOOR (FIRM) LEVEL
# ============================================

FIRM_INFO = {
    "name": "NOVA Partners",
    "location": "Amsterdam",
    "employees": 12,
    "clients": 45
}

TEAM_MEMBERS = [
    {"name": "Lisa van der Berg", "role": "Managing Partner", "clients": 8, "workload": 85, "avatar": "👩‍💼"},
    {"name": "Mark de Vries", "role": "Senior Accountant", "clients": 12, "workload": 92, "avatar": "👨‍💼"},
    {"name": "Sophie Jansen", "role": "Accountant", "clients": 10, "workload": 78, "avatar": "👩‍💻"},
    {"name": "Thomas Bakker", "role": "Junior Accountant", "clients": 8, "workload": 65, "avatar": "👨‍💻"},
    {"name": "Emma de Groot", "role": "Fiscalist", "clients": 7, "workload": 88, "avatar": "👩‍⚖️"},
]

# Demo clients for the firm
DEMO_CLIENTS = [
    {
        "id": "CL001",
        "name": "Vermeer Bouw B.V.",
        "contact": "Jan Vermeer",
        "kvk": "12345678",
        "btw": "NL123456789B01",
        "sector": "Bouw & Constructie",
        "omzet_ytd": 612500,
        "omzet_prev": 545200,
        "winst_ytd": 89400,
        "openstaand": 142000,
        "status": "green",
        "accountant": "Mark de Vries",
        "alerts": [],
        "last_activity": "2 uur geleden"
    },
    {
        "id": "CL002",
        "name": "TechStart B.V.",
        "contact": "Jessica de Vries",
        "kvk": "23456789",
        "btw": "NL234567890B01",
        "sector": "IT & Software",
        "omzet_ytd": 890000,
        "omzet_prev": 720000,
        "winst_ytd": 156000,
        "openstaand": 45000,
        "status": "green",
        "accountant": "Sophie Jansen",
        "alerts": [],
        "last_activity": "1 dag geleden"
    },
    {
        "id": "CL003",
        "name": "Restaurant De Gouden Lepel",
        "contact": "Ahmed El-Amrani",
        "kvk": "34567890",
        "btw": "NL345678901B01",
        "sector": "Horeca",
        "omzet_ytd": 425000,
        "omzet_prev": 480000,
        "winst_ytd": 28500,
        "openstaand": 67500,
        "status": "yellow",
        "accountant": "Lisa van der Berg",
        "alerts": ["BTW deadline nadert", "Margedruk door stijgende kosten"],
        "last_activity": "3 uur geleden"
    },
    {
        "id": "CL004",
        "name": "Logistics Plus B.V.",
        "contact": "Robert Smit",
        "kvk": "45678901",
        "btw": "NL456789012B01",
        "sector": "Transport & Logistiek",
        "omzet_ytd": 1250000,
        "omzet_prev": 1180000,
        "winst_ytd": 125000,
        "openstaand": 312000,
        "status": "yellow",
        "accountant": "Mark de Vries",
        "alerts": ["Hoge debiteurenstand"],
        "last_activity": "5 uur geleden"
    },
    {
        "id": "CL005",
        "name": "Retail Mode B.V.",
        "contact": "Nina Petrova",
        "kvk": "56789012",
        "btw": "NL567890123B01",
        "sector": "Retail",
        "omzet_ytd": 320000,
        "omzet_prev": 450000,
        "winst_ytd": -45000,
        "openstaand": 89000,
        "status": "red",
        "accountant": "Emma de Groot",
        "alerts": ["Negatief resultaat", "Liquiditeitsprobleem dreigt", "Urgent gesprek nodig"],
        "last_activity": "30 min geleden"
    },
    {
        "id": "CL006",
        "name": "Gezondheidscentrum Oost",
        "contact": "Dr. Karin van Dijk",
        "kvk": "67890123",
        "btw": "NL678901234B01",
        "sector": "Zorg",
        "omzet_ytd": 780000,
        "omzet_prev": 720000,
        "winst_ytd": 98000,
        "openstaand": 23000,
        "status": "green",
        "accountant": "Thomas Bakker",
        "alerts": [],
        "last_activity": "1 dag geleden"
    },
    {
        "id": "CL007",
        "name": "Bakkerij Het Zoete Leven",
        "contact": "Peter Willems",
        "kvk": "78901234",
        "btw": "NL789012345B01",
        "sector": "Food & Beverage",
        "omzet_ytd": 285000,
        "omzet_prev": 260000,
        "winst_ytd": 42000,
        "openstaand": 12500,
        "status": "green",
        "accountant": "Sophie Jansen",
        "alerts": [],
        "last_activity": "2 dagen geleden"
    },
    {
        "id": "CL008",
        "name": "Architectenbureau Modern",
        "contact": "Isabelle Dubois",
        "kvk": "89012345",
        "btw": "NL890123456B01",
        "sector": "Zakelijke Diensten",
        "omzet_ytd": 520000,
        "omzet_prev": 485000,
        "winst_ytd": 112000,
        "openstaand": 78000,
        "status": "green",
        "accountant": "Lisa van der Berg",
        "alerts": [],
        "last_activity": "4 uur geleden"
    },
]

FIRM_ALERTS = [
    {"type": "urgent", "client": "Retail Mode B.V.", "message": "Liquiditeitsprobleem - direct actie vereist", "time": "30 min geleden"},
    {"type": "warning", "client": "Restaurant De Gouden Lepel", "message": "BTW Q4 deadline over 5 dagen", "time": "2 uur geleden"},
    {"type": "warning", "client": "Logistics Plus B.V.", "message": "DSO gestegen naar 62 dagen", "time": "5 uur geleden"},
    {"type": "info", "client": "TechStart B.V.", "message": "Jaarrekening 2023 klaar voor review", "time": "1 dag geleden"},
]

# AI Agents (inclusive/international names)
AI_AGENTS = {
    "ARIA": {
        "full_name": "AI Recognition & Invoice Assistant",
        "role": "Factuurverwerking",
        "color": "#14b8a6",
        "status": "Actief",
        "processed_today": 47,
        "accuracy": 99.2,
        "description": "Herkent en verwerkt inkomende facturen automatisch",
        "odoo_link": "Sales & Purchase Orders"
    },
    "NOVA": {
        "full_name": "Numerical Operations & Verification Agent",
        "role": "Documentanalyse", 
        "color": "#8b5cf6",
        "status": "Actief",
        "processed_today": 23,
        "accuracy": 98.7,
        "description": "Analyseert contracten en financiële documenten",
        "odoo_link": "Voorraad & Projecten"
    },
    "SAGE": {
        "full_name": "Strategic Advisory & Guidance Engine",
        "role": "Fiscaal Advies",
        "color": "#f59e0b",
        "status": "Actief",
        "processed_today": 12,
        "accuracy": 97.5,
        "description": "Geeft proactief fiscaal en belastingadvies",
        "odoo_link": "HR & Payroll"
    },
    "LUNA": {
        "full_name": "Lookout & Understanding for Numerical Analysis",
        "role": "Forecasting",
        "color": "#3b82f6",
        "status": "Actief",
        "processed_today": 8,
        "accuracy": 94.3,
        "description": "Maakt voorspellingen en scenario-analyses",
        "odoo_link": "CRM Pipeline"
    },
    "ALEX": {
        "full_name": "Advisory Liaison & Expert eXchange",
        "role": "Klantvragen",
        "color": "#ec4899",
        "status": "Actief",
        "processed_today": 156,
        "accuracy": 96.8,
        "description": "Beantwoordt vragen en geeft uitleg",
        "odoo_link": "Alle Modules"
    }
}

# Demo Invoices (client-level)
DEMO_INVOICES = [
    {"id": "F2024-001", "supplier": "Bouwmaterialen Jansen B.V.", "amount": 4750.00, "vat": 997.50, "date": "2024-01-15", "status": "verwerkt", "category": "Inkoop materialen", "rgs": "WIkworGro", "odoo_po": "PO2024-042"},
    {"id": "F2024-002", "supplier": "Transport De Vries", "amount": 1250.00, "vat": 262.50, "date": "2024-01-16", "status": "verwerkt", "category": "Transport", "rgs": "WKprUitTra", "odoo_po": "PO2024-038"},
    {"id": "F2024-003", "supplier": "Energie Direct", "amount": 892.50, "vat": 187.43, "date": "2024-01-17", "status": "verwerkt", "category": "Energie", "rgs": "WBehHuiEne", "odoo_po": None},
    {"id": "F2024-004", "supplier": "Kraan & Hijswerk Utrecht", "amount": 3200.00, "vat": 672.00, "date": "2024-01-18", "status": "wacht op review", "category": "Ingehuurde diensten", "rgs": "WKprUitInh", "odoo_po": "PO2024-045"},
    {"id": "F2024-005", "supplier": "Sanitair Groothandel NL", "amount": 2180.00, "vat": 457.80, "date": "2024-01-19", "status": "nieuw", "category": "Inkoop materialen", "rgs": "WIkworGro", "odoo_po": "PO2024-047"},
    {"id": "F2024-006", "supplier": "Verzekeringen Centraal", "amount": 1450.00, "vat": 0.00, "date": "2024-01-20", "status": "nieuw", "category": "Verzekeringen", "rgs": "WBehVerBed", "odoo_po": None},
    {"id": "F2024-007", "supplier": "ICT Solutions Partner", "amount": 599.00, "vat": 125.79, "date": "2024-01-21", "status": "nieuw", "category": "Automatisering", "rgs": "WBehAutSof", "odoo_po": None},
    {"id": "F2024-008", "supplier": "Houthandel Rotterdam", "amount": 6420.00, "vat": 1348.20, "date": "2024-01-22", "status": "nieuw", "category": "Inkoop materialen", "rgs": "WIkworGro", "odoo_po": "PO2024-051"},
]

# Odoo CRM Pipeline Data
ODOO_CRM_PIPELINE = [
    {"id": "CRM-001", "name": "Nieuwbouw Villa Wassenaar", "client": "Fam. Bakker", "stage": "Onderhandeling", "amount": 285000, "probability": 75, "expected_close": "2024-02-15", "contact": "M. Bakker", "email": "m.bakker@email.nl", "phone": "+31 6 12345678", "notes": "Wachten op bouwvergunning"},
    {"id": "CRM-002", "name": "Renovatie Kantoorpand Utrecht", "client": "TechStart B.V.", "stage": "Voorstel", "amount": 125000, "probability": 50, "expected_close": "2024-03-01", "contact": "J. de Vries", "email": "j.devries@techstart.nl", "phone": "+31 6 23456789", "notes": "Concurrent offerte bij Bouwgroep X"},
    {"id": "CRM-003", "name": "Uitbouw Woning Hilversum", "client": "Fam. Jansen", "stage": "Onderhandeling", "amount": 68000, "probability": 80, "expected_close": "2024-02-28", "contact": "P. Jansen", "email": "pjansen@gmail.com", "phone": "+31 6 34567890", "notes": "Akkoord op prijs, contract deze week"},
    {"id": "CRM-004", "name": "Bedrijfshal Nieuwegein", "client": "Logistics Plus", "stage": "Kwalificatie", "amount": 420000, "probability": 25, "expected_close": "2024-05-15", "contact": "R. Smit", "email": "r.smit@logisticsplus.nl", "phone": "+31 6 45678901", "notes": "Eerste gesprek positief, site visit gepland"},
    {"id": "CRM-005", "name": "Verbouwing Restaurant Amsterdam", "client": "Eet & Geniet B.V.", "stage": "Voorstel", "amount": 95000, "probability": 60, "expected_close": "2024-03-15", "contact": "A. Hendriks", "email": "a.hendriks@eetengeniet.nl", "phone": "+31 6 56789012", "notes": "Offerte verstuurd, follow-up volgende week"},
    {"id": "CRM-006", "name": "Dakrenovatie Appartementencomplex", "client": "VvE Parkzicht", "stage": "Lead", "amount": 180000, "probability": 15, "expected_close": "2024-06-01", "contact": "K. Visser", "email": "vve.parkzicht@gmail.com", "phone": "+31 6 67890123", "notes": "Eerste contact via website"},
    {"id": "CRM-007", "name": "Aanbouw Praktijkruimte Amersfoort", "client": "Huisartsenpraktijk Centrum", "stage": "Gewonnen", "amount": 78000, "probability": 100, "expected_close": "2024-01-20", "contact": "Dr. M. Kok", "email": "m.kok@hapcentrum.nl", "phone": "+31 6 78901234", "notes": "Contract getekend!"},
    {"id": "CRM-008", "name": "Showroom Verbouwing Breda", "client": "AutoMax B.V.", "stage": "Kwalificatie", "amount": 210000, "probability": 30, "expected_close": "2024-04-15", "contact": "T. van Dam", "email": "t.vandam@automax.nl", "phone": "+31 6 89012345", "notes": "Budget bevestigd, wachten op specificaties"},
]

# Odoo Purchase Orders
ODOO_PURCHASE_ORDERS = [
    {"id": "PO2024-042", "supplier": "Bouwmaterialen Jansen B.V.", "amount": 4750.00, "status": "Geleverd", "date": "2024-01-10", "project": "CRM-007"},
    {"id": "PO2024-038", "supplier": "Transport De Vries", "amount": 1250.00, "status": "Geleverd", "date": "2024-01-12", "project": "CRM-007"},
    {"id": "PO2024-045", "supplier": "Kraan & Hijswerk Utrecht", "amount": 3200.00, "status": "Gepland", "date": "2024-01-25", "project": "CRM-001"},
    {"id": "PO2024-047", "supplier": "Sanitair Groothandel NL", "amount": 2180.00, "status": "Besteld", "date": "2024-01-18", "project": "CRM-003"},
    {"id": "PO2024-051", "supplier": "Houthandel Rotterdam", "amount": 6420.00, "status": "Besteld", "date": "2024-01-20", "project": "CRM-001"},
]

# Odoo HR Data
ODOO_HR = {
    "employees": [
        {"name": "Jan Vermeer", "role": "Directeur", "salary": 7500, "fte": 1.0},
        {"name": "Karin de Boer", "role": "Projectleider", "salary": 5200, "fte": 1.0},
        {"name": "Pieter Bakker", "role": "Voorman", "salary": 4500, "fte": 1.0},
        {"name": "Sander Visser", "role": "Timmerman", "salary": 3800, "fte": 1.0},
        {"name": "Ahmed El-Ahmadi", "role": "Metselaar", "salary": 3600, "fte": 1.0},
        {"name": "Tomasz Kowalski", "role": "Metselaar", "salary": 3600, "fte": 1.0},
        {"name": "Erik Jansen", "role": "Elektricien", "salary": 4000, "fte": 0.8},
        {"name": "Mohammed Al-Rashid", "role": "Loodgieter", "salary": 3900, "fte": 1.0},
    ],
    "total_fte": 7.8,
    "total_salary_costs": 36100,
    "wkr_budget": 10830,  # 3% van loonsom
    "wkr_used": 7250,
}

# RGS Mapping voor W&V
RGS_WV = {
    "WOmzNet": {"name": "Netto-omzet", "amount": 612500, "category": "Omzet"},
    "WOmzOov": {"name": "Overige opbrengsten", "amount": 8500, "category": "Omzet"},
    "WIkworGro": {"name": "Grond- en hulpstoffen", "amount": -185000, "category": "Kostprijs"},
    "WIkworUitworInh": {"name": "Uitbesteed werk", "amount": -95000, "category": "Kostprijs"},
    "WPersLonSal": {"name": "Lonen en salarissen", "amount": -180000, "category": "Personeelskosten"},
    "WPersSocLas": {"name": "Sociale lasten", "amount": -42000, "category": "Personeelskosten"},
    "WPersPenLas": {"name": "Pensioenlasten", "amount": -18000, "category": "Personeelskosten"},
    "WBehHuiHur": {"name": "Huur bedrijfspand", "amount": -36000, "category": "Huisvesting"},
    "WBehHuiEne": {"name": "Energie", "amount": -8500, "category": "Huisvesting"},
    "WBehVerBed": {"name": "Bedrijfsverzekeringen", "amount": -12000, "category": "Overig"},
    "WBehAutAfsTrm": {"name": "Afschrijving transportmiddelen", "amount": -15000, "category": "Afschrijvingen"},
    "WBehAutAfsMac": {"name": "Afschrijving machines", "amount": -8500, "category": "Afschrijvingen"},
    "WFinRenRba": {"name": "Rentelasten bankschuld", "amount": -4200, "category": "Financieel"},
}

# RGS Mapping voor Balans
RGS_BALANS = {
    "activa": {
        "BIvaMatTer": {"name": "Terreinen", "amount": 125000},
        "BIvaMatBeg": {"name": "Bedrijfsgebouwen", "amount": 285000},
        "BIvaMatMae": {"name": "Machines en installaties", "amount": 95000},
        "BIvaMatTrm": {"name": "Transportmiddelen", "amount": 68000},
        "BVrdVor": {"name": "Voorraden grondstoffen", "amount": 42000},
        "BVorDebHad": {"name": "Debiteuren", "amount": 142000},
        "BLimBan": {"name": "Bankrekeningen", "amount": 89000},
        "BLimKas": {"name": "Kas", "amount": 2500},
    },
    "passiva": {
        "BEivGok": {"name": "Gestort kapitaal", "amount": 100000},
        "BEivOvr": {"name": "Overige reserves", "amount": 285000},
        "BEivWin": {"name": "Onverdeeld resultaat", "amount": 89400},
        "BLasLls": {"name": "Langlopende schulden", "amount": 180000},
        "BSchCreHan": {"name": "Crediteuren", "amount": 78000},
        "BSchBelBtw": {"name": "BTW schuld", "amount": 45000},
        "BSchBelLhe": {"name": "Loonheffing", "amount": 18000},
        "BSchOvrOvs": {"name": "Overige schulden", "amount": 53100},
    }
}

# BTW/ICP Data
BTW_DATA = {
    "periodes": [
        {"periode": "Q4 2024", "status": "Open", "deadline": "2025-01-31", "btw_verschuldigd": 45000, "btw_voorbelasting": 28750, "btw_af_te_dragen": 16250, "icp_leveringen": 12500, "icp_verwervingen": 8200},
        {"periode": "Q3 2024", "status": "Ingediend", "deadline": "2024-10-31", "btw_verschuldigd": 52000, "btw_voorbelasting": 31200, "btw_af_te_dragen": 20800, "icp_leveringen": 15800, "icp_verwervingen": 6500},
        {"periode": "Q2 2024", "status": "Betaald", "deadline": "2024-07-31", "btw_verschuldigd": 48500, "btw_voorbelasting": 29100, "btw_af_te_dragen": 19400, "icp_leveringen": 9200, "icp_verwervingen": 11000},
        {"periode": "Q1 2024", "status": "Betaald", "deadline": "2024-04-30", "btw_verschuldigd": 41200, "btw_voorbelasting": 24720, "btw_af_te_dragen": 16480, "icp_leveringen": 7500, "icp_verwervingen": 5800},
    ],
    "icp_relaties": [
        {"land": "🇩🇪 Duitsland", "btw_nr": "DE123456789", "bedrijf": "Bauhaus GmbH", "leveringen": 8500, "verwervingen": 4200},
        {"land": "🇧🇪 België", "btw_nr": "BE0123456789", "bedrijf": "Bouwmaterialen BVBA", "leveringen": 3000, "verwervingen": 2500},
        {"land": "🇫🇷 Frankrijk", "btw_nr": "FR12345678901", "bedrijf": "Construction SARL", "leveringen": 1000, "verwervingen": 1500},
    ]
}

# Odoo Boekhouding Sync Data
ODOO_SYNC_STATUS = {
    "modules": [
        {"naam": "Bankrekeningen", "status": "warning", "laatste_sync": "2 uur geleden", "details": "ING synchronisatie mislukt", "items_pending": 3},
        {"naam": "Verkoopfacturen", "status": "ok", "laatste_sync": "15 min geleden", "details": "Volledig gesynchroniseerd", "items_pending": 0},
        {"naam": "Inkoopfacturen", "status": "ok", "laatste_sync": "15 min geleden", "details": "Volledig gesynchroniseerd", "items_pending": 0},
        {"naam": "Grootboek", "status": "ok", "laatste_sync": "15 min geleden", "details": "Alle mutaties verwerkt", "items_pending": 0},
        {"naam": "BTW Module", "status": "ok", "laatste_sync": "1 dag geleden", "details": "Q4 aangifte in voorbereiding", "items_pending": 1},
        {"naam": "Salarisadministratie", "status": "ok", "laatste_sync": "3 dagen geleden", "details": "December loonrun verwerkt", "items_pending": 0},
    ],
    "ai_booking_stats": {
        "totaal_mutaties": 1247,
        "automatisch_geboekt": 1089,
        "handmatig_nodig": 158,
        "success_rate": 87.3
    }
}

# Openstaande bankmutaties (AI kon niet boeken)
OPEN_BANK_MUTATIONS = [
    {"id": "BM-001", "datum": "2025-01-28", "bank": "ING", "bedrag": 2450.00, "omschrijving": "SEPA OVERBOEKING - Ref: INV-2024-0892", "reden": "Geen matchende factuur gevonden", "suggestie": "Mogelijk betaling klant Janssen BV (factuur ontbreekt)"},
    {"id": "BM-002", "datum": "2025-01-27", "bank": "ING", "bedrag": -875.50, "omschrijving": "IDEAL BETALING - Webshop Order #4521", "reden": "Onbekende grootboekrekening", "suggestie": "Boeken op 8400 - Kantoorkosten?"},
    {"id": "BM-003", "datum": "2025-01-26", "bank": "ABN AMRO", "bedrag": -15000.00, "omschrijving": "Aflossing lening ABN", "reden": "Lening niet gekoppeld in Odoo", "suggestie": "Koppel lening #LN-2022-001 in Odoo"},
    {"id": "BM-004", "datum": "2025-01-25", "bank": "ING", "bedrag": 125.00, "omschrijving": "Terugboeking PIN transactie", "reden": "Oorspronkelijke transactie niet gevonden", "suggestie": "Handmatig onderzoeken"},
    {"id": "BM-005", "datum": "2025-01-24", "bank": "ING", "bedrag": -3200.00, "omschrijving": "Automatische incasso Belastingdienst", "reden": "Meerdere belastingsoorten mogelijk", "suggestie": "BTW of Loonheffing? Check beschikking"},
]

# Investeringen & Financiering Data
INVESTERINGEN_DATA = {
    "activa": [
        {"categorie": "Terreinen", "rgs": "BIvaMatTer", "aanschaf": 125000, "afschrijving_cum": 0, "boekwaarde": 125000, "methode": "Geen (grond)", "restwaarde": 125000, "levensduur": None},
        {"categorie": "Bedrijfsgebouwen", "rgs": "BIvaMatBeg", "aanschaf": 450000, "afschrijving_cum": 165000, "boekwaarde": 285000, "methode": "Lineair", "restwaarde": 100000, "levensduur": 30},
        {"categorie": "Machines & installaties", "rgs": "BIvaMatMae", "aanschaf": 180000, "afschrijving_cum": 85000, "boekwaarde": 95000, "methode": "Lineair", "restwaarde": 10000, "levensduur": 10},
        {"categorie": "Transportmiddelen", "rgs": "BIvaMatTrm", "aanschaf": 125000, "afschrijving_cum": 57000, "boekwaarde": 68000, "methode": "Lineair", "restwaarde": 15000, "levensduur": 5},
        {"categorie": "Inventaris", "rgs": "BIvaMatInv", "aanschaf": 45000, "afschrijving_cum": 32000, "boekwaarde": 13000, "methode": "Lineair", "restwaarde": 0, "levensduur": 5},
        {"categorie": "ICT Hardware", "rgs": "BIvaMatIct", "aanschaf": 28000, "afschrijving_cum": 19000, "boekwaarde": 9000, "methode": "Lineair", "restwaarde": 0, "levensduur": 3},
    ],
    "afschrijvingen_jaar": [
        {"categorie": "Bedrijfsgebouwen", "2022": 11667, "2023": 11667, "2024": 11667, "2025_budget": 11667},
        {"categorie": "Machines & installaties", "2022": 17000, "2023": 17000, "2024": 17000, "2025_budget": 17000},
        {"categorie": "Transportmiddelen", "2022": 22000, "2023": 22000, "2024": 22000, "2025_budget": 22000},
        {"categorie": "Inventaris", "2022": 9000, "2023": 9000, "2024": 9000, "2025_budget": 5000},
        {"categorie": "ICT Hardware", "2022": 9333, "2023": 9333, "2024": 9333, "2025_budget": 0},
    ],
    "geplande_investeringen": [
        {"omschrijving": "Nieuwe bedrijfswagen", "bedrag": 45000, "datum": "Q2 2025", "status": "Goedgekeurd"},
        {"omschrijving": "Server upgrade", "bedrag": 12000, "datum": "Q1 2025", "status": "In bestelling"},
        {"omschrijving": "Productielijn uitbreiding", "bedrag": 85000, "datum": "Q3 2025", "status": "In overweging"},
    ]
}

FINANCIERING_DATA = {
    "leningen_ontvangen": [
        {"id": "LN-2022-001", "verstrekker": "ABN AMRO Bank", "type": "Hypothecaire lening", "hoofdsom": 350000, "openstaand": 280000, "rente": 3.2, "aflossing_maand": 2500, "einddatum": "2037-06-01", "onderpand": "Bedrijfspand"},
        {"id": "LN-2023-001", "verstrekker": "Rabobank", "type": "Bedrijfskrediet", "hoofdsom": 75000, "openstaand": 52000, "rente": 4.8, "aflossing_maand": 1800, "einddatum": "2026-12-01", "onderpand": "Geen"},
        {"id": "LN-2024-001", "verstrekker": "Qredits", "type": "Investeringskrediet", "hoofdsom": 25000, "openstaand": 22500, "rente": 5.5, "aflossing_maand": 850, "einddatum": "2027-03-01", "onderpand": "Geen"},
    ],
    "leningen_verstrekt": [
        {"id": "LV-2023-001", "debiteur": "Dochter BV", "type": "Rekening-courant", "hoofdsom": 50000, "openstaand": 35000, "rente": 2.0, "aflossing_maand": 1500, "einddatum": "2025-12-01"},
    ],
    "kredietfaciliteiten": [
        {"bank": "ING", "type": "Rekening-courant krediet", "limiet": 100000, "benut": 15000, "beschikbaar": 85000},
        {"bank": "ABN AMRO", "type": "Garantiekrediet", "limiet": 50000, "benut": 12000, "beschikbaar": 38000},
    ],
    "aflossingsschema_2025": [
        {"maand": "Jan", "abn_hypo": 2500, "rabo_krediet": 1800, "qredits": 850, "totaal": 5150},
        {"maand": "Feb", "abn_hypo": 2500, "rabo_krediet": 1800, "qredits": 850, "totaal": 5150},
        {"maand": "Mar", "abn_hypo": 2500, "rabo_krediet": 1800, "qredits": 850, "totaal": 5150},
        {"maand": "Apr", "abn_hypo": 2500, "rabo_krediet": 1800, "qredits": 850, "totaal": 5150},
        {"maand": "Mei", "abn_hypo": 2500, "rabo_krediet": 1800, "qredits": 850, "totaal": 5150},
        {"maand": "Jun", "abn_hypo": 2500, "rabo_krediet": 1800, "qredits": 850, "totaal": 5150},
        {"maand": "Jul", "abn_hypo": 2500, "rabo_krediet": 1800, "qredits": 850, "totaal": 5150},
        {"maand": "Aug", "abn_hypo": 2500, "rabo_krediet": 1800, "qredits": 850, "totaal": 5150},
        {"maand": "Sep", "abn_hypo": 2500, "rabo_krediet": 1800, "qredits": 850, "totaal": 5150},
        {"maand": "Okt", "abn_hypo": 2500, "rabo_krediet": 1800, "qredits": 850, "totaal": 5150},
        {"maand": "Nov", "abn_hypo": 2500, "rabo_krediet": 1800, "qredits": 850, "totaal": 5150},
        {"maand": "Dec", "abn_hypo": 2500, "rabo_krediet": 1800, "qredits": 850, "totaal": 5150},
    ]
}

# Vennootschapsbelasting Data
VPB_DATA = {
    "boekjaar": "2024",
    "fiscale_winst": 89400,
    "tarieven": {
        "schijf_1": {"grens": 200000, "percentage": 19},
        "schijf_2": {"grens": None, "percentage": 25.8}
    },
    "berekening": {
        "winst_voor_vpb": 89400,
        "kleinschaligheidsinvesteringsaftrek": 5200,
        "overige_fiscale_correcties": -2100,
        "belastbare_winst": 82100,
        "vpb_schijf_1": 15599,  # 82100 * 19%
        "vpb_totaal": 15599
    },
    "voorlopige_aanslagen": [
        {"jaar": "2024", "bedrag": 14000, "status": "Betaald", "betaaldatum": "2024-06-15"},
        {"jaar": "2024", "bedrag": 14000, "status": "Open", "betaaldatum": "2025-02-28"},
    ],
    "deadlines": [
        {"omschrijving": "Aangifte Vpb 2024", "deadline": "2025-06-01", "status": "Nog in te dienen"},
        {"omschrijving": "Betaling voorlopige aanslag 2024", "deadline": "2025-02-28", "status": "Open"},
        {"omschrijving": "Definitieve aanslag 2023", "deadline": "Ontvangen", "status": "Akkoord"},
    ]
}

# ============================================
# HELPER FUNCTIONS
# ============================================

def format_currency(amount):
    """Format number as Dutch currency"""
    if amount >= 0:
        return f"€ {amount:,.0f}".replace(",", ".")
    else:
        return f"€ {amount:,.0f}".replace(",", ".")

def get_client_by_id(client_id):
    """Get client data by ID"""
    for client in DEMO_CLIENTS:
        if client['id'] == client_id:
            return client
    return DEMO_CLIENTS[0]  # Default to first client

# ============================================
# SIDEBAR NAVIGATION
# ============================================

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #14b8a6; font-size: 32px; margin: 0;">NOVA</h1>
        <p style="color: #64748b; font-size: 12px; margin: 5px 0 0 0;">Platform Demo</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Portal Toggle
    st.markdown("**PORTAL**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏢 Kantoor", key="portal_kantoor", use_container_width=True, 
                     type="primary" if st.session_state.portal_mode == 'kantoor' else "secondary"):
            st.session_state.portal_mode = 'kantoor'
            st.session_state.current_view = 'dashboard'
            st.session_state.selected_client = None
            st.rerun()
    with col2:
        if st.button("👤 Klant", key="portal_klant", use_container_width=True,
                     type="primary" if st.session_state.portal_mode == 'klant' else "secondary"):
            st.session_state.portal_mode = 'klant'
            st.session_state.current_view = 'dashboard'
            st.rerun()
    
    st.markdown("---")
    
    # Different navigation based on portal mode
    if st.session_state.portal_mode == 'kantoor':
        # KANTOOR PORTAL NAVIGATION
        st.markdown("**MISSION CONTROL**")
        
        kantoor_nav = {
            "🎯 Overzicht": "dashboard",
            "👥 Klantenportfolio": "clients",
            "📋 Teamworkload": "team",
            "🚨 Alerts & Acties": "alerts",
            "🤖 AI Agents Overzicht": "agents",
        }
        
        for label, view in kantoor_nav.items():
            if st.button(label, key=f"knav_{view}", use_container_width=True):
                st.session_state.current_view = view
        
        # Quick client lookup
        st.markdown("---")
        st.markdown("**KLANT ZOEKEN**")
        client_names = [c['name'] for c in DEMO_CLIENTS]
        selected = st.selectbox("Selecteer klant", [""] + client_names, key="client_lookup", label_visibility="collapsed")
        if selected:
            for c in DEMO_CLIENTS:
                if c['name'] == selected:
                    if st.button(f"📂 Naar {c['name']}", key="goto_client", use_container_width=True):
                        st.session_state.selected_client = c['id']
                        st.session_state.portal_mode = 'klant'
                        st.session_state.current_view = 'dashboard'
                        st.rerun()
    
    else:
        # KLANT PORTAL NAVIGATION
        # Show selected client info
        if st.session_state.selected_client:
            client = get_client_by_id(st.session_state.selected_client)
        else:
            client = DEMO_CLIENTS[0]
            st.session_state.selected_client = client['id']
        
        st.markdown(f"""
        <div style="background: #f1f5f9; padding: 16px; border-radius: 12px; margin-bottom: 20px;">
            <p style="color: #64748b; font-size: 11px; margin: 0;">KLANT</p>
            <p style="color: #0f172a; font-weight: 600; margin: 4px 0;">{client['name']}</p>
            <p style="color: #64748b; font-size: 12px; margin: 0;">{client['contact']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Back to kantoor button
        if st.button("← Terug naar Kantoor", key="back_to_kantoor", use_container_width=True):
            st.session_state.portal_mode = 'kantoor'
            st.session_state.current_view = 'dashboard'
            st.rerun()
        
        st.markdown("---")
        
        # Client navigation
        st.markdown("**NAVIGATIE**")
        
        nav_options = {
            "🎯 Dashboard": "dashboard",
            "📄 Facturen": "invoices",
            "📊 Winst & Verlies": "pnl",
            "⚖️ Balans": "balance",
            "🏗️ Investeringen": "investments",
            "🤖 AI Agents": "agents",
            "💬 Chat met ALEX": "chat",
            "📈 Forecasting": "forecast"
        }
        
        for label, view in nav_options.items():
            if st.button(label, key=f"cnav_{view}", use_container_width=True):
                st.session_state.current_view = view
        
        # Odoo section
        st.markdown("---")
        st.markdown("""<span class="odoo-badge">ODOO INTEGRATIE</span>""", unsafe_allow_html=True)
        st.markdown("")
        
        odoo_options = {
            "📚 Boekhouding": "odoo_accounting",
            "🎯 CRM Pipeline": "crm",
            "📦 Inkoop (PO's)": "purchase",
            "👥 HR & Personeel": "hr",
        }
        
        for label, view in odoo_options.items():
            if st.button(label, key=f"onav_{view}", use_container_width=True):
                st.session_state.current_view = view
        
        # Fiscaal section
        st.markdown("---")
        st.markdown("**📋 FISCAAL**")
        
        fiscaal_options = {
            "🧾 BTW & ICP": "btw",
            "🏛️ Vennootschapsbelasting": "vpb",
        }
        
        for label, view in fiscaal_options.items():
            if st.button(label, key=f"fnav_{view}", use_container_width=True):
                st.session_state.current_view = view

# ============================================
# MAIN CONTENT - KANTOOR PORTAL
# ============================================

if st.session_state.portal_mode == 'kantoor':
    
    if st.session_state.current_view == 'dashboard':
        # KANTOOR DASHBOARD - MISSION CONTROL
        st.title("🏢 Mission Control")
        st.markdown(f"**{FIRM_INFO['name']}** | {datetime.now().strftime('%d %B %Y')}")
        
        # Firm-wide KPIs
        st.markdown("### 📊 Kantoor KPI's")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Actieve Klanten", "45", "+3 dit kwartaal")
        with col2:
            total_omzet = sum(c['omzet_ytd'] for c in DEMO_CLIENTS)
            st.metric("Totale Omzet Portfolio", format_currency(total_omzet), "+8.2%")
        with col3:
            st.metric("Openstaande Facturen", format_currency(sum(c['openstaand'] for c in DEMO_CLIENTS)), "")
        with col4:
            st.metric("Declarabiliteit", "78%", "+5%")
        with col5:
            st.metric("AI Verwerkingen Vandaag", "246", "")
        
        st.markdown("---")
        
        # Two columns: Alerts and Quick Overview
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.markdown("### 🚨 Actieve Alerts")
            for alert in FIRM_ALERTS[:4]:
                alert_class = "alert-card-red" if alert['type'] == 'urgent' else "alert-card"
                icon = "🔴" if alert['type'] == 'urgent' else "🟡" if alert['type'] == 'warning' else "🔵"
                st.markdown(f"""
                <div class="{alert_class}">
                    <strong>{icon} {alert['client']}</strong><br>
                    <span style="color: #64748b;">{alert['message']}</span><br>
                    <small style="color: #94a3b8;">{alert['time']}</small>
                </div>
                """, unsafe_allow_html=True)
        
        with col_right:
            st.markdown("### 📈 Portfolio Gezondheid")
            # Status distribution
            green = len([c for c in DEMO_CLIENTS if c['status'] == 'green'])
            yellow = len([c for c in DEMO_CLIENTS if c['status'] == 'yellow'])
            red = len([c for c in DEMO_CLIENTS if c['status'] == 'red'])
            
            fig = go.Figure(data=[go.Pie(
                labels=['Gezond', 'Aandacht nodig', 'Kritiek'],
                values=[green, yellow, red],
                hole=0.6,
                marker_colors=['#10b981', '#f59e0b', '#ef4444']
            )])
            fig.update_layout(
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.1),
                margin=dict(t=20, b=20, l=20, r=20),
                height=250
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Client Overview Table
        st.markdown("### 👥 Klanten Overzicht (Top 8)")
        
        for client in DEMO_CLIENTS:
            status_color = {"green": "#10b981", "yellow": "#f59e0b", "red": "#ef4444"}[client['status']]
            growth = ((client['omzet_ytd'] / client['omzet_prev']) - 1) * 100 if client['omzet_prev'] > 0 else 0
            growth_str = f"+{growth:.1f}%" if growth >= 0 else f"{growth:.1f}%"
            growth_color = "#10b981" if growth >= 0 else "#ef4444"
            
            col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 2, 2, 1])
            
            with col1:
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="width: 12px; height: 12px; border-radius: 50%; background: {status_color};"></div>
                    <div>
                        <strong>{client['name']}</strong><br>
                        <small style="color: #64748b;">{client['sector']}</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"**{format_currency(client['omzet_ytd'])}**<br><small style='color: {growth_color};'>{growth_str}</small>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"**{format_currency(client['winst_ytd'])}**<br><small style='color: #64748b;'>Resultaat</small>", unsafe_allow_html=True)
            with col4:
                st.markdown(f"**{format_currency(client['openstaand'])}**<br><small style='color: #64748b;'>Openstaand</small>", unsafe_allow_html=True)
            with col5:
                st.markdown(f"**{client['accountant']}**<br><small style='color: #64748b;'>{client['last_activity']}</small>", unsafe_allow_html=True)
            with col6:
                if st.button("→", key=f"goto_{client['id']}", help=f"Naar {client['name']}"):
                    st.session_state.selected_client = client['id']
                    st.session_state.portal_mode = 'klant'
                    st.session_state.current_view = 'dashboard'
                    st.rerun()
            
            st.markdown("<hr style='margin: 8px 0; border: none; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
    
    elif st.session_state.current_view == 'clients':
        # KLANTENPORTFOLIO
        st.title("👥 Klantenportfolio")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Status", ["Alle", "Gezond", "Aandacht nodig", "Kritiek"])
        with col2:
            sector_filter = st.selectbox("Sector", ["Alle"] + list(set(c['sector'] for c in DEMO_CLIENTS)))
        with col3:
            accountant_filter = st.selectbox("Accountant", ["Alle"] + list(set(c['accountant'] for c in DEMO_CLIENTS)))
        
        # Filter clients
        filtered_clients = DEMO_CLIENTS.copy()
        if status_filter != "Alle":
            status_map = {"Gezond": "green", "Aandacht nodig": "yellow", "Kritiek": "red"}
            filtered_clients = [c for c in filtered_clients if c['status'] == status_map.get(status_filter)]
        if sector_filter != "Alle":
            filtered_clients = [c for c in filtered_clients if c['sector'] == sector_filter]
        if accountant_filter != "Alle":
            filtered_clients = [c for c in filtered_clients if c['accountant'] == accountant_filter]
        
        st.markdown(f"**{len(filtered_clients)} klanten gevonden**")
        st.markdown("---")
        
        # Client cards
        for client in filtered_clients:
            status_class = f"client-status-{client['status']}"
            alert_html = ""
            if client['alerts']:
                alert_html = f"<br><span style='color: #f59e0b; font-size: 12px;'>⚠️ {len(client['alerts'])} alert(s)</span>"
            
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                <div class="client-card {status_class}">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <h3 style="margin: 0 0 8px 0;">{client['name']}</h3>
                            <p style="color: #64748b; margin: 0;">{client['contact']} | {client['sector']}</p>
                            <p style="color: #64748b; font-size: 12px; margin: 4px 0 0 0;">Accountant: {client['accountant']}{alert_html}</p>
                        </div>
                        <div style="text-align: right;">
                            <p style="font-size: 24px; font-weight: 700; margin: 0; color: #0f172a;">{format_currency(client['omzet_ytd'])}</p>
                            <p style="color: #64748b; font-size: 12px; margin: 0;">Omzet YTD</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("Bekijk →", key=f"view_{client['id']}", use_container_width=True):
                    st.session_state.selected_client = client['id']
                    st.session_state.portal_mode = 'klant'
                    st.session_state.current_view = 'dashboard'
                    st.rerun()
    
    elif st.session_state.current_view == 'team':
        # TEAM WORKLOAD
        st.title("📋 Team Workload")
        st.markdown(f"**{FIRM_INFO['name']}** | {len(TEAM_MEMBERS)} teamleden")
        
        st.markdown("---")
        
        for member in TEAM_MEMBERS:
            workload_color = "#10b981" if member['workload'] < 80 else "#f59e0b" if member['workload'] < 90 else "#ef4444"
            
            col1, col2, col3, col4 = st.columns([2, 1, 3, 1])
            
            with col1:
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 32px;">{member['avatar']}</span>
                    <div>
                        <strong>{member['name']}</strong><br>
                        <small style="color: #64748b;">{member['role']}</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.metric("Klanten", member['clients'])
            
            with col3:
                st.progress(member['workload'] / 100)
                st.markdown(f"<small style='color: {workload_color};'>{member['workload']}% bezetting</small>", unsafe_allow_html=True)
            
            with col4:
                if member['workload'] >= 90:
                    st.warning("Overbelast")
                elif member['workload'] >= 80:
                    st.info("Druk")
                else:
                    st.success("OK")
            
            st.markdown("---")
        
        # Team stats
        st.markdown("### 📊 Team Statistieken")
        col1, col2, col3 = st.columns(3)
        with col1:
            avg_workload = sum(m['workload'] for m in TEAM_MEMBERS) / len(TEAM_MEMBERS)
            st.metric("Gemiddelde Bezetting", f"{avg_workload:.0f}%")
        with col2:
            total_clients = sum(m['clients'] for m in TEAM_MEMBERS)
            st.metric("Totaal Klanten", total_clients)
        with col3:
            overloaded = len([m for m in TEAM_MEMBERS if m['workload'] >= 90])
            st.metric("Teamleden Overbelast", overloaded)
    
    elif st.session_state.current_view == 'alerts':
        # ALERTS & ACTIES
        st.title("🚨 Alerts & Acties")
        
        # Alert summary
        urgent = len([a for a in FIRM_ALERTS if a['type'] == 'urgent'])
        warning = len([a for a in FIRM_ALERTS if a['type'] == 'warning'])
        info = len([a for a in FIRM_ALERTS if a['type'] == 'info'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🔴 Urgent", urgent)
        with col2:
            st.metric("🟡 Waarschuwing", warning)
        with col3:
            st.metric("🔵 Informatief", info)
        
        st.markdown("---")
        
        # Alert list
        for alert in FIRM_ALERTS:
            alert_class = "alert-card-red" if alert['type'] == 'urgent' else "alert-card"
            icon = "🔴" if alert['type'] == 'urgent' else "🟡" if alert['type'] == 'warning' else "🔵"
            
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                <div class="{alert_class}">
                    <strong>{icon} {alert['client']}</strong><br>
                    <span>{alert['message']}</span><br>
                    <small style="color: #94a3b8;">{alert['time']}</small>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                # Find the client and go to their dashboard
                for c in DEMO_CLIENTS:
                    if c['name'] == alert['client']:
                        if st.button("Bekijk →", key=f"alert_{alert['client']}_{alert['time']}", use_container_width=True):
                            st.session_state.selected_client = c['id']
                            st.session_state.portal_mode = 'klant'
                            st.session_state.current_view = 'dashboard'
                            st.rerun()
                        break
    
    elif st.session_state.current_view == 'agents':
        # AI AGENTS OVERZICHT (KANTOOR LEVEL)
        st.title("🤖 AI Agents - Kantoor Overzicht")
        st.markdown("Alle AI-agents actief over het hele klantenportfolio")
        
        # Summary stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_processed = sum(a['processed_today'] for a in AI_AGENTS.values())
            st.metric("Totaal Verwerkt Vandaag", total_processed)
        with col2:
            avg_accuracy = sum(a['accuracy'] for a in AI_AGENTS.values()) / len(AI_AGENTS)
            st.metric("Gemiddelde Nauwkeurigheid", f"{avg_accuracy:.1f}%")
        with col3:
            st.metric("Actieve Agents", len(AI_AGENTS))
        with col4:
            st.metric("Besparing (geschat)", "€ 12.400/maand")
        
        st.markdown("---")
        
        for name, agent in AI_AGENTS.items():
            st.markdown(f"""
            <div class="agent-card agent-{name.lower()}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="margin: 0; color: {agent['color']};">{name}</h3>
                        <p style="color: #64748b; margin: 4px 0;">{agent['full_name']}</p>
                        <p style="margin: 4px 0;">{agent['description']}</p>
                    </div>
                    <div style="text-align: right;">
                        <p style="font-size: 28px; font-weight: 700; margin: 0;">{agent['processed_today']}</p>
                        <p style="color: #64748b; font-size: 12px;">verwerkt vandaag</p>
                        <p style="color: #10b981; font-weight: 600;">{agent['accuracy']}% nauwkeurig</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ============================================
# MAIN CONTENT - KLANT PORTAL
# ============================================

else:  # portal_mode == 'klant'
    
    # Get current client
    if st.session_state.selected_client:
        current_client = get_client_by_id(st.session_state.selected_client)
    else:
        current_client = DEMO_CLIENTS[0]
        st.session_state.selected_client = current_client['id']
    
    if st.session_state.current_view == 'dashboard':
        st.title("🎯 Mijn Financiële Cockpit")
        st.markdown(f"Welkom terug, **{current_client['contact']}** | {datetime.now().strftime('%d %B %Y')}")
        
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Omzet YTD",
                value=format_currency(current_client['omzet_ytd']),
                delta=f"+{((current_client['omzet_ytd']/current_client['omzet_prev'])-1)*100:.1f}% vs vorig jaar"
            )
        
        with col2:
            marge = (current_client['winst_ytd'] / current_client['omzet_ytd'] * 100) if current_client['omzet_ytd'] > 0 else 0
            st.metric(
                label="Winstmarge",
                value=f"{marge:.1f}%",
                delta="+2.1pp"
            )
        
        with col3:
            st.metric(
                label="Openstaande facturen",
                value=format_currency(current_client['openstaand']),
                delta="-€23.500 deze week"
            )
        
        with col4:
            st.metric(
                label="Cashflow prognose (30d)",
                value="€ 89.200",
                delta="Positief"
            )
        
        # Charts row
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Omzet Verloop")
            months = ['Jan', 'Feb', 'Mrt', 'Apr', 'Mei', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dec']
            omzet_data = [45000, 52000, 48000, 61000, 55000, 58000, 62000, 59000, 67000, 71000, 68000, 66000]
            
            fig = px.line(x=months, y=omzet_data, markers=True)
            fig.update_traces(line_color='#14b8a6', line_width=3)
            fig.update_layout(
                xaxis_title="", yaxis_title="",
                margin=dict(t=20, b=20),
                height=250
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 💰 Kosten Verdeling")
            kosten_data = {
                'Categorie': ['Personeel', 'Materialen', 'Huisvesting', 'Overig'],
                'Bedrag': [240000, 185000, 44500, 53300]
            }
            fig = px.pie(kosten_data, values='Bedrag', names='Categorie', hole=0.5)
            fig.update_traces(marker_colors=['#14b8a6', '#8b5cf6', '#f59e0b', '#64748b'])
            fig.update_layout(margin=dict(t=20, b=20), height=250)
            st.plotly_chart(fig, use_container_width=True)
        
        # AI Insights
        st.markdown("---")
        st.markdown("### 🤖 AI Inzichten")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="agent-card agent-sage">
                <strong style="color: #f59e0b;">💡 SAGE - Fiscaal Tip</strong>
                <p style="margin: 8px 0 0 0;">Overweeg de energie-investeringsaftrek (EIA) voor uw nieuwe machines. Potentiële besparing: €12.500</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="agent-card agent-luna">
                <strong style="color: #3b82f6;">📊 LUNA - Prognose</strong>
                <p style="margin: 8px 0 0 0;">Op basis van huidige trend: Q1 omzet verwacht €185.000 (+8% YoY)</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="agent-card agent-aria">
                <strong style="color: #14b8a6;">📄 ARIA - Facturen</strong>
                <p style="margin: 8px 0 0 0;">4 nieuwe facturen verwerkt. 1 wacht op uw goedkeuring.</p>
            </div>
            """, unsafe_allow_html=True)

    elif st.session_state.current_view == 'invoices':
        st.title("📄 Factuurverwerking")
        st.markdown(f"**{current_client['name']}** | Powered by ARIA")
        
        # Upload section
        st.markdown("### 📤 Factuur Uploaden")
        uploaded_file = st.file_uploader("Sleep een factuur hierheen of klik om te uploaden", type=['pdf', 'jpg', 'png'])
        
        if uploaded_file:
            with st.spinner("🤖 ARIA analyseert de factuur..."):
                import time
                time.sleep(2)
            
            st.success("✅ Factuur succesvol geanalyseerd!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Gedetecteerde gegevens:**")
                st.markdown("""
                - **Leverancier:** Bouwmaterialen Jansen B.V.
                - **Factuurnummer:** F2024-009
                - **Bedrag:** € 3.250,00
                - **BTW:** € 682,50
                - **RGS Code:** WIkworGro (Grond- en hulpstoffen)
                """)
            with col2:
                st.markdown("**Vertrouwensscore:**")
                st.progress(0.96)
                st.markdown("96% - Hoge betrouwbaarheid")
                
                if st.button("✅ Goedkeuren en verwerken", type="primary"):
                    st.success("Factuur verwerkt en geboekt!")
        
        st.markdown("---")
        
        # Invoice tabs
        st.markdown("### 📋 Factuuroverzicht")
        tab1, tab2, tab3 = st.tabs(["🆕 Nieuw (4)", "⏳ Review (1)", "✅ Verwerkt (3)"])
        
        def show_invoice_list(invoices, tab_prefix):
            for inv in invoices:
                col1, col2, col3, col4, col5 = st.columns([2, 3, 2, 2, 1])
                with col1:
                    st.markdown(f"**{inv['id']}**")
                with col2:
                    st.markdown(inv['supplier'])
                with col3:
                    st.markdown(f"€ {inv['amount']:,.2f}")
                with col4:
                    st.markdown(inv['date'])
                with col5:
                    if st.button("👁️", key=f"{tab_prefix}_view_{inv['id']}"):
                        st.session_state.selected_invoice = inv
                st.markdown("---")
        
        with tab1:
            show_invoice_list([i for i in DEMO_INVOICES if i['status'] == 'nieuw'], "new")
        with tab2:
            show_invoice_list([i for i in DEMO_INVOICES if i['status'] == 'wacht op review'], "review")
        with tab3:
            show_invoice_list([i for i in DEMO_INVOICES if i['status'] == 'verwerkt'], "processed")

    elif st.session_state.current_view == 'pnl':
        st.title("📊 Winst & Verlies")
        st.markdown(f"**{current_client['name']}** | Periode: Januari 2024 YTD")
        
        # Create P&L statement
        st.markdown("""
        <div class="rgs-header">
            <span>RGS Code</span>
            <span style="float: right;">Bedrag</span>
        </div>
        """, unsafe_allow_html=True)
        
        categories = {}
        for code, data in RGS_WV.items():
            cat = data['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append((code, data))
        
        total = 0
        for category, items in categories.items():
            st.markdown(f"**{category}**")
            cat_total = 0
            for code, data in items:
                st.markdown(f"""
                <div class="rgs-row">
                    <span>{data['name']} <small style="color: #94a3b8;">({code})</small></span>
                    <span style="float: right;">{format_currency(data['amount'])}</span>
                </div>
                """, unsafe_allow_html=True)
                cat_total += data['amount']
            st.markdown(f"""
            <div class="rgs-row" style="background: #f1f5f9; font-weight: 600;">
                <span>Subtotaal {category}</span>
                <span style="float: right;">{format_currency(cat_total)}</span>
            </div>
            """, unsafe_allow_html=True)
            total += cat_total
            st.markdown("")
        
        st.markdown(f"""
        <div class="rgs-row rgs-total" style="background: #0f172a; color: white; border-radius: 0 0 12px 12px;">
            <span style="font-size: 18px;">NETTO RESULTAAT</span>
            <span style="float: right; font-size: 18px;">{format_currency(total)}</span>
        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.current_view == 'balance':
        st.title("⚖️ Balans")
        st.markdown(f"**{current_client['name']}** | Per 31 januari 2024")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ACTIVA")
            st.markdown('<div class="rgs-header">Omschrijving</div>', unsafe_allow_html=True)
            
            total_activa = 0
            for code, data in RGS_BALANS['activa'].items():
                st.markdown(f"""
                <div class="rgs-row">
                    <span>{data['name']} <small style="color: #94a3b8;">({code})</small></span>
                    <span style="float: right;">{format_currency(data['amount'])}</span>
                </div>
                """, unsafe_allow_html=True)
                total_activa += data['amount']
            
            st.markdown(f"""
            <div class="rgs-row rgs-total" style="background: #0f172a; color: white;">
                <span>TOTAAL ACTIVA</span>
                <span style="float: right;">{format_currency(total_activa)}</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### PASSIVA")
            st.markdown('<div class="rgs-header">Omschrijving</div>', unsafe_allow_html=True)
            
            total_passiva = 0
            for code, data in RGS_BALANS['passiva'].items():
                st.markdown(f"""
                <div class="rgs-row">
                    <span>{data['name']} <small style="color: #94a3b8;">({code})</small></span>
                    <span style="float: right;">{format_currency(data['amount'])}</span>
                </div>
                """, unsafe_allow_html=True)
                total_passiva += data['amount']
            
            st.markdown(f"""
            <div class="rgs-row rgs-total" style="background: #0f172a; color: white;">
                <span>TOTAAL PASSIVA</span>
                <span style="float: right;">{format_currency(total_passiva)}</span>
            </div>
            """, unsafe_allow_html=True)

    elif st.session_state.current_view == 'agents':
        st.title("🤖 AI Agents")
        st.markdown(f"**{current_client['name']}** | Jouw digitale financiële team")
        
        for name, agent in AI_AGENTS.items():
            st.markdown(f"""
            <div class="agent-card agent-{name.lower()}">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <h3 style="margin: 0; color: {agent['color']};">{name}</h3>
                        <p style="color: #64748b; font-size: 12px; margin: 4px 0;">{agent['full_name']}</p>
                        <p style="margin: 8px 0 0 0;"><strong>{agent['role']}</strong></p>
                        <p style="color: #64748b;">{agent['description']}</p>
                        <p style="color: #714B67; font-size: 12px;"><span class="odoo-badge">Odoo: {agent['odoo_link']}</span></p>
                    </div>
                    <div style="text-align: right;">
                        <span class="status-active">{agent['status']}</span>
                        <p style="margin: 12px 0 0 0; font-size: 24px; font-weight: 700;">{agent['processed_today']}</p>
                        <p style="color: #64748b; font-size: 12px;">verwerkt vandaag</p>
                        <p style="color: #10b981; font-weight: 500;">{agent['accuracy']}% nauwkeurig</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    elif st.session_state.current_view == 'chat':
        st.title("💬 Chat met ALEX")
        st.markdown(f"**{current_client['name']}** | Uw persoonlijke financieel adviseur")
        
        # Chat interface
        chat_container = st.container()
        
        # Welcome message
        with chat_container:
            st.markdown("""
            <div style="background: #f1f5f9; padding: 16px; border-radius: 12px; margin-bottom: 16px;">
                <strong style="color: #ec4899;">🤖 ALEX</strong>
                <p style="margin: 8px 0 0 0;">Goedemiddag! Ik ben ALEX, uw AI-adviseur. Ik kan u helpen met vragen over uw financiën, facturen, belastingen en meer. Wat kan ik voor u doen?</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show chat history
            for msg in st.session_state.chat_history:
                if msg['role'] == 'user':
                    st.markdown(f"""
                    <div style="background: #14b8a6; color: white; padding: 16px; border-radius: 12px; margin: 8px 0; margin-left: 20%;">
                        <p style="margin: 0;">{msg['content']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: #f1f5f9; padding: 16px; border-radius: 12px; margin: 8px 0; margin-right: 20%;">
                        <strong style="color: #ec4899;">🤖 ALEX</strong>
                        <p style="margin: 8px 0 0 0;">{msg['content']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Input
        user_input = st.chat_input("Stel een vraag...")
        
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Simulated responses
            responses = {
                "btw": "Op basis van uw huidige administratie is uw BTW-positie voor Q1 2024: € 45.000 te betalen. De deadline voor de aangifte is 28 februari. Wilt u dat ik de conceptaangifte voor u genereer?",
                "factuur": "Er staan momenteel 4 nieuwe facturen klaar voor verwerking. De grootste is van Houthandel Rotterdam (€ 6.420). Wilt u dat ik deze facturen automatisch laat verwerken door ARIA?",
                "winst": f"Uw netto resultaat YTD is {format_currency(current_client['winst_ytd'])}. Dit is een verbetering van 12% ten opzichte van dezelfde periode vorig jaar. De belangrijkste drivers zijn hogere omzet en betere kostbeheersing.",
                "default": "Ik begrijp uw vraag. Laat me even kijken in uw gegevens... Op basis van uw financiële situatie kan ik u het volgende adviseren. Wilt u meer specifieke informatie over een bepaald onderwerp?"
            }
            
            # Simple keyword matching for demo
            response = responses['default']
            lower_input = user_input.lower()
            if 'btw' in lower_input:
                response = responses['btw']
            elif 'factuur' in lower_input or 'facturen' in lower_input:
                response = responses['factuur']
            elif 'winst' in lower_input or 'resultaat' in lower_input:
                response = responses['winst']
            
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()

    elif st.session_state.current_view == 'forecast':
        st.title("📈 Forecasting & Scenario's")
        st.markdown(f"**{current_client['name']}** | Powered by LUNA")
        
        # Forecast chart
        st.markdown("### 📊 Omzet Prognose")
        
        months = ['Jan', 'Feb', 'Mrt', 'Apr', 'Mei', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dec']
        actual = [45000, 52000, 48000, None, None, None, None, None, None, None, None, None]
        forecast = [45000, 52000, 48000, 55000, 58000, 62000, 65000, 63000, 68000, 72000, 70000, 75000]
        optimistic = [45000, 52000, 48000, 58000, 63000, 68000, 72000, 70000, 76000, 82000, 80000, 88000]
        pessimistic = [45000, 52000, 48000, 52000, 53000, 55000, 56000, 54000, 58000, 60000, 58000, 62000]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=actual, name='Actueel', line=dict(color='#0f172a', width=3)))
        fig.add_trace(go.Scatter(x=months, y=forecast, name='Forecast', line=dict(color='#14b8a6', width=2, dash='dash')))
        fig.add_trace(go.Scatter(x=months, y=optimistic, name='Optimistisch', line=dict(color='#10b981', width=1, dash='dot')))
        fig.add_trace(go.Scatter(x=months, y=pessimistic, name='Pessimistisch', line=dict(color='#ef4444', width=1, dash='dot')))
        
        fig.update_layout(
            xaxis_title="", yaxis_title="Omzet (€)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            margin=dict(t=40, b=20),
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Scenario cards
        st.markdown("### 🎯 Scenario Analyse")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card" style="border-left: 4px solid #10b981;">
                <h4 style="color: #10b981;">Optimistisch</h4>
                <p class="metric-value">€ 788.000</p>
                <p class="metric-label">Jaaromzet prognose</p>
                <p style="color: #10b981;">+28% vs. vorig jaar</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card" style="border-left: 4px solid #14b8a6;">
                <h4 style="color: #14b8a6;">Basis</h4>
                <p class="metric-value">€ 713.000</p>
                <p class="metric-label">Jaaromzet prognose</p>
                <p style="color: #14b8a6;">+16% vs. vorig jaar</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card" style="border-left: 4px solid #ef4444;">
                <h4 style="color: #ef4444;">Pessimistisch</h4>
                <p class="metric-value">€ 638.000</p>
                <p class="metric-label">Jaaromzet prognose</p>
                <p style="color: #64748b;">+4% vs. vorig jaar</p>
            </div>
            """, unsafe_allow_html=True)

    elif st.session_state.current_view == 'crm':
        st.title("🎯 CRM Pipeline")
        st.markdown(f"**{current_client['name']}** | Odoo CRM Integratie")
        
        # Pipeline funnel
        st.markdown("### 📊 Pipeline Funnel")
        
        stages = ['Lead', 'Kwalificatie', 'Voorstel', 'Onderhandeling', 'Gewonnen']
        stage_values = []
        for stage in stages:
            total = sum(d['amount'] for d in ODOO_CRM_PIPELINE if d['stage'] == stage)
            stage_values.append(total)
        
        fig = go.Figure(go.Funnel(
            y=stages,
            x=stage_values,
            textinfo="value+percent initial",
            texttemplate="€%{value:,.0f}<br>%{percentInitial:.0%}",
            marker=dict(color=['#f1f5f9', '#f3e8ff', '#dbeafe', '#fef3c7', '#dcfce7'])
        ))
        fig.update_layout(margin=dict(t=20, b=20), height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # LUNA insight
        weighted_value = sum(d['amount'] * d['probability'] / 100 for d in ODOO_CRM_PIPELINE)
        st.markdown(f"""
        <div class="agent-card agent-luna">
            <strong style="color: #3b82f6;">🔮 LUNA Pipeline Analyse</strong>
            <p style="margin: 8px 0 0 0;">Gewogen pipeline waarde: <strong>{format_currency(weighted_value)}</strong></p>
            <p>Top prioriteit: <strong>Nieuwbouw Villa Wassenaar</strong> - 75% kans, sluit naar verwachting 15 februari</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Deal list
        st.markdown("### 📋 Actieve Deals")
        for deal in ODOO_CRM_PIPELINE:
            stage_colors = {
                'Lead': '#f1f5f9', 'Kwalificatie': '#f3e8ff', 
                'Voorstel': '#dbeafe', 'Onderhandeling': '#fef3c7', 'Gewonnen': '#dcfce7'
            }
            st.markdown(f"""
            <div class="invoice-row">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{deal['name']}</strong>
                        <p style="color: #64748b; margin: 4px 0;">{deal['client']} | {deal['contact']}</p>
                    </div>
                    <div style="text-align: right;">
                        <span style="background: {stage_colors[deal['stage']]}; padding: 4px 12px; border-radius: 20px; font-size: 12px;">{deal['stage']}</span>
                        <p style="font-size: 20px; font-weight: 700; margin: 8px 0 0 0;">{format_currency(deal['amount'])}</p>
                        <p style="color: #64748b; font-size: 12px;">{deal['probability']}% kans</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    elif st.session_state.current_view == 'purchase':
        st.title("📦 Inkoop & Purchase Orders")
        st.markdown(f"**{current_client['name']}** | Odoo Purchase Integratie")
        
        # 3-way matching overview
        st.markdown("### ✅ 3-Way Matching Status")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Volledig gematcht", "3", "")
        with col2:
            st.metric("Wacht op levering", "1", "")
        with col3:
            st.metric("In bestelling", "1", "")
        
        st.markdown("---")
        
        # PO List
        st.markdown("### 📋 Purchase Orders")
        for po in ODOO_PURCHASE_ORDERS:
            status_colors = {'Geleverd': '#dcfce7', 'Gepland': '#fef3c7', 'Besteld': '#dbeafe'}
            st.markdown(f"""
            <div class="invoice-row">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{po['id']}</strong>
                        <p style="color: #64748b; margin: 4px 0;">{po['supplier']}</p>
                        <p style="color: #94a3b8; font-size: 12px;">Project: {po['project']}</p>
                    </div>
                    <div style="text-align: right;">
                        <span style="background: {status_colors[po['status']]}; padding: 4px 12px; border-radius: 20px; font-size: 12px;">{po['status']}</span>
                        <p style="font-size: 18px; font-weight: 700; margin: 8px 0 0 0;">{format_currency(po['amount'])}</p>
                        <p style="color: #64748b; font-size: 12px;">{po['date']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    elif st.session_state.current_view == 'hr':
        st.title("👥 HR & Personeel")
        st.markdown(f"**{current_client['name']}** | Odoo HR Integratie")
        
        # HR Overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Medewerkers", len(ODOO_HR['employees']))
        with col2:
            st.metric("FTE", ODOO_HR['total_fte'])
        with col3:
            st.metric("Loonkosten/maand", format_currency(ODOO_HR['total_salary_costs']))
        with col4:
            wkr_pct = (ODOO_HR['wkr_used'] / ODOO_HR['wkr_budget']) * 100
            st.metric("WKR Benut", f"{wkr_pct:.0f}%")
        
        # SAGE insight
        st.markdown(f"""
        <div class="agent-card agent-sage">
            <strong style="color: #f59e0b;">💡 SAGE - WKR Advies</strong>
            <p style="margin: 8px 0 0 0;">WKR Budget: {format_currency(ODOO_HR['wkr_budget'])} | Benut: {format_currency(ODOO_HR['wkr_used'])} | Ruimte: {format_currency(ODOO_HR['wkr_budget'] - ODOO_HR['wkr_used'])}</p>
            <p style="color: #64748b;">Tip: Overweeg kerstpakketten of een personeelsuitje om het resterende budget optimaal te benutten.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Employee list
        st.markdown("### 👥 Personeelsoverzicht")
        for emp in ODOO_HR['employees']:
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(f"**{emp['name']}**")
                st.markdown(f"<small style='color: #64748b;'>{emp['role']}</small>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"{format_currency(emp['salary'])}/maand")
            with col3:
                st.markdown(f"{emp['fte']} FTE")
            st.markdown("---")

    elif st.session_state.current_view == 'btw':
        st.title("🧾 BTW & ICP Aangifte")
        st.markdown(f"**{current_client['name']}** | Omzetbelasting & Intracommunautaire Prestaties")
        
        # Deadline alert
        days_until_deadline = 5  # Demo: Q4 deadline nadert
        if days_until_deadline <= 7:
            st.markdown(f"""
            <div class="alert-card">
                <strong>⚠️ BTW Deadline Alert</strong><br>
                <span>Q4 2024 aangifte dient uiterlijk <strong>31 januari 2025</strong> ingediend te worden ({days_until_deadline} dagen)</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Current period overview
        st.markdown("### 📊 Huidig Kwartaal (Q4 2024)")
        current_btw = BTW_DATA["periodes"][0]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("BTW Verschuldigd", format_currency(current_btw["btw_verschuldigd"]))
        with col2:
            st.metric("BTW Voorbelasting", format_currency(current_btw["btw_voorbelasting"]))
        with col3:
            st.metric("Af te dragen", format_currency(current_btw["btw_af_te_dragen"]), 
                     delta=f"-{format_currency(current_btw['btw_voorbelasting'])}", delta_color="off")
        with col4:
            st.metric("Status", current_btw["status"])
        
        # SAGE insight
        st.markdown(f"""
        <div class="agent-card agent-sage">
            <strong style="color: #f59e0b;">💡 SAGE - BTW Analyse</strong>
            <p style="margin: 8px 0 0 0;">De voorbelasting ratio is <strong>{(current_btw['btw_voorbelasting']/current_btw['btw_verschuldigd']*100):.1f}%</strong> - dit ligt binnen normale marges voor de bouwsector.</p>
            <p style="color: #64748b;">Let op: ICP-leveringen naar Duitsland (€8.500) vereisen correcte vermelding in de ICP-opgave.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # BTW History
        st.markdown("### 📅 BTW Overzicht per Periode")
        btw_df = pd.DataFrame(BTW_DATA["periodes"])
        btw_df["btw_verschuldigd"] = btw_df["btw_verschuldigd"].apply(format_currency)
        btw_df["btw_voorbelasting"] = btw_df["btw_voorbelasting"].apply(format_currency)
        btw_df["btw_af_te_dragen"] = btw_df["btw_af_te_dragen"].apply(format_currency)
        btw_df.columns = ["Periode", "Status", "Deadline", "Verschuldigd", "Voorbelasting", "Af te dragen", "ICP Lev.", "ICP Verw."]
        st.dataframe(btw_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # ICP Overview
        st.markdown("### 🇪🇺 ICP-Opgave (Intracommunautaire Prestaties)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**ICP Leveringen (verkopen naar EU)**")
            for rel in BTW_DATA["icp_relaties"]:
                st.markdown(f"""
                <div class="invoice-row">
                    <div style="display: flex; justify-content: space-between;">
                        <div>
                            <strong>{rel['land']}</strong><br>
                            <span style="color: #64748b;">{rel['bedrijf']}</span><br>
                            <small style="color: #94a3b8;">{rel['btw_nr']}</small>
                        </div>
                        <div style="text-align: right;">
                            <span style="font-size: 18px; font-weight: 700;">{format_currency(rel['leveringen'])}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("**ICP Verwervingen (inkopen uit EU)**")
            for rel in BTW_DATA["icp_relaties"]:
                st.markdown(f"""
                <div class="invoice-row">
                    <div style="display: flex; justify-content: space-between;">
                        <div>
                            <strong>{rel['land']}</strong><br>
                            <span style="color: #64748b;">{rel['bedrijf']}</span><br>
                            <small style="color: #94a3b8;">{rel['btw_nr']}</small>
                        </div>
                        <div style="text-align: right;">
                            <span style="font-size: 18px; font-weight: 700;">{format_currency(rel['verwervingen'])}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📤 Concept aangifte genereren", key="btw_concept", use_container_width=True):
                st.success("✅ Concept BTW-aangifte Q4 2024 gegenereerd")
        with col2:
            if st.button("📋 ICP-opgave voorbereiden", key="icp_prepare", use_container_width=True):
                st.success("✅ ICP-opgave Q4 2024 voorbereid")
        with col3:
            if st.button("📧 Ter goedkeuring naar klant", key="btw_approve", use_container_width=True):
                st.info("📧 E-mail verzonden naar Jan Vermeer")

    elif st.session_state.current_view == 'vpb':
        st.title("🏛️ Vennootschapsbelasting")
        st.markdown(f"**{current_client['name']}** | Vpb {VPB_DATA['boekjaar']}")
        
        # Deadline overview
        st.markdown("### 📅 Deadlines & Status")
        for dl in VPB_DATA["deadlines"]:
            status_color = "#dcfce7" if dl["status"] == "Akkoord" or dl["status"] == "Betaald" else "#fef3c7" if dl["status"] == "Open" else "#fee2e2"
            st.markdown(f"""
            <div class="invoice-row">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{dl['omschrijving']}</strong>
                        <p style="color: #64748b; margin: 4px 0;">Deadline: {dl['deadline']}</p>
                    </div>
                    <span style="background: {status_color}; padding: 4px 12px; border-radius: 20px; font-size: 12px;">{dl['status']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Vpb Calculation
        st.markdown("### 🧮 Vpb Berekening 2024 (Voorlopig)")
        
        calc = VPB_DATA["berekening"]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <table style="width: 100%; border-collapse: collapse;">
                    <tr style="border-bottom: 1px solid #e2e8f0;">
                        <td style="padding: 12px 0;"><strong>Commerciële winst voor belasting</strong></td>
                        <td style="text-align: right; padding: 12px 0;">{format_currency(calc['winst_voor_vpb'])}</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;">
                        <td style="padding: 12px 0; color: #10b981;">Kleinschaligheidsinvesteringsaftrek (KIA)</td>
                        <td style="text-align: right; padding: 12px 0; color: #10b981;">- {format_currency(calc['kleinschaligheidsinvesteringsaftrek'])}</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e2e8f0;">
                        <td style="padding: 12px 0; color: #ef4444;">Overige fiscale correcties</td>
                        <td style="text-align: right; padding: 12px 0; color: #ef4444;">+ {format_currency(abs(calc['overige_fiscale_correcties']))}</td>
                    </tr>
                    <tr style="background: #f8fafc;">
                        <td style="padding: 12px 0;"><strong>Belastbare winst</strong></td>
                        <td style="text-align: right; padding: 12px 0;"><strong>{format_currency(calc['belastbare_winst'])}</strong></td>
                    </tr>
                    <tr>
                        <td style="padding: 12px 0;">Vpb 19% (tot €200.000)</td>
                        <td style="text-align: right; padding: 12px 0;">{format_currency(calc['vpb_schijf_1'])}</td>
                    </tr>
                    <tr style="background: #0f172a; color: white;">
                        <td style="padding: 12px 0;"><strong>Totaal verschuldigde Vpb</strong></td>
                        <td style="text-align: right; padding: 12px 0;"><strong>{format_currency(calc['vpb_totaal'])}</strong></td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Effective tax rate
            effective_rate = (calc['vpb_totaal'] / calc['winst_voor_vpb']) * 100
            st.markdown(f"""
            <div class="metric-card" style="text-align: center;">
                <p class="metric-label">Effectieve belastingdruk</p>
                <p class="metric-value">{effective_rate:.1f}%</p>
                <p style="color: #64748b; font-size: 12px;">Nominaal tarief: 19%</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Tarieven info
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-label">Vpb Tarieven 2024</p>
                <p><strong>19%</strong> tot €200.000</p>
                <p><strong>25,8%</strong> boven €200.000</p>
            </div>
            """, unsafe_allow_html=True)
        
        # SAGE insight
        st.markdown(f"""
        <div class="agent-card agent-sage">
            <strong style="color: #f59e0b;">💡 SAGE - Fiscaal Advies</strong>
            <p style="margin: 8px 0 0 0;">De KIA-aftrek van €5.200 is correct toegepast op basis van de investeringen in 2024.</p>
            <p style="color: #64748b;">Overweeg om vóór jaareinde nog investeringen te doen - de drempel voor KIA (€2.800) is al bereikt, extra aftrek mogelijk tot €19.500 bij investeringen tot €387.580.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Voorlopige aanslagen
        st.markdown("### 💳 Voorlopige Aanslagen")
        
        col1, col2, col3 = st.columns(3)
        total_va = sum(va['bedrag'] for va in VPB_DATA['voorlopige_aanslagen'])
        paid_va = sum(va['bedrag'] for va in VPB_DATA['voorlopige_aanslagen'] if va['status'] == 'Betaald')
        
        with col1:
            st.metric("Totaal voorlopige aanslagen", format_currency(total_va))
        with col2:
            st.metric("Reeds betaald", format_currency(paid_va))
        with col3:
            expected_return = total_va - calc['vpb_totaal']
            if expected_return > 0:
                st.metric("Verwachte teruggave", format_currency(expected_return), delta="terug te ontvangen")
            else:
                st.metric("Nog te betalen", format_currency(abs(expected_return)), delta="bij te betalen", delta_color="inverse")
        
        for va in VPB_DATA['voorlopige_aanslagen']:
            status_color = "#dcfce7" if va["status"] == "Betaald" else "#fef3c7"
            st.markdown(f"""
            <div class="invoice-row">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>Voorlopige aanslag {va['jaar']}</strong>
                        <p style="color: #64748b; margin: 4px 0;">Vervaldatum: {va['betaaldatum']}</p>
                    </div>
                    <div style="text-align: right;">
                        <span style="background: {status_color}; padding: 4px 12px; border-radius: 20px; font-size: 12px;">{va['status']}</span>
                        <p style="font-size: 18px; font-weight: 700; margin: 8px 0 0 0;">{format_currency(va['bedrag'])}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Action buttons
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Vpb Prognose updaten", key="vpb_prognose", use_container_width=True):
                st.success("✅ Vpb prognose 2024 geüpdatet")
        with col2:
            if st.button("📧 Fiscaal rapport naar klant", key="vpb_report", use_container_width=True):
                st.info("📧 Rapport verzonden naar Jan Vermeer")

    elif st.session_state.current_view == 'odoo_accounting':
        st.title("📚 Odoo Boekhouding")
        st.markdown(f"**{current_client['name']}** | Live synchronisatie met Odoo")
        
        # Sync Status Overview
        st.markdown("### 🔄 Synchronisatie Status")
        
        col1, col2, col3, col4 = st.columns(4)
        stats = ODOO_SYNC_STATUS["ai_booking_stats"]
        
        with col1:
            st.metric("Totaal Mutaties", f"{stats['totaal_mutaties']:,}")
        with col2:
            st.metric("Auto. Geboekt (AI)", f"{stats['automatisch_geboekt']:,}", delta=f"{stats['success_rate']}% success")
        with col3:
            st.metric("Handmatig Nodig", f"{stats['handmatig_nodig']}", delta="actie vereist", delta_color="inverse")
        with col4:
            ok_modules = len([m for m in ODOO_SYNC_STATUS["modules"] if m["status"] == "ok"])
            total_modules = len(ODOO_SYNC_STATUS["modules"])
            st.metric("Modules Online", f"{ok_modules}/{total_modules}")
        
        st.markdown("---")
        
        # Module Status
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.markdown("### 📡 Module Status")
            for mod in ODOO_SYNC_STATUS["modules"]:
                if mod["status"] == "ok":
                    status_icon = "🟢"
                    status_bg = "#dcfce7"
                elif mod["status"] == "warning":
                    status_icon = "🟡"
                    status_bg = "#fef3c7"
                else:
                    status_icon = "🔴"
                    status_bg = "#fee2e2"
                
                pending_badge = f"<span style='background: #fee2e2; color: #dc2626; padding: 2px 8px; border-radius: 12px; font-size: 11px; margin-left: 8px;'>{mod['items_pending']} pending</span>" if mod['items_pending'] > 0 else ""
                
                st.markdown(f"""
                <div class="invoice-row" style="background: {status_bg};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{status_icon} {mod['naam']}</strong>{pending_badge}
                            <p style="color: #64748b; margin: 4px 0 0 0; font-size: 13px;">{mod['details']}</p>
                        </div>
                        <div style="text-align: right;">
                            <small style="color: #94a3b8;">{mod['laatste_sync']}</small>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col_right:
            st.markdown("### 🤖 AI Booking Performance")
            
            # Pie chart for AI vs Manual
            fig = go.Figure(data=[go.Pie(
                labels=['Automatisch (AI)', 'Handmatig nodig'],
                values=[stats['automatisch_geboekt'], stats['handmatig_nodig']],
                hole=0.6,
                marker_colors=['#10b981', '#f59e0b']
            )])
            fig.update_layout(
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2),
                margin=dict(t=20, b=40, l=20, r=20),
                height=250,
                annotations=[dict(text=f"{stats['success_rate']}%", x=0.5, y=0.5, font_size=24, showarrow=False)]
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div class="agent-card agent-aria">
                <strong style="color: #3b82f6;">📊 ARIA - Boekings Analyse</strong>
                <p style="margin: 8px 0 0 0;">87% van alle mutaties wordt automatisch verwerkt. De resterende 13% betreft voornamelijk:</p>
                <ul style="margin: 4px 0; color: #64748b;">
                    <li>Onbekende debiteuren/crediteuren (6%)</li>
                    <li>Complexe aflettering (4%)</li>
                    <li>Ontbrekende facturen (3%)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Open Bank Mutations
        st.markdown("### 🏦 Openstaande Bankmutaties")
        st.markdown("*Mutaties die AI niet automatisch kon boeken - actie vereist*")
        
        for mut in OPEN_BANK_MUTATIONS:
            amount_color = "#10b981" if mut['bedrag'] > 0 else "#ef4444"
            amount_prefix = "+" if mut['bedrag'] > 0 else ""
            
            st.markdown(f"""
            <div class="invoice-row">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div style="flex: 1;">
                        <div style="display: flex; gap: 12px; align-items: center;">
                            <strong>{mut['id']}</strong>
                            <span style="background: #e2e8f0; padding: 2px 8px; border-radius: 8px; font-size: 11px;">{mut['bank']}</span>
                            <small style="color: #94a3b8;">{mut['datum']}</small>
                        </div>
                        <p style="color: #0f172a; margin: 8px 0 4px 0;">{mut['omschrijving']}</p>
                        <p style="color: #dc2626; font-size: 12px; margin: 0;">⚠️ {mut['reden']}</p>
                        <p style="color: #10b981; font-size: 12px; margin: 4px 0 0 0;">💡 {mut['suggestie']}</p>
                    </div>
                    <div style="text-align: right; min-width: 120px;">
                        <span style="font-size: 20px; font-weight: 700; color: {amount_color};">{amount_prefix}€ {abs(mut['bedrag']):,.2f}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Forceer sync alle modules", key="odoo_force_sync", use_container_width=True):
                st.success("✅ Synchronisatie gestart voor alle modules")
        with col2:
            if st.button("📋 Exporteer openstaande mutaties", key="odoo_export_mut", use_container_width=True):
                st.success("✅ Excel export gedownload")
        with col3:
            if st.button("🔧 Naar Odoo Boekhouding", key="odoo_goto", use_container_width=True):
                st.info("🔗 Opent Odoo in nieuw tabblad...")

    elif st.session_state.current_view == 'investments':
        st.title("🏗️ Investeringen & Financiering")
        st.markdown(f"**{current_client['name']}** | Kapitaalgoederen en leningen overzicht")
        
        tab1, tab2, tab3 = st.tabs(["💼 Vaste Activa", "📉 Afschrijvingen", "🏦 Financiering"])
        
        with tab1:
            st.markdown("### 💼 Vaste Activa Overzicht")
            
            # Summary metrics
            total_aanschaf = sum(a['aanschaf'] for a in INVESTERINGEN_DATA['activa'])
            total_afschr = sum(a['afschrijving_cum'] for a in INVESTERINGEN_DATA['activa'])
            total_boekwaarde = sum(a['boekwaarde'] for a in INVESTERINGEN_DATA['activa'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Totaal Aanschafwaarde", format_currency(total_aanschaf))
            with col2:
                st.metric("Cumulatieve Afschrijving", format_currency(total_afschr))
            with col3:
                st.metric("Totale Boekwaarde", format_currency(total_boekwaarde))
            
            st.markdown("---")
            
            # Activa table
            st.markdown("**Kapitaalgoederen per categorie**")
            
            for actief in INVESTERINGEN_DATA['activa']:
                afschr_pct = (actief['afschrijving_cum'] / actief['aanschaf'] * 100) if actief['aanschaf'] > 0 else 0
                
                st.markdown(f"""
                <div class="invoice-row">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="flex: 1;">
                            <strong>{actief['categorie']}</strong>
                            <span style="color: #94a3b8; font-size: 12px; margin-left: 8px;">({actief['rgs']})</span>
                            <p style="color: #64748b; margin: 4px 0 0 0; font-size: 13px;">
                                {actief['methode']} | Levensduur: {actief['levensduur'] or 'n.v.t.'} jaar | Restwaarde: {format_currency(actief['restwaarde'])}
                            </p>
                        </div>
                        <div style="text-align: right; min-width: 300px;">
                            <div style="display: flex; justify-content: space-between; gap: 20px;">
                                <div>
                                    <small style="color: #94a3b8;">Aanschaf</small><br>
                                    <span>{format_currency(actief['aanschaf'])}</span>
                                </div>
                                <div>
                                    <small style="color: #94a3b8;">Afgeschr.</small><br>
                                    <span style="color: #ef4444;">-{format_currency(actief['afschrijving_cum'])}</span>
                                </div>
                                <div>
                                    <small style="color: #94a3b8;">Boekwaarde</small><br>
                                    <strong>{format_currency(actief['boekwaarde'])}</strong>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Planned investments
            st.markdown("### 📅 Geplande Investeringen")
            for inv in INVESTERINGEN_DATA['geplande_investeringen']:
                status_color = "#dcfce7" if inv['status'] == "Goedgekeurd" else "#fef3c7" if inv['status'] == "In bestelling" else "#e2e8f0"
                st.markdown(f"""
                <div class="invoice-row">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{inv['omschrijving']}</strong>
                            <p style="color: #64748b; margin: 4px 0 0 0;">Planning: {inv['datum']}</p>
                        </div>
                        <div style="display: flex; align-items: center; gap: 16px;">
                            <span style="background: {status_color}; padding: 4px 12px; border-radius: 20px; font-size: 12px;">{inv['status']}</span>
                            <strong style="font-size: 18px;">{format_currency(inv['bedrag'])}</strong>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown("### 📉 Afschrijvingsschema")
            
            # Yearly depreciation chart
            years = ['2022', '2023', '2024', '2025 (budget)']
            categories = [a['categorie'] for a in INVESTERINGEN_DATA['afschrijvingen_jaar']]
            
            fig = go.Figure()
            for afschr in INVESTERINGEN_DATA['afschrijvingen_jaar']:
                fig.add_trace(go.Bar(
                    name=afschr['categorie'],
                    x=years,
                    y=[afschr['2022'], afschr['2023'], afschr['2024'], afschr['2025_budget']]
                ))
            
            fig.update_layout(
                barmode='stack',
                title="Afschrijvingen per jaar per categorie",
                yaxis_title="Bedrag (€)",
                legend=dict(orientation="h", yanchor="bottom", y=-0.3),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Depreciation table
            st.markdown("**Jaarlijkse afschrijvingslasten**")
            
            total_2024 = sum(a['2024'] for a in INVESTERINGEN_DATA['afschrijvingen_jaar'])
            total_2025 = sum(a['2025_budget'] for a in INVESTERINGEN_DATA['afschrijvingen_jaar'])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Afschrijving 2024", format_currency(total_2024))
            with col2:
                delta = total_2025 - total_2024
                st.metric("Budget 2025", format_currency(total_2025), delta=format_currency(delta) if delta != 0 else None)
            
            # SAGE insight
            st.markdown(f"""
            <div class="agent-card agent-sage">
                <strong style="color: #f59e0b;">💡 SAGE - Investeringsadvies</strong>
                <p style="margin: 8px 0 0 0;">De afschrijvingslasten dalen in 2025 doordat de ICT Hardware volledig is afgeschreven.</p>
                <p style="color: #64748b;">Let op: bij de geplande investering in bedrijfswagen (€45.000) komt er circa €7.500/jaar afschrijving bij. Dit beïnvloedt ook de KIA-berekening voor de Vpb.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with tab3:
            st.markdown("### 🏦 Financiering Overzicht")
            
            # Summary
            total_schuld = sum(l['openstaand'] for l in FINANCIERING_DATA['leningen_ontvangen'])
            total_uitstaand = sum(l['openstaand'] for l in FINANCIERING_DATA['leningen_verstrekt'])
            total_krediet_beschikbaar = sum(k['beschikbaar'] for k in FINANCIERING_DATA['kredietfaciliteiten'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Totale Schuld", format_currency(total_schuld), delta="leningen ontvangen", delta_color="off")
            with col2:
                st.metric("Uitstaande Leningen", format_currency(total_uitstaand), delta="verstrekt aan derden", delta_color="off")
            with col3:
                st.metric("Beschikbaar Krediet", format_currency(total_krediet_beschikbaar))
            
            st.markdown("---")
            
            # Loans received
            st.markdown("**📥 Ontvangen Leningen**")
            for lening in FINANCIERING_DATA['leningen_ontvangen']:
                progress = 1 - (lening['openstaand'] / lening['hoofdsom'])
                st.markdown(f"""
                <div class="invoice-row">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div style="flex: 1;">
                            <strong>{lening['verstrekker']}</strong>
                            <span style="background: #e2e8f0; padding: 2px 8px; border-radius: 8px; font-size: 11px; margin-left: 8px;">{lening['type']}</span>
                            <p style="color: #64748b; margin: 4px 0 0 0; font-size: 13px;">
                                Rente: {lening['rente']}% | Aflossing: {format_currency(lening['aflossing_maand'])}/mnd | Einddatum: {lening['einddatum']}
                            </p>
                            <p style="color: #94a3b8; margin: 2px 0 0 0; font-size: 12px;">
                                Onderpand: {lening['onderpand']}
                            </p>
                        </div>
                        <div style="text-align: right; min-width: 180px;">
                            <p style="color: #94a3b8; margin: 0;">Openstaand</p>
                            <strong style="font-size: 20px; color: #ef4444;">{format_currency(lening['openstaand'])}</strong>
                            <p style="color: #64748b; font-size: 12px; margin: 4px 0 0 0;">van {format_currency(lening['hoofdsom'])}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Loans given
            st.markdown("**📤 Verstrekte Leningen**")
            for lening in FINANCIERING_DATA['leningen_verstrekt']:
                st.markdown(f"""
                <div class="invoice-row">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{lening['debiteur']}</strong>
                            <span style="background: #dbeafe; padding: 2px 8px; border-radius: 8px; font-size: 11px; margin-left: 8px;">{lening['type']}</span>
                            <p style="color: #64748b; margin: 4px 0 0 0; font-size: 13px;">
                                Rente: {lening['rente']}% | Aflossing: {format_currency(lening['aflossing_maand'])}/mnd
                            </p>
                        </div>
                        <div style="text-align: right;">
                            <strong style="font-size: 18px; color: #10b981;">{format_currency(lening['openstaand'])}</strong>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Credit facilities
            st.markdown("**💳 Kredietfaciliteiten**")
            for krediet in FINANCIERING_DATA['kredietfaciliteiten']:
                benut_pct = (krediet['benut'] / krediet['limiet']) * 100
                bar_color = "#10b981" if benut_pct < 50 else "#f59e0b" if benut_pct < 80 else "#ef4444"
                st.markdown(f"""
                <div class="invoice-row">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="flex: 1;">
                            <strong>{krediet['bank']} - {krediet['type']}</strong>
                            <div style="background: #e2e8f0; border-radius: 4px; height: 8px; margin-top: 8px; width: 200px;">
                                <div style="background: {bar_color}; border-radius: 4px; height: 8px; width: {benut_pct}%;"></div>
                            </div>
                            <p style="color: #64748b; margin: 4px 0 0 0; font-size: 12px;">
                                {benut_pct:.0f}% benut
                            </p>
                        </div>
                        <div style="text-align: right;">
                            <p style="color: #94a3b8; margin: 0; font-size: 12px;">Beschikbaar</p>
                            <strong style="font-size: 18px; color: #10b981;">{format_currency(krediet['beschikbaar'])}</strong>
                            <p style="color: #64748b; font-size: 12px; margin: 0;">van {format_currency(krediet['limiet'])}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Monthly repayment schedule chart
            st.markdown("### 📅 Aflossingsschema 2025")
            
            months = [a['maand'] for a in FINANCIERING_DATA['aflossingsschema_2025']]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name='ABN Hypotheek', x=months, y=[a['abn_hypo'] for a in FINANCIERING_DATA['aflossingsschema_2025']], marker_color='#3b82f6'))
            fig.add_trace(go.Bar(name='Rabo Krediet', x=months, y=[a['rabo_krediet'] for a in FINANCIERING_DATA['aflossingsschema_2025']], marker_color='#f59e0b'))
            fig.add_trace(go.Bar(name='Qredits', x=months, y=[a['qredits'] for a in FINANCIERING_DATA['aflossingsschema_2025']], marker_color='#10b981'))
            
            fig.update_layout(
                barmode='stack',
                title="Maandelijkse aflossingsverplichtingen",
                yaxis_title="Bedrag (€)",
                legend=dict(orientation="h", yanchor="bottom", y=-0.3),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Annual summary
            total_aflossing_jaar = sum(a['totaal'] for a in FINANCIERING_DATA['aflossingsschema_2025'])
            total_rente_jaar = (280000 * 0.032) + (52000 * 0.048) + (22500 * 0.055)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Totale Aflossing 2025", format_currency(total_aflossing_jaar))
            with col2:
                st.metric("Geschatte Rentelast 2025", format_currency(total_rente_jaar))
            
            # SAGE insight
            st.markdown(f"""
            <div class="agent-card agent-sage">
                <strong style="color: #f59e0b;">💡 SAGE - Financieringsadvies</strong>
                <p style="margin: 8px 0 0 0;">Het Rabobank bedrijfskrediet loopt eind 2026 af. Overweeg tijdig herfinanciering als de kredietbehoefte blijft bestaan.</p>
                <p style="color: #64748b;">De huidige schuldgraad (Debt/Equity ratio) is gezond. Er is ruimte voor aanvullende financiering indien nodig voor de geplande investeringen.</p>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 12px;">
    NOVA Platform Demo | Conceptueel ontwerp voor het accountantskantoor van de toekomst<br>
    Inclusief Odoo ERP integratie voor end-to-end business operations
</div>
""", unsafe_allow_html=True)
