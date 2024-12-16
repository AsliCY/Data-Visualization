import gradio as gr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load the data
df = pd.read_csv('data_season.csv')

def create_yield_analysis(crop_name):
    if crop_name == "All Crops":
        crop_data = df
    else:
        crop_data = df[df['Crops'] == crop_name]
    
    fig = px.scatter(crop_data, 
                    x='Temperature', 
                    y='yeilds',
                    color='Season',
                    size='Rainfall',
                    hover_data=['Humidity', 'Soil type'],
                    title=f'Yield Analysis for {crop_name}',
                    labels={'Temperature': 'Temperature (°C)',
                           'yeilds': 'Yield',
                           'Rainfall': 'Rainfall (mm)'})
    return fig

def show_seasonal_pattern(season_name):
    season_data = df[df['Season'] == season_name]
    avg_yield = season_data.groupby('Crops')['yeilds'].mean().sort_values(ascending=False)
    
    plt.figure(figsize=(12, 6))
    avg_yield.plot(kind='bar')
    plt.title(f'Average Yield by Crop in {season_name} Season')
    plt.xlabel('Crops')
    plt.ylabel('Average Yield')
    plt.xticks(rotation=45)
    return plt

def get_crop_insights(crop_name):
    if crop_name == "All Crops":
        return "Please select a specific crop for detailed insights."
    
    crop_data = df[df['Crops'] == crop_name]
    
    insights = f"""
    Detailed Analysis for {crop_name}:
    
    1. Production Metrics:
       - Average Yield: {crop_data['yeilds'].mean():.2f} units per area
       - Maximum Yield: {crop_data['yeilds'].max():.2f}
       - Minimum Yield: {crop_data['yeilds'].min():.2f}
    
    2. Growing Conditions:
       - Average Temperature: {crop_data['Temperature'].mean():.2f}°C
       - Average Rainfall: {crop_data['Rainfall'].mean():.2f} mm
       - Average Humidity: {crop_data['Humidity'].mean():.2f}%
    
    3. Economic Metrics:
       - Average Price: ₹{crop_data['price'].mean():.2f}
       - Price Range: ₹{crop_data['price'].min():.2f} - ₹{crop_data['price'].max():.2f}
    
    4. Seasonal Distribution:
    {crop_data['Season'].value_counts().to_string()}
    
    5. Preferred Soil Types:
    {crop_data['Soil type'].value_counts().to_string()}
    """
    return insights

def show_price_trends():
    plt.figure(figsize=(12, 6))
    avg_prices = df.groupby('Crops')['price'].mean().sort_values(ascending=False)
    avg_prices.plot(kind='bar')
    plt.title('Average Price by Crop')
    plt.xlabel('Crops')
    plt.ylabel('Average Price (₹)')
    plt.xticks(rotation=45)
    return plt

def get_key_insights():
    # Calculate key metrics
    top_yield_crops = df.groupby('Crops')['yeilds'].mean().nlargest(3)
    top_price_crops = df.groupby('Crops')['price'].mean().nlargest(3)
    most_common_crops = df.groupby('Crops').size().nlargest(3)
    best_season = df.groupby('Season')['yeilds'].mean().idxmax()
    
    insights = f"""
    ## 🎯 Key Findings from the Analysis
    
    ### 🏆 Top Performers
    
    1. **Highest Yielding Crops:**
       {', '.join(f"{crop} ({yield_:.0f} units)" for crop, yield_ in top_yield_crops.items())}
    
    2. **Most Valuable Crops:**
       {', '.join(f"{crop} (₹{price:.0f})" for crop, price in top_price_crops.items())}
    
    3. **Most Commonly Grown Crops:**
       {', '.join(f"{crop} ({count} records)" for crop, count in most_common_crops.items())}
    
    ### 🌱 Environmental Insights
    
    - **Best Performing Season:** {best_season}
    - **Temperature Range:** {df['Temperature'].min():.1f}°C to {df['Temperature'].max():.1f}°C
    - **Average Rainfall:** {df['Rainfall'].mean():.1f} mm
    - **Humidity Levels:** {df['Humidity'].min():.1f}% to {df['Humidity'].max():.1f}%
    
    ### 💡 Notable Trends
    
    - Higher yields generally correlate with moderate temperatures
    - Rainfall has significant impact on crop performance
    - Price variations observed across seasons
    """
    return insights

# Create Gradio interface
with gr.Blocks(title="Karnataka Agricultural Analysis") as demo:
    with gr.Tab("Overview"):
        gr.Markdown("""
        # 🌾 Karnataka Agricultural Analysis Dashboard
        
        ## About This Dashboard
        This interactive dashboard provides comprehensive insights into agricultural patterns 
        in Karnataka, analyzing crop yields, weather impacts, and economic factors.
        
        ## 📊 Understanding the Data
        
        ### Growing Seasons:
        - **Kharif (Monsoon)**: June-October
        - **Rabi (Winter)**: November-April
        - **Zaid (Summer)**: March-June
        
        ### Key Metrics Explained:
        - **Yield**: Crop production per unit area
        - **Temperature**: Measured in Celsius (°C)
        - **Rainfall**: Measured in millimeters (mm)
        - **Humidity**: Percentage of moisture in air
        - **Price**: Measured in Indian Rupees (₹)
        """)
        
        gr.Markdown(get_key_insights())
    
    with gr.Tab("Crop Analysis"):
        gr.Markdown("""
        ### 📈 Crop Analysis Guide
        
        This section helps you understand:
        - How different crops perform under various conditions
        - Impact of temperature and rainfall on yields
        - Crop-specific growing conditions
        
        **How to use:**
        1. Select a crop from the dropdown
        2. Analyze the scatter plot patterns
        3. Review detailed insights in the text box
        """)
        
        with gr.Row():
            crop_dropdown = gr.Dropdown(
                choices=["All Crops"] + sorted(df['Crops'].unique().tolist()),
                value="All Crops",
                label="Select Crop for Analysis"
            )
        with gr.Row():
            with gr.Column():
                yield_plot = gr.Plot(label="Yield Analysis")
            with gr.Column():
                insights_text = gr.Textbox(label="Crop Insights", lines=10)
        crop_dropdown.change(
            fn=create_yield_analysis,
            inputs=crop_dropdown,
            outputs=yield_plot
        )
        crop_dropdown.change(
            fn=get_crop_insights,
            inputs=crop_dropdown,
            outputs=insights_text
        )
    
    with gr.Tab("Seasonal Patterns"):
        gr.Markdown("""
        ### 🌺 Seasonal Analysis Guide
        
        Understand how crops perform across different seasons:
        - Compare yields across seasons
        - Identify optimal growing periods
        - Analyze seasonal trends
        
        **Using the Analysis:**
        1. Select a season from the dropdown
        2. Compare crop performances
        3. Note the yield variations
        """)
        
        season_dropdown = gr.Dropdown(
            choices=sorted(df['Season'].unique().tolist()),
            label="Select Season"
        )
        season_plot = gr.Plot(label="Seasonal Analysis")
        season_dropdown.change(
            fn=show_seasonal_pattern,
            inputs=season_dropdown,
            outputs=season_plot
        )
    
    with gr.Tab("Price Analysis"):
        gr.Markdown("""
        ### 💰 Price Analysis Guide
        
        Explore crop prices and economic trends:
        - Compare prices across different crops
        - Analyze price variations
        - Identify high-value crops
        
        **Understanding the Data:**
        - Mean: Average price for the crop
        - Min/Max: Price range
        - Std: Price variability
        """)
        
        price_plot = gr.Plot(label="Price Trends")
        price_button = gr.Button("Show Price Trends")
        price_button.click(
            fn=show_price_trends,
            outputs=price_plot
        )
        
        with gr.Row():
            gr.DataFrame(
                df.groupby('Crops')['price'].agg(['mean', 'min', 'max', 'std'])
                .round(2)
                .sort_values('mean', ascending=False),
                label="Detailed Price Statistics by Crop"
            )

# Launch the app
if __name__ == "__main__":
    demo.launch(share=True)