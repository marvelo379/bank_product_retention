# # # import numpy as np
# # # import plotly.express as px
# # # import plotly.figure_factory as ff
# # # import streamlit as st


# # # def render_high_value_detector(df, filters):
# # #     st.subheader("🎯 High-Value Disengaged Customer Analytics Dashboard")

# # #     # 1. Filter dataset for High-Value Disengaged Customers
# # #     hv = df[
# # #         (df["Balance"] >= filters["BalanceThreshold"])
# # #         & (df["EstimatedSalary"] >= filters["SalaryThreshold"])
# # #         & ((df["low_engagement_flag"] == 1) | (df["is_dormant_high_value"] == 1))
# # #     ]

# # #     if hv.empty:
# # #         st.warning(
# # #             "No customers match the current High-Value Disengaged criteria. Adjust filters to populate charts."
# # #         )
# # #         return

# # #     # 2. Executive Key Metrics
# # #     c1, c2, c3, c4 = st.columns(4)
# # #     c1.metric("At-Risk Customers", f"{len(hv):,}")
# # #     c2.metric("Avg Balance", f"${hv['Balance'].mean():,.0f}")
# # #     c3.metric("Avg CLV", f"${hv['Estimated_CLV'].mean():,.0f}")
# # #     c4.metric(
# # #     "Avg Engagement",
# # #     f"{hv['engagement_score'].mean() * 100:.2f}%"
# # # )

# # #     st.markdown("---")

# # #     # Organizing charts into intuitive tabs for dashboard real estate optimization
# # #     tab1, tab2, tab3, tab4 = st.tabs(
# # #         [
# # #             "📊 Core Profiles & Distribution",
# # #             "📈 Engagement Cross-Analysis",
# # #             "🧩 Segment & Cluster Deep Dives",
# # #             "🗺️ Core Matrices & Correlations",
# # #         ]
# # #     )

# # #     # -------------------------------------------------------------------------
# # #     # TAB 1: Core Profiles & Distributions
# # #     # -------------------------------------------------------------------------
# # #     with tab1:
# # #         st.markdown("### Core Metric Distributions & Profiles")
# # #         col1, col2 = st.columns(2)

# # #         with col1:
# # #             st.markdown("##### 📦 Product Mix")
# # #             prod_col = (
# # #                 "Product_Group" if "Product_Group" in hv.columns else "NumOfProducts"
# # #             )
# # #             prod_mix = hv[prod_col].value_counts().reset_index(name="Count")
# # #             fig_prod = px.pie(
# # #                 prod_mix,
# # #                 values="Count",
# # #                 names=prod_col,
# # #                 hole=0.4,
# # #                 color_discrete_sequence=px.colors.sequential.YlOrRd_r,
# # #             )
# # #             fig_prod.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=280)
# # #             st.plotly_chart(fig_prod, use_container_width=True)

# # #             st.markdown("##### 💰 Balance Distribution")
# # #             fig_bal_dist = px.histogram(
# # #                 hv,
# # #                 x="Balance",
# # #                 nbins=15,
# # #                 color_discrete_sequence=["#e65c00"],
# # #                 marginal="rug",
# # #             )
# # #             fig_bal_dist.update_layout(
# # #                 margin=dict(l=10, r=10, t=10, b=10), height=280
# # #             )
# # #             st.plotly_chart(fig_bal_dist, use_container_width=True)

# # #         with col2:
# # #             st.markdown("##### ⏳ Tenure & Loyalty Profile")
# # #             loy_col = (
# # #                 "Loyalty_Category" if "Loyalty_Category" in hv.columns else "Tenure"
# # #             )
# # #             fig_loyalty = px.histogram(
# # #                 hv,
# # #                 x="Tenure",
# # #                 color=loy_col if loy_col != "Tenure" else None,
# # #                 nbins=10,
# # #                 color_discrete_sequence=px.colors.sequential.Oranges_r,
# # #             )
# # #             fig_loyalty.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=280)
# # #             st.plotly_chart(fig_loyalty, use_container_width=True)

# # #             st.markdown("##### 💎 CLV Distribution")
# # #             fig_clv_dist = px.histogram(
# # #                 hv,
# # #                 x="Estimated_CLV",
# # #                 nbins=15,
# # #                 color_discrete_sequence=["#1f77b4"],
# # #                 marginal="rug",
# # #             )
# # #             fig_clv_dist.update_layout(
# # #                 margin=dict(l=10, r=10, t=10, b=10), height=280
# # #             )
# # #             st.plotly_chart(fig_clv_dist, use_container_width=True)

# # #     # -------------------------------------------------------------------------
# # #     # TAB 2: Engagement Cross-Analysis
# # #     # -------------------------------------------------------------------------
# # #     with tab2:
# # #         st.markdown("### Engagement Cross-Analysis Insights")

# # #         col1, col2 = st.columns(2)
# # #         with col1:
# # #             st.markdown("##### ⚡ Engagement Score Distribution")
# # #             fig_eng_dist = px.histogram(
# # #                 hv,
# # #                 x="engagement_score",
# # #                 nbins=15,
# # #                 color_discrete_sequence=["#2ca02c"],
# # #                 marginal="box",
# # #             )
# # #             fig_eng_dist.update_layout(height=300)
# # #             st.plotly_chart(fig_eng_dist, use_container_width=True)

# # #             st.markdown("##### 📉 Balance vs. Engagement")
# # #             fig_bal_eng = px.scatter(
# # #                 hv,
# # #                 x="engagement_score",
# # #                 y="Balance",
# # #                 color="NumOfProducts",
# # #                 trendline="ols",
# # #                 color_continuous_scale=px.colors.sequential.Viridis,
# # #             )
# # #             fig_bal_eng.update_layout(height=320)
# # #             st.plotly_chart(fig_bal_eng, use_container_width=True)

# # #         with col2:
# # #             st.markdown("##### 💵 Balance by Engagement Level")
# # #             eng_lvl_col = (
# # #                 "Engagement_Level"
# # #                 if "Engagement_Level" in hv.columns
# # #                 else "Engagement_Segment"
# # #             )
# # #             fig_box_eng = px.box(
# # #                 hv,
# # #                 x=eng_lvl_col,
# # #                 y="Balance",
# # #                 color=eng_lvl_col,
# # #                 color_discrete_sequence=px.colors.qualitative.Safe,
# # #             )
# # #             fig_box_eng.update_layout(height=300, showlegend=False)
# # #             st.plotly_chart(fig_box_eng, use_container_width=True)

# # #             st.markdown("##### 📈 CLV vs. Engagement")
# # #             fig_clv_eng = px.scatter(
# # #                 hv,
# # #                 x="engagement_score",
# # #                 y="Estimated_CLV",
# # #                 color="IsActiveMember" if "IsActiveMember" in hv.columns else None,
# # #                 trendline="ols",
# # #                 color_discrete_sequence=px.colors.qualitative.Bold,
# # #             )
# # #             fig_clv_eng.update_layout(height=320)
# # #             st.plotly_chart(fig_clv_eng, use_container_width=True)

# # #     # -------------------------------------------------------------------------
# # #     # TAB 3: Segment & Cluster Deep Dives
# # #     # -------------------------------------------------------------------------
# # #     with tab3:
# # #         st.markdown("### Behavioral Cluster Drilldowns")
# # #         cluster_col = "cluster_id" if "cluster_id" in hv.columns else "Cluster"

# # #         if cluster_col in hv.columns:
# # #             # Ensure cluster IDs string format for discreet chart labeling
# # #             hv_plot = hv.copy()
# # #             hv_plot[cluster_col] = hv_plot[cluster_col].astype(str)

# # #             col1, col2 = st.columns(2)
# # #             with col1:
# # #                 st.markdown("##### 📦 Cluster vs. Balance Dynamics")
# # #                 fig_clust_bal = px.box(
# # #                     hv_plot,
# # #                     x=cluster_col,
# # #                     y="Balance",
# # #                     color=cluster_col,
# # #                     points="all",
# # #                     color_discrete_sequence=px.colors.qualitative.Pastel,
# # #                 )
# # #                 fig_clust_bal.update_layout(height=350, showlegend=False)
# # #                 st.plotly_chart(fig_clust_bal, use_container_width=True)

# # #             with col2:
# # #                 st.markdown("##### ⚡ Cluster vs. Engagement Levels")
# # #                 fig_clust_eng = px.box(
# # #                     hv_plot,
# # #                     x=cluster_col,
# # #                     y="engagement_score",
# # #                     color=cluster_col,
# # #                     points="all",
# # #                     color_discrete_sequence=px.colors.qualitative.Pastel,
# # #                 )
# # #                 fig_clust_eng.update_layout(height=350, showlegend=False)
# # #                 st.plotly_chart(fig_clust_eng, use_container_width=True)
# # #         else:
# # #             st.info(
# # #                 "Cluster features are missing or altered in the underlying dataframe segment."
# # #             )

# # #     # -------------------------------------------------------------------------
# # #     # TAB 4: Core Matrices & Correlations
# # #     with tab4:
        
# # #         st.markdown("### Matrix Diagnostics")

# # #     # 1. Financial Matrix: Balance vs Salary Base Scatter Plot Setup
# # #         st.markdown("##### 💸 Salary vs. Balance Ecosystem")
    
# # #     fig_financial = px.scatter(
# # #         hv,
# # #         x="EstimatedSalary",
# # #         y="Balance",
# # #         size="Estimated_CLV",
# # #         color="Estimated_CLV", 
# # #         hover_data=["CustomerId", "Age", "Tenure"],
# # #         # Fixed parameter name here:
# # #         color_continuous_scale="Plasma", 
# # #     )
# # #     fig_financial.update_layout(
# # #         height=350, legend=dict(orientation="h", y=-0.2, x=0)
# # #     )
# # #     st.plotly_chart(fig_financial, use_container_width=True)

# # #     st.markdown("---")

# # #     col1, col2 = st.columns(2)

# # #     with col1:
# # #         st.markdown("##### 🗺️ High-Value vs. Engagement Risk Matrix")

# # #         # Formulate actionable Quadrant Scatter View mapping Value against Action
# # #         mid_clv = hv["Estimated_CLV"].median()
# # #         mid_eng = hv["engagement_score"].median()

# # #         fig_quad = px.scatter(
# # #             hv,
# # #             x="engagement_score",
# # #             y="Estimated_CLV",
# # #             color="Estimated_CLV",
# # #             hover_data=["CustomerId", "Balance"],
# # #             labels={
# # #                 "engagement_score": "Engagement Score",
# # #                 "Estimated_CLV": "Customer Lifetime Value (CLV)",
# # #             },
# # #             # Fixed parameter name here too:
# # #             color_continuous_scale="Turbo",
# # #         )
        
# # #         # Quadrant Dividing Line Markers
# # #         fig_quad.add_vline(x=mid_eng, line_dash="dash", line_color="red")
# # #         fig_quad.add_hline(y=mid_clv, line_dash="dash", line_color="red")

# # #         fig_quad.update_layout(
# # #             height=380, legend=dict(orientation="h", y=-0.3, x=0)
# # #         )
# # #         st.plotly_chart(fig_quad, use_container_width=True)

# # #     with col2:
# # #         st.markdown("##### 🌡️ Feature Correlation Heatmap")

# # #         # Selection of key features for correlation analysis
# # #         core_corr_cols = [
# # #             "Balance",
# # #             "EstimatedSalary",
# # #             "Estimated_CLV",
# # #             "engagement_score",
# # #             "Tenure",
# # #             "NumOfProducts",
# # #             "Age",
# # #             "CreditScore",
# # #         ]
# # #         # Match only features that successfully exist inside the df frame
# # #         available_corr_cols = [c for c in core_corr_cols if c in hv.columns]

# # #         if len(available_corr_cols) > 1:
# # #             corr_matrix = hv[available_corr_cols].corr().round(2)

# # #             fig_corr = ff.create_annotated_heatmap(
# # #                 z=corr_matrix.values,
# # #                 x=list(corr_matrix.columns),
# # #                 y=list(corr_matrix.index),
# # #                 colorscale="RdBu", # Note: ff.create_annotated_heatmap DOES use 'colorscale'
# # #                 zmin=-1,
# # #                 zmax=1,
# # #             )
# # #             fig_corr.update_layout(
# # #                 height=380, margin=dict(l=10, r=10, t=30, b=10)
# # #             )
# # #             st.plotly_chart(fig_corr, use_container_width=True)
# # #         else:
# # #             st.info("Insufficient quantitative variables for valid Correlation mapping.")

# # import numpy as np
# # import pandas as pd
# # import plotly.figure_factory as ff
# # import plotly.graph_objects as go
# # import streamlit as st


# # def render_high_value_detector(df, filters):
# #     st.subheader("🎯 High-Value Disengaged Customer Analytics Dashboard")

# #     # 1. Filter dataset for High-Value Disengaged Customers
# #     hv = df[
# #         (df["Balance"] >= filters["BalanceThreshold"])
# #         & (df["EstimatedSalary"] >= filters["SalaryThreshold"])
# #         & ((df["low_engagement_flag"] == 1) | (df["is_dormant_high_value"] == 1))
# #     ].copy()

# #     if hv.empty:
# #         st.warning(
# #             "No customers match the current High-Value Disengaged criteria. Adjust filters to populate charts."
# #         )
# #         return

# #     # 2. Executive Key Metrics
# #     c1, c2, c3, c4 = st.columns(4)
# #     c1.metric("At-Risk Customers", f"{len(hv):,}")
# #     c2.metric("Avg Balance", f"${hv['Balance'].mean():,.0f}")
# #     c3.metric("Avg CLV", f"${hv['Estimated_CLV'].mean():,.0f}")
# #     c4.metric("Avg Engagement", f"{hv['engagement_score'].mean() * 100:.2f}%")

# #     st.markdown("---")

# #     tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
# #         [
# #             "📊 Core Profiles & Distribution",
# #             "📈 Engagement Cross-Analysis",
# #             "🧩 Segment & Cluster Deep Dives",
# #             "🗺️ Core Matrices & Correlations",
# #             "🚨 Churn & Risk Analytics",
# #             "🌍 Geo-Demographic & Top-N Risk",
# #         ]
# #     )

# #     # -------------------------------------------------------------------------
# #     # TAB 1: Core Profiles & Distributions
# #     # -------------------------------------------------------------------------
# #     with tab1:
# #         st.markdown("### Core Metric Distributions & Profiles")
# #         col1, col2 = st.columns(2)

# #         with col1:
# #             st.markdown("##### 📦 Product Mix")
# #             prod_col = "Product_Group" if "Product_Group" in hv.columns else "NumOfProducts"
# #             prod_counts = hv[prod_col].value_counts()
            
# #             fig_prod = go.Figure(data=[go.Pie(
# #                 labels=prod_counts.index, 
# #                 values=prod_counts.values, 
# #                 hole=0.4,
# #                 marker=dict(colors=colorscale_to_list("YlOrRd_r", len(prod_counts)))
# #             )])
# #             fig_prod.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=280)
# #             st.plotly_chart(fig_prod, use_container_width=True)

# #             st.markdown("##### 💰 Balance Distribution")
# #             fig_bal_dist = go.Figure(data=[go.Histogram(x=hv["Balance"], nbinsx=15, marker_color="#e65c00")])
# #             fig_bal_dist.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=280, xaxis_title="Balance", yaxis_title="Count")
# #             st.plotly_chart(fig_bal_dist, use_container_width=True)

# #         with col2:
# #             st.markdown("##### ⏳ Tenure & Loyalty Profile")
# #             fig_loyalty = go.Figure(data=[go.Histogram(x=hv["Tenure"], nbinsx=10, marker_color="#ff7f0e")])
# #             fig_loyalty.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=280, xaxis_title="Tenure", yaxis_title="Count")
# #             st.plotly_chart(fig_loyalty, use_container_width=True)

# #             st.markdown("##### 💎 CLV Distribution")
# #             fig_clv_dist = go.Figure(data=[go.Histogram(x=hv["Estimated_CLV"], nbinsx=15, marker_color="#1f77b4")])
# #             fig_clv_dist.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=280, xaxis_title="Estimated CLV", yaxis_title="Count")
# #             st.plotly_chart(fig_clv_dist, use_container_width=True)

# #     # -------------------------------------------------------------------------
# #     # TAB 2: Engagement Cross-Analysis
# #     # -------------------------------------------------------------------------
# #     with tab2:
# #         st.markdown("### Engagement Cross-Analysis Insights")
# #         col1, col2 = st.columns(2)
        
# #         with col1:
# #             st.markdown("##### ⚡ Engagement Score Distribution")
# #             fig_eng_dist = go.Figure(data=[go.Histogram(x=hv["engagement_score"], nbinsx=15, marker_color="#2ca02c")])
# #             fig_eng_dist.update_layout(height=300, xaxis_title="Engagement Score", yaxis_title="Count")
# #             st.plotly_chart(fig_eng_dist, use_container_width=True)

# #             st.markdown("##### 📉 Balance vs. Engagement")
# #             fig_bal_eng = go.Figure(data=[go.Scatter(
# #                 x=hv["engagement_score"], 
# #                 y=hv["Balance"], 
# #                 mode="markers",
# #                 marker=dict(color=hv["NumOfProducts"], colorscale="Viridis", showscale=True, title="Products")
# #             )])
# #             # Optional linear trendline approximation manual calculation
# #             if len(hv) > 1:
# #                 m, b = np.polyfit(hv["engagement_score"], hv["Balance"], 1)
# #                 fig_bal_eng.add_trace(go.Scatter(x=hv["engagement_score"], y=m*hv["engagement_score"]+b, mode="lines", name="OLS Trend", line=dict(color="red")))
# #             fig_bal_eng.update_layout(height=320, xaxis_title="Engagement Score", yaxis_title="Balance", showlegend=False)
# #             st.plotly_chart(fig_bal_eng, use_container_width=True)

# #         with col2:
# #             st.markdown("##### 💵 Balance by Engagement Level")
# #             eng_lvl_col = "Engagement_Level" if "Engagement_Level" in hv.columns else "Engagement_Segment"
# #             fig_box_eng = go.Figure()
# #             for name, group in hv.groupby(eng_lvl_col):
# #                 fig_box_eng.add_trace(go.Box(y=group["Balance"], name=str(name)))
# #             fig_box_eng.update_layout(height=300, showlegend=False, yaxis_title="Balance")
# #             st.plotly_chart(fig_box_eng, use_container_width=True)

# #             st.markdown("##### 📈 CLV vs. Engagement")
# #             fig_clv_eng = go.Figure()
# #             active_col = "IsActiveMember" if "IsActiveMember" in hv.columns else "active_flag"
# #             for name, group in hv.groupby(active_col):
# #                 lbl = "Active" if name == 1 else "Inactive"
# #                 fig_clv_eng.add_trace(go.Scatter(x=group["engagement_score"], y=group["Estimated_CLV"], mode="markers", name=lbl))
# #             fig_clv_eng.update_layout(height=320, xaxis_title="Engagement Score", yaxis_title="Estimated CLV")
# #             st.plotly_chart(fig_clv_eng, use_container_width=True)

# #     # -------------------------------------------------------------------------
# #     # TAB 3: Segment & Cluster Deep Dives
# #     # -------------------------------------------------------------------------
# #     with tab3:
# #         st.markdown("### Behavioral Cluster Drilldowns")
# #         cluster_col = "cluster_id" if "cluster_id" in hv.columns else "Cluster"

# #         if cluster_col in hv.columns:
# #             col1, col2 = st.columns(2)
# #             with col1:
# #                 st.markdown("##### 📦 Cluster vs. Balance Dynamics")
# #                 fig_clust_bal = go.Figure()
# #                 for name, group in hv.groupby(cluster_col):
# #                     fig_clust_bal.add_trace(go.Box(y=group["Balance"], name=f"Cluster {name}", boxpoints="all"))
# #                 fig_clust_bal.update_layout(height=350, showlegend=False, yaxis_title="Balance")
# #                 st.plotly_chart(fig_clust_bal, use_container_width=True)

# #             with col2:
# #                 st.markdown("##### ⚡ Cluster vs. Engagement Levels")
# #                 fig_clust_eng = go.Figure()
# #                 for name, group in hv.groupby(cluster_col):
# #                     fig_clust_eng.add_trace(go.Box(y=group["engagement_score"], name=f"Cluster {name}", boxpoints="all"))
# #                 fig_clust_eng.update_layout(height=350, showlegend=False, yaxis_title="Engagement Score")
# #                 st.plotly_chart(fig_clust_eng, use_container_width=True)
# #         else:
# #             st.info("Cluster features are missing or altered in the underlying dataframe segment.")

# #     # -------------------------------------------------------------------------
# #     # TAB 4: Core Matrices & Correlations
# #     # -------------------------------------------------------------------------
# #     with tab4:
# #         st.markdown("### Matrix Diagnostics")
# #         st.markdown("##### 💸 Salary vs. Balance Ecosystem")

# #         # Handle size scaling normalization securely for scatter sizing definitions
# #         max_clv = hv["Estimated_CLV"].max() if hv["Estimated_CLV"].max() > 0 else 1
# #         sizes = (hv["Estimated_CLV"] / max_clv) * 30 + 10

# #         fig_financial = go.Figure(data=[go.Scatter(
# #             x=hv["EstimatedSalary"],
# #             y=hv["Balance"],
# #             mode="markers",
# #             marker=dict(
# #                 size=sizes,
# #                 color=hv["Estimated_CLV"],
# #                 colorscale="Plasma",
# #                 showscale=True,
# #                 title="CLV"
# #             ),
# #             text=[f"ID: {cid}<br>Age: {age}<br>Tenure: {ten}" for cid, age, ten in zip(hv["CustomerId"], hv["Age"], hv["Tenure"])],
# #             hoverinfo="text+x+y"
# #         )])
# #         fig_financial.update_layout(height=350, xaxis_title="Estimated Salary", yaxis_title="Balance")
# #         st.plotly_chart(fig_financial, use_container_width=True)

# #         st.markdown("---")
# #         col1, col2 = st.columns(2)

# #         with col1:
# #             st.markdown("##### 🗺️ High-Value vs. Engagement Risk Matrix")
# #             mid_clv = hv["Estimated_CLV"].median()
# #             mid_eng = hv["engagement_score"].median()

# #             fig_quad = go.Figure(data=[go.Scatter(
# #                 x=hv["engagement_score"],
# #                 y=hv["Estimated_CLV"],
# #                 mode="markers",
# #                 marker=dict(color=hv["Estimated_CLV"], colorscale="Turbo", showscale=True)
# #             )])
# #             fig_quad.add_shape(type="line", x0=mid_eng, y0=hv["Estimated_CLV"].min(), x1=mid_eng, y1=hv["Estimated_CLV"].max(), line=dict(color="red", dash="dash"))
# #             fig_quad.add_shape(type="line", x0=hv["engagement_score"].min(), y0=mid_clv, x1=hv["engagement_score"].max(), y1=mid_clv, line=dict(color="red", dash="dash"))
# #             fig_quad.update_layout(height=380, xaxis_title="Engagement Score", yaxis_title="Customer Lifetime Value (CLV)")
# #             st.plotly_chart(fig_quad, use_container_width=True)

# #         with col2:
# #             st.markdown("##### 🌡️ Feature Correlation Heatmap")
# #             core_corr_cols = ["Balance", "EstimatedSalary", "Estimated_CLV", "engagement_score", "Tenure", "NumOfProducts", "Age", "CreditScore"]
# #             available_corr_cols = [c for c in core_corr_cols if c in hv.columns]

# #             if len(available_corr_cols) > 1:
# #                 corr_matrix = hv[available_corr_cols].corr().round(2)
# #                 fig_corr = ff.create_annotated_heatmap(
# #                     z=corr_matrix.values,
# #                     x=list(corr_matrix.columns),
# #                     y=list(corr_matrix.index),
# #                     colorscale="RdBu",
# #                     zmin=-1, zmax=1
# #                 )
# #                 fig_corr.update_layout(height=380, margin=dict(l=10, r=10, t=30, b=10))
# #                 st.plotly_chart(fig_corr, use_container_width=True)
# #             else:
# #                 st.info("Insufficient quantitative variables for valid Correlation mapping.")

# #     # -------------------------------------------------------------------------
# #     # TAB 5: Churn & Risk Analytics
# #     # -------------------------------------------------------------------------
# #     with tab5:
# #         st.markdown("### Churn & Retention Segmentation")
# #         col1, col2 = st.columns(2)

# #         with col1:
# #             st.markdown("##### 📉 Churn by Balance Segment")
# #             bal_cat = "Balance_Category" if "Balance_Category" in hv.columns else "high_balance_flag"
            
# #             fig_bal_churn = go.Figure()
# #             if bal_cat in hv.columns:
# #                 for status, color in zip([0, 1], ["#2ca02c", "#d62728"]):
# #                     lbl = "Retained" if status == 0 else "Churned"
# #                     sub = hv[hv["Exited"] == status]
# #                     counts = sub[bal_cat].value_counts(normalize=True) * 100
# #                     fig_bal_churn.add_trace(go.Bar(x=counts.index, y=counts.values, name=lbl, marker_color=color))
# #             fig_bal_churn.update_layout(height=300, barmode="group", yaxis_title="Percentage (%)")
# #             st.plotly_chart(fig_bal_churn, use_container_width=True)

# #         with col2:
# #             st.markdown("##### 💳 Churn by Credit Score Band")
# #             hv_copy = hv.copy()
# #             hv_copy["CreditScore_Band"] = pd.cut(
# #                 hv_copy["CreditScore"],
# #                 bins=[0, 579, 669, 739, 799, 850],
# #                 labels=["Poor", "Fair", "Good", "Very Good", "Exceptional"]
# #             )
# #             fig_cs_churn = go.Figure()
# #             for status, color in zip([0, 1], ["#2ca02c", "#d62728"]):
# #                 lbl = "Retained" if status == 0 else "Churned"
# #                 sub = hv_copy[hv_copy["Exited"] == status]
# #                 counts = sub["CreditScore_Band"].value_counts(normalize=True) * 100
# #                 fig_cs_churn.add_trace(go.Bar(x=counts.index, y=counts.values, name=lbl, marker_color=color))
# #             fig_cs_churn.update_layout(height=300, barmode="group", yaxis_title="Percentage (%)")
# #             st.plotly_chart(fig_cs_churn, use_container_width=True)

# #         st.markdown("---")
# #         col3, col4 = st.columns(2)

# #         with col3:
# #             st.markdown("##### 📦 Churn by Products Held")
# #             fig_prod_churn = go.Figure()
# #             for status, color in zip([0, 1], ["#2ca02c", "#d62728"]):
# #                 lbl = "Retained" if status == 0 else "Churned"
# #                 sub = hv[hv["Exited"] == status]
# #                 counts = sub["NumOfProducts"].value_counts(normalize=True) * 100
# #                 fig_prod_churn.add_trace(go.Bar(x=counts.index, y=counts.values, name=lbl, marker_color=color))
# #             fig_prod_churn.update_layout(height=300, barmode="stack", yaxis_title="Percentage (%)")
# #             st.plotly_chart(fig_prod_churn, use_container_width=True)

# #         with col4:
# #             st.markdown("##### 💵 Average Balance: Retained vs. Churned")
# #             avg_bal = hv.groupby("Exited")["Balance"].mean()
# #             fig_avg_bal = go.Figure(data=[go.Bar(
# #                 x=["Retained Base", "Churned Base"],
# #                 y=[avg_bal.get(0, 0), avg_bal.get(1, 0)],
# #                 marker_color=["#1f77b4", "#ff7f0e"]
# #             )])
# #             fig_avg_bal.update_layout(height=300, yaxis_title="Average Balance ($)")
# #             st.plotly_chart(fig_avg_bal, use_container_width=True)

# #     # -------------------------------------------------------------------------
# #     # TAB 6: Geo-Demographic & Top-N Risk
# #     # -------------------------------------------------------------------------
# #     with tab6:
# #         st.markdown("### Geographic Real-Estate & High-Value Risks")

# #         # Map One-Hot encoded elements safely to structural layout categories
# #         hv_geo = hv.copy()
# #         if "Geography_Germany" in hv_geo.columns and "Geography_Spain" in hv_geo.columns:
# #             hv_geo["Geography"] = np.select(
# #                 [hv_geo["Geography_Germany"] == 1, hv_geo["Geography_Spain"] == 1],
# #                 ["Germany", "Spain"], default="France"
# #             )
# #         else:
# #             hv_geo["Geography"] = "Unknown Base"

# #         col1, col2 = st.columns(2)

# #         with col1:
# #             st.markdown("##### 🌐 High-Value vs. Standard Churn by Geography")
# #             df_total_geo = df.copy()
# #             if "Geography_Germany" in df_total_geo.columns and "Geography_Spain" in df_total_geo.columns:
# #                 df_total_geo["Geography"] = np.select(
# #                     [df_total_geo["Geography_Germany"] == 1, df_total_geo["Geography_Spain"] == 1],
# #                     ["Germany", "Spain"], default="France"
# #                 )
# #             else:
# #                 df_total_geo["Geography"] = "Unknown Base"

# #             std_geo_rates = df_total_geo.groupby("Geography")["Exited"].mean() * 100
# #             hv_geo_rates = hv_geo.groupby("Geography")["Exited"].mean() * 100

# #             fig_geo_comp = go.Figure(data=[
# #                 go.Bar(x=std_geo_rates.index, y=std_geo_rates.values, name="Standard Cohort", marker_color="#8da0cb"),
# #                 go.Bar(x=hv_geo_rates.index, y=hv_geo_rates.values, name="High-Value Segment", marker_color="#fc8d62")
# #             ])
# #             fig_geo_comp.update_layout(height=320, barmode="group", yaxis_title="Churn Rate (%)")
# #             st.plotly_chart(fig_geo_comp, use_container_width=True)

# #         with col2:
# #             st.markdown("##### ⚥ High-Value Balance at Risk: Country & Gender")
# #             hv_geo["Gender"] = np.where(hv_geo["Gender_Male"] == 1, "Male", "Female")
            
# #             fig_geo_gender = go.Figure()
# #             for gender, color in zip(["Male", "Female"], ["#17becf", "#e377c2"]):
# #                 sub = hv_geo[hv_geo["Gender"] == gender]
# #                 geo_sums = sub.groupby("Geography")["Balance"].sum()
# #                 fig_geo_gender.add_trace(go.Bar(x=geo_sums.index, y=geo_sums.values, name=gender, marker_color=color))
            
# #             fig_geo_gender.update_layout(height=320, barmode="stack", yaxis_title="Total Balance Exposure ($)")
# #             st.plotly_chart(fig_geo_gender, use_container_width=True)

# #         st.markdown("---")

# #         # 3. Churned High-Value Customer Details Table with Dynamic Slider Control
# #         st.markdown("##### 🚨 Churned High-Value Customer Registry")
# #         churned_hv = hv_geo[hv_geo["Exited"] == 1]

# #         if not churned_hv.empty:
# #             max_limit = min(len(churned_hv), 100)
# #             top_n = st.slider(
# #                 "Filter Registry Focus Depth (Top N Rows)",
# #                 min_value=5,
# #                 max_value=max_limit if max_limit > 5 else 10,
# #                 value=9,
# #                 step=1,
# #             )

# #             display_cols = ["CustomerId", "Surname", "Geography", "Gender", "Age", "Balance", "EstimatedSalary", "Estimated_CLV", "engagement_score", "NumOfProducts"]
# #             available_display = [c for c in display_cols if c in churned_hv.columns]

# #             churned_sorted = churned_hv.sort_values(
# #                 by=["Balance", "engagement_score"], ascending=[False, True]
# #             )[available_display].head(top_n)

# #             st.dataframe(
# #                 churned_sorted.style.format(
# #                     {
# #                         "Balance": "${:,.2f}",
# #                         "EstimatedSalary": "${:,.2f}",
# #                         "Estimated_CLV": "${:,.2f}",
# #                         "engagement_score": "{:.2f}%",
# #                     }
# #                 ),
# #                 use_container_width=True,
# #             )
# #         else:
# #             st.success("Excellent! Zero High-Value customers matching criteria have churned.")


# # def colorscale_to_list(scale_name, num_colors):
# #     """Helper function to fetch sequential layout colors from built-in maps safely."""
# #     import plotly.colors as colors
# #     try:
# #         scale = getattr(colors.sequential, scale_name)
# #         return colors.sample_colorscale(scale, num_colors)
# #     except AttributeError:
# #         return ["#1f77b4"] * num_colors
# import numpy as np
# import pandas as pd
# import plotly.figure_factory as ff
# import plotly.graph_objects as go
# import streamlit as st


# def render_high_value_detector(df, filters):
#     st.subheader("🎯 High-Value Disengaged Customer Analytics Dashboard")

#     # 1. Filter dataset for High-Value Disengaged Customers
#     hv = df[
#         (df["Balance"] >= filters["BalanceThreshold"])
#         & (df["EstimatedSalary"] >= filters["SalaryThreshold"])
#         & ((df["low_engagement_flag"] == 1) | (df["is_dormant_high_value"] == 1))
#     ].copy()

#     if hv.empty:
#         st.warning(
#             "No customers match the current High-Value Disengaged criteria. Adjust filters to populate charts."
#         )
#         return

#     # 2. Executive Key Metrics
#     c1, c2, c3, c4 = st.columns(4)
#     c1.metric("At-Risk Customers", f"{len(hv):,}")
#     c2.metric("Avg Balance", f"${hv['Balance'].mean():,.0f}")
#     c3.metric("Avg CLV", f"${hv['Estimated_CLV'].mean():,.0f}")
#     c4.metric("Avg Engagement", f"{hv['engagement_score'].mean() * 100:.2f}%")

#     st.markdown("---")

#     tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
#         [
#             "📊 Core Profiles & Distribution",
#             "📈 Engagement Cross-Analysis",
#             "🧩 Segment & Cluster Deep Dives",
#             "🗺️ Core Matrices & Correlations",
#             "🚨 Churn & Risk Analytics",
#             "🌍 Geo-Demographic & Top-N Risk",
#         ]
#     )

#     # -------------------------------------------------------------------------
#     # TAB 1: Core Profiles & Distributions
#     # -------------------------------------------------------------------------
#     with tab1:
#         st.markdown("### Core Metric Distributions & Profiles")
#         col1, col2 = st.columns(2)

#         with col1:
#             st.markdown("##### 📦 Product Mix")
#             prod_col = "Product_Group" if "Product_Group" in hv.columns else "NumOfProducts"
#             prod_counts = hv[prod_col].value_counts()
            
#             fig_prod = go.Figure(data=[go.Pie(
#                 labels=prod_counts.index, 
#                 values=prod_counts.values, 
#                 hole=0.4,
#                 marker=dict(colors=colorscale_to_list("YlOrRd_r", len(prod_counts)))
#             )])
#             fig_prod.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=280)
#             st.plotly_chart(fig_prod, use_container_width=True)

#             st.markdown("##### 💰 Balance Distribution")
#             fig_bal_dist = go.Figure(data=[go.Histogram(x=hv["Balance"], nbinsx=15, marker_color="#e65c00")])
#             fig_bal_dist.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=280, xaxis_title="Balance", yaxis_title="Count")
#             st.plotly_chart(fig_bal_dist, use_container_width=True)

#         with col2:
#             st.markdown("##### ⏳ Tenure & Loyalty Profile")
#             fig_loyalty = go.Figure(data=[go.Histogram(x=hv["Tenure"], nbinsx=10, marker_color="#ff7f0e")])
#             fig_loyalty.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=280, xaxis_title="Tenure", yaxis_title="Count")
#             st.plotly_chart(fig_loyalty, use_container_width=True)

#             st.markdown("##### 💎 CLV Distribution")
#             fig_clv_dist = go.Figure(data=[go.Histogram(x=hv["Estimated_CLV"], nbinsx=15, marker_color="#1f77b4")])
#             fig_clv_dist.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=280, xaxis_title="Estimated CLV", yaxis_title="Count")
#             st.plotly_chart(fig_clv_dist, use_container_width=True)

#     # -------------------------------------------------------------------------
#     # TAB 2: Engagement Cross-Analysis
#     # -------------------------------------------------------------------------
#     with tab2:
#         st.markdown("### Engagement Cross-Analysis Insights")
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.markdown("##### ⚡ Engagement Score Distribution")
#             fig_eng_dist = go.Figure(data=[go.Histogram(x=hv["engagement_score"], nbinsx=15, marker_color="#2ca02c")])
#             fig_eng_dist.update_layout(height=300, xaxis_title="Engagement Score", yaxis_title="Count")
#             st.plotly_chart(fig_eng_dist, use_container_width=True)

#             st.markdown("##### 📉 Balance vs. Engagement")
#             # FIXED: Nested colorbar title properly inside the colorbar dictionary property
#             fig_bal_eng = go.Figure(data=[go.Scatter(
#                 x=hv["engagement_score"], 
#                 y=hv["Balance"], 
#                 mode="markers",
#                 marker=dict(
#                     color=hv["NumOfProducts"], 
#                     colorscale="Viridis", 
#                     showscale=True, 
#                     colorbar=dict(title="Products")
#                 )
#             )])
#             if len(hv) > 1:
#                 m, b = np.polyfit(hv["engagement_score"], hv["Balance"], 1)
#                 fig_bal_eng.add_trace(go.Scatter(x=hv["engagement_score"], y=m*hv["engagement_score"]+b, mode="lines", name="OLS Trend", line=dict(color="red")))
#             fig_bal_eng.update_layout(height=320, xaxis_title="Engagement Score", yaxis_title="Balance", showlegend=False)
#             st.plotly_chart(fig_bal_eng, use_container_width=True)

#         with col2:
#             st.markdown("##### 💵 Balance by Engagement Level")
#             eng_lvl_col = "Engagement_Level" if "Engagement_Level" in hv.columns else "Engagement_Segment"
#             fig_box_eng = go.Figure()
#             for name, group in hv.groupby(eng_lvl_col):
#                 fig_box_eng.add_trace(go.Box(y=group["Balance"], name=str(name)))
#             fig_box_eng.update_layout(height=300, showlegend=False, yaxis_title="Balance")
#             st.plotly_chart(fig_box_eng, use_container_width=True)

#             st.markdown("##### 📈 CLV vs. Engagement")
#             fig_clv_eng = go.Figure()
#             active_col = "IsActiveMember" if "IsActiveMember" in hv.columns else "active_flag"
#             for name, group in hv.groupby(active_col):
#                 lbl = "Active" if name == 1 else "Inactive"
#                 fig_clv_eng.add_trace(go.Scatter(x=group["engagement_score"], y=group["Estimated_CLV"], mode="markers", name=lbl))
#             fig_clv_eng.update_layout(height=320, xaxis_title="Engagement Score", yaxis_title="Estimated CLV")
#             st.plotly_chart(fig_clv_eng, use_container_width=True)

#     # -------------------------------------------------------------------------
#     # TAB 3: Segment & Cluster Deep Dives
#     # -------------------------------------------------------------------------
#     with tab3:
#         st.markdown("### Behavioral Cluster Drilldowns")
#         cluster_col = "cluster_id" if "cluster_id" in hv.columns else "Cluster"

#         if cluster_col in hv.columns:
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.markdown("##### 📦 Cluster vs. Balance Dynamics")
#                 fig_clust_bal = go.Figure()
#                 for name, group in hv.groupby(cluster_col):
#                     fig_clust_bal.add_trace(go.Box(y=group["Balance"], name=f"Cluster {name}", boxpoints="all"))
#                 fig_clust_bal.update_layout(height=350, showlegend=False, yaxis_title="Balance")
#                 st.plotly_chart(fig_clust_bal, use_container_width=True)

#             with col2:
#                 st.markdown("##### ⚡ Cluster vs. Engagement Levels")
#                 fig_clust_eng = go.Figure()
#                 for name, group in hv.groupby(cluster_col):
#                     fig_clust_eng.add_trace(go.Box(y=group["engagement_score"], name=f"Cluster {name}", boxpoints="all"))
#                 fig_clust_eng.update_layout(height=350, showlegend=False, yaxis_title="Engagement Score")
#                 st.plotly_chart(fig_clust_eng, use_container_width=True)
#         else:
#             st.info("Cluster features are missing or altered in the underlying dataframe segment.")

#     # -------------------------------------------------------------------------
#     # TAB 4: Core Matrices & Correlations
#     # -------------------------------------------------------------------------
#     with tab4:
#         st.markdown("### Matrix Diagnostics")
#         st.markdown("##### 💸 Salary vs. Balance Ecosystem")

#         max_clv = hv["Estimated_CLV"].max() if hv["Estimated_CLV"].max() > 0 else 1
#         sizes = (hv["Estimated_CLV"] / max_clv) * 30 + 10

#         # FIXED: Nested colorbar title properly inside colorbar dictionary property
#         fig_financial = go.Figure(data=[go.Scatter(
#             x=hv["EstimatedSalary"],
#             y=hv["Balance"],
#             mode="markers",
#             marker=dict(
#                 size=sizes,
#                 color=hv["Estimated_CLV"],
#                 colorscale="Plasma",
#                 showscale=True,
#                 colorbar=dict(title="CLV")
#             ),
#             text=[f"ID: {cid}<br>Age: {age}<br>Tenure: {ten}" for cid, age, ten in zip(hv["CustomerId"], hv["Age"], hv["Tenure"])],
#             hoverinfo="text+x+y"
#         )])
#         fig_financial.update_layout(height=350, xaxis_title="Estimated Salary", yaxis_title="Balance")
#         st.plotly_chart(fig_financial, use_container_width=True)

#         st.markdown("---")
#         col1, col2 = st.columns(2)

#         with col1:
#             st.markdown("##### 🗺️ High-Value vs. Engagement Risk Matrix")
#             mid_clv = hv["Estimated_CLV"].median()
#             mid_eng = hv["engagement_score"].median()

#             fig_quad = go.Figure(data=[go.Scatter(
#                 x=hv["engagement_score"],
#                 y=hv["Estimated_CLV"],
#                 mode="markers",
#                 marker=dict(color=hv["Estimated_CLV"], colorscale="Turbo", showscale=True)
#             )])
#             fig_quad.add_shape(type="line", x0=mid_eng, y0=hv["Estimated_CLV"].min(), x1=mid_eng, y1=hv["Estimated_CLV"].max(), line=dict(color="red", dash="dash"))
#             fig_quad.add_shape(type="line", x0=hv["engagement_score"].min(), y0=mid_clv, x1=hv["engagement_score"].max(), y1=mid_clv, line=dict(color="red", dash="dash"))
#             fig_quad.update_layout(height=380, xaxis_title="Engagement Score", yaxis_title="Customer Lifetime Value (CLV)")
#             st.plotly_chart(fig_quad, use_container_width=True)

#         with col2:
#             st.markdown("##### 🌡️ Feature Correlation Heatmap")
#             core_corr_cols = ["Balance", "EstimatedSalary", "Estimated_CLV", "engagement_score", "Tenure", "NumOfProducts", "Age", "CreditScore"]
#             available_corr_cols = [c for c in core_corr_cols if c in hv.columns]

#             if len(available_corr_cols) > 1:
#                 corr_matrix = hv[available_corr_cols].corr().round(2)
#                 fig_corr = ff.create_annotated_heatmap(
#                     z=corr_matrix.values,
#                     x=list(corr_matrix.columns),
#                     y=list(corr_matrix.index),
#                     colorscale="RdBu",
#                     zmin=-1, zmax=1
#                 )
#                 fig_corr.update_layout(height=380, margin=dict(l=10, r=10, t=30, b=10))
#                 st.plotly_chart(fig_corr, use_container_width=True)
#             else:
#                 st.info("Insufficient quantitative variables for valid Correlation mapping.")

#     # -------------------------------------------------------------------------
#     # TAB 5: Churn & Risk Analytics
#     # -------------------------------------------------------------------------
#     with tab5:
#         st.markdown("### Churn & Retention Segmentation")
#         col1, col2 = st.columns(2)

#         with col1:
#             st.markdown("##### 📉 Churn by Balance Segment")
#             bal_cat = "Balance_Category" if "Balance_Category" in hv.columns else "high_balance_flag"
            
#             fig_bal_churn = go.Figure()
#             if bal_cat in hv.columns:
#                 for status, color in zip([0, 1], ["#2ca02c", "#d62728"]):
#                     lbl = "Retained" if status == 0 else "Churned"
#                     sub = hv[hv["Exited"] == status]
#                     counts = sub[bal_cat].value_counts(normalize=True) * 100
#                     fig_bal_churn.add_trace(go.Bar(x=counts.index, y=counts.values, name=lbl, marker_color=color))
#             fig_bal_churn.update_layout(height=300, barmode="group", yaxis_title="Percentage (%)")
#             st.plotly_chart(fig_bal_churn, use_container_width=True)

#         with col2:
#             st.markdown("##### 💳 Churn by Credit Score Band")
#             hv_copy = hv.copy()
#             hv_copy["CreditScore_Band"] = pd.cut(
#                 hv_copy["CreditScore"],
#                 bins=[0, 579, 669, 739, 799, 850],
#                 labels=["Poor", "Fair", "Good", "Very Good", "Exceptional"]
#             )
#             fig_cs_churn = go.Figure()
#             for status, color in zip([0, 1], ["#2ca02c", "#d62728"]):
#                 lbl = "Retained" if status == 0 else "Churned"
#                 sub = hv_copy[hv_copy["Exited"] == status]
#                 counts = sub["CreditScore_Band"].value_counts(normalize=True) * 100
#                 fig_cs_churn.add_trace(go.Bar(x=counts.index, y=counts.values, name=lbl, marker_color=color))
#             fig_cs_churn.update_layout(height=300, barmode="group", yaxis_title="Percentage (%)")
#             st.plotly_chart(fig_cs_churn, use_container_width=True)

#         st.markdown("---")
#         col3, col4 = st.columns(2)

#         with col3:
#             st.markdown("##### 📦 Churn by Products Held")
#             fig_prod_churn = go.Figure()
#             for status, color in zip([0, 1], ["#2ca02c", "#d62728"]):
#                 lbl = "Retained" if status == 0 else "Churned"
#                 sub = hv[hv["Exited"] == status]
#                 counts = sub["NumOfProducts"].value_counts(normalize=True) * 100
#                 fig_prod_churn.add_trace(go.Bar(x=counts.index, y=counts.values, name=lbl, marker_color=color))
#             fig_prod_churn.update_layout(height=300, barmode="stack", yaxis_title="Percentage (%)")
#             st.plotly_chart(fig_prod_churn, use_container_width=True)

#         with col4:
#             st.markdown("##### 💵 Average Balance: Retained vs. Churned")
#             avg_bal = hv.groupby("Exited")["Balance"].mean()
#             fig_avg_bal = go.Figure(data=[go.Bar(
#                 x=["Retained Base", "Churned Base"],
#                 y=[avg_bal.get(0, 0), avg_bal.get(1, 0)],
#                 marker_color=["#1f77b4", "#ff7f0e"]
#             )])
#             fig_avg_bal.update_layout(height=300, yaxis_title="Average Balance ($)")
#             st.plotly_chart(fig_avg_bal, use_container_width=True)

#     # -------------------------------------------------------------------------
#     # TAB 6: Geo-Demographic & Top-N Risk
#     # -------------------------------------------------------------------------
#     with tab6:
#         st.markdown("### Geographic Real-Estate & High-Value Risks")

#         hv_geo = hv.copy()
#         if "Geography_Germany" in hv_geo.columns and "Geography_Spain" in hv_geo.columns:
#             hv_geo["Geography"] = np.select(
#                 [hv_geo["Geography_Germany"] == 1, hv_geo["Geography_Spain"] == 1],
#                 ["Germany", "Spain"], default="France"
#             )
#         else:
#             hv_geo["Geography"] = "Unknown Base"

#         col1, col2 = st.columns(2)

#         with col1:
#             st.markdown("##### 🌐 High-Value vs. Standard Churn by Geography")
#             df_total_geo = df.copy()
#             if "Geography_Germany" in df_total_geo.columns and "Geography_Spain" in df_total_geo.columns:
#                 df_total_geo["Geography"] = np.select(
#                     [df_total_geo["Geography_Germany"] == 1, df_total_geo["Geography_Spain"] == 1],
#                     ["Germany", "Spain"], default="France"
#                 )
#             else:
#                 df_total_geo["Geography"] = "Unknown Base"

#             std_geo_rates = df_total_geo.groupby("Geography")["Exited"].mean() * 100
#             hv_geo_rates = hv_geo.groupby("Geography")["Exited"].mean() * 100

#             fig_geo_comp = go.Figure(data=[
#                 go.Bar(x=std_geo_rates.index, y=std_geo_rates.values, name="Standard Cohort", marker_color="#8da0cb"),
#                 go.Bar(x=hv_geo_rates.index, y=hv_geo_rates.values, name="High-Value Segment", marker_color="#fc8d62")
#             ])
#             fig_geo_comp.update_layout(height=320, barmode="group", yaxis_title="Churn Rate (%)")
#             st.plotly_chart(fig_geo_comp, use_container_width=True)

#         with col2:
#             st.markdown("##### ⚥ High-Value Balance at Risk: Country & Gender")
#             hv_geo["Gender"] = np.where(hv_geo["Gender_Male"] == 1, "Male", "Female")
            
#             fig_geo_gender = go.Figure()
#             for gender, color in zip(["Male", "Female"], ["#17becf", "#e377c2"]):
#                 sub = hv_geo[hv_geo["Gender"] == gender]
#                 geo_sums = sub.groupby("Geography")["Balance"].sum()
#                 fig_geo_gender.add_trace(go.Bar(x=geo_sums.index, y=geo_sums.values, name=gender, marker_color=color))
            
#             fig_geo_gender.update_layout(height=320, barmode="stack", yaxis_title="Total Balance Exposure ($)")
#             st.plotly_chart(fig_geo_gender, use_container_width=True)

#         st.markdown("---")

#         st.markdown("##### 🚨 Churned High-Value Customer Registry")
#         churned_hv = hv_geo[hv_geo["Exited"] == 1]

#         if not churned_hv.empty:
#             max_limit = min(len(churned_hv), 100)
#             top_n = st.slider(
#                 "Filter Registry Focus Depth (Top N Rows)",
#                 min_value=5,
#                 max_value=max_limit if max_limit > 5 else 10,
#                 value=9,
#                 step=1,
#             )

#             display_cols = ["CustomerId", "Surname", "Geography", "Gender", "Age", "Balance", "EstimatedSalary", "Estimated_CLV", "engagement_score", "NumOfProducts"]
#             available_display = [c for c in display_cols if c in churned_hv.columns]

#             churned_sorted = churned_hv.sort_values(
#                 by=["Balance", "engagement_score"], ascending=[False, True]
#             )[available_display].head(top_n)

#             st.dataframe(
#                 churned_sorted.style.format(
#                     {
#                         "Balance": "${:,.2f}",
#                         "EstimatedSalary": "${:,.2f}",
#                         "Estimated_CLV": "${:,.2f}",
#                         "engagement_score": "{:.2f}%",
#                     }
#                 ),
#                 use_container_width=True,
#             )
#         else:
#             st.success("Excellent! Zero High-Value customers matching criteria have churned.")


# def colorscale_to_list(scale_name, num_colors):
#     """Helper function to fetch sequential layout colors from built-in maps safely."""
#     import plotly.colors as colors
#     try:
#         scale = getattr(colors.sequential, scale_name)
#         return colors.sample_colorscale(scale, num_colors)
#     except AttributeError:
#         return ["#1f77b4"] * num_colors

import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import streamlit as st


def render_high_value_detector(df, filters):
    st.subheader("🎯 High-Value Disengaged Customer Analytics Dashboard")

    # -------------------------------------------------------------------------
    # 1. Dataset Preprocessing & Segmentation Triggers
    # -------------------------------------------------------------------------
    # Create copies to safely introduce localized display groups
    # -------------------------------------------------------------------------
    # 1. Dataset Preprocessing & Segmentation Triggers (FIXED)
    # -------------------------------------------------------------------------
    df_clean = df.copy()
    
    # Reverse engineer Geography from one-hot flags if necessary
    if "Geography" not in df_clean.columns:
        if "Geography_Germany" in df_clean.columns and "Geography_Spain" in df_clean.columns:
            df_clean["Geography"] = np.select(
                [df_clean["Geography_Germany"] == 1, df_clean["Geography_Spain"] == 1],
                ["Germany", "Spain"], default="France"
            )
        else:
            df_clean["Geography"] = "France"

    if "Gender" not in df_clean.columns:
        df_clean["Gender"] = np.where(df_clean["Gender_Male"] == 1, "Male", "Female")

    # Dynamic Quantile Binning for Credit Score (High, Medium, Low)
    df_clean["CreditScore_Band"] = pd.qcut(
        df_clean["CreditScore"], q=3, labels=["Low", "Medium", "High"]
    )

    # SAFELY BIN BALANCE BY ISOLATING ZERO-BALANCES FIRST
    df_clean["Balance_Band"] = "Low"  # Default fallback state
    
    positive_balance_mask = df_clean["Balance"] > 0
    positive_balances = df_clean.loc[positive_balance_mask, "Balance"]

    if not positive_balances.empty:
        # Determine how many unique non-zero values exist
        unique_vals = positive_balances.nunique()
        
        if unique_vals >= 3:
            # Safe to split into Low, Medium, High among funded accounts
            df_clean.loc[positive_balance_mask, "Balance_Band"] = pd.qcut(
                positive_balances, q=3, labels=["Low", "Medium", "High"]
            )
        elif unique_vals == 2:
            # Fallback if there are only 2 unique positive values
            df_clean.loc[positive_balance_mask, "Balance_Band"] = pd.qcut(
                positive_balances, q=2, labels=["Medium", "High"]
            )
        else:
            # If everyone left has the exact same positive balance
            df_clean.loc[positive_balance_mask, "Balance_Band"] = "High"

    # 2. Extract High-Value Disengaged Target Cohort (hv)
    hv = df_clean[
        (df_clean["Balance"] >= filters["BalanceThreshold"])
        & (df_clean["EstimatedSalary"] >= filters["SalaryThreshold"])
        & ((df_clean["low_engagement_flag"] == 1) | (df_clean["is_dormant_high_value"] == 1))
    ].copy()

    if hv.empty:
        st.warning(
            "No customers match the current High-Value Disengaged criteria. Adjust filters to populate charts."
        )
        return

    # 3. Executive Summary Matrix Indicators
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("At-Risk Customers", f"{len(hv):,}")
    c2.metric("Avg Balance", f"${hv['Balance'].mean():,.0f}")
    c3.metric("Avg CLV", f"${hv['Estimated_CLV'].mean():,.0f}")
    c4.metric("Avg Engagement", f"{hv['engagement_score'].mean() * 100:.2f}%")

    st.markdown("---")

    # 4. Master Layout Tabs Configuration
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📊 Financial & Engagement Core",
            "🧩 Behavioral Risk & Clustering",
            "🚨 Churn Dynamics (Low/Med/High)",
            "🌍 Geo-Demographics & Registry Tracker",
        ]
    )

    # -------------------------------------------------------------------------
    # TAB 1: Core Profiles & Distributions
    # -------------------------------------------------------------------------
    with tab1:
        st.markdown("### Financial & Engagement Foundations")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### 📦 Product Mix Allocation")
            prod_col = "Product_Group" if "Product_Group" in hv.columns else "NumOfProducts"
            prod_counts = hv[prod_col].value_counts()
            fig_prod = go.Figure(data=[go.Pie(
                labels=prod_counts.index, values=prod_counts.values, hole=0.4,
                marker=dict(colors=colorscale_to_list("YlOrRd_r", len(prod_counts)))
            )])
            fig_prod.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=260)
            st.plotly_chart(fig_prod, use_container_width=True)

            st.markdown("##### 💰 Capital Balance Spread")
            fig_bal_dist = go.Figure(data=[go.Histogram(x=hv["Balance"], nbinsx=15, marker_color="#e65c00")])
            fig_bal_dist.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=260, xaxis_title="Balance ($)", yaxis_title="Count")
            st.plotly_chart(fig_bal_dist, use_container_width=True)

        with col2:
            st.markdown("##### ⚡ Engagement Score Distribution")
            fig_eng_dist = go.Figure(data=[go.Histogram(x=hv["engagement_score"], nbinsx=15, marker_color="#2ca02c")])
            fig_eng_dist.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=260, xaxis_title="Engagement Score", yaxis_title="Count")
            st.plotly_chart(fig_eng_dist, use_container_width=True)

            st.markdown("##### 📈 CLV Vector Mapping")
            fig_clv_dist = go.Figure(data=[go.Histogram(x=hv["Estimated_CLV"], nbinsx=15, marker_color="#1f77b4")])
            fig_clv_dist.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=260, xaxis_title="Estimated CLV ($)", yaxis_title="Count")
            st.plotly_chart(fig_clv_dist, use_container_width=True)

    # -------------------------------------------------------------------------
    # TAB 2: Behavioral Risk & Clustering Matrix
    # -------------------------------------------------------------------------
    with tab2:
        st.markdown("### Behavioral Variance Deep Dives")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### 📉 Balance Asset Correlation Vectors")
            fig_bal_eng = go.Figure(data=[go.Scatter(
                x=hv["engagement_score"], y=hv["Balance"], mode="markers",
                marker=dict(color=hv["NumOfProducts"], colorscale="Viridis", showscale=True, colorbar=dict(title="Products"))
            )])
            if len(hv) > 1:
                m, b = np.polyfit(hv["engagement_score"], hv["Balance"], 1)
                fig_bal_eng.add_trace(go.Scatter(x=hv["engagement_score"], y=m*hv["engagement_score"]+b, mode="lines", name="OLS Trend", line=dict(color="red")))
            fig_bal_eng.update_layout(height=320, xaxis_title="Engagement Score", yaxis_title="Balance ($)", showlegend=False)
            st.plotly_chart(fig_bal_eng, use_container_width=True)

        with col2:
            st.markdown("##### 🗺️ High-Value vs. Engagement Risk Quadrants")
            mid_clv = hv["Estimated_CLV"].median()
            mid_eng = hv["engagement_score"].median()
            fig_quad = go.Figure(data=[go.Scatter(
                x=hv["engagement_score"], y=hv["Estimated_CLV"], mode="markers",
                marker=dict(color=hv["Estimated_CLV"], colorscale="Turbo", showscale=True)
            )])
            fig_quad.add_shape(type="line", x0=mid_eng, y0=hv["Estimated_CLV"].min(), x1=mid_eng, y1=hv["Estimated_CLV"].max(), line=dict(color="red", dash="dash"))
            fig_quad.add_shape(type="line", x0=hv["engagement_score"].min(), y0=mid_clv, x1=hv["engagement_score"].max(), y1=mid_clv, line=dict(color="red", dash="dash"))
            fig_quad.update_layout(height=320, xaxis_title="Engagement Score", yaxis_title="CLV ($)")
            st.plotly_chart(fig_quad, use_container_width=True)

        st.markdown("---")
        st.markdown("##### 🌡️ Latent Feature Correlation Network")
        core_corr_cols = ["Balance", "EstimatedSalary", "Estimated_CLV", "engagement_score", "Tenure", "NumOfProducts", "Age", "CreditScore"]
        available_corr_cols = [c for c in core_corr_cols if c in hv.columns]
        if len(available_corr_cols) > 1:
            corr_matrix = hv[available_corr_cols].corr().round(2)
            fig_corr = ff.create_annotated_heatmap(
                z=corr_matrix.values, x=list(corr_matrix.columns), y=list(corr_matrix.index),
                colorscale="RdBu", zmin=-1, zmax=1
            )
            fig_corr.update_layout(height=340, margin=dict(l=10, r=10, t=30, b=10))
            st.plotly_chart(fig_corr, use_container_width=True)

    # -------------------------------------------------------------------------
    # TAB 3: Churn Dynamics (Low / Medium / High Matrix)
    # -------------------------------------------------------------------------
    with tab3:
        st.markdown("### Churn Segmentation Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### 📉 Churn Density by Balance Segment (Low / Med / High)")
            fig_bal_churn = go.Figure()
            # Grouping by the dynamically calculated high/medium/low balance bands
            for status, color in zip([0, 1], ["#2ca02c", "#d62728"]):
                lbl = "Retained" if status == 0 else "Churned"
                subset = hv[hv["Exited"] == status]
                # Maintain order consistency across standard category indexes
                counts = subset["Balance_Band"].value_counts(normalize=True).reindex(["Low", "Medium", "High"]).fillna(0) * 100
                fig_bal_churn.add_trace(go.Bar(x=counts.index, y=counts.values, name=lbl, marker_color=color))
            fig_bal_churn.update_layout(height=300, barmode="group", xaxis_title="Balance Band", yaxis_title="Segment Composition (%)")
            st.plotly_chart(fig_bal_churn, use_container_width=True)

        with col2:
            st.markdown("##### 💳 Churn Density by Credit Score Band (Low / Med / High)")
            fig_cs_churn = go.Figure()
            # Grouping by the dynamically calculated high/medium/low credit score bands
            for status, color in zip([0, 1], ["#2ca02c", "#d62728"]):
                lbl = "Retained" if status == 0 else "Churned"
                subset = hv[hv["Exited"] == status]
                counts = subset["CreditScore_Band"].value_counts(normalize=True).reindex(["Low", "Medium", "High"]).fillna(0) * 100
                fig_cs_churn.add_trace(go.Bar(x=counts.index, y=counts.values, name=lbl, marker_color=color))
            fig_cs_churn.update_layout(height=300, barmode="group", xaxis_title="Credit Score Band", yaxis_title="Segment Composition (%)")
            st.plotly_chart(fig_cs_churn, use_container_width=True)

        st.markdown("---")
        col3, col4 = st.columns(2)

        with col3:
            st.markdown("##### 📦 Churn Attrition by Products Held")
            fig_prod_churn = go.Figure()
            for status, color in zip([0, 1], ["#2ca02c", "#d62728"]):
                lbl = "Retained" if status == 0 else "Churned"
                subset = hv[hv["Exited"] == status]
                counts = subset["NumOfProducts"].value_counts(normalize=True).sort_index().fillna(0) * 100
                fig_prod_churn.add_trace(go.Bar(x=counts.index, y=counts.values, name=lbl, marker_color=color))
            fig_prod_churn.update_layout(height=300, barmode="stack", xaxis_title="Number of Products", yaxis_title="Composition (%)")
            st.plotly_chart(fig_prod_churn, use_container_width=True)

        with col4:
            st.markdown("##### 💵 Capital Exposure: Retained vs. Churned")
            avg_bal = hv.groupby("Exited")["Balance"].mean()
            fig_avg_bal = go.Figure(data=[go.Bar(
                x=["Retained High Value", "Churned High Value"],
                y=[avg_bal.get(0, 0), avg_bal.get(1, 0)],
                marker_color=["#1f77b4", "#ff7f0e"]
            )])
            fig_avg_bal.update_layout(height=300, yaxis_title="Average Capital Portfolio ($)")
            st.plotly_chart(fig_avg_bal, use_container_width=True)

    # -------------------------------------------------------------------------
    # TAB 4: Geo-Demographics & Registry Tracker
    # -------------------------------------------------------------------------
    with tab4:
        st.markdown("### Geographic Real Estate Frameworks")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### 🌐 Baseline Cohort vs. High-Value Churn by Territory")
            # Calculate aggregate territorial attrition rates
            std_geo_rates = df_clean.groupby("Geography")["Exited"].mean() * 100
            hv_geo_rates = hv.groupby("Geography")["Exited"].mean() * 100
            
            # Align indices perfectly to handle empty/missing regions gracefully
            all_regions = sorted(list(set(df_clean["Geography"].unique()).union(set(hv["Geography"].unique()))))
            std_geo_rates = std_geo_rates.reindex(all_regions).fillna(0)
            hv_geo_rates = hv_geo_rates.reindex(all_regions).fillna(0)

            fig_geo_comp = go.Figure(data=[
                go.Bar(x=std_geo_rates.index, y=std_geo_rates.values, name="Standard Base Cohort", marker_color="#8da0cb"),
                go.Bar(x=hv_geo_rates.index, y=hv_geo_rates.values, name="High-Value At-Risk Segment", marker_color="#fc8d62")
            ])
            fig_geo_comp.update_layout(height=320, barmode="group", xaxis_title="Geography", yaxis_title="Observed Churn Rate (%)")
            st.plotly_chart(fig_geo_comp, use_container_width=True)

        with col2:
            st.markdown("##### ⚥ High-Value Asset Capital at Risk: Territory & Gender")
            fig_geo_gender = go.Figure()
            # Isolate total continuous balance capital locked across geographic segments
            for gender, color in zip(["Male", "Female"], ["#17becf", "#e377c2"]):
                sub = hv[hv["Gender"] == gender]
                geo_sums = sub.groupby("Geography")["Balance"].sum().reindex(all_regions).fillna(0)
                fig_geo_gender.add_trace(go.Bar(x=geo_sums.index, y=geo_sums.values, name=gender, marker_color=color))
            
            fig_geo_gender.update_layout(height=320, barmode="stack", xaxis_title="Geography", yaxis_title="Total Bal Exposure ($)")
            st.plotly_chart(fig_geo_gender, use_container_width=True)

        st.markdown("---")

        # -------------------------------------------------------------------------
        # High-Value Churned Details Ledger Block
        # -------------------------------------------------------------------------
        st.markdown("##### 🚨 At-Risk Registry Ledger: Churned High-Value Targets")
        churned_hv = hv[hv["Exited"] == 1]

        if not churned_hv.empty:
            max_limit = min(len(churned_hv), 100)
            
            # Integrated top-N slider controls mapping to target requirements
            top_n = st.slider(
                "Filter Ledger Display Target Frame Depth (Top N Rows)",
                min_value=5, max_value=max_limit if max_limit > 5 else 10, value=9, step=1
            )

            display_cols = [
                "CustomerId", "Surname", "Geography", "Gender", "Age", 
                "Balance", "EstimatedSalary", "Estimated_CLV", "engagement_score", "NumOfProducts"
            ]
            available_display = [c for c in display_cols if c in churned_hv.columns]

            # Prioritize target priority ranking by asset magnitude & drop-off intensity
            churned_sorted = churned_hv.sort_values(
                by=["Balance", "engagement_score"], ascending=[False, True]
            )[available_display].head(top_n)

            st.dataframe(
                churned_sorted.style.format(
                    {
                        "Balance": "${:,.2f}",
                        "EstimatedSalary": "${:,.2f}",
                        "Estimated_CLV": "${:,.2f}",
                        "engagement_score": "{:.2f}%",
                    }
                ),
                use_container_width=True,
            )
        else:
            st.success("Exemplary Risk Score Profile! Zero High-Value customers matching current boundaries have churned.")


def colorscale_to_list(scale_name, num_colors):
    """Retrieves standard hex arrays smoothly out of categorical strings without calling px."""
    import plotly.colors as colors
    try:
        scale = getattr(colors.sequential, scale_name)
        return colors.sample_colorscale(scale, num_colors)
    except AttributeError:
        return ["#1f77b4"] * num_colors