table_cte_mapper = {
    'bigquery_onecard_events' : """bigquery_onecard_events AS (
    SELECT
        CAST(FROM_UNIXTIME(event_timestamp/1000000) AS TIMESTAMP) AS event_timestamp,
        DATE_PARSE(event_date, '%Y%m%d') AS event_date,
        event_name,
        CAST(user_id AS BIGINT) AS customer_no,
        platform,
        CASE
            WHEN app_info.id = 'com.creditcard.onecard' THEN 'onecard'
            WHEN app_info.id = 'tech.fplabs.score' THEN 'onescore'
            ELSE NULL
        END AS app_name,
        app_info.version AS app_version,
        device.mobile_brand_name AS mobile_brand,
        device.mobile_model_name AS mobile_model
    FROM
        -- fpl_event.bigquery_onecard_events
        fpl_ds_analytics.sk_sohel_bq_events
        -- ,UNNEST(event_params) AS ep
)""",
    'score_event_tracker' : """score_event_tracker AS (
    SELECT
        created_at AS event_timestamp,
        customer_no,
        tenant_id,
        primary_event AS primary_event_name,
        secondary_event AS secondary_event_name,
        tertiary_event AS tertiary_event_name,
        status,
        product_code,
        journey AS journey_stage,
        details AS event_details
    FROM
        fpl_ds_onboarding.BOFU_L1_score_event_tracker
)""",
    'all_bank_vc' : """all_bank_vc AS (
    SELECT
        CAST(realid AS BIGINT) AS customer_no, 
        regis_date AS registration_timestamp,
        credit_limit,
        bank_name,
        product_type,
        final_channel,
        status,
        virtual_activation_date
    FROM(
        SELECT
            realid, 
            regis_date,
            credit_limit,
            bank_name,
            product_type,
            final_channel,
            status,
            virtual_activation_date
        FROM
            fpl_ds_onboarding_l2.BOB_bofu_l2_all_bank_vc 
        UNION ALL
        SELECT
            realid, 
            regis_date,
            credit_limit,
            bank_name,
            product_type,
            final_channel,
            status,
            virtual_activation_date
        FROM
            fpl_ds_onboarding_l2.IDIB_bofu_l2_all_bank_vc 
        UNION ALL
        SELECT
            realid, 
            regis_date,
            credit_limit,
            bank_name,
            product_type,
            final_channel,
            status,
            virtual_activation_date
        FROM
            fpl_ds_onboarding_l2.SIB_bofu_l2_all_bank_vc 
        UNION ALL
        SELECT
            realid, 
            regis_date,
            credit_limit,
            bank_name,
            product_type,
            final_channel,
            status,
            virtual_activation_date
        FROM
            fpl_ds_onboarding_l2.FED_bofu_l2_all_bank_vc 
        UNION ALL
        SELECT
            realid, 
            regis_date,
            credit_limit,
            bank_name,
            product_type,
            final_channel,
            status,
            virtual_activation_date
        FROM
            fpl_ds_onboarding_l2.SBM_bofu_l2_all_bank_vc 
        )
    )"""
}