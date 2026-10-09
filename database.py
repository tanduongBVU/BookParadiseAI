import psycopg2


def ket_noi_database():
    conn = psycopg2.connect(
        host="localhost",
        database="BookParadise_DB",
        user="postgres",
        password="123456",
        port="5432"
    )

    return conn


# =========================================================
# BINH LUAN
# =========================================================

def lay_binh_luan(ma_binh_luan):
    conn = ket_noi_database()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT noi_dung
        FROM quan_ly_ban_sach.binh_luan
        WHERE ma_binh_luan = %s
        """,
        (ma_binh_luan,)
    )

    ket_qua = cursor.fetchone()

    cursor.close()
    conn.close()

    if ket_qua is None:
        return None

    return ket_qua[0]


def cap_nhat_binh_luan(ma_binh_luan, trang_thai, hien_thi):
    conn = ket_noi_database()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE quan_ly_ban_sach.binh_luan
        SET trang_thai_ai = %s,
            hien_thi = %s
        WHERE ma_binh_luan = %s
        """,
        (trang_thai, hien_thi, ma_binh_luan)
    )

    conn.commit()

    cursor.close()
    conn.close()


# =========================================================
# NGUOI DUNG
# =========================================================

def lay_nguoi_dung(ma_nguoi_dung):
    conn = ket_noi_database()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT ho_ten, email
        FROM quan_ly_ban_sach.nguoi_dung
        WHERE ma_nguoi_dung = %s
        """,
        (ma_nguoi_dung,)
    )

    ket_qua = cursor.fetchone()

    cursor.close()
    conn.close()

    return ket_qua


def cap_nhat_nguoi_dung(ma_nguoi_dung, trang_thai, hien_thi):
    conn = ket_noi_database()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE quan_ly_ban_sach.nguoi_dung
        SET trang_thai_ai = %s,
            hien_thi = %s
        WHERE ma_nguoi_dung = %s
        """,
        (trang_thai, hien_thi, ma_nguoi_dung)
    )

    conn.commit()

    cursor.close()
    conn.close()


# =========================================================
# SACH
# =========================================================

def lay_sach(ma_sach):
    conn = ket_noi_database()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT ten_sach, mo_ta, gia
        FROM quan_ly_ban_sach.sach
        WHERE ma_sach = %s
        """,
        (ma_sach,)
    )

    ket_qua = cursor.fetchone()

    cursor.close()
    conn.close()

    return ket_qua


def cap_nhat_sach(ma_sach, trang_thai, hien_thi):
    conn = ket_noi_database()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE quan_ly_ban_sach.sach
        SET trang_thai_ai = %s,
            hien_thi = %s
        WHERE ma_sach = %s
        """,
        (trang_thai, hien_thi, ma_sach)
    )

    conn.commit()

    cursor.close()
    conn.close()


# =========================================================
# DON HANG
# =========================================================

def lay_don_hang(ma_don_hang):
    conn = ket_noi_database()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT ma_nguoi_dung, tong_tien
        FROM quan_ly_ban_sach.don_hang
        WHERE ma_don_hang = %s
        """,
        (ma_don_hang,)
    )

    ket_qua = cursor.fetchone()

    cursor.close()
    conn.close()

    return ket_qua


def cap_nhat_don_hang(ma_don_hang, trang_thai, hien_thi):
    conn = ket_noi_database()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE quan_ly_ban_sach.don_hang
        SET trang_thai_ai = %s,
            hien_thi = %s
        WHERE ma_don_hang = %s
        """,
        (trang_thai, hien_thi, ma_don_hang)
    )

    conn.commit()

    cursor.close()
    conn.close()


# =========================================================
# CHI TIET DON HANG
# =========================================================

def lay_chi_tiet_don_hang(ma_chi_tiet):
    conn = ket_noi_database()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT ma_don_hang,
               ma_sach,
               so_luong,
               don_gia,
               trang_thai_ai,
               hien_thi
        FROM quan_ly_ban_sach.chi_tiet_don_hang
        WHERE ma_chi_tiet = %s
        """,
        (ma_chi_tiet,)
    )

    ket_qua = cursor.fetchone()

    cursor.close()
    conn.close()

    return ket_qua


def cap_nhat_chi_tiet_don_hang(ma_chi_tiet, trang_thai, hien_thi):
    conn = ket_noi_database()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE quan_ly_ban_sach.chi_tiet_don_hang
        SET trang_thai_ai = %s,
            hien_thi = %s
        WHERE ma_chi_tiet = %s
        """,
        (trang_thai, hien_thi, ma_chi_tiet)
    )

    conn.commit()

    cursor.close()
    conn.close()
