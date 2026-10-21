
"""BookParadise AI Optimizer - giam sat hieu nang tim kiem sach."""

import re
import time

import psycopg2
from database import ket_noi_database


POLL_SECONDS = 1
BATCH_SIZE = 100

# Nguong thoi gian tim kiem (mili giay).
SLOW_THRESHOLD_MS = 2000
VERY_SLOW_THRESHOLD_MS = 5000


def phan_tich_tim_kiem(description):
    """Doc thoi gian tim kiem tu mo ta su kien."""

    ket_qua = re.search(
        r"mất\s+(\d+)\s*ms",
        description or "",
        re.IGNORECASE,
    )

    if not ket_qua:
        return 0, "Info", (
            "Chua doc duoc thoi gian tim kiem tu mo ta su kien."
        )

    thoi_gian_ms = int(ket_qua.group(1))

    if thoi_gian_ms >= VERY_SLOW_THRESHOLD_MS:
        return thoi_gian_ms, "High", (
            f"Tim kiem rat cham: {thoi_gian_ms} ms. "
            "Can kiem tra truy van SQL, index va tai database."
        )

    if thoi_gian_ms > SLOW_THRESHOLD_MS:
        return thoi_gian_ms, "Medium", (
            f"Tim kiem cham: {thoi_gian_ms} ms. "
            "Nen kiem tra truy van SQL va du lieu tra ve."
        )

    return thoi_gian_ms, "Info", (
        f"Thoi gian tim kiem: {thoi_gian_ms} ms."
    )


def xu_ly_su_kien(cursor, event):
    """Phan tich va cap nhat mot su kien slow_search."""

    event_id, source_ip, description, is_simulated = event

    thoi_gian_ms, muc_do, ket_luan = phan_tich_tim_kiem(
        description
    )

    if thoi_gian_ms >= VERY_SLOW_THRESHOLD_MS:
        diem = 80
    elif thoi_gian_ms > SLOW_THRESHOLD_MS:
        diem = 60
    else:
        diem = 0

    cursor.execute(
        """
        UPDATE quan_ly_ban_sach.security_events
        SET risk_score = %s,
            severity = %s,
            analysis_result = %s,
            detection_status = 'Detected'
        WHERE id = %s
          AND event_type = 'slow_search'
          AND detection_status = 'Pending'
        """,
        (diem, muc_do, ket_luan, event_id),
    )

    # Chi in ket qua khi cap nhat thanh cong.
    if cursor.rowcount == 0:
        return

    nhan = "MO PHONG" if is_simulated else "THUC TE"

    if thoi_gian_ms > SLOW_THRESHOLD_MS:
        print(
            f"\n[AI OPTIMIZER][{muc_do}][{nhan}] "
            f"ID={event_id} | "
            f"IP={source_ip} | "
            f"Thoi gian={thoi_gian_ms} ms",
            flush=True,
        )
        print(f"Phan tich: {ket_luan}", flush=True)
        print("-" * 65, flush=True)
    else:
        print(
            f"[AI OPTIMIZER][INFO] ID={event_id} | {ket_luan}",
            flush=True,
        )


def main():
    print("=" * 65)
    print("BOOKPARADISE AI OPTIMIZER")
    print("Dang giam sat su kien slow_search trong PostgreSQL.")
    print("Canh bao: tren 2000 ms.")
    print("Rat cham: tu 5000 ms tro len.")
    print("Nhan Ctrl+C de dung.")
    print("=" * 65)

    conn = ket_noi_database()

    try:
        conn.set_isolation_level(
            psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
        )

        with conn.cursor() as cursor:
            while True:
                cursor.execute(
                    """
                    SELECT id, source_ip, description, is_simulated
                    FROM quan_ly_ban_sach.security_events
                    WHERE event_type = 'slow_search'
                      AND detection_status = 'Pending'
                    ORDER BY id
                    LIMIT %s
                    """,
                    (BATCH_SIZE,),
                )

                events = cursor.fetchall()

                if not events:
                    time.sleep(POLL_SECONDS)
                    continue

                for event in events:
                    try:
                        xu_ly_su_kien(cursor, event)
                    except psycopg2.Error as exc:
                        print(
                            f"[LOI DB] Khong xu ly duoc "
                            f"su kien ID={event[0]}: {exc}",
                            flush=True,
                        )

    except KeyboardInterrupt:
        print("\nAI Optimizer da dung.")

    except psycopg2.Error as exc:
        print(
            f"[LOI KET NOI DATABASE] {exc}",
            flush=True,
        )

    finally:
        conn.close()


if __name__ == "__main__":
    main()
