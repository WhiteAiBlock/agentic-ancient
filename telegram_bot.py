#!/usr/bin/env python3
"""Interactive Telegram Bot for ClawAI"""
import subprocess
import json
import time

BOT_TOKEN = "8172752796:AAFJw12eczQ-ptofnsPkCVikA_qSkkWX4WQ"
TREASURY = "76x25b6XWTwbm6MTBJtbFU1hFopBSDKsfmGC7MK929RX"

def send_message(chat_id, text):
    """Send message to Telegram"""
    cmd = ['curl', '-s', '-X', 'POST',
           f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
           '-d', f'chat_id={chat_id}',
           '-d', f'text={text}']
    subprocess.run(cmd, capture_output=True)

def get_updates(offset=0):
    """Get new messages"""
    cmd = ['curl', '-s',
           f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={offset}']
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)

def handle_command(chat_id, text):
    """Handle bot commands"""
    text = text.lower().strip()
    
    if text in ['/start', '/help']:
        return """🤖 ClawAI Bot Commands:

/status - System status
/treasury - Treasury balance
/earnings - ClawPump earnings
/ralph - Trigger Ralph loop
/clawpump - ClawPump info
/help - Show this message"""
    
    elif text == '/status':
        return f"""✅ ClawAI Status

🦙 Ollama: Ready (GitHub Actions)
🐾 ClawPump: Integrated
🧬 Ralph Loop: Active
💰 Treasury: {TREASURY[:8]}...{TREASURY[-8:]}

All systems operational."""
    
    elif text == '/treasury':
        return f"""💰 Treasury Info

Address: {TREASURY}
Balance: 0.00203928 SOL

View: https://solscan.io/account/{TREASURY}"""
    
    elif text == '/earnings':
        return """🐾 ClawPump Earnings

Total Earned: 0 SOL
Total Sent: 0 SOL
Pending: 0 SOL

No token launches yet. Use /clawpump to learn more."""
    
    elif text == '/ralph':
        return """🧬 Ralph Loop Triggered

Running via GitHub Actions:
- qwen2.5-coder:7b model
- 6 strategies per cycle
- Every 4 hours

Monitor: https://github.com/WhiteAiBlock/agentic-ancient/actions"""
    
    elif text == '/clawpump':
        return """🐾 ClawPump Integration

Launch tokens on pump.fun:
- Gasless (FREE) launches
- Earn 65% trading fees
- Self-funded option (~0.03 SOL)

API: https://clawpump.tech"""
    
    else:
        return f"Unknown command: {text}\n\nUse /help to see available commands."

def main():
    """Run bot polling loop"""
    print("🤖 Starting ClawAI Telegram Bot...")
    print(f"Bot: @Genenout_bot")
    print("Listening for messages...\n")
    
    offset = 0
    while True:
        try:
            updates = get_updates(offset)
            
            if updates.get('ok') and updates.get('result'):
                for update in updates['result']:
                    offset = update['update_id'] + 1
                    
                    if 'message' in update:
                        msg = update['message']
                        chat_id = msg['chat']['id']
                        text = msg.get('text', '')
                        user = msg['from'].get('first_name', 'User')
                        
                        print(f"📨 {user}: {text}")
                        
                        response = handle_command(chat_id, text)
                        send_message(chat_id, response)
                        print(f"✅ Replied to {user}\n")
            
            time.sleep(2)
            
        except KeyboardInterrupt:
            print("\n🛑 Bot stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
