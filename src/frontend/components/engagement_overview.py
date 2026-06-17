# 

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st

def render_engagement_overview(df):
    # Establish local clean working copy to avoid mutation side effects
    plot_df = df.copy()
    plot_df["Status"] = plot_df["Exited"].map({1: "Churned", 0: "Retained"})

    # -------------------------------------------------------------------------
    # DATA RECONSTRUCTION LAYER (Cross-Checking Columns)
    # -------------------------------------------------------------------------
    # Correcting OHE Geo Columns to Single Feature
    if "Geography" not in plot_df.columns:
        if "Geography_Germany" in plot_df.columns and "Geography_Spain" in plot_df.columns:
            conditions = [
                (plot_df["Geography_Germany"] == 1),
                (plot_df["Geography_Spain"] == 1)
            ]
            choices = ["Germany", "Spain"]
            plot_df["Geography"] = np.select(conditions, choices, default="France")
        else:
            plot_df["Geography"] = "Unknown"

    # Fixing Gender Column Logic (Resolving the missing Male issue)
    if "Gender" not in plot_df.columns:
        if "Gender_Male" in plot_df.columns:
            # Check if boolean or binary integer and safely map
            plot_df["Gender"] = plot_df["Gender_Male"].apply(lambda x: "Male" if x in [1, True] else "Female")
        else:
            plot_df["Gender"] = "Unknown"

    # -------------------------------------------------------------------------
    # INTERACTIVE HEADER & EXECUTIVE METRIC RIBBON
    # -------------------------------------------------------------------------
   
    
   
    c1, c2, c3, c4 = st.columns(4)

    total_customers = len(plot_df)
    churn_rate = plot_df["Exited"].mean() * 100 if total_customers > 0 else 0
    avg_engagement = plot_df["engagement_score"].mean() if total_customers > 0 else 0
    active_pct = plot_df["IsActiveMember"].mean() * 100 if total_customers > 0 else 0

    with c1:
        st.metric(label="👥 Total Portfolio Base", value=f"{total_customers:,}")
    with c2:
        st.metric(label="📉 Overall Churn Rate", value=f"{churn_rate:.2f}%")
    with c3:
        st.metric(
    label="⚡ Avg Engagement Score", 
    value=f"{avg_engagement * 100:.2f}%"
)
    with c4:
        st.metric(label="🟢 Active Members Mix", value=f"{active_pct:.1f}%")

    # Granular Risk Targets Ribbon
    c5, c6, c7 = st.columns(3)
    active_members = plot_df[plot_df["IsActiveMember"] == 1]
    inactive_members = plot_df[plot_df["IsActiveMember"] == 0]
    active_churn_rate = active_members["Exited"].mean() * 100 if len(active_members) > 0 else 0
    inactive_churn_rate = inactive_members["Exited"].mean() * 100 if len(inactive_members) > 0 else 0

    high_balance_threshold = plot_df["Balance"].median()
    hv_at_risk = plot_df[(plot_df["Balance"] > high_balance_threshold) & (plot_df["Exited"] == 1)]["Balance"].sum()

    with c5:
        st.metric(label="🔥 Active Churn Rate", value=f"{active_churn_rate:.2f}%")
    with c6:
        st.metric(label="❄️ Inactive Churn Rate", value=f"{inactive_churn_rate:.2f}%")
    

    # -------------------------------------------------------------------------
    # SECTION 1: GEOGRAPHIC INTERPRETATION HUB
    # -------------------------------------------------------------------------
    st.markdown("---")
    st.subheader("🌍 Regional Risk & Market Distribution")
    
    # Building summary dataframe to feed hover_data cleanly
    geo_summary = plot_df.groupby("Geography").agg(
        Total_Customers=("CustomerId", "count"),
        Churn_Rate=("Exited", lambda x: round(x.mean() * 100, 2)),
        Active_Mix=("IsActiveMember", lambda x: round(x.mean() * 100, 2)),
        Avg_Balance=("Balance", lambda x: round(x.mean(), 2))
    ).reset_index()

    # Dynamic Bar chart embedded with deep tabular hover parameters
    fig_geo_bar = px.bar(
        geo_summary,
        x="Geography",
        y="Total_Customers",
        color="Churn_Rate",
        title="<b>Portfolio Volume by Territory (Hover for Comprehensive Metrics)</b>",
        labels={
            "Total_Customers": "Total Customer Base",
            "Geography": "Country / Region",
            "Churn_Rate": "Churn Rate (%)",
            "Active_Mix": "Active Member Mix (%)",
            "Avg_Balance": "Average Account Balance ($)"
        },
        color_continuous_scale=px.colors.sequential.Reds,
        hover_data=["Total_Customers", "Churn_Rate", "Active_Mix", "Avg_Balance"]
    )
    fig_geo_bar.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(200,200,200,0.15)")
    )
    st.plotly_chart(fig_geo_bar, use_container_width=True)

    # -------------------------------------------------------------------------
    # SECTION 2: DEMOGRAPHIC & ACTIVITY DEEP-DIVES (Grouped Structurally)
    # -------------------------------------------------------------------------
    st.markdown("---")
    st.subheader("🧬 Demographic Profile & Lifecycle Segments")
    col_d1, col_d2 = st.columns(2)

    with col_d1:
        # Age Bands Churn Configuration
        age_bins = [0, 30, 45, 60, np.inf]
        age_labels = ["Under 30", "30-45", "46-60", "60+"]
        plot_df["Age_Band"] = pd.cut(plot_df["Age"], bins=age_bins, labels=age_labels)
        
        age_churn = plot_df.groupby("Age_Band", observed=False)["Exited"].mean().reset_index()
        age_churn["Churn Rate (%)"] = age_churn["Exited"] * 100

        fig_age = px.bar(
            age_churn, x="Age_Band", y="Churn Rate (%)",
            title="<b>Churn Conversion by Lifecycle Age Bands</b>",
            color="Churn Rate (%)", color_continuous_scale=px.colors.sequential.Oranges
        )
        fig_age.update_layout(plot_bgcolor="rgba(0,0,0,0)", coloraxis_showscale=False)
        st.plotly_chart(fig_age, use_container_width=True)

    with col_d2:
        # Validated Cross-Gender Breakdown (Both Male & Female represented explicitly)
        fig_gender = px.histogram(
            plot_df, x="Gender", color="Status", barmode="group",
            title="<b>Gender Churn and Retention Volumetric Proportions</b>",
            color_discrete_map={"Churned": "#EF553B", "Retained": "#636EFA"}
        )
        fig_gender.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_gender, use_container_width=True)

    col_d3, col_d4 = st.columns(2)

    with col_d3:
        # Active vs Non-Active Structural Distribution
        plot_df["Membership"] = plot_df["IsActiveMember"].map({1: "Active Member", 0: "Inactive Member"})
        fig_active = px.histogram(
            plot_df, x="Membership", color="Status", barmode="stack",
            title="<b>Volumetric Churn across System Activity States</b>",
            color_discrete_map={"Churned": "#EF553B", "Retained": "#636EFA"}
        )
        fig_active.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_active, use_container_width=True)

    with col_d4:
        # Tenure vs Engagement Interaction Field
        scatter_sample = plot_df.sample(n=min(3000, len(plot_df)), random_state=42)
        fig_tenure_eng = px.scatter(
            scatter_sample, x="Tenure", y="engagement_score", color="Status",
            title="<b>Tenure vs Engagement Score Matrix Space</b> (Sampled)",
            color_discrete_map={"Churned": "#EF553B", "Retained": "#636EFA"}, opacity=0.6
        )
        fig_tenure_eng.update_layout(plot_bgcolor="rgba(245,245,245,0.3)")
        st.plotly_chart(fig_tenure_eng, use_container_width=True)

    # -------------------------------------------------------------------------
    # SECTION 3: STRATEGIC MATRIX & INTERACTION FRAMEWORKS
    # -------------------------------------------------------------------------
    st.markdown("---")
    st.subheader("🧮 Matrix Frameworks & Behavior Isolation")
    col_m1, col_m2 = st.columns(2)

    with col_m1:
        # Engagement Score Resolution
        fig_c1 = px.histogram(
            plot_df, x="engagement_score", color="Engagement_Segment", barmode="stack",
            title="<b>Engagement Score Resolution Space</b>",
            color_discrete_sequence=px.colors.qualitative.G10
        )
        fig_c1.add_shape(
            type="line", x0=0.55, y0=0, x1=0.55, y1=1, yref="paper",
            line=dict(color="Red", width=2, dash="dash")
        )
        fig_c1.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_c1, use_container_width=True)

    with col_m2:
        # Customer Value Segment vs Churn Mapping
        val_order = ["Platinum Value", "High Value", "Medium Value", "Low Value"]
        val_order = [v for v in val_order if v in plot_df["customer_value_segment"].unique()]
        
        fig_c2 = px.histogram(
            plot_df, x="customer_value_segment", color="Status", barmode="group",
            category_orders={"customer_value_segment": val_order},
            title="<b>Upgraded Strategic Value Segments vs Churn Status</b>",
            color_discrete_map={"Churned": "#EF553B", "Retained": "#636EFA"}
        )
        fig_c2.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_c2, use_container_width=True)

    col_m3, col_m4 = st.columns(2)

    with col_m3:
        # Heatmap Matrix: Commitment vs Engagement Churn Impact
        matrix_pivot = plot_df.groupby(["Commitment_Category", "Engagement_Category"])["Exited"].mean().reset_index()
        matrix_pivot["Churn Rate"] = matrix_pivot["Exited"] * 100
        
        fig_heat1 = px.density_heatmap(
            matrix_pivot, x="Engagement_Category", y="Commitment_Category", z="Churn Rate",
            histfunc="sum", text_auto=".1f", title="<b>Churn Rate Matrix (Commitment x Engagement %)</b>",
            color_continuous_scale="YlOrRd"
        )
        st.plotly_chart(fig_heat1, use_container_width=True)

    with col_m4:
        # Mismatch Cross Space Analysis
        fig_mis = px.scatter(
            scatter_sample, x="EstimatedSalary", y="Balance", color="Mismatch_Category",
            title="<b>Salary vs Balance Cross Space Analysis</b> (Sampled)",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_mis.update_layout(plot_bgcolor="rgba(245,245,245,0.3)", legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig_mis, use_container_width=True)

    # -------------------------------------------------------------------------
    # SECTION 4: CLUSTER STRATEGIC DNA PROFILE MATRIX
    # -------------------------------------------------------------------------
    st.markdown("---")
    st.subheader("🧬 Cluster Strategic DNA Profile Matrix")
    
    if "cluster_id" in plot_df.columns:
        cluster_profiles = plot_df.groupby("cluster_id").agg(
            Avg_Balance=("Balance", "mean"),
            Avg_Engagement=("engagement_score", "mean"),
            Churn_Rate=("Exited", "mean"),
            Loyalty_Ratio=("Loyalty_Ratio", "mean")
        ).reset_index()

        # Completely unique names assigned per index to eliminate collision
        def assign_cluster_label(row):
            c_id = int(row["cluster_id"])
            if row["Churn_Rate"] > 0.25:
                return f"Cluster {c_id}: High Churn-Prone"
            elif row["Avg_Balance"] > plot_df["Balance"].median() and row["Avg_Engagement"] > 50:
                return f"Cluster {c_id}: Loyal Premium Core"
            elif c_id == 3:
                return f"Cluster 3: Dormant Wealth Portfolio"
            elif c_id == 4:
                return f"Cluster 4: High-Asset Passive Retail"
            elif row["Avg_Engagement"] > 60:
                return f"Cluster {c_id}: Active Growth Driver"
            else:
                return f"Cluster {c_id}: Low Value Volatile"

        cluster_profiles["Strategic_Label"] = cluster_profiles.apply(assign_cluster_label, axis=1)
        
        metrics = ["Avg_Balance", "Avg_Engagement", "Churn_Rate", "Loyalty_Ratio"]
        hm_data = cluster_profiles.set_index("Strategic_Label")[metrics]
        
        # Scaling variables natively between [0, 1] for normalization mapping
        hm_norm = (hm_data - hm_data.min()) / (hm_data.max() - hm_data.min())
        
        fig_dna = ff.create_annotated_heatmap(
            z=hm_norm.values,
            x=list(hm_data.columns),
            y=list(hm_data.index),
            annotation_text=hm_data.round(2).astype(str).values,
            colorscale="YlGnBu"
        )
        fig_dna.update_layout(
            title="<b>Cluster Strategic DNA Profiles (Normalized Colors vs Real Values)</b>",
            xaxis_title="Core DNA Dimension",
            yaxis_title="De-duplicated Strategic Clusters"
        )
        st.plotly_chart(fig_dna, use_container_width=True)
    else:
        st.warning("⚠️ 'cluster_id' column not found. High-level cluster DNA scaling skipped.")