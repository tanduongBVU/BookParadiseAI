import pandas as pd
import re
import psycopg2

# =========================================================
# BƯỚC 1: EXTRACT - SINH DỮ LIỆU GIẢ LẬP (MOCK DATA BẨN)
# =========================================================
data = {
    'ho_ten': ['  nguyen van A ', 'tran Minh Binh', 'Le hoang Nam  ', '  dinh van CHIEN '],
    # Sửa email nam@gmail.com thành một email mới hoàn toàn
    'email': ['a_new@gmail.com', 'binh_ERROR.com', 'nam_new@gmail.com', 'chien_new@yahoo.com'] 
}
df = pd.DataFrame(data)
print("--- 1. DỮ LIỆU BAN ĐẦU (BẨN) ---")
print(df)


# =========================================================
# BƯỚC 2: TRANSFORM - LÀM SẠCH VÀ CHUẨN HÓA DỮ LIỆU
# =========================================================
# Cắt khoảng trắng 2 đầu và in hoa chữ cái đầu (Ví dụ: '  nguyen van A ' -> 'Nguyen Van A')
df['ho_ten'] = df['ho_ten'].str.strip().str.title()

# Hàm kiểm tra email bằng Regex
def check_email(email):
    if re.match(r'^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$', email):
        return email
    return None # Trả về None nếu email sai định dạng

df['email'] = df['email'].apply(check_email)

# Lọc bỏ các dòng có email không hợp lệ (None)
df_clean = df.dropna(subset=['email'])

print("\n--- 2. DỮ LIỆU SAU KHI LÀM SẠCH (CHUẨN) ---")
print(df_clean)


# =========================================================
# BƯỚC 3: LOAD - NẠP DỮ LIỆU VÀO POSTGRESQL
# =========================================================
def ket_noi_database():
    return psycopg2.connect(
        host="localhost",
        database="BookParadise_DB",
        user="postgres",
        password="1",
        port="5432"
    )

def load_data_vao_db(dataframe):
    print("\n--- 3. TIẾN HÀNH NẠP VÀO DATABASE ---")
    conn = ket_noi_database()
    cursor = conn.cursor()

    # Câu lệnh SQL INSERT (thêm mật khẩu vì bảng yêu cầu NOT NULL)
    sql_insert = """
        INSERT INTO quan_ly_ban_sach.nguoi_dung (ho_ten, email, mat_khau)
        VALUES (%s, %s, %s)
    """
    
    so_dong_thanh_cong = 0

    try:
        # Duyệt qua từng dòng trong DataFrame đã làm sạch
        for index, row in dataframe.iterrows():
            ho_ten = row['ho_ten']
            email = row['email']
            mat_khau = '123456' # Mật khẩu mặc định cho dữ liệu mồi
            
            # Thực thi câu lệnh
            cursor.execute(sql_insert, (ho_ten, email, mat_khau))
            so_dong_thanh_cong += 1
            print(f"Đang chèn: {ho_ten} - {email}")

        # Commit để lưu toàn bộ thay đổi vào CSDL
        conn.commit()
        print(f"\n✓ THÀNH CÔNG: Đã nạp {so_dong_thanh_cong} dòng dữ liệu sạch vào hệ thống!")

    except Exception as e:
        # Nếu có lỗi (ví dụ trùng email UNIQUE), hoàn tác lại toàn bộ (Fail-Safe)
        conn.rollback()
        print(f"\n❌ LỖI TRONG QUÁ TRÌNH NẠP (Đã Rollback): {e}")
        
    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()

# Thực thi bước Load
load_data_vao_db(df_clean)