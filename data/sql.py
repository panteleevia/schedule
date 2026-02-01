from sqlalchemy import create_engine
import pandas as pd

DB_USER = "i.panteleev"
DB_PASSWORD = "aeLrTz1VXLCzPbIIaXNtXOJLtM3rDWaG"
DB_HOST = "192.168.2.126"
DB_PORT = 3306
DB_NAME = "support"

def get_schedule():
    engine = create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    query = """
    SELECT
        day_of_week,
        day_number,
        hour,
        CEIL(AVG(daily_ticket_count)/8) AS avg_operators_needed
    FROM (
        SELECT
            DAYNAME(s.created_at) AS day_of_week,
            DAYOFWEEK(s.created_at) AS day_number,
            HOUR(s.created_at) AS hour,
            DATE(s.created_at) AS date,
            AVG(s.`time`) AS avg_response_time,
            COUNT(*) AS daily_ticket_count
        FROM support.stat_expectation AS s
        JOIN support.ticket_list AS t ON t.id = s.ticket_id
        LEFT JOIN support.ticket_comments AS delay_comment
            ON delay_comment.ticket_id = s.ticket_id
            AND delay_comment.type = 'delay'
            AND (
                UNIX_TIMESTAMP(delay_comment.date) BETWEEN UNIX_TIMESTAMP(s.created_at) - s.time
                AND UNIX_TIMESTAMP(s.created_at)
            )
        LEFT JOIN support.ticket_comments AS transferred_comment
            ON transferred_comment.ticket_id = s.ticket_id
            AND transferred_comment.type = 'transfer'
            AND (
                UNIX_TIMESTAMP(transferred_comment.date) BETWEEN UNIX_TIMESTAMP(s.created_at) - s.time
                AND UNIX_TIMESTAMP(s.created_at)
            )
        WHERE s.created_at >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
            AND delay_comment.id IS NULL
            AND transferred_comment.id IS NULL
            AND s.department in ('support_l2', 'support_cloud', 'support_cloud_l2 ')
        GROUP BY DAYOFWEEK(s.created_at), DAYNAME(s.created_at), HOUR(s.created_at), DATE(s.created_at)
    ) AS daily_stats
    GROUP BY day_of_week, day_number, hour
    """

    df_stats = pd.read_sql(query, engine)
    return df_stats