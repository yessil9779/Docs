SELECT playlist_view.id as epg_playlist_view_id,
    playlist_view.beg_datetime as epg_playlist_view_beg_datetime,
    playlist_view.channel_id as epg_playlist_view_channel_id,
       playlist_view.content_id as epg_playlist_view_content_id,
       playlist_view.episode_id as epg_playlist_view_episode_id,
       playlist_view.is_live as epg_playlist_view_is_live,
       playlist_view.is_premiere as epg_playlist_view_is_premiere,
    playlist_view.is_del as epg_playlist_view_is_del,
    channel_view.name as epg_channel_view_name,
    content_view.id as epg_content_view_id,
    content_view.name as epg_content_view_name,
    content_view.original_id as epg_content_view_original_id,
    content_view.original_name as epg_content_view_original_name,
    content_view.desc_short as epg_content_view_desc_short,
    content_view.desc_normal as epg_content_view_desc_normal,
    content_view.desc_large as epg_content_view_desc_large,
    content_view.category_id as epg_content_view_category_id,
    content_view.country1_id as epg_content_view_country1_id,
    content_view.country2_id as epg_content_view_country2_id,
    content_view.production as epg_content_view_production,
    content_view.years as epg_content_view_years,
    content_view.rating as epg_content_view_rating,
    content_view.kinopoisk as epg_content_view_kinopoisk,
    content_view.id_kinopoisk as epg_content_view_id_kinopoisk,
    content_view.imdb as epg_content_view_imdb,
    content_view.id_imdb as epg_content_view_id_imdb,
    content_view.is_live as epg_content_view_is_live,
    content_view.is_premiere as epg_content_view_is_premiere,
    content_view.budget_currency as epg_content_view_budget_currency,
    content_view.budget_amount as epg_content_view_budget_amount,
    episode_view.id as epg_episode_view_id,
       episode_view.content_id as epg_episode_view_content_id,
    episode_view.name as epg_episode_view_name,
    episode_view.season as epg_episode_view_season,
    episode_view.episode_number as epg_episode_view_episode_number,
    episode_view.part_number as epg_episode_view_part_number,
    episode_view.original_id as epg_episode_view_original_id,
    episode_view.original_name as epg_episode_view_original_name,
    episode_view.desc_short as epg_episode_view_desc_short,
    episode_view.desc_normal as epg_episode_view_desc_normal,
    episode_view.desc_large as epg_episode_view_desc_large,
    episode_view.category_id as epg_episode_view_category_id,
    episode_view.country1_id as epg_episode_view_country1_id,
    episode_view.country2_id as epg_episode_view_country2_id,
    episode_view.production as epg_episode_view_production,
    episode_view.years as epg_episode_view_years,
    episode_view.rating as epg_episode_view_rating,
    episode_view.kinopoisk as epg_episode_view_kinopoisk,
    episode_view.id_kinopoisk as epg_episode_view_id_kinopoisk,
    episode_view.imdb as epg_episode_view_imdb,
    episode_view.id_imdb as epg_episode_view_id_imdb,
    episode_view.is_live as epg_episode_view_is_live,
    episode_view.is_premiere as epg_episode_view_is_premiere,
    episode_view.budget_currency as epg_episode_view_budget_currency,
    episode_view.budget_amount as epg_episode_view_budget_amount,
    category_view.name as epg_category_view_name,
    country_view1.name as epg_country_view1_name,
    country_view2.name as epg_country_view2_name,
    (
        SELECT STRING_AGG(topic_view.name, ', ')
        FROM epg.content_topic_view content_topic_view
        JOIN epg.topic_view topic_view ON content_topic_view.topic_id = topic_view.id
        WHERE content_view.id = content_topic_view.content_id
  ) as epg_topic_view_name,
  (
        SELECT STRING_AGG(production_view.name, ', ')
        FROM epg.content_production_view content_production_view
        JOIN epg.production_view production_view ON content_production_view.production_id = production_view.id
        WHERE content_view.id = content_production_view.content_id
  ) as epg_production_view_name,
  (
        SELECT STRING_AGG(genre_view.name, ', ')
        FROM epg.content_genre_view content_genre_view
        JOIN epg.genre_view genre_view ON content_genre_view.genre_id = genre_view.id
        WHERE content_view.id = content_genre_view.content_id
  ) as epg_genre_view_name,
  (
        SELECT STRING_AGG(person_type_view.name+':'+person_view.name, ', ')
        FROM epg.content_person_view content_person_view
        JOIN epg.person_type_view person_type_view ON content_person_view.type_id = person_type_view.id
        JOIN epg.person_view person_view ON content_person_view.person_id = person_view.id
        WHERE content_view.id = content_person_view.content_id
  ) as epg_person_type_name_person_name

FROM epg.playlist_view playlist_view
LEFT JOIN epg.channel_view channel_view on playlist_view.channel_id = channel_view.id
LEFT JOIN epg.content_view content_view on playlist_view.content_id = content_view.id
LEFT JOIN epg.episode_view episode_view on playlist_view.episode_id = episode_view.id
LEFT JOIN epg.category_view category_view on content_view.category_id = category_view.id
LEFT JOIN epg.country_view country_view1 on content_view.country1_id = country_view1.id
LEFT JOIN epg.country_view country_view2 on content_view.country2_id = country_view2.id

where CAST(playlist_view.channel_id AS INT) = 140
and playlist_view.beg_datetime between ':start_date' and ':end_date'
