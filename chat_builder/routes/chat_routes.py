from flask import Blueprint, render_template, request, jsonify
import google.generativeai as genai
from groq import Groq
import os
from dotenv import load_dotenv

# تحميل المتغيرات البيئية
load_dotenv()

# تهيئة النماذج
models = {}

# تهيئة نموذج Google Gemini إذا كان المفتاح متوفراً
gemini_api_key = os.getenv('GOOGLE_API_KEY')
if gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)
        models['gemini'] = genai.GenerativeModel('gemini-pro')
        print("Gemini model initialized successfully")
    except Exception as e:
        print(f"Error initializing Gemini model: {e}")

# تهيئة نموذج Groq Llama إذا كان المفتاح متوفراً
groq_api_key = os.getenv('GROQ_API_KEY')
if groq_api_key:
    try:
        models['llama'] = Groq(api_key=groq_api_key)
        print("Llama model initialized successfully")
    except Exception as e:
        print(f"Error initializing Llama model: {e}")

chat_bp = Blueprint('chat', __name__)

def get_chat_prompt(stage, text):
    """إنشاء النص التوجيهي المناسب للمرحلة في المحادثة"""
    base_prompts = {
        'initial': "مرحباً! نحن هنا لمساعدتك في بناء قضيتك. هل يمكنك إخبارنا أولاً عن نوع القضية التي تريد مناقشتها؟",
        'parties': "شكراً لتحديد نوع القضية. الآن، هل يمكنك إخبارنا عن الأطراف المشاركة في القضية؟\n\nمثلاً:\n- من هم الأطراف الرئيسيون؟\n- ما هي صفتهم القانونية؟",
        'facts': "حسناً، دعنا نتحدث عن وقائع القضية. هل يمكنك سرد الأحداث بالترتيب الزمني؟",
        'documents': "ما هي المستندات والأدلة المتوفرة لديك لدعم القضية؟",
        'completion_check': "دعنا نلخص المعلومات التي قدمتها حتى الآن. هل هناك أي معلومات إضافية تود إضافتها؟"
    }
    
    prompt = base_prompts.get(stage, "كيف يمكننا مساعدتك؟")
    
    gemini_prompt = f"""أنت مساعد قانوني ذكي يعمل مع زميلك للمساعدة في بناء القضية.
دورك هو:
1. فهم القضية من منظور عام
2. طرح الأسئلة التوضيحية المناسبة
3. التأكد من اكتمال المعلومات الأساسية

السياق الحالي:
{text}

السؤال/التوجيه:
{prompt}"""

    llama_prompt = f"""أنت مساعد قانوني متخصص في القانون الفلسطيني تعمل مع زميلك.
دورك هو:
1. تحليل الجوانب القانونية للقضية
2. التأكد من توافق المعلومات مع القانون
3. اقتراح النقاط القانونية المهمة

السياق الحالي:
{text}

السؤال/التوجيه:
{prompt}"""

    return {
        'gemini': gemini_prompt,
        'llama': llama_prompt
    }

@chat_bp.route('/chat')
def chat_page():
    """عرض صفحة المحادثة"""
    return render_template('chat/chat.html')

@chat_bp.route('/api/chat', methods=['POST'])
def chat():
    """معالجة رسائل المحادثة"""
    data = request.json
    message = data.get('message', '')
    stage = data.get('stage', 'initial')
    
    if not models:
        return jsonify({
            "status": "error",
            "message": "لا توجد نماذج متاحة"
        }), 400
    
    try:
        prompts = get_chat_prompt(stage, message)
        responses = []
        
        # الحصول على رد من Gemini
        if 'gemini' in models:
            try:
                gemini_response = models['gemini'].generate_content(prompts['gemini'])
                print(gemini_response)  # طباعة محتوى الاستجابة
                print(dir(gemini_response))  # طباعة الخصائص المتاحة في الكائن
                if gemini_response and hasattr(gemini_response, 'text'):
                    responses.append(f"🤖 Gemini يقول:\n{gemini_response.text}\n")
                elif hasattr(gemini_response, 'content'):
                    responses.append(f"🤖 Gemini يقول:\n{gemini_response.content}\n")
                else:
                    responses.append("🤖 Gemini لم يتمكن من تقديم رد.")
            except Exception as e:
                responses.append(f"🤖 Gemini حدث خطأ: {str(e)}")
        
        # الحصول على رد من Llama
        if 'llama' in models:
            try:
                completion = models['llama'].chat.completions.create(
                    messages=[{
                        "role": "user",
                        "content": prompts['llama']
                    }],
                    model="llama-3.3-70b-versatile",
                    temperature=1,
                    max_tokens=1024,
                    top_p=1,
                    stream=False,
                    stop=None
                )
                responses.append(f"🤖 Llama يقول:\n{completion['choices'][0]['message']['content']}\n")
            except Exception as e:
                responses.append(f"🤖 Llama حدث خطأ: {str(e)}")
        
        if responses:
            combined_response = "\n".join(responses)
            return jsonify({
                "status": "success",
                "result": combined_response
            })
        else:
            return jsonify({
                "status": "error",
                "message": "لم نتمكن من الحصول على رد من أي نموذج"
            }), 500
            
    except Exception as e:
        print(f"Error in chat: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500