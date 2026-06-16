import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def render_product_analysis(df):
    st.subheader("📦 Product Utilization & Impact Analysis")
    st.markdown("Analyze how the number of products held, relationship depth, and strategic value combinations correlate with customer churn metrics.")

    # -------------------------------------------------------------------------
    # 0. Core Vectorized Pipeline Engineering (Runtime Data Fallbacks)
    # -------------------------------------------------------------------------
    plot_df = df.copy()
    plot_df["Status"] = plot_df["Exited"].map({0: "Retained", 1: "Churned"})
    
    # Structural Fallback Layer: Ensure advanced segment metrics exist at runtime
    if 'Product_Group' not in plot_df.columns:
        plot_df['Product_Group'] = np.where(plot_df['NumOfProducts'] == 1, 'Single Product', 'Multi Product')
        
    if 'Product_Depth_Segment' not in plot_df.columns:
        min_eng, max_eng = plot_df['engagement_score'].min(), plot_df['engagement_score'].max()
        norm_eng = ((plot_df['engagement_score'] - min_eng) / (max_eng - min_eng + 1e-5)) * 100
        plot_df['Product_Depth_Segment'] = np.select(
            [norm_eng <= 33, norm_eng <= 66], 
            ['Low Depth', 'Medium Depth'], 
            default='High Depth'
        )
        
    if 'Strategic_Risk_Segment' not in plot_df.columns:
        plot_df['Strategic_Risk_Segment'] = np.select([
            (plot_df['Product_Group'] == 'Single Product') & (plot_df['IsActiveMember'] == 0),
            (plot_df['Product_Group'] == 'Single Product') & (plot_df['IsActiveMember'] == 1),
            (plot_df['Product_Group'] == 'Multi Product') & (plot_df['IsActiveMember'] == 0)
        ], [
            'Segment 1: Silent Risk', 'Segment 2: Cross-Sell Opportunity', 'Segment 3: Retention Focus'
        ], default='Segment 4: Loyal Customers')

    # -------------------------------------------------------------------------
    # 1. KPI Top Summary Cards
    # -------------------------------------------------------------------------
    avg_churn = plot_df["Exited"].mean()
    avg_utilization = plot_df["Product_Utilization_Ratio"].mean() if "Product_Utilization_Ratio" in plot_df.columns else 0.0
    
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric("Total Customers", f"{len(plot_df):,}")
    with kpi2:
        st.metric("Average Churn Rate", f"{avg_churn:.1%}")
    with kpi3:
        st.metric("Avg Product Utilization", f"{avg_utilization:.2f}")

    st.write("---")

    # -------------------------------------------------------------------------
    # 2. Base Relationship Layout: Volume vs Density
    # -------------------------------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        churn_product = plot_df.groupby("NumOfProducts")["Exited"].mean().reset_index()
        churn_product["Churn Rate (%)"] = churn_product["Exited"] * 100

        fig_bar = px.bar(
            churn_product,
            x="NumOfProducts",
            y="Churn Rate (%)",
            title="<b>Churn Rate by Number of Products</b>",
            labels={"NumOfProducts": "Number of Products Held"},
            color="Churn Rate (%)",
            color_continuous_scale="Reds",
            text_auto=".1f"
        )
        fig_bar.update_layout(coloraxis_showscale=False, plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        fig_hist = px.histogram(
            plot_df,
            x="Product_Utilization_Ratio" if "Product_Utilization_Ratio" in plot_df.columns else "engagement_score",
            color="Status",
            title="<b>Product Utilization Distribution Profile</b>",
            labels={"Product_Utilization_Ratio": "Product Utilization Ratio", "count": "Customer Count"},
            barmode="overlay",
            color_discrete_map={"Retained": "#2b5c8f", "Churned": "#d9534f"},
            opacity=0.75
        )
        fig_hist.update_layout(plot_bgcolor="rgba(0,0,0,0)", legend_title_text="Status")
        st.plotly_chart(fig_hist, use_container_width=True)

    # -------------------------------------------------------------------------
    # 3. New Advanced Chart Insertions: Segment Matrices & Value Pools
    # -------------------------------------------------------------------------
    st.markdown("### 📊 Advanced Portfolio Risk & Behavioral Mappings")
    col3, col4 = st.columns(2)

    with col3:
        # Plot 1 Conversion: Churn Rates by Binary Product Grouping
        group_data = plot_df.groupby('Product_Group')["Exited"].mean().reset_index()
        group_data["Churn Rate (%)"] = group_data["Exited"] * 100
        
        fig_group = px.bar(
            group_data,
            x="Product_Group",
            y="Churn Rate (%)",
            title="<b>Churn Core Breakdown: Single vs. Multi-Product Tiers</b>",
            color="Product_Group",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            text_auto=".1f"
        )
        fig_group.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_group, use_container_width=True)

    with col4:
        # Plot 2 Conversion: Retention Trend Across Relationship Depth Profiles
        depth_data = plot_df.groupby('Product_Depth_Segment')["Exited"].mean().reset_index()
        # Enforce analytical sorting layout
        depth_map = {'Low Depth': 0, 'Medium Depth': 1, 'High Depth': 2}
        depth_data['Sort_Order'] = depth_data['Product_Depth_Segment'].map(depth_map)
        depth_data = depth_data.sort_values('Sort_Order')
        depth_data["Retention Rate (%)"] = (1 - depth_data["Exited"]) * 100
        
        fig_depth = px.line(
            depth_data,
            x="Product_Depth_Segment",
            y="Retention Rate (%)",
            title="<b>Retention Rate Trend by Relationship Depth Profile</b>",
            markers=True,
            labels={"Product_Depth_Segment": "Engagement Depth Profile"}
        )
        fig_depth.update_traces(line=dict(color="teal", width=4), marker=dict(size=10))
        fig_depth.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_depth, use_container_width=True)

    col5, col6 = st.columns(2)

    with col5:
        # Plot 3 Conversion: Customer Distribution Share across Strategic Risk Matrices
        risk_counts = plot_df['Strategic_Risk_Segment'].value_counts().reset_index()
        risk_counts.columns = ['Strategic_Risk_Segment', 'Volume']
        
        fig_pie = px.pie(
            risk_counts,
            values='Volume',
            names='Strategic_Risk_Segment',
            title='<b>Customer Base Volume Allocation across Strategic Risk Pools</b>',
            color_discrete_sequence=px.colors.qualitative.Safe,
            hole=0.4
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    with col6:
        # Plot 4 Conversion: Dual-Axis Graph (Avg Balance vs Churn Profile Map)
        seg_summary = plot_df.groupby('Strategic_Risk_Segment').agg(
            Churn_Rate=('Exited', lambda x: x.mean() * 100),
            Avg_Bal=('Balance', 'mean')
        ).reset_index().sort_values('Churn_Rate', ascending=False)

        # Build clean dual-axis traces via primary graphical handles
        fig_dual = go.Figure()
        fig_dual.add_trace(go.Bar(
            x=seg_summary['Strategic_Risk_Segment'],
            y=seg_summary['Avg_Bal'],
            name='Avg Balance ($)',
            marker_color='lightgray',
            opacity=0.85
        ))
        fig_dual.add_trace(go.Scatter(
            x=seg_summary['Strategic_Risk_Segment'],
            y=seg_summary['Churn_Rate'],
            name='Churn Rate (%)',
            yaxis='y2',
            mode='lines+markers',
            line=dict(color='crimson', width=3),
            marker=dict(size=8)
        ))
        fig_dual.update_layout(
            title="<b>Risk vs Value Mapping: Asset Balance vs. Churn</b>",
            xaxis=dict(tickangle=-15),
            yaxis=dict(title="Avg Wallet Asset Balance ($)", side="left"),
            yaxis2=dict(title="Segment Churn Rate (%)", side="right", overlaying="y", showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_dual, use_container_width=True)

    # -------------------------------------------------------------------------
    # 4. Enriched Segment Summary Table Framework
    # -------------------------------------------------------------------------
    st.markdown("### 📊 Product Segment Performance Summary")
    
    # Fallback to map data gracefully if Product_Segment isn't pre-computed
    if "Product_Segment" not in plot_df.columns:
        plot_df["Product_Segment"] = plot_df["Product_Group"]

    summary = (
        plot_df.groupby("Product_Segment")
        .agg(
            Customers=("CustomerId", "count"),
            ChurnRate=("Exited", "mean"),
            AvgEngagement=("engagement_score", "mean")
        )
        .reset_index()
    )

    st.data_editor(
        summary,
        column_config={
            "Product_Segment": st.column_config.TextColumn("Product Segment Designation"),
            "Customers": st.column_config.NumberColumn("Total Active Customers", format="%d"),
            "ChurnRate": st.column_config.ProgressColumn(
                "Observed Churn Rate",
                help="Average churn rate per product slice",
                format=".1%",
                min_value=0.0,
                max_value=1.0,
            ),
            "AvgEngagement": st.column_config.NumberColumn("Avg Segment Engagement", format="%.2f")
        },
        disabled=True,
        use_container_width=True,
        hide_index=True
    )