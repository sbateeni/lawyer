from groq import Groq
import google.generativeai as genai
import os
from dotenv import load_dotenv

# تحميل المتغيرات البيئية
load_dotenv()


def test_gemini() -> bool:
    """اختبار نموذج Gemini"""
    try:
        # تهيئة النموذج
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        model = genai.GenerativeModel('gemini-pro')

        # نص الاختبار
        test_text = """
        قام المدعي برفع دعوى ضد المدعى عليه بتاريخ 1/1/2024 يطالب فيها بمبلغ 10000 دينار
        قيمة قرض حسن تم منحه للمدعى عليه بتاريخ 1/6/2023 ولم يقم بسداده رغم المطالبات المتكررة
        """

        # إرسال الطلب
        response = model.generate_content(test_text)

        print("\n=== اختبار Gemini ===")
        print("النتيجة:", response.text)
        print("تم الاختبار بنجاح!")
        return True

    except Exception as e:
        print("خطأ في اختبار Gemini:", str(e))
        return False


def test_groq() -> bool:
    """اختبار نموذج Groq"""
    try:
        # تهيئة النموذج
        client = Groq(api_key=os.getenv('GROQ_API_KEY'))

        # نص الاختبار
        test_text = """
        قام المدعي برفع دعوى ضد المدعى عليه بتاريخ 1/1/2024 يطالب فيها بمبلغ 10000 دينار
        قيمة قرض حسن تم منحه للمدعى عليه بتاريخ 1/6/2023 ولم يقم بسداده رغم المطالبات المتكررة
        """

        # إرسال الطلب
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "user",
                "content": test_text
            }],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None
        )

        print("\n=== اختبار Groq ===")
        print("النتيجة:", completion.choices[0].message.content)
        print("تم الاختبار بنجاح!")
        return True

    except Exception as e:
        print("خطأ في اختبار Groq:", str(e))
        return False


if __name__ == "__main__":
    print("بدء اختبار النماذج...")

    gemini_result = test_gemini()
    groq_result = test_groq()

    print("\n=== نتائج الاختبار ===")
    print("Gemini:", "نجاح" if gemini_result else "فشل")
    print("Groq:", "نجاح" if groq_result else "فشل")
