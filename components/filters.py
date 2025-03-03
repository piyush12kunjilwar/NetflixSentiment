import streamlit as st

def create_filters(df):
    """Create sidebar filters for the dashboard."""
    
    st.sidebar.header('Filters')
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(df['timestamp'].min().date(), df['timestamp'].max().date()),
        min_value=df['timestamp'].min().date(),
        max_value=df['timestamp'].max().date()
    )
    
    # Show filter
    selected_shows = st.sidebar.multiselect(
        'Select Shows',
        options=df['show'].unique(),
        default=df['show'].unique()
    )
    
    # Genre filter
    selected_genres = st.sidebar.multiselect(
        'Select Genres',
        options=df['genre'].unique(),
        default=df['genre'].unique()
    )
    
    # Region filter
    selected_regions = st.sidebar.multiselect(
        'Select Regions',
        options=df['user_region'].unique(),
        default=df['user_region'].unique()
    )
    
    # Age range filter
    age_range = st.sidebar.slider(
        'Age Range',
        min_value=int(df['user_age'].min()),
        max_value=int(df['user_age'].max()),
        value=(int(df['user_age'].min()), int(df['user_age'].max()))
    )
    
    # Apply filters
    mask = (
        (df['timestamp'].dt.date >= date_range[0]) &
        (df['timestamp'].dt.date <= date_range[1]) &
        (df['show'].isin(selected_shows)) &
        (df['genre'].isin(selected_genres)) &
        (df['user_region'].isin(selected_regions)) &
        (df['user_age'].between(age_range[0], age_range[1]))
    )
    
    filtered_df = df[mask]
    
    return filtered_df
