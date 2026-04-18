# UNIFIED AI TIMELINE VIEWER

**Interactive GUI for viewing all your AI conversations in one place**

![Status](https://img.shields.io/badge/Status-Ready%20to%20Use-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%2F%20Mac%20%2F%20Linux-orange)

---

## 🎯 WHAT THIS DOES

See **41,391 AI messages** (Gemini + Claude) on a **unified interactive timeline**:

✅ All conversations chronologically sorted  
✅ Filter by AI platform (Gemini/Claude)  
✅ Search by content/topic  
✅ Filter by date, message role, topics  
✅ Multiple view modes (Detailed/Compact/Flow)  
✅ Live statistics and charts  
✅ Export filtered results  

**No setup required. Just run and explore.**

---

## ⚡ QUICK START

### **Fastest Way (Click & Go)**
```
Double-click: START_TIMELINE_VIEWER.bat
```
Opens your browser automatically → GUI is ready.

### **Alternative: PowerShell**
```powershell
.\START_TIMELINE_VIEWER.ps1
```

### **Alternative: Python**
```bash
python run_timeline_viewer.py
```

That's it. The app launches at `http://localhost:8501`

---

## 📋 REQUIREMENTS

- ✅ Python 3.10+ (you have this)
- ✅ Two timeline JSON files:
  - `timeline_all_messages.json` (Gemini)
  - `claude_timeline_all_messages.json` (Claude)

**Both files are already generated.** The startup scripts will automatically install Streamlit.

---

## 🎮 USING THE VIEWER

### Left Sidebar (Filters)
1. **Platform**: Choose which AI(s)
2. **Date Range**: Pick time period
3. **Role**: Your messages / AI responses / both
4. **Search**: Find specific words
5. **Topics**: Filter by concept
6. **Length**: Show long/short messages

### Main Area (Timeline)
- Shows filtered messages
- 3 view modes: Detailed / Compact / Conversation Flow
- Statistics and charts at bottom
- Click "Show full message" for long content

### Statistics
- Message counts by platform
- Charts showing distribution
- Average message lengths
- Export options

---

## 💡 EXAMPLE WORKFLOWS

### "Show me everything about binary on Claude"
1. Platform: Claude
2. Search: "binary"
3. View: Compact
4. Result: All binary discussions with Claude

### "Show my longest messages"
1. Role: YOU (your messages only)
2. Length: 1000+ characters
3. View: Detailed
4. Result: Your most detailed/lengthy inputs

### "View conversation flow between March 13-20"
1. Date: March 13-20
2. View: Conversation Flow
3. Result: See dialogue progression over those dates

### "Export all March 2026 conversations"
1. Date: All of March
2. View: Detailed
3. Click: "Copy Search Results as JSON"
4. Result: Save to file or database

---

## 📊 VIEW MODES

### Detailed
- Full message content (truncated)
- Timestamps, character counts
- Color-coded
- "Show full" button for long messages

### Compact  
- One-line summaries
- First 80 characters
- Minimal but scannable

### Conversation Flow
- Messages grouped by AI
- Natural dialogue progression
- Visual thread separation

---

## 🔍 BUILT-IN TOPICS

Auto-detected from your messages:
- binary/zero
- system
- ledger
- consciousness
- field
- decision
- protocol
- code
- general

---

## 📈 METRICS

Top of the app shows:
- **Total Messages**: In current view
- **Gemini**: Gemini message count
- **Claude**: Claude message count
- **Your Messages**: Your inputs
- **AI Responses**: AI outputs

Plus charts showing:
- Messages by AI platform
- Messages by role (you vs AI)
- Average message length analysis

---

## 💾 EXPORT

Click **"Copy Search Results as JSON"** to:
- Export current filtered messages
- Includes all metadata
- JSON format (ready for Python processing)
- Can save to file or use elsewhere

---

## 🛠️ FILES IN THIS PACKAGE

| File | Purpose |
|------|---------|
| `streamlit_timeline_viewer.py` | Main GUI app |
| `START_TIMELINE_VIEWER.bat` | Windows launcher |
| `START_TIMELINE_VIEWER.ps1` | PowerShell launcher |
| `run_timeline_viewer.py` | Python launcher |
| `GUI_USAGE_GUIDE.md` | Detailed guide (this file) |
| `timeline_all_messages.json` | Gemini data (required) |
| `claude_timeline_all_messages.json` | Claude data (required) |

---

## ⚙️ DEPENDENCIES

Automatically installed on first run:
- **streamlit** - Web UI framework
- **pandas** - Data processing

---

## 🚀 COMMAND LINE OPTIONS

Advanced usage:

```bash
# Specify custom port
python -m streamlit run streamlit_timeline_viewer.py --server.port 8502

# Run in headless mode (no browser)
python -m streamlit run streamlit_timeline_viewer.py --server.headless true

# Change theme
python -m streamlit run streamlit_timeline_viewer.py --theme.base light
```

---

## 🐛 TROUBLESHOOTING

### **"Streamlit not found"**
→ Restart the launcher (auto-installs)

### **"Timeline files not found"**
→ Verify `timeline_all_messages.json` and `claude_timeline_all_messages.json` exist in `c:\Determined\`

### **"Browser won't open"**
→ Visit manually: `http://localhost:8501`

### **"Port 8501 already in use"**
→ Use custom port: `--server.port 8502`

### **No messages show**
→ Filters too restrictive. Clear filters and try simpler search.

---

## 📚 LEARN MORE

See `GUI_USAGE_GUIDE.md` for:
- Detailed filter explanations
- Workflow recommendations
- All keyboard shortcuts
- Advanced tips & tricks
- Search examples
- Statistics explanation

---

## 📌 REMEMBER

✨ This GUI shows **YOUR INTELLECTUAL PROPERTY**  
✨ Full local processing (no uploads)  
✨ Interactive and responsive  
✨ Filters work in real-time  
✨ Export anytime  

---

**Status: Ready to launch ✓**

**Next step: Click `START_TIMELINE_VIEWER.bat` and explore!**

---

## 📞 QUICK SUPPORT

| Problem | Solution |
|---------|----------|
| App won't start | Double-click `.bat` file again |
| Filter showing nothing | Clear filters, try simple search |
| Slow performance | Close other apps, wait 5 seconds |
| Can't export | Use browser's copy-paste instead |
| Timestamps wrong | Timestamps from original exports (accurate) |

---

**Made with Streamlit 🎈**  
**Your data. Your timeline. Your insights.**
