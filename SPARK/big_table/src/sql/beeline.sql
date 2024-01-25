SELECT e.channel_id as beeline_efir_view_channel_id,
    e.efir_date as beeline_efir_view_efir_date,
    e.time_view as beeline_efir_view_time_view,
    e.scope as beeline_efir_view_scope,
    e.cnt_connect as beeline_efir_view_cnt_connect,
    e.cnt_disconnect as beeline_efir_view_cnt_disconnect,
    e.time_view_avg as beeline_efir_view_time_view_avg,
    e.time_view_avg_connect as beeline_efir_view_time_view_avg_connect,
    e.scope_avg as beeline_efir_view_scope_avg,
    e.tvr as beeline_efir_view_tvr,
    e.cnt as beeline_efir_view_cnt,
    e.tvr_max as beeline_efir_view_tvr_max,
    e.cnt_max as beeline_efir_view_cnt_max,
    e.efir_beg_date as beeline_efir_view_efir_beg_date,
    e.efir_end_date as beeline_efir_view_efir_end_date,
    c.bv_id as beeline_channel_view_bv_id

FROM olap.beeline.efir_view e
JOIN olap.dbo.channel_view c on c.id = e.channel_id
where e.efir_date between ':start_date' and ':end_date'
