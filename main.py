import psycopg2

import select



from database import (

    ket_noi_database,

    lay_binh_luan,

    cap_nhat_binh_luan,



    lay_nguoi_dung,

    cap_nhat_nguoi_dung,



    lay_sach,

    cap_nhat_sach,



    lay_don_hang,
    cap_nhat_don_hang,

    lay_chi_tiet_don_hang,

    cap_nhat_chi_tiet_don_hang

)



from ai_rules import (

    kiem_tra_binh_luan,

    kiem_tra_spam_account,

    kiem_tra_sach,

    kiem_tra_so_luong_mua,

    kiem_tra_gia_mua

)





# =========================================================

# KET NOI POSTGRESQL

# =========================================================



conn = ket_noi_database()



conn.set_isolation_level(

    psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT

)



cursor = conn.cursor()





# =========================================================

# LISTEN 5 KENH

# =========================================================



cursor.execute("LISTEN kenh_binh_luan;")

cursor.execute("LISTEN kenh_nguoi_dung;")

cursor.execute("LISTEN kenh_sach;")

cursor.execute("LISTEN kenh_don_hang;")

cursor.execute("LISTEN kenh_chi_tiet_don_hang;")





print("========================================")

print("BOOKPARADISE AI WORKER")

print("========================================")

print("Python AI Worker dang cho PostgreSQL...")

print("Dang LISTEN 5 kenh:")

print("- kenh_binh_luan")

print("- kenh_nguoi_dung")

print("- kenh_sach")

print("- kenh_don_hang")

print("- kenh_chi_tiet_don_hang")

print("========================================")





# =========================================================

# VONG LAP CHINH

# =========================================================



while True:



    if select.select([conn], [], [], 5) == ([], [], []):

        continue



    conn.poll()



    while conn.notifies:



        thong_bao = conn.notifies.pop(0)



        kenh = thong_bao.channel

        payload = thong_bao.payload



        print()

        print("========================================")

        print("CO DU LIEU MOI")

        print("Kenh:", kenh)

        print("Ma du lieu:", payload)

        print("========================================")





        # =================================================

        # BINH LUAN

        # =================================================



        if kenh == "kenh_binh_luan":



            ma_binh_luan = int(payload)



            noi_dung = lay_binh_luan(ma_binh_luan)



            if noi_dung is None:



                print("Khong tim thay binh luan.")



                continue



            print("Noi dung:", noi_dung)



            vi_pham = kiem_tra_binh_luan(noi_dung)



            if vi_pham:



                print("⚠ CANH BAO AI")

                print("Phat hien binh luan vi pham!")



                cap_nhat_binh_luan(

                    ma_binh_luan,

                    "Vi_Pham_Tieu_Chuan",

                    False

                )



                print("Trang thai: Vi_Pham_Tieu_Chuan")

                print("Hien thi: FALSE")



            else:



                print("✓ Binh luan hop le.")



                cap_nhat_binh_luan(

                    ma_binh_luan,

                    "Cho_Kiem_Duyet",

                    True

                )



                print("Trang thai: Cho_Kiem_Duyet")

                print("Hien thi: TRUE")





        # =================================================

        # NGUOI DUNG

        # =================================================



        elif kenh == "kenh_nguoi_dung":



            ma_nguoi_dung = int(payload)



            nguoi_dung = lay_nguoi_dung(ma_nguoi_dung)



            if nguoi_dung is None:



                print("Khong tim thay nguoi dung.")



                continue



            ho_ten = nguoi_dung[0]

            email = nguoi_dung[1]



            print("Ho ten:", ho_ten)

            print("Email:", email)



            spam = kiem_tra_spam_account(email)



            if spam:



                print("⚠ CANH BAO AI")

                print("Phat hien tai khoan spam!")



                cap_nhat_nguoi_dung(

                    ma_nguoi_dung,

                    "Spam_Account",

                    False

                )



                print("Trang thai: Spam_Account")

                print("Hien thi: FALSE")



            else:



                print("✓ Tai khoan binh thuong.")



                cap_nhat_nguoi_dung(

                    ma_nguoi_dung,

                    "Cho_Kiem_Duyet",

                    True

                )



                print("Trang thai: Cho_Kiem_Duyet")

                print("Hien thi: TRUE")





        # =================================================

        # SACH

        # =================================================



        elif kenh == "kenh_sach":



            ma_sach = int(payload)



            sach = lay_sach(ma_sach)



            if sach is None:



                print("Khong tim thay sach.")



                continue



            ten_sach = sach[0]

            mo_ta = sach[1]

            gia = float(sach[2])



            print("Ten sach:", ten_sach)

            print("Gia:", gia)



            ket_qua = kiem_tra_sach(

                ten_sach,

                mo_ta,

                gia

            )



            if ket_qua == "Loi_Gia_Ban_Du_Lieu_Rac":



                print("⚠ CANH BAO AI")

                print("Phat hien nhieu loi trong sach!")

                print("- Gia sach bi am")

                print("- Ten sach chua qua nhieu ky tu rac")



                cap_nhat_sach(

                    ma_sach,

                    "Loi_Gia_Ban_Du_Lieu_Rac",

                    False

                )



                print("Trang thai: Loi_Gia_Ban_Du_Lieu_Rac")

                print("Hien thi: FALSE")



            elif ket_qua == "Loi_Gia_Ban":



                print("⚠ CANH BAO AI")

                print("Phat hien gia sach bat thuong!")



                cap_nhat_sach(

                    ma_sach,

                    "Loi_Gia_Ban",

                    False

                )



                print("Trang thai: Loi_Gia_Ban")

                print("Hien thi: FALSE")



            elif ket_qua == "Du_Lieu_Rac":



                print("⚠ CANH BAO AI")

                print("Phat hien du lieu sach rac!")



                cap_nhat_sach(

                    ma_sach,

                    "Du_Lieu_Rac",

                    False

                )



                print("Trang thai: Du_Lieu_Rac")

                print("Hien thi: FALSE")



            else:



                print("✓ Sach hop le.")



                cap_nhat_sach(

                    ma_sach,

                    "Cho_Kiem_Duyet",

                    True

                )



                print("Trang thai: Cho_Kiem_Duyet")

                print("Hien thi: TRUE")





        # =================================================

        # DON HANG

        # =================================================



        elif kenh == "kenh_don_hang":



            ma_don_hang = int(payload)



            don_hang = lay_don_hang(ma_don_hang)



            if don_hang is None:



                print("Khong tim thay don hang.")



                continue



            ma_nguoi_dung = don_hang[0]

            tong_tien = float(don_hang[1])



            print("Ma nguoi dung:", ma_nguoi_dung)

            print("Tong tien:", tong_tien)



            print("✓ Don hang da duoc ghi nhan.")



            # Phan kiem tra so luong nam o

            # kenh_chi_tiet_don_hang.





        # =================================================

        # CHI TIET DON HANG

        # =================================================



        elif kenh == "kenh_chi_tiet_don_hang":



            ma_chi_tiet = int(payload)



            chi_tiet = lay_chi_tiet_don_hang(

                ma_chi_tiet

            )



            if chi_tiet is None:



                print("Khong tim thay chi tiet don hang.")



                continue



            ma_don_hang = chi_tiet[0]

            ma_sach = chi_tiet[1]

            so_luong = chi_tiet[2]

            don_gia = float(chi_tiet[3])



            print("Ma don hang:", ma_don_hang)

            print("Ma sach:", ma_sach)

            print("So luong:", so_luong)

            print("Don gia:", don_gia)



            bat_thuong_so_luong = kiem_tra_so_luong_mua(

                so_luong

            )



            bat_thuong_gia = kiem_tra_gia_mua(

                don_gia

            )



            # -------------------------------------------------

            # CA 2 LOI

            # -------------------------------------------------



            if bat_thuong_so_luong and bat_thuong_gia:



                print("⚠ CANH BAO AI")

                print("Phat hien nhieu bat thuong!")

                print("- So luong mua qua lon")

                print("- Don gia bi am")



                print("So luong:", so_luong)

                print("Nguong:", 50)

                print("Don gia:", don_gia)



                cap_nhat_chi_tiet_don_hang(

                    ma_chi_tiet,

                    "Canh_Bao_Dau_Co_Loi_Gia",

                    False

                )



                cap_nhat_don_hang(

                    ma_don_hang,

                    "Canh_Bao_Dau_Co",

                    False

                )



                print("Trang thai ChiTietDonHang: Canh_Bao_Dau_Co_Loi_Gia")

                print("Trang thai DonHang: Canh_Bao_Dau_Co")

                print("Hien thi: FALSE")





            # -------------------------------------------------

            # CHI SO LUONG BAT THUONG

            # -------------------------------------------------



            elif bat_thuong_so_luong:



                print("⚠ CANH BAO AI")

                print("Phat hien so luong mua bat thuong!")

                print("So luong:", so_luong)

                print("Nguong:", 50)



                cap_nhat_chi_tiet_don_hang(

                    ma_chi_tiet,

                    "Canh_Bao_Dau_Co",

                    False

                )



                cap_nhat_don_hang(

                    ma_don_hang,

                    "Canh_Bao_Dau_Co",

                    False

                )



                print("Trang thai ChiTietDonHang: Canh_Bao_Dau_Co")

                print("Trang thai DonHang: Canh_Bao_Dau_Co")

                print("Hien thi: FALSE")





            # -------------------------------------------------

            # CHI DON GIA BAT THUONG

            # -------------------------------------------------



            elif bat_thuong_gia:



                print("⚠ CANH BAO AI")

                print("Phat hien don gia bat thuong!")

                print("Don gia:", don_gia)



                cap_nhat_chi_tiet_don_hang(

                    ma_chi_tiet,

                    "Loi_Gia_Ban",

                    False

                )



                print("Trang thai: Loi_Gia_Ban")

                print("Hien thi: FALSE")





            # -------------------------------------------------

            # HOP LE

            # -------------------------------------------------



            else:



                print("✓ Chi tiet don hang hop le.")



                cap_nhat_chi_tiet_don_hang(

                    ma_chi_tiet,

                    "Cho_Kiem_Duyet",

                    True

                )



                print("Trang thai: Cho_Kiem_Duyet")

                print("Hien thi: TRUE")





        else:



            print("Kenh khong duoc xu ly:", kenh)
