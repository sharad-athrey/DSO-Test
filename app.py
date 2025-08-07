import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar

# Page configuration
st.set_page_config(
    page_title="DSO Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
/* Main app background - light gray for better contrast */
.stApp {
    background-color: #f8f9fa !important;
}

/* Ensure text is dark and visible */
.stApp .main .block-container {
    background-color: #ffffff !important;
    color: #333333 !important;
    padding: 2rem 1rem;
    border-radius: 10px;
    margin-top: 1rem;
}

/* Sidebar styling - light blue background */
.css-1d391kg, section[data-testid="stSidebar"] {
    background-color: #e3f2fd !important;
}

/* Headers and text styling */
h1, h2, h3, h4, h5, h6, p, div, span, label {
    color: #333333 !important;
}

/* Sidebar text styling */
.css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3, 
.css-1d391kg p, .css-1d391kg div, .css-1d391kg span,
.css-1d391kg label {
    color: #1565c0 !important;
}

/* Fix selectbox styling */
.stSelectbox > div > div {
    background-color: white !important;
    color: #333333 !important;
    border: 1px solid #e0e0e0 !important;
}

/* Fix selectbox in sidebar */
.css-1d391kg .stSelectbox > div > div {
    background-color: white !important;
    color: #333333 !important;
    border: 1px solid #90caf9 !important;
}

/* Fix selectbox labels */
.stSelectbox label, .css-1d391kg .stSelectbox label {
    color: #1565c0 !important;
    background-color: transparent !important;
}

/* Fix multiselect styling */
.stMultiSelect > div > div {
    background-color: white !important;
    color: #333333 !important;
    border: 1px solid #e0e0e0 !important;
}

/* Fix multiselect in sidebar */
.css-1d391kg .stMultiSelect > div > div {
    background-color: white !important;
    color: #333333 !important;
    border: 1px solid #90caf9 !important;
}

/* Fix multiselect labels */
.stMultiSelect label, .css-1d391kg .stMultiSelect label {
    color: #1565c0 !important;
    background-color: transparent !important;
}

/* Fix dropdown menus */
.css-1d391kg div[data-baseweb="select"] > div,
.css-1d391kg div[data-baseweb="select"] div {
    background-color: white !important;
    color: #333333 !important;
}

/* Fix multiselect tags */
.css-1d391kg .stMultiSelect [data-baseweb="tag"] {
    background-color: #e3f2fd !important;
    color: #1565c0 !important;
    border: 1px solid #90caf9 !important;
}

/* Fix dropdown options */
div[role="option"] {
    background-color: white !important;
    color: #333333 !important;
}

div[role="option"]:hover {
    background-color: #f5f5f5 !important;
    color: #333333 !important;
}

/* Fix any remaining dark inputs */
input, select, textarea {
    background-color: white !important;
    color: #333333 !important;
    border: 1px solid #e0e0e0 !important;
}

/* Sidebar inputs */
.css-1d391kg input, .css-1d391kg select, .css-1d391kg textarea {
    background-color: white !important;
    color: #333333 !important;
    border: 1px solid #90caf9 !important;
}

/* Metric cards */
.metric-card {
    background: white !important;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    border-left: 4px solid #667eea;
    color: #333333 !important;
}

/* Button styling */
.stButton > button {
    background-color: #667eea !important;
    color: white !important;
    border-radius: 5px;
    border: none;
    padding: 0.5rem 1rem;
}

.stButton > button:hover {
    background-color: #5a6fd8 !important;
}

/* Date info box */
.date-info {
    background-color: #bbdefb !important;
    border: 1px solid #90caf9;
    padding: 12px;
    border-radius: 8px;
    margin: 10px 0;
    font-size: 14px;
    color: #1565c0 !important;
}

/* Metrics styling */
[data-testid="metric-container"] {
    background-color: white !important;
    border: 1px solid #e0e0e0;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

[data-testid="metric-container"] * {
    color: #333333 !important;
}

/* Expander styling */
.streamlit-expanderHeader {
    background-color: #f8f9fa !important;
    color: #333333 !important;
}

.streamlit-expanderContent {
    background-color: white !important;
    color: #333333 !important;
}

/* Info/warning/success message styling */
.stAlert {
    color: #333333 !important;
    background-color: white !important;
}

.stInfo {
    background-color: #e3f2fd !important;
    color: #1565c0 !important;
}

.stSuccess {
    background-color: #e8f5e8 !important;
    color: #2e7d32 !important;
}

.stWarning {
    background-color: #fff3e0 !important;
    color: #f57c00 !important;
}

/* Chart backgrounds */
.plotly, .js-plotly-plot {
    background-color: white !important;
}

/* Fix any remaining dark elements */
* {
    color: inherit !important;
}

/* Override Streamlit's default dark theme */
.css-1d391kg * {
    background-color: inherit !important;
}

/* Ensure all dropdown components are white */
div[data-baseweb="select"] {
    background-color: white !important;
}

div[data-baseweb="select"] > div {
    background-color: white !important;
    color: #333333 !important;
}

/* Fix the dropdown arrow and controls */
.css-1d391kg div[data-baseweb="select"] svg {
    fill: #1565c0 !important;
}

/* Fix any popover menus */
div[data-baseweb="popover"] {
    background-color: white !important;
}

div[data-baseweb="popover"] * {
    background-color: white !important;
    color: #333333 !important;
}
</style>
""", unsafe_allow_html=True)

# Sample data generation
@st.cache_data
def generate_sample_data():
    # Generate data for a full year including current dates
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)  # Extended to cover current date
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Generate more realistic DSO data with trends
    np.random.seed(42)  # For consistent data
    base_dso = 45
    trend = np.linspace(0, -5, len(dates))  # Slight improvement over time
    noise = np.random.normal(0, 3, len(dates))
    dso_values = (base_dso + trend + noise).clip(25, 65)
    
    dso_data = {
        'Date': dates,
        'DSO': dso_values
    }
    
    trading_partners_data = {
        'Trading Partner': [
            'Global Fashion Co', 'Style Partners Ltd', 'Fashion Forward Inc', 'Trend Setters Corp', 'Urban Apparel Group',
            'SportShoe Dynamics', 'Comfort Walk Ltd', 'Athletic Gear Co', 'Fashion Footwear Inc', 'Premium Steps Ltd',
            'Vision Optics Co', 'Clear Sight Partners', 'Lens Craft Solutions', 'Optical Innovations', 'Eye Care Retail'
        ],
        'Outstanding': [85000, 45000, 65000, 32000, 78000, 95000, 52000, 48000, 67000, 71000, 38000, 29000, 43000, 35000, 41000],
        'Days_Overdue': [45, 23, 67, 12, 34, 55, 28, 41, 15, 38, 31, 19, 52, 26, 44],
        'Status': ['Overdue', 'Due Soon', 'Overdue', 'Current', 'Due Soon', 'Overdue', 'Due Soon', 'Overdue', 'Current', 'Due Soon', 'Due Soon', 'Current', 'Overdue', 'Due Soon', 'Overdue'],
        'Business_Unit': ['Apparel', 'Apparel', 'Apparel', 'Apparel', 'Apparel', 
                         'Footwear', 'Footwear', 'Footwear', 'Footwear', 'Footwear',
                         'Eyewear', 'Eyewear', 'Eyewear', 'Eyewear', 'Eyewear'],
        'Num_Overdue_Invoices': [3, 0, 5, 0, 2, 4, 1, 2, 0, 3, 2, 0, 6, 1, 4]  # <-- Add this line
    }
    
    return pd.DataFrame(dso_data), pd.DataFrame(trading_partners_data)

def get_trading_partners_by_bu(trading_partners_df, selected_bu):
    """Filter trading partners based on selected business unit"""
    if selected_bu == "All":
        return trading_partners_df['Trading Partner'].tolist()
    else:
        filtered_partners = trading_partners_df[trading_partners_df['Business_Unit'] == selected_bu]
        return filtered_partners['Trading Partner'].tolist()

def get_date_range_fixed():
    """Calculate fixed date ranges based on business requirements"""
    current_date = datetime.now()
    
    # Month Till Date: From start of current month to today
    month_start = datetime(current_date.year, current_date.month, 1).date()
    month_end = current_date.date()
    
    # Quarter Till Date: From June 1st to today (Q2 starts in June for fiscal year)
    quarter_start = datetime(current_date.year, 6, 1).date()
    quarter_end = current_date.date()
    
    # Year Till Date: From April 1st to today (fiscal year starts in April)
    if current_date.month >= 4:
        ytd_start = datetime(current_date.year, 4, 1).date()
    else:
        ytd_start = datetime(current_date.year - 1, 4, 1).date()
    ytd_end = current_date.date()
    
    return {
        'Month Till Date': (month_start, month_end),
        'Quarter Till Date': (quarter_start, quarter_end),
        'Year Till Date': (ytd_start, ytd_end)
    }

def calculate_dso_metrics(start_date, end_date, trading_partners_df, dso_df, selected_partner_filter, selected_bu):
    """Calculate DSO-specific metrics based on ALL selected filters"""
    
    # Filter trading partners based on both BU and selected partners
    if selected_bu == "All":
        bu_filtered_partners = trading_partners_df
    else:
        bu_filtered_partners = trading_partners_df[trading_partners_df['Business_Unit'] == selected_bu]
    
    # Then filter by selected partners
    filtered_trading_partners = bu_filtered_partners[
        bu_filtered_partners['Trading Partner'].isin(selected_partner_filter)
    ]
    
    # Filter DSO data for the selected period
    filtered_dso_df = dso_df[(dso_df['Date'].dt.date >= start_date) & (dso_df['Date'].dt.date <= end_date)]
    
    # Calculate days in period
    days_in_period = (end_date - start_date).days + 1
    
    # DSO Calculation - varies by Business Unit and period
    if len(filtered_dso_df) > 0:
        # Base DSO from time series data
        base_dso = filtered_dso_df['DSO'].mean()
        
        # Adjust DSO based on Business Unit characteristics
        bu_multipliers = {
            'Apparel': 1.0,      # Standard DSO
            'Footwear': 0.85,    # Faster collection (athletic/seasonal)
            'Eyewear': 1.15,     # Slower collection (medical/insurance)
            'All': 1.0           # Average across all BUs
        }
        
        bu_multiplier = bu_multipliers.get(selected_bu, 1.0)
        
        # Adjust based on number of partners (more partners = better diversification = lower DSO)
        partner_count = len(filtered_trading_partners)
        if partner_count > 0:
            partner_adjustment = max(0.9, 1 - (partner_count - 1) * 0.02)  # Small improvement with more partners
        else:
            partner_adjustment = 1.2  # Penalty for no partners
        
        current_dso = base_dso * bu_multiplier * partner_adjustment
        
        # Calculate trend
        if len(filtered_dso_df) > 1:
            dso_trend = (filtered_dso_df['DSO'].iloc[-1] - filtered_dso_df['DSO'].iloc[0]) * bu_multiplier
        else:
            dso_trend = 0
    else:
        # Fallback values when no data
        bu_defaults = {
            'Apparel': 45.0,
            'Footwear': 38.0,
            'Eyewear': 52.0,
            'All': 45.0
        }
        current_dso = bu_defaults.get(selected_bu, 45.0)
        dso_trend = -2.3
    
    # Accounts Receivable - Based on selected trading partners and BU
    if len(filtered_trading_partners) > 0:
        base_ar = filtered_trading_partners['Outstanding'].sum()
        
        # Scale by period length
        period_multiplier = max(0.5, min(days_in_period / 30, 3))
        accounts_receivable = int(base_ar * period_multiplier)
        ar_delta = int(accounts_receivable * 0.03)
    else:
        accounts_receivable = 0
        ar_delta = 0
    
    # Credit Sales - Based on AR, DSO, and period
    if current_dso > 0 and accounts_receivable > 0:
        # DSO = AR / (Credit Sales / Days), so Credit Sales = (AR * Days) / DSO
        credit_sales = int((accounts_receivable * days_in_period) / current_dso)
        credit_sales_delta = int(credit_sales * 0.04)
    else:
        credit_sales = 0
        credit_sales_delta = 0
    
    return {
        'dso': round(current_dso, 1),
        'dso_delta': round(dso_trend, 1),
        'accounts_receivable': accounts_receivable,
        'ar_delta': ar_delta,
        'credit_sales': credit_sales,
        'credit_sales_delta': credit_sales_delta,
        'partner_count': len(filtered_trading_partners),
        'bu_name': selected_bu,
        'period_days': days_in_period
    }

# Main app
def main():
    st.title("🏢 DSO Dashboard - Days Sales Outstanding")
    st.markdown("Monitor and manage your accounts receivable performance")
    
    # Generate sample data
    dso_df, trading_partners_df = generate_sample_data()
    
    # Get fixed date ranges
    date_ranges = get_date_range_fixed()
    
    # Sidebar filters
    st.sidebar.header("📅 Time Period Filters")
    
    # Filter type selection - fixed periods only
    filter_type = st.sidebar.selectbox(
        "Select Filter Type:",
        ["Month Till Date", "Quarter Till Date", "Year Till Date"]
    )
    
    # Get the corresponding date range
    start_date, end_date = date_ranges[filter_type]
    
    # Display selected date range with specific period descriptions
    days_diff = (end_date - start_date).days + 1
    
    # Period descriptions
    period_descriptions = {
        'Month Till Date': f"Current month ({start_date.strftime('%B %Y')})",
        'Quarter Till Date': f"Q2 FY{start_date.year} (Jun-Aug)",
        'Year Till Date': f"FY{start_date.year}-{start_date.year+1} (Apr-Mar)"
    }
    
    st.sidebar.markdown(f"""
    <div class="date-info">
    📅 <strong>{period_descriptions[filter_type]}:</strong><br>
    <strong>From:</strong> {start_date.strftime('%B %d, %Y')}<br>
    <strong>To:</strong> {end_date.strftime('%B %d, %Y')}<br>
    <strong>Duration:</strong> {days_diff} days
    </div>
    """, unsafe_allow_html=True)
    
    # Business Unit filter
    st.sidebar.header("🏭 Business Unit Filter")
    
    # Get unique business units
    business_units = ["All"] + sorted(trading_partners_df['Business_Unit'].unique().tolist())
    
    selected_bu = st.sidebar.selectbox(
        "Select Business Unit:",
        options=business_units,
        index=0  # Default to "All"
    )
    
    # Get trading partners for selected business unit
    available_partners = get_trading_partners_by_bu(trading_partners_df, selected_bu)
    
    # Display BU info
    if selected_bu == "All":
        bu_info = f"All Business Units ({len(trading_partners_df)} partners)"
    else:
        bu_partner_count = len(trading_partners_df[trading_partners_df['Business_Unit'] == selected_bu])
        bu_info = f"{selected_bu} BU ({bu_partner_count} partners)"
    
    st.sidebar.info(f"📊 {bu_info}")
    
    # Trading Partner filter
    st.sidebar.header("🤝 Trading Partner Filters")
    
    # Add "All" option to trading partners (filtered by BU)
    all_partners_for_bu = ["All"] + available_partners
    
    selected_partners = st.sidebar.multiselect(
        "Select Trading Partners:",
        options=all_partners_for_bu,
        default=["All"],
        help=f"Trading partners for {selected_bu if selected_bu != 'All' else 'all business units'}"
    )
    
    # Handle "All" selection logic
    if "All" in selected_partners:
        partner_filter = available_partners
    else:
        partner_filter = [p for p in selected_partners if p != "All"]
    
    # Calculate DSO metrics based on ALL selected filters
    metrics = calculate_dso_metrics(start_date, end_date, trading_partners_df, dso_df, partner_filter, selected_bu)
    
    # Key DSO Metrics Row with dynamic values
    st.subheader("📈 DSO Key Metrics")
    if selected_bu == "All":
        bu_display = "All Business Units"
    else:
        bu_display = f"{selected_bu} Business Unit"
    
    if len(partner_filter) == len(available_partners):
        st.markdown(f"**DSO = (Accounts Receivable ÷ Credit Sales) × Number of Days** - Showing **{bu_display} - All Partners**")
    else:
        st.markdown(f"**DSO = (Accounts Receivable ÷ Credit Sales) × Number of Days** - Showing **{bu_display} - {len(partner_filter)} Selected Partners**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Days Sales Outstanding", use_container_width=True):
            st.balloons()
            if metrics['accounts_receivable'] > 0 and metrics['credit_sales'] > 0:
                st.info(f"DSO Formula: ({metrics['accounts_receivable']:,} ÷ {metrics['credit_sales']:,}) × {days_diff} days = {metrics['dso']} days")
            else:
                st.warning("No receivables data for selected filters")
        st.metric(
            label="DSO", 
            value=f"{metrics['dso']} days", 
            delta=f"{metrics['dso_delta']:+.1f} days",
            help=f"DSO for {metrics['partner_count']} partners in {selected_bu} over {metrics['period_days']} days"
        )
    
    with col2:
        if st.button("💰 Accounts Receivable", use_container_width=True):
            st.success(f"AR for {metrics['partner_count']} selected trading partners in {selected_bu}")
            st.info(f"Total AR: ${metrics['accounts_receivable']:,}")
        st.metric(
            label="Accounts Receivable (AR)", 
            value=f"${metrics['accounts_receivable']:,}", 
            delta=f"${metrics['ar_delta']:+,}",
            help=f"Outstanding invoices for selected filters"
        )
    
    with col3:
        if st.button("💳 Credit Sales", use_container_width=True):
            st.info(f"Credit sales for {metrics['partner_count']} selected trading partners")
            st.success(f"Period Credit Sales: ${metrics['credit_sales']:,}")
        st.metric(
            label="Credit Sales", 
            value=f"${metrics['credit_sales']:,}", 
            delta=f"${metrics['credit_sales_delta']:+,}",
            help=f"Credit sales based on DSO calculation"
        )
    
    # Enhanced DSO Calculation Explanation
    with st.expander("🔍 DSO Calculation Details"):
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"""
            **Current Calculation:**
            - **Period:** {period_descriptions[filter_type]}
            - **Business Unit:** {selected_bu}
            - **Partners:** {metrics['partner_count']} of {len(available_partners)} available
            - **Days:** {metrics['period_days']}
            - **AR:** ${metrics['accounts_receivable']:,}
            - **Credit Sales:** ${metrics['credit_sales']:,}
            - **DSO Formula:** ({metrics['accounts_receivable']:,} ÷ {metrics['credit_sales']:,}) × {metrics['period_days']} = **{metrics['dso']} days**
            """)
        with col_b:
            if metrics['accounts_receivable'] > 0:
                turnover_ratio = metrics['credit_sales'] / metrics['accounts_receivable'] if metrics['accounts_receivable'] > 0 else 0
                collection_efficiency = 100 / metrics['dso'] if metrics['dso'] > 0 else 0
                st.markdown(f"""
                **Performance Insights:**
                - **Collection Time:** {metrics['dso']} days average
                - **Turnover Ratio:** {turnover_ratio:.2f}x per period
                - **Daily Collection:** {collection_efficiency:.1f}% of sales
                - **BU Performance:** {selected_bu}
                - **Period Impact:** {metrics['period_days']} days analyzed
                - **Filter Effect:** {metrics['partner_count']} partners included
                """)
            else:
                st.markdown("""
                **No data available:**
                - No receivables for current filter selection
                - Try selecting different business unit or partners
                - Check if partners have outstanding amounts
                """)
    
    # Enhanced Charts Section with filter-aware data
    st.subheader("📊 Analytics")
    
    # Filter data based on date range and create BU-specific trends
    filtered_dso_df = dso_df[(dso_df['Date'].dt.date >= start_date) & (dso_df['Date'].dt.date <= end_date)].copy()
    
    # Adjust DSO trend data based on business unit
    if len(filtered_dso_df) > 0 and selected_bu != "All":
        bu_adjustments = {
            'Apparel': 1.0,
            'Footwear': 0.85,
            'Eyewear': 1.15
        }
        adjustment = bu_adjustments.get(selected_bu, 1.0)
        filtered_dso_df['DSO'] = filtered_dso_df['DSO'] * adjustment
    
    st.info(f"📈 Showing data for **{len(filtered_dso_df)} days** - {period_descriptions[filter_type]} - **{bu_display}** - **{len(partner_filter)} Partners**")
    
    chart_col1, chart_col2 = st.columns([2, 1])
    
    with chart_col1:
        st.markdown(f"**DSO Trend Over Time - {selected_bu}**")
        
        # Always show chart - either filtered data or sample data
        if len(filtered_dso_df) > 0:
            chart_data = filtered_dso_df
            chart_title = f"DSO Trend - {period_descriptions[filter_type]} - {selected_bu} ({len(partner_filter)} partners)"
        else:
            # Generate sample data for the selected period
            sample_dates = pd.date_range(start=start_date, end=end_date, freq='D')
            np.random.seed(42)
            base_dso = {'Apparel': 45, 'Footwear': 38, 'Eyewear': 52, 'All': 45}[selected_bu]
            sample_dso = np.random.normal(base_dso, 5, len(sample_dates)).clip(25, 65)
            chart_data = pd.DataFrame({'Date': sample_dates, 'DSO': sample_dso})
            chart_title = f"Sample DSO Trend - {period_descriptions[filter_type]} - {selected_bu}"
            st.warning("⚠️ Using sample data for demonstration")
        
        fig_line = px.line(
            chart_data, 
            x='Date', 
            y='DSO',
            title=chart_title,
            line_shape='linear',
            markers=True
        )
        
        # Add target line
        target_dso = 30
        fig_line.add_hline(y=target_dso, line_dash="dash", line_color="red", 
                          annotation_text="Target DSO (30 days)")
        
        # Add current DSO line
        current_dso = metrics['dso']
        fig_line.add_hline(y=current_dso, line_dash="dot", line_color="blue", 
                          annotation_text=f"Current DSO ({current_dso} days)")
        
        fig_line.update_layout(
            height=400,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font_color='black',
            title_font_color='black',
            xaxis=dict(
                gridcolor='lightgray',
                tickfont=dict(color='black'),
                title='Date'
            ),
            yaxis=dict(
                gridcolor='lightgray',
                tickfont=dict(color='black'),
                title='DSO (Days)'
            ),
            showlegend=True
        )
        fig_line.update_traces(line_color='#667eea', marker_color='#667eea')
        
        st.plotly_chart(fig_line, use_container_width=True, key=f"dso_trend_{selected_bu}_{filter_type}")
    
    with chart_col2:
        st.markdown(f"**AR Aging Analysis - {selected_bu}**")
        # Dynamic aging data based on actual selected partners
        if len(partner_filter) > 0:
            if selected_bu == "All":
                selected_partners_df = trading_partners_df[
                    trading_partners_df['Trading Partner'].isin(partner_filter)
                ]
            else:
                selected_partners_df = trading_partners_df[
                    (trading_partners_df['Trading Partner'].isin(partner_filter)) &
                    (trading_partners_df['Business_Unit'] == selected_bu)
                ]
            total_ar = selected_partners_df['Outstanding'].sum()
            
            if total_ar > 0:
                # Realistic aging distribution
                aging_amounts = [
                    int(total_ar * 0.47),  # 0-30 days
                    int(total_ar * 0.26),  # 31-60 days
                    int(total_ar * 0.16),  # 61-90 days
                    int(total_ar * 0.11)   # 90+ days
                ]
            else:
                aging_amounts = [0, 0, 0, 0]
        else:
            aging_amounts = [0, 0, 0, 0]
        
        aging_data = pd.DataFrame({
            'Age Group': ['0-30 days', '31-60 days', '61-90 days', '90+ days'],
            'Amount': aging_amounts
        })
        
        # Only show pie chart if there's data
        if sum(aging_amounts) > 0:
            fig_pie = px.pie(
                aging_data,
                values='Amount', 
                names='Age Group',
                title=f"Receivables Aging - {selected_bu} ({len(partner_filter)} partners)",
                color_discrete_sequence=['#4CAF50', '#FFC107', '#FF9800', '#F44336']
            )
            fig_pie.update_layout(
                height=400,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font_color='black',
                title_font_color='black',
                legend=dict(font=dict(color='black'))
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("No receivables data for selected filters")
            # Show placeholder chart
            placeholder_data = pd.DataFrame({
                'Age Group': ['0-30 days', '31-60 days', '61-90 days', '90+ days'],
                'Amount': [100, 60, 30, 10]  # Sample data
            })
            fig_placeholder = px.pie(
                placeholder_data,
                values='Amount', 
                names='Age Group',
                title=f"Sample AR Aging - {selected_bu}",
                color_discrete_sequence=['#4CAF50', '#FFC107', '#FF9800', '#F44336']
            )
            fig_placeholder.update_layout(
                height=400,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font_color='black',
                title_font_color='black',
                legend=dict(font=dict(color='black'))
            )
            st.plotly_chart(fig_placeholder, use_container_width=True)

    # --- Invoices Paid On Time wrt Payment Terms ---
    with st.container():
        st.markdown("""
        <div style="margin-top: 2rem; margin-bottom: 0.5rem;">
            <h4 style="color:#1565c0; margin-bottom:0;">📊 Invoices Paid On Time vs Payment Terms</h4>
            <span style="font-size:15px; color:#333;">
                Track how payment terms affect timely invoice payments.
            </span>
        </div>
        """, unsafe_allow_html=True)

        payment_terms = ['Net 15', 'Net 30', 'Net 45', 'Net 60']
        invoices_paid_on_time = [12, 29, 23, 12]
        total_invoices = [20, 40, 30, 15]
        percent_on_time = [round(paid/total*100, 1) for paid, total in zip(invoices_paid_on_time, total_invoices)]
        payment_df = pd.DataFrame({
            'Payment Term': payment_terms,
            'Invoices Paid On Time': invoices_paid_on_time,
            'Total Invoices': total_invoices,
            'Percent On Time': percent_on_time
        })

        fig_bar = px.bar(
            payment_df,
            x='Payment Term',
            y='Percent On Time',
            text='Percent On Time',
            color='Payment Term',
            color_discrete_sequence=px.colors.qualitative.Set2,
            title=""
        )
        fig_bar.update_traces(
            texttemplate='%{text}%',
            textposition='outside',
            marker_line_width=1.5,
            marker_line_color='#333'
        )
        fig_bar.update_layout(
            yaxis_title="Paid On Time (%)",
            xaxis_title="Payment Term",
            height=350,
            plot_bgcolor='#f8f9fa',
            paper_bgcolor='#f8f9fa',
            font_color='#333333',
            title_font_color='#1565c0',
            margin=dict(t=30, b=30, l=10, r=10),
            showlegend=False
        )
        fig_bar.update_yaxes(showgrid=True, gridcolor='#e0e0e0', zerolinecolor='#e0e0e0')
        fig_bar.update_xaxes(tickfont=dict(size=14, color='#1565c0'))

        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Enhanced Additional Analytics Section
    st.subheader("📈 Additional Analytics")
    
    analysis_col1, analysis_col2 = st.columns(2)
    
    with analysis_col1:
        st.markdown("**Collection Rate**")
        current_dso = metrics['dso']
        collection_rate = 365 / current_dso if current_dso > 0 else 0
        st.markdown(f"- **Collection Rate:** {collection_rate:.1f} times per year")
    
    with analysis_col2:
        st.markdown("**AR Turnover**")
        ar_turnover = metrics['credit_sales'] / metrics['accounts_receivable'] if metrics['accounts_receivable'] > 0 else 0
        st.markdown(f"- **AR Turnover:** {ar_turnover:.2f}x")
    
    # Interactive Data Tables
    st.subheader("📋 Trading Partner Details")
    
    # Filter trading partners based on sidebar selection (remove status filter)
    filtered_partners = trading_partners_df[
        trading_partners_df['Trading Partner'].isin(partner_filter)
    ]
    
    if len(filtered_partners) == 0:
        st.warning("No trading partners match the selected filters.")
    else:
        st.info(f"Showing {len(filtered_partners)} trading partners from {selected_bu if selected_bu != 'All' else 'all business units'}")
    
    # Add action buttons for each trading partner
    for index, row in filtered_partners.iterrows():
        with st.expander(f"{row['Trading Partner']} ({row['Business_Unit']}) - ${row['Outstanding']:,} ({row['Status']})"):
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                if st.button(f"📞 Contact {row['Trading Partner']}", key=f"contact_{index}"):
                    st.success(f"Initiating contact with {row['Trading Partner']}")
            
            with col_b:
                if st.button(f"📅 Schedule Follow-up", key=f"schedule_{index}"):
                    st.info(f"Follow-up scheduled for {row['Trading Partner']}")
            
            with col_c:
                if st.button(f"💸 Cleo Payments", key=f"payment_{index}"):
                    st.warning(f"Improve Cash Flow with Cleo payments {row['Trading Partner']}")
            
            # Show trading partner details
            st.markdown(f"""
**Business Unit:** {row['Business_Unit']}  
**Status:** {row['Status']}
""")

            # --- DSO, AR, Credit Sales, Outstanding, Overdue Invoices for this partner ---
            partner_ar = row['Outstanding']
            base_dso = metrics['dso']
            overdue_factor = 1 + (row['Days_Overdue'] / 100) if row['Days_Overdue'] > 0 else 1
            partner_dso = round(base_dso * overdue_factor, 1)
            partner_credit_sales = int((partner_ar * metrics['period_days']) / partner_dso) if partner_dso > 0 else 0
            num_overdue = row['Num_Overdue_Invoices']
            amount_overdue = int(row['Outstanding'] * min(num_overdue, 1) if num_overdue > 0 else 0)  # For demo, 1 invoice = all outstanding

            # Display all metrics in one table
            col_dso, col_ar, col_sales, col_out, col_num, col_amt = st.columns(6)
            with col_dso:
                st.metric("DSO", f"{partner_dso} days")
            with col_ar:
                st.metric("Account Receivable", f"${partner_ar:,}")
            with col_sales:
                st.metric("Credit Sales", f"${partner_credit_sales:,}")
            with col_out:
                st.metric("Outstanding", f"${partner_ar:,}")
            with col_num:
                st.metric("No. of Invoices Overdue", f"{num_overdue}")
            with col_amt:
                st.metric("Overdue Invoices Amt", f"${amount_overdue:,}")
    
    # Action Bar
    st.subheader("🚀 Quick Actions")
    action_col1, action_col2, action_col3, action_col4 = st.columns(4)
    
    with action_col1:
        if st.button("📤 Send Bulk Reminders", use_container_width=True):
            with st.spinner("Sending reminders..."):
                import time
                time.sleep(2)
            st.success(f"Reminders sent to {len(filtered_partners)} trading partners in {selected_bu}!")
    
    with action_col2:
        if st.button("📊 Export Report", use_container_width=True):
            filename = f"dso_report_{selected_bu.lower().replace(' ', '_')}_{filter_type.lower().replace(' ', '_')}.csv"
            st.download_button(
                label="Download CSV",
                data=filtered_partners.to_csv(index=False),
                file_name=filename,
                mime="text/csv"
            )
    
    with action_col3:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    with action_col4:
        if st.button("⚙️ Collection Strategy", use_container_width=True):
            st.info(f"Opening collection strategy for {selected_bu}...")

if __name__ == "__main__":
    main()