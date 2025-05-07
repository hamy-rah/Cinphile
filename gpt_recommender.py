import openai
import re

client = openai.OpenAI(api_key="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")  # 👈 جایگزین کن

# تاریخچه مکالمه برای هر کاربر
conversation_history = {}
# لیست فیلم‌های پیشنهادی قبلی برای هر کاربر
user_movie_log = {}

def extract_movie_title(text):
    """
    تلاش برای استخراج نام فیلم از پاسخ GPT (با فرض اینکه در کوتیشن یا اول پیام باشه)
    """
    match = re.search(r'"([^"]+)"', text)  # دنبال چیزی مثل "The Shawshank Redemption"
    if match:
        return match.group(1).strip()
    match = re.search(r'I recommend .*?([A-Z][\w\s:!\'\-&]+)', text)
    if match:
        return match.group(1).strip()
    return None

def get_movie_recommendation(user_id, user_prompt):
    system_message = (
        "You are a smart and friendly assistant that only recommends movies or TV series. "
        "If the user says 'another', 'seen it', 'not this one', or similar, understand that they want a new recommendation. "
        "Avoid recommending the same movie twice. Keep track of movies you suggest and try to vary your responses."
    )

    if user_id not in conversation_history:
        conversation_history[user_id] = [{"role": "system", "content": system_message}]
        user_movie_log[user_id] = []

    conversation_history[user_id].append({"role": "user", "content": user_prompt})

    for _ in range(3):  # تا ۳ بار تلاش برای دریافت فیلم متفاوت
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=conversation_history[user_id],
                temperature=0.8,
                max_tokens=300
            )

            reply = response.choices[0].message.content.strip()
            title = extract_movie_title(reply)

            if title and title in user_movie_log[user_id]:
                conversation_history[user_id].append({
                    "role": "user",
                    "content": f"I’ve already seen '{title}'. Please recommend something else."
                })
                continue

            if title:
                user_movie_log[user_id].append(title)

            conversation_history[user_id].append({"role": "assistant", "content": reply})
            return reply

        except Exception as e:
            print("GPT API Error:", e)
            return "⚠️ Sorry, I couldn't fetch a recommendation right now."

    return "😕 I couldn't find a different movie right now. Try again later."
