"""Copy for the per-service landing pages (English and Arabic).

Prices, service names and the shared FAQ answers are NOT stored here: tools/build.py reads
them from index.html so they always match what visitors see on the home page. This file only
holds the extra wording each page needs. Statements are limited to what the site already says
about the service (see index.html); do not add claims (timelines, client numbers, results)
that the home page does not make.
"""

# --------------------------------------------------------------------------- AI service pages
# `match` is the English service title on the home page (data-request-title).
AI_PAGES = [
    {
        "slug": "ai-product-visuals",
        "match": "AI Product Visuals",
        "title": {
            "en": "AI Product Photography & Visuals",
            "ar": "صور ورسومات منتجات بالذكاء الاصطناعي",
        },
        "description": {
            "en": "AI product photos and campaign visuals without a photoshoot, from AED 499. H.M Media creates them for brands across the UAE, GCC and the Middle East.",
            "ar": "صور منتجات وتصاميم حملات بالذكاء الاصطناعي بدون جلسة تصوير، تبدأ من 499 درهم. تنفذها H.M Media للعلامات التجارية في الإمارات والخليج والشرق الأوسط.",
        },
        "h1": {
            "en": ("AI product photos and visuals", "without a photoshoot."),
            "ar": ("صور وتصاميم منتجات بالذكاء الاصطناعي", "بدون جلسة تصوير."),
        },
        "intro": {
            "en": "Send us your product and a few lines about your brand, and we turn them into studio-quality photos and campaign visuals made with AI. It suits online stores, social media, ads and launches, and it skips the cost and logistics of a photoshoot.",
            "ar": "أرسل لنا منتجك وبضعة أسطر عن علامتك، ونحوّلها إلى صور وتصاميم حملات بجودة الاستوديو بالذكاء الاصطناعي. مناسبة للمتاجر الإلكترونية والسوشيال ميديا والإعلانات وإطلاق المنتجات، وتوفّر عليك تكلفة جلسة التصوير وتعقيداتها.",
        },
        "gets": {
            "en": [
                "Studio-quality product photos created with AI",
                "Campaign visuals for social media, ads and online stores",
                "Visual direction that follows your brand, colours and references",
                "An exact quote and agreed deliverables before work starts",
            ],
            "ar": [
                "صور منتجات بجودة الاستوديو بالذكاء الاصطناعي",
                "تصاميم حملات للسوشيال ميديا والإعلانات والمتاجر الإلكترونية",
                "هوية بصرية تتبع علامتك وألوانك ومراجعك",
                "عرض سعر دقيق وتسليمات متفق عليها قبل بدء العمل",
            ],
        },
        "good_for": {
            "en": [
                "Online stores and marketplaces",
                "Perfume, cosmetics, beverages and packaged goods",
                "Launch posts, paid ads and seasonal campaigns",
                "Brands that need many visuals quickly",
            ],
            "ar": [
                "المتاجر الإلكترونية والأسواق الرقمية",
                "العطور ومستحضرات التجميل والمشروبات والمنتجات المعبأة",
                "منشورات الإطلاق والإعلانات المدفوعة وحملات المواسم",
                "العلامات التي تحتاج عدداً كبيراً من التصاميم بسرعة",
            ],
        },
        "faq": [
            {
                "q": {"en": "Do I need a photoshoot first?", "ar": "هل أحتاج جلسة تصوير أولاً؟"},
                "a": {
                    "en": "No. This service is built so you do not need a photoshoot. Send a product photo and your references, and we create the visuals with AI.",
                    "ar": "لا. هذه الخدمة مصممة بحيث لا تحتاج جلسة تصوير. أرسل صورة المنتج ومراجعك، ونصنع التصاميم بالذكاء الاصطناعي.",
                },
            },
            {
                "q": {"en": "Can the visuals match my brand?", "ar": "هل تتوافق التصاميم مع هوية علامتي؟"},
                "a": {
                    "en": "Yes. Share your logo or brand guidelines, colours and reference images, and we direct the visuals to match them.",
                    "ar": "نعم. شاركنا شعارك أو دليل هويتك وألوانك وصور المراجع، ونوجّه التصاميم لتتوافق معها.",
                },
            },
        ],
        "related": ["ai-video-ads", "cgi-3d-product-ads", "ai-automation"],
    },
    {
        "slug": "ai-video-ads",
        "match": "AI Video Ads & Avatars",
        "title": {
            "en": "AI Video Ads & AI Avatars (Arabic & English)",
            "ar": "إعلانات فيديو وأفاتار بالذكاء الاصطناعي (عربي وإنجليزي)",
        },
        "description": {
            "en": "AI video ads, presenters and UGC-style clips in Arabic or English, from AED 799. H.M Media produces them for brands across the UAE, GCC and the Middle East.",
            "ar": "إعلانات فيديو ومقدمون ومقاطع بأسلوب UGC بالذكاء الاصطناعي بالعربية أو الإنجليزية، تبدأ من 799 درهم. تنتجها H.M Media للعلامات التجارية في الإمارات والخليج والشرق الأوسط.",
        },
        "h1": {
            "en": ("AI video ads and avatars", "in Arabic or English."),
            "ar": ("إعلانات فيديو وأفاتار بالذكاء الاصطناعي", "بالعربية أو الإنجليزية."),
        },
        "intro": {
            "en": "Video ads, AI presenters and UGC-style clips made with AI, in Arabic or English. Tell us the product, the offer and the platform, and we create the videos and hand over final files, ready for your platforms.",
            "ar": "إعلانات فيديو ومقدمون ومقاطع بأسلوب UGC بالذكاء الاصطناعي، بالعربية أو الإنجليزية. أخبرنا بالمنتج والعرض والمنصة، ونصنع الفيديوهات ونسلّمك الملفات النهائية جاهزة لمنصاتك.",
        },
        "gets": {
            "en": [
                "Video ads made with AI, in Arabic or English",
                "AI presenters and avatars",
                "UGC-style clips for social media",
                "Final files ready for your platforms",
            ],
            "ar": [
                "إعلانات فيديو بالذكاء الاصطناعي بالعربية أو الإنجليزية",
                "مقدمون وأفاتار بالذكاء الاصطناعي",
                "مقاطع بأسلوب UGC للسوشيال ميديا",
                "ملفات نهائية جاهزة لمنصاتك",
            ],
        },
        "good_for": {
            "en": [
                "National Day and seasonal campaigns",
                "Product launches and special offers",
                "Brands that need video without a film crew",
            ],
            "ar": [
                "حملات اليوم الوطني والمواسم",
                "إطلاق المنتجات والعروض الخاصة",
                "العلامات التي تحتاج فيديو بدون فريق تصوير",
            ],
        },
        "faq": [
            {
                "q": {"en": "Can the videos be in Arabic?", "ar": "هل يمكن أن تكون الفيديوهات بالعربية؟"},
                "a": {
                    "en": "Yes. We produce AI video ads, presenters and UGC-style clips in Arabic or English.",
                    "ar": "نعم. ننتج إعلانات الفيديو والمقدمين ومقاطع UGC بالذكاء الاصطناعي بالعربية أو الإنجليزية.",
                },
            },
            {
                "q": {"en": "Can you also film real video?", "ar": "هل تصوّرون فيديو حقيقياً أيضاً؟"},
                "a": {
                    "en": "Yes. Our agency services include reels and short videos, explainer videos, logo animation and a photo and video shoot day. See Video & Motion.",
                    "ar": "نعم. تشمل خدمات الوكالة الريلز والفيديوهات القصيرة وفيديوهات الشرح وتحريك الشعار ويوم تصوير فوتو وفيديو. راجع فيديو وموشن.",
                },
            },
        ],
        "related": ["ai-product-visuals", "cgi-3d-product-ads", "ai-chatbots-whatsapp-agents"],
    },
    {
        "slug": "cgi-3d-product-ads",
        "match": "CGI & 3D Product Ads",
        "title": {
            "en": "CGI & 3D Product Ads and Animations",
            "ar": "إعلانات منتجات CGI وثلاثية الأبعاد",
        },
        "description": {
            "en": "3D product animations and CGI scenes for ads, from AED 1,999. H.M Media creates them for brands across the UAE, GCC and the Middle East.",
            "ar": "رسوم متحركة ثلاثية الأبعاد لمنتجك ومشاهد CGI للإعلانات، تبدأ من 1,999 درهم. تنفذها H.M Media للعلامات التجارية في الإمارات والخليج والشرق الأوسط.",
        },
        "h1": {
            "en": ("CGI and 3D product ads", "that stop the scroll."),
            "ar": ("إعلانات منتجات CGI وثلاثية الأبعاد", "تلفت الانتباه من أول نظرة."),
        },
        "intro": {
            "en": "3D product animations and CGI scenes that show your product at its best on screen. They work for launches, social ads and online store pages where a normal photo or video is not enough.",
            "ar": "رسوم متحركة ثلاثية الأبعاد لمنتجك ومشاهد CGI تُظهره بأفضل شكل على الشاشة. مناسبة للإطلاقات وإعلانات السوشيال وصفحات المتاجر الإلكترونية حين لا تكفي الصورة أو الفيديو العاديان.",
        },
        "gets": {
            "en": [
                "3D product animations",
                "CGI scenes built around your product",
                "Ad-ready videos for social media and paid campaigns",
                "Visual style that follows your brand and references",
            ],
            "ar": [
                "رسوم متحركة ثلاثية الأبعاد لمنتجك",
                "مشاهد CGI مبنية حول منتجك",
                "فيديوهات جاهزة للإعلان على السوشيال والحملات المدفوعة",
                "أسلوب بصري يتبع علامتك ومراجعك",
            ],
        },
        "good_for": {
            "en": [
                "Product launches",
                "Premium and luxury products",
                "Social and paid ads that need to stand out",
            ],
            "ar": [
                "إطلاق المنتجات",
                "المنتجات الفاخرة والراقية",
                "إعلانات السوشيال والإعلانات المدفوعة التي تحتاج أن تتميز",
            ],
        },
        "faq": [
            {
                "q": {"en": "How is CGI different from AI product visuals?", "ar": "ما الفرق بين CGI وصور المنتجات بالذكاء الاصطناعي؟"},
                "a": {
                    "en": "AI product visuals are product photos and campaign visuals created with AI. CGI and 3D ads are 3D product animations and scenes, which take more production work and start from a higher price.",
                    "ar": "صور المنتجات بالذكاء الاصطناعي هي صور وتصاميم حملات تُنشأ بالذكاء الاصطناعي. أما إعلانات CGI والثلاثية الأبعاد فهي رسوم متحركة ومشاهد ثلاثية الأبعاد لمنتجك، وتحتاج عملاً إنتاجياً أكبر وتبدأ من سعر أعلى.",
                },
            },
        ],
        "related": ["ai-product-visuals", "ai-video-ads"],
    },
    {
        "slug": "ai-chatbots-whatsapp-agents",
        "match": "AI Chatbots & WhatsApp Agents",
        "title": {
            "en": "AI Chatbots & WhatsApp Agents for Business",
            "ar": "شات بوت ووكلاء واتساب بالذكاء الاصطناعي للأعمال",
        },
        "description": {
            "en": "AI chatbots and WhatsApp agents that answer customers, capture leads and book appointments 24/7, from AED 1,499. Built by H.M Media for businesses in the UAE, GCC and the Middle East.",
            "ar": "شات بوت ووكلاء واتساب بالذكاء الاصطناعي يردّون على العملاء ويجمعون العملاء المحتملين ويحجزون المواعيد على مدار الساعة، تبدأ من 1,499 درهم. تبنيها H.M Media للشركات في الإمارات والخليج والشرق الأوسط.",
        },
        "h1": {
            "en": ("AI chatbots and WhatsApp agents", "that work 24/7."),
            "ar": ("شات بوت ووكلاء واتساب بالذكاء الاصطناعي", "يعملون على مدار الساعة."),
        },
        "intro": {
            "en": "An assistant that answers customer questions, captures leads and books appointments around the clock, as a chatbot or a WhatsApp agent. Tell us the problem you want to solve and we design the assistant around it, with a clear timeline and quote.",
            "ar": "مساعد يرد على أسئلة العملاء ويجمع العملاء المحتملين ويحجز المواعيد على مدار الساعة، كشات بوت أو كوكيل واتساب. أخبرنا بالمشكلة التي تريد حلها ونصمم المساعد حولها، مع جدول زمني وعرض سعر واضحين.",
        },
        "gets": {
            "en": [
                "A chatbot or WhatsApp agent that answers your customers",
                "Lead capture, so enquiries are not lost",
                "Appointment booking",
                "A clear timeline and quote before we start",
            ],
            "ar": [
                "شات بوت أو وكيل واتساب يرد على عملائك",
                "جمع بيانات العملاء المحتملين حتى لا تضيع أي استفسارات",
                "حجز المواعيد",
                "جدول زمني وعرض سعر واضحان قبل البدء",
            ],
        },
        "good_for": {
            "en": [
                "Businesses that take bookings or visits",
                "Shops and services that answer the same questions every day",
                "Teams that lose leads outside working hours",
            ],
            "ar": [
                "الأعمال التي تستقبل حجوزات أو زيارات",
                "المتاجر والخدمات التي تجيب عن الأسئلة نفسها كل يوم",
                "الفرق التي تخسر عملاء محتملين خارج ساعات العمل",
            ],
        },
        "faq": [
            {
                "q": {"en": "Can you build a custom chatbot for my business?", "ar": "هل يمكنكم بناء شات بوت مخصص لعملي؟"},
                "a": {
                    "en": "Yes. Tell us the problem you want to solve, such as answering customers, taking bookings or capturing leads, and we propose the right solution with a clear timeline and quote.",
                    "ar": "نعم. أخبرنا بالمشكلة التي تريد حلها، مثل الرد على العملاء أو أخذ الحجوزات أو جمع العملاء المحتملين، ونقترح الحل المناسب مع جدول زمني وعرض سعر واضحين.",
                },
            },
            {
                "q": {"en": "Does it work on WhatsApp?", "ar": "هل يعمل على واتساب؟"},
                "a": {
                    "en": "Yes. We build WhatsApp agents that answer customers, capture leads and book appointments.",
                    "ar": "نعم. نبني وكلاء واتساب يردّون على العملاء ويجمعون العملاء المحتملين ويحجزون المواعيد.",
                },
            },
        ],
        "related": ["ai-automation", "ai-apps-smart-websites"],
    },
    {
        "slug": "ai-apps-smart-websites",
        "match": "AI Apps & Smart Websites",
        "title": {
            "en": "Custom AI Apps & Smart Websites",
            "ar": "تطبيقات ومواقع ذكية بالذكاء الاصطناعي حسب الطلب",
        },
        "description": {
            "en": "Custom AI tools, web apps and websites with AI built in, from AED 3,999. H.M Media designs and builds them for businesses across the UAE, GCC and the Middle East.",
            "ar": "أدوات وتطبيقات ويب ومواقع بالذكاء الاصطناعي حسب الطلب، تبدأ من 3,999 درهم. تصممها وتبنيها H.M Media للشركات في الإمارات والخليج والشرق الأوسط.",
        },
        "h1": {
            "en": ("Custom AI apps and smart websites", "built for your business."),
            "ar": ("تطبيقات ومواقع ذكية بالذكاء الاصطناعي", "مبنية لعملك."),
        },
        "intro": {
            "en": "Custom AI tools, web apps and websites with AI built in. We start from the problem you want to solve, for example a web app that writes product descriptions in Arabic and English, and propose the right solution with a clear timeline and quote.",
            "ar": "أدوات وتطبيقات ويب ومواقع بالذكاء الاصطناعي حسب الطلب. نبدأ من المشكلة التي تريد حلها، مثل تطبيق ويب يكتب أوصاف المنتجات بالعربية والإنجليزية، ونقترح الحل المناسب مع جدول زمني وعرض سعر واضحين.",
        },
        "gets": {
            "en": [
                "Custom AI tools and web apps",
                "Websites with AI built in",
                "A clear scope, timeline and quote before work starts",
            ],
            "ar": [
                "أدوات وتطبيقات ويب مخصصة بالذكاء الاصطناعي",
                "مواقع بذكاء اصطناعي مدمج",
                "نطاق عمل وجدول زمني وعرض سعر واضحة قبل بدء العمل",
            ],
        },
        "good_for": {
            "en": [
                "Businesses with repetitive writing or support work",
                "Brands that need a website and an AI feature together",
                "Teams that want a tool built around their own process",
            ],
            "ar": [
                "الأعمال التي فيها كتابة أو دعم متكرر",
                "العلامات التي تحتاج موقعاً وميزة ذكاء اصطناعي معاً",
                "الفرق التي تريد أداة مبنية حول طريقة عملها",
            ],
        },
        "faq": [
            {
                "q": {"en": "What kind of AI app can you build?", "ar": "ما نوع تطبيقات الذكاء الاصطناعي التي يمكنكم بناؤها؟"},
                "a": {
                    "en": "Custom AI tools, web apps and websites with AI built in. Tell us the problem you want to solve, such as answering customers, taking bookings or writing content, and we propose the right solution.",
                    "ar": "أدوات وتطبيقات ويب ومواقع بالذكاء الاصطناعي حسب الطلب. أخبرنا بالمشكلة التي تريد حلها، مثل الرد على العملاء أو أخذ الحجوزات أو كتابة المحتوى، ونقترح الحل المناسب.",
                },
            },
            {
                "q": {"en": "I only need a regular website. Do you do that?", "ar": "أحتاج موقعاً عادياً فقط. هل تقدمون ذلك؟"},
                "a": {
                    "en": "Yes. Websites, landing pages and online stores are listed under Web & E-commerce.",
                    "ar": "نعم. المواقع وصفحات الهبوط والمتاجر الإلكترونية موجودة ضمن مواقع ومتاجر.",
                },
            },
        ],
        "related": ["ai-chatbots-whatsapp-agents", "ai-automation"],
    },
    {
        "slug": "ai-automation",
        "match": "AI Automation",
        "title": {
            "en": "AI Automation for Business Workflows",
            "ar": "أتمتة بالذكاء الاصطناعي لسير العمل في شركتك",
        },
        "description": {
            "en": "AI automation that connects your tools so leads, bookings and content run on autopilot, from AED 999. H.M Media serves businesses across the UAE, GCC and the Middle East.",
            "ar": "أتمتة بالذكاء الاصطناعي تربط أدواتك ليعمل العملاء المحتملون والحجوزات والمحتوى تلقائياً، تبدأ من 999 درهم. تخدم H.M Media الشركات في الإمارات والخليج والشرق الأوسط.",
        },
        "h1": {
            "en": ("AI automation that runs your", "leads, bookings and content."),
            "ar": ("أتمتة بالذكاء الاصطناعي تدير", "عملاءك وحجوزاتك ومحتواك."),
        },
        "intro": {
            "en": "We connect your tools so repetitive work runs on autopilot: new leads, bookings and content. A typical example is sending every new lead from Instagram to WhatsApp and your CRM automatically.",
            "ar": "نربط أدواتك ليعمل العمل المتكرر تلقائياً: العملاء المحتملون الجدد والحجوزات والمحتوى. مثال شائع: إرسال كل عميل جديد من إنستغرام إلى واتساب ونظام إدارة العملاء تلقائياً.",
        },
        "gets": {
            "en": [
                "Your tools connected into one workflow",
                "Leads, bookings and content handled automatically",
                "A clear scope and price before we start",
            ],
            "ar": [
                "أدواتك مربوطة في سير عمل واحد",
                "العملاء المحتملون والحجوزات والمحتوى تُدار تلقائياً",
                "نطاق عمل وسعر واضحان قبل البدء",
            ],
        },
        "good_for": {
            "en": [
                "Businesses that manage leads by hand",
                "Teams that publish content on a schedule",
                "Anyone copying data between apps every day",
            ],
            "ar": [
                "الأعمال التي تدير العملاء المحتملين يدوياً",
                "الفرق التي تنشر المحتوى بجدول منتظم",
                "كل من ينسخ البيانات بين التطبيقات يومياً",
            ],
        },
        "faq": [
            {
                "q": {"en": "What can be automated?", "ar": "ما الذي يمكن أتمتته؟"},
                "a": {
                    "en": "Leads, bookings and content, for example sending every new lead from Instagram to WhatsApp and your CRM. Tell us the task you repeat most and we propose a workflow.",
                    "ar": "العملاء المحتملون والحجوزات والمحتوى، مثل إرسال كل عميل جديد من إنستغرام إلى واتساب ونظام إدارة العملاء. أخبرنا بالمهمة التي تكررها أكثر ونقترح عليك سير عمل.",
                },
            },
        ],
        "related": ["ai-chatbots-whatsapp-agents", "ai-apps-smart-websites"],
    },
]

# --------------------------------------------------------------------------- agency category pages
# `match` is the English group heading on the home page (agency-h). The services listed on each page
# are read from index.html.
GROUP_PAGES = [
    {
        "slug": "design",
        "match": "Design",
        "label": {"en": "Design", "ar": "تصميم"},
        "title": {"en": "Design Services: Social, Logo, Presentation & Print", "ar": "خدمات التصميم: سوشيال وشعارات وعروض ومطبوعات"},
        "description": {
            "en": "Social media designs, logo and brand look, presentations and company profiles, print and event designs, from AED 199. H.M Media serves brands across the UAE, GCC and the Middle East.",
            "ar": "تصاميم سوشيال ميديا وشعار ومظهر للعلامة وعروض تقديمية وبروفايل شركة وتصاميم مطبوعات وفعاليات، تبدأ من 199 درهم. تخدم H.M Media العلامات التجارية في الإمارات والخليج والشرق الأوسط.",
        },
        "h1": {"en": ("Design services", "for brands in the UAE and GCC."), "ar": ("خدمات التصميم", "للعلامات التجارية في الإمارات والخليج.")},
        "intro": {
            "en": "Social media designs, logo and brand look, presentations and company profiles, and print and event designs. Each service below has a clear starting price, and you get an exact quote before work starts.",
            "ar": "تصاميم سوشيال ميديا وشعار ومظهر للعلامة وعروض تقديمية وبروفايل شركة وتصاميم مطبوعات وفعاليات. لكل خدمة أدناه سعر بداية واضح، وتحصل على عرض سعر دقيق قبل بدء العمل.",
        },
        "faq_extra": ["Can I request a one-time project instead of a monthly package?"],
        "related": ["video-and-motion", "marketing-and-growth", "ai-product-visuals"],
    },
    {
        "slug": "video-and-motion",
        "match": "Video & Motion",
        "label": {"en": "Video & Motion", "ar": "فيديو وموشن"},
        "title": {"en": "Video Production & Motion Graphics", "ar": "إنتاج فيديو وموشن جرافيك"},
        "description": {
            "en": "Reels and short videos, explainer videos, logo animation, ad video scripts and photo and video shoot days, from AED 299. H.M Media serves brands across the UAE, GCC and the Middle East.",
            "ar": "ريلز وفيديوهات قصيرة وفيديوهات شرح وتحريك شعار وسيناريو إعلان وأيام تصوير فوتو وفيديو، تبدأ من 299 درهم. تخدم H.M Media العلامات التجارية في الإمارات والخليج والشرق الأوسط.",
        },
        "h1": {"en": ("Video production and motion graphics", "for brands in the UAE and GCC."), "ar": ("إنتاج فيديو وموشن جرافيك", "للعلامات التجارية في الإمارات والخليج.")},
        "intro": {
            "en": "Reels and short videos, explainer videos, logo animation, ad video scripts and photo and video shoot days. Each service below has a clear starting price, and you get an exact quote before work starts.",
            "ar": "ريلز وفيديوهات قصيرة وفيديوهات شرح وتحريك شعار وسيناريو إعلان وأيام تصوير فوتو وفيديو. لكل خدمة أدناه سعر بداية واضح، وتحصل على عرض سعر دقيق قبل بدء العمل.",
        },
        "faq_extra": ["How fast can you deliver a project?"],
        "related": ["ai-video-ads", "cgi-3d-product-ads", "design"],
    },
    {
        "slug": "marketing-and-growth",
        "match": "Marketing & Growth",
        "label": {"en": "Marketing & Growth", "ar": "تسويق ونمو"},
        "title": {"en": "Social Media Management, Ads & Local SEO", "ar": "إدارة السوشيال ميديا والإعلانات والسيو المحلي"},
        "description": {
            "en": "Monthly social media management, sponsored ads, Google Business and local SEO, Arabic and English copywriting, and social media audits, from AED 299. H.M Media serves brands across the UAE, GCC and the Middle East.",
            "ar": "إدارة شهرية للسوشيال ميديا وإعلانات ممولة وملف نشاط جوجل وسيو محلي وكتابة محتوى بالعربية والإنجليزية وتدقيق للحسابات، تبدأ من 299 درهم. تخدم H.M Media العلامات التجارية في الإمارات والخليج والشرق الأوسط.",
        },
        "h1": {"en": ("Marketing and growth", "for brands in the UAE and GCC."), "ar": ("التسويق والنمو", "للعلامات التجارية في الإمارات والخليج.")},
        "intro": {
            "en": "Monthly social media, sponsored ads, Google Business and local SEO, Arabic and English copywriting, and social media audits with a strategy. Each service below has a clear starting price, and you get an exact quote before work starts.",
            "ar": "إدارة شهرية للسوشيال ميديا وإعلانات ممولة وملف نشاط جوجل وسيو محلي وكتابة محتوى بالعربية والإنجليزية وتدقيق للحسابات مع استراتيجية. لكل خدمة أدناه سعر بداية واضح، وتحصل على عرض سعر دقيق قبل بدء العمل.",
        },
        "faq_extra": ["Can I request a one-time project instead of a monthly package?"],
        "related": ["design", "video-and-motion", "ai-automation"],
    },
    {
        "slug": "web-and-ecommerce",
        "match": "Web & E-commerce",
        "label": {"en": "Web & E-commerce", "ar": "مواقع ومتاجر"},
        "title": {"en": "Website, Landing Page & Online Store Setup", "ar": "تصميم المواقع وصفحات الهبوط وإعداد المتاجر الإلكترونية"},
        "description": {
            "en": "Websites, landing pages and online store setup, from AED 2,999. H.M Media builds them for brands across the UAE, GCC and the Middle East.",
            "ar": "مواقع وصفحات هبوط وإعداد متاجر إلكترونية، تبدأ من 2,999 درهم. تبنيها H.M Media للعلامات التجارية في الإمارات والخليج والشرق الأوسط.",
        },
        "h1": {"en": ("Websites and online stores", "for brands in the UAE and GCC."), "ar": ("مواقع ومتاجر إلكترونية", "للعلامات التجارية في الإمارات والخليج.")},
        "intro": {
            "en": "Websites, landing pages and online store setup. Want AI built into your site, such as a chatbot or a custom tool? See AI Apps & Smart Websites. Each service below has a clear starting price.",
            "ar": "مواقع وصفحات هبوط وإعداد متاجر إلكترونية. تريد ذكاءً اصطناعياً مدمجاً في موقعك، مثل شات بوت أو أداة مخصصة؟ راجع تطبيقات ومواقع ذكية. لكل خدمة أدناه سعر بداية واضح.",
        },
        "faq_extra": ["What do you need from me before starting?"],
        "related": ["ai-apps-smart-websites", "ai-chatbots-whatsapp-agents", "design"],
    },
]

# FAQ questions from the home page that every service page repeats (answers are read from index.html).
SHARED_FAQ = ["Are your prices fixed?", "What do you need from me before starting?", "Do you work with clients outside the UAE?"]

# --------------------------------------------------------------------------- interface strings
UI = {
    "en": {
        "dir": "ltr",
        "services": "Services",
        "home_label": "H.M Media",
        "nav": [("#ai", "AI Services"), ("#agency", "Agency"), ("#process", "Process"), ("#faq", "FAQ"), ("#contact", "Contact")],
        "start": "Start a project",
        "menu": "Open menu",
        "language": "Language",
        "breadcrumb": "Breadcrumb",
        "crumb_ai": "AI services",
        "crumb_agency": "Agency services",
        "eyebrow_ai": "AI services",
        "eyebrow_agency": "Agency services",
        "starting_from": "Starting from",
        "request": "Request on WhatsApp",
        "gets": "What you get",
        "good_for": "Good for",
        "included": "Included services",
        "how": "How it works",
        "how_h": ("Three simple", "steps."),
        "steps": [
            ("Tell us what you need", "Send a message on WhatsApp or use the form — a few lines are enough."),
            ("We build it with AI + human craft", "We agree on scope, price, and timeline, then create and refine with you."),
            ("You launch", "Get final files or a working solution, ready for your platforms."),
        ],
        "faq_h": ("Common", "questions."),
        "related": "Related services",
        "talk_h": ("Ready to start?", "Just talk to us."),
        "talk_lead": "Tell us your idea in one message — we'll suggest the right solution and price.",
        "talk_btn": "Talk to us directly",
        "talk_small": "We reply within 24 hours",
        "wa_msg": "Hi Hussein, I'm interested in: {title}{price}.\nSelected from: {source}.\nPlease share the next step and an exact quote.",
        "wa_msg_group": "Hi Hussein, I'm interested in: {title}.\nSelected from: {source}.\nPlease share the next step and an exact quote.",
        "wa_talk": "Hi Hussein 👋\nI'd like to talk to you directly.\nSelected from: {source}.\nHere's what I need:",
        "footer_tag": ("Where creativity", "meets technology."),
        "footer_loc": "Based in the UAE · Serving brands across the GCC, the Middle East and worldwide",
        "footer_services": "Services",
        "footer_contact": "Contact",
        "whatsapp": "WhatsApp",
        "email": "Email",
        "rights": "H.M Media. All rights reserved.",
        "founder": "Founded by Hussein Mlhem",
        "back_top": "Back to top ↑",
        "page_word": "page",
        "view_all": "All services",
    },
    "ar": {
        "dir": "rtl",
        "services": "الخدمات",
        "home_label": "H.M Media",
        "nav": [("#ai", "خدمات الذكاء الاصطناعي"), ("#agency", "خدمات الوكالة"), ("#process", "طريقة العمل"), ("#faq", "الأسئلة"), ("#contact", "تواصل معنا")],
        "start": "ابدأ مشروعك",
        "menu": "فتح القائمة",
        "language": "اللغة",
        "breadcrumb": "مسار التنقل",
        "crumb_ai": "خدمات الذكاء الاصطناعي",
        "crumb_agency": "خدمات الوكالة",
        "eyebrow_ai": "خدمات الذكاء الاصطناعي",
        "eyebrow_agency": "خدمات الوكالة",
        "starting_from": "يبدأ من",
        "request": "اطلب عبر واتساب",
        "gets": "ما تحصل عليه",
        "good_for": "لمن تناسب؟",
        "included": "الخدمات المتضمنة",
        "how": "كيف نعمل",
        "how_h": ("ثلاث خطوات", "بسيطة."),
        "steps": [
            ("أخبرنا بما تحتاجه", "أرسل رسالة على واتساب أو استخدم النموذج — بضعة أسطر تكفي."),
            ("ننفذ بالذكاء الاصطناعي ولمسة بشرية", "نتفق على المطلوب والسعر والمدة، ثم ننفذ ونعدّل معك."),
            ("تطلق مشروعك", "تستلم الملفات النهائية أو حلاً جاهزاً للعمل على منصاتك."),
        ],
        "faq_h": ("أسئلة", "شائعة."),
        "related": "خدمات ذات صلة",
        "talk_h": ("جاهز للبدء؟", "تحدث معنا مباشرة."),
        "talk_lead": "أخبرنا بفكرتك في رسالة واحدة — وسنقترح عليك الحل والسعر المناسبين.",
        "talk_btn": "تحدث معنا مباشرة",
        "talk_small": "نرد خلال 24 ساعة",
        "wa_msg": "مرحباً حسين، أنا مهتم بـ: {title}{price}.\nالاختيار: {source}.\nأرجو إرسال الخطوة التالية وعرض سعر دقيق.",
        "wa_msg_group": "مرحباً حسين، أنا مهتم بـ: {title}.\nالاختيار: {source}.\nأرجو إرسال الخطوة التالية وعرض سعر دقيق.",
        "wa_talk": "مرحباً حسين 👋\nأريد التحدث معك مباشرة.\nالاختيار: {source}.\nهذا ما أحتاجه:",
        "footer_tag": ("حيث يلتقي الإبداع", "بالتكنولوجيا."),
        "footer_loc": "مقرّنا الإمارات · نخدم العلامات التجارية في الخليج والشرق الأوسط والعالم",
        "footer_services": "الخدمات",
        "footer_contact": "تواصل",
        "whatsapp": "واتساب",
        "email": "البريد الإلكتروني",
        "rights": "H.M Media. جميع الحقوق محفوظة.",
        "founder": "أسّسها حسين ملحم",
        "back_top": "العودة للأعلى ↑",
        "page_word": "صفحة",
        "view_all": "كل الخدمات",
    },
}
