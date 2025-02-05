from typing import Optional, Literal
from pydantic import BaseModel, Field


class DigitalLifestyle(BaseModel):
    """DigitalLifestyle Model with structured formatting."""

    Thinking_about_how_you_engage_with_the_digital_world_generally_which_of_the_following_statements_do_you_agree_with: Optional[
        Literal[
            "base",
            "i_actively_seek_to_improve_my_digital/computing_skills",
            "i_enjoy_having_so_much_information_at_my_fingertips",
            "nowadays_it_is_important_to_understand_the_digital_world_if_you_want_a_career",
            "i_feel_forced_to_be_online",
            "my_digital_skills_give_me_a_greater_sense_of_freedom",
            "digital_skills_are_essential_for_everyday_life",
            "the_covid-19_pandemic_and_lockdown_have_pushed_me_to_improve_my_digital_skills",
            "none_of_the_above",
        ]
    ] = Field(
        default=None,
        description="Thinking_about_how_you_engage_with_the_digital_world_generally_which_of_the_following_statements_do_you_agree_with",
    )
    Thinking_about_your_current_level_of_digital_expertise_please_rate_your_level_of_competence_understanding_about_the_following_digital_topics_or_Searching_for_information_online: Optional[
        Literal[
            "base",
            "very_good",
            "good",
            "neither_good_nor_bad",
            "bad",
            "very_bad",
            "never_tried",
            "dont_know",
        ]
    ] = Field(
        default=None,
        description="Thinking_about_your_current_level_of_digital_expertise_please_rate_your_level_of_competence_understanding_about_the_following_digital_topics_or_Searching_for_information_online",
    )
    Thinking_about_your_current_level_of_digital_expertise_please_rate_your_level_of_competence_understanding_about_the_following_digital_topics_or_Using_office_packages: Optional[
        Literal[
            "base",
            "very_good",
            "good",
            "neither_good_nor_bad",
            "bad",
            "very_bad",
            "never_tried",
            "dont_know",
        ]
    ] = Field(
        default=None,
        description="Thinking_about_your_current_level_of_digital_expertise_please_rate_your_level_of_competence_understanding_about_the_following_digital_topics_or_Using_office_packages",
    )
    Thinking_about_your_current_level_of_digital_expertise_please_rate_your_level_of_competence_understanding_about_the_following_digital_topics_or_Using_email: Optional[
        Literal[
            "base",
            "very_good",
            "good",
            "neither_good_nor_bad",
            "bad",
            "very_bad",
            "never_tried",
            "dont_know",
        ]
    ] = Field(
        default=None,
        description="Thinking_about_your_current_level_of_digital_expertise_please_rate_your_level_of_competence_understanding_about_the_following_digital_topics_or_Using_email",
    )
    Thinking_about_your_current_level_of_digital_expertise_please_rate_your_level_of_competence_understanding_about_the_following_digital_topics_or_Using_social_media: Optional[
        Literal[
            "base",
            "very_good",
            "good",
            "neither_good_nor_bad",
            "bad",
            "very_bad",
            "never_tried",
            "dont_know",
        ]
    ] = Field(
        default=None,
        description="Thinking_about_your_current_level_of_digital_expertise_please_rate_your_level_of_competence_understanding_about_the_following_digital_topics_or_Using_social_media",
    )
    Thinking_about_your_current_level_of_digital_expertise_please_rate_your_level_of_competence_understanding_about_the_following_digital_topics_or_Using_messenger_services: Optional[
        Literal[
            "base",
            "very_good",
            "good",
            "neither_good_nor_bad",
            "bad",
            "very_bad",
            "never_tried",
            "dont_know",
        ]
    ] = Field(
        default=None,
        description="Thinking_about_your_current_level_of_digital_expertise_please_rate_your_level_of_competence_understanding_about_the_following_digital_topics_or_Using_messenger_services",
    )
    Thinking_about_your_current_level_of_digital_expertise_please_rate_your_level_of_competence_understanding_about_the_following_digital_topics_or_Video_calling_apps: Optional[
        Literal[
            "base",
            "very_good",
            "good",
            "neither_good_nor_bad",
            "bad",
            "very_bad",
            "never_tried",
            "dont_know",
        ]
    ] = Field(
        default=None,
        description="Thinking_about_your_current_level_of_digital_expertise_please_rate_your_level_of_competence_understanding_about_the_following_digital_topics_or_Video_calling_apps",
    )
    Thinking_about_your_current_level_of_digital_expertise_please_rate_your_level_of_competence_understanding_about_the_following_digital_topics_or_Setting_up_accounts_on_websitesorservices: Optional[
        Literal[
            "base",
            "very_good",
            "good",
            "neither_good_nor_bad",
            "bad",
            "very_bad",
            "never_tried",
            "dont_know",
        ]
    ] = Field(
        default=None,
        description="Thinking_about_your_current_level_of_digital_expertise_please_rate_your_level_of_competence_understanding_about_the_following_digital_topics_or_Setting_up_accounts_on_websitesorservices",
    )
    Thinking_about_your_current_level_of_digital_expertise_please_rate_your_level_of_competence_understanding_about_the_following_digital_topics_or_Online_shopping: Optional[
        Literal[
            "base",
            "very_good",
            "good",
            "neither_good_nor_bad",
            "bad",
            "very_bad",
            "never_tried",
            "dont_know",
        ]
    ] = Field(
        default=None,
        description="Thinking_about_your_current_level_of_digital_expertise_please_rate_your_level_of_competence_understanding_about_the_following_digital_topics_or_Online_shopping",
    )
    Thinking_about_your_current_level_of_digital_expertise_please_rate_your_level_of_competence_understanding_about_the_following_digital_topics_or_Problem_solving_ie_using_FAQsortutorialsorchats: Optional[
        Literal[
            "base",
            "very_good",
            "good",
            "neither_good_nor_bad",
            "bad",
            "very_bad",
            "never_tried",
            "dont_know",
        ]
    ] = Field(
        default=None,
        description="Thinking_about_your_current_level_of_digital_expertise_please_rate_your_level_of_competence_understanding_about_the_following_digital_topics_or_Problem_solving_ie_using_FAQsortutorialsorchats",
    )
    Thinking_about_your_current_level_of_digital_expertise_please_rate_your_level_of_competence_understanding_about_the_following_digital_topics_or_Digital_privacy: Optional[
        Literal[
            "base",
            "very_good",
            "good",
            "neither_good_nor_bad",
            "bad",
            "very_bad",
            "never_tried",
            "dont_know",
        ]
    ] = Field(
        default=None,
        description="Thinking_about_your_current_level_of_digital_expertise_please_rate_your_level_of_competence_understanding_about_the_following_digital_topics_or_Digital_privacy",
    )
    Thinking_about_your_current_level_of_digital_expertise_please_rate_your_level_of_competence_understanding_about_the_following_digital_topics_or_Online_payment: Optional[
        Literal[
            "base",
            "very_good",
            "good",
            "neither_good_nor_bad",
            "bad",
            "very_bad",
            "never_tried",
            "dont_know",
        ]
    ] = Field(
        default=None,
        description="Thinking_about_your_current_level_of_digital_expertise_please_rate_your_level_of_competence_understanding_about_the_following_digital_topics_or_Online_payment",
    )
    Have_you_taken_or_are_you_planning_to_take_any_training_courses_related_to_digital_skills_Please_exclude_all_courses_offered_by_your_school_university_and_or_workplace: Optional[
        Literal[
            "base",
            "yes_i_have_taken_a_course_in_the_last_12_months",
            "yes_i_plan_to_take_a_course_in_the_next_12_months",
            "both",
            "neither",
            "base.1",
            "applying_for_jobs",
            "basic_computer_skills",
            "basic_online_skills",
            "office_suites",
            "online_financial_management",
            "programming",
            "specific_software",
            "website_design",
            "other",
        ]
    ] = Field(
        default=None,
        description="Have_you_taken_or_are_you_planning_to_take_any_training_courses_related_to_digital_skills_Please_exclude_all_courses_offered_by_your_school_university_and_or_workplace",
    )
    And_which_of_these_courses_did_you_have_to_pay_for: Optional[
        Literal[
            "base",
            "applying_for_jobs",
            "basic_computer_skills",
            "basic_online_skills",
            "office_suites",
            "online_financial_management",
            "programming",
            "specific_software _(eg_photoshop)",
            "website_design",
            "other",
            "the_courses_were_free",
        ]
    ] = Field(
        default=None, description="And_which_of_these_courses_did_you_have_to_pay_for"
    )
    Which_of_the_following_topics_do_you_plan_to_take_a_course_in_over_the_next_12_months: Optional[
        Literal[
            "base",
            "applying_for_jobs",
            "basic_computer_skills",
            "basic_online_skills",
            "office_suites",
            "online_financial_management",
            "programming",
            "specific_software _(eg_photoshop)",
            "website_design",
            "other",
        ]
    ] = Field(
        default=None,
        description="Which_of_the_following_topics_do_you_plan_to_take_a_course_in_over_the_next_12_months",
    )
    Which_of_the_following_statements_do_you_agree_with: Optional[
        Literal[
            "base",
            "i_don’t_like_to_provide_financial_information_or_payment_details_online",
            "i_am_concerned_about_the_amount_of_personal_data_that_companies_collect_from_me",
            "i_feel_uncomfortable_knowing_that_digital_voice_assistants_record_nearly_everything",
            "i_don’t_think_about_security_or_privacy_when_creating_accounts_and_passwords",
            "i_am_worried_about_someone_hacking_my_account_and_accessing_my_personal_data",
            "i_don’t_trust_the_government_to_protect_me_online",
            "i_worry_that_i_don’t_have_control_over_what_i_have_previously_posted_online",
            "none_of_the_above",
            "base.1",
            "since_covid-19_began_i_have_started_shopping_online_more",
            "being_able_to_rent_products_from_online_stores_that_i_wouldn’t_have_been_able_to_afford_otherwise_is_appealing_to_me",
            "i_don’t_think_artificial_intelligence_can_replace_human_customer_service",
            "i_prefer_to_use_cash_or_debit/credit_cards_over_online_or_mobile_payments",
            "paying_by_cash_should_be_replaced_with_digital_alternatives",
            "when_i_shop_online_i_miss_the_element_of_social_interaction_with_friends",
            "none_of_the_above.1",
            "base.2",
            "the_government_should_put_more_services_online",
            "the_government_needs_to_do_more_to_improve_its_digital_capabilities",
            "if_possible_i_receive_my_utility_bills_or_bank_statements_via_e-mail_or_online",
            "i_do_not_like_all_the_different_online_systems_companies_use",
            "since_the_covid-19_pandemic_began_i_manage_more_aspects_of_my_life_digitally",
            "none_of_the_above.2",
            "base.3",
            "i_think_most_of_the_information_on_social_media_is unreliable",
            "when_i_read_news_online_i_always_check_if_the_source_is_trustworthy",
            "big_tech_companies_should_stay_politically_neutral",
            "tech_companies_should_do_more_to_stop_the_spread_of_fake_news_online",
            "tech_companies_need_to_do_more_to_stop_politicians_spreading_lies_online",
            "i_don’t_trust_big_tech_to_use_my_data_appropriately",
            "tech_companies_often_have_better_solutions_for_recent_challenges_than_governments",
            "i_like_that_websites_show_me_things_that_are_relevant_to_me_by_collecting_my_data",
            "none_of_the_above.3",
        ]
    ] = Field(
        default=None, description="Which_of_the_following_statements_do_you_agree_with"
    )
    When_you_think_about_your_digital_privacy_which_of_the_following_apply_to_you: Optional[
        Literal[
            "base",
            "i_worry_about_my_personal_data_when_using_digital_services",
            "i_delete_cookies_regularly",
            "i_use_a_vpn_to_protect_my_privacy",
            "i_use_certain_browsers_or_search_engines_to_protect_my_privacy",
            "i_cover_my_devices_camera_lenses_when_they_are_not_used",
            "i_always_pay_attention_to_what_kind_of_information_i_give_to_tech_companies",
            "i_change_my_passwords_and_login_information_regularly",
            "i_use_the_same_password_and_e-mail_address_for_several_accounts",
            "i_read_the_terms_and_conditions_before_agreeing_to_them",
            "i_don’t_mind_giving_personal_information_if_this_leads_to_improved_services",
            "none_of_the_above",
        ]
    ] = Field(
        default=None,
        description="When_you_think_about_your_digital_privacy_which_of_the_following_apply_to_you",
    )
    Thinking_about_the_way_you_interact_socially_online_which_of_the_following_statements_do_you_agree_with: Optional[
        Literal[
            "base",
            "increased_digitalization_has_made_me_lonely",
            "i_have_more_friends_online_than_i_do_offline",
            "the_more_“likes”_i_get_the_more_valued_i_feel",
            "more_needs_to_be_done_by_tech_companies_to_tackle_cyberbullying",
            "i_am_more_likely_to_express_controversial_opinions_online",
            "the_internet_has_been_essential_for_my_mental_health_during_the_covid-19_pandemic",
            "i_like_it_when_politicians_use_social_media_channels_to_communicate_with_people",
            "people_should_not_be_allowed_to_use_anonymized_accounts",
            "none_of_the_above",
        ]
    ] = Field(
        default=None,
        description="Thinking_about_the_way_you_interact_socially_online_which_of_the_following_statements_do_you_agree_with",
    )
    Which_of_these_digital_methods_did_you_use_to_communicate_with_friends_and_family_in_the_past_12_months: Optional[
        Literal[
            "base",
            "telephone_via_internet_(without_video)",
            "video_calling",
            "messenger apps_(eg_whatsapp)",
            "social media",
            "forums",
            "e-mail",
            "in-game_messaging",
            "digital_hangouts_(eg_discord)",
            "other",
            "i_did_not_use_digital_methods_to_contact_my_friends_and_family",
            "base.1",
            "social_media_user",
            "non-user",
        ]
    ] = Field(
        default=None,
        description="Which_of_these_digital_methods_did_you_use_to_communicate_with_friends_and_family_in_the_past_12_months",
    )
    In_general_what_are_your_reasons_for_using_social_media: Optional[
        Literal[
            "base",
            "to_stay_connected_with_colleagues_&_business_partners",
            "to_stay_informed_about_what_happens_in_the_world",
            "to_keep_in_touch_with_friends_&_family",
            "to_feel_part_of_a_community",
            "to_distract_myself_from_my_daily_routine",
            "to_see_fun_and_exciting_content",
            "to_share_my_opinions_and_ideas",
            "to_show_a_different_side_of_me",
            "to_show_people_what_i_do/own",
            "to_compare_myself_with_others",
            "other",
            "don’t_know",
        ]
    ] = Field(
        default=None,
        description="In_general_what_are_your_reasons_for_using_social_media",
    )
    In_general_when_do_you_use_social_media: Optional[
        Literal[
            "base",
            "during_breaks_at_work/school/university",
            "during_meals",
            "during_my_morning_routine",
            "during_work_and/or_lesson_time",
            "in_bed/before_going_to_sleep",
            "in_the_bathroom/on_the_toilet",
            "in_the_evening/after_coming_home",
            "on_my_way_to_work/school/university",
            "whenever_i_need_to_kill_time",
            "while_visiting_a_café/bar/restaurant",
            "while_watching_tv",
            "don’t_know",
        ]
    ] = Field(default=None, description="In_general_when_do_you_use_social_media")
    Which_of_the_following_have_you_done_on_social_media_in_the_past_4_weeks: Optional[
        Literal[
            "base",
            "commented_on_posts",
            "followed_companies",
            "followed_people",
            "liked_company_posts",
            "liked_posts_by_other_users",
            "posted_pictures/videos",
            "posted_texts/status_updates",
            "connected_with_colleagues",
            "connected_with_friends",
            "sent_private_messages",
            "shared_company_posts",
            "shared_posts_by_other_users",
            "none_of_the_above",
            "base.1",
            "expressed_my_opinion_about_current_topics",
            "researched_products",
            "wrote_a_recommendation/review",
            "booked_a_table_at_a_restaurant/a_leisure_time_activity",
            "shared_photos_or_videos_or_live_videos",
            "took_part_in_a_live_event",
            "watched_a_live_video",
            "read_news",
            "stayed_up-to-date_with_current_events",
            "made_an_appointment",
            "found_information_about_a_product/service/conditions",
            "made_a_complaint_to_a_company_or_brand",
            "asked_specific_questions_about_an_order_or_other_issue_for_a_company_or_brand",
            "ordered_a_product_or_service",
            "none_of_the_above.1",
        ]
    ] = Field(
        default=None,
        description="Which_of_the_following_have_you_done_on_social_media_in_the_past_4_weeks",
    )
    Have_you_expressed_your_opinion_about_any_of_the_following_topics_on_social_media_in_the_past_4_weeks_: Optional[
        Literal[
            "base",
            "arts_and_culture",
            "beauty_and_personal_care",
            "cars_and_motorcycles",
            "celebrities",
            "computers_smartphones_and/or_technology",
            "family_and_kids",
            "fashion",
            "food_and_drinks",
            "health_and_medicine",
            "household_chores",
            "life-hacks/how-tos",
            "media_(eg_books_music_movies_and_tv_series)",
            "politics_and_societal_topics",
            "jobs",
            "sports",
            "vacation_and_travel",
            "video_games",
            "i_have_not_expressed_an_opinion_about_any_of_these_topics",
            "base.1",
            "acitve_social_media_user",
            "passive_social_media_user",
        ]
    ] = Field(
        default=None,
        description="Have_you_expressed_your_opinion_about_any_of_the_following_topics_on_social_media_in_the_past_4_weeks_",
    )
    Which_of_the_following_social_media_platforms_do_you_know_even_if_just_by_name: (
        Optional[
            Literal[
                "base",
                "facebook",
                "flickr",
                "instagram",
                "linkedin",
                "pinterest",
                "reddit",
                "snapchat",
                "tiktok",
                "tumblr",
                "twitter",
                "wechat",
                "youtube",
                "quora",
                "xing",
                "jodel",
                "none_of_the_above",
            ]
        ]
    ) = Field(
        default=None,
        description="Which_of_the_following_social_media_platforms_do_you_know_even_if_just_by_name",
    )
    And_which_of_these_social_media_platforms_do_you_use_regularly: Optional[
        Literal[
            "base",
            "facebook",
            "flickr",
            "instagram",
            "linkedin",
            "pinterest",
            "reddit",
            "snapchat",
            "tiktok",
            "tumblr",
            "twitter",
            "wechat",
            "youtube",
            "quora",
            "xing",
            "jodel",
            "i_don’t_use_social_media_regularly",
        ]
    ] = Field(
        default=None,
        description="And_which_of_these_social_media_platforms_do_you_use_regularly",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Overall_usage_frequency: Optional[
        Literal["base", "frequent", "occasional", "dont_know"]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Overall_usage_frequency",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Facebook: (
        Optional[
            Literal[
                "base",
                "several_times_a_day",
                "once_a_day",
                "several_times_a_week",
                "once_a_week",
                "less_often",
            ]
        ]
    ) = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Facebook",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Flickr: Optional[
        Literal[
            "base",
            "several_times_a_day",
            "once_a_day",
            "several_times_a_week",
            "once_a_week",
            "less_often",
        ]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Flickr",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Instagram: (
        Optional[
            Literal[
                "base",
                "several_times_a_day",
                "once_a_day",
                "several_times_a_week",
                "once_a_week",
                "less_often",
                "dont_know",
            ]
        ]
    ) = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Instagram",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_LinkedIn: (
        Optional[
            Literal[
                "base",
                "several_times_a_day",
                "once_a_day",
                "several_times_a_week",
                "once_a_week",
                "less_often",
            ]
        ]
    ) = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_LinkedIn",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Pinterest: (
        Optional[
            Literal[
                "base",
                "several_times_a_day",
                "once_a_day",
                "several_times_a_week",
                "once_a_week",
                "less_often",
            ]
        ]
    ) = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Pinterest",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Reddit: Optional[
        Literal[
            "base",
            "several_times_a_day",
            "once_a_day",
            "several_times_a_week",
            "once_a_week",
            "less_often",
        ]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Reddit",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Snapchat: (
        Optional[
            Literal[
                "base",
                "several_times_a_day",
                "once_a_day",
                "several_times_a_week",
                "once_a_week",
                "less_often",
            ]
        ]
    ) = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Snapchat",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_TikTok: Optional[
        Literal[
            "base",
            "several_times_a_day",
            "once_a_day",
            "several_times_a_week",
            "once_a_week",
            "less_often",
        ]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_TikTok",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Tumblr: Optional[
        Literal[
            "base",
            "several_times_a_day",
            "once_a_day",
            "several_times_a_week",
            "once_a_week",
            "less_often",
        ]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Tumblr",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Twitter: (
        Optional[
            Literal[
                "base",
                "several_times_a_day",
                "once_a_day",
                "several_times_a_week",
                "once_a_week",
                "less_often",
            ]
        ]
    ) = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Twitter",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_WeChat: Optional[
        Literal["base", "several_times_a_day", "once_a_day", "several_times_a_week"]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_WeChat",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_YouTube: (
        Optional[
            Literal[
                "base",
                "several_times_a_day",
                "once_a_day",
                "several_times_a_week",
                "once_a_week",
                "less_often",
                "dont_know",
            ]
        ]
    ) = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_YouTube",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Quora: Optional[
        Literal[
            "base",
            "several_times_a_day",
            "once_a_day",
            "several_times_a_week",
            "once_a_week",
            "less_often",
        ]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Quora",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Xing: Optional[
        Literal[
            "base",
            "several_times_a_day",
            "once_a_day",
            "several_times_a_week",
            "once_a_week",
            "less_often",
        ]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Xing",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Jodel: Optional[
        Literal["base", "several_times_a_day", "once_a_day", "several_times_a_week"]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Jodel",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_Facebook: Optional[
        Literal["base", "frequent_(daily)", "occasional"]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_Facebook",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_Flickr: Optional[
        Literal["base", "frequent_(daily)", "occasional"]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_Flickr",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_Instagram: Optional[
        Literal["base", "frequent_(daily)", "occasional", "dont_know"]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_Instagram",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_LinkedIn: Optional[
        Literal["base", "frequent_(daily)", "occasional"]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_LinkedIn",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_Pinterest: Optional[
        Literal["base", "frequent_(daily)", "occasional"]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_Pinterest",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_Reddit: Optional[
        Literal["base", "frequent_(daily)", "occasional"]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_Reddit",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_Snapchat: Optional[
        Literal["base", "frequent_(daily)", "occasional"]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_Snapchat",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_TikTok: Optional[
        Literal["base", "frequent_(daily)", "occasional"]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_TikTok",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_Tumblr: Optional[
        Literal["base", "frequent_(daily)", "occasional"]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_Tumblr",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_Twitter: Optional[
        Literal["base", "frequent_(daily)", "occasional"]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_Twitter",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_WeChat: Optional[
        Literal["base", "frequent_(daily)", "occasional"]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_WeChat",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_YouTube: Optional[
        Literal["base", "frequent_(daily)", "occasional", "dont_know"]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_YouTube",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_Quora: Optional[
        Literal["base", "frequent_(daily)", "occasional"]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_Quora",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_Xing: Optional[
        Literal["base", "frequent_(daily)", "occasional"]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_Xing",
    )
    How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_Jodel: Optional[
        Literal["base", "frequent_(daily)", "occasional"]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_the_following_social_media_platforms_Usage_frequency_Jodel",
    )
    Approximately_how_long_do_you_spend_on_the_following_social_media_platforms_in_an_average_week: Optional[
        Literal[
            "base",
            "light",
            "moderate",
            "high",
            "dont_know",
            "facebook_base",
            "facebook_less_than_1_hour",
            "facebook_1_to_5_hours",
            "facebook_6_to_10_hours",
            "facebook_11_to_15_hours",
            "facebook_16_to_20_hours",
            "facebook_more_than_20_hours",
            "facebook_dont_know",
            "flickr_base",
            "flickr_less_than_1_hour",
            "flickr_1_to_5_hours",
            "flickr_6_to_10_hours",
            "flickr_11_to_15_hours",
            "flickr_16_to_20_hours",
            "flickr_dont_know",
            "instagram_base",
            "instagram_less_than_1_hour",
            "instagram_1_to_5_hours",
            "instagram_6_to_10_hours",
            "instagram_11_to_15_hours",
            "instagram_16_to_20_hours",
            "instagram_more_than_20_hours",
            "instagram_dont_know",
            "linkedin_base",
            "linkedin_less_than_1_hour",
            "linkedin_1_to_5_hours",
            "linkedin_6_to_10_hours",
            "linkedin_11_to_15_hours",
            "linkedin_16_to_20_hours",
            "linkedin_more_than_20_hours",
            "linkedin_dont_know",
            "pinterest_base",
            "pinterest_less_than_1_hour",
            "pinterest_1_to_5_hours",
            "pinterest_6_to_10_hours",
            "pinterest_11_to_15_hours",
            "pinterest_more_than_20_hours",
            "pinterest_dont_know",
            "reddit_base",
            "reddit_less_than_1_hour",
            "reddit_1_to_5_hours",
            "reddit_6_to_10_hours",
            "reddit_16_to_20_hours",
            "reddit_more_than_20_hours",
            "reddit_dont_know",
            "snapchat_base",
            "snapchat_less_than_1_hour",
            "snapchat_1_to_5_hours",
            "snapchat_6_to_10_hours",
            "snapchat_11_to_15_hours",
            "snapchat_16_to_20_hours",
            "snapchat_more_than_20_hours",
            "snapchat_dont_know",
            "tiktok_base",
            "tiktok_less_than_1_hour",
            "tiktok_1_to_5_hours",
            "tiktok_6_to_10_hours",
            "tiktok_16_to_20_hours",
            "tiktok_more_than_20_hours",
            "tiktok_dont_know",
            "tumblr_base",
            "tumblr_less_than_1_hour",
            "tumblr_1_to_5_hours",
            "tumblr_6_to_10_hours",
            "tumblr_11_to_15_hours",
            "tumblr_more_than_20_hours",
            "tumblr_dont_know",
            "twitter_base",
            "twitter_less_than_1_hour",
            "twitter_1_to_5_hours",
            "twitter_6_to_10_hours",
            "twitter_11_to_15_hours",
            "twitter_16_to_20_hours",
            "twitter_more_than_20_hours",
            "twitter_dont_know",
            "wechat_base",
            "wechat_less_than_1_hour",
            "wechat_1_to_5_hours",
            "wechat_6_to_10_hours",
            "wechat_dont_know",
            "youtube_base",
            "youtube_less_than_1_hour",
            "youtube_1_to_5_hours",
            "youtube_6_to_10_hours",
            "youtube_11_to_15_hours",
            "youtube_16_to_20_hours",
            "youtube_more_than_20_hours",
            "youtube_dont_know",
            "quora_base",
            "quora_less_than_1_hour",
            "quora_6_to_10_hours",
            "quora_11_to_15_hours",
            "quora_dont_know",
            "xing_base",
            "xing_less_than_1_hour",
            "xing_1_to_5_hours",
            "xing_6_to_10_hours",
            "xing_16_to_20_hours",
            "xing_more_than_20_hours",
            "xing_dont_know",
            "jodel_base",
            "jodel_less_than_1_hour",
            "jodel_1_to_5_hours",
            "jodel_6_to_10_hours",
            "jodel_dont_know",
            "usage_intensity_facebook_base",
            "usage_intensity_facebook_light",
            "usage_intensity_facebook_moderate",
            "usage_intensity_facebook_high",
            "usage_intensity_facebook_dont_know",
            "usage_intensity_flickr_base",
            "usage_intensity_flickr_light",
            "usage_intensity_flickr_moderate",
            "usage_intensity_flickr_high",
            "usage_intensity_flickr_dont_know",
            "usage_intensity_instagram_base",
            "usage_intensity_instagram_light",
            "usage_intensity_instagram_moderate",
            "usage_intensity_instagram_high",
            "usage_intensity_instagram_dont_know",
            "usage_intensity_linkedin_base",
            "usage_intensity_linkedin_light",
            "usage_intensity_linkedin_moderate",
            "usage_intensity_linkedin_high",
            "usage_intensity_linkedin_dont_know",
            "usage_intensity_pinterest_base",
            "usage_intensity_pinterest_light",
            "usage_intensity_pinterest_moderate",
            "usage_intensity_pinterest_high",
            "usage_intensity_pinterest_dont_know",
            "usage_intensity_reddit_base",
            "usage_intensity_reddit_light",
            "usage_intensity_reddit_moderate",
            "usage_intensity_reddit_high",
            "usage_intensity_reddit_dont_know",
            "usage_intensity_snapchat_base",
            "usage_intensity_snapchat_light",
            "usage_intensity_snapchat_moderate",
            "usage_intensity_snapchat_high",
            "usage_intensity_snapchat_dont_know",
            "usage_intensity_tiktok_base",
            "usage_intensity_tiktok_light",
            "usage_intensity_tiktok_moderate",
            "usage_intensity_tiktok_high",
            "usage_intensity_tiktok_dont_know",
            "usage_intensity_tumblr_base",
            "usage_intensity_tumblr_light",
            "usage_intensity_tumblr_moderate",
            "usage_intensity_tumblr_high",
            "usage_intensity_tumblr_dont_know",
            "usage_intensity_twitter_base",
            "usage_intensity_twitter_light",
            "usage_intensity_twitter_moderate",
            "usage_intensity_twitter_high",
            "usage_intensity_twitter_dont_know",
            "usage_intensity_wechat_base",
            "usage_intensity_wechat_light",
            "usage_intensity_wechat_moderate",
            "usage_intensity_wechat_dont_know",
            "usage_intensity_youtube_base",
            "usage_intensity_youtube_light",
            "usage_intensity_youtube_moderate",
            "usage_intensity_youtube_high",
            "usage_intensity_youtube_dont_know",
            "usage_intensity_quora_base",
            "usage_intensity_quora_light",
            "usage_intensity_quora_moderate",
            "usage_intensity_quora_dont_know",
            "usage_intensity_xing_base",
            "usage_intensity_xing_light",
            "usage_intensity_xing_moderate",
            "usage_intensity_xing_high",
            "usage_intensity_xing_dont_know",
            "usage_intensity_jodel_base",
            "usage_intensity_jodel_light",
            "usage_intensity_jodel_moderate",
            "usage_intensity_jodel_dont_know",
        ]
    ] = Field(
        default=None,
        description="Approximately_how_long_do_you_spend_on_the_following_social_media_platforms_in_an_average_week",
    )
    Which_of_the_following_digital_platforms_did_you_use_for_personal_purposes_in_the_last_4_weeks_Digital_platform_usage: Optional[
        Literal["base", "digital_platform_user", "non-user"]
    ] = Field(
        default=None,
        description="Which_of_the_following_digital_platforms_did_you_use_for_personal_purposes_in_the_last_4_weeks_Digital_platform_usage",
    )
    Which_of_the_following_digital_platforms_do_you_know_even_if_only_by_name: Optional[
        Literal[
            "base",
            "discord",
            "facebook_messenger",
            "facetime",
            "google_duo",
            "google_hangouts",
            "imo",
            "kik",
            "skype",
            "slack",
            "snapchat",
            "telegram",
            "threema",
            "viber",
            "wechat",
            "whatsapp",
            "zoom",
            "jitsi",
            "none_of_the_above",
        ]
    ] = Field(
        default=None,
        description="Which_of_the_following_digital_platforms_do_you_know_even_if_only_by_name",
    )
    Which_of_the_following_digital_platforms_did_you_use_for_personal_purposes_in_the_last_4_weeks: Optional[
        Literal[
            "base",
            "discord",
            "facebook_messenger",
            "facetime",
            "google_duo",
            "google_hangouts",
            "imo",
            "kik",
            "skype",
            "slack",
            "snapchat",
            "telegram",
            "threema",
            "viber",
            "wechat",
            "whatsapp",
            "zoom",
            "jitsi",
            "i_did_not_use_any_of_these_platforms_for_personal_purposes",
            "base.1",
            "video_calling_user",
            "non-user",
            "base.2",
            "frequent_(at_least_weekly)",
            "occasional",
            "dont_know",
        ]
    ] = Field(
        default=None,
        description="Which_of_the_following_digital_platforms_did_you_use_for_personal_purposes_in_the_last_4_weeks",
    )
    How_often_do_you_normally_use_video_calls_for_personal_purposes: Optional[
        Literal[
            "base",
            "several_times_a_day",
            "once_a_day",
            "several_times_a_week",
            "once_a_week",
            "several_times_a_month",
            "once_a_month",
            "less_often",
            "i_dont_use_video_calling_for_personal_purposes",
            "don’t_know",
        ]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_video_calls_for_personal_purposes",
    )
    The_following_questions_are_about_digital_media_services_Which_of_the_following_statements_do_you_agree_with: Optional[
        Literal[
            "base",
            "digital_services_allow_me_to_discover_new_and_exciting_content",
            "i_prefer_digital_content_as_it_is_easier_to_manage",
            "i_want_to_access_my_music/movies_on_all_my_devices_(tv_smartphone_tablet_etc)",
            "it_is_important_to_me_to_get_the_best_image_and_sound_quality",
            "it_is_too_expensive_to_afford_all_the_streaming_services_that_i_want",
            "i_am_willing_to_pay_for_extra_content_on_news_websites",
            "traditional_and_print_media_do_not_play_a_role_in_my_personal_life_anymore",
            "none_of_the_above",
        ]
    ] = Field(
        default=None,
        description="The_following_questions_are_about_digital_media_services_Which_of_the_following_statements_do_you_agree_with",
    )
    Which_of_the_following_digital_media_services_have_you_used_in_the_past_12_months: (
        Optional[
            Literal[
                "base",
                "audiobooks_(download/streaming)",
                "ebooks",
                "digital_music_content_(download/streaming)",
                "digital_video_content_(download/streaming)",
                "enewspapers_&_emagazines",
                "online_radio",
                "podcasts",
                "other",
                "i_dont_use_any_digital_media_services",
            ]
        ]
    ) = Field(
        default=None,
        description="Which_of_the_following_digital_media_services_have_you_used_in_the_past_12_months",
    )
    When_or_where_do_you_use_your_digital_media_services: Optional[
        Literal[
            "base",
            "in_the_bathroom/on_the_toilet",
            "while_doing_sports",
            "during_my_morning_routine",
            "on_my_way_to_work/school/university",
            "during_meals",
            "during_breaks_at_work/school/university",
            "during_work_and/or_lesson_time",
            "whenever_i_need_to_kill_time",
            "while_watching_tv",
            "while_visiting_a_café/bar/restaurant",
            "in_the_evening/after_coming_home",
            "in_bed/before_going_to_sleep",
            "other",
            "don’t_know",
        ]
    ] = Field(
        default=None, description="When_or_where_do_you_use_your_digital_media_services"
    )
    How_often_do_you_normally_use_these_services_Audiobooks_downloadorstreaming: (
        Optional[
            Literal[
                "base",
                "several_times_a_day",
                "once_a_day",
                "several_times_a_week",
                "once_a_week",
                "less_often",
                "don’t_know",
            ]
        ]
    ) = Field(
        default=None,
        description="How_often_do_you_normally_use_these_services_Audiobooks_downloadorstreaming",
    )
    How_often_do_you_normally_use_these_services_eBooks: Optional[
        Literal[
            "base",
            "several_times_a_day",
            "once_a_day",
            "several_times_a_week",
            "once_a_week",
            "less_often",
            "don’t_know",
        ]
    ] = Field(
        default=None, description="How_often_do_you_normally_use_these_services_eBooks"
    )
    How_often_do_you_normally_use_these_services_Digital_music_content_downloadorstreaming: Optional[
        Literal[
            "base",
            "several_times_a_day",
            "once_a_day",
            "several_times_a_week",
            "once_a_week",
            "less_often",
            "don’t_know",
        ]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_these_services_Digital_music_content_downloadorstreaming",
    )
    How_often_do_you_normally_use_these_services_Digital_video_content_downloadorstreaming: Optional[
        Literal[
            "base",
            "several_times_a_day",
            "once_a_day",
            "several_times_a_week",
            "once_a_week",
            "less_often",
            "don’t_know",
        ]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_these_services_Digital_video_content_downloadorstreaming",
    )
    How_often_do_you_normally_use_these_services_eNewspapers_and_eMagazines: Optional[
        Literal[
            "base",
            "several_times_a_day",
            "once_a_day",
            "several_times_a_week",
            "once_a_week",
            "less_often",
        ]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_these_services_eNewspapers_and_eMagazines",
    )
    How_often_do_you_normally_use_these_services_Online_radio: Optional[
        Literal[
            "base",
            "several_times_a_day",
            "once_a_day",
            "several_times_a_week",
            "once_a_week",
            "less_often",
            "don’t_know",
        ]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_these_services_Online_radio",
    )
    How_often_do_you_normally_use_these_services_Podcasts: Optional[
        Literal[
            "base",
            "several_times_a_day",
            "once_a_day",
            "several_times_a_week",
            "once_a_week",
            "less_often",
            "don’t_know",
        ]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_these_services_Podcasts",
    )
    Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_Audiobooks_downloadorstreaming: Optional[
        Literal[
            "base",
            "less_than_1_hour",
            "1_to_5_hours",
            "6_to_10_hours",
            "11_to_15_hours",
            "16_to_20_hours",
            "more_than_20_hours",
            "i_do_not_use_this_weekly",
        ]
    ] = Field(
        default=None,
        description="Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_Audiobooks_downloadorstreaming",
    )
    Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_eBooks: (
        Optional[
            Literal[
                "base",
                "less_than_1_hour",
                "1_to_5_hours",
                "6_to_10_hours",
                "11_to_15_hours",
                "16_to_20_hours",
                "more_than_20_hours",
                "dont_know",
            ]
        ]
    ) = Field(
        default=None,
        description="Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_eBooks",
    )
    Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_Digital_music_content_downloadorstreaming: Optional[
        Literal[
            "base",
            "less_than_1_hour",
            "1_to_5_hours",
            "6_to_10_hours",
            "11_to_15_hours",
            "16_to_20_hours",
            "more_than_20_hours",
            "dont_know",
        ]
    ] = Field(
        default=None,
        description="Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_Digital_music_content_downloadorstreaming",
    )
    Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_Digital_video_content_downloadorstreaming: Optional[
        Literal[
            "base",
            "less_than_1_hour",
            "1_to_5_hours",
            "6_to_10_hours",
            "11_to_15_hours",
            "16_to_20_hours",
            "more_than_20_hours",
            "i_do_not_use_this_weekly",
            "dont_know",
        ]
    ] = Field(
        default=None,
        description="Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_Digital_video_content_downloadorstreaming",
    )
    Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_eNewspapers_and_eMagazines: Optional[
        Literal[
            "base",
            "less_than_1_hour",
            "1_to_5_hours",
            "6_to_10_hours",
            "11_to_15_hours",
            "16_to_20_hours",
            "more_than_20_hours",
            "dont_know",
        ]
    ] = Field(
        default=None,
        description="Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_eNewspapers_and_eMagazines",
    )
    Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_Online_radio: Optional[
        Literal[
            "base",
            "less_than_1_hour",
            "1_to_5_hours",
            "6_to_10_hours",
            "11_to_15_hours",
            "16_to_20_hours",
            "more_than_20_hours",
            "dont_know",
        ]
    ] = Field(
        default=None,
        description="Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_Online_radio",
    )
    Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_Podcasts: Optional[
        Literal[
            "base",
            "less_than_1_hour",
            "1_to_5_hours",
            "6_to_10_hours",
            "11_to_15_hours",
            "16_to_20_hours",
            "more_than_20_hours",
            "i_do_not_use_this_weekly",
        ]
    ] = Field(
        default=None,
        description="Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_Podcasts",
    )
    How_often_do_you_normally_use_these_services_Media_frequency_Audiobooks: Optional[
        Literal["base", "frequent", "occasional", "dont_know"]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_these_services_Media_frequency_Audiobooks",
    )
    Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_Media_intensity_Audiobooks: Optional[
        Literal["base", "light", "moderate", "high"]
    ] = Field(
        default=None,
        description="Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_Media_intensity_Audiobooks",
    )
    Which_platforms_have_you_used_to_listen_to_audiobooks_streamed_downloaded_in_the_past_12_months_as_a_paying_customer: Optional[
        Literal[
            "base",
            "apple_books",
            "audible",
            "downpour",
            "google_play_bücher",
            "rakuten_kobo/kobo_audiobooks",
            "scribd",
            "thalia",
            "other",
            "don’t_know",
            "i_did_not_pay_for_audiobooks",
        ]
    ] = Field(
        default=None,
        description="Which_platforms_have_you_used_to_listen_to_audiobooks_streamed_downloaded_in_the_past_12_months_as_a_paying_customer",
    )
    How_often_do_you_normally_use_these_services_Media_frequency_eBooks: Optional[
        Literal["base", "frequent", "occasional", "dont_know"]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_these_services_Media_frequency_eBooks",
    )
    Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_Media_intensity_eBooks: Optional[
        Literal["base", "light", "moderate", "high", "dont_know"]
    ] = Field(
        default=None,
        description="Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_Media_intensity_eBooks",
    )
    Which_platforms_have_you_used_to_get_eBooks_in_the_past_12_months_as_a_paying_customer: Optional[
        Literal[
            "base",
            "amazon",
            "apple_books",
            "beam",
            "bolde",
            "buecherde",
            "ebookde",
            "google_play_bücher",
            "hugendubel",
            "rakuten_kobo/kobo_audiobooks",
            "thalia",
            "weltbild",
            "other",
            "don’t_know",
            "i_did_not_pay_for_ebooks",
        ]
    ] = Field(
        default=None,
        description="Which_platforms_have_you_used_to_get_eBooks_in_the_past_12_months_as_a_paying_customer",
    )
    Which_devices_do_you_normally_use_to_read_eBooks: Optional[
        Literal["base", "laptop/pc", "tablet", "smartphone", "ereader"]
    ] = Field(
        default=None, description="Which_devices_do_you_normally_use_to_read_eBooks"
    )
    You_said_you_have_an_eReader_What_brand_of_eReader_is_it: Optional[
        Literal[
            "base",
            "amazon_kindle",
            "kobo",
            "pocketbook",
            "tolino",
            "other",
            "don’t_know",
        ]
    ] = Field(
        default=None,
        description="You_said_you_have_an_eReader_What_brand_of_eReader_is_it",
    )
    Concerning_eBooks_and_or_audiobooks_what_type_of_content_do_you_consume: Optional[
        Literal[
            "base",
            "fantasy/science_fiction/dystopian",
            "adventure",
            "romance",
            "contemporary",
            "horror",
            "thriller/crime/mystery",
            "historical_fiction",
            "memoir/autobiography",
            "self-help/personal_development/motivational",
            "history",
            "travel",
            "humor/comedy",
            "advice/how-to",
            "other",
            "don’t_know",
        ]
    ] = Field(
        default=None,
        description="Concerning_eBooks_and_or_audiobooks_what_type_of_content_do_you_consume",
    )
    How_often_do_you_normally_use_these_services_Media_frequency_Digital_music: (
        Optional[Literal["base", "frequent", "occasional", "dont_know"]]
    ) = Field(
        default=None,
        description="How_often_do_you_normally_use_these_services_Media_frequency_Digital_music",
    )
    Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_Media_intensity_Digital_music: Optional[
        Literal["base", "light", "moderate", "high", "dont_know"]
    ] = Field(
        default=None,
        description="Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_Media_intensity_Digital_music",
    )
    Which_of_these_music_streaming_platforms_have_you_used_in_the_past_12_months_as_a_paying_customer: Optional[
        Literal[
            "base",
            "amazon_music",
            "apple_music",
            "deezer",
            "google_play_music",
            "itunes_store",
            "napster",
            "qobuz",
            "soundcloud",
            "spotify",
            "tidal",
            "youtube_music",
            "other",
            "don’t_know",
            "i_did_not_pay_for_digital_music_content",
        ]
    ] = Field(
        default=None,
        description="Which_of_these_music_streaming_platforms_have_you_used_in_the_past_12_months_as_a_paying_customer",
    )
    Concerning_digital_music_streaming_downloading_which_genres_do_you_consume: (
        Optional[
            Literal[
                "base",
                "classical_music",
                "dance/electronic",
                "jazz_and_blues",
                "pop/adult_contemporary",
                "religious",
                "rock/alternative/indie",
                "urban_music_(hip_hop_r&b_etc)",
                "hardrock/punk/metal",
                "techno/house",
                "country/folk/world_music",
                "oldies",
                "deutscher_schlager/volksmusik",
                "other",
                "dont_know",
            ]
        ]
    ) = Field(
        default=None,
        description="Concerning_digital_music_streaming_downloading_which_genres_do_you_consume",
    )
    How_often_do_you_normally_use_these_services_Media_frequency_Digital_video: (
        Optional[Literal["base", "frequent", "occasional", "dont_know"]]
    ) = Field(
        default=None,
        description="How_often_do_you_normally_use_these_services_Media_frequency_Digital_video",
    )
    Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_Media_intensity_Digital_video: Optional[
        Literal["base", "light", "moderate", "high", "dont_know"]
    ] = Field(
        default=None,
        description="Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_Media_intensity_Digital_video",
    )
    Which_platforms_have_you_used_to_watch_video_content_streaming_downloading_in_the_past_12_months_as_a_paying_customer: Optional[
        Literal[
            "base",
            "amazon_prime_video",
            "anime_on_demand",
            "apple_tv+",
            "chili",
            "crunchyroll",
            "disney+",
            "google_play_filme_&_serien",
            "itunes_store",
            "magentatv",
            "maxdome",
            "netflix",
            "pantaflix",
            "playstation_store",
            "sky",
            "videoload",
            "xbox_games_store_/_microsoft_store",
            "youtube",
            "other",
            "don’t_know",
            "i_did_not_pay_for_digital_video_content",
        ]
    ] = Field(
        default=None,
        description="Which_platforms_have_you_used_to_watch_video_content_streaming_downloading_in_the_past_12_months_as_a_paying_customer",
    )
    Concerning_digital_video_streaming_downloading_which_genres_are_you_interested_in: (
        Optional[
            Literal[
                "base",
                "animation_(cartoons_anime_etc)",
                "comedies",
                "documentaries",
                "dramas",
                "game_shows",
                "horror",
                "kids_shows",
                "music_videos_&_shows",
                "news_(local_or_national)",
                "reality_tv",
                "religious",
                "science_fiction_and_fantasy",
                "soap_operas_&_telenovelas",
                "sports",
                "talk_shows",
                "thriller/mystery/crime",
                "other",
                "dont_know",
            ]
        ]
    ) = Field(
        default=None,
        description="Concerning_digital_video_streaming_downloading_which_genres_are_you_interested_in",
    )
    How_often_do_you_normally_use_these_services_Media_frequency_eNewspapers: Optional[
        Literal["base", "frequent", "occasional"]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_these_services_Media_frequency_eNewspapers",
    )
    Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_Media_intensity_eNewspapers: Optional[
        Literal["base", "light", "moderate", "high", "dont_know"]
    ] = Field(
        default=None,
        description="Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_Media_intensity_eNewspapers",
    )
    Concerning_eMagazines_and_eNewspapers_what_type_of_content_do_you_consume: Optional[
        Literal[
            "base",
            "arts_&_crafts_magazines",
            "automotive_magazines",
            "comics_&_manga_magazines",
            "computers_&_electronics_magazines",
            "cooking_&_food_magazines",
            "entertainment_&_television_magazines",
            "fashion_style_or_beauty_magazines",
            "financial_&_business_magazines",
            "health_fitness_or_sports_magazines",
            "house_&_gardening_magazines_(incl_interior_design)",
            "music_magazines",
            "political_magazines",
            "religious_magazines",
            "technology_science_nature_or_medical_magazines",
            "travel_magazines",
            "womens_magazines",
            "daily_financial_newspapers",
            "evening_newspapers",
            "free_newspapers_(eg_washington_examiner)",
            "morning_newspapers",
            "newspaper_inserts_(eg_tv_guides)",
            "other",
            "don’t_know",
        ]
    ] = Field(
        default=None,
        description="Concerning_eMagazines_and_eNewspapers_what_type_of_content_do_you_consume",
    )
    How_often_do_you_normally_use_these_services_Media_frequency_Podcasts: Optional[
        Literal["base", "frequent", "occasional", "dont_know"]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_these_services_Media_frequency_Podcasts",
    )
    Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_Media_intensity_Podcasts: Optional[
        Literal["base", "light", "moderate", "high"]
    ] = Field(
        default=None,
        description="Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_Media_intensity_Podcasts",
    )
    Which_platforms_did_you_use_to_stream_download_podcasts_in_the_past_12_months_as_a_paying_customer: Optional[
        Literal[
            "base",
            "apple_podcasts",
            "audionow",
            "castbox",
            "castro",
            "deezer",
            "google_podcasts",
            "iheartradio",
            "overcast",
            "pocket_casts",
            "podbean",
            "podcastaddict",
            "soundcloud",
            "spotify",
            "stitcher",
            "other",
            "don’t_know",
            "i_did_not_pay_for_podcasts",
        ]
    ] = Field(
        default=None,
        description="Which_platforms_did_you_use_to_stream_download_podcasts_in_the_past_12_months_as_a_paying_customer",
    )
    Concerning_podcasts_what_type_of_content_do_you_consume: Optional[
        Literal[
            "base",
            "arts_crafts_&_design",
            "automotive",
            "entertainment_&_comedy",
            "technology_&_electronics",
            "cooking_&_food",
            "fashion_style_&_beauty",
            "finance_&_business",
            "health_fitness_&_sports",
            "history",
            "interior_decorating_house_&_gardening",
            "music",
            "movie_&_tv_series",
            "daily_news_updates",
            "parenting_&_partnership",
            "politics",
            "religion",
            "science_nature_or_medical",
            "traveling",
            "true_crime",
            "other",
            "don’t_know",
        ]
    ] = Field(
        default=None,
        description="Concerning_podcasts_what_type_of_content_do_you_consume",
    )
    How_often_do_you_normally_use_these_services_Media_frequency_Online_radio: Optional[
        Literal["base", "frequent", "occasional", "dont_know"]
    ] = Field(
        default=None,
        description="How_often_do_you_normally_use_these_services_Media_frequency_Online_radio",
    )
    Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_Media_intensity_Online_radio: Optional[
        Literal["base", "light", "moderate", "high", "dont_know"]
    ] = Field(
        default=None,
        description="Approximately_how_many_hours_in_an_average_week_do_you_use_these_services_Media_intensity_Online_radio",
    )
    Do_you_use_a_second_device_or_screen_while_watching_TV_or_video_content: Optional[
        Literal["base", "yes", "no", "don’t_know"]
    ] = Field(
        default=None,
        description="Do_you_use_a_second_device_or_screen_while_watching_TV_or_video_content",
    )
    If_yes_which_devices_do_you_normally_use_in_parallel: Optional[
        Literal[
            "base",
            "desktop_pc",
            "gaming_console_(eg_ps4_xbox)",
            "laptop_with_touch_screen",
            "regular_laptop_(without_touch_screen)",
            "smartphone",
            "tablet",
            "other",
        ]
    ] = Field(
        default=None, description="If_yes_which_devices_do_you_normally_use_in_parallel"
    )
    And_what_do_you_do_on_the_second_device: Optional[
        Literal[
            "base",
            "chat_to_/_message_friends",
            "use_social_media",
            "play_games",
            "read_my_e-mails",
            "read_the_news",
            "search_for_products_to_buy",
            "search_for_information_related_to_what_im_watching",
            "share_my_opinion_of_a_tv_show",
            "interact_with_the_online_content_of_the_tv_show",
            "other",
            "don’t_know",
        ]
    ] = Field(default=None, description="And_what_do_you_do_on_the_second_device")
    How_often_do_you_normally_purchase_products_online: Optional[
        Literal[
            "base",
            "once_per_week_or_more_often",
            "2-3_times_per_month",
            "once_per_month",
            "several_times_per_year",
            "less_often",
            "i_do_not_purchase_anything_online",
            "don’t_know",
            "base.1",
            "online_shopper",
            "non-online_shopper",
            "online_shopping_frequency_base",
            "online_shopping_frequency_frequent_(at_least_weekly)",
            "online_shopping_frequency_occasional",
            "online_shopping_frequency_dont_know",
        ]
    ] = Field(
        default=None, description="How_often_do_you_normally_purchase_products_online"
    )
    Which_type_of_products_have_you_bought_online_in_the_past_12_months: Optional[
        Literal[
            "base",
            "fmcg_(eg_food_and_cosmetics)",
            "apparel_(eg_clothes_shoes_and_accessories)",
            "media_and_recreational_supplies_(eg_films_music_hobby_equipment)",
            "household_and_garden_items_(eg_furniture)",
            "consumer_electronics_and_household_appliances_(eg_tvs_laptops)",
            "other",
            "don’t_know",
        ]
    ] = Field(
        default=None,
        description="Which_type_of_products_have_you_bought_online_in_the_past_12_months",
    )
    Before_purchasing_products_online_how_did_you_first_become_aware_of_the_products: (
        Optional[
            Literal[
                "base",
                "blog_post",
                "digital_media_advertising",
                "e-mail_advertising/newsletter/promotion",
                "featured_in_a_tv_program/movie/series",
                "from_friends_and/or_family",
                "online_advertising",
                "online_media_articles",
                "online_review",
                "online_store",
                "physical_store",
                "print_media_articles",
                "social_media",
                "tv/movie_advertising",
                "other",
                "don’t_know",
                "please_think_about_the_past_12_months_product_awareness_base",
                "please_think_about_the_past_12_months_product_awareness_online",
                "please_think_about_the_past_12_months_product_awareness_offline",
                "please_think_about_the_past_12_months_product_awareness_other",
                "please_think_about_the_past_12_months_product_awareness_dont_know",
            ]
        ]
    ) = Field(
        default=None,
        description="Before_purchasing_products_online_how_did_you_first_become_aware_of_the_products",
    )
    Before_purchasing_a_product_online_in_the_past_12_months_did_you_do_any_research_into_the_product: Optional[
        Literal[
            "base",
            "discussed_with_friends_or_family",
            "engaged_in_online_discussions_about_the_product",
            "read_online_reviews_from_consumers",
            "read_online_reviews_from_experts",
            "read_print_media_reviews_from_experts",
            "visited_a_physical_store_to_see_or_test_the_product",
            "visited_the_company_or_brand_website",
            "watched_youtube_reviews",
            "watched_unboxing_videos",
            "other",
            "i_did_not_do_any_research_about_the_product_before_purchasing",
        ]
    ] = Field(
        default=None,
        description="Before_purchasing_a_product_online_in_the_past_12_months_did_you_do_any_research_into_the_product",
    )
    What_were_the_most_important_reasons_for_deciding_where_to_purchase_products_online: Optional[
        Literal[
            "base",
            "advertising",
            "availability",
            "best_delivery/shipping",
            "best_price",
            "policy_on_returns",
            "preferred_website",
            "recommendation_from_experts",
            "recommendation_from_family_or_friends",
            "other",
            "don’t_know",
        ]
    ] = Field(
        default=None,
        description="What_were_the_most_important_reasons_for_deciding_where_to_purchase_products_online",
    )
    How_did_you_pay_for_the_products_purchased_online_in_the_past_12_months: Optional[
        Literal[
            "base",
            "by_invoice",
            "cash_in_advance",
            "cash_on_delivery",
            "credit_card",
            "debit_card",
            "direct_debit",
            "online_payment_(eg_paypal_amazon_pay)",
            "prepaid_cards/vouchers",
            "other",
            "don’t_know",
        ]
    ] = Field(
        default=None,
        description="How_did_you_pay_for_the_products_purchased_online_in_the_past_12_months",
    )
    Which_online_shopping_or_marketplace_websites_have_you_purchased_any_products_from_in_the_past_12_months: Optional[
        Literal[
            "base",
            "amazon",
            "apple",
            "bonprix",
            "conrad",
            "cyberport",
            "ebay",
            "h&m",
            "idealo",
            "lidl",
            "mediamarkt",
            "notebooksbilliger",
            "otto",
            "saturn",
            "tchibo",
            "zalando",
            "none_of_the_above",
        ]
    ] = Field(
        default=None,
        description="Which_online_shopping_or_marketplace_websites_have_you_purchased_any_products_from_in_the_past_12_months",
    )
    Which_of_the_following_online_payment_systems_have_you_used_in_the_past_12_months_to_purchase_these_products_online: Optional[
        Literal[
            "base",
            "2checkout",
            "amazon_pay",
            "apple_pay",
            "billpay",
            "giropay",
            "google_pay",
            "klarna",
            "masterpass",
            "neteller",
            "paydirekt",
            "paypal",
            "skrill",
            "stripe",
            "transferwise",
            "trustly",
            "other",
            "dont_know",
        ]
    ] = Field(
        default=None,
        description="Which_of_the_following_online_payment_systems_have_you_used_in_the_past_12_months_to_purchase_these_products_online",
    )
    After_purchasing_a_product_online_in_the_past_12_months_did_you_provide_any_feedback_reviews_If_so_where: Optional[
        Literal[
            "base",
            "contacted_the_product_company_or_brand_directly_via_website_or_e-mail",
            "contacted_the_website_where_i_purchased_the_product_directly_via_website_or_e-mail",
            "discussed_with_friends_and_family",
            "online_forums",
            "social_media",
            "publicly_on_the_product_company_or_brand_website",
            "publicly_on_the_website_where_i_purchased_the_product",
            "review_sites",
            "i_went_to_a_physical_store",
            "other",
            "i_did_not_provide_any_reviews_or_feedback",
            "/_feedback_type_base",
            "/_feedback_type_positive",
            "/_feedback_type_negative",
            "/_feedback_type_practical",
            "/_feedback_type_other",
        ]
    ] = Field(
        default=None,
        description="After_purchasing_a_product_online_in_the_past_12_months_did_you_provide_any_feedback_reviews_If_so_where",
    )
    Which_topics_did_you_cover_in_your_feedback_reviews: Optional[
        Literal[
            "base",
            "negative_feedback_about_customer_service",
            "negative_feedback_about_delivery_or_shipping",
            "negative_feedback_about_the_product",
            "negative_feedback_about_the_website_usability",
            "positive_feedback_about_customer_service",
            "positive_feedback_about_delivery_or_shipping",
            "positive_feedback_about_the_product",
            "positive_feedback_about_the_website_usability",
            "practical_feedback_on_how_to_use_or_what_to_expect_from_the_product",
            "other",
        ]
    ] = Field(
        default=None, description="Which_topics_did_you_cover_in_your_feedback_reviews"
    )
    When_you_are_at_a_physical_store_do_you_use_the_internet_on_a_device_for_any_of_the_following: Optional[
        Literal[
            "base",
            "comparing_prices_online",
            "searching_information_about_a_product",
            "talking_with_friends/family",
            "taking_notes_of_a_product_to_buy_it_online_later",
            "when_an_item_is_out_of_stock_purchasing_it_online",
            "following_a_qr_code_on_a_shelf/product",
            "none_of_the_above",
        ]
    ] = Field(
        default=None,
        description="When_you_are_at_a_physical_store_do_you_use_the_internet_on_a_device_for_any_of_the_following",
    )
    When_you_shopped_at_a_physical_store_which_payment_methods_did_you_use_in_the_past_12_months: Optional[
        Literal[
            "base",
            "cash",
            "credit_card",
            "debit_card",
            "prepaid_cards/vouchers",
            "payment_via_smartphone",
            "payment_via_smartwatch",
            "other",
            "don’t_know",
        ]
    ] = Field(
        default=None,
        description="When_you_shopped_at_a_physical_store_which_payment_methods_did_you_use_in_the_past_12_months",
    )
    The_following_questions_are_about_your_interests_and_hobbies_Which_of_the_following_statements_do_you_agree_with: Optional[
        Literal[
            "base",
            "i_discuss_my_hobby_with_others_in_online_communities",
            "i_go_online_to_find_people_to_take_part_in_hobbies_with_me_offline",
            "apps_provide_new_ways_for_me_to_enhance_my_offline_hobbies",
            "i_regularly_visit_websites_to_keep_up_to_date_with_my_hobby",
            "i_first_discovered/heard_about_my_hobby_online",
            "i_order_specialist_equipment_for_my_hobby_exclusively_online",
            "none_of_the_above",
        ]
    ] = Field(
        default=None,
        description="The_following_questions_are_about_your_interests_and_hobbies_Which_of_the_following_statements_do_you_agree_with",
    )
    Which_of_the_following_occupies_your_leisure_time: Optional[
        Literal[
            "base",
            "arts_and_crafts",
            "charity_work",
            "dancing",
            "dating",
            "esports",
            "food",
            "gardening",
            "health_and_fitness",
            "music",
            "pets",
            "photography",
            "playing_sports",
            "reading/writing",
            "socializing",
            "technology/computers",
            "travel",
            "video_games",
            "volunteering",
            "watching_sports",
            "other",
            "dont_know",
            "base.1",
            "engages_digitally",
            "does_not_engage_digitally",
        ]
    ] = Field(
        default=None, description="Which_of_the_following_occupies_your_leisure_time"
    )
    Which_of_your_hobbies_or_interests_do_you_engage_digitally_with_eg_use_an_app_watch_online_tutorials_discuss_on_forums_etc: Optional[
        Literal[
            "base",
            "arts_and_crafts",
            "charity_work",
            "dancing",
            "dating",
            "food",
            "gardening",
            "health_and_fitness",
            "music",
            "pets",
            "photography",
            "playing_sports",
            "reading/writing",
            "socializing",
            "travel",
            "volunteering",
            "watching_sports",
            "i_don’t_engage_with_any_of_my_hobbies_digitally",
            "base.1",
            "engages_digitally",
            "does_not_engage_digitally",
        ]
    ] = Field(
        default=None,
        description="Which_of_your_hobbies_or_interests_do_you_engage_digitally_with_eg_use_an_app_watch_online_tutorials_discuss_on_forums_etc",
    )
    The_following_questions_are_about_how_digital_technology_interacts_with_health_and_fitness_Which_of_the_following_applies_to_you: Optional[
        Literal[
            "base",
            "i_use_tracking_devices_(eg_smartwatch)",
            "i_use_free_fitness_apps",
            "i_use_paid_fitness_apps",
            "i_use_free_online_workout_videos",
            "i_pay_for_online_fitness_classes",
            "i_follow_sport/fitness_influencers_on_social_media",
            "i_research_new_training_methods_online",
            "i_use_the_digital_technology_provided_at_my_gym",
            "i_use_computer_programs_to_monitor_my_health_fitness",
            "i_work_out_using_video_games",
            "other",
            "i_dont_engage_with_my_health_and_fitness_in_a_digital_way",
        ]
    ] = Field(
        default=None,
        description="The_following_questions_are_about_how_digital_technology_interacts_with_health_and_fitness_Which_of_the_following_applies_to_you",
    )
    Why_do_you_use_fitness_apps_and_tracking_devices: Optional[
        Literal[
            "base",
            "they_allow_me_to_better_understand_my_body_and_to_advance_my_physical_health_specifically",
            "it_allows_me_to_challenge_myself",
            "it_allows_me_to_keep_track_of_/record_my_workouts",
            "it_motivates_me_to_compare_my_results_to_others",
            "in-app_games_and_rewards_make_exercising_more_fun",
            "other",
            "don’t_know",
        ]
    ] = Field(
        default=None, description="Why_do_you_use_fitness_apps_and_tracking_devices"
    )
    Which_of_the_following_tracking_devices_smartwatches_with_fitness_functions_do_you_own: Optional[
        Literal[
            "base",
            "adidas",
            "amazfit",
            "apple",
            "asus",
            "fitbit",
            "garmin",
            "honor",
            "huawei",
            "misfit",
            "polar",
            "samsung",
            "sony",
            "tomtom",
            "withings_/_nokia",
            "xiaomi/mi",
            "mykronoz",
            "other",
            "don’t_know",
        ]
    ] = Field(
        default=None,
        description="Which_of_the_following_tracking_devices_smartwatches_with_fitness_functions_do_you_own",
    )
    Have_you_used_online_dating_in_the_past_12_months: Optional[
        Literal["base", "yes", "no", "prefer_not_to_say"]
    ] = Field(
        default=None, description="Have_you_used_online_dating_in_the_past_12_months"
    )
    You_said_you_use_online_dating
    _what_were_the_reasons_you_decided_to_start_online_dating: Optional[
        Literal[
            "base",
            "just_to_have_a_good_time/fun/distraction",
            "i_was_curious",
            "to_find_intimate_partners",
            "to_have_fun_with_no_strings_attached",
            "to_lift_my_self-esteem",
            "to_find_someone_to_go_through_everyday_life_with",
            "to_find_love/emotional_connection",
            "to_get_romance_back_in_my_life",
            "i_was_just_looking_for_friends",
            "other",
            "don’t_know",
        ]
    ] = Field(
        default=None,
        description="You_said_you_use_online_dating;_what_were_the_reasons_you_decided_to_start_online_dating",
    )
    Which_of_the_following_platforms_have_you_used_in_the_past_12_months: Optional[
        Literal[
            "base",
            "badoo",
            "bumble",
            "c-date",
            "christianminglecom",
            "coffee_meets_bagel",
            "edarling",
            "elitepartner",
            "grindr",
            "happn",
            "jaumo",
            "lovescout24",
            "lovoo",
            "neude",
            "parship",
            "tinder",
            "other",
            "dont_know",
            "base.1",
            "paid_for_online_dating_services",
            "did_not_pay",
        ]
    ] = Field(
        default=None,
        description="Which_of_the_following_platforms_have_you_used_in_the_past_12_months",
    )
    And_for_which_of_these_services_did_you_pay: Optional[
        Literal[
            "base",
            "badoo",
            "bumble",
            "c-date",
            "christianminglecom",
            "coffee_meets_bagel",
            "edarling",
            "elitepartner",
            "grindr",
            "happn",
            "jaumo",
            "lovescout24",
            "lovoo",
            "neude",
            "parship",
            "tinder",
            "i_did_not_pay_for_an_online_dating_platform",
            "base.1",
            "online_course_participant",
            "did_not_take_part_in_an_online_course",
        ]
    ] = Field(default=None, description="And_for_which_of_these_services_did_you_pay")
    Have_you_taken_online_training_courses_eg_master_classes_in_any_of_these_fields_in_the_past_12_months: Optional[
        Literal[
            "base",
            "lifestyle_(eg_makeup_interior_design)",
            "culinary_arts",
            "language_courses",
            "music_&_entertainment_(eg_instruments_comedy)",
            "writing",
            "film_&_tv_(eg_filmmaking_directing)",
            "science_&_technology",
            "business_politics_&_society",
            "sports_&_games_(eg_poker_game_design_tennis)",
            "design_photography_&_fashion",
            "other",
            "i_have_not_taken_any_online_training_courses",
            "base.1",
            "paid_for_online_course",
            "did_not_pay",
        ]
    ] = Field(
        default=None,
        description="Have_you_taken_online_training_courses_eg_master_classes_in_any_of_these_fields_in_the_past_12_months",
    )
    And_for_which_of_these_courses_did_you_pay_for: Optional[
        Literal[
            "base",
            "lifestyle_(eg_makeup_interior_design)",
            "culinary_arts",
            "language_courses",
            "music_&_entertainment_(eg_instruments_comedy)",
            "writing",
            "film_&_tv_(eg_filmmaking_directing)",
            "science_&_technology",
            "business_politics_&_society",
            "sports_&_games_(eg_poker_game_design_tennis)",
            "design_photography_&_fashion",
            "other",
            "i_did_not_pay_for_any_course_or_training",
        ]
    ] = Field(
        default=None, description="And_for_which_of_these_courses_did_you_pay_for"
    )
    The_following_questions_are_about_working_from_home_Have_you_worked_from_home_in_the_past_12_months: Optional[
        Literal["base", "yes", "no", "i_do_not_work"]
    ] = Field(
        default=None,
        description="The_following_questions_are_about_working_from_home_Have_you_worked_from_home_in_the_past_12_months",
    )
    Thinking_about_working_from_home_which_of_the_following_statements_do_you_agree_with: Optional[
        Literal[
            "base",
            "my_productivity_is_better_when_i_work_from_home",
            "working_from_home_has_had_a_negative_impact_on_my_mental_well-being",
            "i_find_i_have_more_free_time_when_i_work_from_home",
            "i_have_used_the_programs_i_work_with_to_contact_friends_and_family_(eg_zoom)",
            "i_feel_lonely_working_from_home",
            "i_miss_social_interactions_at_the_office",
            "as_a_society_we_should_work_from_home_more_after_covid-19",
            "none_of_the_above",
        ]
    ] = Field(
        default=None,
        description="Thinking_about_working_from_home_which_of_the_following_statements_do_you_agree_with",
    )
    What_were_the_reasons_you_worked_from_home_in_the_past_12_months: Optional[
        Literal[
            "base",
            "covid-19/coronavirus",
            "it_is_part_of_my_company’s_policy_(unrelated_to_covid-19)",
            "i_work_at_home_full-time",
            "my_job_is_in_itself_home-based",
            "my_company_does_not_have_an_office",
            "childcare",
            "i_have_been_taking_care_of_relatives",
            "other",
            "don’t_know",
            "base.1",
            "due_to",
            "only_due_to",
            "in_general_despite",
        ]
    ] = Field(
        default=None,
        description="What_were_the_reasons_you_worked_from_home_in_the_past_12_months",
    )
    Which_of_these_statements_do_you_agree_with: Optional[
        Literal[
            "base",
            "i_consciously_decide_to_“digitally_detox”_(eg_reduce_my_internet_usage)_to_improve_my_mental_well-being",
            "i_am_afraid_i_will_miss_something_important_if_i_dont_check_my_smartphone_constantly",
            "i_hate_it_when_people_look_at_their_phones_in_the_middle_of_a_conversation",
            "the_expectation_i_should_always_be_available_is_mentally_exhausting",
            "increased_digitalization_has_had_a_negative_impact_on_people’s_mental_health",
            "during_the_covid-19/coronavirus_pandemic_being_able_to_connect_with_friends_digitally_made/makes_me_feel_less_lonely",
            "digitalization_has_helped_me_feel_close_to_friends_and_family_who_live_far_away",
            "none_of_the_above",
        ]
    ] = Field(default=None, description="Which_of_these_statements_do_you_agree_with")
    How_has_the_growing_influence_of_online_and_digital_technology_impacted_your_mental_wellbeing_Wellbeing_Impact: Optional[
        Literal[
            "base",
            "postive_impact",
            "negative_impact",
            "no_impact",
            "neither_/_dont_know",
        ]
    ] = Field(
        default=None,
        description="How_has_the_growing_influence_of_online_and_digital_technology_impacted_your_mental_wellbeing_Wellbeing_Impact",
    )
    How_has_the_growing_influence_of_online_and_digital_technology_impacted_your_mental_wellbeing: Optional[
        Literal[
            "base",
            "improved_it",
            "improved_it_slightly",
            "neither_nor",
            "made_it_slightly_worse",
            "made_it_worse",
            "don’t_know",
        ]
    ] = Field(
        default=None,
        description="How_has_the_growing_influence_of_online_and_digital_technology_impacted_your_mental_wellbeing",
    )
    How_do_you_prefer_to_contact_brands_or_companies_online: Optional[
        Literal[
            "base",
            "via_e-mail",
            "via_the_websites_contact_form",
            "via_social_media_channels_(eg_facebook)",
            "via_a_chat_on_the_website_(eg_a_chatbot/ai)",
            "via_a_private_messaging_service_(eg_whatsapp)",
            "via_video_chat",
            "other",
            "don’t_know",
        ]
    ] = Field(
        default=None,
        description="How_do_you_prefer_to_contact_brands_or_companies_online",
    )
    When_you_think_about_brands_and_companies_on_social_media_which_types_of_content_are_you_interested_in_seeing_from_them: Optional[
        Literal[
            "base",
            "their_employees",
            "company_news",
            "collaborations_with_influencers",
            "market/industry_insights",
            "behind-the-scenes_content",
            "contests_and_giveaways",
            "takeover_posts_by_guests",
            "previews_and_teasers",
            "faqs_from_customers",
            "tips_and_tricks",
            "events",
            "special_sales_offers",
            "polls_and_surveys",
            "press_mentions",
            "other",
            "don’t_know",
        ]
    ] = Field(
        default=None,
        description="When_you_think_about_brands_and_companies_on_social_media_which_types_of_content_are_you_interested_in_seeing_from_them",
    )
    And_in_what_way_do_you_like_to_receive_this_content_from_brands_and_companies_on_social_media: Optional[
        Literal[
            "base",
            "videos",
            "live_videos",
            "video_stories",
            "gifs",
            "images",
            "infographics",
            "memes",
            "written_posts_(eg_blogs_articles_guides)",
            "links_to_external_content",
            "user_testimonials_and_reviews",
            "other",
            "don’t_know",
        ]
    ] = Field(
        default=None,
        description="And_in_what_way_do_you_like_to_receive_this_content_from_brands_and_companies_on_social_media",
    )
    Where_have_you_seen_or_heard_ads_online_in_the_past_4_weeks: Optional[
        Literal[
            "base",
            "advertising_videos_on_websites",
            "advertising_videos_on_youtube",
            "banner_ads_on_websites_(integrated_or_pop-ups)",
            "e-mails/newsletters",
            "within_apps",
            "audiobooks",
            "emagazines_&_enewspapers",
            "podcasts",
            "online_radio",
            "digital_video_streaming_platforms",
            "live_streaming_platforms",
            "digital_music_platforms",
            "sponsored_posts_on_social_media_(from_brands_i_dont_follow)",
            "posts_on_social_media_(from_brands_i_actively_follow)",
            "influencer_posts_on_social_media",
            "sponsored_results_in_search_engines",
            "other",
            "i_did_not_see/hear_any_online_ads",
            "base.1",
            "reactive_to_advertising",
            "nonreactive_to_advertising",
        ]
    ] = Field(
        default=None,
        description="Where_have_you_seen_or_heard_ads_online_in_the_past_4_weeks",
    )
    Which_of_these_advertisements_caused_you_to_actively_click_on_them_or_look_up_additional_information: Optional[
        Literal[
            "base",
            "advertising_videos_on_websites",
            "advertising_videos_on_youtube",
            "banner_ads_on_websites_(integrated_or_pop-ups)",
            "e-mails/newsletters",
            "within_apps",
            "audiobooks",
            "emagazines_&_enewspapers",
            "podcasts",
            "online_radio",
            "digital_video_streaming_platforms",
            "live_streaming_platforms",
            "digital_music_platforms",
            "sponsored_posts_on_social_media_(from_brands_i_dont_follow)",
            "posts_on_social_media_(from_brands_i_actively_follow)",
            "influencer_posts_on_social_media",
            "sponsored_results_in_search_engines",
            "other",
            "i_did_not_click_on_any_of_them",
        ]
    ] = Field(
        default=None,
        description="Which_of_these_advertisements_caused_you_to_actively_click_on_them_or_look_up_additional_information",
    )
    Which_devices_do_you_use_regularly_at_home: Optional[
        Literal[
            "base",
            "desktop_pc",
            "gaming_console_(eg_ps4_xbox)",
            "laptop_with_touch_screen",
            "regular_laptop_(without_touch_screen)",
            "smart_speakers_(eg_amazon_echo)",
            "smart_tv",
            "smartphone",
            "smartwatch",
            "streaming_device_(eg_apple_tv_chromecast)",
            "tablet",
            "mobile_and_stationary_user_base",
            "mobile_and_stationary_user_mobile_user_only_(smartphone)",
            "mobile_and_stationary_user_stationary_user_only_(desktop_pc_/_laptop)",
            "mobile_and_stationary_user_mobile_and_stationary_user_(smartphone_/_desktop_pc_/_laptop)",
            "mobile_and_stationary_user_other_devices_only",
        ]
    ] = Field(default=None, description="Which_devices_do_you_use_regularly_at_home")
    Which_operating_systems_do_you_use_on_your_computer_egdesktop_or_laptop: Optional[
        Literal[
            "base",
            "microsoft_windows",
            "macos",
            "linux",
            "chrome_os",
            "ubuntu",
            "other",
            "don’t_know",
        ]
    ] = Field(
        default=None,
        description="Which_operating_systems_do_you_use_on_your_computer_egdesktop_or_laptop",
    )
    Which_operating_systems_do_you_use_on_your_mobile_devices_eg_tablet_or_smartphone: (
        Optional[
            Literal[
                "base",
                "android_os",
                "ios",
                "linux",
                "blackberry_os",
                "windows",
                "harmony_os",
                "other",
                "don’t_know",
            ]
        ]
    ) = Field(
        default=None,
        description="Which_operating_systems_do_you_use_on_your_mobile_devices_eg_tablet_or_smartphone",
    )
    Which_virtual_assistants_do_you_use_with_your_smart_speakers: Optional[
        Literal[
            "base",
            "google_assistant",
            "siri",
            "alexa",
            "cortana",
            "duer",
            "aligenie",
            "hound",
            "other",
            "don’t_know",
        ]
    ] = Field(
        default=None,
        description="Which_virtual_assistants_do_you_use_with_your_smart_speakers",
    )
    The_following_questions_are_about_which_digital_services_you_use_How_do_you_prefer_to_register_when_using_a_new_digital_service_platform_or_product: Optional[
        Literal[
            "base",
            "i_create_a_new_account_with_a_new_e-mail_address",
            "i_create_a_new_account_with_an_existing_e-mail_address",
            "i_log_in_with_an_existing_account_from_a_different_service_(eg_facebook)",
            "other",
            "don’t_know",
        ]
    ] = Field(
        default=None,
        description="The_following_questions_are_about_which_digital_services_you_use_How_do_you_prefer_to_register_when_using_a_new_digital_service_platform_or_product",
    )
    Which_account_do_you_mainly_use_when_logging_into_a_new_digital_service_platform_or_product: Optional[
        Literal[
            "base",
            "facebook_account",
            "google_account",
            "microsoft_account",
            "alipay_account",
            "apple_account",
            "other",
            "don’t_know",
        ]
    ] = Field(
        default=None,
        description="Which_account_do_you_mainly_use_when_logging_into_a_new_digital_service_platform_or_product",
    )
    Do_you_use_any_of_these_cloud_storage_solutions_for_personal_use: Optional[
        Literal[
            "base",
            "google_one/google_drive",
            "apple_icloud",
            "dropbox",
            "microsoft_onedrive",
            "amazon_drive_cloud",
            "box",
            "mega",
            "ali_yun",
            "baidu_yun/wangpan",
            "kingsoft_kuaipan",
            "pcloud",
            "synccom",
            "degoo",
            "opendrive",
            "nextcloud",
            "i_don’t_use_any_cloud_storage_systems",
            "don’t_know",
            "base.1",
            "cloud_storage_user",
            "non-user",
        ]
    ] = Field(
        default=None,
        description="Do_you_use_any_of_these_cloud_storage_solutions_for_personal_use",
    )
    What_do_you_use_your_cloud_storage_services_for: Optional[
        Literal[
            "base",
            "photos",
            "backups",
            "office_documents",
            "music/videos",
            "financial_information",
            "passwords/login_data",
            "other",
            "don’t_know",
        ]
    ] = Field(
        default=None, description="What_do_you_use_your_cloud_storage_services_for"
    )
    Do_you_use_any_of_these_services_and_or_software_to_create_andoror_edit_word_spreadsheet_andoror_presentation_files_for_personal_tasks: Optional[
        Literal[
            "base",
            "microsoft_office",
            "openoffice",
            "iwork",
            "libreoffice",
            "wps_office",
            "yozosoft",
            "google_docs_/_g_suite",
            "g_suite",
            "zoho_office_suite",
            "i_don’t_use_any_personally",
            "don’t_know",
            "base.1",
            "office_suite_user",
            "non-user",
        ]
    ] = Field(
        default=None,
        description="Do_you_use_any_of_these_services_and_or_software_to_create_andoror_edit_word_spreadsheet_andoror_presentation_files_for_personal_tasks",
    )
