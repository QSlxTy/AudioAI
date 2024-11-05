

prompt_meeting_minutes = """
Создай протокол встречи на основе расшифровки.

Требования:
- Учитывай контекст беседы и выделяй ключевые моменты, которые необходимо зафиксировать в протоколе.
- Обеспечь полноту и точность при описании решений и назначении ответственных.
- В случаях, когда сроки выполнения не указаны, предложи их на основе контекста и логики обсуждения.
- Упоминай любые потенциальные риски или вызовы, связанные с выполнением решений.
- В заключении укажи на возможные дальнейшие шаги и кто должен их инициировать.

Формат ответа:

**Участники:**
- Укажи количество участников и время, когда каждый участник говорит свою первую фразу. Пример:
  - SPEAKER_01 (первая фраза в 00:01:14)
  - SPEAKER_02 (первая фраза в 00:10:23)
  - и т.д.

**Основные вопросы:**
1. Укажи тему обсуждения, кто начал обсуждение, и кратко изложи основную информацию по теме.
2. Для каждого вопроса/темы укажи спикеров, которые вносили важные замечания, и опиши суть их замечаний.
3. В случае разногласий, кратко опиши суть разногласий и как они были решены.

**Решения и действия:**
- Для каждого обсужденного вопроса укажи принятое решение или назначенные действия.
- Укажи ответственных за выполнение каждого действия и сроки выполнения, если они были упомянуты.
- В случае отсутствия указанных сроков, предложи их на основе контекста.

**Заключение:**
- Кратко подведи итоги встречи.
- Укажи, какие вопросы остались нерешенными и будут обсуждаться на следующей встрече, если это было упомянуто.
- Отметь потенциальные риски или проблемы, которые могут возникнуть при реализации решений.
"""


prompt_summary = """
Создай краткую выжимку на основе расшифровки.

Требования:
- Выделяй ключевые моменты обсуждения, включая цели встречи, основную тему и сделанные выводы.
- Определи ключевых спикеров и кратко изложи основные тезисы их выступлений.
- Упомяни наиболее важные и значимые цитаты, которые отражают суть обсуждения или важные моменты встречи.
- Учитывай контекст беседы и подчеркивай только самое важное, чтобы выжимка была сжато и информативно передана.

Формат ответа:

**Основные моменты записи:**
1. Введение и цели обсуждения: [Краткое описание, что обсуждалось SPEAKER_01 и SPEAKER_02]
2. Основная тема: [Краткое изложение главной темы обсуждения]
3. Заключение: [Выводы и основные решения]

**Ключевые спикеры:**
- SPEAKER_01: [Основные тезисы выступления]
- SPEAKER_03: [Основные тезисы выступления]

"""


prompt_analysis = """
Создай анализ встречи на основе расшифровки.

Участники:
- Укажи количество участников и время, когда каждый участник говорит свою первую фразу. Пример:
  - SPEAKER_01 (первая фраза в 00:01:14)
  - SPEAKER_02 (первая фраза в 00:10:23)
  - и т.д.

Требования:
- Учитывай контекст беседы и охватывай ключевые моменты, которые отражают основные темы обсуждения.
- Определяй эмоциональное состояние и тональность речи каждого участника, опираясь на их реплики и общий стиль общения.
- Выделяй разногласия между участниками и указывай, как эти разногласия были решены, кто поддержал те или иные решения.
- Если обсуждались конкретные проблемы или вызовы, укажи их, а также предложенные пути их решения.
- Включай оценку эффективности взаимодействия участников, а также возможные области для улучшения в дальнейшем.

Формат ответа:

Анализ диалога:

Эмоции и тональность (опиши речь каждого спикера):
- SPEAKER_01: [Описание эмоций, тональности, например, уверенный, спокойный]
- SPEAKER_03: [Описание эмоций, например, озабоченный, настороженный]
- и т.д.

Ключевые моменты:
1. Обсуждение [Темы 1]: [Краткое изложение ключевых моментов]
2. Дискуссия по [Теме 2]: [Краткий анализ мнений]
- и т.д.

Разногласия и их разрешение (если это применимо):
- Разногласие: [Описание разногласия между SPEAKER_ХХ и SPEAKER_ХХ]
- Решение: [Как было найдено решение, кто поддержал].

Заключение:
- [Итоговая оценка диалога, эффективность взаимодействия участников].
- [Области для улучшения или возможные дальнейшие шаги].
"""


prompt_tasks = """
Создай перечень действий на основе расшифровки.

Участники:
- Укажи количество участников и время, когда каждый участник говорит свою первую фразу. Пример:
  - SPEAKER_01 (первая фраза в 00:01:14)
  - SPEAKER_02 (первая фраза в 00:10:23)
  - и т.д.

Требования:
- Учитывай контекст беседы и выделяй только важные действия, которые требуют последующих шагов.
- Определяй ответственных за каждое действие, включая те, которые не были явно обозначены в разговоре, но логически вытекают из обсуждения. Выделяй ключевые задачи и назначай ответственных лиц.
- Если сроки выполнения задач не были указаны, предложи их на основе контекста.
- Выделяй потенциальные риски или проблемы, которые могут возникнуть при выполнении этих действий.
- Если сроки выполнения задач не были указаны, пропиши, что "сроки не обсуждались".
- Формат ответа должен быть компактным, чтобы удобно использовать для дальнейшего управления задачами.

Формат ответа:

Перечень действий на основе обсуждения:

1. Действие 1:
   - Описание: [Что необходимо сделать на основе обсуждения]
   - Ответственный: SPEAKER_01
   - Срок выполнения: [Дата/время]

2. Действие 2:
   - Описание: [Что необходимо сделать на основе обсуждения]
   - Ответственный: SPEAKER_03
   - Срок выполнения: [Дата/время]

3. Действие 3:
   - Описание: [Что необходимо сделать на основе обсуждения]
   - Ответственный: SPEAKER_02
   - Срок выполнения: [Дата/время]

Общий статус: [Краткая сводка статуса задач, прогресс, возможные риски].
"""

