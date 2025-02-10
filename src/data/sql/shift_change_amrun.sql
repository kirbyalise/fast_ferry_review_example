WITH OrderedEvents AS (
SELECT
   Event.start_timestamp
   , Event.end_timestamp
   , Status.STATUS_DESC
   , Event.equip_ident
   , Haul.START_SHIFT_DATE
   ,CASE
       WHEN
           (CAST(Event.start_timestamp AS TIME) >= '03:00:00' AND CAST(Event.start_timestamp AS TIME) < '11:00:00')
           OR (CAST(Event.end_timestamp AS TIME) > '03:00:00' AND CAST(Event.end_timestamp AS TIME) <= '11:00:00') THEN '1'
       WHEN
           (CAST(Event.start_timestamp AS TIME) >= '15:00:00' AND CAST(Event.start_timestamp AS TIME) < '23:00:00')
           OR (CAST(Event.end_timestamp AS TIME) > '15:00:00' AND CAST(Event.end_timestamp AS TIME) <= '23:00:00') THEN '2'
   END AS shift
   , LAG(Event.end_timestamp) OVER (
       PARTITION BY
           Event.equip_ident,
           CASE
               WHEN
                   (CAST(Event.start_timestamp AS TIME) >= '03:00:00' AND CAST(Event.start_timestamp AS TIME) < '11:00:00')
                   OR (CAST(Event.end_timestamp AS TIME) > '03:00:00' AND CAST(Event.end_timestamp AS TIME) <= '11:00:00') THEN '1'
               WHEN
                   (CAST(Event.start_timestamp AS TIME) >= '15:00:00' AND CAST(Event.start_timestamp AS TIME) < '23:00:00')
                   OR (CAST(Event.end_timestamp AS TIME) > '15:00:00' AND CAST(Event.end_timestamp AS TIME) <= '23:00:00') THEN '2'
           END
       ORDER BY Event.start_timestamp
   ) AS prev_end_timestamp
FROM ODS_WENCO.DAL.dbo_HAUL_CYCLE_TRANS Haul
LEFT JOIN ODS_WENCO.DAL.dbo_HAUL_UNIT_STATUS_TRANS_COL HaulKey
   ON Haul.HAUL_CYCLE_REC_IDENT = HaulKey.HAUL_CYCLE_REC_IDENT
INNER JOIN ODS_WENCO.DAL.dbo_EQUIP_STATUS_TRANS Event
   ON HaulKey.EQUIP_STATUS_REC_IDENT = Event.equip_status_rec_ident
LEFT JOIN ODS_WENCO.DAL.dbo_EQUIP_STATUS_CODE Status
   ON Event.status_code = Status.STATUS_CODE
WHERE Status.STATUS_DESC = 'SHIFT CHANGE'
   AND Haul.START_SHIFT_DATE BETWEEN '2023-01-01' AND '2024-11-28'
   AND Haul.LOAD_LOCATION_SNAME like '%amr%'
   AND Event.equip_ident like '29%'
),
GroupedEvents AS (
SELECT
   OE.start_timestamp,
   OE.end_timestamp,
   OE.equip_ident,
   OE.STATUS_DESC,
   OE.shift,
   SUM(CASE WHEN prev_end_timestamp IS NULL OR prev_end_timestamp < start_timestamp THEN 1 ELSE 0 END)
       OVER (PARTITION BY STATUS_DESC, equip_ident, shift ORDER BY start_timestamp) AS group_id
FROM OrderedEvents as OE
)
SELECT
   MIN(start_timestamp) AS start_time,
   MAX(end_timestamp) AS end_time,
   equip_ident,
   shift,
   STATUS_DESC,
   ROUND(SUM(DATEDIFF(SECOND , start_timestamp, end_timestamp)/60.0), 1) AS total_combined_minutes
FROM GroupedEvents
GROUP BY STATUS_DESC, equip_ident, shift, group_id
ORDER BY start_time DESC;