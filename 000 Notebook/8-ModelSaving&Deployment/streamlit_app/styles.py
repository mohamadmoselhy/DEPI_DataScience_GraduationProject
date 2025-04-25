"""
Custom styling for the Streamlit app with modern material design.
"""

def apply_custom_styles():
    return """
    <style>
        /* Modern Gradient Background */
        .stApp {
            background: linear-gradient(135deg, #1a1c2c 0%, #0E1117 100%);
        }

        /* Material Design Shadow Mixin */
        @property --shadow-color {
            syntax: '<color>';
            initial-value: rgba(0, 0, 0, 0.1);
            inherits: false;
        }

        /* Glass Effect Mixin */
        .glass-effect {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
        }

        /* Typography System */
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: rgba(255, 255, 255, 0.9);
            line-height: 1.6;
        }

        p, label, .stMarkdown, .stText {
            color: rgba(255, 255, 255, 0.9) !important;
            font-size: 1rem;
            letter-spacing: 0.3px;
        }

        /* Modern Headers */
        h1, h2, h3, h4, h5, h6 {
            color: white !important;
            font-family: 'Inter', sans-serif;
            letter-spacing: -0.5px;
            line-height: 1.2;
        }

        h1 {
            font-size: 2.75rem !important;
            font-weight: 700 !important;
            background: linear-gradient(120deg, #fff, #a5b4fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1.5rem !important;
        }

        h2 {
            font-size: 2rem !important;
            font-weight: 600 !important;
            color: rgba(255, 255, 255, 0.95) !important;
        }

        /* Material Title Box */
        .title-box {
            text-align: center;
            font-size: 2rem;
            font-weight: bold;
            color: white;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(70, 130, 180, 0.1) 100%);
            padding: 1.5rem;
            border-radius: 16px;
            margin: 1rem 0 2rem 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 24px -1px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }

        .title-box:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 32px -1px rgba(0, 0, 0, 0.3);
            border-color: rgba(255, 255, 255, 0.2);
        }

        /* Compact Sidebar Layout */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1A1C24 0%, #141519 100%);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
            padding: 1rem;
            min-width: 350px !important;
            width: 350px !important;
        }

        /* Adjust main content when sidebar is open */
        section[data-testid="stSidebarContent"] {
            max-height: 100vh !important;
            overflow-y: hidden !important;
        }

        /* Grid Layout for Form */
        .stForm > div:first-child {
            display: grid !important;
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 0.5rem !important;
            padding: 0.5rem !important;
        }

        /* Compact Form Elements */
        .stTextInput > div,
        .stNumberInput > div,
        .stSelectbox > div {
            margin: 0.25rem 0 !important;
        }

        /* Reduce spacing in form elements */
        .stTextInput label,
        .stNumberInput label,
        .stSelectbox label {
            font-size: 0.875rem !important;
            margin-bottom: 0.25rem !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }

        /* Compact Input Fields */
        .stTextInput input,
        .stNumberInput input,
        .stSelectbox > div > div,
        .stTextInput > div[data-baseweb="input"] > div,
        .stNumberInput > div[data-baseweb="input"] > div {
            background: #1E1E1E !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 8px !important;
            padding: 0.5rem 0.75rem !important;
            min-height: 36px !important;
            font-size: 0.875rem !important;
        }

        /* Compact Selectbox */
        .stSelectbox > div > div {
            min-height: 36px !important;
        }

        /* Remove extra margins */
        .element-container {
            margin-bottom: 0 !important;
        }

        /* Adjust sidebar header */
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            font-size: 1.1rem !important;
            margin-bottom: 0.5rem !important;
            padding-bottom: 0.25rem !important;
        }

        /* Compact dividers */
        hr {
            margin: 0.5rem 0 !important;
        }

        /* Make submit button stick to bottom */
        .stButton {
            position: sticky !important;
            bottom: 1rem !important;
            padding: 0.5rem !important;
            margin-top: 1rem !important;
        }

        /* Adjust button size */
        .stButton button {
            width: 100% !important;
            padding: 0.5rem !important;
        }

        /* Hide scrollbar but keep functionality */
        [data-testid="stSidebarContent"]::-webkit-scrollbar {
            width: 0px !important;
        }

        /* Compact form sections */
        .stForm > div {
            padding: 0 !important;
        }

        /* Adjust spacing for form groups */
        .stForm > div > div {
            margin-bottom: 0 !important;
        }

        /* Modern Material Buttons */
        .stButton button {
            background: linear-gradient(135deg, #6366f1 0%, #4682B4 100%) !important;
            color: white !important;
            border: none !important;
            padding: 0.75rem 1.5rem !important;
            font-weight: 500 !important;
            border-radius: 12px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 0.875rem;
        }

        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(99, 102, 241, 0.3);
            background: linear-gradient(135deg, #4F46E5 0%, #3A6B99 100%) !important;
        }

        .stButton button:active {
            transform: translateY(0);
            box-shadow: 0 2px 8px rgba(99, 102, 241, 0.2);
        }

        /* Modern Alert Boxes */
        .stSuccess, .stWarning, .stError, .stInfo {
            background: rgba(38, 39, 48, 0.6) !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
            margin: 1rem 0 !important;
        }

        /* Enhanced Help Text and Tooltips */
        .stMarkdown small {
            color: rgba(255, 255, 255, 0.6) !important;
            font-size: 0.875rem;
        }

        .stTooltipIcon {
            color: rgba(255, 255, 255, 0.4) !important;
            transition: color 0.2s ease;
        }

        .stTooltipIcon:hover {
            color: rgba(255, 255, 255, 0.8) !important;
        }

        /* Modern Data Visualization */
        .js-plotly-plot .plotly {
            background: rgba(38, 39, 48, 0.6) !important;
            border-radius: 12px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Modern DataFrames */
        .dataframe {
            border-collapse: separate !important;
            border-spacing: 0 !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            background: rgba(26, 28, 36, 0.6) !important;
            backdrop-filter: blur(10px);
        }

        .dataframe th {
            background: rgba(38, 39, 48, 0.8) !important;
            color: white !important;
            padding: 1rem !important;
            font-weight: 600 !important;
        }

        .dataframe td {
            background: rgba(26, 28, 36, 0.4) !important;
            color: rgba(255, 255, 255, 0.9) !important;
            padding: 0.75rem 1rem !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        }

        /* Layout Optimization */
        .block-container {
            padding: 2rem !important;
            max-width: 1200px !important;
            margin: 0 auto !important;
        }

        /* Language Selector */
        div[data-testid="stSelectbox"] {
            min-width: 140px !important;
            max-width: 140px !important;
        }

        /* RTL Support with Modern Styling */
        .rtl body { 
            direction: rtl; 
            text-align: right; 
        }

        .rtl [data-testid="stSidebar"] *,
        .rtl .stButton > button,
        .rtl .stSelectbox > div > div,
        .rtl .stNumberInput > div > div,
        .rtl label {
            direction: rtl !important;
            text-align: right !important;
        }

        .rtl label { 
            display: block; 
            width: 100%; 
        }

        .rtl .stPlotlyChart, 
        .rtl .stImage, 
        .rtl .stDataFrame {
            direction: ltr !important;
        }

        /* Card Container for Content Sections */
        .content-section {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 1px solid rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }

        .content-section:hover {
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(255, 255, 255, 0.1);
            transform: translateY(-2px);
        }
    </style>
    """ 