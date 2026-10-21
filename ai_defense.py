
"""BookParadise AI Defense - phat hien su kien bao mat bang quy tac."""

import re
import time

import psycopg2
from database import ket_noi_database


POLL_SECONDS = 1
BATCH_SIZE = 100

# Han che in canh bao trung trong cung tien trinh.
canh_bao_da_in = {}


def nen_in_canh_bao(event_type, source_ip, mo_ta, muc_do):
    """Han che canh bao trung trong 60 giay."""

    now = time.time()

    het_han = [
        key for key, thoi_diem in canh_bao_da_in.items()
        if now - thoi_diem >= 60
    ]

    for key in het_han:
        del canh_bao_da_in[key]

    api = ""
    noi_dung = ""

    if event_type == "request_burst":
        ket_qua_api = re.search(
            r"\bvao\s+(.+)$",
            mo_ta,
            re.IGNORECASE,
        )

        if ket_qua_api:
            api = ket_qua_api.group(1).strip()

    elif event_type == "suspicious_input":
        # Phan biet cac dau vao khac nhau de khong mat canh bao.
        noi_dung = mo_ta

    khoa = (event_type, source_ip, api, muc_do, noi_dung)

    if khoa in canh_bao_da_in:
        return False

    canh_bao_da_in[khoa] = now
    return True


def phan_tich_su_kien(
    cursor,
    event_id,
    event_type,
    source_ip,
    is_simulated,
):
    diem = 0
    muc_do = "Info"
    ly_do = "Chua phat hien bat thuong theo cac quy tac hien co."
    mo_ta = ""

    # Lay mo ta chi tiet cua su kien.
    cursor.execute(
        """
        SELECT description
        FROM quan_ly_ban_sach.security_events
        WHERE id = %s
        """,
        (event_id,),
    )

    ket_qua = cursor.fetchone()
    if ket_qua:
        mo_ta = ket_qua[0] or ""

    # --------------------------------------------------
    # 1. DANG NHAP THAT BAI
    # --------------------------------------------------
    if event_type == "login_failed":
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM quan_ly_ban_sach.security_events AS hien_tai
            JOIN quan_ly_ban_sach.security_events AS su_kien
              ON su_kien.id = %s
            WHERE hien_tai.event_type = 'login_failed'
              AND hien_tai.source_ip = su_kien.source_ip
              AND hien_tai.created_at >=
                  su_kien.created_at - INTERVAL '5 minutes'
              AND hien_tai.created_at <= su_kien.created_at
              AND hien_tai.id <= su_kien.id
            """,
            (event_id,),
        )

        so_lan = cursor.fetchone()[0]

        if so_lan >= 5:
            diem = 85
            ly_do = (
                f"Phat hien {so_lan} lan dang nhap that bai "
                "tu cung IP trong 5 phut."
            )
        elif so_lan >= 3:
            diem = 55
            ly_do = (
                f"Co {so_lan} lan dang nhap that bai "
                "tu cung IP trong 5 phut; can theo doi."
            )
        else:
            diem = 0
            ly_do = (
                f"Ghi nhan {so_lan} lan dang nhap that bai "
                "tu cung IP trong 5 phut; tiep tuc theo doi."
            )

    # --------------------------------------------------
    # 2. REQUEST TANG DOT BIEN
    # --------------------------------------------------
    elif event_type == "request_burst":
        ket_qua_so_luong = re.search(
            r"(\d+)\s+requests?\s*(?:/\s*)?"
            r"(?:phút|phut|minute)",
            mo_ta,
            re.IGNORECASE,
        )

        so_request = (
            int(ket_qua_so_luong.group(1))
            if ket_qua_so_luong
            else 0
        )

        if so_request >= 20:
            diem = 85
            ly_do = (
                f"Phat hien {so_request} request/phut tu cung IP; "
                "co dau hieu spam API nghiem trong."
            )
        elif so_request >= 10:
            diem = 70
            ly_do = (
                f"Phat hien {so_request} request/phut tu cung IP; "
                "co dau hieu tang dot bien."
            )
        elif so_request >= 5:
            diem = 45
            ly_do = (
                f"Phat hien {so_request} request/phut tu cung IP; "
                "vuot nguong theo doi."
            )
        elif so_request >= 3:
            diem = 0
            ly_do = (
                f"Ghi nhan {so_request} request/phut tu cung IP; "
                "muc Info, tiep tuc theo doi."
            )

    # --------------------------------------------------
    # 3. DAU VAO DANG NGO
    # --------------------------------------------------
    elif event_type == "suspicious_input":
        diem = 90
        ly_do = (
            "Phat hien dau vao co mau dang ngo; "
            "can kiem tra noi dung binh luan."
        )

    # --------------------------------------------------
    # XAC DINH MUC DO
    # --------------------------------------------------
    if diem >= 80:
        muc_do = "High"
    elif diem >= 50:
        muc_do = "Medium"
    elif diem > 0:
        muc_do = "Low"
    else:
        muc_do = "Info"

    # Cap nhat ket qua phan tich vao database.
    cursor.execute(
        """
        UPDATE quan_ly_ban_sach.security_events
        SET risk_score = %s,
            severity = %s,
            analysis_result = %s,
            detection_status = 'Detected'
        WHERE id = %s
        """,
        (diem, muc_do, ly_do, event_id),
    )

    if nen_in_canh_bao(event_type, source_ip, mo_ta, muc_do):
        prefix = "GIA LAP" if is_simulated else "SU KIEN"

        print(
            f"\n[{prefix}][{muc_do}] "
            f"ID={event_id} | {diem}/100",
            flush=True,
        )
        print(f"Loai su kien: {event_type}", flush=True)
        print(f"IP: {source_ip}", flush=True)
        print(f"Mo ta: {mo_ta}", flush=True)
        print(f"Ket qua AI: {ly_do}", flush=True)

        if event_type == "login_failed":
            print(
                "Luu y: He thong ghi nhan dang nhap that bai.",
                flush=True,
            )

        elif event_type == "suspicious_input":
            print(
                "Luu y: Kiem tra noi dung dau vao ben duoi "
                "neu mo ta co luu noi dung.",
                flush=True,
            )

        print("-" * 60, flush=True)


def main():
    print("=" * 60)
    print("BOOKPARADISE AI DEFENSE")
    print("Dang giam sat security_events; nhan Ctrl+C de dung.")
    print("Login failed: 3 lan = Medium, 5 lan = High.")
    print("Request burst: 3 = Info, 5 = Low, 10 = Medium, 20 = High.")
    print("Suspicious input: High, 90/100.")
    print("Bo phat hien theo quy tac, khong phai mo hinh ML.")
    print("=" * 60)

    conn = ket_noi_database()

    try:
        conn.set_isolation_level(
            psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
        )

        with conn.cursor() as cursor:
            while True:
                cursor.execute(
                    """
                    SELECT id, event_type, source_ip, is_simulated
                    FROM quan_ly_ban_sach.security_events
                    WHERE detection_status = 'Pending'
                    AND event_type <> 'slow_search'
                    ORDER BY id
                    LIMIT %s
                    """,
                    (BATCH_SIZE,),
                )

                events = cursor.fetchall()

                if not events:
                    time.sleep(POLL_SECONDS)
                    continue

                for (
                    event_id,
                    event_type,
                    source_ip,
                    is_simulated,
                ) in events:
                    try:
                        phan_tich_su_kien(
                            cursor,
                            event_id,
                            event_type,
                            source_ip,
                            is_simulated,
                        )

                    except psycopg2.Error as exc:
                        print(
                            f"[LOI] Su kien ID={event_id}: {exc}",
                            flush=True,
                        )

                        cursor.execute(
                            """
                            UPDATE quan_ly_ban_sach.security_events
                            SET detection_status = 'Error',
                                analysis_result = %s
                            WHERE id = %s
                            """,
                            (
                                "Loi khi phan tich: " + str(exc)[:500],
                                event_id,
                            ),
                        )

    except KeyboardInterrupt:
        print("\nAI Defense da dung.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
