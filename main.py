import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from groq import Groq

# ==========================================
# 1. ማዋቀሪያዎች እና ቁልፎች
# ==========================================
TELEGRAM_BOT_TOKEN = "8641566663:AAEE3hoItahW-Nvv6Ve3f11J8jQcpIfMzfM"  # <--- የቦት ቶከንዎን እዚህ ያስገቡ
GROQ_API_KEY = "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"              # <--- የ Groq API Key-ዎን እዚህ ያስገቡ

client = Groq(api_key=GROQ_API_KEY)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ==========================================
# 2. የቦት ትዕዛዞች (Commands)
# ==========================================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ሰላም! እንኳን ወደ እጅግ ፈጣኑ Sonic AI ቻት ቦት በደህና መጡ። 🤖⚡️\n\n"
        "• ማንኛውንም ጥያቄ ለመጠየቅ በቀጥታ ጽሁፍ ይጻፉ (ሙሉ በሙሉ ነፃ እና ፈጣን ነው)!\n\n"
        "ℹ️ እርዳታ ለማግኘት፦ `/help`\n"
        "🔒 የግላዊነት መመሪያ፦ `/privacy`"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ምዕራፍ መመሪያዎች (Help Menu):\n\n"
        "1. **AI Chat:** ማንኛውንም ጥያቄ መጠየቅ፣ ጽሑፍ ማስጻፍ ይችላሉ።\n"
        "2. ከቦቱ ጋር መነጋገር ለመጀመር በቀጥታ የሚፈልጉትን ጽሁፍ መጻፍ ብቻ ነው የሚጠበቅብዎት።"
    )

async def privacy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔒 **የግላዊነት መመሪያ (Privacy Policy)**\n\n"
        "ይህ ቦት የእርስዎን ግላዊ መረጃዎች በአግባቡ ይይዛል። የሚላኩት ጽሑፎች ለአገልግሎት ማሰናጃ ብቻ የሚውሉ ሲሆን ለሶስተኛ አካል አንዳንተላለፍም።"
    )

# ==========================================
# 3. የ AI Chat (አሁን ባለው ትክክለኛ ሞዴል)
# ==========================================
async def handle_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_chat_action("typing")
    
    try:
        # በአዲሶቹ አካውንቶች ላይ ያለምንም ችግር የሚሰራው ሞዴል
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_text,
                }
            ],
            model="openai/gpt-oss-20b",
        )
        
        response_text = chat_completion.choices[0].message.content
        
        # መልእክቱ ከረዘመ በክፍል መላክ
        if len(response_text) > 4000:
            for i in range(0, len(response_text), 4000):
                part = response_text[i:i+4000]
                await update.message.reply_text(part)
        else:
            await update.message.reply_text(response_text)
            
    except Exception as e:
        await update.message.reply_text(f"⚠️ ስህተት ተከሰተ፡ {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # ትዕዛዞች ምዝገባ
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("privacy", privacy_command))
    
    # የጽሑፍ ውይይት
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_chat))
    
    print("ቦቱ በፈጣኑ የ Groq (llama3-8b-8192) ሲስተም ሥራ ጀምሯል...")
    app.run_polling()