import streamlit as st
# Chỉ import 5 file bạn đã chuẩn bị
from data.Skills_Library import intelligence, physical, art, social, academic

# --- Khai báo các biến cần thiết ---

if "active_skills" not in st.session_state:
    st.session_state.active_skills = []  # Lưu danh sách các object kỹ năng

# --- 1. POPUP BÀI VIẾT (LARGE DIALOG) ---


@st.dialog("📖 KHÁM PHÁ KỸ NĂNG", width="large")
def show_full_article(item):
    st.markdown(f"# {item['title']}")
    st.markdown(item['content'])
    st.divider()

    # Kiểm tra xem kỹ năng đã có trong giỏ hàng chưa
    is_added = any(s['id'] == item['id']
                   for s in st.session_state.active_skills)

    if is_added:
        st.warning("✅ Kỹ năng này đã có trong giỏ hàng kiến thức.")
        if st.button("Xóa khỏi giỏ hàng", use_container_width=True):
            st.session_state.active_skills = [
                s for s in st.session_state.active_skills if s['id'] != item['id']]
            st.rerun()
    else:
        if st.button("🚀 Thêm vào Giỏ hàng kiến thức", use_container_width=True):
            st.session_state.active_skills.append(item)
            st.toast(f"Đã nạp: {item['title']}", icon="🧠")
            st.rerun()


def render_skill_cards(data_list):
    cols = st.columns(2)
    for i, item in enumerate(data_list):
        with cols[i % 2]:
            with st.container(border=True):
                # Hiển thị dấu tích nếu đã chọn
                is_selected = any(s['id'] == item['id']
                                  for s in st.session_state.active_skills)
                title_prefix = "✅ " if is_selected else ""

                st.subheader(f"{title_prefix}{item['title']}")
                st.write(f"_{item['desc']}_")

                if st.button("👁️ Xem ngay", key=f"btn_{item['id']}", use_container_width=True):
                    show_full_article(item)


def show_knowledge_cart():
    st.header("🛒 Giỏ hàng Kiến thức")

    if not st.session_state.active_skills:
        st.info("Giỏ hàng đang trống. Hãy chọn các kỹ năng để nạp vào bộ não AI!")
        return

    # Hiển thị số lượng kỹ năng đang có bằng Metric cho "ngầu"
    st.metric("Kỹ năng đã nạp", f"{len(st.session_state.active_skills)} / 15",
              help="Số lượng kỹ năng AI đang sở hữu")

    st.write(
        "Dưới đây là danh sách các module kiến thức mà Trợ lý AI của bạn đã được 'nạp não':")

    # Hiển thị danh sách kỹ năng
    for skill in st.session_state.active_skills:
        # Dùng container với border để tạo cảm giác các module riêng biệt
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{skill['title']}**")
                st.caption(skill['desc'])
            with col2:
                if st.button("🗑️", key=f"del_{skill['id']}", help="Xoá kỹ năng này"):
                    st.session_state.active_skills = [
                        s for s in st.session_state.active_skills if s['id'] != skill['id']
                    ]
                    st.rerun()

    st.divider()
    # Nút dọn dẹp nhanh
    if st.button("🗑️ Làm trống bộ não (Xoá tất cả)", type="secondary", use_container_width=True):
        st.session_state.active_skills = []
        st.rerun()

# --- 2. HÀM VẼ CARD ---


def render_skill_cards(data_list):
    if not data_list:
        st.info("📭 Nội dung đang được cập nhật, Leader đợi chút nhé!")
        return

    cols = st.columns(2)
    for i, item in enumerate(data_list):
        with cols[i % 2]:
            with st.container(border=True):
                # Chỉ báo nếu kỹ năng đang được chọn
                if st.session_state.get('current_skill_name') == item['title']:
                    st.markdown(":green[● Đang nạp trong AI]")

                st.subheader(item["title"])
                st.write(f"_{item['desc']}_")

                if st.button("👁️ Xem ngay", key=f"btn_{item['id']}", use_container_width=True):
                    show_full_article(item)

# --- 3. MAIN UI ---


def show():
    # Quản lý Tabs
    tabs = st.tabs(["🧠 Trí tuệ", "🎨 Nghệ thuật", "💪 Thể chất",
                   "🌍 Xã hội", "📚 Học thuật", "🛒 Giỏ hàng kiến thức"])

    with tabs[0]:
        render_skill_cards(getattr(intelligence, 'DATA', []))
    with tabs[1]:
        render_skill_cards(getattr(art, 'DATA', []))
    with tabs[2]:
        render_skill_cards(getattr(physical, 'DATA', []))
    with tabs[3]:
        render_skill_cards(getattr(social, 'DATA', []))
    with tabs[4]:
        render_skill_cards(getattr(academic, 'DATA', []))
    with tabs[5]:
        show_knowledge_cart()


if __name__ == "__main__":
    show()
