import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:priya@localhost:3306/food_db')
import pymysql

connection = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="priya")

cursor = connection.cursor()

import numpy as np
df = pd.read_sql("SELECT * FROM delivery_table", engine)

st.title(" 🛵 Online Food Delivery Analysis: Data Driven Business Insights 🛵")
st.subheader("Explore Online food delivery trends with SQL Queries 📈 ")
st.divider()

tab1, tab2, tab3 = st.tabs(["Analyst task", "KPI" , "Data visualization"])

with tab1:
        st.header("Analyst Task")
        sql_queries = {
        "1. Identify top spending customers":"""SELECT customer_id, sum(final_amount) AS total_spent
                FROM food_db.delivery_table
                GROUP BY customer_id
                ORDER BY total_spent Desc
                LIMIT 10;"""  ,
                 
        "2. Analyze age group vs order value":"""SELECT customer_age_group, AVG(final_amount) AS avg_order_value 
                FROM food_db.delivery_table 
                GROUP BY customer_age_group
                ORDER BY avg_order_value DESC;""",

        "3. Weekend vs weekday order patterns": """SELECT order_day, COUNT(order_id) AS total_orders,
                SUM(final_amount) AS revenue
                FROM food_db.delivery_table
                GROUP BY order_day 
                ORDER BY revenue DESC;""",

        "4. Monthly revenue trends": """SELECT YEAR(order_date) AS year, MONTH(order_date) AS month,
                SUM(final_amount) AS revenue, avg(final_amount) AS avg_amount
                FROM food_db.delivery_table
                GROUP BY year, month
                ORDER BY year, month;""",

        "5. Impact of discounts on profit": """SELECT discount_applied, 
                ROUND(AVG(profit_margin_percentage),2) AS avg_profit_margin, 
                ROUND(SUM(final_amount), 2) AS revenue FROM food_db.delivery_table
                GROUP BY discount_applied 
                ORDER BY discount_applied;""",

        "6. High-revenue cities and cuisines":"""SELECT city,cuisine_type,
               SUM(final_amount) AS total_revenue
               FROM food_db.delivery_table
               GROUP BY city, cuisine_type
               ORDER BY total_revenue DESC;""",

        "7. Average delivery time by city" : """SELECT city,AVG(delivery_time_min) AS avg_delivery_time
                FROM food_db.delivery_table
                GROUP BY city
                ORDER BY avg_delivery_time DESC;""",

        "8. Distance vs delivery delay analysis":"""SELECT
                ROUND((distance_km),0) AS distance_km, 
                round(AVG(delivery_time_min),2) AS avg_delivery_time
                FROM food_db.delivery_table
                GROUP BY distance_km
                ORDER BY avg_delivery_time
                DESC;""",

        "9. Delivery rating vs delivery time": """SELECT 
                delivery_rating,
                COUNT(*) AS total_orders,
                AVG(delivery_time_min) AS delivery_time
                FROM food_db.delivery_table
                GROUP BY delivery_rating
                ORDER BY delivery_rating DESC;""",

        "10. Top-rated restaurants": """SELECT
                restaurant_name, AVG(restaurant_rating) AS avg_rating,
                COUNT(order_id) AS total_orders
                FROM food_db.delivery_table
                GROUP BY restaurant_name
                ORDER BY avg_rating DESC, total_orders DESC limit 10;""",
       
        "11. Cancellation rate by restaurant": """ SELECT  restaurant_name, 
                COUNT(*) AS total_orders, 
                SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
                ROUND(SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS cancellation_rate
                FROM food_db.delivery_table
                GROUP BY restaurant_name
                ORDER BY cancellation_rate DESC limit 10;""",

        "12. Cuisine-wise performance": """SELECT cuisine_type,
                COUNT(order_id) AS total_orders,
                ROUND(AVG(final_amount), 2) AS avg_order_value,
                ROUND(SUM(final_amount), 2) AS total_revenue,
                ROUND(AVG(restaurant_rating), 2) AS avg_rating,
                AVG(profit_margin_percentage) AS avg_profit_margin
                FROM food_db.delivery_table
                GROUP BY cuisine_type
                ORDER BY total_revenue DESC;""",
       
        "13. Peak hour demand analysis" : """SELECT
                peak_hour, COUNT(order_id) AS total_orders,
                ROUND(SUM(final_amount), 2) AS total_revenue
                FROM food_db.delivery_table
                GROUP BY peak_hour
                ORDER BY total_orders DESC""",
       
        "14. Payment mode preferences": """SELECT
                payment_mode,
                COUNT(order_id) AS total_orders,
                ROUND(SUM(final_amount), 2) AS total_revenue
                FROM food_db.delivery_table
                GROUP BY payment_mode
                ORDER BY total_orders DESC;""",
       
        "15. Cancellation reason analysis" :"""SELECT
                cancellation_reason,
                COUNT(order_id) AS total_cancellations
                FROM food_db.delivery_table
                WHERE order_status = 'Cancelled'
                GROUP BY cancellation_reason
                ORDER BY total_cancellations DESC;"""        
          } 
        question_option = list(sql_queries.keys())

        selected_question = st.selectbox("🎯Select any task below and get the corresponding SQL queries to analyze data:",
                                         list(sql_queries.keys()), index =None, placeholder="TASK...")
        
        if selected_question:    
              query = sql_queries[selected_question]    
              result = st.code(query)
              data = pd.read_sql(query,engine)
              st.dataframe(data, use_container_width=True)
              cursor.execute(query)
              results = cursor.fetchall()

from streamlit_extras.metric_cards import style_metric_cards

with tab2:
        st.header("KPI ANALYSIS")
        dashboard_query = {

        "1. TOTAL ORDERS" : """SELECT COUNT(order_id) AS total_orders FROM food_db.delivery_table;""",

        "2. TOTAL REVENUE": """SELECT SUM(final_amount) AS total_revenue FROM food_db.delivery_table;""",

        "3. AVERAGE ORDER VALUE" :"""SELECT  ROUND(AVG(final_amount),2) AS avg_order_value FROM food_db.delivery_table;""",

        "4. AVERAGE DELIVERY TIME": """SELECT ROUND(AVG(delivery_time_min),2) AS avg_delivery_time FROM food_db.delivery_table;""",

        "5. CANCELLATION RATE": """SELECT ROUND(SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),2) 
                AS cancellation_rate FROM food_db.delivery_table;""",

        "6. AVERAGE DELIVERY RATING" : """SELECT  ROUND(AVG(delivery_rating), 2) AS avg_delivery_rating
               FROM food_db.delivery_table;""",

        "7. PROFIT MARGIN PERCENTAGE": """SELECT ROUND(AVG(profit_margin_percentage), 2) AS profit_margin_percentage
               FROM food_db.delivery_table;"""        
        }

        q2 = list(dashboard_query.keys())
        
        question = st.selectbox("🔍 Select Analysis", list(dashboard_query.keys()), index= None, placeholder="Choose an analysis...")

        if question:
                queries = dashboard_query[question]            
                dg=pd.read_sql(queries, engine)
                st.subheader("📊 Analytics Summary")      
                if question == "1. TOTAL ORDERS":           
                        st.metric("📦 Total Orders",f"{dg.iloc[0,0]:,}")
                elif question == "2. TOTAL REVENUE":                   
                        st.metric("💰 Total Revenue",f"₹{dg.iloc[0,0]:,.2f}")
                elif question == "3. AVERAGE ORDER VALUE":
                        st.metric("🛒 Avg Order Value", f"₹{dg.iloc[0,0]:,.2f}")
                elif question == "4. AVERAGE DELIVERY TIME":
                        st.metric("🚚 Avg Delivery Time", f"{dg.iloc[0,0]:,.2f}")     
                elif question == "5. CANCELLATION RATE":
                        st.metric("⚠️ Cancellation Rate (%)", f"{dg.iloc[0,0]} %")
                elif question == "6. AVERAGE DELIVERY RATING":
                        st.metric("⭐ Avg Delivery Rating",f"{dg.iloc[0,0]:,.2f}")
                else:
                        st.metric("🪙 Profit Margin (%)",f"{dg.iloc[0,0]:,.2f}%")      
                        
                style_metric_cards(background_color="#DCE2E2",
                                border_left_color="#075040FF",
                                border_color="#070707FF",
                                box_shadow=True)
           

import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_sql("SELECT * FROM delivery_table", engine)


with tab3:
        st.header("EDA-DATA VISUALIZATION")
        eda =(
        "1. Distribution of Order Values",
        "2.Distribution of delivery_time_min",
        "3. City-Wise order analysis",
        "4. Cuisine-Wise Order analysis",
        "5. Weekend vs Weekday demand",
        "6. Distance Vs Delivery delay analysis",
        "7. Cancellation reason analysis",
        "8. Correlation analysis among numeric features"
        )
        
        selected_eda = st.selectbox("📋select analytics for visualizing the data", eda,
                                    index= None, placeholder = "select 👉🏻")
        
        if selected_eda == "1. Distribution of Order Values":
                fig = px.box(df,x ='order_value',title='Order Values-Outlier')
                st.write("Chart is loading...")
                st.plotly_chart(fig, use_container_width=True)

                fig = px.histogram(df, x='order_value', nbins=30, title='📦Distribution Of Order Value')
                fig.update_layout(xaxis_title="Order Value (₹)", yaxis_title="Number of Orders",bargap=0.05)                
                st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("📌 Business Insights")
                st.markdown("""
                        - Most customers place orders worth between **₹900 and ₹2500**.
                        - The average customer prefers **medium-priced orders** rather than very low- or very high-priced orders.
                        - Medium-value orders contribute the **largest share of the platform's revenue**.
                        - A smaller group of customers places **high-value orders (₹3000–₹5000)**.
                        - Although fewer in number, high-value orders contribute **significantly to overall revenue**.
                        - Customer spending patterns appear **stable and consistent** across orders.
                        - There are **no significant outliers** in order values, indicating good data quality.
                        - Attractive offers and promotions may encourage customers to place **higher-value orders**.
                        - Promotions such as **combo meals, free delivery, and discounts** can help increase average order value.
                        - Identifying and retaining **high-spending customers** through loyalty programs can improve revenue and profitability.
                        """)
                
        elif selected_eda == "2.Distribution of delivery_time_min":
                fig = px.box(df,x='delivery_time_min',title='📦 Delivery Time Range & Outliers')
                st.write("Chart is loading...")
                st.plotly_chart(fig, use_container_width=True)
                
                fig = px.histogram(df, x='delivery_time_min', nbins=20, title='Distribution of Delivery Time🚚')
                fig.update_layout(xaxis_title="Delivery Time (Minutes)",yaxis_title="Number of Orders")
                st.plotly_chart(fig, use_container_width=True)

                avg_delivery = df.groupby('city')['delivery_time_min'].mean().sort_values().reset_index()
                fig = px.bar(avg_delivery,x="city",y="delivery_time_min",title="📍 Average Delivery Time by City", text_auto=".1f",
                             color="delivery_time_min")
                fig.update_layout(xaxis_title="City", yaxis_title="Average Delivery Time (Minutes)")
                st.plotly_chart(fig, use_container_width=True) 
                st.subheader("📌 Business Insights")
                st.markdown("""
                        - Most orders are delivered within **50–70 minutes**, indicating consistent delivery performance.
                        - A small percentage of orders take **120–300 minutes**, representing significant delivery delays.
                        - Extended delivery times can negatively impact **customer satisfaction** and overall experience.
                        - Traffic congestion and adverse weather conditions may contribute to longer delivery durations.
                        - Longer delivery distances are likely to increase the time required to fulfill orders.
                        - Delays in restaurant order preparation can affect overall delivery efficiency.
                        - High order volumes during peak hours can slow down deliveries.
                        - Consistently delayed deliveries can result in **lower customer ratings** and reduced customer loyalty.
                        - Optimizing delivery routes, improving restaurant coordination, and increasing delivery partner 
                            availability during peak hours can help reduce delays and encourage repeat orders.
                        """)
        elif selected_eda == "3. City-Wise order analysis":
                city_orders = df['city'].value_counts().reset_index()
                city_orders.columns = ['city', 'orders']
                fig = px.histogram(city_orders,x='city', y='orders',title='City_wise_orders📅')
                fig.update_layout(xaxis_title='City',yaxis_title='Number of Orders')
                st.write("chart is loading")
                st.plotly_chart(fig, use_container_width=True) 
        
                
                city_revenue = df.groupby('city')['final_amount'].sum().reset_index()
                fig = px.histogram(city_revenue, x='city',y='final_amount', title='Revenue by City💰')
                st.plotly_chart(fig, use_container_width=True) 

                fig = px.box(df, x='delivery_time_min', y='city', title = 'Delivery Time Distribution by City⏰')
                st.plotly_chart(fig, use_container_width=True) 
                st.subheader("📌 Business Insights")
                st.markdown("""                            
                            - Hyderabad records approximately 33,000+ orders. Other cities (Bangalore, Delhi, Mumbai, Chennai)
                                have around **16,000–17,000 orders** each.
                            - Hyderabad contributes approximately **₹62 million in revenue**. Other cities generate around **₹30–31 million**
                                each. Revenue follows the same pattern as order volume, indicating strong customer demand in Hyderabad.
                            - Hyderabad is the platform's largest revenue-generating city and should be treated as a strategic priority market.
                            - Bangalore, Chennai, Delhi, and Mumbai show very similar order volumes and revenue figures. 
                                This balanced distribution reduces business risk and creates opportunities for scalable growth.
                            - Cities with more orders generate proportionally more revenue. Increasing order frequency may have a greater 
                                impact on revenue than increasing average order value.
                            - Hyderabad has the highest order volume and, from previous analysis, also showed the highest cancellation counts.
                            - Hyderabad has the highest order volume and, from previous analysis, also showed the highest cancellation counts.
                            - As demand increases, operational challenges such as delivery delays and cancellations become more critical.
                            - Even small operational improvements in Hyderabad can result in substantial revenue gains and customer retention.
                            """)

        elif selected_eda == "4. Cuisine-Wise Order analysis":
                cuisine_orders = df['cuisine_type'].value_counts().reset_index()
                cuisine_orders.columns = ['cuisine_type', 'orders']
                fig = px.histogram(cuisine_orders,x='cuisine_type',  y='orders',title='Cuisine-wise orders📅')
                st.write("Chart is loading...")
                st.plotly_chart(fig, use_container_width=True)

                cuisine_based_revenue = df.groupby('cuisine_type')['final_amount'].sum().reset_index()
                fig = px.histogram(cuisine_based_revenue, x='cuisine_type',y='final_amount', title='Revenue by cuisine💹')
                st.plotly_chart(fig, use_container_width=True)

                fig = px.box(df, x='delivery_time_min', y='cuisine_type', title = 'Delivery Time Distribution by Cuisine⏰')
                st.plotly_chart(fig, use_container_width=True)

                cuisine_demand = df.groupby('cuisine_type')['order_status'].value_counts().unstack().fillna(0)
                fig = px.bar(cuisine_demand, x=cuisine_demand.index, y=cuisine_demand.columns,title='Cuisine Demand by Status 📈', barmode='group')
                st.plotly_chart(fig, use_container_width=True)
                st.subheader("📌 Business Insights")

                st.markdown("""
                        * Indian cuisine has approximately 33,000+ orders. Other cuisines (Arabian, Chinese, Mexican, Italian) each have around 16,000–17,000 orders.
                        * Any disruption in Indian cuisine operations can significantly affect overall business performance.
                        * Indian cuisine generates approximately ₹63 million in revenue. Other cuisines generate around ₹30 million each.
                        * Revenue distribution closely follows order volume, indicating that Indian cuisine contributes the largest share of business revenue.
                        * The platform is not overly dependent on a single international cuisine category, reducing business risk.
                        * Maintaining high service quality for Indian cuisine can directly improve customer satisfaction and revenue.
                        * Indian cuisine has the highest cancellation count (~5,000 orders). Other cuisines have approximately 2,500 cancellations each.
                        * Delivered orders significantly exceed cancelled orders across all cuisine categories.
                        * Improve preparation and delivery efficiency. Reduce cancellations to protect revenue.
                        * Create combo offers and cuisine-specific campaigns.
                        * Allocate more delivery partners during peak demand periods for Indian cuisine.""")
        
        elif selected_eda == "5. Weekend vs Weekday demand":
                fig = px. histogram(df, x='order_day', nbins=30,title='Weekend vs Weekday Orders📅')
                st.write("Chart is loading...")
                st.plotly_chart(fig, use_container_width=True)

                revenue = df.groupby('order_day')['final_amount'].sum().reset_index()
                fig = px.histogram(revenue, x='order_day',y='final_amount', title='Revenue by week💵')
                st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("📌 Business Insights")
                st.markdown("""
                        * Weekdays generate the majority of orders, with around 71,000 orders  compared to 29,000 orders on weekends.
                        * Weekday revenue is significantly higher, generating approximately ₹132 million, while weekends generate around ₹53 million.
                        * Weekdays contribute nearly 2.5 times more revenue than weekends, making them the most important period for the business.
                        * Higher weekday revenue is mainly due to higher order volume, not because customers spend more per order.
                        * Customers show strong dependence on food delivery during weekdays, likely due to work schedules and convenience needs.
                        * Any delivery delays or service disruptions on weekdays could have a major impact on revenue and customer satisfaction.
                        * Weekend demand is considerably lower, indicating potential untapped revenue opportunities.
                        * Weekend promotions, discounts, and family meal offers could help increase order volume and revenue.""")

        elif selected_eda == "6. Distance Vs Delivery delay analysis":
                fig =px.scatter(df, x='distance_km', y='delivery_time_min', title ='🔵Distance vs Delivery Time')
                st.write("Chart is loading...")
                st.plotly_chart(fig, use_container_width=True)

                sample_df = df.sample(5000, random_state=42)
                fig = px.scatter(sample_df, x='distance_km', y='delivery_time_min',opacity=0.5,
                                 title='🔵Distance vs Delivery Time')
                st.plotly_chart(fig, use_container_width=True)
                st.subheader("📌 Business Insights")

                st.markdown("""
                        * Distance has a very weak impact on delivery time, as the trendline is almost flat.
                        * Orders with similar distances show large differences in delivery times. For example, orders around 10–15 km can be delivered in both under 50 minutes and over 250 minutes.
                        * Delivery times vary significantly even for similar distances, suggesting other factors influence delivery duration.
                        * Short-distance orders also experience long delivery times**, highlighting potential operational inefficiencies.
                        * The wide spread of delivery times indicates inconsistent service levels** across orders.
                        * Delivery efficiency cannot be evaluated based on distance alone**, as similar distances show large variations in delivery time.
                        * Improving operational processes may yield greater benefits than reducing delivery distance.
                        * Customers are likely to tolerate longer delivery times for distant orders. However, long delays for nearby orders can negatively affect customer satisfaction and increase cancellations.
                        """)
        elif selected_eda == "7. Cancellation reason analysis":
                cancel_reason = (df['cancellation_reason'].value_counts().reset_index())
                cancel_reason.columns = ['Cancellation Reason', 'Count']
                fig = px.bar(cancel_reason, x='Cancellation Reason', y='Count', title='❌Cancellation Reason Analysis',
         text='Count', color='Cancellation Reason')
                fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
                st.write("Chart is loading...")
                st.plotly_chart(fig, use_container_width=True)
                
                cancelled_df = df[df['order_status'] == 'Cancelled']
                fig = px.histogram(cancelled_df,x='city',color='cancellation_reason',barmode='group', title='Cancellation Reasons by City⚠️')
                fig.update_layout( xaxis_title='City',yaxis_title='Number of Cancelled Orders')
                st.plotly_chart(fig, use_container_width=True)

                cancelled_df = df[df['order_status'] == 'Cancelled']
                fig = px.histogram(cancelled_df,x='cuisine_type',color='cancellation_reason',barmode='group',
                                   title='Cancellation Reasons by Cuisine_type🍽️')
                fig.update_layout( xaxis_title='Cuisine',yaxis_title='Number of Cancelled Orders')
                st.plotly_chart(fig, use_container_width=True)

                revenue_loss = cancelled_df.groupby('cancellation_reason')['order_value'].sum().reset_index()
                fig = px.bar(revenue_loss, x='cancellation_reason', y='order_value', title='Revenue Loss by Cancellation Reason🙅')
                st.plotly_chart(fig, use_container_width=True)

                st.subheader("📌 Business Insights")
                st.markdown("""
                        * Around 85 percentage of orders were completed without cancellation.This indicates strong operational performance 
                            and customer acceptance.
                        * Late delivery accounts for approximately 9,100 cancellations, making it the largest cancellation reason. 
                            Delayed orders lead directly to lost revenue and customer dissatisfaction.
                        * Customer-Initiated Cancellations  and resaurant - related issues are relatively Low. 
                            Only around 3,000 orders were cancelled.
                        * Revenue loss due to late delivery is approximately ₹17.5 million. Approximately ₹5.8 million in 
                            revenue was lost due to customer cancellations and around ₹5.7 million was lost because of restaurant-related issues.
                        * Hyderabad records more than double the late-delivery cancellations compared to other cities. 
                            This  may be due to high order volume, traffic congestion or insufficient delivery partners.
                        * Indian cuisine has the highest cancellation count, likely due to higher demand and preparation complexity.
                        * By reducing delivery delays, improving restaurant efficiency, and strengthening operations in high-demand areas, 
                            the platform can potentially recover a significant portion of the ₹29 million revenue currently lost through 
                            cancellations.""")

        
        elif selected_eda == "8. Correlation analysis among numeric features":
                        numeric_df = df.select_dtypes(include=['int64', 'float64'])
                        fig, ax = plt.subplots(figsize=(12, 8))
                        sns.heatmap(numeric_df.corr(), annot=True, cmap='mako_r', fmt=".2f", linewidths=0.8,ax=ax)
                        ax.set_title("📊 Correlation Heatmap of Online Food Delivery Analysis")
                        st.pyplot(fig)      
                        st.subheader("📌 Business Insights")
                        st.markdown("""
                                * Order Value and Final Amount are Perfectly Correlated (Correlation = 1.00). This means the 
                                    final amount customers pay is primarily determined by the order value.
                                * Discount Applied has a Weak Negative Relationship with Final Amount (-0.07). Discounts are not significantly reducing revenue.
                                * Delivery Rating and Profit Margin have Moderate Positive Correlation (0.33).When customers receive orders on time and in good condition, satisfaction increases.
                                * Distance and delivery time show nearly zero correlation.Longer distances are not necessarily causing delays. Factors such as traffic, restaurant preparation time, and rider availability may have a larger impact.
                                * Customer Age has No Significant Relationship with Other Variables. Ordering behavior is similar across age groups.
                                * Restaurant ratings show very weak relationships with order value and profit margin.
                                * Apart from a few relationships, most correlations are close to zero. Customer behavior and delivery performance are influenced by multiple factors rather than a single variable.
                                * Increase average order value through upselling and combo offers.
                                * Improve delivery quality to boost customer satisfaction and profits.""")


with st.sidebar:
    st.title("🍔 Food Delivery Analytics")
    st.markdown("""
    ### 📌 Project Overview
    This interactive dashboard analyzes food delivery operations using SQL and Python. It provides insights into customer behavior, 
                restaurant performance, delivery efficiency, revenue trends, and business profitability through interactive visualizations and key performance indicators.
    """)

    st.markdown("---")
    st.markdown("""
    Explore business performance through📊:

    - Order Analytics

    - Revenue & Profit

    - Delivery Performance

    - Restaurant Insights

    - Customer Ratings

    - Discount Analysis

    - Interactive Visualizations

    - SQL-Based Analytics""")

    st.markdown("---")

    st.markdown(""" 
        ### 🛠 Tech Stack

         • Python

         • Streamlit

         • MySQL

         • Pandas

         • Plotly

         • SQLAlchemy """)

    st.markdown("---")
    st.success("📈 Transforming food delivery data into actionable business insights.")    