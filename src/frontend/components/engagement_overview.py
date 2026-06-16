import plotly.figure_factory as ff

import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

def render_engagement_overview(df):
    # Fix import typo implicitly and provide dashboard heading
    st.subheader("📊 Engagement vs Churn Analysis")
    
    # -------------------------------------------------------------------------
    # 1. Key Metrics Ribbon
    # -------------------------------------------------------------------------
    c1, c2, c3, c4 = st.columns(4)
    
    total_customers = len(df)
    churn_rate = df["Exited"].mean() * 100 if total_customers > 0 else 0
    avg_engagement = df["engagement_score"].mean() if total_customers > 0 else 0
    active_pct = df["IsActiveMember"].mean() * 100 if total_customers > 0 else 0

    with c1:
        st.metric(label="👥 Total Customers", value=f"{total_customers:,}")
    with c2:
        st.metric(label="📉 Churn Rate", value=f"{churn_rate:.2f}%")
    with c3:
        st.metric(label="⚡ Avg Engagement Score", value=f"{avg_engagement:.2f}")
    with c4:
        st.metric(label="🟢 Active Members", value=f"{active_pct:.1f}%")
        
    st.markdown("---")

    # Mapping Exited to string for explicit categorical legend colors across plots
    plot_df = df.copy()
    plot_df["Status"] = plot_df["Exited"].map({1: "Churned", 0: "Retained"})

    # -------------------------------------------------------------------------
    # 2. Side-by-Side Analysis (Distributions)
    # -------------------------------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        fig_hist = px.histogram(
            plot_df,
            x="engagement_score",
            color="Status",
            marginal="rug",
            barmode="overlay",
            title="<b>Engagement Score Distribution by Status</b>",
            color_discrete_map={"Churned": "#EF553B", "Retained": "#636EFA"},
            labels={"engagement_score": "Engagement Score", "Status": "Customer Status"}
        )
        fig_hist.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(200,200,200,0.2)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        fig_box = px.box(
            plot_df,
            x="Status",
            y="engagement_score",
            color="Status",
            points="outliers",
            title="<b>Engagement Variations across Churn States</b>",
            color_discrete_map={"Churned": "#EF553B", "Retained": "#636EFA"},
            labels={"engagement_score": "Engagement Score", "Status": "Customer Status"}
        )
        fig_box.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(showgrid=True, gridcolor="rgba(200,200,200,0.2)"),
            showlegend=False
        )
        st.plotly_chart(fig_box, use_container_width=True)

    # -------------------------------------------------------------------------
    # 3. Categorical Segments vs Churn Risk
    # -------------------------------------------------------------------------
    col3, col4 = st.columns(2)

    with col3:
        churn_by_segment = (
            plot_df.groupby("Engagement_Segment")["Exited"]
            .mean()
            .reset_index()
            .sort_values(by="Exited", ascending=False)
        )
        churn_by_segment["Churn Rate (%)"] = churn_by_segment["Exited"] * 100

        fig_seg = px.bar(
            churn_by_segment,
            x="Engagement_Segment",
            y="Churn Rate (%)",
            title="<b>Churn Rate by Engagement Segment</b>",
            color="Churn Rate (%)",
            color_continuous_scale=px.colors.sequential.Reds,
            labels={"Engagement_Segment": "Engagement Segment"}
        )
        fig_seg.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(showgrid=True, gridcolor="rgba(200,200,200,0.2)"),
            coloraxis_showscale=False,
            xaxis_tickangle=-15
        )
        st.plotly_chart(fig_seg, use_container_width=True)

    with col4:
        churn_by_risk = (
            plot_df.groupby("Strategic_Risk_Segment")["Exited"]
            .mean()
            .reset_index()
            .sort_values(by="Exited", ascending=False)
        )
        churn_by_risk["Churn Rate (%)"] = churn_by_risk["Exited"] * 100

        fig_risk = px.bar(
            churn_by_risk,
            x="Strategic_Risk_Segment",
            y="Churn Rate (%)",
            title="<b>Churn Rate by Strategic Risk Segment</b>",
            color="Churn Rate (%)",
            color_continuous_scale=px.colors.sequential.OrRd,
            labels={"Strategic_Risk_Segment": "Strategic Risk Segment"}
        )
        fig_risk.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(showgrid=True, gridcolor="rgba(200,200,200,0.2)"),
            coloraxis_showscale=False,
            xaxis_tickangle=-15
        )
        st.plotly_chart(fig_risk, use_container_width=True)

    # -------------------------------------------------------------------------
    # NEW INSERTIONS FROM PART 2 & PART 3 (Converted seamlessly to Plotly)
    # -------------------------------------------------------------------------
    st.markdown("---")
    st.markdown("### 📈 Deep-Dive Behavioral Profiles & Matrix Segmentations")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        # Plot A: Distribution of Engineered Engagement Segments (Barplot)
        segment_counts = plot_df["Engagement_Segment"].value_counts(normalize=True).reset_index()
        segment_counts.columns = ["Engagement_Segment", "Percentage"]
        segment_counts["Percentage"] *= 100
        
        fig_a = px.bar(
            segment_counts,
            x="Engagement_Segment",
            y="Percentage",
            title="<b>Distribution of Isolated 5-Cluster Engagement Segments</b>",
            color="Percentage",
            color_continuous_scale=px.colors.sequential.Viridis,
            labels={"Engagement_Segment": "Segment Designation", "Percentage": "Percentage of Base (%)"}
        )
        fig_a.update_layout(plot_bgcolor="rgba(0,0,0,0)", coloraxis_showscale=False, xaxis_tickangle=-15)
        st.plotly_chart(fig_a, use_container_width=True)

    with col_b:
        # Plot C1: Engagement Score Bimodal Resolution (Stacked Histogram)
        fig_c1 = px.histogram(
            plot_df,
            x="engagement_score",
            color="Engagement_Segment",
            barmode="stack",
            title="<b>Engagement Score Bimodal Resolution (5 Clusters)</b>",
            color_discrete_sequence=px.colors.qualitative.G10,
            labels={"engagement_score": "Engagement Score"}
        )
        # Replicating the target threshold marker line via shapes
        fig_c1.add_shape(
            type="line", x0=0.55, y0=0, x1=0.55, y1=1, yref="paper",
            line=dict(color="Red", width=2, dash="dash")
        )
        fig_c1.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_c1, use_container_width=True)

    col_c, col_d = st.columns(2)
    
    with col_c:
        # Plot C2: Upgraded Strategic Value Segments vs Churn Status (Grouped Countplot)
        # Ensuring categorical chronological ordering
        val_order = ["Platinum Value", "High Value", "Medium Value", "Low Value"]
        val_order = [v for v in val_order if v in plot_df["customer_value_segment"].unique()]
        
        fig_c2 = px.histogram(
            plot_df,
            x="customer_value_segment",
            color="Status",
            barmode="group",
            category_orders={"customer_value_segment": val_order},
            title="<b>Upgraded Strategic Value Segments vs Churn Status</b>",
            color_discrete_map={"Churned": "#EF553B", "Retained": "#636EFA"},
            labels={"customer_value_segment": "Customer Value Segment"}
        )
        fig_c2.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_c2, use_container_width=True)

    with col_d:
        # Phase 2: Commitment Score vs Engagement Score Scatter Metric Map
        # Enforcing data sample safety boundaries for responsive frame rates
        scatter_sample = plot_df.sample(n=min(3000, len(plot_df)), random_state=42)
        fig_scat2 = px.scatter(
            scatter_sample,
            x="Financial_Commitment_Score",
            y="engagement_score",
            color="Commitment_Engagement_Segment",
            title="<b>Commitment Score vs Engagement Score</b> (Sampled)",
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={"Financial_Commitment_Score": "Financial Commitment Score", "engagement_score": "Engagement Score"}
        )
        fig_scat2.update_layout(plot_bgcolor="rgba(245,245,245,0.3)")
        st.plotly_chart(fig_scat2, use_container_width=True)

    st.markdown("---")
    st.markdown("### 🧮 Matrix Frameworks & Risk Mapping Indicators")

    col_e, col_f = st.columns(2)

    with col_e:
        # Phase 2 Heatmap Matrix: Churn Rate Heatmap (Commitment x Engagement)
        matrix_pivot = plot_df.groupby(["Commitment_Category", "Engagement_Category"])["Exited"].mean().reset_index()
        matrix_pivot["Churn Rate"] = matrix_pivot["Exited"] * 100
        
        # Mapping to pivot structure dynamically for categorical heat matrices
        fig_heat1 = px.density_heatmap(
            matrix_pivot,
            x="Engagement_Category",
            y="Commitment_Category",
            z="Churn Rate",
            histfunc="sum",
            text_auto=".1f",
            title="<b>Churn Rate Heatmap (Commitment x Engagement %)</b>",
            color_continuous_scale="YlOrRd"
        )
        st.plotly_chart(fig_heat1, use_container_width=True)

    with col_f:
        # Phase 4 Mismatch Scatter: Salary vs Balance Cross Space Analysis
        fig_mis = px.scatter(
            scatter_sample,
            x="EstimatedSalary",
            y="Balance",
            color="Mismatch_Category",
            title="<b>Salary vs Balance Cross Space Analysis</b>",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            labels={"EstimatedSalary": "Estimated Salary", "Balance": "Account Balance"}
        )
        fig_mis.update_layout(plot_bgcolor="rgba(245,245,245,0.3)", legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig_mis, use_container_width=True)

    col_g, col_h = st.columns(2)

    with col_g:
        # Phase 5 Heatmap Visual: Distribution Share - Balance Category vs Activity Group
        activity_cross = plot_df.groupby(["Balance_Category", "Activity_Group"], observed=False).size().reset_index(name="Counts")
        # Normalize columns manually to simulate crosstab parameters
        total_per_group = activity_cross.groupby("Activity_Group")["Counts"].transform("sum")
        activity_cross["Share (%)"] = (activity_cross["Counts"] / total_per_group) * 100

        fig_heat2 = px.density_heatmap(
            activity_cross,
            x="Activity_Group",
            y="Balance_Category",
            z="Share (%)",
            histfunc="sum",
            text_auto=".1f",
            title="<b>Distribution Share: Balance Category vs Activity Group (%)</b>",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig_heat2, use_container_width=True)

    with col_h:
        # Phase 8: Premium Risk Visualizations (Validated Churn Conversion)
        # Safely computing validation frames dynamically
        premium_df = plot_df[plot_df["Premium_Risk_Group"] != "Standard Portfolio"]
        if len(premium_df) > 0:
            premium_summary = premium_df.groupby("Premium_Risk_Group")["Exited"].mean().reset_index()
            premium_summary["Churn Percentage (%)"] = premium_summary["Exited"] * 100
            premium_summary = premium_summary.sort_values(by="Churn Percentage (%)", ascending=False)
            
            fig_prem = px.bar(
                premium_summary,
                x="Premium_Risk_Group",
                y="Churn Percentage (%)",
                title="<b>Validated Churn Conversion across Premium Sub-Groups</b>",
                color="Churn Percentage (%)",
                color_continuous_scale=px.colors.sequential.Reds_r,
                labels={"Premium_Risk_Group": "Premium Risk Sub-Tier"}
            )
            fig_prem.update_layout(plot_bgcolor="rgba(0,0,0,0)", coloraxis_showscale=False, xaxis_tickangle=-10)
            st.plotly_chart(fig_prem, use_container_width=True)
        else:
            st.info("No premium segment exceptions filtered in current portfolio context.")

    # -------------------------------------------------------------------------
    # 4. Multi-Dimensional Portfolio Strategy DNA Heatmap
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # 4. Multi-Dimensional Portfolio Strategy DNA Heatmap
    # -------------------------------------------------------------------------
    st.markdown("### 🧬 Cluster Strategic DNA Profile Matrix")
    
    # Check if cluster_id exists in the dataframe before proceeding
    if "cluster_id" in plot_df.columns:
        import plotly.figure_factory as ff

        # --- STEP 1: CALCULATE CLUSTER PROFILES (The Missing Link) ---
        cluster_profiles = (
            plot_df.groupby("cluster_id")
            .agg(
                Avg_Balance=("Balance", "mean"),
                Avg_Engagement=("engagement_score", "mean"),
                Churn_Rate=("Exited", "mean"),
                Loyalty_Ratio=("Loyalty_Ratio", "mean")
            )
            .reset_index()
        )

        # --- STEP 2: DYNAMIC STRATEGIC LABELING ---
        def assign_cluster_label(row):
            if row["Churn_Rate"] > 0.25:
                return f"Cluster {int(row['cluster_id'])}: Churn-Prone"
            elif row["Avg_Balance"] > plot_df["Balance"].median() and row["Avg_Engagement"] > 50:
                return f"Cluster {int(row['cluster_id'])}: Loyal Premium"
            elif row["Avg_Balance"] > plot_df["Balance"].median() and row["Avg_Engagement"] <= 50:
                return f"Cluster {int(row['cluster_id'])}: Dormant Wealth"
            elif row["Avg_Engagement"] > 60:
                return f"Cluster {int(row['cluster_id'])}: Active Growth"
            else:
                return f"Cluster {int(row['cluster_id'])}: Low Value Retail"

        cluster_profiles["Strategic_Label"] = cluster_profiles.apply(assign_cluster_label, axis=1)
        
        # --- STEP 3: PREPARE MATRICES FOR THE HEATMAP ---
        metrics = ["Avg_Balance", "Avg_Engagement", "Churn_Rate", "Loyalty_Ratio"]
        hm_data = cluster_profiles.set_index("Strategic_Label")[metrics]
        
        # Scale variables between [0, 1] for visual calibration consistency
        hm_norm = (hm_data - hm_data.min()) / (hm_data.max() - hm_data.min())
        
        # Extract underlying array values for the figure factory canvas
        z_colors = hm_norm.values                     # Color intensity map
        annotation_text = hm_data.round(2).astype(str).values  # Real numeric text overlay
        x_labels = list(hm_data.columns)               # Metric titles
        y_labels = list(hm_data.index)                 # Generated cluster labels

        # --- STEP 4: GENERATE THE ANNOTATED HEATMAP ---
        fig_dna = ff.create_annotated_heatmap(
            z=z_colors,
            x=x_labels,
            y=y_labels,
            annotation_text=annotation_text,
            colorscale="YlGnBu"
        )
        
        fig_dna.update_layout(
            title="<b>Cluster Strategic DNA Profiling Matrix (Normalized Colors vs Real Data)</b>",
            xaxis_title="Core DNA Dimension",
            yaxis_title="Strategic Behavioral Cluster"
        )
        
        st.plotly_chart(fig_dna, use_container_width=True)
        
    else:
        st.warning("⚠️ The column 'cluster_id' was not found in the provided DataFrame. Ensure Phase 9 calculations run upstream.")