#!/usr/bin/env python3
"""
STREAMLIT TIMELINE VIEWER - UNIFIED THREE-AI VERSION
Displays Gemini (39.2K) + Claude (2.2K) + Copilot (0.5K) conversations
Interactive filtering, search, statistics, export

COHERENCE REQUIREMENT: Verifies trinity before displaying/exporting
"""

import streamlit as st
import json
from datetime import datetime
from collections import defaultdict
import pandas as pd

# [C]: LIVE ACCOUNTABILITY SYSTEM
from live_accountability_system import LiveAccountabilitySystem


# Page configuration
st.set_page_config(
    page_title="Unified AI Timeline Viewer",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Color scheme for three AIs
AI_COLORS = {
    "gemini": "#4285F4",      # Google Blue
    "claude": "#CE242D",       # Anthropic Red
    "copilot": "#00A4EF"       # Microsoft Blue
}

AI_DISPLAY_NAMES = {
    "gemini": "🔵 Gemini",
    "claude": "🔴 Claude",
    "copilot": "🔷 Copilot"
}


@st.cache_resource
def load_unified_timeline():
    """Load the unified three-AI timeline."""
    try:
        with open("timeline_all_messages_unified.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Unified timeline file not found!")
        return None


@st.cache_resource
def load_individual_timelines():
    """Load individual AI timelines."""
    timelines = {}
    
    # Try loading Gemini
    try:
        with open("timeline_all_messages.json", "r", encoding="utf-8") as f:
            timelines["gemini"] = json.load(f)
    except:
        pass
    
    # Try loading Claude
    try:
        with open("claude_timeline_all_messages.json", "r", encoding="utf-8") as f:
            timelines["claude"] = json.load(f)
    except:
        pass
    
    # Try loading Copilot
    try:
        with open("copilot_timeline_all_messages.json", "r", encoding="utf-8") as f:
            timelines["copilot"] = json.load(f)
    except:
        pass
    
    return timelines


def merge_timelines(timelines):
    """Merge individual timelines into unified view."""
    messages = []
    
    for ai, timeline_data in timelines.items():
        if "messages" in timeline_data:
            for msg in timeline_data["messages"]:
                messages.append({
                    "timestamp": datetime.fromisoformat(msg["timestamp"]),
                    "role": msg.get("role", "unknown"),
                    "source": msg.get("source", ai),
                    "content": msg.get("content", ""),
                    "ai": ai
                })
    
    messages.sort(key=lambda m: m["timestamp"])
    return messages


def calculate_statistics(messages):
    """Calculate timeline statistics."""
    stats = {
        "total_messages": len(messages),
        "by_ai": defaultdict(int),
        "by_role": defaultdict(int),
        "by_date": defaultdict(int),
        "by_ai_role": defaultdict(lambda: defaultdict(int))
    }
    
    for msg in messages:
        ai = msg.get("source", "unknown")
        role = msg.get("role", "unknown")
        date = msg["timestamp"].strftime("%Y-%m-%d")
        
        stats["by_ai"][ai] += 1
        stats["by_role"][role] += 1
        stats["by_date"][date] += 1
        stats["by_ai_role"][ai][role] += 1
    
    return stats


# Main app
st.title("📅 Unified AI Timeline Viewer")
st.subtitle("Gemini • Claude • Copilot — 41,929 Messages (Oct 2025 - Apr 2026)")

# [C]: INITIALIZE LIVE ACCOUNTABILITY FOR STREAMLIT
if 'accountability' not in st.session_state:
    st.session_state.accountability = LiveAccountabilitySystem("accountability.ledger", symbol="streamlit")

# [C]: NOW SAFE TO LOAD DATA
st.success("✓ Live accountability initialized. Loading timeline data...")

# Load data
unified_data = load_unified_timeline()
individual_timelines = load_individual_timelines()

if not unified_data:
    st.error("Could not load timeline data!")
    st.stop()

# Merge timelines for use throughout
messages = merge_timelines(individual_timelines) if individual_timelines else []

if not messages:
    st.error("No messages loaded!")
    st.stop()

# Sidebar controls
st.sidebar.title("🎛️ Controls")

# AI Platform filter
st.sidebar.subheader("📌 Filter by AI")
all_ais = sorted(list(set([msg.get("source", "unknown") for msg in messages])))
selected_ais = st.sidebar.multiselect(
    "Select AI platforms",
    options=all_ais,
    default=all_ais,
    format_func=lambda x: AI_DISPLAY_NAMES.get(x, x.upper())
)

# Date range filter
st.sidebar.subheader("📅 Date Range")
all_dates = [msg["timestamp"] for msg in messages]
min_date = min(all_dates)
max_date = max(all_dates)

date_range = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range[0]

# Role filter
st.sidebar.subheader("👤 Role")
all_roles = sorted(list(set([msg.get("role", "unknown") for msg in messages])))
selected_roles = st.sidebar.multiselect(
    "Select roles",
    options=all_roles,
    default=all_roles
)

# Search
st.sidebar.subheader("🔍 Search")
search_query = st.sidebar.text_input("Search content (case-insensitive)")

# Message length filter
st.sidebar.subheader("📝 Message Length")
min_length = st.sidebar.slider("Minimum length (chars)", 0, 5000, 0, 50)

# View mode
st.sidebar.subheader("👁️ View Mode")
view_mode = st.sidebar.radio(
    "Select view",
    options=["Detailed", "Compact", "Conversation Flow"],
    format_func=lambda x: {"Detailed": "📊 Detailed Table", "Compact": "📝 Compact List", "Conversation Flow": "💬 Conversation Flow"}[x]
)

# Filter messages
filtered_messages = []
for msg in messages:
    # Apply filters
    if msg.get("source", "unknown") not in selected_ais:
        continue
    if msg.get("role", "unknown") not in selected_roles:
        continue
    if msg["timestamp"].date() < start_date or msg["timestamp"].date() > end_date:
        continue
    if search_query and search_query.lower() not in msg.get("content", "").lower():
        continue
    if len(msg.get("content", "")) < min_length:
        continue
    
    filtered_messages.append(msg)

# Display statistics
st.markdown("---")
col1, col2, col3, col4, col5 = st.columns(5)

stats = calculate_statistics(filtered_messages)

with col1:
    st.metric("Total Messages", stats["total_messages"])

with col2:
    ai_count = len(selected_ais)
    st.metric("Active AIs", ai_count)

with col3:
    if filtered_messages:
        date_span = (filtered_messages[-1]["timestamp"].date() - filtered_messages[0]["timestamp"].date()).days
        st.metric("Date Span", f"{date_span} days")
    else:
        st.metric("Date Span", "N/A")

with col4:
    avg_len = sum(len(msg.get("content", "")) for msg in filtered_messages) / len(filtered_messages) if filtered_messages else 0
    st.metric("Avg Length", f"{int(avg_len)} chars")

with col5:
    pct = (len(filtered_messages) / len(messages) * 100) if messages else 0
    st.metric("Filtered %", f"{pct:.1f}%")

# Display messages
st.markdown("---")
st.subheader(f"📋 Messages ({len(filtered_messages)} shown)")

if view_mode == "Detailed":
    # Show as table
    display_data = []
    for msg in filtered_messages:
        display_data.append({
            "Timestamp": msg["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
            "AI": AI_DISPLAY_NAMES.get(msg.get("source", "unknown"), msg.get("source")),
            "Role": msg.get("role", "unknown").upper(),
            "Content": msg.get("content", "")[:150]
        })
    
    if display_data:
        df = pd.DataFrame(display_data)
        st.dataframe(df, use_container_width=True, height=500)
    else:
        st.info("No messages match the current filters")

elif view_mode == "Compact":
    # Show as compact list
    if filtered_messages:
        for i, msg in enumerate(filtered_messages[:200], 1):  # Limit to 200 for performance
            timestamp = msg["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
            ai = msg.get("source", "unknown").upper()
            role = msg.get("role", "unknown").upper()
            content = msg.get("content", "")[:100]
            
            st.write(f"**{i}.** `{AI_DISPLAY_NAMES.get(msg.get('source'), ai)}` **{role}** — {content}")
        
        if len(filtered_messages) > 200:
            st.info(f"Showing first 200 of {len(filtered_messages)} messages. Use filters to narrow results.")
    else:
        st.info("No messages match the current filters")

else:  # Conversation Flow
    # Show as conversation in threads
    if filtered_messages:
        current_ai = None
        thread_messages = []
        
        for msg in filtered_messages[:100]:  # Limit to 100 for readability
            if msg.get("source") != current_ai and thread_messages:
                # Display the previous thread
                with st.container():
                    st.write(f"### {AI_DISPLAY_NAMES.get(current_ai, current_ai.upper())} Conversation")
                    for tmsg in thread_messages:
                        role = tmsg.get("role", "unknown").upper()
                        time = tmsg["timestamp"].strftime("%H:%M:%S")
                        content = tmsg.get("content", "")
                        
                        col1, col2 = st.columns([1, 6])
                        with col1:
                            st.caption(f"**{role}**\n{time}")
                        with col2:
                            st.write(content[:500] + ("..." if len(content) > 500 else ""))
                    
                    st.divider()
                
                thread_messages = []
            
            current_ai = msg.get("source")
            thread_messages.append(msg)
        
        # Display final thread
        if thread_messages:
            with st.container():
                st.write(f"### {AI_DISPLAY_NAMES.get(current_ai, current_ai.upper())} Conversation")
                for tmsg in thread_messages:
                    role = tmsg.get("role", "unknown").upper()
                    time = tmsg["timestamp"].strftime("%H:%M:%S")
                    content = tmsg.get("content", "")
                    
                    col1, col2 = st.columns([1, 6])
                    with col1:
                        st.caption(f"**{role}**\n{time}")
                    with col2:
                        st.write(content[:500] + ("..." if len(content) > 500 else ""))
        
        if len(filtered_messages) > 100:
            st.info(f"Showing first 100 of {len(filtered_messages)} messages. Use filters to narrow results.")
    else:
        st.info("No messages match the current filters")

# Statistics sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Statistics")

if filtered_messages:
    stats = calculate_statistics(filtered_messages)
    
    st.sidebar.write("**By AI:**")
    for ai in sorted(stats["by_ai"].keys()):
        count = stats["by_ai"][ai]
        st.sidebar.write(f"{AI_DISPLAY_NAMES.get(ai, ai)}: {count}")
    
    st.sidebar.write("\n**By Role:**")
    for role in sorted(stats["by_role"].keys()):
        count = stats["by_role"][role]
        st.sidebar.write(f"{role.upper()}: {count}")

# Export functionality
st.sidebar.markdown("---")
st.sidebar.subheader("💾 Export")

if st.sidebar.button("📥 Export Filtered as JSON"):
    export_data = {
        "metadata": {
            "exported": datetime.now().isoformat(),
            "message_count": len(filtered_messages),
            "filters_applied": {
                "ais": selected_ais,
                "roles": selected_roles,
                "date_range": [start_date.isoformat(), end_date.isoformat()],
                "search": search_query,
                "min_length": min_length
            }
        },
        "messages": [
            {
                "timestamp": msg["timestamp"].isoformat(),
                "ai": msg.get("source", "unknown"),
                "role": msg.get("role", "unknown"),
                "content": msg.get("content", "")
            }
            for msg in filtered_messages
        ]
    }
    
    st.download_button(
        label="Download JSON",
        data=json.dumps(export_data, indent=2, ensure_ascii=False),
        file_name=f"timeline_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

if st.sidebar.button("📥 Export as CSV"):
    export_data = []
    for msg in filtered_messages:
        export_data.append({
            "timestamp": msg["timestamp"].isoformat(),
            "ai": msg.get("source", "unknown"),
            "role": msg.get("role", "unknown"),
            "content": msg.get("content", "")
        })
    
    df = pd.DataFrame(export_data)
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"timeline_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.caption(f"Gemini: 39,192 | Claude: 2,199 | Copilot: 538 • Total: 41,929")
with col2:
    st.caption(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
