import base64
import hashlib
import os
import re
import shutil
import tempfile

import streamlit as st
import streamlit.components.v1 as components

import engine

APP_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(APP_DIR, "assets")
BACKGROUND_PATH = os.path.join(ASSET_DIR, "background.svg")
MUSIC_PATH = os.path.join(ASSET_DIR, "music.wav")

st.set_page_config(
    page_title="Phiếu Nhận Xét Học Viên | CIE VIETNAM",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)


def _b64_file(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("ascii")
    except Exception:
        return ""


BG_B64 = _b64_file(BACKGROUND_PATH)
MUSIC_B64 = _b64_file(MUSIC_PATH)
BG_URL = f"data:image/svg+xml;base64,{BG_B64}" if BG_B64 else ""

# =========================================================================
# CSS - giao dien app
# =========================================================================
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{ font-family: 'Be Vietnam Pro', sans-serif; }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    .stApp {{ background: linear-gradient(160deg, #f4f7ff 0%, #eef2ff 45%, #fff7f7 100%); }}
    .block-container {{ max-width: 900px; padding-top: 1.5rem; padding-bottom: 2rem; }}

    .waiting-screen {{
        min-height: 640px; border-radius: 28px; overflow: hidden; position: relative;
        display:flex; align-items:center; justify-content:center; text-align:center;
        background-image: linear-gradient(135deg, rgba(8,25,45,.82), rgba(31,78,121,.70), rgba(128,42,42,.68)), url('{BG_URL}');
        background-size: cover; background-position:center;
        box-shadow: 0 22px 70px rgba(16,42,67,.28);
        color:white;
    }}
    .waiting-content {{ padding: 40px 24px; max-width: 680px; position:relative; z-index:2; }}
    .waiting-logo {{ font-size: 64px; line-height:1; margin-bottom: 18px; filter: drop-shadow(0 5px 18px rgba(0,0,0,.25)); }}
    .waiting-badge {{ display:inline-block; padding:7px 16px; border:1px solid rgba(255,255,255,.35); border-radius:999px; background:rgba(255,255,255,.12); font-size:.8rem; font-weight:700; letter-spacing:.8px; }}
    .waiting-title {{ font-size:2.5rem; font-weight:800; margin:18px 0 10px; letter-spacing:.2px; }}
    .waiting-sub {{ font-size:1.05rem; line-height:1.65; opacity:.92; margin:0 auto 28px; }}
    .music-note {{ margin-top:16px; font-size:.82rem; opacity:.78; }}

    .hero {{
        background: linear-gradient(120deg, #173b5c 0%, #1f4e79 55%, #9b3a3a 130%);
        border-radius: 22px; padding: 30px; margin-bottom: 20px;
        box-shadow: 0 14px 40px rgba(31,78,121,.20); text-align:center; color:white;
        position:relative; overflow:hidden;
    }}
    .hero::before {{ content:""; position:absolute; width:190px; height:190px; right:-70px; top:-75px; border-radius:50%; background:rgba(255,255,255,.11); }}
    .hero h1 {{ font-size:1.9rem; font-weight:800; margin:8px 0 5px; }}
    .hero p {{ margin:0; opacity:.9; font-size:.95rem; }}
    .badge {{ display:inline-block; background:rgba(255,255,255,.15); border:1px solid rgba(255,255,255,.3); border-radius:999px; padding:5px 14px; font-size:.76rem; font-weight:700; letter-spacing:.5px; }}

    .stat-row {{ display:flex; gap:12px; margin-bottom:18px; }}
    .stat-card {{ flex:1; background:white; border:1px solid #e9edf5; border-radius:15px; padding:14px 10px; text-align:center; box-shadow:0 5px 18px rgba(31,78,121,.06); }}
    .stat-card .num {{ font-size:1.45rem; font-weight:800; color:#1f4e79; line-height:1.1; }}
    .stat-card .lbl {{ font-size:.76rem; color:#6b7280; margin-top:4px; }}

    .upload-card, .result-card {{ background:white; border:1px solid #e9edf5; border-radius:18px; padding:20px; margin-bottom:16px; box-shadow:0 7px 24px rgba(31,78,121,.07); }}
    .result-card {{ border-color:#b9dfc7; background:linear-gradient(145deg,#ffffff,#f3fff7); }}
    .result-title {{ font-size:1.3rem; font-weight:800; color:#197044; margin-bottom:4px; }}
    .result-sub {{ color:#52606d; font-size:.92rem; }}

    div[data-testid="stFileUploader"] section {{ border:2px dashed #94b3d6 !important; border-radius:14px !important; background:#f7faff !important; }}
    div[data-testid="stFileUploader"] section:hover {{ border-color:#1f4e79 !important; background:#eef4fc !important; }}
    .stButton > button, .stDownloadButton > button {{ border-radius:11px !important; font-weight:700 !important; min-height:44px; }}
    .stButton > button[kind="primary"] {{ background:linear-gradient(120deg,#1f4e79,#2f6fb0) !important; border:none !important; color:white !important; }}
    .success-button .stButton > button {{ background:linear-gradient(120deg,#168653,#2ca56d) !important; color:white !important; border:none !important; }}

    .history-item {{ display:flex; justify-content:space-between; gap:12px; padding:9px 4px; border-bottom:1px solid #f0f2f6; font-size:.9rem; }}
    .history-item:last-child {{ border-bottom:none; }}
    .history-item .cnt {{ background:#e8f0fe; color:#1f4e79; border-radius:999px; padding:2px 9px; font-weight:700; font-size:.78rem; white-space:nowrap; }}
    .footer-note {{ text-align:center; color:#9aa3b2; font-size:.78rem; margin-top:22px; }}

    @media (max-width: 650px) {{
        .waiting-screen {{ min-height:560px; }}
        .waiting-title {{ font-size:2rem; }}
        .stat-row {{ gap:7px; }}
        .stat-card .num {{ font-size:1.2rem; }}
        .stat-card .lbl {{ font-size:.68rem; }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================================
# State
# =========================================================================
def init_state():
    defaults = {
        "started": False,
        "uploader_key": 0,
        "processed_token": None,
        "auto_download_token": None,
        "celebrate_token": None,
        "result_zip": None,
        "result_filename": None,
        "result_source": None,
        "result_count": 0,
        "history": [],
        "total_students": 0,
        "logo_path": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()

if not st.session_state["logo_path"]:
    tmp_dir = tempfile.mkdtemp()
    logo_path = os.path.join(tmp_dir, "logo.png")
    with open(logo_path, "wb") as f:
        f.write(base64.b64decode(engine.DEFAULT_LOGO_B64))
    st.session_state["logo_path"] = logo_path

engine.COMPANY_LOGO_PATH = st.session_state["logo_path"]


def safe_name(value):
    return re.sub(r'[\\/:*?"<>|]', "_", str(value)).strip()


def build_zip_for_students(students):
    tmp_dir = tempfile.mkdtemp()
    used_names = set()
    for student in students:
        doc = engine.build_phieu(student)
        lop = safe_name(student["class_info"].get("lop") or student["class_info"].get("sheet") or "Lop")
        ten = safe_name(student["name"])
        base = f"{lop}__{ten}"
        fname = base
        i = 2
        while fname in used_names:
            fname = f"{base}_{i}"
            i += 1
        used_names.add(fname)
        doc.save(os.path.join(tmp_dir, fname + ".docx"))

    zip_base = os.path.join(tempfile.mkdtemp(), "PhieuNhanXet")
    zip_path = shutil.make_archive(zip_base, "zip", tmp_dir)
    with open(zip_path, "rb") as f:
        return f.read()


def trigger_browser_download(filename, data_bytes):
    """Best-effort automatic browser download; manual button remains available."""
    b64 = base64.b64encode(data_bytes).decode("ascii")
    safe_filename = safe_name(filename).replace('"', "_")
    html = f"""
    <html><body>
    <script>
    try {{
        const b64data = "{b64}";
        const byteChars = atob(b64data);
        const byteNumbers = new Array(byteChars.length);
        for (let i = 0; i < byteChars.length; i++) byteNumbers[i] = byteChars.charCodeAt(i);
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], {{type: "application/zip"}});
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "{safe_filename}";
        document.body.appendChild(a);
        a.click();
        a.remove();
        setTimeout(() => URL.revokeObjectURL(url), 5000);
    }} catch (e) {{ console.log(e); }}
    </script>
    </body></html>
    """
    components.html(html, height=0, width=0)


def music_player():
    if not MUSIC_B64:
        return
    components.html(
        f"""
        <div style='font-family:Arial,sans-serif;text-align:center;margin:6px 0 8px'>
          <div style='font-size:12px;color:#6b7280;margin-bottom:4px'>🎵 Nhạc nền · nếu trình duyệt không tự phát, bấm Play</div>
          <audio controls loop preload='auto' style='width:min(420px,95%);height:34px'>
            <source src='data:audio/wav;base64,{MUSIC_B64}' type='audio/wav'>
          </audio>
        </div>
        """,
        height=70,
        width=700,
    )


# =========================================================================
# Màn hình chờ
# =========================================================================
if not st.session_state["started"]:
    st.markdown(
        """
        <div class="waiting-screen">
          <div class="waiting-content">
            <div class="waiting-logo">🎓</div>
            <div class="waiting-badge">CIE VIETNAM · AUTO REPORT TOOL</div>
            <div class="waiting-title">Phiếu Nhận Xét Học Viên</div>
            <p class="waiting-sub">Tự động phân tích dữ liệu điểm, tạo nhận xét phù hợp và xuất toàn bộ phiếu Word cho từng học viên.</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("🚀  BẮT ĐẦU", type="primary", use_container_width=True):
            st.session_state["started"] = True
            st.rerun()
    music_player()
    st.markdown("<div class='footer-note'>Thiết kế để giáo viên thao tác nhanh: upload → xử lý → tải phiếu → thêm lớp tiếp theo.</div>", unsafe_allow_html=True)
    st.stop()

# =========================================================================
# Header app
# =========================================================================
st.markdown(
    """
    <div class="hero">
      <div class="badge">🎓 CIE VIETNAM · AUTO REPORT TOOL</div>
      <h1>Tạo Phiếu Nhận Xét & Đánh Giá Học Viên</h1>
      <p>Upload file điểm → hệ thống tự động phân tích → tạo Word → tải ZIP về máy.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="stat-row">
      <div class="stat-card"><div class="num">{len(st.session_state['history'])}</div><div class="lbl">Lớp đã xử lý</div></div>
      <div class="stat-card"><div class="num">{st.session_state['total_students']}</div><div class="lbl">Phiếu đã tạo</div></div>
      <div class="stat-card"><div class="num">∞</div><div class="lbl">Lớp có thể xử lý</div></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================================
# Upload + xử lý tự động
# =========================================================================
st.markdown('<div class="upload-card">', unsafe_allow_html=True)
st.markdown("### 📁 1. Upload dữ liệu lớp")
st.caption("Chọn file Excel .xlsx. Sau khi tải lên, hệ thống sẽ tự động phân tích và tạo phiếu — không cần bấm thêm nút xử lý.")

uploaded_file = st.file_uploader(
    "Chọn file Excel",
    type=["xlsx"],
    key=f"uploader_{st.session_state['uploader_key']}",
    label_visibility="collapsed",
)
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    file_token = hashlib.sha256(file_bytes).hexdigest()

    if st.session_state["processed_token"] != file_token:
        progress = st.progress(0, text="📥 Đang nhận file...")
        tmp_dir = tempfile.mkdtemp()
        tmp_path = os.path.join(tmp_dir, safe_name(uploaded_file.name))
        with open(tmp_path, "wb") as f:
            f.write(file_bytes)

        try:
            progress.progress(20, text="🔎 Đang đọc cấu trúc workbook...")
            progress.progress(40, text="📊 Đang tính điểm và kiểm tra dữ liệu...")
            students = engine.process_workbook(tmp_path)
        except Exception as exc:
            progress.empty()
            st.error(f"❌ Không đọc được file này: {exc}")
            students = []
            st.session_state["processed_token"] = file_token

        if students:
            progress.progress(68, text="🧠 Đang tạo nhận xét và kiến nghị...")
            progress.progress(84, text="📝 Đang tạo phiếu Word cho từng học viên...")
            zip_data = build_zip_for_students(students)
            progress.progress(100, text="🎉 Hoàn tất!")
            progress.empty()

            st.session_state["batch_counter"] += 1
            st.session_state["total_students"] += len(students)
            zip_filename = (
                f"PhieuNhanXet_{st.session_state['batch_counter']:02d}_"
                f"{safe_name(uploaded_file.name).replace('.xlsx', '')}.zip"
            )
            st.session_state["history"].append((uploaded_file.name, len(students)))
            st.session_state["processed_token"] = file_token
            st.session_state["auto_download_token"] = None
            st.session_state["result_zip"] = zip_data
            st.session_state["result_filename"] = zip_filename
            st.session_state["result_source"] = uploaded_file.name
            st.session_state["result_count"] = len(students)

            if st.session_state["celebrate_token"] != file_token:
                st.session_state["celebrate_token"] = file_token
                st.balloons()
        else:
            progress.empty()
            st.warning("⚠️ Không tìm thấy học viên nào trong file này. Kiểm tra lại cấu trúc file.")

# =========================================================================
# Kết quả / tự động tải xuống
# =========================================================================
if st.session_state["result_zip"] is not None and st.session_state["result_source"]:
    st.markdown(
        f"""
        <div class="result-card">
          <div class="result-title">🎉 Chúc mừng! Đã xử lý thành công</div>
          <div class="result-sub">Đã tạo <b>{st.session_state['result_count']} phiếu</b> từ file <b>{st.session_state['result_source']}</b>.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Tự động tải đúng 1 lần cho mỗi file.
    if st.session_state["auto_download_token"] != st.session_state["processed_token"]:
        trigger_browser_download(st.session_state["result_filename"], st.session_state["result_zip"])
        st.session_state["auto_download_token"] = st.session_state["processed_token"]

    c1, c2 = st.columns(2)
    with c1:
        st.download_button(
            "⬇️ Tải lại file ZIP",
            data=st.session_state["result_zip"],
            file_name=st.session_state["result_filename"],
            mime="application/zip",
            use_container_width=True,
        )
    with c2:
        if st.button("➕ THÊM LỚP KHÁC", type="primary", use_container_width=True):
            st.session_state["uploader_key"] += 1
            st.session_state["processed_token"] = None
            st.session_state["auto_download_token"] = None
            st.session_state["celebrate_token"] = None
            st.session_state["result_zip"] = None
            st.session_state["result_filename"] = None
            st.session_state["result_source"] = None
            st.session_state["result_count"] = 0
            st.rerun()

# =========================================================================
# Lịch sử
# =========================================================================
if st.session_state["history"]:
    with st.expander(f"📊 Lịch sử đã xử lý ({len(st.session_state['history'])} lớp · {st.session_state['total_students']} phiếu)"):
        for filename, count in reversed(st.session_state["history"]):
            st.markdown(
                f'<div class="history-item"><span>📄 {filename}</span><span class="cnt">{count} phiếu</span></div>',
                unsafe_allow_html=True,
            )

# =========================================================================
# Tùy chỉnh
# =========================================================================
with st.expander("⚙️ Tùy chỉnh logo công ty (không bắt buộc)"):
    new_logo = st.file_uploader(
        "Upload logo mới (.png/.jpg)",
        type=["png", "jpg", "jpeg"],
        key="logo_uploader",
    )
    if new_logo is not None:
        new_path = os.path.join(tempfile.mkdtemp(), safe_name(new_logo.name))
        with open(new_path, "wb") as f:
            f.write(new_logo.getbuffer())
        st.session_state["logo_path"] = new_path
        engine.COMPANY_LOGO_PATH = new_path
        st.success("✅ Đã đổi logo. Logo mới sẽ được dùng cho các phiếu tạo tiếp theo.")

st.markdown('<div class="footer-note">Made for CIE VIETNAM · Powered by Streamlit</div>', unsafe_allow_html=True)
