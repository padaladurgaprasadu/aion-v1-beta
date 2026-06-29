with open('frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace border colors and other leftovers
content = content.replace("1px solid #333", "1px solid var(--border-color)")
content = content.replace("borderBottom: '1px solid #2a2a2a'", "borderBottom: '1px solid var(--border-color)'")
content = content.replace("border-bottom: 1px solid #333", "border-bottom: 1px solid var(--border-color)")
content = content.replace("border-top: 1px dashed #333", "border-top: 1px dashed var(--border-color)")

# Add light-theme CSS overrides
css_path = 'frontend/src/index.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

if '--modal-text-color' not in css_content:
    css_content = css_content.replace(
        "--input-bg: rgba(0, 0, 0, 0.2);",
        "--input-bg: rgba(0, 0, 0, 0.2);\n  --modal-text-color: #ccc;"
    )
    css_content = css_content.replace(
        "--input-bg: #ffffff;",
        "--input-bg: #ffffff;\n  --modal-text-color: #000;"
    )

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css_content)

# Update App.jsx for modal-text-color
content = content.replace("color: '#ccc'", "color: 'var(--modal-text-color)'")
content = content.replace("color: '#aaa'", "color: 'var(--modal-text-color)'")
content = content.replace("color: '#888'", "color: 'var(--modal-text-color)'")

with open('frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Second refactor done")
