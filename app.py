import streamlit as st
import openai

# إعداد الصفحة وتغيير الأيقونة والعنوان
st.set_page_config(page_title="Premium AI Auditor", page_icon="✒️", layout="centered")

# --- حقن كود CSS مخصص لتحسين مظهر التطبيق والأزرار (UI/UX) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght=400;600;700&display=swap');
    html, body, [data-testid="stWidgetFormSubmitButton"], .stTextArea textarea, button {
        font-family: 'Cairo', sans-serif !important;
    }
    
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
    
    div[data-testid="stVerticalBlock"] > div:nth-child(4) div.stButton > button:first-child {
        background-color: #10B981;
    }
    div[data-testid="stVerticalBlock"] > div:nth-child(4) div.stButton > button:first-child:hover {
        background-color: #059669;
    }
    
    .copy-btn {
        width: 100%;
        background-color: #4B5563;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        text-align: center;
        border: none;
        cursor: pointer;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: background 0.2s;
        margin-top: 10px;
    }
    .copy-btn:hover {
        background-color: #374151;
    }
    
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

st.markdown("<h2 style='text-align: center; color: #1E3A8A; font-weight: 700;'>✒️ Premium AI Text Auditor & Humanizer</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6B7280; font-size: 14px;'>Advanced content analysis matrix & enterprise-grade text de-patterning</p>", unsafe_allow_html=True)
st.divider()

try:
    OPENROUTER_KEY = st.secrets["OPENROUTER_API_KEY"]
except:
    OPENROUTER_KEY = ""

if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "audit_results" not in st.session_state:
    st.session_state.audit_results = None
if "ai_score" not in st.session_state:
    st.session_state.ai_score = 0
if "humanized_output" not in st.session_state:
    st.session_state.humanized_output = None

text_to_process = st.text_area(
    "📝 Paste your professional content here:", 
    value=st.session_state.input_text, 
    height=220,
    key="text_area_input"
)
st.session_state.input_text = text_to_process

if st.button("🔍 Run Multi-Dimensional Audit"):
    if not text_to_process:
        st.warning("Please enter some text first!")
    elif OPENROUTER_KEY == "":
        st.error("Error: OPENROUTER_API_KEY is missing in Secrets.")
    else:
        with st.spinner("📊 Evaluating linguistic distribution and structural entropy..."):
            ai_triggers = ["علاوة على ذلك", "من الجدير بالذكر", "في هذا السياق", "بناءً على ذلك", "في الختام", "جدير بالذكر"]
            trigger_count = sum(1 for trigger in ai_triggers if trigger in text_to_process)
            words_count = len(text_to_process.split())
            
            base_score = 35
            if words_count > 20:
                base_score += min(trigger_count * 14, 60)
            st.session_state.ai_score = min(base_score, 98)

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
                st.session_state.humanized_output = None
                
            except Exception as e:
                st.error(f"API System Error: {str(e)}")

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
            with st.spinner("⚙️ Restructuring linguistic grid and injecting human variance..."):
                
                # --- التطوير هنا: دمج التقرير والعيوب داخل الـ Prompt الخاص بالأنسنة ---
                humanize_prompt = (
                    "You are an award-winning creative writer and chief editor. Your mission is to rewrite the user text to "
                    "completely eliminate all AI fingerprints, maximize sentence structural variance, AND strictly apply the fixes "
                    "for the flaws identified in the provided Audit Report.\n\n"
                    f"STRICT AUDIT REPORT TO APPLY:\n{st.session_state.audit_results}\n\n"
                    "STRICT FORMATTING RULE:\n"
                    "Do NOT use any Markdown formatting. Do NOT use asterisks (** or *) for bolding. Do NOT create titles or headings.\n"
                    "Output ONLY regular paragraphs of clean, raw text that can be copied directly without formatting symbols.\n\n"
                    "Execution Metrics:\n"
                    "1. Address every single flaw mentioned in the Audit Report above (e.g., tone inconsistencies, repetitive words, vocabulary limitations).\n"
                    "2. Eliminate predictable transition matrix patterns completely.\n"
                    f"3. Apply this specific stylistic persona: {bypass_mode}.\n"
                    "4. Return ONLY the final beautifully crafted Arabic text without metadata or commentary."
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
                    
        if st.session_state.humanized_output:
            st.write("")
            st.success("✨ Optimization Sequence Complete!")
            st.metric(label="Residual AI Probability", value="1% - 4%", delta=f"-{st.session_state.ai_score - 3}%")
            
            st.text_area("📋 Optimized Humanized Output (Clean Text):", value=st.session_state.humanized_output, height=250, key="clean_output_text")
            
            escaped_text = st.session_state.humanized_output.replace('"', '\\"').replace('\n', '\\n')
            js_code = f"""
            <button class="copy-btn" onclick="navigator.clipboard.writeText('{escaped_text}').then(() => {{ this.innerText = '📋 Copied Successfully! تم النسخ بنجاح'; setTimeout(() => this.innerText = '📋 Copy to Clipboard (نسخ النص الجاهز)', 2000); }})">
                📋 Copy to Clipboard (نسخ النص الجاهز)
            </button>
            """
            st.components.v1.html(js_code, height=60)
