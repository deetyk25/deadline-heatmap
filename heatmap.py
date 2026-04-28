import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# load
df = pd.read_csv("notion.csv")

# fix column names (lowercase everything)
df.columns = df.columns.str.lower()

# clean dates (remove timezone text like "(PDT)")
df['date'] = df['date'].str.replace(r"\(.*\)", "", regex=True)

# parse dates safely
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# drop rows with no date (like Lab 4)
df = df.dropna(subset=['date'])

# filter quarter (your CSV says "Spring", not "Spring 2026")
df = df[df['quarter'] == 'Spring']

# optional: remove completed
df = df[df['status'] != 'Done']

# extract time features
df['week'] = df['date'].dt.isocalendar().week
df['day'] = df['date'].dt.dayofweek  # 0=Mon

# weights (lowercase to match your data)
weights = {
    'homework': 1,
    'project': 1,
    'assignment': 1.5,
    'lab': 2,
    'exam': 3
}

df['weight'] = df['type'].str.lower().map(weights).fillna(1)

# loop per course
courses = df['course'].unique()

for course in courses:
    subset = df[df['course'] == course]
    
    counts = subset.groupby(['week', 'day'])['weight'].sum().reset_index()
    
    pivot = counts.pivot(index='week', columns='day', values='weight').fillna(0)
    
    # fix day labels BEFORE plotting
    pivot = pivot.reindex(columns=range(7), fill_value=0)
    pivot.columns = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    plt.figure(figsize=(10, 5))
    sns.heatmap(pivot, annot=True, fmt=".1f")
    plt.title(f"Deadline Heatmap - {course}")
    plt.xlabel("Day of Week")
    plt.ylabel("Week")
    plt.show()





# COLOR ICONS
type_icons = {
    'homework': '📚',
    'project': '💼',
    'assignment': '📁',
    'lab': '🔬',
    'exam': '💯',
}

# HOVER TEXT
def format_day(group):
    group = group.sort_values('weight', ascending=False)
    
    lines = []
    for _, row in group.iterrows():
        icon = type_icons.get(row['type'].lower(), '⬜')
        
        lines.append(
            f"{icon} <b>{row['name']}</b><br>"
            f"<span style='color:gray'>{row['course']} • {row['type']}</span>"
        )
    
    return "<br>".join(lines)

assignments_per_day = df.groupby('date').apply(format_day)

# DAILY STRESS + FULL RANGE
full_range = pd.date_range(df['date'].min(), df['date'].max(), freq='D')

daily = df.groupby('date')['weight'].sum().reindex(full_range, fill_value=0)
assignments_per_day = assignments_per_day.reindex(full_range, fill_value="✨ No deadlines ✨")

# BUILD CALENDAR DF
cal_df = pd.DataFrame({
    'date': full_range,
    'weight': daily.values,
    'assignments': assignments_per_day.values
})

# sequential week index
cal_df['year'] = cal_df['date'].dt.year
cal_df['week'] = cal_df['date'].dt.isocalendar().week

# combine year + week so June/July don’t collide
cal_df['week_id'] = cal_df['year'].astype(str) + "-W" + cal_df['week'].astype(str)

cal_df['day'] = cal_df['date'].dt.dayofweek
cal_df['label'] = cal_df['date'].dt.strftime('%b %d')

# PIVOTS
pivot = cal_df.pivot(index='week_id', columns='day', values='weight')
hover = cal_df.pivot(index='week_id', columns='day', values='assignments')
labels = cal_df.pivot(index='week_id', columns='day', values='label')

pivot = pivot.sort_index().reindex(columns=range(7), fill_value=0)
hover = hover.reindex_like(pivot).fillna("✨ No deadlines ✨")
labels = labels.reindex_like(pivot).fillna("")

pivot = pivot.fillna(0)
hover = hover.fillna("✨ No deadlines ✨")
labels = labels.fillna("")

# INTERACTIVE HEATMAP
fig = px.imshow(
    pivot,
    color_continuous_scale=[
        [0.0, "#1a001a"],   # near black purple
        # [0.0, "#F6F3F3"],
        [0.2, "#f563a2"],   # pink
        [0.4, "#ff2e88"],   # pink
        [0.6, "#c2185b"],   # dark purple
        [0.8, "#AB22AB"],   # dark purple
        [1.0, "#5a1b5a"],   # near black purple
    ],
    aspect='auto'
)

fig.update_traces(
    text=hover.values,
    customdata=labels.values,
    hovertemplate=
    "<b>%{customdata}</b><br>" +
    "Stress: %{z}<br><br>" +
    "%{text}<extra></extra>"
)

fig.update_layout(
    title="🔥 Interactive Deadline Stress Heatmap",
    xaxis=dict(
        title="Day of the Week",
        tickmode='array',
        tickvals=list(range(7)),
        ticktext=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    ),
    yaxis=dict(
        title="Calendar Week",
        tickmode='array',
        tickvals=list(range(len(pivot.index))),
        ticktext=list(pivot.index)
    ),
    coloraxis_colorbar=dict(title="Stress"),
    font=dict(
        family="Arial, Helvetica, sans-serif",
        size=13,
        color="white"
    ),
    paper_bgcolor="#0b0b0d",
    plot_bgcolor="#0b0b0d",
)

fig.show()
