import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st


def render_high_value_detector(df, filters):
    st.subheader("🎯 High-Value Disengaged Customer Analytics Dashboard")

    # 1. Filter dataset for High-Value Disengaged Customers
    hv = df[
        (df["Balance"] >= filters["BalanceThreshold"])
        & (df["EstimatedSalary"] >= filters["SalaryThreshold"])
        & ((df["low_engagement_flag"] == 1) | (df["is_dormant_high_value"] == 1))
    ]

    if hv.empty:
        st.warning(
            "No customers match the current High-Value Disengaged criteria. Adjust filters to populate charts."
        )
        return

    # 2. Executive Key Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("At-Risk Customers", f"{len(hv):,}")
    c2.metric("Avg Balance", f"${hv['Balance'].mean():,.0f}")
    c3.metric("Avg CLV", f"${hv['Estimated_CLV'].mean():,.0f}")
    c4.metric("Avg Engagement", f"{hv['engagement_score'].mean():.2f}")

    st.markdown("---")

    # Organizing charts into intuitive tabs for dashboard real estate optimization
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📊 Core Profiles & Distribution",
            "📈 Engagement Cross-Analysis",
            "🧩 Segment & Cluster Deep Dives",
            "🗺️ Core Matrices & Correlations",
        ]
    )

    # -------------------------------------------------------------------------
    # TAB 1: Core Profiles & Distributions
    # -------------------------------------------------------------------------
    with tab1:
        st.markdown("### Core Metric Distributions & Profiles")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### 📦 Product Mix")
            prod_col = (
                "Product_Group" if "Product_Group" in hv.columns else "NumOfProducts"
            )
            prod_mix = hv[prod_col].value_counts().reset_index(name="Count")
            fig_prod = px.pie(
                prod_mix,
                values="Count",
                names=prod_col,
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.YlOrRd_r,
            )
            fig_prod.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=280)
            st.plotly_chart(fig_prod, use_container_width=True)

            st.markdown("##### 💰 Balance Distribution")
            fig_bal_dist = px.histogram(
                hv,
                x="Balance",
                nbins=15,
                color_discrete_sequence=["#e65c00"],
                marginal="rug",
            )
            fig_bal_dist.update_layout(
                margin=dict(l=10, r=10, t=10, b=10), height=280
            )
            st.plotly_chart(fig_bal_dist, use_container_width=True)

        with col2:
            st.markdown("##### ⏳ Tenure & Loyalty Profile")
            loy_col = (
                "Loyalty_Category" if "Loyalty_Category" in hv.columns else "Tenure"
            )
            fig_loyalty = px.histogram(
                hv,
                x="Tenure",
                color=loy_col if loy_col != "Tenure" else None,
                nbins=10,
                color_discrete_sequence=px.colors.sequential.Oranges_r,
            )
            fig_loyalty.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=280)
            st.plotly_chart(fig_loyalty, use_container_width=True)

            st.markdown("##### 💎 CLV Distribution")
            fig_clv_dist = px.histogram(
                hv,
                x="Estimated_CLV",
                nbins=15,
                color_discrete_sequence=["#1f77b4"],
                marginal="rug",
            )
            fig_clv_dist.update_layout(
                margin=dict(l=10, r=10, t=10, b=10), height=280
            )
            st.plotly_chart(fig_clv_dist, use_container_width=True)

    # -------------------------------------------------------------------------
    # TAB 2: Engagement Cross-Analysis
    # -------------------------------------------------------------------------
    with tab2:
        st.markdown("### Engagement Cross-Analysis Insights")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### ⚡ Engagement Score Distribution")
            fig_eng_dist = px.histogram(
                hv,
                x="engagement_score",
                nbins=15,
                color_discrete_sequence=["#2ca02c"],
                marginal="box",
            )
            fig_eng_dist.update_layout(height=300)
            st.plotly_chart(fig_eng_dist, use_container_width=True)

            st.markdown("##### 📉 Balance vs. Engagement")
            fig_bal_eng = px.scatter(
                hv,
                x="engagement_score",
                y="Balance",
                color="NumOfProducts",
                trendline="ols",
                color_continuous_scale=px.colors.sequential.Viridis,
            )
            fig_bal_eng.update_layout(height=320)
            st.plotly_chart(fig_bal_eng, use_container_width=True)

        with col2:
            st.markdown("##### 💵 Balance by Engagement Level")
            eng_lvl_col = (
                "Engagement_Level"
                if "Engagement_Level" in hv.columns
                else "Engagement_Segment"
            )
            fig_box_eng = px.box(
                hv,
                x=eng_lvl_col,
                y="Balance",
                color=eng_lvl_col,
                color_discrete_sequence=px.colors.qualitative.Safe,
            )
            fig_box_eng.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig_box_eng, use_container_width=True)

            st.markdown("##### 📈 CLV vs. Engagement")
            fig_clv_eng = px.scatter(
                hv,
                x="engagement_score",
                y="Estimated_CLV",
                color="IsActiveMember" if "IsActiveMember" in hv.columns else None,
                trendline="ols",
                color_discrete_sequence=px.colors.qualitative.Bold,
            )
            fig_clv_eng.update_layout(height=320)
            st.plotly_chart(fig_clv_eng, use_container_width=True)

    # -------------------------------------------------------------------------
    # TAB 3: Segment & Cluster Deep Dives
    # -------------------------------------------------------------------------
    with tab3:
        st.markdown("### Behavioral Cluster Drilldowns")
        cluster_col = "cluster_id" if "cluster_id" in hv.columns else "Cluster"

        if cluster_col in hv.columns:
            # Ensure cluster IDs string format for discreet chart labeling
            hv_plot = hv.copy()
            hv_plot[cluster_col] = hv_plot[cluster_col].astype(str)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("##### 📦 Cluster vs. Balance Dynamics")
                fig_clust_bal = px.box(
                    hv_plot,
                    x=cluster_col,
                    y="Balance",
                    color=cluster_col,
                    points="all",
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                )
                fig_clust_bal.update_layout(height=350, showlegend=False)
                st.plotly_chart(fig_clust_bal, use_container_width=True)

            with col2:
                st.markdown("##### ⚡ Cluster vs. Engagement Levels")
                fig_clust_eng = px.box(
                    hv_plot,
                    x=cluster_col,
                    y="engagement_score",
                    color=cluster_col,
                    points="all",
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                )
                fig_clust_eng.update_layout(height=350, showlegend=False)
                st.plotly_chart(fig_clust_eng, use_container_width=True)
        else:
            st.info(
                "Cluster features are missing or altered in the underlying dataframe segment."
            )

    # -------------------------------------------------------------------------
    # TAB 4: Core Matrices & Correlations
    with tab4:
        
        st.markdown("### Matrix Diagnostics")

    # 1. Financial Matrix: Balance vs Salary Base Scatter Plot Setup
        st.markdown("##### 💸 Salary vs. Balance Ecosystem")
    
    fig_financial = px.scatter(
        hv,
        x="EstimatedSalary",
        y="Balance",
        size="Estimated_CLV",
        color="Estimated_CLV", 
        hover_data=["CustomerId", "Age", "Tenure"],
        # Fixed parameter name here:
        color_continuous_scale="Plasma", 
    )
    fig_financial.update_layout(
        height=350, legend=dict(orientation="h", y=-0.2, x=0)
    )
    st.plotly_chart(fig_financial, use_container_width=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### 🗺️ High-Value vs. Engagement Risk Matrix")

        # Formulate actionable Quadrant Scatter View mapping Value against Action
        mid_clv = hv["Estimated_CLV"].median()
        mid_eng = hv["engagement_score"].median()

        fig_quad = px.scatter(
            hv,
            x="engagement_score",
            y="Estimated_CLV",
            color="Estimated_CLV",
            hover_data=["CustomerId", "Balance"],
            labels={
                "engagement_score": "Engagement Score",
                "Estimated_CLV": "Customer Lifetime Value (CLV)",
            },
            # Fixed parameter name here too:
            color_continuous_scale="Turbo",
        )
        
        # Quadrant Dividing Line Markers
        fig_quad.add_vline(x=mid_eng, line_dash="dash", line_color="red")
        fig_quad.add_hline(y=mid_clv, line_dash="dash", line_color="red")

        fig_quad.update_layout(
            height=380, legend=dict(orientation="h", y=-0.3, x=0)
        )
        st.plotly_chart(fig_quad, use_container_width=True)

    with col2:
        st.markdown("##### 🌡️ Feature Correlation Heatmap")

        # Selection of key features for correlation analysis
        core_corr_cols = [
            "Balance",
            "EstimatedSalary",
            "Estimated_CLV",
            "engagement_score",
            "Tenure",
            "NumOfProducts",
            "Age",
            "CreditScore",
        ]
        # Match only features that successfully exist inside the df frame
        available_corr_cols = [c for c in core_corr_cols if c in hv.columns]

        if len(available_corr_cols) > 1:
            corr_matrix = hv[available_corr_cols].corr().round(2)

            fig_corr = ff.create_annotated_heatmap(
                z=corr_matrix.values,
                x=list(corr_matrix.columns),
                y=list(corr_matrix.index),
                colorscale="RdBu", # Note: ff.create_annotated_heatmap DOES use 'colorscale'
                zmin=-1,
                zmax=1,
            )
            fig_corr.update_layout(
                height=380, margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig_corr, use_container_width=True)
        else:
            st.info("Insufficient quantitative variables for valid Correlation mapping.")