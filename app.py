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
    
    h1, h2, h3 { color: #0f172a; }
    
    .sidebar .sidebar-content { background: #0f172a; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'dashboard'
if 'selected_invoice' not in st.session_state:
    st.session_state.selected_invoice = None
if 'processed_invoices' not in st.session_state:
    st.session_state.processed_invoices = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'selected_deal' not in st.session_state:
    st.session_state.selected_deal = None

# Demo Data
DEMO_CLIENT = {
    "name": "Vermeer Bouw B.V.",
    "contact": "Jan Vermeer",
    "kvk": "12345678",
    "btw": "NL123456789B01"
}

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

# Demo Invoices
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
        {"name": "Ahmed Hassan", "role": "Uitvoerder", "salary": 4500, "fte": 1.0},
        {"name": "Maria Santos", "role": "Administratie", "salary": 3800, "fte": 0.8},
        {"name": "Pieter Bakker", "role": "Timmerman", "salary": 4000, "fte": 1.0},
        {"name": "Tom Visser", "role": "Metselaar", "salary": 3900, "fte": 1.0},
        {"name": "Lisa van Dijk", "role": "Timmerman", "salary": 3800, "fte": 1.0},
        {"name": "Kevin Jansen", "role": "Leerling", "salary": 2200, "fte": 1.0},
    ],
    "total_fte": 7.8,
    "total_monthly_cost": 34900,
    "wkr_budget": 5880,
    "wkr_used": 3200,
}

# RGS Winst & Verlies (Dutch Standard)
RGS_PNL = {
    "Netto-omzet": {
        "WOmzNol": {"label": "Netto-omzet uit leveringen", "amount": 485000},
        "WOmzNod": {"label": "Netto-omzet uit diensten", "amount": 127500},
    },
    "Kostprijs van de omzet": {
        "WIkworGro": {"label": "Grond- en hulpstoffen", "amount": -142500},
        "WKprUitInh": {"label": "Uitbesteed werk / ingehuurde diensten", "amount": -68000},
        "WKprUitTra": {"label": "Transportkosten", "amount": -18500},
    },
    "Personeelskosten": {
        "WPerLes": {"label": "Lonen en salarissen", "amount": -165000},
        "WPerSol": {"label": "Sociale lasten", "amount": -38500},
        "WPerPen": {"label": "Pensioenlasten", "amount": -24000},
    },
    "Overige bedrijfskosten": {
        "WBehHuiHuu": {"label": "Huur", "amount": -36000},
        "WBehHuiEne": {"label": "Energie", "amount": -12400},
        "WBehVerBed": {"label": "Verzekeringen", "amount": -8200},
        "WBehAutSof": {"label": "Software & automatisering", "amount": -7800},
        "WBehKanTel": {"label": "Telefoon & communicatie", "amount": -3600},
        "WBehAdvAdv": {"label": "Advieskosten", "amount": -15000},
    },
    "Afschrijvingen": {
        "WAfsMat": {"label": "Afschrijving materiële vaste activa", "amount": -28000},
    },
    "Financiële baten en lasten": {
        "WFbeRon": {"label": "Rentebaten", "amount": 1250},
        "WFlaRba": {"label": "Rentelasten", "amount": -8500},
    }
}

# RGS Balans (Dutch Standard)
RGS_BALANCE = {
    "ACTIVA": {
        "Vaste activa": {
            "BMvaTer": {"label": "Terreinen", "amount": 125000},
            "BMvaBeg": {"label": "Bedrijfsgebouwen", "amount": 380000},
            "BMvaMei": {"label": "Machines en installaties", "amount": 95000},
            "BMvaVer": {"label": "Vervoermiddelen", "amount": 68000},
            "BMvaKan": {"label": "Inventaris", "amount": 24000},
        },
        "Vlottende activa": {
            "BVrdVoo": {"label": "Voorraden", "amount": 87500},
            "BVorDebHan": {"label": "Debiteuren", "amount": 142000},
            "BVorOvrBel": {"label": "Belastingvorderingen", "amount": 28500},
            "BLimBan": {"label": "Bank", "amount": 156000},
            "BLimKas": {"label": "Kas", "amount": 2500},
        }
    },
    "PASSIVA": {
        "Eigen vermogen": {
            "BEivGok": {"label": "Gestort kapitaal", "amount": 250000},
            "BEivAlr": {"label": "Algemene reserve", "amount": 185000},
            "BEivOwi": {"label": "Onverdeelde winst", "amount": 47750},
        },
        "Langlopende schulden": {
            "BLasLba": {"label": "Lening bank", "amount": 320000},
        },
        "Kortlopende schulden": {
            "BSchCreHan": {"label": "Crediteuren", "amount": 98500},
            "BSchBepLoo": {"label": "Loonbelasting", "amount": 18500},
            "BSchBepOmb": {"label": "Omzetbelasting", "amount": 32750},
            "BSchOvsPen": {"label": "Pensioenpremies", "amount": 8000},
        }
    }
}

# Sidebar navigation
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #14b8a6; font-size: 32px; margin: 0;">NOVA</h1>
        <p style="color: #64748b; font-size: 12px; margin: 5px 0 0 0;">Platform Demo</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Client info
    st.markdown(f"""
    <div style="background: #f1f5f9; padding: 16px; border-radius: 12px; margin-bottom: 20px;">
        <p style="color: #64748b; font-size: 11px; margin: 0;">DEMO KLANT</p>
        <p style="color: #0f172a; font-weight: 600; margin: 4px 0;">{DEMO_CLIENT['name']}</p>
        <p style="color: #64748b; font-size: 12px; margin: 0;">{DEMO_CLIENT['contact']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    st.markdown("**NAVIGATIE**")
    
    nav_options = {
        "🎯 Dashboard": "dashboard",
        "📄 Facturen": "invoices",
        "📊 Winst & Verlies": "pnl",
        "⚖️ Balans": "balance",
        "🤖 AI Agents": "agents",
        "💬 Chat met ALEX": "chat",
        "📈 Forecasting": "forecast"
    }
    
    for label, view in nav_options.items():
        if st.button(label, key=f"nav_{view}", use_container_width=True):
            st.session_state.current_view = view
    
    # Odoo section
    st.markdown("---")
    st.markdown("""<span class="odoo-badge">ODOO INTEGRATIE</span>""", unsafe_allow_html=True)
    st.markdown("")
    
    odoo_options = {
        "🎯 CRM Pipeline": "crm",
        "📦 Inkoop (PO's)": "purchase",
        "👥 HR & Personeel": "hr",
    }
    
    for label, view in odoo_options.items():
        if st.button(label, key=f"nav_{view}", use_container_width=True):
            st.session_state.current_view = view

# Main content based on navigation
if st.session_state.current_view == 'dashboard':
    st.title("🎯 Mijn Financiële Cockpit")
    st.markdown(f"Welkom terug, **{DEMO_CLIENT['contact']}** | {datetime.now().strftime('%d %B %Y')}")
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Omzet YTD",
            value="€ 612.500",
            delta="+12.3% vs vorig jaar"
        )
    
    with col2:
        st.metric(
            label="Brutomarge",
            value="34.2%",
            delta="+2.1pp"
        )
    
    with col3:
        st.metric(
            label="Openstaande facturen",
            value="€ 142.000",
            delta="-€23.500 deze week"
        )
    
    with col4:
        st.metric(
            label="Cashflow prognose (30d)",
            value="€ 89.200",
            delta="Positief"
        )
    
    st.markdown("---")
    
    # Odoo Pipeline Summary
    st.subheader("🎯 CRM Pipeline Overzicht")
    st.markdown('<span class="odoo-badge">VIA ODOO</span>', unsafe_allow_html=True)
    
    pipeline_cols = st.columns(5)
    stages = ["Lead", "Kwalificatie", "Voorstel", "Onderhandeling", "Gewonnen"]
    stage_colors = ["#64748b", "#8b5cf6", "#3b82f6", "#f59e0b", "#10b981"]
    
    for i, (stage, color) in enumerate(zip(stages, stage_colors)):
        deals = [d for d in ODOO_CRM_PIPELINE if d['stage'] == stage]
        total = sum(d['amount'] for d in deals)
        with pipeline_cols[i]:
            st.markdown(f"""
            <div style="background: white; padding: 16px; border-radius: 12px; border-top: 4px solid {color}; text-align: center;">
                <p style="color: #64748b; font-size: 12px; margin: 0;">{stage}</p>
                <p style="color: #0f172a; font-size: 24px; font-weight: 700; margin: 8px 0;">€ {total:,.0f}</p>
                <p style="color: #64748b; font-size: 11px; margin: 0;">{len(deals)} deal(s)</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts row
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📈 Omzet vs Kosten")
        
        months = ['Aug', 'Sep', 'Okt', 'Nov', 'Dec', 'Jan']
        omzet = [85000, 92000, 88000, 95000, 110000, 97500]
        kosten = [62000, 68000, 65000, 71000, 78000, 72000]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Omzet', x=months, y=omzet, marker_color='#14b8a6'))
        fig.add_trace(go.Bar(name='Kosten', x=months, y=kosten, marker_color='#0f172a'))
        fig.update_layout(
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=20, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        st.subheader("💰 Cashflow Forecast")
        st.caption("🔗 Inclusief verwachte pipeline-inkomsten")
        
        weeks = ['Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8']
        cashflow = [45000, 28000, 52000, 38000, 89200]
        colors = ['#14b8a6' if x > 0 else '#ef4444' for x in cashflow]
        
        fig = go.Figure(data=[go.Bar(x=weeks, y=cashflow, marker_color=colors)])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=20, b=0),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Agent status row
    st.markdown("---")
    st.subheader("🤖 AI Agents Status")
    
    agent_cols = st.columns(5)
    for i, (name, agent) in enumerate(AI_AGENTS.items()):
        with agent_cols[i]:
            st.markdown(f"""
            <div style="background: white; padding: 16px; border-radius: 12px; border-left: 4px solid {agent['color']}; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 600; color: #0f172a;">{name}</span>
                    <span class="status-active">{agent['status']}</span>
                </div>
                <p style="color: #64748b; font-size: 12px; margin: 8px 0;">{agent['role']}</p>
                <p style="color: #0f172a; font-size: 20px; font-weight: 700; margin: 0;">{agent['processed_today']}</p>
                <p style="color: #64748b; font-size: 11px; margin: 0;">verwerkt vandaag</p>
            </div>
            """, unsafe_allow_html=True)

elif st.session_state.current_view == 'crm':
    st.title("🎯 CRM Pipeline")
    st.markdown('<span class="odoo-badge">ODOO CRM</span> Beheer je sales pipeline en deals', unsafe_allow_html=True)
    
    # Pipeline Summary
    col1, col2, col3, col4 = st.columns(4)
    
    total_pipeline = sum(d['amount'] for d in ODOO_CRM_PIPELINE)
    weighted_pipeline = sum(d['amount'] * d['probability'] / 100 for d in ODOO_CRM_PIPELINE)
    won_deals = sum(d['amount'] for d in ODOO_CRM_PIPELINE if d['stage'] == 'Gewonnen')
    
    with col1:
        st.metric("Totale Pipeline", f"€ {total_pipeline:,.0f}")
    with col2:
        st.metric("Gewogen Waarde", f"€ {weighted_pipeline:,.0f}")
    with col3:
        st.metric("Gewonnen (YTD)", f"€ {won_deals:,.0f}")
    with col4:
        st.metric("Conversie %", "23%", delta="+5% vs Q4")
    
    st.markdown("---")
    
    # Pipeline Funnel
    st.subheader("📊 Pipeline Funnel")
    
    stages = ["Lead", "Kwalificatie", "Voorstel", "Onderhandeling", "Gewonnen"]
    stage_values = []
    for stage in stages:
        deals = [d for d in ODOO_CRM_PIPELINE if d['stage'] == stage]
        stage_values.append(sum(d['amount'] for d in deals))
    
    fig = go.Figure(go.Funnel(
        y = stages,
        x = stage_values,
        textposition = "inside",
        textinfo = "value+percent initial",
        marker = {"color": ["#64748b", "#8b5cf6", "#3b82f6", "#f59e0b", "#10b981"]},
        texttemplate = "€%{value:,.0f}<br>%{percentInitial:.0%}"
    ))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Deal List
    st.subheader("📋 Alle Deals")
    
    # Filter
    stage_filter = st.multiselect("Filter op fase:", stages, default=stages)
    
    for deal in ODOO_CRM_PIPELINE:
        if deal['stage'] not in stage_filter:
            continue
            
        stage_colors = {
            "Lead": "#64748b",
            "Kwalificatie": "#8b5cf6",
            "Voorstel": "#3b82f6",
            "Onderhandeling": "#f59e0b",
            "Gewonnen": "#10b981"
        }
        
        with st.expander(f"**{deal['name']}** - {deal['client']} | € {deal['amount']:,.0f}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                **Deal Details**
                - **Fase:** <span style="background: {stage_colors[deal['stage']]}20; color: {stage_colors[deal['stage']]}; padding: 2px 8px; border-radius: 4px;">{deal['stage']}</span>
                - **Waarde:** € {deal['amount']:,.0f}
                - **Kans:** {deal['probability']}%
                - **Gewogen:** € {deal['amount'] * deal['probability'] / 100:,.0f}
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                **Contact**
                - **Naam:** {deal['contact']}
                - **Email:** {deal['email']}
                - **Telefoon:** {deal['phone']}
                """)
            
            with col3:
                st.markdown(f"""
                **Status**
                - **Verwachte closing:** {deal['expected_close']}
                - **Notities:** {deal['notes']}
                """)
            
            # LUNA Insight
            if deal['probability'] >= 50:
                expected_income = deal['amount'] * deal['probability'] / 100
                st.info(f"💡 **LUNA Insight:** Deze deal heeft {deal['probability']}% kans. Als gewonnen, verwacht ik de eerste betaling (30%) rond {deal['expected_close']}. Dit is € {expected_income * 0.3:,.0f} voor je cashflow.")
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                if st.button("📧 Email versturen", key=f"email_{deal['id']}"):
                    st.success("Email concept geopend!")
            with col_b:
                if st.button("📞 Bel notitie", key=f"call_{deal['id']}"):
                    st.info("Bel notitie venster...")
            with col_c:
                if st.button("➡️ Volgende fase", key=f"next_{deal['id']}"):
                    st.success(f"Deal verplaatst naar volgende fase!")

elif st.session_state.current_view == 'purchase':
    st.title("📦 Inkoop & Purchase Orders")
    st.markdown('<span class="odoo-badge">ODOO PURCHASE</span> Beheer je inkooporders en leveranciers', unsafe_allow_html=True)
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Open PO's", "5")
    with col2:
        st.metric("Totaal open", f"€ {sum(po['amount'] for po in ODOO_PURCHASE_ORDERS):,.0f}")
    with col3:
        st.metric("Deze maand", f"€ {sum(po['amount'] for po in ODOO_PURCHASE_ORDERS):,.0f}")
    with col4:
        st.metric("Gemiddelde levertijd", "4.2 dagen")
    
    st.markdown("---")
    st.subheader("📋 Purchase Orders")
    
    for po in ODOO_PURCHASE_ORDERS:
        status_colors = {"Geleverd": "#10b981", "Besteld": "#3b82f6", "Gepland": "#f59e0b"}
        
        col1, col2, col3, col4, col5 = st.columns([1.5, 2.5, 1.5, 1.5, 1])
        
        with col1:
            st.markdown(f"**{po['id']}**")
            st.caption(po['date'])
        
        with col2:
            st.markdown(po['supplier'])
            project = next((d['name'] for d in ODOO_CRM_PIPELINE if d['id'] == po['project']), "Algemeen")
            st.caption(f"🔗 {project}")
        
        with col3:
            st.markdown(f"**€ {po['amount']:,.2f}**")
        
        with col4:
            color = status_colors.get(po['status'], '#64748b')
            st.markdown(f"<span style='background: {color}20; color: {color}; padding: 4px 12px; border-radius: 12px; font-size: 12px;'>{po['status']}</span>", unsafe_allow_html=True)
        
        with col5:
            if st.button("👁️", key=f"po_{po['id']}"):
                st.info(f"Details voor {po['id']}")
        
        st.markdown("---")
    
    # 3-way matching info
    st.markdown("### 🔗 3-Way Matching met ARIA")
    st.info("""
    **Automatische factuurmatching actief!**
    
    ARIA controleert automatisch of inkomende facturen matchen met:
    1. ✅ Purchase Order (bestelling)
    2. ✅ Goods Receipt (ontvangst)
    3. ✅ Invoice (factuur)
    
    Bij een mismatch wordt de factuur gemarkeerd voor review.
    """)

elif st.session_state.current_view == 'hr':
    st.title("👥 HR & Personeel")
    st.markdown('<span class="odoo-badge">ODOO HR</span> Personeelsoverzicht en loonkosten', unsafe_allow_html=True)
    
    # HR Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Medewerkers", len(ODOO_HR['employees']))
    with col2:
        st.metric("Totaal FTE", ODOO_HR['total_fte'])
    with col3:
        st.metric("Loonkosten/maand", f"€ {ODOO_HR['total_monthly_cost']:,.0f}")
    with col4:
        wkr_remaining = ODOO_HR['wkr_budget'] - ODOO_HR['wkr_used']
        st.metric("WKR ruimte over", f"€ {wkr_remaining:,.0f}")
    
    st.markdown("---")
    
    # Employee List
    st.subheader("👥 Personeelsbestand")
    
    df_employees = pd.DataFrame(ODOO_HR['employees'])
    df_employees['Bruto salaris'] = df_employees['salary'].apply(lambda x: f"€ {x:,.0f}")
    df_employees.columns = ['Naam', 'Functie', 'Salaris', 'FTE', 'Bruto salaris']
    
    st.dataframe(
        df_employees[['Naam', 'Functie', 'FTE', 'Bruto salaris']],
        hide_index=True,
        use_container_width=True
    )
    
    st.markdown("---")
    
    # SAGE Insights
    st.subheader("💡 SAGE Fiscale Inzichten")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### WKR Analyse")
        wkr_pct = (ODOO_HR['wkr_used'] / ODOO_HR['wkr_budget']) * 100
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = ODOO_HR['wkr_used'],
            number = {'prefix': "€ ", 'valueformat': ",.0f"},
            delta = {'reference': ODOO_HR['wkr_budget'], 'relative': False, 'valueformat': ",.0f"},
            gauge = {
                'axis': {'range': [None, ODOO_HR['wkr_budget']]},
                'bar': {'color': "#14b8a6"},
                'steps': [
                    {'range': [0, ODOO_HR['wkr_budget'] * 0.8], 'color': "#dcfce7"},
                    {'range': [ODOO_HR['wkr_budget'] * 0.8, ODOO_HR['wkr_budget']], 'color': "#fef3c7"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': ODOO_HR['wkr_budget']
                }
            },
            title = {'text': "WKR Benutting"}
        ))
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
        
        st.success(f"✅ Nog **€ {wkr_remaining:,.0f}** WKR-ruimte beschikbaar dit jaar")
    
    with col2:
        st.markdown("### SAGE Adviezen")
        st.warning("""
        **💡 Optimalisatie mogelijkheden:**
        
        1. **Fietsregeling**: 3 medewerkers komen in aanmerking. 
           Potentiële besparing: € 1.200/jaar
        
        2. **Thuiswerkvergoeding**: Huidige regeling onder WKR.
           Advies: verhoog naar € 2,35/dag (fiscaal optimaal)
        
        3. **Pensioenopbouw**: Kevin (leerling) bouwt nog geen 
           pensioen op. Overweeg vrijwillige deelname.
        """)
        
        if st.button("📊 Genereer volledig loonkosten rapport"):
            st.info("SAGE genereert rapport...")

elif st.session_state.current_view == 'invoices':
    st.title("📄 Factuurverwerking")
    st.markdown("Bekijk en beheer inkomende facturen met AI-ondersteuning van **ARIA**")
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Nieuw", "4", delta="vandaag")
    with col2:
        st.metric("Wacht op review", "1")
    with col3:
        st.metric("Verwerkt", "3")
    with col4:
        st.metric("AI Nauwkeurigheid", "99.2%")
    
    st.markdown("---")
    
    # Invoice upload simulation
    uploaded_file = st.file_uploader("📤 Upload een factuur (PDF/afbeelding)", type=['pdf', 'png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        with st.spinner("🤖 ARIA analyseert de factuur..."):
            import time
            time.sleep(2)
        
        st.success("✅ Factuur succesvol geanalyseerd!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Herkende gegevens:**")
            st.json({
                "leverancier": "Demo Leverancier B.V.",
                "factuurnummer": "F-2024-NEW",
                "datum": datetime.now().strftime("%Y-%m-%d"),
                "bedrag_excl": 1250.00,
                "btw": 262.50,
                "totaal": 1512.50,
                "categorie": "Algemene kosten",
                "rgs_code": "WBehOve",
                "confidence": "98.5%",
                "odoo_match": "PO2024-053 (98% match)"
            })
        with col2:
            st.markdown("**AI Suggestie:**")
            st.info("💡 ARIA heeft een match gevonden met **PO2024-053** in Odoo Purchase. De bedragen komen overeen. 3-way matching is succesvol!")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("✅ Goedkeuren & Boeken", type="primary"):
                    st.success("Factuur geboekt!")
            with col_b:
                if st.button("✏️ Aanpassen"):
                    st.info("Edit mode...")
    
    st.markdown("---")
    st.subheader("📋 Factuuroverzicht")
    
    # Filter tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Alle", "Nieuw (4)", "Wacht op review (1)", "Verwerkt (3)"])
    
    def show_invoice_list(invoices):
        for inv in invoices:
            status_color = {"nieuw": "#3b82f6", "wacht op review": "#f59e0b", "verwerkt": "#10b981"}
            col1, col2, col3, col4, col5 = st.columns([2, 3, 2, 2, 1])
            
            with col1:
                st.markdown(f"**{inv['id']}**")
                st.caption(inv['date'])
            with col2:
                st.markdown(inv['supplier'])
                if inv.get('odoo_po'):
                    st.caption(f"🔗 {inv['odoo_po']}")
                else:
                    st.caption(f"RGS: {inv['rgs']}")
            with col3:
                st.markdown(f"€ {inv['amount']:,.2f}")
                st.caption(f"BTW: € {inv['vat']:,.2f}")
            with col4:
                st.markdown(f"<span style='background: {status_color.get(inv['status'], '#gray')}20; color: {status_color.get(inv['status'], 'gray')}; padding: 4px 12px; border-radius: 12px; font-size: 12px;'>{inv['status'].upper()}</span>", unsafe_allow_html=True)
            with col5:
                if st.button("👁️", key=f"view_{inv['id']}"):
                    st.session_state.selected_invoice = inv
            
            st.markdown("---")
    
    with tab1:
        show_invoice_list(DEMO_INVOICES)
    with tab2:
        show_invoice_list([i for i in DEMO_INVOICES if i['status'] == 'nieuw'])
    with tab3:
        show_invoice_list([i for i in DEMO_INVOICES if i['status'] == 'wacht op review'])
    with tab4:
        show_invoice_list([i for i in DEMO_INVOICES if i['status'] == 'verwerkt'])

elif st.session_state.current_view == 'pnl':
    st.title("📊 Winst & Verliesrekening")
    st.markdown("Volgens Nederlandse RGS-standaard | Periode: januari 2024")
    
    # Summary metrics
    total_revenue = sum(item['amount'] for cat in ['Netto-omzet'] for item in RGS_PNL.get(cat, {}).values())
    total_costs = sum(item['amount'] for cat in RGS_PNL.keys() if cat != 'Netto-omzet' for item in RGS_PNL.get(cat, {}).values())
    net_result = total_revenue + total_costs
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Totale omzet", f"€ {total_revenue:,.0f}")
    with col2:
        st.metric("Totale kosten", f"€ {abs(total_costs):,.0f}")
    with col3:
        st.metric("Netto resultaat", f"€ {net_result:,.0f}", delta=f"{(net_result/total_revenue*100):.1f}% marge")
    
    st.markdown("---")
    
    # Detailed P&L
    for category, items in RGS_PNL.items():
        with st.expander(f"**{category}**", expanded=True):
            df_data = []
            for code, data in items.items():
                df_data.append({
                    "RGS Code": code,
                    "Omschrijving": data['label'],
                    "Bedrag": f"€ {data['amount']:,.0f}"
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, hide_index=True, use_container_width=True)
            
            subtotal = sum(item['amount'] for item in items.values())
            st.markdown(f"**Subtotaal: € {subtotal:,.0f}**")
    
    st.markdown("---")
    st.markdown(f"### 🎯 Netto Resultaat: € {net_result:,.0f}")

elif st.session_state.current_view == 'balance':
    st.title("⚖️ Balans")
    st.markdown("Volgens Nederlandse RGS-standaard | Per 31 januari 2024")
    
    # Calculate totals
    total_activa = sum(
        item['amount'] 
        for section in RGS_BALANCE['ACTIVA'].values() 
        for item in section.values()
    )
    total_passiva = sum(
        item['amount'] 
        for section in RGS_BALANCE['PASSIVA'].values() 
        for item in section.values()
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Totaal Activa", f"€ {total_activa:,.0f}")
    with col2:
        st.metric("Totaal Passiva", f"€ {total_passiva:,.0f}")
    
    if total_activa == total_passiva:
        st.success("✅ Balans is in evenwicht")
    else:
        st.error(f"⚠️ Balansverschil: € {total_activa - total_passiva:,.0f}")
    
    st.markdown("---")
    
    col_activa, col_passiva = st.columns(2)
    
    with col_activa:
        st.subheader("ACTIVA")
        for section_name, items in RGS_BALANCE['ACTIVA'].items():
            with st.expander(f"**{section_name}**", expanded=True):
                df_data = []
                for code, data in items.items():
                    df_data.append({
                        "RGS": code,
                        "Omschrijving": data['label'],
                        "Bedrag": f"€ {data['amount']:,.0f}"
                    })
                df = pd.DataFrame(df_data)
                st.dataframe(df, hide_index=True, use_container_width=True)
                
                subtotal = sum(item['amount'] for item in items.values())
                st.markdown(f"**Subtotaal: € {subtotal:,.0f}**")
    
    with col_passiva:
        st.subheader("PASSIVA")
        for section_name, items in RGS_BALANCE['PASSIVA'].items():
            with st.expander(f"**{section_name}**", expanded=True):
                df_data = []
                for code, data in items.items():
                    df_data.append({
                        "RGS": code,
                        "Omschrijving": data['label'],
                        "Bedrag": f"€ {data['amount']:,.0f}"
                    })
                df = pd.DataFrame(df_data)
                st.dataframe(df, hide_index=True, use_container_width=True)
                
                subtotal = sum(item['amount'] for item in items.values())
                st.markdown(f"**Subtotaal: € {subtotal:,.0f}**")

elif st.session_state.current_view == 'agents':
    st.title("🤖 AI Agents")
    st.markdown("Uw digitale collega's - altijd beschikbaar, continu lerend")
    
    for name, agent in AI_AGENTS.items():
        with st.expander(f"**{name}** - {agent['full_name']}", expanded=True):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div style="border-left: 4px solid {agent['color']}; padding-left: 16px;">
                    <h4 style="margin: 0; color: {agent['color']};">{agent['role']}</h4>
                    <p style="color: #64748b; margin: 8px 0;">{agent['description']}</p>
                    <p style="margin: 4px 0;"><span class="odoo-badge">ODOO</span> <span style="color: #64748b; font-size: 12px; margin-left: 8px;">{agent['odoo_link']}</span></p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.metric("Verwerkt vandaag", agent['processed_today'])
            
            with col3:
                st.metric("Nauwkeurigheid", f"{agent['accuracy']}%")
            
            # Activity simulation
            st.markdown("**Recente activiteit:**")
            activities = [
                f"✅ Document verwerkt - {datetime.now() - timedelta(minutes=random.randint(1, 30))}",
                f"✅ Analyse voltooid - {datetime.now() - timedelta(minutes=random.randint(31, 60))}",
                f"💡 Advies gegenereerd - {datetime.now() - timedelta(hours=random.randint(1, 3))}",
            ]
            for activity in activities[:2]:
                st.caption(activity)

elif st.session_state.current_view == 'chat':
    st.title("💬 Chat met ALEX")
    st.markdown("Uw AI-assistent voor al uw financiële vragen")
    
    # Chat responses
    ALEX_RESPONSES = {
        "btw": "Op basis van uw administratie heeft u dit kwartaal **€ 32.750** aan BTW te betalen. De deadline is 28 februari. Wilt u dat ik een herinnering instel?",
        "cashflow": "Uw cashflow voor de komende 30 dagen ziet er positief uit: **€ 89.200** verwacht saldo. Inclusief de verwachte binnenkomst van **€ 23.400** uit de deal 'Aanbouw Praktijkruimte Amersfoort' (via Odoo CRM).",
        "factuur": "Er staan momenteel **8 facturen** open ter waarde van **€ 142.000**. De oudste is 45 dagen oud van Bouwbedrijf De Groot. Wilt u dat ik een betalingsherinnering opstel?",
        "winst": "Uw netto resultaat YTD is **€ 47.750**, een marge van 7.8%. Dit is 12% hoger dan dezelfde periode vorig jaar. De grootste kostenpost is personeel (38% van de omzet).",
        "belasting": "SAGE heeft een fiscale optimalisatie gevonden: door de investeringsaftrek op de nieuwe machines kunt u mogelijk **€ 8.500** besparen. Zal ik een uitgebreide analyse maken?",
        "pipeline": "Je Odoo CRM pipeline staat op **€ 1.461.000** totaal. De gewogen waarde (rekening houdend met kansen) is **€ 533.300**. De deal 'Nieuwbouw Villa Wassenaar' (€285K, 75% kans) is het meest kansrijk.",
        "personeel": "Je hebt momenteel **8 medewerkers** (7.8 FTE). De maandelijkse loonkosten zijn **€ 34.900**. SAGE signaleert dat er nog **€ 2.680** WKR-ruimte over is dit jaar.",
    }
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Stel een vraag aan ALEX..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        response = "Ik begrijp uw vraag. Laat me even in uw gegevens kijken... "
        prompt_lower = prompt.lower()
        
        for keyword, answer in ALEX_RESPONSES.items():
            if keyword in prompt_lower:
                response = answer
                break
        else:
            response = f"Interessante vraag! Op basis van uw administratie en Odoo-data kan ik u vertellen dat {DEMO_CLIENT['name']} er financieel gezond voorstaat. De liquiditeitsratio is 1.8 en de solvabiliteit 42%. Heeft u een specifiekere vraag over uw BTW, cashflow, facturen, pipeline of personeel?"
        
        # Add assistant response
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
    
    # Quick questions
    st.markdown("---")
    st.markdown("**💡 Snelle vragen:**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("💰 Hoeveel BTW?"):
            st.session_state.chat_history.append({"role": "user", "content": "Hoeveel BTW moet ik betalen?"})
            st.session_state.chat_history.append({"role": "assistant", "content": ALEX_RESPONSES["btw"]})
            st.rerun()
    with col2:
        if st.button("📈 Mijn pipeline?"):
            st.session_state.chat_history.append({"role": "user", "content": "Hoe staat mijn pipeline ervoor?"})
            st.session_state.chat_history.append({"role": "assistant", "content": ALEX_RESPONSES["pipeline"]})
            st.rerun()
    with col3:
        if st.button("👥 Personeelskosten?"):
            st.session_state.chat_history.append({"role": "user", "content": "Wat zijn mijn personeelskosten?"})
            st.session_state.chat_history.append({"role": "assistant", "content": ALEX_RESPONSES["personeel"]})
            st.rerun()
    with col4:
        if st.button("💵 Cashflow?"):
            st.session_state.chat_history.append({"role": "user", "content": "Wat is mijn cashflow?"})
            st.session_state.chat_history.append({"role": "assistant", "content": ALEX_RESPONSES["cashflow"]})
            st.rerun()

elif st.session_state.current_view == 'forecast':
    st.title("📈 Forecasting & Scenario's")
    st.markdown("Powered by **LUNA** - Lookout & Understanding for Numerical Analysis")
    st.markdown('<span class="odoo-badge">INCL. CRM PIPELINE DATA</span>', unsafe_allow_html=True)
    
    # Pipeline to Cashflow
    st.subheader("🔮 Pipeline → Cashflow Prognose")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### CRM Pipeline Analyse")
        pipeline_df = pd.DataFrame([
            {"Fase": "Kwalificatie", "Deals": 2, "Waarde": "€ 630.000", "Kans": "25%", "Gewogen": "€ 157.500"},
            {"Fase": "Voorstel", "Deals": 2, "Waarde": "€ 220.000", "Kans": "55%", "Gewogen": "€ 121.000"},
            {"Fase": "Onderhandeling", "Deals": 2, "Waarde": "€ 353.000", "Kans": "77%", "Gewogen": "€ 271.810"},
        ])
        st.dataframe(pipeline_df, hide_index=True, use_container_width=True)
        
        st.metric("Totale gewogen pipeline", "€ 550.310")
    
    with col2:
        st.markdown("### Verwachte inkomsten per kwartaal")
        
        quarters = ['Q1 2024', 'Q2 2024', 'Q3 2024']
        expected = [146000, 280000, 125000]
        
        fig = go.Figure(data=[go.Bar(x=quarters, y=expected, marker_color=['#10b981', '#14b8a6', '#64748b'])])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=250
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    💡 **LUNA Insight:** Op basis van je Odoo CRM pipeline en historische conversiedata verwacht ik 
    **€ 146.000** extra omzet in Q1 2024. De deal 'Nieuwbouw Villa Wassenaar' heeft de hoogste 
    impact op je cashflow. Bij sluiting ontvang je naar verwachting de eerste termijn (30%) = **€ 85.500**.
    """)
    
    st.markdown("---")
    
    # Forecast chart
    st.subheader("📊 Omzetprognose komende 6 maanden")
    
    months = ['Feb', 'Mrt', 'Apr', 'Mei', 'Jun', 'Jul']
    actual = [97500, None, None, None, None, None]
    forecast = [97500, 102000, 98000, 115000, 108000, 95000]
    lower = [97500, 95000, 88000, 100000, 92000, 78000]
    upper = [97500, 109000, 108000, 130000, 124000, 112000]
    
    fig = go.Figure()
    
    # Confidence interval
    fig.add_trace(go.Scatter(
        x=months + months[::-1],
        y=upper + lower[::-1],
        fill='toself',
        fillcolor='rgba(20, 184, 166, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Betrouwbaarheidsinterval'
    ))
    
    # Forecast line
    fig.add_trace(go.Scatter(
        x=months, y=forecast,
        mode='lines+markers',
        name='Prognose',
        line=dict(color='#14b8a6', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Scenario analysis
    st.markdown("---")
    st.subheader("🎭 Scenario Analyse")
    
    scenario = st.selectbox("Kies een scenario:", [
        "Basis scenario",
        "Groei scenario (+20% omzet)",
        "Krimp scenario (-15% omzet)",
        "Nieuwe klant scenario"
    ])
    
    col1, col2, col3 = st.columns(3)
    
    if scenario == "Basis scenario":
        with col1:
            st.metric("Verwachte omzet (12m)", "€ 1.250.000")
        with col2:
            st.metric("Verwacht resultaat", "€ 95.000")
        with col3:
            st.metric("Liquiditeit einde jaar", "€ 180.000")
    elif scenario == "Groei scenario (+20% omzet)":
        with col1:
            st.metric("Verwachte omzet (12m)", "€ 1.500.000", delta="+20%")
        with col2:
            st.metric("Verwacht resultaat", "€ 145.000", delta="+52%")
        with col3:
            st.metric("Liquiditeit einde jaar", "€ 220.000", delta="+22%")
        st.info("💡 LUNA advies: Bij dit groeiscenario is extra werkkapitaal nodig. Overweeg een kredietfaciliteit van €50.000.")
    elif scenario == "Krimp scenario (-15% omzet)":
        with col1:
            st.metric("Verwachte omzet (12m)", "€ 1.062.500", delta="-15%")
        with col2:
            st.metric("Verwacht resultaat", "€ 35.000", delta="-63%")
        with col3:
            st.metric("Liquiditeit einde jaar", "€ 95.000", delta="-47%")
        st.warning("⚠️ LUNA waarschuwing: In dit scenario daalt de liquiditeit onder het gewenste minimum. Kostenreductie van 10% wordt aanbevolen.")
    else:
        with col1:
            st.metric("Verwachte omzet (12m)", "€ 1.400.000", delta="+12%")
        with col2:
            st.metric("Verwacht resultaat", "€ 125.000", delta="+32%")
        with col3:
            st.metric("Liquiditeit einde jaar", "€ 165.000", delta="-8%")
        st.success("✅ LUNA analyse: Nieuwe klant verhoogt omzet maar vereist initiële investering. Break-even na 4 maanden.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 12px; padding: 20px;">
    <p><strong>NOVA Platform</strong> - Demo versie | <span class="odoo-badge">ODOO CONNECTED</span></p>
    <p>De toekomst van accounting, vandaag.</p>
</div>
""", unsafe_allow_html=True)
