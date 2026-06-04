import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import json
import time

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# 1. 페이지 기본 설정 및 테마
st.set_page_config(page_title="SafeSpace — PTSD 회복 플랫폼", page_icon="🌿", layout="wide")

st.markdown("""
    <style>
    /* 메인 배경색 및 폰트 */
    .stApp { background-color: #FAF8F5; font-family: 'Noto Sans KR', sans-serif; }
    h1, h2, h3 { color: #4A5D4C !important; font-family: 'Noto Serif KR', serif; }
    p, div, span, label { color: #2D2D2A; }
    
    /* 사이드바 배경색 */
    [data-testid="stSidebar"] { background-color: #D1DBCE; }
    
    /* 🌿 오직 '사이드바' 메뉴에만 적용되는 완벽 커스텀 🌿 */
    
    /* 1. 메뉴 사이 간격 띄우기 */
    [data-testid="stSidebar"] div[data-testid="stRadio"] > div[role="radiogroup"] {
        gap: 12px !important; 
    }

    /* 2. 라디오 버튼의 베이스(Label)를 둥근 네모 박스로 만들기 */
    [data-testid="stSidebar"] div[data-testid="stRadio"] label {
        background-color: #829B85 !important;
        border-radius: 12px !important;
        padding: 14px 10px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        border: none !important;
        width: 100% !important;
    }

    /* 3. 마우스 올렸을 때 색상 변화 */
    [data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {
        background-color: #6a826d !important;
        transform: translateY(-2px);
    }

    /* 4. 🟢 현재 선택된 메뉴 (진한 초록색 #4A5D4C) */
    [data-testid="stSidebar"] div[data-testid="stRadio"] label[data-checked="true"],
    [data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) {
        background-color: #4A5D4C !important;
        box-shadow: 0 4px 10px rgba(74, 93, 76, 0.4) !important;
    }

    /* 5. 빨간색/회색 동그라미 아이콘 영구 삭제 */
    [data-testid="stSidebar"] div[data-testid="stRadio"] label > div:first-child,
    [data-testid="stSidebar"] div[data-testid="stRadio"] input[type="radio"] {
        display: none !important;
        opacity: 0 !important;
        width: 0px !important;
        height: 0px !important;
        margin: 0px !important;
        padding: 0px !important;
        position: absolute !important;
    }

    /* 6. 메뉴 텍스트 정렬 및 스타일 */
    [data-testid="stSidebar"] div[data-testid="stRadio"] label div, 
    [data-testid="stSidebar"] div[data-testid="stRadio"] label p {
        color: white !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        margin: 0 !important;
        text-align: center !important;
        width: 100% !important;
    }
    
    /* 본문 일반 버튼 스타일 */
    div.stButton > button { background-color: #4A5D4C; color: white; border-radius: 30px; border: none; padding: 0.6rem 2rem; font-weight: bold; }
    div.stButton > button:hover { background-color: #829B85; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. 사이드바 네비게이션
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 2rem;'>Safe<span style='color: #B59B6D; font-style: italic;'>Space</span></h1>", unsafe_allow_html=True)
    st.write("---")
    page = st.radio("메뉴 이동", ["홈", "PCL-5 심리검사", "나만의 안식처 (CBT)", "EMDR 세션", "VR 노출치료"], label_visibility="collapsed")

# ---------------------------------------------------------
# 페이지 1: 홈 
# ---------------------------------------------------------
if page == "홈":
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown("<div style='color:#829B85; font-weight:600; letter-spacing:0.1em; font-size:0.8rem; margin-bottom:1rem;'>PTSD 회복 플랫폼</div>", unsafe_allow_html=True)
        st.markdown("<h1 style='font-size: 3.5rem; font-weight: 300; line-height: 1.3;'>당신의 속도로,<br><em style='color:#4A5D4C; font-style:italic; font-weight:500;'>안전한 공간</em>에서<br><strong style='font-weight:600;'>회복을 시작하세요</strong></h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#5E5E56; font-size:1.1rem; line-height:1.8; margin-top:2rem;'>비용 부담 없이, 시공간 제약 없이. 검증된 PTSD 치료법을 디지털로 만나보세요.<br>AI 기반 인지행동치료, EMDR, VR 노출치료를 한 곳에서.</p>", unsafe_allow_html=True)
        
    with col2:
        # index.html의 통계 카드 재현
        st.markdown("""
        <div style="background: rgba(247,244,238,0.92); border: 1px solid rgba(122,158,126,0.25); border-radius: 16px; padding: 2rem; box-shadow: 0 8px 32px rgba(0,0,0,0.08); margin-top: 2rem;">
            <div style="font-size: 2.5rem; color: #4A5D4C; font-weight: bold;">60–70%</div>
            <div style="color: #5E5E56; margin-bottom: 1.5rem;">CBT 증상 완화율</div>
            <div style="display: flex; align-items: center; gap: 0.6rem;">
                <div style="width: 10px; height: 10px; border-radius: 50%; background: #829B85;"></div>
                <span style="color: #4A5D4C; font-weight: bold;">AI 기반 CBT 세션 진행 중</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    st.markdown("<h2 style='text-align:center;'>검증된 치료법을 <em style='color:#4A5D4C;'>디지털로</em> 구현했습니다</h2>", unsafe_allow_html=True)
    st.write("")
    
    c1, c2, c3, c4 = st.columns(4)
    
    def custom_card(title, text):
        return f"""
        <div style="background-color: #F0F4F1; border: 1px solid #D1DBCE; padding: 1.5rem; border-radius: 16px; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
            <div style="color: #4A5D4C; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.8rem;">{title}</div>
            <div style="color: #5E5E56; font-size: 0.95rem; line-height: 1.6; word-break: keep-all;">{text}</div>
        </div>
        """

    c1.markdown(custom_card("01 심리검사", "PCL-5 설문을 통해 현재 증상을 파악합니다."), unsafe_allow_html=True)
    c2.markdown(custom_card("02 인지행동치료", "AI 채팅을 통해 부정적 사고 패턴을 수정합니다."), unsafe_allow_html=True)
    c3.markdown(custom_card("03 EMDR", "안구운동을 통해 외상 기억을 재처리합니다."), unsafe_allow_html=True)
    c4.markdown(custom_card("04 VR 노출치료", "가상 환경에 노출하여 공포 반응을 감소시킵니다."), unsafe_allow_html=True)

# ---------------------------------------------------------
# 페이지 2: PCL-5 심리검사
# ---------------------------------------------------------
elif page == "PCL-5 심리검사":
    st.markdown("<div style='text-align:center;'><div style='color:#829B85; font-weight:600; letter-spacing:0.1em;'>PTSD ASSESSMENT</div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center;'>나의 마음 상태를<br>정밀하게 확인해보세요</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#5E5E56;'>지난 한 달 동안 당신을 괴롭혔던 스트레스 경험을 떠올리며 답변해 주세요.</p></div>", unsafe_allow_html=True)
    st.write("---")
    
    questions = [
        "[재경험] 그 스트레스 경험에 대한 불쾌하고 기억하고 싶지 않은 기억이 반복적으로 떠오릅니까?",
        "[재경험] 그 스트레스 경험에 대한 악몽을 반복해서 꾸십니까?",
        "[재경험] 별안간 그 스트레스 경험을 실제로 다시 겪는 것처럼 느껴지거나 행동하게 됩니까?",
        "[재경험] 뭔가 그 스트레스 경험을 다시 떠오르게 한다면, 매우 불쾌한 감정을 느끼십니까?",
        "[재경험] 뭔가 그 스트레스 경험을 다시 떠오르게 한다면, 격한 신체 반응이 나타납니까?",
        "[회피] 그 스트레스 경험과 관련된 기억이나 생각 또는 감정을 피하십니까?",
        "[회피] 그 스트레스 경험을 떠오르게 하는 외부 상황을 피하십니까?",
        "[인지/정서] 그 스트레스 경험의 중요한 부분을 기억하기 어렵습니까?",
        "[인지/정서] 자기 자신, 다른 사람들, 혹은 세상에 대해 매우 부정적인 신념을 가지고 있습니까?",
        "[인지/정서] 그 경험에 대하여 자기 자신 탓이나 다른 사람 탓을 하고 있습니까?",
        "[인지/정서] 공포, 혐오, 분노, 죄책감, 수치심 같은 매우 부정적인 감정이 있습니까?",
        "[인지/정서] 이전에 자주 즐겼던 활동들에 대한 흥미를 잃어버렸습니까?",
        "[인지/정서] 다른 사람들과 동떨어졌거나 단절되었다고 느끼십니까?",
        "[인지/정서] 긍정적인 감정을 느끼는 것이 어렵습니까?",
        "[각성/반응] 과민 행동, 분노 폭발 또는 공격적인 행동을 하십니까?",
        "[각성/반응] 너무 많은 위험을 감수하거나 자신에게 해가 될 수 있는 위험한 행동을 하십니까?",
        "[각성/반응] 조금도 방심하지 않으려고 하거나 주변을 감시하거나 혹은 경계하게 되십니까?",
        "[각성/반응] 조마조마한 느낌이 들거나 쉽게 깜짝 놀라십니까?",
        "[각성/반응] 집중하기가 어렵습니까?",
        "[각성/반응] 잠들기가 어렵거나 중간에 깨십니까?"
    ]
    
    scores = []
    for i, q in enumerate(questions):
        st.markdown(f"**{i+1}. {q}**")
        score = st.radio(f"질문 {i+1} 답변", options=[0, 1, 2, 3, 4], 
                         format_func=lambda x: ["아님 (0)", "약간 (1)", "보통 (2)", "많이 (3)", "아주 (4)"][x], 
                         horizontal=True, key=f"q{i}", label_visibility="collapsed")
        scores.append(score)
        st.write("") 
    
    st.write("---")
    if st.button("검사 결과 확인하기", use_container_width=True):
        total = sum(scores)
        st.markdown(f"<h1 style='text-align:center; font-size:4rem;'>{total}점</h1>", unsafe_allow_html=True)
        if total >= 33:
            st.error("🚨 **고위험군:** PCL-5 진단 기준(33점)을 초과했습니다. 전문가와 상담을 추천합니다.")
        else:
            st.success("🌱 **양호:** 현재 증상 수치가 낮습니다. 지속적인 마음 관리를 유지해 보세요.")

# ---------------------------------------------------------
# 페이지 3: 나만의 안식처 CBT (cbt.html + app.py 완벽 재현)
# ---------------------------------------------------------
elif page == "나만의 안식처 (CBT)":
    st.markdown("<h2 style='text-align:center;'>나만의 안식처 🌿</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#5E5E56;'>🔒 네가 여기서 한 모든 이야기는 절대 남지 않고 완벽하게 보호돼.</p>", unsafe_allow_html=True)
    
    panic_mode = st.toggle("🙈 화면 숨기기 (패닉 버튼)")
    
    if panic_mode:
        st.error("### 화면이 안전하게 보호되고 있습니다.\n\n주변이 안전해지면 다시 토글을 꺼서 대화로 돌아오세요.")
    else:
        if "cbt_history" not in st.session_state:
            st.session_state.cbt_history = [{"role": "assistant", "content": "안녕! 오늘 하루는 어땠어? 안전하게 지켜줄 테니까, 무슨 일이든 편하게 다 얘기해 줘."}]
        
        for msg in st.session_state.cbt_history:
            st.chat_message(msg["role"]).write(msg["content"])
        
        if user_input := st.chat_input("편하게 속마음을 적어주세요..."):
            st.chat_message("user").write(user_input)
            
            # Gemini API 호출 (app.py의 프롬프트 로직 완벽 이식)
            conversation_context = ""
            for chat in st.session_state.cbt_history:
                role = "친구(사용자)" if chat['role'] == 'user' else "나(AI)"
                conversation_context += f"{role}: {chat['content']}\n"
            
            # 네가 준 10대 사례 + 5단계 프롬프트 원본
            prompt = f"""
            [Identity]
            당신은 과거의 상처나 트라우마(PTSD)로 힘들어하는 사용자를 곁에서 진심으로 위로하고 챙겨주는 '가장 친하고 믿음직한 오랜 친구'입니다. 의사나 전문가처럼 딱딱하게 굴지 말고, 언제든 기대어 쉴 수 있는 편안한 절친처럼 다가가세요.

            [PTSD Case Knowledge Base: 다채로운 맞춤형 공감을 위한 10가지 사례집]
            아래 10가지 사례를 바탕으로 환자의 상황을 유추하여, 뻔한 질문 대신 상황에 맞는 매우 세밀하고 입체적인 질문을 던지세요. 
            ※ 핵심 원칙: 환자가 어떤 사례에 속하든 대화 중간에 "여기는 완벽하게 비밀이 지켜지는 우리 둘만의 공간이니까, 누구에게도 말 못 할 이야기라도 눈치 보지 말고 나한테는 다 쏟아내도 돼"라는 뉘앙스를 자연스럽게 풍겨서, 프라이버시에 대한 걱정을 없애고 솔직하게 얘기할 수 있도록 유도하세요.
            1. 대형 재난/사고: 브레이크 소리, 타는 냄새, 밀폐된 공간 등에서 재경험.
            2. 강력 범죄 피해: 어두운 골목, 낯선 사람의 발소리 등에 대한 극심한 과각성.
            3. 직업적 트라우마(소방관/경찰/의료진): 타인을 구하지 못했다는 끔찍한 죄책감과 무기력증.
            4. 아동기 학대/가정 폭력: 누군가 큰 소리를 내거나 물건 떨어지는 소리에 이성이 멈추고 얼어붙음.
            5. 전쟁/전투 트라우마: 폭죽 소리나 헬기 소리 등 특정 소음에 대한 과민 반응 및 악몽.
            6. 학교 폭력 및 심각한 따돌림: 다수의 시선이 쏠리거나 귓속말을 볼 때 극도의 고립감과 공포.
            7. 데이트 폭력 및 가스라이팅: 지나친 연락 집착이나 통제하려는 말투에 숨이 막히고 자책함.
            8. 상실/사별 트라우마: 사랑하는 사람과 관련된 장소/물건을 마주쳤을 때의 슬픔과 플래시백.
            9. 의료 사고 및 중증 질환: 병원 특유의 냄새, 기계 알림음, 조명 환경에서 호흡 곤란을 겪음.
            10. 사이버 불링 및 디지털 범죄: 특정 메신저 알림음이 울리거나 화면만 봐도 세상과 단절되고 싶어 함.

            [Mission: 자연스러운 마음 챙김 5단계 안내]
            1단계: 상황 파악
            2단계: 감정 공감
            3단계: 자동적 사고 찾기
            4단계: 근거 찾기
            5단계: 대안적 사고 유도

            [🚨 CRUCIAL RULE 1: 친구가 "막막해", "모르겠어"라고 할 때]
            생각을 강요하지 말고, 그라운딩 기법을 다정하게 제안하세요.

            [🚨 CRUCIAL RULE 2: 작별 인사와 철저한 비밀 보장 (Ending Rule)]
            마무리할 때는 질문으로 끝내지 말고 훈훈하게 마침표로 끝내세요.

            [이전 대화 맥락]
            {conversation_context}

            [현재 친구(사용자)의 말]
            "{user_input}"
            """
            
            with st.spinner("친구가 타자를 치고 있어요..."):
                try:
                    response = model.generate_content(
                        prompt,
                        safety_settings={
                            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                        }
                    )
                    reply = response.text
                except Exception as e:
                    reply = "미안해, 잠시 생각하느라 대답이 늦었어. 다시 말해줄래?"
            
            st.session_state.cbt_history.append({"role": "user", "content": user_input})
            st.session_state.cbt_history.append({"role": "assistant", "content": reply})
            st.chat_message("assistant").write(reply)
            st.rerun()

        st.write("---")
        if st.button("📝 대화 요약하여 내 기기에 저장하기"):
            if len(st.session_state.cbt_history) < 3:
                st.warning("우리가 나눈 이야기가 아직 조금 부족한 것 같아. 조금 더 마음을 털어놓아 볼까?")
            else:
                with st.spinner("오늘 대화한 내용을 정리 중이야..."):
                    summary_prompt = f"""
                    다음 대화 기록을 분석해서 전문적인 'CBT 사고기록지'를 작성해줘.
                    반드시 다음 6개의 키값을 가진 JSON 구조여야 해:
                    {{"situation": "", "emotion": "", "automatic_thought": "", "evidence": "", "alternative_thought": "", "result": ""}}
                    대화 기록: {st.session_state.cbt_history}
                    """
                    try:
                        res = model.generate_content(summary_prompt, generation_config={"response_mime_type": "application/json"})
                        data = json.loads(res.text.strip())
                        
                        fileContent = "[🌿 오늘의 마음 정리 (CBT 사고기록지)]\n\n"
                        fileContent += f"상황: {data.get('situation', '')}\n\n"
                        fileContent += f"감정: {data.get('emotion', '')}\n\n"
                        fileContent += f"스쳐간 생각: {data.get('automatic_thought', '')}\n\n"
                        fileContent += f"증거 찾기: {data.get('evidence', '')}\n\n"
                        fileContent += f"대안적 생각: {data.get('alternative_thought', '')}\n\n"
                        fileContent += f"결과: {data.get('result', '')}"
                        
                        st.download_button("텍스트 파일 다운로드", fileContent, file_name="내마음일기.txt")
                        st.success("요약이 완료되었습니다! 위 버튼을 눌러 다운로드하세요.")
                    except Exception as e:
                        st.error("정리하는 중에 에러가 발생했어.")

# ---------------------------------------------------------
# 페이지 4: EMDR 세션 (emdr.html 완벽 재현 + 오디오 연동)
# ---------------------------------------------------------
elif page == "EMDR 세션":
    st.markdown("<h2 style='text-align:center;'>EMDR 세션</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#5E5E56;'>💡 검은색 화면을 한 번 클릭하면 세션이 시작됩니다. 눈으로 점을 따라가세요.</p>", unsafe_allow_html=True)
    
    # 음성 가이드 오디오 (Streamlit 네이티브 오디오 플레이어로 재생)
    st.audio("ElevenLabs_2026-05-31T23_23_51_Sarah — Calm and kind_pvc_sp90_s50_sb75_se0_b_m2.mp3", format="audio/mp3")

    # 네가 짠 p5.js 코드를 하나도 안 건드리고 그대로 Iframe으로 이식
    emdr_html = """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
    <style>
        body { margin: 0; display: flex; justify-content: center; align-items: center; background-color: #FAF8F5; }
        #canvas-container { border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); overflow: hidden; cursor: pointer; }
    </style>
    <div id="canvas-container"></div>
    <script>
        let centerX, centerY;
        let range = 180;
        let speed = 0.035;
        let isRunning = false; 
        let phaseFrame = 0;
        let workDuration = 600;
        let restDuration = 240;
        let canPlayLeft = true;
        let canPlayRight = true;
        let hasStarted = false; 
        let audioCtx;

        function setup() {
            let canvas = createCanvas(800, 400);
            canvas.parent('canvas-container');
            centerX = width / 2;
            centerY = height / 2;
        }

        function draw() {
            background(10, 40); 
            if (!hasStarted) {
                fill(255); noStroke(); textAlign(CENTER, CENTER); textSize(16);
                text("화면을 클릭하여 시작하세요", centerX, centerY);
                return; 
            }
            let x = centerX;
            if (isRunning) {
                x = centerX + sin(frameCount * speed) * range;
                if (x < centerX - range + 5 && canPlayLeft) { playNativeBeep(-1); canPlayLeft = false; canPlayRight = true; }
                if (x > centerX + range - 5 && canPlayRight) { playNativeBeep(1); canPlayRight = false; canPlayLeft = true; }
            }
            noStroke(); fill(255); ellipse(x, centerY, 25, 25);
            stroke(255, 30); line(centerX, 0, centerX, height);

            phaseFrame++;
            if (isRunning && phaseFrame > workDuration) { isRunning = false; phaseFrame = 0; } 
            else if (!isRunning && phaseFrame > restDuration) { isRunning = true; phaseFrame = 0; }
        }

        function playNativeBeep(panValue) {
            if (!audioCtx) return; 
            let osc = audioCtx.createOscillator();
            let gainNode = audioCtx.createGain();
            let panner = audioCtx.createStereoPanner();
            osc.type = 'sine'; osc.frequency.value = 600; 
            panner.pan.value = panValue; 
            gainNode.gain.setValueAtTime(0, audioCtx.currentTime);
            gainNode.gain.linearRampToValueAtTime(0.4, audioCtx.currentTime + 0.01);
            gainNode.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.1);
            osc.connect(panner); panner.connect(gainNode); gainNode.connect(audioCtx.destination);
            osc.start(); osc.stop(audioCtx.currentTime + 0.15); 
        }

        function mousePressed() {
            if (mouseX > 0 && mouseX < width && mouseY > 0 && mouseY < height) {
                if (!hasStarted) {
                    let AudioContext = window.AudioContext || window.webkitAudioContext;
                    audioCtx = new AudioContext();
                    hasStarted = true; isRunning = true;
                }
            }
        }
    </script>
    """
    components.html(emdr_html, height=450)

# ---------------------------------------------------------
# 페이지 5: VR 노출치료 (vr.html 완벽 재현 + 오디오 버튼)
# ---------------------------------------------------------
elif page == "VR 노출치료":
    st.markdown("<h2 style='text-align:center;'>모바일 VR 노출 치료</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#5E5E56;'>자신의 스마트폰을 이용해 가상 환경을 탐색하며 공포 반응을 점진적으로 줄여나갑니다.</p>", unsafe_allow_html=True)
    st.write("---")
    
    vr_data = {
        "밀폐/공간": [
            {"level": "Lv.1", "name": "넓은 실내", "link": "https://skybox.blockadelabs.com/e/78c7cd96d3091522e826c1829954b847", "audio": None},
            {"level": "Lv.2", "name": "좁은 복도", "link": "https://skybox.blockadelabs.com/e/406da99640f2fb0b4bc07a25eee1c2d1", "audio": None},
            {"level": "Lv.3", "name": "엘리베이터", "link": "https://skybox.blockadelabs.com/e/db3f0065617fcda654a395a7486b7dab", "audio": None}
        ],
        "소음/충돌": [
            {"level": "Lv.1", "name": "조용한 거리", "link": "https://skybox.blockadelabs.com/e/3fd1de422876b1b8fff3c4eae5391695", "audio": "noise_lv.1.wav"},
            {"level": "Lv.2", "name": "교통 소음", "link": "https://skybox.blockadelabs.com/e/fdb63f2e817aad68a31529c52a6b40a1", "audio": "noise_lv.2.wav"},
            {"level": "Lv.3", "name": "사고 현장음", "link": "https://skybox.blockadelabs.com/e/5eb5116c64f7258aa066b19c57e4156f", "audio": "noise_lv.3.wav"}
        ],
        "군중/시선": [
            {"level": "Lv.1", "name": "공원 산책", "link": "https://skybox.blockadelabs.com/e/9818f888aefc0ab4a7ed7cc8eb9ea81c", "audio": None}, 
            {"level": "Lv.2", "name": "붐비는 카페", "link": "https://skybox.blockadelabs.com/e/12716360bc8b1d5f7af337b0b94740ca", "audio": None},
            {"level": "Lv.3", "name": "지하철 혼잡", "link": "https://skybox.blockadelabs.com/e/c243023d72c34eba6edf5ad574072fd3", "audio": None}
        ],
        "의료/병원": [
            {"level": "Lv.1", "name": "병원 외관", "link": "https://skybox.blockadelabs.com/e/33f4b5dfe6338eb5dd289fc89b8f6585", "audio": None},
            {"level": "Lv.2", "name": "대기실", "link": "https://skybox.blockadelabs.com/e/620593fb840199b29aae9070abbc2b5e", "audio": None},
            {"level": "Lv.3", "name": "응급실", "link": "https://skybox.blockadelabs.com/e/340cabf7a7da0ca95b7634b102c0d127", "audio": None}
        ]
    }
    
    category = st.selectbox("진행할 노출 훈련 카테고리를 선택하세요", list(vr_data.keys()))
    st.write("---")
    
    for item in vr_data[category]:
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {item['level']} - {item['name']}")
                if item['audio']:
                    st.audio(item['audio'], format="audio/wav")
            with col2:
                st.write("")
                st.link_button("🚪 VR 입장하기", item["link"], use_container_width=True)
        st.write("---")