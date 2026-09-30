import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

st.title("💰 TÍNH LÃI TIỀN GỬI TIẾT KIỆM")
st.write("Tính tiền lãi theo **lãi đơn** hoặc **lãi kép**.")

st.divider()

# =========================
# NHẬP THÔNG TIN
# =========================

so_tien_gui = st.number_input(
    "💵 Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=10_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "📅 Kỳ hạn (tháng)",
    min_value=1,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "📈 Lãi suất (%/năm)",
    min_value=0.0,
    value=6.0,
    step=0.1,
    format="%.2f"
)

hinh_thuc_lai = st.selectbox(
    "💡 Hình thức tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

hinh_thuc_nhan = st.selectbox(
    "💳 Hình thức nhận lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)

st.divider()

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================

def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ"


# =========================
# TÍNH TOÁN
# =========================

if st.button("🧮 TÍNH LÃI", use_container_width=True):

    if so_tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất theo năm chuyển sang số thập phân
    r = lai_suat / 100

    # Số tháng gửi
    n_thang = ky_han

    # =========================
    # LÃI ĐƠN
    # =========================
    if hinh_thuc_lai == "Lãi đơn":

        # Tổng tiền lãi
        tong_lai = so_tien_gui * r * (n_thang / 12)

        # Tiền lãi mỗi kỳ
        if hinh_thuc_nhan == "Lãnh lãi theo tháng":
            lai_dinh_ky = so_tien_gui * r / 12
            so_ky = n_thang

        elif hinh_thuc_nhan == "Lãnh lãi theo quý":
            lai_dinh_ky = so_tien_gui * r / 4
            so_ky = n_thang // 3

            # Nếu kỳ hạn không chia hết cho 3,
            # phần tháng lẻ vẫn được tính vào tổng lãi.
            if n_thang % 3 != 0:
                lai_dinh_ky = None

        else:
            lai_dinh_ky = tong_lai
            so_ky = 1

        tong_tien = so_tien_gui + tong_lai

    # =========================
    # LÃI KÉP
    # =========================
    else:

        # Xác định số lần nhập lãi vào gốc
        if hinh_thuc_nhan == "Lãnh lãi theo tháng":
            so_ky = n_thang
            lai_dinh_ky = None

            # Lãi suất mỗi tháng
            r_ky = r / 12

            # Công thức lãi kép
            tong_tien = so_tien_gui * (1 + r_ky) ** so_ky
            tong_lai = tong_tien - so_tien_gui

        elif hinh_thuc_nhan == "Lãnh lãi theo quý":
            so_ky = n_thang // 3

            # Nếu kỳ hạn không đủ số quý,
            # dùng số tháng thực tế để tính phần còn lại.
            if n_thang % 3 == 0:
                r_ky = r / 4

                tong_tien = so_tien_gui * (1 + r_ky) ** so_ky
                tong_lai = tong_tien - so_tien_gui

                lai_dinh_ky = None
            else:
                # Tính theo tháng cho phần kỳ hạn không tròn quý
                r_thang = r / 12
                tong_tien = so_tien_gui * (1 + r_thang) ** n_thang
                tong_lai = tong_tien - so_tien_gui
                lai_dinh_ky = None

        else:
            # Lãi kép cuối kỳ:
            # Tính theo số tháng của kỳ hạn
            r_thang = r / 12

            tong_tien = so_tien_gui * (1 + r_thang) ** n_thang
            tong_lai = tong_tien - so_tien_gui

            lai_dinh_ky = tong_lai
            so_ky = 1

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================

    st.success("✅ Tính toán thành công!")

    st.subheader("📊 KẾT QUẢ")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💰 Tiền gửi ban đầu",
            dinh_dang_tien(so_tien_gui)
        )

    with col2:
        st.metric(
            "📈 Lãi suất",
            f"{lai_suat:.2f}%/năm"
        )

    st.divider()

    # Tiền lãi định kỳ
    st.write("### 💵 Tiền lãi định kỳ")

    if hinh_thuc_lai == "Lãi đơn":

        if hinh_thuc_nhan == "Lãnh lãi theo tháng":
            st.info(
                f"**{dinh_dang_tien(lai_dinh_ky)} / tháng**"
            )

        elif hinh_thuc_nhan == "Lãnh lãi theo quý":
            if n_thang % 3 == 0:
                st.info(
                    f"**{dinh_dang_tien(lai_dinh_ky)} / quý**"
                )
            else:
                st.info(
                    "Kỳ hạn không tròn quý nên tiền lãi cuối cùng "
                    "được tính theo số tháng thực tế."
                )

        else:
            st.info(
                f"**{dinh_dang_tien(tong_lai)} cuối kỳ**"
            )

    else:

        if hinh_thuc_nhan == "Lãnh lãi theo tháng":
            st.info(
                "Lãi được nhập vào gốc mỗi tháng, "
                "nên tiền lãi của mỗi tháng sẽ tăng dần."
            )

        elif hinh_thuc_nhan == "Lãnh lãi theo quý":
            st.info(
                "Lãi được nhập vào gốc mỗi quý, "
                "nên tiền lãi của mỗi quý sẽ tăng dần."
            )

        else:
            st.info(
                f"**{dinh_dang_tien(tong_lai)} cuối kỳ**"
            )

    st.divider()

    # Tổng tiền lãi
    st.metric(
        "💵 TỔNG TIỀN LÃI",
        dinh_dang_tien(tong_lai)
    )

    # Tổng tiền gốc + lãi
    st.metric(
        "🏦 TỔNG TIỀN GỐC + LÃI",
        dinh_dang_tien(tong_tien)
    )

    # =========================
    # THÔNG TIN CÔNG THỨC
    # =========================

    with st.expander("📚 Xem công thức tính"):

        if hinh_thuc_lai == "Lãi đơn":
            st.write("**Công thức lãi đơn:**")
            st.latex(
                r"L = P \times r \times \frac{n}{12}"
            )

            st.write("Trong đó:")
            st.write("- P: Số tiền gửi ban đầu")
            st.write("- r: Lãi suất năm")
            st.write("- n: Số tháng gửi")
            st.write("- L: Tổng tiền lãi")

        else:
            st.write("**Công thức lãi kép:**")
            st.latex(
                r"A = P \times (1 + r)^n"
            )

            st.write("Trong đó:")
            st.write("- P: Số tiền gửi ban đầu")
            st.write("- r: Lãi suất mỗi kỳ")
            st.write("- n: Số kỳ nhập lãi")
            st.write("- A: Tổng tiền gốc + lãi")

    st.caption(
        "Lưu ý: Đây là công cụ mô phỏng theo công thức toán học. "
        "Lãi suất và cách tính thực tế của ngân hàng có thể khác."
          )
