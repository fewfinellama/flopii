import streamlit as st
import os
import json
from core.db import init_db, set_setting, get_setting
from core.identity import generate_identity, import_identity


# Function to update Streamlit config.toml for theme toggling
def set_theme(theme_mode):
    config_dir = ".streamlit"
    os.makedirs(config_dir, exist_ok=True)
    config_path = os.path.join(config_dir, "config.toml")

    if theme_mode == "Dark":
        config_content = """[theme]
base="dark"
primaryColor="#00c2ff"
backgroundColor="#030712"
secondaryBackgroundColor="#070d1a"
textColor="#ffffff"
font="sans serif"
"""
    else:
        config_content = """[theme]
base="light"
primaryColor="#00c2ff"
backgroundColor="#ffffff"
secondaryBackgroundColor="#f0f2f6"
textColor="#000000"
font="sans serif"
"""

    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            if f.read() == config_content:
                return False

    with open(config_path, "w") as f:
        f.write(config_content)
    return True


if "theme_choice" not in st.session_state:
    st.session_state.theme_choice = "Dark"

st.set_page_config(
    page_title="Flopii",
    page_icon=":material/smart_toy:",
    layout="centered",
    initial_sidebar_state="expanded",
)


def load_css():
    st.markdown(
        """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
        html, body, [class*="css"]  { font-family: 'Plus Jakarta Sans', sans-serif; }
        code, pre, .stButton>button, .stBadge, .technocore-hash, .technocore-tag {
            font-family: 'JetBrains Mono', monospace !important;
        }
        h1, h2, h3 { font-weight: 700; }
        .stButton>button { border-radius: 8px; font-weight: 600; }
        div[data-testid="stSidebarUserContent"] { padding-top: 1rem; }
    </style>
    """,
        unsafe_allow_html=True,
    )


def main():
    load_css()
    init_db()

    # Sidebar
    with st.sidebar:
        try:
            st.image("flop logo.jpg", width="stretch")
        except:
            st.title("Flopii")

        page = st.radio(
            "Navigation",
            ["Dashboard", "Setup Wizard", "Admin Panel"],
            label_visibility="collapsed",
        )

        theme_selection = st.segmented_control(
            "Theme", ["Dark", "Light"], default=st.session_state.theme_choice
        )

        if theme_selection and theme_selection != st.session_state.theme_choice:
            st.session_state.theme_choice = theme_selection
            if set_theme(theme_selection):
                st.rerun()

    # Main Content
    if page == "Dashboard":
        st.title("Flopii Dashboard")
        st.markdown(
            "<div style='text-align: center;'><span style='color: #00c2ff; font-weight: bold;'>🟢 Status:</span> Online & Broadcasting</div>",
            unsafe_allow_html=True,
        )

        latest_payload = get_setting("latest_payload")
        if latest_payload:
            with st.container(border=True):
                st.subheader("Latest Market Update")
                st.code(latest_payload, language="markdown")

                target = get_setting("target_room") or "/r/flopii"
                st.caption(f"Broadcasted to Technocore: `{target}`")
        else:
            st.info(
                "The agent hasn't run its first cycle yet. Latest curated updates will appear here once it runs."
            )

    elif page == "Setup Wizard":
        st.title("Setup Wizard")
        st.caption("Configure your Flopii agent identity and intelligence.")

        with st.container(border=True):
            st.subheader("Identity Management")
            current_did = get_setting("agent_did")
            if current_did:
                st.success(f"Identity Configured! DID: `{current_did}`")

                col1, col2 = st.columns(2)
                if os.path.exists("identity.pem"):
                    with open("identity.pem", "rb") as f:
                        col1.download_button(
                            label="Download Backup (.pem)",
                            data=f,
                            file_name="identity.pem",
                            mime="application/x-pem-file",
                            icon=":material/download:",
                        )

                if col2.button("Reset Identity"):
                    set_setting("agent_did", "")
                    st.rerun()
            else:
                tab1, tab2 = st.tabs(["Create New", "Import Existing"])
                with tab1:
                    passphrase = st.text_input(
                        "Passphrase to encrypt identity.pem (optional but recommended)",
                        type="password",
                        key="new_pass",
                    )
                    if st.button("Generate Identity", type="primary"):
                        try:
                            new_did = generate_identity(passphrase)
                            set_setting("agent_did", new_did)
                            set_setting("agent_passphrase", passphrase)
                            st.success(f"Identity generated! DID: `{new_did}`")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error generating identity: {e}")
                with tab2:
                    uploaded_file = st.file_uploader(
                        "Upload your identity.pem file", type=["pem"]
                    )
                    import_passphrase = st.text_input(
                        "Passphrase (if encrypted)", type="password", key="imp_pass"
                    )
                    if (
                        st.button("Import Identity", type="primary")
                        and uploaded_file is not None
                    ):
                        try:
                            pem_bytes = uploaded_file.read()
                            new_did = import_identity(pem_bytes, import_passphrase)
                            set_setting("agent_did", new_did)
                            set_setting("agent_passphrase", import_passphrase)
                            st.success(
                                f"Identity imported successfully! DID: `{new_did}`"
                            )
                            st.rerun()
                        except ValueError as e:
                            st.error("Incorrect passphrase or invalid PEM file.")
                        except Exception as e:
                            st.error(f"Error importing identity: {e}")

        with st.container(border=True):
            st.subheader("AI Brain Configuration")
            provider = st.selectbox(
                "LLM Provider", ["OpenAI", "Groq", "Ollama", "Anthropic"]
            )
            api_key = st.text_input(
                "API Key", type="password", value=get_setting("api_key") or ""
            )

            if st.button("Save Settings"):
                set_setting("llm_provider", provider)
                set_setting("api_key", api_key)
                st.toast("Settings saved securely!")

    elif page == "Admin Panel":
        st.title("Admin Control Panel")
        st.caption("Manage your agent's sources and operations.")

        with st.container(border=True):
            st.subheader("Data Sources & Destinations")
            tickers = st.text_input(
                "Crypto Tickers (comma separated)",
                value=get_setting("crypto_tickers") or "BTC,ETH,SOL",
            )
            rss = st.text_area(
                "RSS Feeds (one URL per line)",
                value=get_setting("rss_feeds") or "https://cryptopanic.com/news/rss/",
            )
            target_room = st.text_input(
                "Target Technocore Room",
                value=get_setting("target_room") or "/r/flopii",
            )

            if st.button("Save Configuration"):
                set_setting("crypto_tickers", tickers)
                set_setting("rss_feeds", rss)
                set_setting("target_room", target_room)
                st.toast("Data sources updated!")

        with st.container(border=True):
            st.subheader("Agent Controls")

            agent_active = get_setting("agent_status") == "active"
            col1, col2 = st.columns(2)
            with col1:
                if agent_active:
                    st.success("Agent is **ACTIVE** in background.")
                    if st.button("Pause Agent"):
                        set_setting("agent_status", "paused")
                        st.rerun()
                else:
                    st.warning("Agent is **PAUSED**.")
                    if st.button("Resume Agent", type="primary"):
                        set_setting("agent_status", "active")
                        st.rerun()

            with col2:
                if st.button("Force Run Now"):
                    from core.agent import run_agent_cycle

                    with st.spinner("Executing Pipeline..."):
                        result = run_agent_cycle()
                        if result["status"] == "success":
                            st.toast("Successfully broadcasted to Technocore!")
                        else:
                            st.error(result["message"])

        st.subheader("Audit Logs")
        from core.db import get_post_logs

        logs = get_post_logs(5)
        if logs:
            for log in logs:
                timestamp, room, status, response, payload = log
                icon = "✅" if status == "Success" else "❌"
                with st.expander(f"{icon} {timestamp} — {room}"):
                    st.markdown("**Technocore Response:**")
                    try:
                        st.json(json.loads(response))
                    except:
                        st.write(response)
                    st.markdown("**Payload Sent:**")
                    st.code(payload, language="markdown")
        else:
            st.caption("No posts made yet.")


if __name__ == "__main__":
    main()
