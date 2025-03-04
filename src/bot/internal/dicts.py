# fmt: off

texts = {
    'welcome': 'Здравствуйте, дорогой любимый садовник! 🌱\n'
               'Я ваш личный помощник по озеленению — тот, кто поможет вам создать настоящий райский уголок, '
               'будь то уютный садик или зелёное пространство внутри дома. '
               'Расскажите мне немного о ваших планах, и мы вместе воплотим их в жизнь!',
    'begin': 'Что вас больше всего волнует сегодня?\n'
             'Возможно, вы хотите спланировать свой участок или, быть может, украсить дом живыми растениями? '
             'Давайте поговорим об этом!',
    'space': 'Расскажите, пожалуйста, какой территорией или пространством вы обладаете?\n'
             'Это может быть уютный сад за городом или светлая комната в квартире. '
             'Пусть наша беседа станет началом вашего зелёного приключения!',
    'indoor_area': "Как здорово, что вы хотите добавить больше зелени в свой дом!\n"
                   "Расскажите, пожалуйста, о пространстве, которое вы хотите озеленить. "
                   "Это может быть гостиная, спальня или даже офис. Каков примерно её размер? "
                   "Например, '20 квадратных метров' или 'комнатка-студия'.",
    'indoor_budget': "А теперь давайте поговорим о бюджете для ваших комнатных растений. Какие планы? "
                     "Например, 'хочу пару красивых цветов до 5 тысяч' или 'готов создать целую коллекцию'. "
                     "Ваше желание — наш закон!",
    'indoor_budget_reply': "Превосходно! С учётом вашего бюджета, я смогу предложить множество интересных идей, "
                           "которые сделают вашу  помещение ещё прекраснее!",
    'outdoor_area': "Какая замечательная идея — создать свой маленький сад! "
                    "А теперь, расскажите поподробнее: какой размер вашего участка? "
                    "Может быть, это  небольшой дворик или просторный участок? "
                    "Например, '10x10 метров' или '5 соток'. Каждый квадратный метр имеет значение!",
    'outdoor_budget': "Чтобы предложить вам самые подходящие варианты, позвольте узнать: "
                      "какой у вас примерный бюджет на создание вашего зелёного уг олка? "
                      "Не нужно точных цифр — просто дайте приблизительную оценку. "
                      "Например, 'до 10 тысяч рублей' или 'готов потратиться на что-то особенное'.",
    'outdoor_budget_reply': "Превосходно! С учётом вашего бюджета, я смогу предложить множество интересных идей, "
                            "которые сделают вашу  территорию  ещё прекраснее!",
    'geo_indoor': 'Из какого вы города или региона? Это поможет мне учесть особенности вашего климата '
                  'и предложить подходящие растения.',
    'geo_indoor_room_1': "Представьте на мгновение свой идеальный интерьер с живыми растениями. "
                         "Где бы вы хотели видеть эти прекрасные создания? "
                         "В светлой гостиной, наполненной солнцем, или, быть может, "
                         "в спокойной спальне, где они помогут вам расслабиться? "
                         "Расскажите мне об этом месте, и мы вместе создадим атмосферу вашей мечты!",
    'geo_indoor_room_2': "Дорогой друг, давайте теперь поговорим о вашем  пространстве. "
                         "Какой комнатой или зоной вы хотите заняться? "
                         "Это может быть уютная гостиная, светлая спальня или даже рабочий уголок в офисе. "
                         "Расскажите мне больше об этом месте, чтобы мы могли вместе создать идеальный зелёный оазис!",
    'geo_outdoor': 'Дорогой друг, чтобы учесть все особенности вашего климата и подобрать наиболее подходящие растения, '
                   'расскажите, пожалуйста, из какого вы города или региона? '
                   'Это поможет нам создать идеальный план, который будет работать именно для вас!',
    'geo_reply': 'Отлично! {} — место с удивительным климатом. '
                 'Теперь я знаю, какие растения будут чувствовать себя здесь как дома!',
    'indoor_style': "Какой стиль озеленения помещения вам больше всего по душе? "
                    "Городской шик, тропические джунгли, экологичность или что-то уникальное? "
                    "Ваш выбор задаст тон всему пространству!",
    'indoor_style_reply': "Какой восхитительный выбор! {} — это именно то, что сделает ваше пространство  особенным. "
                          "Мы обязательно учтём этот важный момент!",
    'outdoor_style': "А теперь самое интересное: какой стиль сада вы хотели бы воплотить? "
                     "Возможно, вы любите естественную красоту природы, или же вам ближе классический порядок, "
                     "или, быть может, вы фанат минимализма? Расскажите, каким видите свой идеальный сад!",
    'outdoor_style_reply': "Какой восхитительный выбор! {} — это именно то, что сделает вашу территорию особенным. "
                           "Мы обязательно учтём этот важный момент!",
    'confirmation_indoor': "Знаете, как здорово мы продвинулись! Представляю себе ваше пространство — уютное, "
                           "наполненное светом и готовое встретить новых зелёных жителей. "
                           "Вы рассказали мне, что ваше помещение имеет размер примерно {}, "
                           "а ваш бюджет позволяет воплотить действительно интересные идеи. "
                           "К тому же, я учту особенности вашего региона, чтобы выбрать растения, "
                           "которые будут чувствовать себя здесь как дома. "
                           "И конечно, ваш любимый стиль {} станет основой для создания уникального интерьера, "
                           "где каждое растение будет не просто украшением, а настоящим источником энергии и гармонии.",
    'change_settings_indoor': 'Если что-то нужно изменить, не стесняйтесь сказать! '
                              'Мы можем скорректировать любые детали, чтобы всё было идеально.',
    'confirmation_outdoor': "Как прекрасно представить ваш [участок] — просторный, живой и полный возможностей! "
                            "Мы уже знаем, что он имеет примерно [такой-то] размер, "
                            "находится в вашем любимом [месте на карте], и вы хотите создать именно [стиль пользователя] сад, "
                            "который будет радовать вас каждый день. "
                            "Ваш бюджет позволит нам воплотить множество замечательных идей, "
                            "от выбора подходящих растений до планирования их размещения. "
                            "Здесь каждый квадратный метр станет частью вашей истории, "
                            "где природа и дизайн объединятся в идеальном сочетании!",
    'change_settings_outdoor': 'Если что-то нужно изменить, не стесняйтесь сказать! '
                               'Мы можем скорректировать любые детали, чтобы всё было идеально.',
    'indoor_interests': "Какие растения вы хотели бы увидеть в своём доме? "
                        "Или, быть может, вам нужен план их размещения? "
                        "Давайте создадим идеальное пространство для жизни!",
    'outdoor_interests': "Что вас больше всего интересует сейчас? "
                         "Возможно, список подходящих растений, план размещения или советы по уходу? "
                         "Давайте решим это вместе!",

}

# fmt: on
