import re

with open('frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Add management functions after handleNewChat
funcs_code = """
  const handleRenameChat = (chatId, e) => {
    e.stopPropagation();
    const chat = chatHistoryList.find(c => c.id === chatId);
    if (!chat) return;
    const newTitle = window.prompt("Enter new title for this chat:", chat.title);
    if (newTitle && newTitle.trim() !== "") {
        const newList = chatHistoryList.map(c => c.id === chatId ? { ...c, title: newTitle.trim() } : c);
        setChatHistoryList(newList);
        try {
            localStorage.setItem('aion_chat_history', JSON.stringify(newList));
        } catch (err) {}
    }
  };

  const handleDeleteChat = (chatId, e) => {
    e.stopPropagation();
    if (window.confirm("Are you sure you want to delete this chat thread?")) {
        const newList = chatHistoryList.filter(c => c.id !== chatId);
        setChatHistoryList(newList);
        try {
            localStorage.setItem('aion_chat_history', JSON.stringify(newList));
        } catch (err) {}
        
        // If we deleted the active chat, clear the screen
        if (currentChatId === chatId) {
            handleNewChat();
        }
    }
  };
"""

if "const handleRenameChat" not in content:
    content = content.replace(
        "const handleNewChat = () => {",
        funcs_code + "\n  const handleNewChat = () => {"
    )

# Update sidebar item JSX
# Currently it looks like:
# <div key={chat.id} className={`sidebar-history-item ${currentChatId === chat.id ? 'active' : ''}`} onClick={() => handleLoadChat(chat.id)} title={chat.title}>
#   💬 <span className="history-item-text">{chat.title}</span>
# </div>

new_item_jsx = """<div 
                key={chat.id} 
                className={`sidebar-history-item ${currentChatId === chat.id ? 'active' : ''}`}
                onClick={() => handleLoadChat(chat.id)}
                title={chat.title}
                style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '10px 12px' }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', overflow: 'hidden' }}>
                    💬 <span className="history-item-text" style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{chat.title}</span>
                </div>
                <div className="history-actions" style={{ display: 'flex', gap: '6px' }}>
                    <button onClick={(e) => handleRenameChat(chat.id, e)} style={{ background: 'transparent', border: 'none', cursor: 'pointer', opacity: 0.7, fontSize: '0.8rem' }} title="Rename">✏️</button>
                    <button onClick={(e) => handleDeleteChat(chat.id, e)} style={{ background: 'transparent', border: 'none', cursor: 'pointer', opacity: 0.7, fontSize: '0.8rem' }} title="Delete">🗑️</button>
                </div>
              </div>"""

# Replace the original map return block
import re
pattern = re.compile(r'<div\s+key=\{chat\.id\}\s+className=\{`sidebar-history-item.*?</div>', re.DOTALL)
if "handleRenameChat(chat.id" not in content:
    content = pattern.sub(new_item_jsx, content)

with open('frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Chat management added!")
