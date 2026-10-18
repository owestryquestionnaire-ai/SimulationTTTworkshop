import streamlit as st
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="Training Guide Builder", layout="wide")

# 2. Shared Multi-User State Manager (Real-time Database Simulation)
@st.cache_resource
def get_shared_state():
    return {
        "Group A": {"selected_themes": set(), "custom_equipments": [], "cb_state": set(), "txt_state": {}, "custom_points": {}},
        "Group B": {"selected_themes": set(), "custom_equipments": [], "cb_state": set(), "txt_state": {}, "custom_points": {}},
        "Group C": {"selected_themes": set(), "custom_equipments": [], "cb_state": set(), "txt_state": {}, "custom_points": {}},
        "Group D": {"selected_themes": set(), "custom_equipments": [], "cb_state": set(), "txt_state": {}, "custom_points": {}},
    }

# 3. Local Session State & URL Parameter Persistence
try:
    if "group" in st.query_params:
        st.session_state.current_group = st.query_params["group"]
except:
    pass

if "current_group" not in st.session_state:
    st.session_state.current_group = None

steps = [
    "Step 1: Background", 
    "Step 2: Themes", 
    "Step 3: Checklists", 
    "Step 4: Equipment", 
    "Step 5: Roles",
    "Step 6: Print View"
]

if "current_step" not in st.session_state:
    st.session_state.current_step = steps[0]

# --- LOGIN SCREEN ---
if st.session_state.current_group is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='text-align: center; margin-top: 80px;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-size: 32px;'>Welcome! Please join your assigned group:</h3><br>", unsafe_allow_html=True)
        
        selected_group = st.selectbox("Select Group", ["Group A", "Group B", "Group C", "Group D"], label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Join Group Session ➡️", type="primary", use_container_width=True):
            st.session_state.current_group = selected_group
            try:
                st.query_params["group"] = selected_group
            except:
                pass
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


# --- SMART BACKGROUND AUTO-SYNC (Every 5 seconds) ---
# This invisible script clicks the "Sync" button every 5 seconds automatically.
# It pauses if you are currently typing in a text box so it doesn't erase your work.
components.html(
    """
    <script>
    setInterval(function() {
        var active = window.parent.document.activeElement;
        if (active && (active.tagName === "INPUT" || active.tagName === "TEXTAREA")) {
            return; 
        }
        var buttons = window.parent.document.querySelectorAll("button");
        buttons.forEach(function(btn) {
            if (btn.innerText.includes("🔄 Sync")) {
                btn.click();
            }
        });
    }, 5000);
    </script>
    """,
    height=0,
    width=0
)


# --- Shared State Fetcher ---
shared = get_shared_state()[st.session_state.current_group]


# --- STRICT CLOUD-SYNC WRAPPERS ---
# These functions FORCE the local screen to copy the cloud data every time the page refreshes safely
def sync_cb(key):
    if st.session_state.get(key, False):
        shared["cb_state"].add(key)
    else:
        shared["cb_state"].discard(key)

def sync_txt(key):
    # Safety Check: Only save if the key actually exists in memory to avoid KeyError crashes
    if key in st.session_state:
        shared["txt_state"][key] = st.session_state[key]

def render_synced_checkbox(label, key):
    cloud_val = (key in shared["cb_state"])
    st.checkbox(label, value=cloud_val, key=key, on_change=sync_cb, args=(key,))

def render_synced_text(label, key, placeholder="", label_visibility="visible"):
    cloud_val = shared["txt_state"].get(key, "")
    st.text_input(label, value=cloud_val, key=key, placeholder=placeholder, label_visibility=label_visibility, on_change=sync_txt, args=(key,))


# --- Global Data Dictionaries ---
def get_theme_options(theme_str):
    if "Introduction" in theme_str:
        return [
            "Did I introduce myself and co-trainer?",
            "Did I describe the goal, objectives, duration of this training clearly?",
            "Did I hear at least 2 participants to express their needs and expectation from this training?",
            "Did I explain clearly that this training is not an assessment of their performance?"
        ]
    elif "Scene set up" in theme_str:
        return [
            "Did I set up the suctioning unit, manikin, and patient's environment similar to the ward setting?",
            "Did I offer logistical details (e.g., environment orientation, facilities) to the participants?",
            "Did I establish frictional contract with the participants?",
            "Did I mention the pre-reading materials and explain their relevance to simulation training today?"
        ]
    elif "Familiarization" in theme_str:
        return [
            "Did I mention the capacity of each manikin?",
            "Did I mention how to use the wall oxygen and suction unit in the room?",
            "Did I mention what respiratory equipment were available?",
            "Did I introduce the function of bedside monitor?",
            "Were the participants given time to familiar with the environment and equipment prior to training?"
        ]
    elif "Indications" in theme_str:
        return [
            "Did I explain patients are indicated for suctioning when they have signs and symptoms of sputum retention, while other physical modalities have been exhausted?",
            "Did I mention when suctioning should not be performed and when precautions should be taken?",
            "Did I mention specific infection control consideration to be taken during suctioning?" 
        ]
    elif "Preparation" in theme_str:
        return [
            "Did I mention why preparing the patient, environment and required equipment prior to the procedures is important?",
            "Did I mention PPE, suctioning catheters, extra clean gloves, water for flushing the tubing, pulse oximeter, sputum saver and oxygen delivery device if indicated, and adequate lighting should be prepared?",
            "Did I mention explanations to patient is required?",
            "Did I describe how the patient should be positioned?",
            "Did I mention when and how pre-oxygenation should be performed?",
            "Did I demonstrate how to check the suction pressure and troubleshoot problems in the suctioning unit?"
        ]
    elif "General principles" in theme_str:
        return [
            "Did I introduce different routes and depths of suctioning and the sizes of catheters / explain their indications?",
            "Did I mention HR, SpO2, and patient's facial expression should be closely monitored during suctioning?",
            "Did I mention suctioning time should be as minimal as possible?",
            "Did I mention suctioning pressure should be applied in an intermittent manner as the suctioning catheter is withdrawn?",
            "Did I mention recovery time / oxygen if indicated should be given between each suctioning bout?"
        ]
    elif "Oropharyngeal" in theme_str:
        return [
            "Did I mention any loose teeth / coiled R/T in mouth should be checked?",
            "Did I demonstrate how the suctioning catheter should be inserted along the angle of mouth to prevent provocation of gag reflex?",
            "Did I mention how the catheter should be inserted with slightly more than 1 finger's length to reach the pharynx?",
            "Did I describe what to do if the catheter is bitten / if the patient vomits?",
            "Did I let participants have hands-on experience?"
        ]
    elif "Nasopharyngeal" in theme_str:
        return [
            "Did I demonstrate how the suctioning catheter should be inserted medially?",
            "Did I mention the catheter should never be inserted forcefully even when resistance is felt?",
            "Did I describe how a cough should be provoked / manually stimulated for the catheter to enter the trachea?",
            "Did I let the participants have hands-on experience?"
        ]
    elif "ETT" in theme_str:
        return [
            "Did I describe the 4 critical situations to inform the doctor for emergency management (kink/blocked tube, tube too shallow, tube too deep, malfunctioning balloon)?",
            "Did I demonstrate how to connect the close suction unit to the ETT, and to the suction unit?",
            "Did I mention the ventilator alarm should be silenced temporarily if applicable?",
            "Did I demonstrate how the suctioning catheter should be inserted till the carina is touched, and should be withdrawn slightly before suctioning pressure is applied?",
            "Did I explain that suctioning pressure application can be stopped soon after the catheter is withdrawn into the ETT again?",
            "Did I demonstrate how to flush the suction catheter in the close suction system?",
            "Did I mention the need of OP suctioning for patients with ETT?",
            "Did I let the participants have hands-on experience?"
        ]
    elif "TT" in theme_str:
        return [
            "Did I demonstrate how to connect the close suction unit to the TT and the suction unit / connect the suction catheter to the suction unit to perform open suction with sterile technique?",
            "Did I briefly introduce the Protex and Shiley TT and how to handle a blocked Shiley inner tube?",
            "Did I demonstrate how shallow and deep suctioning should be performed?",
            "Did I mention the need of OP suctioning for tracheostomized cases?",
            "Did I let participants have hands-on experience?"
        ]
    elif "accessories" in theme_str:
        return [
            "Did I demonstrate how the sputum saving device is used effectively?",
            "Did I explain the indications for NPA / OPA and demonstrate how they are inserted?",
            "Did I explain the indications for Yankauer suction tip and demonstrate how it is used?",
            "Did I let the participants have hands-on experience?"
        ]
    elif "Change of condition" in theme_str:
        return [
            "Did I mention common critical events prior to, during and after suctioning?",
            "Did I mention how to responds to patient change of condition prior to, during and after suctioning?",
            "Did I mention oxygen should be reapplied/increased if the patient became hypoxemic following the procedure?"
        ]
    elif "Post-suction" in theme_str:
        return [
            "Did I mention oxygen should be reapplied/increased if the patient became hypoxemic following the procedure?",
            "Did I mention how the patient should be re-assessed?",
            "Did I describe how the suctioning tubing should be rinsed?",
            "Did I mention how documentation should be done?"
        ]
    return []

equipment_dict = {
    "1. Manikin": [
        "Laerdal airway management manikin", 
        "Laerdar trach airway management manikin", 
        "Transparent suction model - Sakamotol model", 
        "Laerdal paed airway management manikin"
    ],
    "2. Sim monitor": [
        "iPad with SIMPL app", 
        "Microsoft notebook with sim ventilator", 
        "Bedside monitor with mobile stand", 
        "ECG leads, SpO2 probe", 
        "Cough assist machine - Clearway"
    ],
    "3. Suction equipment": [
        "Suction catheter size 10, 12, 14", 
        "Yaukauer suction tube - two models", 
        "Closed suction catheter", 
        "Screw down needleless syringe (10 or 20 mL)", 
        "10 mL normal saline", 
        "KY jelly - single pack", 
        "20 mL sterile water"
    ],
    "4. Oxygen Delivery Device (ODD)": [
        "Oxygen device - NRM, simple mask, nasal cannula, HFOT cannula - small and medium size", 
        "NIV mask"
    ],
    "5. Airway": [
        "OP airways - common size", 
        "Trach tubes - subglottic, cuff and cuffless, shiley", 
        "ETT", 
        "Trach tight", 
        "Barometer"
    ],
    "6. PPE": [
        "Gloves: small, medium, large", 
        "Face shield and PPE"
    ]
}


def go_to_step(step_name):
    st.session_state.current_step = step_name

def toggle_theme(theme_name):
    if theme_name in shared["selected_themes"]:
        shared["selected_themes"].remove(theme_name)
    else:
        shared["selected_themes"].add(theme_name)

def get_dynamic_objectives(selected_themes):
    objs = []
    clean_themes = [t.replace('\n', ' ') for t in selected_themes]
    
    if any("Indications" in t for t in clean_themes):
        objs.append("Understand indications and contraindications of suctioning")
    if any("Preparation" in t or "General principles" in t for t in clean_themes):
        objs.append("Understand general proper procedures of suctioning")
    if any("Oropharyngeal" in t or "Nasopharyngeal" in t for t in clean_themes):
        objs.append("Master skills of safe and effective suctioning")
    if any("ETT" in t or "TT" in t for t in clean_themes):
        objs.append("Master skills of safe and effective suctioning in tracheostomized patient.")
    if any("accessories" in t for t in clean_themes):
        objs.append("Understand use of suctioning accessories")
    if any("Change of condition" in t for t in clean_themes):
        objs.append("Correctly identify and respond to critical events or error prior to, during and after suctioning")
        
    return objs

# --- Button Callback Functions ---
def select_all_checklist(theme_key, num_options):
    for i in range(num_options):
        cb_key = f"chk_{theme_key}_{i}"
        shared["cb_state"].add(cb_key)
        st.session_state[cb_key] = True
    c_points = shared["custom_points"].get(theme_key, [])
    for i in range(len(c_points)):
        cb_key = f"custom_chk_{theme_key}_{i}"
        shared["cb_state"].add(cb_key)
        st.session_state[cb_key] = True

def remove_all_checklist(theme_key, num_options):
    for i in range(num_options):
        cb_key = f"chk_{theme_key}_{i}"
        shared["cb_state"].discard(cb_key)
        st.session_state[cb_key] = False
    c_points = shared["custom_points"].get(theme_key, [])
    for i in range(len(c_points)):
        cb_key = f"custom_chk_{theme_key}_{i}"
        shared["cb_state"].discard(cb_key)
        st.session_state[cb_key] = False

def select_all_equipment(cat, items):
    for item in items:
        cb_key = f"eq_{cat}_{item}"
        shared["cb_state"].add(cb_key)
        st.session_state[cb_key] = True

def remove_all_equipment(cat, items):
    for item in items:
        cb_key = f"eq_{cat}_{item}"
        shared["cb_state"].discard(cb_key)
        st.session_state[cb_key] = False

def select_all_custom_eq():
    for i in range(len(shared["custom_equipments"])):
        cb_key = f"custom_eq_chk_{i}"
        shared["cb_state"].add(cb_key)
        st.session_state[cb_key] = True

def remove_all_custom_eq():
    for i in range(len(shared["custom_equipments"])):
        cb_key = f"custom_eq_chk_{i}"
        shared["cb_state"].discard(cb_key)
        st.session_state[cb_key] = False

def add_custom_point(theme_key):
    input_key = f"input_{theme_key}"
    new_point = st.session_state.get(input_key, "").strip()
    
    if theme_key not in shared["custom_points"]:
        shared["custom_points"][theme_key] = []
        
    if new_point and new_point not in shared["custom_points"][theme_key]:
        shared["custom_points"][theme_key].append(new_point)
        idx = len(shared["custom_points"][theme_key]) - 1
        shared["cb_state"].add(f"custom_chk_{theme_key}_{idx}")
    st.session_state[input_key] = ""

def render_checklist(options, theme_key):
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        st.button("✅ Select All", key=f"sel_all_chk_{theme_key}", on_click=select_all_checklist, args=(theme_key, len(options)))
    with btn_col2:
        st.button("❌ Remove All", key=f"rem_all_chk_{theme_key}", on_click=remove_all_checklist, args=(theme_key, len(options)))
    
    for i, opt in enumerate(options):
        cb_key = f"chk_{theme_key}_{i}"
        render_synced_checkbox(opt, cb_key)
            
    c_points = shared["custom_points"].get(theme_key, [])
    for i, custom_opt in enumerate(c_points):
        cb_key = f"custom_chk_{theme_key}_{i}"
        render_synced_checkbox(custom_opt, cb_key)
            
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([5, 1])
    with col1:
        st.text_input("Add new point", key=f"input_{theme_key}", label_visibility="collapsed", placeholder="Type a custom checklist item here...")
    with col2:
        st.button("Add Point", key=f"add_btn_{theme_key}", on_click=add_custom_point, args=(theme_key,))

def add_custom_equipment():
    new_eq = st.session_state.get("input_custom_eq", "").strip()
    if new_eq and new_eq not in shared["custom_equipments"]:
        shared["custom_equipments"].append(new_eq)
        idx = len(shared["custom_equipments"]) - 1
        shared["cb_state"].add(f"custom_eq_chk_{idx}")
    st.session_state.input_custom_eq = ""


# 3. CSS Styling - FORCING 24PX GLOBALLY & RESTORING COLORS
st.markdown("""
<style>
    div[data-testid="stMarkdownContainer"] p, 
    div[data-testid="stMarkdownContainer"] li {
        font-size: 24px !important;
        line-height: 1.6 !important;
    }

    .main-header {
        font-size: 32px; 
        font-weight: 800;
        color: #000;
        margin-bottom: -5px;
        font-family: Arial, sans-serif;
    }
    
    div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }
    div[role="radiogroup"] {
        display: flex;
        gap: 8px; 
        border-bottom: 2px solid #ddd;
        padding-bottom: 10px;
        margin-bottom: 20px;
        flex-wrap: wrap;
    }
    div[role="radiogroup"] label {
        cursor: pointer;
    }
    div[role="radiogroup"] label p {
        font-size: 20px !important; 
        font-weight: 600 !important;
        color: #555 !important;
        margin: 0;
        padding: 5px 8px; 
    }
    
    .step-header {
        font-size: 32px !important;
        font-weight: 700 !important;
        color: #222 !important;
        margin-top: 15px;
        margin-bottom: 15px;
        font-family: Arial, sans-serif;
        border-bottom: 2px solid #eee;
        padding-bottom: 8px;
    }
    
    /* ---------------------------------------------------
       1. MAIN THEME BUTTONS & COLORS
       --------------------------------------------------- */
    [data-testid="column"]:has([class*="marker-"]) button, 
    [data-testid="stColumn"]:has([class*="marker-"]) button {
        width: 100% !important; 
        height: 160px !important; 
        border-radius: 16px !important;
        border: 2px solid #dadce0 !important;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.05) !important;
        transition: 0.2s ease-in-out !important;
    }
    
    [data-testid="column"]:has([class*="marker-"]) button p, 
    [data-testid="stColumn"]:has([class*="marker-"]) button p {
        font-size: 32px !important; 
        font-weight: normal !important;
        color: #111 !important;
        white-space: pre-wrap !important;
        line-height: 1.3 !important;
        margin: 0 !important;
    }

    [data-testid="column"]:has([class*="marker-"]) button:hover, 
    [data-testid="stColumn"]:has([class*="marker-"]) button:hover {
        transform: translateY(-2px) !important;
        filter: brightness(0.95) !important;
        border: 2px solid #666 !important;
    }

    /* Restored Dual Selectors for Cloud and Local Support */
    [data-testid="column"]:has(.marker-blue) button, [data-testid="stColumn"]:has(.marker-blue) button { background-color: #d4e4ff !important; }
    [data-testid="column"]:has(.marker-pink) button, [data-testid="stColumn"]:has(.marker-pink) button { background-color: #ffd4d4 !important; }
    [data-testid="column"]:has(.marker-purple) button, [data-testid="stColumn"]:has(.marker-purple) button { background-color: #eed4ff !important; }
    [data-testid="column"]:has(.marker-peach) button, [data-testid="stColumn"]:has(.marker-peach) button { background-color: #ffe4d4 !important; }
    [data-testid="column"]:has(.marker-green) button, [data-testid="stColumn"]:has(.marker-green) button { background-color: #d4ffd4 !important; }
    [data-testid="column"]:has(.marker-cyan) button, [data-testid="stColumn"]:has(.marker-cyan) button { background-color: #d4ffff !important; }
    [data-testid="column"]:has(.marker-lavender) button, [data-testid="stColumn"]:has(.marker-lavender) button { background-color: #e6e6fa !important; }
    [data-testid="column"]:has(.marker-lemon) button, [data-testid="stColumn"]:has(.marker-lemon) button { background-color: #fffacd !important; }
    [data-testid="column"]:has(.marker-rose) button, [data-testid="stColumn"]:has(.marker-rose) button { background-color: #ffe4e1 !important; }
    [data-testid="column"]:has(.marker-yellow) button, [data-testid="stColumn"]:has(.marker-yellow) button { background-color: #fff9d4 !important; }
    [data-testid="column"]:has(.marker-silver) button, [data-testid="stColumn"]:has(.marker-silver) button { background-color: #f2f2f2 !important; }
    [data-testid="column"]:has(.marker-mint) button, [data-testid="stColumn"]:has(.marker-mint) button { background-color: #e0f8ee !important; }
    [data-testid="column"]:has(.marker-coral) button, [data-testid="stColumn"]:has(.marker-coral) button { background-color: #ffdab9 !important; }

    /* ---------------------------------------------------
       2. EXPANDER HEADERS
       --------------------------------------------------- */
    div[data-testid="stExpander"] summary p {
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #111 !important;
    }

    /* ---------------------------------------------------
       3. WIDGET FONTS (Inputs, Labels, Checkboxes)
       --------------------------------------------------- */
    label[data-testid="stWidgetLabel"] p {
        font-size: 24px !important;
        font-weight: bold !important;
        color: #000 !important;
    }
    
    div[data-testid="stCheckbox"] {
        border-bottom: 1px solid #e0e0e0;
        padding: 12px 8px !important;
        margin-bottom: 0px !important;
        border-radius: 4px;
        transition: background-color 0.15s ease;
    }
    div[data-testid="stCheckbox"]:hover {
        background-color: #f8f9fa;
    }
    div[data-testid="stCheckbox"] label span, 
    div[data-testid="stCheckbox"] label p {
        font-size: 24px !important; 
        line-height: 1.6 !important;
    }
    div[data-testid="stExpander"] label p {
        font-size: 24px !important;
        font-weight: 500 !important;
    }
    div[data-testid="stTextInput"] input {
        font-size: 24px !important;
        padding: 12px !important;
    }

    /* ---------------------------------------------------
       4. "ADD POINT/ITEM" & MINOR BUTTONS
       --------------------------------------------------- */
    div[data-testid="stExpander"] div[data-testid="column"] div[data-testid="stButton"] button {
        height: 52px !important;
        border-radius: 6px !important;
        border: 1px solid #ccc !important;
        background-color: #f9f9f9 !important;
    }
    div[data-testid="stExpander"] div[data-testid="column"] div[data-testid="stButton"] button p {
        font-size: 20px !important;
        font-weight: 600 !important;
        color: #333 !important;
    }
    
    /* Top Right Minor Buttons */
    div[data-testid="stVerticalBlock"] div[data-testid="column"] button p {
        font-size: 18px !important;
    }

    /* ---------------------------------------------------
       5. GENERATE & NAVIGATION BUTTONS
       --------------------------------------------------- */
    button[kind="primary"] {
        height: 54px !important;
        width: auto !important; 
        padding: 4px 24px !important;
        border-radius: 6px !important;
        border: 1px solid #2ea44f !important;
        background-color: #2ea44f !important;
        box-shadow: none !important;
        margin-top: 15px;
    }
    button[kind="primary"] p {
        font-size: 24px !important;
        font-weight: 600 !important;
        color: #ffffff !important;
    }
    button[kind="primary"]:hover {
        background-color: #2c974b !important;
        border-color: #2c974b !important;
    }
    div[data-testid="stButton"] button:focus:not(:focus-visible) {
        outline: none !important;
    }

    /* Print Document Styling - 24px Baseline */
    .doc-container {
        background-color: white; 
        padding: 40px; 
        border-radius: 8px; 
        color: #000 !important;
    }
    .doc-container p, .doc-container li, .doc-container strong, .doc-container ul, .doc-container div, .doc-container span {
        font-size: 24px !important; 
        line-height: 1.8 !important;
        color: #000 !important;
    }

</style>
""", unsafe_allow_html=True)


# --- TOP NAVIGATION & HEADER ---
colA, colB = st.columns([2, 1])
with colA:
    st.markdown('<div class="main-header">Write your own training guide:</div>', unsafe_allow_html=True)
with colB:
    st.markdown(f"<div style='text-align:right; font-size:20px; font-weight:bold; color:#2ea44f; margin-bottom: 5px;'>🟢 Active: {st.session_state.current_group}</div>", unsafe_allow_html=True)
    
    # Using an invisible button for the JS to click so it stays hidden from UI
    if st.button("🔄 Sync", key="hidden_sync", help="Hidden button for JS auto-sync"):
        st.rerun()

    if st.button("🗑️ Clear Data", use_container_width=True):
        shared["selected_themes"].clear()
        shared["custom_equipments"].clear()
        shared["cb_state"].clear()
        shared["txt_state"].clear()
        shared["custom_points"].clear()
        
        keys_to_delete = [k for k in st.session_state.keys() if k not in ["current_group", "current_step"]]
        for k in keys_to_delete:
            del st.session_state[k]
        st.rerun()

st.markdown("""
<style>
    /* Hide the auto-sync button so it doesn't clutter the UI */
    div[data-testid="stButton"] button[title="Hidden button for JS auto-sync"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Render the pseudo-tabs
st.radio("Navigation", steps, key="current_step", horizontal=True, label_visibility="collapsed")


# ==========================================
# STEP 1: BACKGROUND OF THE TRAINING 
# ==========================================
if st.session_state.current_step == steps[0]:
    st.markdown('<div class="step-header">Step 1: Background of the training</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size: 24px; line-height: 1.8; color: #333;">
        <strong style="color: #000;">XXX Physiotherapy Department</strong><br>
        <strong style="color: #000;">Phase I Simulation Training - Sputum Suction 2026</strong><br><br>
        <strong>Goal:</strong> Correct and safe physiotherapy practice to perform sputum suctioning on Adult inpatients<br><br>
        <strong>Date:</strong> 23/10/2026<br>
        <strong>Duration:</strong> 20 minutes<br>
        <strong>Target Participant:</strong> New recruit RPT or staff with interest<br>
        <strong>Participants per class:</strong> 5
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    for i in range(5):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            txt_key = f"t_name_{i}"
            render_synced_text(
                f"Trainer {i+1} Name", 
                key=txt_key,
                placeholder="Enter trainer name"
            )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.button("To Step 2 ➡️", type="primary", on_click=go_to_step, args=(steps[1],))

# ==========================================
# STEP 2: CHOOSE THE THEMES 
# ==========================================
elif st.session_state.current_step == steps[1]:
    st.markdown('<div class="step-header">Step 2: Choose the themes you want to include</div>', unsafe_allow_html=True)

    themes_row1 = ["Indications and\ncontraindications", "Preparation for\nsuctioning", "General principles\nof suctioning"]
    colors_row1 = ["blue", "pink", "purple"]

    themes_row2 = ["Oropharyngeal suctioning", "Nasopharyngeal/\nNasotracheal suctioning", "Suctioning on patient\nwith ETT"]
    colors_row2 = ["peach", "green", "cyan"]

    themes_row3 = ["Suctioning on patient\nwith TT", "Use of suctioning\naccessories", "Change of condition\nmanagement"]
    colors_row3 = ["lavender", "lemon", "rose"]

    themes_row4 = ["Post-suction\nmanagement", "Other Theme 1", "Other Theme 2"]
    colors_row4 = ["yellow", "silver", "mint"]

    themes_row5 = ["Other Theme 3", None, None]
    colors_row5 = ["coral", None, None]

    def render_row(cols, themes, colors):
        for col, theme, color in zip(cols, themes, colors):
            with col:
                if theme:
                    st.markdown(f'<div class="marker-{color}" style="display:none;"></div>', unsafe_allow_html=True)
                    label = f"✅ {theme}" if theme in shared["selected_themes"] else theme
                    st.button(label, key=theme, on_click=toggle_theme, args=(theme,), use_container_width=True)

    render_row(st.columns(3), themes_row1, colors_row1)
    render_row(st.columns(3), themes_row2, colors_row2)
    render_row(st.columns(3), themes_row3, colors_row3)
    render_row(st.columns(3), themes_row4, colors_row4)
    render_row(st.columns(3), themes_row5, colors_row5)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.button("To Step 3 ➡️", type="primary", on_click=go_to_step, args=(steps[2],))

# ==========================================
# STEP 3: DEVELOP CHECKLIST POINTS 
# ==========================================
elif st.session_state.current_step == steps[2]:
    st.markdown('<div class="step-header">Step 3: Develop checklist points in each theme</div>', unsafe_allow_html=True)

    with st.expander("Theme 1 'Introduction'", expanded=True):
        render_checklist(get_theme_options("Introduction"), "Mandatory_Intro")

    with st.expander("Theme 2 'Scene set up'", expanded=True):
        render_checklist(get_theme_options("Scene set up"), "Mandatory_Scene")

    with st.expander("Theme 3 'Familiarization'", expanded=True):
        render_checklist(get_theme_options("Familiarization"), "Mandatory_Familiarization")

    all_ordered_themes = ["Indications and\ncontraindications", "Preparation for\nsuctioning", "General principles\nof suctioning",
                          "Oropharyngeal suctioning", "Nasopharyngeal/\nNasotracheal suctioning", "Suctioning on patient\nwith ETT",
                          "Suctioning on patient\nwith TT", "Use of suctioning\naccessories", "Change of condition\nmanagement",
                          "Post-suction\nmanagement", "Other Theme 1", "Other Theme 2", "Other Theme 3"]

    ordered_selections = [t for t in all_ordered_themes if t in shared["selected_themes"]]

    for idx, theme in enumerate(ordered_selections):
        clean_theme_name = theme.replace('\n', ' ')
        theme_number = idx + 4 
        
        with st.expander(f"Theme {theme_number} '{clean_theme_name}'", expanded=True):
            if "Other Theme" in theme:
                txt_key = f"custom_name_{theme}"
                render_synced_text(
                    "Theme Name:", 
                    key=txt_key,
                    placeholder="E.g., Suctioning with Ventilator Case"
                )
                render_checklist([], clean_theme_name)
            else:
                render_checklist(get_theme_options(clean_theme_name), clean_theme_name)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.button("To Step 4 ➡️", type="primary", on_click=go_to_step, args=(steps[3],))

# ==========================================
# STEP 4: EQUIPMENTS REQUIRED 
# ==========================================
elif st.session_state.current_step == steps[3]:
    st.markdown('<div class="step-header">Step 4: Equipments required</div>', unsafe_allow_html=True)
    st.markdown("<div style='font-size: 24px; margin-bottom: 10px;'>Select all the equipment needed for this training scenario:</div>", unsafe_allow_html=True)
    
    eq_cols = st.columns(2)
    categories = list(equipment_dict.keys())
    
    for idx, cat in enumerate(categories):
        with eq_cols[idx % 2]:
            st.markdown(f"<br><div style='font-size: 24px; font-weight: bold;'>{cat}</div>", unsafe_allow_html=True)
            
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                st.button("✅ Select All", key=f"sel_all_{cat}", on_click=select_all_equipment, args=(cat, equipment_dict[cat]))
            with btn_col2:
                st.button("❌ Remove All", key=f"rem_all_{cat}", on_click=remove_all_equipment, args=(cat, equipment_dict[cat]))
            
            for item in equipment_dict[cat]:
                cb_key = f"eq_{cat}_{item}"
                render_synced_checkbox(item, cb_key)

    # --- Add Custom Equipment ---
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("➕ Custom Equipment", expanded=True):
        if shared["custom_equipments"]:
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                st.button("✅ Select All Custom", key="sel_all_custom_eq", on_click=select_all_custom_eq)
            with btn_col2:
                st.button("❌ Remove All Custom", key="rem_all_custom_eq", on_click=remove_all_custom_eq)
            
        for i, custom_eq in enumerate(shared["custom_equipments"]):
            cb_key = f"custom_eq_chk_{i}"
            render_synced_checkbox(custom_eq, cb_key)
                
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns([5, 1])
        with col1:
            st.text_input("Add custom equipment", key="input_custom_eq", label_visibility="collapsed", placeholder="Type a custom equipment item here...")
        with col2:
            st.button("Add Item", key="add_custom_eq_btn", on_click=add_custom_equipment)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.button("To Step 5 ➡️", type="primary", on_click=go_to_step, args=(steps[4],))

# ==========================================
# STEP 5: DIVISION OF LABOUR 
# ==========================================
elif st.session_state.current_step == steps[4]:
    st.markdown('<div class="step-header">Step 5: Division of Labour</div>', unsafe_allow_html=True)
    st.markdown("<div style='font-size: 24px; margin-bottom: 10px;'>Assign trainers to the following roles:</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        render_synced_text("Intro and set the scene:", key="role_intro")
        render_synced_text("Task 1 facilitator:", key="role_task1")
        render_synced_text("Task 2 facilitator:", key="role_task2")
    with col2:
        render_synced_text("Debriefer 1:", key="role_debrief1")
        render_synced_text("Debriefer 2:", key="role_debrief2")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.button("To Step 6 (Print View) ➡️", type="primary", on_click=go_to_step, args=(steps[5],))

# ==========================================
# STEP 6: PRINT VIEW 
# ==========================================
elif st.session_state.current_step == steps[5]:
    st.markdown('<div class="step-header">Step 6: Print View</div>', unsafe_allow_html=True)
    
    # 1. Gather Background Data
    trainer_names_list = [shared["txt_state"].get(f"t_name_{i}", "") for i in range(5) if shared["txt_state"].get(f"t_name_{i}", "").strip()]
    dynamic_objs = get_dynamic_objectives(shared["selected_themes"])
    
    # 2. Re-Build Selected Equipments
    final_equipments = {}
    for cat, items in equipment_dict.items():
        cat_label = cat.split('. ')[1] if '. ' in cat else cat
        sel_items = [item for item in items if f"eq_{cat}_{item}" in shared["cb_state"]]
        if sel_items:
            final_equipments[cat_label] = sel_items
            
    custom_eq_sel = [eq for i, eq in enumerate(shared["custom_equipments"]) if f"custom_eq_chk_{i}" in shared["cb_state"]]
    if custom_eq_sel:
        final_equipments["Custom Equipment"] = custom_eq_sel

    # 3. Re-Build Theme Checklists
    final_checklists = {}
    
    # Mandatory Themes
    for title, key in [("Introduction", "Mandatory_Intro"), ("Scene set up", "Mandatory_Scene"), ("Familiarization", "Mandatory_Familiarization")]:
        pts = []
        for i, opt in enumerate(get_theme_options(title)):
            if f"chk_{key}_{i}" in shared["cb_state"]: pts.append(opt)
        for i, opt in enumerate(shared["custom_points"].get(key, [])):
            if f"custom_chk_{key}_{i}" in shared["cb_state"]: pts.append(opt)
        if pts: final_checklists[title] = pts

    # Optional Themes
    all_ordered_themes = ["Indications and\ncontraindications", "Preparation for\nsuctioning", "General principles\nof suctioning",
                          "Oropharyngeal suctioning", "Nasopharyngeal/\nNasotracheal suctioning", "Suctioning on patient\nwith ETT",
                          "Suctioning on patient\nwith TT", "Use of suctioning\naccessories", "Change of condition\nmanagement",
                          "Post-suction\nmanagement", "Other Theme 1", "Other Theme 2", "Other Theme 3"]
    ordered_selections = [t for t in all_ordered_themes if t in shared["selected_themes"]]

    for theme in ordered_selections:
        clean_theme_name = theme.replace('\n', ' ')
        key = clean_theme_name
        
        final_name = clean_theme_name
        if "Other Theme" in theme:
            custom_name = shared["txt_state"].get(f"custom_name_{theme}", "").strip()
            if custom_name: final_name = custom_name
            
        pts = []
        for i, opt in enumerate(get_theme_options(clean_theme_name)):
            if f"chk_{key}_{i}" in shared["cb_state"]: pts.append(opt)
        for i, opt in enumerate(shared["custom_points"].get(key, [])):
            if f"custom_chk_{key}_{i}" in shared["cb_state"]: pts.append(opt)
        if pts: final_checklists[final_name] = pts

    # Display Visual Print View
    html_out = """
    <div class='doc-container'>
        <div style='text-align: center; margin-bottom: 20px;'>
            <strong style='color: #000; font-size: 34px;'>XXX Physiotherapy Department</strong><br>
            <strong style='color: #000; font-size: 34px;'>Phase I Simulation Training - Sputum Suction 2026</strong>
        </div>
        <p style='margin-top: 10px; margin-bottom: 10px;'><strong style='color: #000;'>Goal:</strong> Correct and safe physiotherapy practice to perform sputum suctioning on Adult inpatients</p>
    """
    
    if dynamic_objs:
        objs_list_html = "".join([f"<li>{o}</li>" for o in dynamic_objs])
        html_out += f"<div style='margin-bottom: 10px;'><strong style='color: #000;'>Objectives:</strong><br>After completion of this training, participant is able to:<ul style='margin-top: 5px; margin-bottom: 10px;'>{objs_list_html}</ul></div>"
    
    html_out += f"""
        <p style='margin-top: 10px; margin-bottom: 0;'><strong style='color: #000;'>Date:</strong> 23/10/2026</p>
        <p style='margin-top: 0; margin-bottom: 0;'><strong style='color: #000;'>Duration:</strong> 20 minutes</p>
        <p style='margin-top: 0; margin-bottom: 0;'><strong style='color: #000;'>Target participant:</strong> New recruit RPT or staff with interest</p>
        <p style='margin-top: 0; margin-bottom: 0;'><strong style='color: #000;'>Participants per class:</strong> 5</p>
        <p style='margin-top: 0; margin-bottom: 10px;'><strong style='color: #000;'>Trainer:</strong> {', '.join(trainer_names_list) if trainer_names_list else 'Unassigned'}</p>
        
        <strong style='color: #000;'>Division of Labour:</strong>
        <ul style='margin-top: 0; margin-bottom: 10px;'>
            <li>Intro and set the scene: {shared['txt_state'].get('role_intro', 'Unassigned')}</li>
            <li>Task 1 facilitator: {shared['txt_state'].get('role_task1', 'Unassigned')}</li>
            <li>Task 2 facilitator: {shared['txt_state'].get('role_task2', 'Unassigned')}</li>
            <li>Debriefer 1: {shared['txt_state'].get('role_debrief1', 'Unassigned')}</li>
            <li>Debriefer 2: {shared['txt_state'].get('role_debrief2', 'Unassigned')}</li>
        </ul>
        
        <strong style='color: #000;'>Equipments:</strong><br>
    """

    if final_equipments:
        for cat, items in final_equipments.items():
            html_out += f"<strong style='color: #000;'>{cat}:</strong> {', '.join(items)}<br>"
    else:
        html_out += "<em>No equipment selected.</em><br>"
        
    html_out += "<div style='font-size: 28px; font-weight: bold; border-bottom: 2px solid #000; padding-bottom: 5px; margin-top: 20px; margin-bottom: 15px; color: #000;'>Checklist for Trainer</div>"
    
    if final_checklists:
        for theme_title, points in final_checklists.items():
            html_out += f"<strong style='color: #000;'>{theme_title}</strong>"
            pts_html = "".join([f"<li>[ ] {point}</li>" for point in points])
            html_out += f"<ul style='list-style-type: none; padding-left: 0; margin-top: 0px; margin-bottom: 20px;'>{pts_html}</ul>"
    else:
        html_out += "<em>No checklist points selected.</em>"
        
    html_out += "</div>"

    html_out = html_out.replace("\n", "")
    st.markdown(html_out, unsafe_allow_html=True)
