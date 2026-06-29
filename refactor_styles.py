import re

with open('frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace hardcoded colors with CSS variables
replacements = {
    "'#1a1a1a'": "'var(--sidebar-bg)'",
    "'#0f0f0f'": "'var(--app-bg)'",
    "'#333'": "'var(--border-color)'",
    "'#2a2a2a'": "'var(--border-color)'",
    "'#0d0d0d'": "'var(--input-bg)'",
    "'#111'": "'var(--sidebar-bg)'",
    "rgba(0,0,0,0.8)": "var(--modal-overlay)",
    "backgroundColor: msg.role === 'user' ? '#333' : 'var(--accent)'": "backgroundColor: msg.role === 'user' ? 'var(--msg-user-bg)' : 'var(--accent)'",
    "backgroundColor: msg.role === 'user' ? '#2a2a2a' : 'transparent'": "backgroundColor: msg.role === 'user' ? 'var(--msg-user-bg)' : 'var(--msg-ai-bg)'",
    "backgroundColor: '#222'": "backgroundColor: 'var(--btn-bg)'",
    "color: '#ccc'": "color: 'var(--text-secondary)'",
    "color: '#ececec'": "color: 'var(--text-primary)'",
    "color: '#fff'": "color: 'var(--text-primary)'",
}

for old, new in replacements.items():
    content = content.replace(old, new)

# Theme State
if 'const [theme, setTheme] = useState' not in content:
    # Add after showSettingsModal
    content = content.replace(
        "const [showSettingsModal, setShowSettingsModal] = useState(false)",
        "const [showSettingsModal, setShowSettingsModal] = useState(false)\n  const [theme, setTheme] = useState(() => localStorage.getItem('aion_theme') || 'Dark (Default)')"
    )

# Theme UseEffect
if 'document.documentElement.classList' not in content:
    # Add after load chat history useEffect
    effect_code = """
  // Apply theme class
  useEffect(() => {
    localStorage.setItem('aion_theme', theme);
    if (theme === 'Light' || (theme === 'System' && window.matchMedia('(prefers-color-scheme: light)').matches)) {
        document.documentElement.classList.add('light-theme');
    } else {
        document.documentElement.classList.remove('light-theme');
    }
  }, [theme]);
"""
    content = content.replace("useEffect(() => {\n    chatEndRef.current", effect_code + "\n  useEffect(() => {\n    chatEndRef.current")

# Settings Modal Select binding
content = content.replace(
    "<select style={{ width: '100%', padding: '12px', backgroundColor: 'var(--input-bg)', border: '1px solid var(--border-color)', borderRadius: '8px', color: 'var(--text-secondary)', appearance: 'none', cursor: 'pointer' }}>",
    "<select value={theme} onChange={(e) => setTheme(e.target.value)} style={{ width: '100%', padding: '12px', backgroundColor: 'var(--input-bg)', border: '1px solid var(--border-color)', borderRadius: '8px', color: 'var(--text-secondary)', appearance: 'none', cursor: 'pointer' }}>"
)

with open('frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Styles refactored!")
