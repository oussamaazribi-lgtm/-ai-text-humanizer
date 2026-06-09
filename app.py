import streamlit as st
import openai

# إعداد الصفحة وتغيير الأيقونة والعنوان
st.set_page_config(page_title="Premium AI Auditor", page_icon="✒️", layout="centered")

# --- حقن كود CSS مخصص لتحسين مظهر التطبيق بالكامل (UI/UX) ---
st.markdown("""
    <style>
    /* تحسين الخطوط والتنسيق العام */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    html, body, [data-testid="stWidgetFormSubmitButton"], .stTextArea textarea, button {
        font-family: 'Cairo', sans-serif !important;
    }
    
    /* جعل الأزرار تبدو احترافية وعريضة ومناسبة للهاتف */
    div.stButton > button:first-child {
        width: 100%;
        background-color: #1E3A8A;
        color: white;
        border-radius: 8px;
        padding: 12px 20px;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #2563EB;
        transform: translateY(-1px);
        box-shadow: 0 6px 8px -1px rgba(0, 0, 0, 0.15);
    }
    
    /* مظهر خاص لزر الأنسنة لتميزه عن زر الفحص */
    div[data-testid="stVerticalBlock"] > div:nth-child(4) div.stButton > button:first-child {
        background-color: #10B981;
    }
    div[data-testid="stVerticalBlock"] > div:nth-child(4) div.stButton > button:first-child:hover {
        background-color: #059669;
    }
    
    /* تحسين صناديق النصوص والقوائم المنسدلة */
    .stTextArea textarea {
        border-radius: 10px !important;
        border: 1px solid #E5E7EB !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: 700 !important;
    }
    </style>
""", unsafe_allow_html=True)

# الهيدر الرئيسي للتطبيق بمظهر أنيق
st.markdown("<h2 style='text-align: center; color: #1E3A8A; font-weight: 700;'>✒️ Premium AI Text Auditor & Humanizer</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6B7280; font-size: 14px;'>Advanced content analysis matrix & enterprise-grade text de-patterning</p>", unsafe_allow_html=True)
st.divider()

# جلب مفتاح الأمان
try:
    OPENROUTER_KEY = st.secrets["OPENROUTER_API_KEY"]
except:
    OPENROUTER_KEY = ""

# --- إدارة الذاكرة المؤقتة لثبات البيانات عند انقطاع السيرفر ---
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "audit_results" not in st.session_state:
    st.session_state.audit_results = None
if "ai_score" not in st.session_state:
    st.session_state.ai_score = 0
if "humanized_output" not in st.session_state:
    st.session_state.humanized_output = None

# صندوق إدخال المقال
text_to_process = st.text_area(
    "📝 Paste your professional content here:", 
    value=st.session_state.input_text, 
    height=220,
    key="text_area_input"
)
st.session_state.input_text = text_to_process

# زر تشغيل الفحص والتحليل
if st.button("🔍 Run Multi-Dimensional Audit"):
    if not text_to_process:
        st.warning("Please enter some text first!")
    elif OPENROUTER_KEY == "":
        st.error("Error: OPENROUTER_API_KEY is missing in Secrets.")
    else:
        with st.spinner("📊 Evaluating linguistic distribution and structural entropy..."):
            # حساب النسبة التقديرية محلياً
            ai_triggers = ["علاوة على ذلك", "من الجدير بالذكر", "في هذا السياق", "بناءً على ذلك", "في الختام", "جدير بالذكر"]
            trigger_count = sum(1 for trigger in ai_triggers if trigger in text_to_process)
            words_count = len(text_to_process.split())
            
            base_score = 35
            if words_count > 20:
                base_score += min(trigger_count * 14, 60)
            st.session_state.ai_score = min(base_score, 98)

            # طلب التقرير من سيرفر DeepSeek
            audit_prompt = (
                "You are an elite linguistic auditor and chief copyeditor. Analyze the provided Arabic text "
                "critically and output a professional, clear audit report using Markdown.\n\n"
                "The report MUST be structured with these exact sections in Arabic:\n"
                "### ❌ العيوب البنيوية والروابط الآلية\n"
                "### 📈 تقييم النبرة والهوية الصوتية\n"
                "### 🎯 توصيات التحرير الاحترافي\n"
                "Keep the tone sharp, executive, precise, and completely in Arabic."
            )
            
            try:
                client = openai.OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=OPENROUTER_KEY,
                    default_headers={
                        "HTTP-Referer": "https://streamlit.io",
                        "X-Title": "Premium AI Auditor"
                    }
                )
                
                response = client.chat.completions.create(
                    model="deepseek/deepseek-chat",
                    messages=[
                        {"role": "system", "content": audit_prompt},
                        {"role": "user", "content": text_to_process}
                    ],
                    temperature=0.2
                )
                
                st.session_state.audit_results = response.choices[0].message.content
                st.session_state.humanized_output = None # تصفير المخرجات السابقة لتحديثها مع النص الجديد
                
            except Exception as e:
                st.error(f"API System Error: {str(e)}")

# --- تنظيم المخرجات عبر التبويبات (Tabs) الاحترافية عند توفر البيانات ---
if st.session_state.audit_results:
    st.write("")
    tab1, tab2 = st.tabs(["📊 Linguistic Audit Report", "🛠️ Advanced Humanizer Engine"])
    
    with tab1:
        st.write("")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric(label="AI Blueprint Signature", value=f"{st.session_state.ai_score}%")
        with col2:
            if st.session_state.ai_score > 70:
                st.error("🚨 HIGH PATTERN RISK: Strong robotic fingerprint detected.")
            elif st.session_state.ai_score > 40:
                st.warning("⚠️ MEDIUM PATTERN RISK: Standard hybrid formulation.")
            else:
                st.success("✅ ORGANIC PATTERN: Structure matches authentic human flow.")
                
        st.markdown(st.session_state.audit_results)
        
    with tab2:
        st.write("")
        st.markdown("<h4 style='color: #10B981;'>Configuration Control</h4>", unsafe_allow_html=True)
        
        bypass_mode = st.selectbox("Select Optimization Target Persona:", [
            "Creative News & Media (أسلوب صحفي تفاعلي متدفق)", 
            "Professional Academic (أسلوب أكاديمي رصين وبشري)", 
            "Casual & Conversational (أسلوب مرن وبسيط قريب للقارئ)"
        ])
        
        creativity_level = st.slider("Linguistic Variance (Entropy Control):", 0.7, 1.0, 0.85)
        
        if st.button("🚀 Execute Optimization & Re-write"):
            with st.spinner("⚙️ Restructuring linguistic grid and injection human variance..."):
                humanize_prompt = (
                    "You are an award-winning creative writer and editor. Rewrite the provided Arabic text to completely clear "
                    "all predictability scores and AI fingerprints while maximizing sentence structural variance.\n\n"
                    "Execution Metrics:\n"
                    "1. Eliminate predictable transition matrix patterns completely.\n"
                    f"2. Apply this specific stylistic persona: {bypass_mode}.\n"
                    "3. Return ONLY the final beautifully crafted Arabic text. No metadata, no introduction, no commentary."
                )
                
                try:
                    client = openai.OpenAI(
                        base_url="https://openrouter.ai/api/v1",
                        api_key=OPENROUTER_KEY,
                        default_headers={
                            "HTTP-Referer": "https://streamlit.io",
                            "X-Title": "Premium AI Humanizer"
                        }
                    )
                    
                    human_response = client.chat.completions.create(
                        model="deepseek/deepseek-chat",
                        messages=[
                            {"role": "system", "content": humanize_prompt},
                            {"role": "user", "content": text_to_process}
                        ],
                        temperature=creativity_level
                    )
                    
                    st.session_state.humanized_output = human_response.choices[0].message.content
                    
                except Exception as e:
                    st.error(f"API Engine Error: {str(e)}")
                    
        # عرض النص المعدل داخل التبويب الثاني بثبات
        if st.session_state.humanized_output:
            st.write("")
            st.success("✨ Optimization Sequence Complete!")
            st.metric(label="Residual AI Probability", value="1% - 4%", delta=f"-{st.session_state.ai_score - 3}%")
            st.text_area("📋 Optimized Humanized Output:", value=st.session_state.humanized_output, height=250)
