# =========================================================
# AI RULE 1 - KIEM TRA BINH LUAN
# =========================================================

def kiem_tra_binh_luan(noi_dung):

    tu_khoa_vi_pham = [
        "ngu ngốc",
        "đáng vứt đi",
        "đồ ngu",
        "lừa đảo",
        "mẹ mày",
        "địt",
        "fuck",
        "shit"
    ]

    noi_dung_thuong = noi_dung.lower()

    for tu_khoa in tu_khoa_vi_pham:

        if tu_khoa in noi_dung_thuong:
            return True

    return False


# =========================================================
# AI RULE 2 - KIEM TRA SPAM ACCOUNT
# =========================================================

def kiem_tra_spam_account(email):

    danh_sach_domain = [
        "@tempmail",
        "@10minutemail",
        "@guerrillamail",
        "@mailinator",
        "@yopmail"
    ]

    email_thuong = email.lower()

    for domain in danh_sach_domain:

        if domain in email_thuong:
            return True

    return False


# =========================================================
# AI RULE 3 - KIEM TRA SACH
# =========================================================

def kiem_tra_sach(ten_sach, mo_ta, gia):

    loi_gia = False
    du_lieu_rac = False

    # -----------------------------------------------------
    # Kiem tra gia am
    # -----------------------------------------------------

    if gia < 0:
        loi_gia = True

    # -----------------------------------------------------
    # Kiem tra ten sach co qua nhieu ky tu rac
    # -----------------------------------------------------

    ky_tu_rac = [
        "@",
        "#",
        "$",
        "%",
        "^",
        "&",
        "*"
    ]

    so_ky_tu_rac = 0

    for ky_tu in ten_sach:

        if ky_tu in ky_tu_rac:
            so_ky_tu_rac = so_ky_tu_rac + 1

    if len(ten_sach) > 0:

        ty_le_ky_tu_rac = so_ky_tu_rac / len(ten_sach)

        if ty_le_ky_tu_rac >= 0.5:
            du_lieu_rac = True

    # -----------------------------------------------------
    # Neu sach co ca 2 loi
    # -----------------------------------------------------

    if loi_gia and du_lieu_rac:
        return "Loi_Gia_Ban_Du_Lieu_Rac"

    # -----------------------------------------------------
    # Chi loi gia
    # -----------------------------------------------------

    if loi_gia:
        return "Loi_Gia_Ban"

    # -----------------------------------------------------
    # Chi co du lieu rac
    # -----------------------------------------------------

    if du_lieu_rac:
        return "Du_Lieu_Rac"

    return None


# =========================================================
# AI RULE 4 - KIEM TRA SO LUONG MUA
# =========================================================

def kiem_tra_so_luong_mua(so_luong):

    if so_luong > 50:
        return True

    return False


