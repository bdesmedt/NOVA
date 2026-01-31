import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Page config
st.set_page_config(
    page_title="NOVA Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS voor NOVA styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --navy: #0f172a;
        --teal: #14b8a6;
        --teal-light: #5eead4;
        --slate: #64748b;
        --light: #f8fafc;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        color: white;
    }
    
    .main-header h1 {
        color: #14b8a6;
        margin: 0;
        font-size: 2.5rem;
    }
    
    .main-header p {
        color: #94a3b8;
        margin: 0.5rem 0 0 0;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        border-left: 4px solid #14b8a6;
        color: white;
    }
    
    .kpi-card h3 {
        color: #94a3b8;
        font-size: 0.875rem;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .kpi-card .value {
        color: white;
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .kpi-card .change {
        font-size: 0.875rem;
    }
    
    .change.positive { color: #4ade80; }
    .change.negative { color: #f87171; }
    
    /* Agent cards */
    .agent-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 1rem;
    }
    
    .agent-status {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .status-active { background: #065f46; color: #6ee7b7; }
    .status-processing { background: #1e40af; color: #93c5fd; }
    .status-standby { background: #374151; color: #9ca3af; }
    
    /* Chat styling */
    .chat-message {
        padding: 1rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
    }
    
    .chat-user {
        background: #1e293b;
        color: white;
        margin-left: 2rem;
    }
    
    .chat-agent {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border-left: 4px solid #14b8a6;
        color: white;
        margin-right: 2rem;
    }
    
    /* Invoice styling */
    .invoice-item {
        background: #1e293b;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        color: white;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Improve sidebar */
    .css-1d391kg {
        background: #0f172a;
    }
    
    /* Table styling */
    .dataframe {
        font-size: 0.875rem;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'processed_invoices' not in st.session_state:
    st.session_state.processed_invoices = []

# Demo data
COMPANY = {
    'name': 'Vermeer Bouw B.V.',
    'owner': 'Jan Vermeer',
    'kvk': '12345678',
    'sector': 'Bouw & Constructie'
}

# Demo financials (RGS-based)
BALANS_DATA = {
    'ACTIVA': {
        'Vaste Activa': {
            'Immateriële vaste activa (BIva)': {
                'Goodwill': 50000,
                'Software': 25000,
            },
            'Materiële vaste activa (BMva)': {
                'Bedrijfsgebouwen': 450000,
                'Machines en installaties': 180000,
                'Transportmiddelen': 95000,
                'Inventaris': 35000,
            },
            'Financiële vaste activa (BFva)': {
                'Deelnemingen': 25000,
                'Leningen u/g': 15000,
            },
        },
        'Vlottende Activa': {
            'Voorraden (BVrd)': {
                'Grond- en hulpstoffen': 45000,
                'Onderhanden werk': 125000,
                'Gereed product': 30000,
            },
            'Vorderingen (BVor)': {
                'Debiteuren': 285000,
                'Overige vorderingen': 18000,
                'Vooruitbetaalde kosten': 12000,
            },
            'Liquide middelen (BLim)': {
                'Bankrekeningen': 142000,
                'Kas': 3000,
            },
        },
    },
    'PASSIVA': {
        'Eigen Vermogen': {
            'Eigen vermogen (BEiv)': {
                'Gestort kapitaal': 100000,
                'Algemene reserve': 285000,
                'Onverdeelde winst': 89000,
            },
        },
        'Voorzieningen': {
            'Voorzieningen (BVrz)': {
                'Pensioenvoorziening': 45000,
                'Garantievoorziening': 25000,
            },
        },
        'Langlopende Schulden': {
            'Langlopende schulden (BLas)': {
                'Hypothecaire leningen': 320000,
                'Bankleningen': 150000,
            },
        },
        'Kortlopende Schulden': {
            'Kortlopende schulden (BKas)': {
                'Crediteuren': 165000,
                'Belastingen en premies': 48000,
                'Overige schulden': 32000,
                'Overlopende passiva': 25000,
            },
        },
    }
}

WINST_VERLIES_DATA = {
    'Netto-omzet (WOmz)': {
        'Omzet projecten': 1850000,
        'Omzet onderhoud': 420000,
        'Omzet advies': 95000,
    },
    'Kostprijs omzet (WKpr)': {
        'Inkoopkosten materialen': -680000,
        'Kosten uitbesteed werk': -425000,
        'Directe personeelskosten': -380000,
    },
    'Overige bedrijfsopbrengsten (WOvb)': {
        'Ontvangen subsidies': 15000,
        'Overige opbrengsten': 8000,
    },
    'Bedrijfskosten': {
        'Personeelskosten (WPer)': {
            'Lonen en salarissen': -285000,
            'Sociale lasten': -58000,
            'Pensioenlasten': -42000,
            'Overige personeelskosten': -18000,
        },
        'Afschrijvingen (WAfs)': {
            'Afschrijving MVA': -65000,
            'Afschrijving IVA': -12000,
        },
        'Huisvestingskosten (WHui)': {
            'Huur': -48000,
            'Energie': -24000,
            'Onderhoud gebouwen': -15000,
        },
        'Verkoopkosten (WVkk)': {
            'Reclame en marketing': -28000,
            'Representatiekosten': -12000,
        },
        'Algemene kosten (WAlg)': {
            'Administratiekosten': -22000,
            'Accountants- en advieskosten': -35000,
            'Verzekeringen': -18000,
            'Kantoorkosten': -15000,
        },
    },
    'Financiële baten en lasten (WFbe)': {
        'Rentebaten': 2000,
        'Rentelasten': -38000,
    },
}

# AI Agents
AGENTS = [
    {
        'name': 'ARIA',
        'full_name': 'AI Recognition & Invoice Assistant',
        'role': 'Factuurverwerking',
        'status': 'active',
        'processed_today': 47,
        'accuracy': 99.2,
        'description': 'Automatische herkenning en verwerking van inkoopfacturen met RGS-codering.',
        'icon': '📄'
    },
    {
        'name': 'NOVA',
        'full_name': 'Numerical Operations & Verification Agent',
        'role': 'Document Analyse',
        'status': 'active',
        'processed_today': 23,
        'accuracy': 98.7,
        'description': 'Classificatie en data-extractie uit alle soorten documenten.',
        'icon': '📋'
    },
    {
        'name': 'SAGE',
        'full_name': 'Strategic Advisory & Guidance Engine',
        'role': 'Fiscaal Advies',
        'status': 'standby',
        'processed_today': 8,
        'accuracy': 97.5,
        'description': 'Proactief fiscaal advies en optimalisatie-suggesties.',
        'icon': '💡'
    },
    {
        'name': 'LUNA',
        'full_name': 'Lookout & Understanding for Numerical Analysis',
        'role': 'Forecasting',
        'status': 'processing',
        'processed_today': 12,
        'accuracy': 94.8,
        'description': 'Cashflow-prognoses en scenario-analyses.',
        'icon': '🔮'
    },
    {
        'name': 'ALEX',
        'full_name': 'Advisory Liaison & Expert eXchange',
        'role': 'Client Support',
        'status': 'active',
        'processed_today': 156,
        'accuracy': 96.3,
        'description': 'Beantwoording van vragen en uitleg over financiële data.',
        'icon': '💬'
    },
]

# Demo invoices
DEMO_INVOICES = [
    {'nummer': 'INV-2024-0892', 'leverancier': 'Bouwmaterialen De Groot', 'bedrag': 4250.00, 'datum': '28-01-2024', 'status': 'Verwerkt', 'rgs': 'WKpr - Inkoopkosten materialen'},
    {'nummer': 'INV-2024-0891', 'leverancier': 'Van Dijk Transport', 'bedrag': 1875.50, 'datum': '27-01-2024', 'status': 'Verwerkt', 'rgs': 'WKpr - Kosten uitbesteed werk'},
    {'nummer': 'INV-2024-0890', 'leverancier': 'Energiedirect', 'bedrag': 892.30, 'datum': '26-01-2024', 'status': 'Verwerkt', 'rgs': 'WHui - Energie'},
    {'nummer': 'INV-2024-0889', 'leverancier': 'Office Supplies BV', 'bedrag': 245.80, 'datum': '25-01-2024', 'status': 'Review nodig', 'rgs': 'WAlg - Kantoorkosten'},
    {'nummer': 'INV-2024-0888', 'leverancier': 'Verzekeringsmaatschappij Centraal', 'bedrag': 3200.00, 'datum': '24-01-2024', 'status': 'Verwerkt', 'rgs': 'WAlg - Verzekeringen'},
]

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h1 style="color: #14b8a6; margin: 0;">🚀 NOVA</h1>
        <p style="color: #64748b; font-size: 0.875rem;">Platform Demo</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Company info
    st.markdown(f"""
    <div style="background: #1e293b; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
        <p style="color: #94a3b8; margin: 0; font-size: 0.75rem;">INGELOGD ALS</p>
        <p style="color: white; margin: 0.25rem 0 0 0; font-weight: 600;">{COMPANY['owner']}</p>
        <p style="color: #64748b; margin: 0; font-size: 0.875rem;">{COMPANY['name']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    page = st.radio(
        "Navigatie",
        ["🎯 Dashboard", "📄 Facturen", "📊 Winst & Verlies", "⚖️ Balans", "🤖 AI Agents", "💬 Chat met ALEX", "📈 Forecasting"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Quick stats
    st.markdown("### 📊 Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Agents actief", "4/5")
    with col2:
        st.metric("Taken vandaag", "246")

# Main content based on navigation
if page == "🎯 Dashboard":
    # Header
    st.markdown(f"""
    <div class="main-header">
        <h1>🚀 Welkom, {COMPANY['owner'].split()[0]}</h1>
        <p>{COMPANY['name']} • Financieel overzicht januari 2024</p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="kpi-card">
            <h3>Omzet YTD</h3>
            <div class="value">€ 2.365.000</div>
            <div class="change positive">↑ 12.4% vs vorig jaar</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="kpi-card">
            <h3>Bruto Marge</h3>
            <div class="value">38.2%</div>
            <div class="change positive">↑ 2.1% vs vorig jaar</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="kpi-card">
            <h3>Openstaand</h3>
            <div class="value">€ 285.000</div>
            <div class="change negative">↓ 23 facturen open</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="kpi-card">
            <h3>Cashflow Forecast</h3>
            <div class="value">€ 89.000</div>
            <div class="change positive">↑ Positief komende 30d</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Omzet vs Kosten (6 maanden)")
        
        months = ['Aug', 'Sep', 'Okt', 'Nov', 'Dec', 'Jan']
        omzet = [185000, 210000, 195000, 225000, 240000, 215000]
        kosten = [142000, 158000, 148000, 168000, 175000, 162000]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=omzet, name='Omzet', line=dict(color='#14b8a6', width=3)))
        fig.add_trace(go.Scatter(x=months, y=kosten, name='Kosten', line=dict(color='#f87171', width=3)))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8',
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
            margin=dict(l=0, r=0, t=30, b=0),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 💰 Cashflow Prognose (weken)")
        
        weeks = ['Week 5', 'Week 6', 'Week 7', 'Week 8', 'Week 9', 'Week 10']
        cashflow = [142000, 128000, 155000, 148000, 172000, 185000]
        colors = ['#14b8a6' if c > 140000 else '#f59e0b' for c in cashflow]
        
        fig = go.Figure(data=[go.Bar(x=weeks, y=cashflow, marker_color=colors)])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8',
            margin=dict(l=0, r=0, t=30, b=0),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity & Tasks
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🤖 AI Agent Activiteit")
        for agent in AGENTS[:3]:
            status_class = f"status-{agent['status']}"
            st.markdown(f"""
            <div style="background: #1e293b; padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="font-size: 1.25rem;">{agent['icon']}</span>
                    <strong style="color: white; margin-left: 0.5rem;">{agent['name']}</strong>
                    <span style="color: #64748b; margin-left: 0.5rem;">{agent['role']}</span>
                </div>
                <div>
                    <span style="color: #14b8a6;">{agent['processed_today']} verwerkt</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### ✅ Openstaande Taken")
        tasks = [
            ('BTW-aangifte Q4 2023', 'Deadline: 31 jan', 'urgent'),
            ('Jaarrekening review', 'In behandeling', 'normal'),
            ('Factuur #0889 goedkeuren', 'Review nodig', 'normal'),
            ('Loonadministratie januari', 'Gepland: 25 jan', 'done'),
        ]
        for task, status, priority in tasks:
            color = '#f87171' if priority == 'urgent' else '#14b8a6' if priority == 'done' else '#94a3b8'
            icon = '🔴' if priority == 'urgent' else '✅' if priority == 'done' else '⏳'
            st.markdown(f"""
            <div style="background: #1e293b; padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.5rem;">
                <span>{icon}</span>
                <span style="color: white; margin-left: 0.5rem;">{task}</span>
                <span style="color: {color}; float: right; font-size: 0.875rem;">{status}</span>
            </div>
            """, unsafe_allow_html=True)

elif page == "📄 Facturen":
    st.markdown("""
    <div class="main-header">
        <h1>📄 Factuurverwerking</h1>
        <p>AI-gestuurde herkenning en RGS-codering door ARIA</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Upload section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📤 Upload Factuur")
        uploaded_file = st.file_uploader("Sleep een factuur hierheen of klik om te uploaden", type=['pdf', 'jpg', 'png'])
        
        if uploaded_file:
            with st.spinner('🤖 ARIA analyseert de factuur...'):
                import time
                time.sleep(2)
            
            # Simulated AI extraction
            st.success('✅ Factuur succesvol geanalyseerd!')
            
            st.markdown("### 🔍 Geëxtraheerde Gegevens")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.text_input("Leverancier", value="Bouwmaterialen De Groot", key="lev")
                st.text_input("Factuurnummer", value="INV-2024-0893", key="inv")
                st.date_input("Factuurdatum", value=datetime.now())
            
            with col_b:
                st.number_input("Bedrag excl. BTW", value=3250.00, format="%.2f")
                st.number_input("BTW", value=682.50, format="%.2f")
                st.selectbox("RGS Code", ["WKpr - Inkoopkosten materialen", "WKpr - Kosten uitbesteed werk", "WHui - Onderhoud"], key="rgs_select")
            
            st.markdown("#### 📝 Regeldetails")
            lines_df = pd.DataFrame({
                'Omschrijving': ['Cement 25kg x 40', 'Bakstenen rood 1000st', 'Bezorgkosten'],
                'Aantal': [40, 1000, 1],
                'Prijs': [12.50, 0.45, 75.00],
                'Totaal': [500.00, 450.00, 75.00],
                'RGS': ['WKpr', 'WKpr', 'WKpr']
            })
            st.dataframe(lines_df, use_container_width=True, hide_index=True)
            
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            with col_btn1:
                if st.button("✅ Goedkeuren & Boeken", type="primary"):
                    st.balloons()
                    st.success("Factuur geboekt in grootboek!")
            with col_btn2:
                if st.button("✏️ Handmatig aanpassen"):
                    st.info("Bewerkmodus geactiveerd")
            with col_btn3:
                if st.button("❌ Afwijzen"):
                    st.warning("Factuur gemarkeerd voor review")
    
    with col2:
        st.markdown("### 📊 ARIA Stats")
        st.markdown("""
        <div class="kpi-card">
            <h3>Vandaag verwerkt</h3>
            <div class="value">47</div>
            <div class="change positive">99.2% accuracy</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="kpi-card">
            <h3>Wachtrij</h3>
            <div class="value">3</div>
            <div class="change">~5 min verwerkingstijd</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent invoices
    st.markdown("### 📋 Recent Verwerkte Facturen")
    
    inv_df = pd.DataFrame(DEMO_INVOICES)
    inv_df.columns = ['Nummer', 'Leverancier', 'Bedrag', 'Datum', 'Status', 'RGS Code']
    inv_df['Bedrag'] = inv_df['Bedrag'].apply(lambda x: f"€ {x:,.2f}")
    
    st.dataframe(inv_df, use_container_width=True, hide_index=True)

elif page == "📊 Winst & Verlies":
    st.markdown("""
    <div class="main-header">
        <h1>📊 Winst & Verlies Rekening</h1>
        <p>Periode: januari 2024 • RGS-gecodeerd</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Period selector
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.selectbox("Periode", ["Januari 2024", "Q4 2023", "Heel 2023"], key="pnl_period")
    with col2:
        st.selectbox("Vergelijk met", ["Vorig jaar", "Budget", "Geen"], key="pnl_compare")
    
    # Calculate totals
    def calc_section(data):
        total = 0
        for key, value in data.items():
            if isinstance(value, dict):
                total += calc_section(value)
            else:
                total += value
        return total
    
    netto_omzet = calc_section(WINST_VERLIES_DATA['Netto-omzet (WOmz)'])
    kostprijs = calc_section(WINST_VERLIES_DATA['Kostprijs omzet (WKpr)'])
    bruto_marge = netto_omzet + kostprijs
    overige_opbrengsten = calc_section(WINST_VERLIES_DATA['Overige bedrijfsopbrengsten (WOvb)'])
    bedrijfskosten = calc_section(WINST_VERLIES_DATA['Bedrijfskosten'])
    financieel = calc_section(WINST_VERLIES_DATA['Financiële baten en lasten (WFbe)'])
    
    resultaat_voor_belasting = bruto_marge + overige_opbrengsten + bedrijfskosten + financieel
    belasting = -resultaat_voor_belasting * 0.25
    netto_resultaat = resultaat_voor_belasting + belasting
    
    # Display P&L
    st.markdown("### Netto-omzet")
    for item, value in WINST_VERLIES_DATA['Netto-omzet (WOmz)'].items():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{item}")
        with col2:
            st.markdown(f"**€ {value:,.0f}**")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("**Totaal netto-omzet**")
    with col2:
        st.markdown(f"**€ {netto_omzet:,.0f}**")
    
    st.divider()
    
    st.markdown("### Kostprijs omzet")
    for item, value in WINST_VERLIES_DATA['Kostprijs omzet (WKpr)'].items():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{item}")
        with col2:
            st.markdown(f"€ {value:,.0f}")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("**Bruto marge**")
    with col2:
        st.markdown(f"**€ {bruto_marge:,.0f}** ({bruto_marge/netto_omzet*100:.1f}%)")
    
    st.divider()
    
    st.markdown("### Bedrijfskosten")
    for category, items in WINST_VERLIES_DATA['Bedrijfskosten'].items():
        st.markdown(f"**{category}**")
        for item, value in items.items():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{item}")
            with col2:
                st.markdown(f"€ {value:,.0f}")
    
    st.divider()
    
    # Summary box
    st.markdown("""
    <div class="kpi-card">
        <h3>NETTO RESULTAAT</h3>
        <div class="value" style="color: #4ade80;">€ {:,.0f}</div>
        <div class="change positive">Marge: {:.1f}%</div>
    </div>
    """.format(netto_resultaat, netto_resultaat/netto_omzet*100), unsafe_allow_html=True)

elif page == "⚖️ Balans":
    st.markdown("""
    <div class="main-header">
        <h1>⚖️ Balans</h1>
        <p>Stand per 31 januari 2024 • RGS-gecodeerd</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## ACTIVA")
        
        totaal_activa = 0
        for hoofdcategorie, subcats in BALANS_DATA['ACTIVA'].items():
            st.markdown(f"### {hoofdcategorie}")
            subtotaal = 0
            for subcat, items in subcats.items():
                st.markdown(f"**{subcat}**")
                for item, value in items.items():
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{item}")
                    with col_b:
                        st.markdown(f"€ {value:,.0f}")
                    subtotaal += value
            st.markdown(f"**Subtotaal: € {subtotaal:,.0f}**")
            totaal_activa += subtotaal
            st.divider()
        
        st.markdown(f"## **TOTAAL ACTIVA: € {totaal_activa:,.0f}**")
    
    with col2:
        st.markdown("## PASSIVA")
        
        totaal_passiva = 0
        for hoofdcategorie, subcats in BALANS_DATA['PASSIVA'].items():
            st.markdown(f"### {hoofdcategorie}")
            subtotaal = 0
            for subcat, items in subcats.items():
                st.markdown(f"**{subcat}**")
                for item, value in items.items():
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{item}")
                    with col_b:
                        st.markdown(f"€ {value:,.0f}")
                    subtotaal += value
            st.markdown(f"**Subtotaal: € {subtotaal:,.0f}**")
            totaal_passiva += subtotaal
            st.divider()
        
        st.markdown(f"## **TOTAAL PASSIVA: € {totaal_passiva:,.0f}**")
    
    # Balance check
    if totaal_activa == totaal_passiva:
        st.success(f"✅ Balans is in evenwicht: € {totaal_activa:,.0f}")
    else:
        st.error(f"⚠️ Balansverschil: € {abs(totaal_activa - totaal_passiva):,.0f}")

elif page == "🤖 AI Agents":
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Agents</h1>
        <p>Jouw digitale collega's — altijd beschikbaar, continu lerend</p>
    </div>
    """, unsafe_allow_html=True)
    
    for agent in AGENTS:
        status_colors = {
            'active': ('#065f46', '#6ee7b7', '🟢 Actief'),
            'processing': ('#1e40af', '#93c5fd', '🔵 Bezig'),
            'standby': ('#374151', '#9ca3af', '⚪ Stand-by')
        }
        bg, fg, status_text = status_colors[agent['status']]
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div class="agent-card">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <span style="font-size: 2.5rem;">{agent['icon']}</span>
                    <div>
                        <h3 style="color: #14b8a6; margin: 0;">{agent['name']}</h3>
                        <p style="color: #64748b; margin: 0; font-size: 0.875rem;">{agent['full_name']}</p>
                        <p style="color: white; margin: 0.5rem 0 0 0;">{agent['description']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.metric("Verwerkt vandaag", agent['processed_today'])
        
        with col3:
            st.metric("Nauwkeurigheid", f"{agent['accuracy']}%")
        
        st.divider()
    
    # Agent collaboration example
    st.markdown("### 🔄 Agent Samenwerking Voorbeeld")
    st.markdown("""
    <div style="background: #1e293b; padding: 1.5rem; border-radius: 1rem;">
        <p style="color: white;"><strong>Scenario:</strong> Factuur komt binnen van nieuwe leverancier</p>
        <br>
        <div style="display: flex; gap: 1rem; align-items: center; flex-wrap: wrap;">
            <div style="background: #0f172a; padding: 1rem; border-radius: 0.5rem; text-align: center;">
                <span style="font-size: 1.5rem;">📄</span>
                <p style="color: #14b8a6; margin: 0.5rem 0 0 0;">ARIA</p>
                <p style="color: #64748b; margin: 0; font-size: 0.75rem;">Herkent & extraheert</p>
            </div>
            <span style="color: #14b8a6; font-size: 1.5rem;">→</span>
            <div style="background: #0f172a; padding: 1rem; border-radius: 0.5rem; text-align: center;">
                <span style="font-size: 1.5rem;">📋</span>
                <p style="color: #14b8a6; margin: 0.5rem 0 0 0;">NOVA</p>
                <p style="color: #64748b; margin: 0; font-size: 0.75rem;">Classificeert document</p>
            </div>
            <span style="color: #14b8a6; font-size: 1.5rem;">→</span>
            <div style="background: #0f172a; padding: 1rem; border-radius: 0.5rem; text-align: center;">
                <span style="font-size: 1.5rem;">💡</span>
                <p style="color: #14b8a6; margin: 0.5rem 0 0 0;">SAGE</p>
                <p style="color: #64748b; margin: 0; font-size: 0.75rem;">Checkt BTW-regels</p>
            </div>
            <span style="color: #14b8a6; font-size: 1.5rem;">→</span>
            <div style="background: #0f172a; padding: 1rem; border-radius: 0.5rem; text-align: center;">
                <span style="font-size: 1.5rem;">🔮</span>
                <p style="color: #14b8a6; margin: 0.5rem 0 0 0;">LUNA</p>
                <p style="color: #64748b; margin: 0; font-size: 0.75rem;">Update cashflow</p>
            </div>
            <span style="color: #14b8a6; font-size: 1.5rem;">→</span>
            <div style="background: #0f172a; padding: 1rem; border-radius: 0.5rem; text-align: center;">
                <span style="font-size: 1.5rem;">💬</span>
                <p style="color: #14b8a6; margin: 0.5rem 0 0 0;">ALEX</p>
                <p style="color: #64748b; margin: 0; font-size: 0.75rem;">Notificeert klant</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif page == "💬 Chat met ALEX":
    st.markdown("""
    <div class="main-header">
        <h1>💬 Chat met ALEX</h1>
        <p>Advisory Liaison & Expert eXchange — Stel je financiële vragen</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat container
    chat_container = st.container()
    
    # Predefined responses
    ALEX_RESPONSES = {
        'btw': """Op basis van je administratie zie ik het volgende voor de BTW-aangifte Q4 2023:

📊 **BTW Overzicht Q4 2023**
- Verschuldigde BTW (verkopen): € 49.350
- Voorbelasting (inkopen): € 38.420
- **Te betalen: € 10.930**

⏰ De deadline is 31 januari. Wil je dat ik de aangifte voorbereid?""",
        
        'cashflow': """Hier is je cashflow-analyse voor de komende 30 dagen:

💰 **Cashflow Prognose**
- Huidige stand: € 145.000
- Verwachte inkomsten: € 185.000
- Verwachte uitgaven: € 142.000
- **Verwacht saldo: € 188.000**

✅ Je liquiditeit ziet er gezond uit. Er zijn geen knelpunten verwacht.""",
        
        'factuur': """Ik zie dat factuur #0889 van Office Supplies een review nodig heeft.

📄 **Factuur Details**
- Leverancier: Office Supplies BV
- Bedrag: € 245,80
- ARIA confidence: 87%

⚠️ De RGS-code kon niet met zekerheid worden bepaald. Opties:
1. WAlg - Kantoorkosten
2. WVkk - Representatiekosten

Welke is correct?""",
        
        'default': """Bedankt voor je vraag! Ik help je graag verder.

Ik kan je helpen met:
- 📊 BTW-aangiftes en deadlines
- 💰 Cashflow analyses en prognoses
- 📄 Factuurstatus en goedkeuringen
- 📈 Financiële rapportages
- 💡 Fiscaal advies

Waar kan ik je mee helpen?"""
    }
    
    # Display chat history
    with chat_container:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="chat-message chat-user">
                    <strong>Jij:</strong><br>{message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message chat-agent">
                    <strong>🤖 ALEX:</strong><br>{message['content']}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Stel een vraag aan ALEX...")
    
    if user_input:
        # Add user message
        st.session_state.chat_history.append({'role': 'user', 'content': user_input})
        
        # Generate response based on keywords
        response = ALEX_RESPONSES['default']
        user_lower = user_input.lower()
        if 'btw' in user_lower or 'aangifte' in user_lower:
            response = ALEX_RESPONSES['btw']
        elif 'cashflow' in user_lower or 'liquiditeit' in user_lower or 'cash' in user_lower:
            response = ALEX_RESPONSES['cashflow']
        elif 'factuur' in user_lower or '0889' in user_lower:
            response = ALEX_RESPONSES['factuur']
        
        st.session_state.chat_history.append({'role': 'assistant', 'content': response})
        st.rerun()
    
    # Quick actions
    st.markdown("### ⚡ Snelle Vragen")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 BTW-aangifte status"):
            st.session_state.chat_history.append({'role': 'user', 'content': 'Wat is de status van mijn BTW-aangifte?'})
            st.session_state.chat_history.append({'role': 'assistant', 'content': ALEX_RESPONSES['btw']})
            st.rerun()
    with col2:
        if st.button("💰 Cashflow prognose"):
            st.session_state.chat_history.append({'role': 'user', 'content': 'Hoe ziet mijn cashflow eruit?'})
            st.session_state.chat_history.append({'role': 'assistant', 'content': ALEX_RESPONSES['cashflow']})
            st.rerun()
    with col3:
        if st.button("📄 Openstaande facturen"):
            st.session_state.chat_history.append({'role': 'user', 'content': 'Zijn er facturen die aandacht nodig hebben?'})
            st.session_state.chat_history.append({'role': 'assistant', 'content': ALEX_RESPONSES['factuur']})
            st.rerun()

elif page == "📈 Forecasting":
    st.markdown("""
    <div class="main-header">
        <h1>📈 Forecasting & Scenario's</h1>
        <p>Powered by LUNA — Kijk vooruit met data-gedreven prognoses</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Scenario selector
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### ⚙️ Scenario Parameters")
        
        omzet_groei = st.slider("Omzetgroei (%)", -20, 30, 10)
        kosten_stijging = st.slider("Kostenstijging (%)", -10, 20, 5)
        investering = st.number_input("Extra investering (€)", 0, 500000, 0, step=10000)
        
        scenario = st.selectbox("Voorgedefinieerd scenario", [
            "Aangepast",
            "🟢 Optimistisch (+15% groei)",
            "🟡 Basis (huidige trend)", 
            "🔴 Conservatief (-5% groei)"
        ])
        
        if scenario == "🟢 Optimistisch (+15% groei)":
            omzet_groei, kosten_stijging = 15, 3
        elif scenario == "🟡 Basis (huidige trend)":
            omzet_groei, kosten_stijging = 8, 5
        elif scenario == "🔴 Conservatief (-5% groei)":
            omzet_groei, kosten_stijging = -5, 8
    
    with col2:
        st.markdown("### 📊 12-Maanden Prognose")
        
        # Generate forecast data
        months = ['Feb', 'Mrt', 'Apr', 'Mei', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dec', 'Jan']
        base_omzet = 200000
        base_kosten = 155000
        
        omzet_forecast = [base_omzet * (1 + omzet_groei/100 * (i/12)) for i in range(1, 13)]
        kosten_forecast = [base_kosten * (1 + kosten_stijging/100 * (i/12)) for i in range(1, 13)]
        winst_forecast = [o - k for o, k in zip(omzet_forecast, kosten_forecast)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=omzet_forecast, name='Omzet', fill='tonexty', line=dict(color='#14b8a6', width=3)))
        fig.add_trace(go.Scatter(x=months, y=kosten_forecast, name='Kosten', line=dict(color='#f87171', width=2, dash='dash')))
        fig.add_trace(go.Bar(x=months, y=winst_forecast, name='Winst', marker_color='#22c55e', opacity=0.5))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8',
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
            margin=dict(l=0, r=0, t=40, b=0),
            height=400,
            barmode='overlay'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Summary metrics
    st.markdown("### 📋 Scenario Samenvatting")
    
    total_omzet = sum(omzet_forecast)
    total_kosten = sum(kosten_forecast)
    total_winst = sum(winst_forecast)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>Verwachte Omzet</h3>
            <div class="value">€ {total_omzet/1000000:.2f}M</div>
            <div class="change {'positive' if omzet_groei > 0 else 'negative'}">{'↑' if omzet_groei > 0 else '↓'} {abs(omzet_groei)}% groei</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>Verwachte Kosten</h3>
            <div class="value">€ {total_kosten/1000000:.2f}M</div>
            <div class="change {'negative' if kosten_stijging > 0 else 'positive'}">{'↑' if kosten_stijging > 0 else '↓'} {abs(kosten_stijging)}% stijging</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        marge = (total_winst / total_omzet) * 100
        st.markdown(f"""
        <div class="kpi-card">
            <h3>Verwachte Winst</h3>
            <div class="value">€ {total_winst/1000:.0f}K</div>
            <div class="change {'positive' if marge > 15 else 'negative'}">{marge:.1f}% marge</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>Break-even</h3>
            <div class="value">Mrt '24</div>
            <div class="change positive">Op schema</div>
        </div>
        """, unsafe_allow_html=True)
    
    # LUNA insights
    st.markdown("### 💡 LUNA Insights")
    st.info("""
    🔮 **Automatische analyse op basis van je scenario:**
    
    - Bij {0}% omzetgroei bereik je een jaaromzet van € {1:.2f}M
    - Je huidige marge van {2:.1f}% is {3} het branchegemiddelde (32%)
    - Aanbeveling: {4}
    """.format(
        omzet_groei,
        total_omzet/1000000,
        marge,
        "boven" if marge > 32 else "onder",
        "Focus op omzetgroei, je kostenbasis is efficiënt." if marge > 32 else "Overweeg kostenoptimalisatie om marge te verbeteren."
    ))

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 1rem;">
    <p>🚀 NOVA Platform Demo • Conceptuele weergave voor presentatiedoeleinden</p>
    <p style="font-size: 0.75rem;">© 2024 — De toekomst van accounting</p>
</div>
""", unsafe_allow_html=True)
