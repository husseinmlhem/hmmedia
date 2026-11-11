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
        "nav": [("#services", "Services"), ("work/", "Portfolio"), ("#faq", "FAQ"), ("#contact", "Contact"), ("one/", "H.M One")],
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
            ("Tell us what you need", "A WhatsApp message is enough."),
            ("We build it with AI + human craft", "We agree on scope, price and timeline, then build."),
            ("You launch", "Final files or a working solution."),
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
        "footer_explore": "Explore",
        "footer_follow": "Follow",
        "footer_faq": "FAQ",
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
        "nav": [("#services", "الخدمات"), ("work/", "أعمالنا"), ("#faq", "الأسئلة"), ("#contact", "تواصل معنا"), ("one/", "H.M One")],
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
            ("أخبرنا بما تحتاجه", "رسالة واتساب تكفي."),
            ("ننفذ بالذكاء الاصطناعي ولمسة بشرية", "نتفق على النطاق والسعر والمدة، ثم ننفذ."),
            ("تطلق مشروعك", "ملفات نهائية أو حل جاهز للعمل."),
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
        "footer_explore": "استكشف",
        "footer_follow": "تابعنا",
        "footer_faq": "الأسئلة الشائعة",
        "whatsapp": "واتساب",
        "email": "البريد الإلكتروني",
        "rights": "H.M Media. جميع الحقوق محفوظة.",
        "founder": "أسّسها حسين ملحم",
        "back_top": "العودة للأعلى ↑",
        "page_word": "صفحة",
        "view_all": "كل الخدمات",
    },
}

# --------------------------------------------------------------------------- About page
# Facts only: everything here is already stated on the home page or the founder's CV. Do not add a founding
# year, team size, client numbers or results unless they are true and the owner has supplied them.
ABOUT = {
    "en": {
        "nav": "About",
        "title": "About H.M Media | AI Creative Studio",
        "description": "H.M Media is an AI creative studio and creative agency for brands in the UAE, GCC and the Middle East, working remotely worldwide in Arabic and English. Founded by Hussein Mlhem.",
        "label": "About",
        "h1": ("About H.M Media,", "an AI creative studio."),
        "intro": "H.M Media is an AI creative studio and creative agency. We build AI product visuals, AI video ads, chatbots, apps and automation, and we also do the classic agency work: design, video, marketing and websites. We are based in the UAE and work with brands across the GCC, the Middle East and worldwide, in Arabic and English.",
        "ai_h": "AI services",
        "agency_h": "Agency services",
        "where_h": "Where we work",
        "where": "We are based in the UAE and work with clients across the UAE, the GCC and internationally. Most projects are handled remotely through clear briefs, shared files and regular communication. We work in Arabic and English.",
        "founder_h": "Founder",
        "founder": "H.M Media was founded by Hussein Mlhem, a Multimedia Lead and Creative Technologist with 9+ years of experience across video, motion design, design and software engineering, and a bachelor's degree in software engineering.",
        "founder_link": "Hussein's profile and CV",
        "contact_h": "Contact",
        "reply": "We reply within 24 hours.",
        "phone": "WhatsApp / phone",
        "email": "Email",
        "socials": "Instagram · Facebook",
        "source": "About page",
    },
    "ar": {
        "nav": "من نحن",
        "title": "من نحن | H.M Media استوديو إبداعي بالذكاء الاصطناعي",
        "description": "H.M Media استوديو إبداعي ووكالة إبداعية بالذكاء الاصطناعي للعلامات التجارية في الإمارات والخليج والشرق الأوسط، وتعمل عن بعد مع العالم بالعربية والإنجليزية. أسّسها حسين ملحم.",
        "label": "من نحن",
        "h1": ("عن H.M Media،", "استوديو إبداعي بالذكاء الاصطناعي."),
        "intro": "H.M Media استوديو إبداعي ووكالة إبداعية. ننفّذ صور المنتجات وإعلانات الفيديو بالذكاء الاصطناعي والشات بوت والتطبيقات والأتمتة، ونقدّم أيضاً خدمات الوكالة التقليدية: التصميم والفيديو والتسويق والمواقع. مقرّنا الإمارات ونعمل مع العلامات التجارية في الخليج والشرق الأوسط والعالم، بالعربية والإنجليزية.",
        "ai_h": "خدمات الذكاء الاصطناعي",
        "agency_h": "خدمات الوكالة",
        "where_h": "أين نعمل",
        "where": "مقرّنا الإمارات ونعمل مع عملاء داخل الإمارات والخليج وخارج المنطقة. أغلب المشاريع تُنفَّذ عن بعد عبر موجز واضح وملفات مشتركة وتواصل منتظم. نعمل بالعربية والإنجليزية.",
        "founder_h": "المؤسس",
        "founder": "أسّس H.M Media حسين ملحم، قائد وسائط متعددة وتقني إبداعي (Multimedia Lead & Creative Technologist) بخبرة تتجاوز 9 سنوات في الفيديو والموشن ديزاين والتصميم وهندسة البرمجيات، وبكالوريوس في هندسة البرمجيات.",
        "founder_link": "الملف الشخصي والسيرة الذاتية لحسين",
        "contact_h": "تواصل",
        "reply": "نرد خلال 24 ساعة.",
        "phone": "واتساب / هاتف",
        "email": "البريد الإلكتروني",
        "socials": "إنستغرام · فيسبوك · يوتيوب",
        "source": "صفحة من نحن",
    },
}

# --------------------------------------------------------------------------- H.M One (business software)
# The platform's sign-in address. Leave as None until the platform is live: the "Log in" button and the
# login link in the structured data are only published when this is set.
ONE_APP_URL = None

# Solutions that are available in the platform today. Descriptions state what exists and nothing more.
ONE_SOLUTIONS = [
    {"icon": "hr", "tags": {"en": "Records · Org chart · Contracts", "ar": "السجلات · الهيكل التنظيمي · العقود"}, "en": ("HR Management", "Employee records, interactive organization chart, contracts, documents, requests, loans, onboarding and offboarding, and end-of-service estimates."),
     "ar": ("إدارة الموارد البشرية", "سجلات الموظفين، مخطط تنظيمي تفاعلي، العقود والوثائق والطلبات والقروض، إجراءات التعيين وإنهاء الخدمة، وتقدير مستحقات نهاية الخدمة.")},
    {"icon": "attendance", "tags": {"en": "Schedules · Leave · Approvals", "ar": "الجداول · الإجازات · الموافقات"}, "en": ("Attendance & Leave", "Attendance records and schedules, leave requests with approvals, spreadsheet import and reports."),
     "ar": ("الحضور والإجازات", "سجلات وجداول الحضور، طلبات الإجازات مع الموافقات، استيراد من جداول البيانات والتقارير.")},
    {"icon": "payroll", "tags": {"en": "Cycles · Payslips · Deductions", "ar": "الدورات · القسائم · الاستقطاعات"}, "en": ("Payroll", "Payroll cycles, payslips, allowances, deductions and loans, with approvals."),
     "ar": ("الرواتب", "دورات الرواتب وقسائمها، البدلات والاستقطاعات والقروض، مع الموافقات.")},
    {"icon": "facility", "tags": {"en": "Properties · Work orders · Technicians", "ar": "العقارات · أوامر العمل · الفنيون"}, "en": ("Facility Management", "Clients, properties and units, work orders, technician assignment, time and cost logs, with basic invoicing and collection."),
     "ar": ("إدارة المرافق", "العملاء والعقارات والوحدات، أوامر العمل وإسنادها للفنيين، سجل الوقت والتكلفة، مع فوترة وتحصيل أساسيين.")},
    {"icon": "assets", "tags": {"en": "Register · Custody · Tags", "ar": "السجل · العهدة · الوسوم"}, "en": ("Asset Management", "Asset register with tags, locations, employee custody, assignment and return, documents, linked to work orders."),
     "ar": ("إدارة الأصول", "سجل الأصول مع الوسوم والمواقع وعهدة الموظفين، الإسناد والإرجاع والمستندات، مرتبط بأوامر العمل.")},
    {"icon": "maintenance", "tags": {"en": "Plans · Auto work orders · Checklists", "ar": "الخطط · أوامر عمل تلقائية · قوائم الفحص"}, "en": ("Preventive Maintenance", "Recurring maintenance plans with due dates, automatic work orders and checklists."),
     "ar": ("الصيانة الوقائية", "خطط صيانة دورية بتواريخ استحقاق، وأوامر عمل تلقائية وقوائم فحص.")},
    {"icon": "procurement", "tags": {"en": "Requests · Quotes · Purchase orders", "ar": "الطلبات · العروض · أوامر الشراء"}, "en": ("Procurement", "Suppliers, purchase requests with approvals, supplier quotes, purchase orders and partial or full receiving."),
     "ar": ("المشتريات", "الموردون، طلبات الشراء مع الموافقات، عروض الموردين، أوامر الشراء والاستلام الجزئي أو الكامل.")},
    {"icon": "inventory", "tags": {"en": "Items · Warehouses · Movements", "ar": "الأصناف · المستودعات · الحركات"}, "en": ("Inventory & Spare Parts", "Items and warehouses with an auditable movement ledger: receive, issue, transfer and adjust."),
     "ar": ("المخزون وقطع الغيار", "الأصناف والمستودعات مع دفتر حركات قابل للتدقيق: استلام وصرف ونقل وتسوية.")},
    {"icon": "finance", "tags": {"en": "VAT invoices · Expenses · Receipts", "ar": "فواتير ضريبية · مصروفات · إيصالات"}, "en": ("Finance & Expenses", "VAT invoices, credit notes, expenses and quotes, payments and receipts, with PDF and Excel export."),
     "ar": ("المالية والمصروفات", "فواتير ضريبية وإشعارات دائنة ومصروفات وعروض أسعار، دفعات وإيصالات، مع تصدير PDF وExcel.")},
]

ONE = {
    "en": {
        "nav": "H.M One",
        "title": "H.M One | Business Software for UAE Companies",
        "description": "H.M One is a business operations platform by H.M Media: HR, attendance, payroll, facility management, assets, maintenance, procurement, inventory and finance. Pick the Solutions you need, or request a custom one.",
        "label": "H.M One",
        "eyebrow": "Business software by H.M Media",
        "h1": ("Your whole company.", "One platform."),
        "tagline": "Private workspace. Arabic and English. Activate only what you need.",
        "pills": [("lock", "Private workspace"), ("puzzle", "Pay per Solution"), ("globe", "Arabic + English"), ("shield", "Roles & approvals")],
        "solutions_hint": "Tap a Solution to request it.",
        "custom_short_h": ("Not on the list?", "We build it."),
        "custom_short": "Internal tools, dashboards, portals and AI features, inside your workspace.",
        "wa_solution": "Hi Hussein, I want this H.M One Solution for my company: {name}.\nSelected from: H.M One page.",
        "intro": "H.M One is our business operations platform for companies in the UAE and the region. Your company gets its own private workspace in Arabic and English, and you activate only the Solutions you need. If what you need does not exist yet, we build it for you.",
        "points_h": "How it is built",
        "points": [
            "A private workspace for each company, isolated from every other company",
            "Buy Solutions individually; no forced bundles",
            "One shared record for employees, clients and suppliers across all Solutions",
            "Roles and permissions for every user, with approvals built in",
            "Arabic and English, right-to-left and left-to-right",
        ],
        "solutions_h": ("Ready", "Solutions."),
        "solutions_lead": "Available today. Activate one or several; they share the same data.",
        "custom_h": ("Need something", "that is not on the list?"),
        "custom": "We design and build custom Solutions: internal tools, dashboards, portals and AI features. Tell us the problem and we reply with a scope, a timeline and a quote. A custom Solution can run inside your H.M One workspace next to the ready ones.",
        "steps": [
            ("Tell us what you need", "Choose ready Solutions or describe a custom one. A short WhatsApp message is enough."),
            ("We set up your workspace", "We create your company workspace, activate your Solutions and create your administrator account."),
            ("Your team logs in", "Add your users and roles and start working. You can add Solutions later."),
        ],
        "faq": [
            ("How much does H.M One cost?", "It depends on the Solutions you choose and the size of your company. Tell us what you need and you get an exact quote before anything starts."),
            ("Do I have to buy every Solution?", "No. Solutions are bought individually and work on their own. A Solution depends on another one only when the work itself requires it."),
            ("Can you build a Solution that is not listed?", "Yes. We build custom Solutions on request. Tell us the problem you want to solve and we propose a scope, a timeline and a quote."),
            ("Is my company's data separate from other companies?", "Yes. Each company has its own isolated workspace, and users only see what their role allows."),
            ("Does it work in Arabic?", "Yes. The whole platform works in Arabic and English, including right-to-left layout."),
        ],
        "cta_ready": "Request a ready Solution",
        "cta_custom": "Request a custom Solution",
        "cta_login": "Log in",
        "wa_ready": "Hi Hussein, I want a ready H.M One Solution for my company.\nSelected from: H.M One page.\nSolutions I am interested in:",
        "wa_custom": "Hi Hussein, I want a custom Solution built for my company.\nSelected from: H.M One page.\nThe problem I want to solve:",
        "source": "H.M One page",
        "home_h": ("H.M One:", "business software for your company."),
        "home_lead": "HR, payroll, facility management, procurement, inventory and finance on one connected platform. Pick the Solutions you need, or ask us to build a custom one.",
        "home_cta": "Explore H.M One",
    },
    "ar": {
        "nav": "H.M One",
        "title": "H.M One | برمجيات إدارة الأعمال لشركات الإمارات",
        "description": "H.M One منصة لإدارة أعمال الشركات من H.M Media: الموارد البشرية، الحضور، الرواتب، إدارة المرافق، الأصول، الصيانة، المشتريات، المخزون والمالية. اختر الحلول التي تحتاجها أو اطلب حلاً مخصصاً.",
        "label": "H.M One",
        "eyebrow": "برمجيات الأعمال من H.M Media",
        "h1": ("شركتك كلها.", "منصة واحدة."),
        "tagline": "مساحة عمل خاصة. عربي وإنجليزي. فعّل ما تحتاجه فقط.",
        "pills": [("lock", "مساحة عمل خاصة"), ("puzzle", "ادفع لكل حل منفرداً"), ("globe", "عربي + إنجليزي"), ("shield", "أدوار وموافقات")],
        "solutions_hint": "اضغط على أي حل لطلبه.",
        "custom_short_h": ("غير موجود في القائمة؟", "نبنيه لك."),
        "custom_short": "أدوات داخلية، لوحات متابعة، بوابات، ومزايا ذكاء اصطناعي، داخل مساحة شركتك.",
        "wa_solution": "مرحباً حسين، أريد هذا الحل من H.M One لشركتي: {name}.\nالاختيار: صفحة H.M One.",
        "intro": "H.M One منصتنا لإدارة عمليات الشركات في الإمارات والمنطقة. تحصل شركتك على مساحة عمل خاصة بها بالعربية والإنجليزية، وتفعّل فقط الحلول التي تحتاجها. وإذا لم يكن ما تحتاجه موجوداً، نبنيه لك.",
        "points_h": "كيف بُنيت المنصة",
        "points": [
            "مساحة عمل خاصة لكل شركة، معزولة عن بقية الشركات",
            "تشتري الحلول منفردة، بلا حزم إجبارية",
            "سجل واحد مشترك للموظفين والعملاء والموردين بين كل الحلول",
            "أدوار وصلاحيات لكل مستخدم، مع نظام موافقات مدمج",
            "عربي وإنجليزي، من اليمين لليسار ومن اليسار لليمين",
        ],
        "solutions_h": ("حلول", "جاهزة."),
        "solutions_lead": "متاحة اليوم. فعّل حلاً واحداً أو عدة حلول، وكلها تعمل على البيانات نفسها.",
        "custom_h": ("تحتاج شيئاً", "غير موجود في القائمة؟"),
        "custom": "نصمم ونبني حلولاً مخصصة: أدوات داخلية، لوحات متابعة، بوابات، ومزايا بالذكاء الاصطناعي. أخبرنا بالمشكلة ونرد عليك بنطاق العمل والمدة وعرض السعر. ويمكن أن يعمل الحل المخصص داخل مساحة شركتك في H.M One بجانب الحلول الجاهزة.",
        "steps": [
            ("أخبرنا بما تحتاجه", "اختر حلولاً جاهزة أو صف حلاً مخصصاً. رسالة قصيرة على واتساب تكفي."),
            ("نجهّز مساحة شركتك", "ننشئ مساحة العمل الخاصة بشركتك، ونفعّل حلولك، وننشئ حساب المسؤول."),
            ("فريقك يسجّل الدخول", "أضف المستخدمين والأدوار وابدأ العمل. ويمكنك إضافة حلول لاحقاً."),
        ],
        "faq": [
            ("كم تكلفة H.M One؟", "تعتمد على الحلول التي تختارها وحجم شركتك. أخبرنا بما تحتاجه وتحصل على عرض سعر دقيق قبل أي بدء."),
            ("هل يجب أن أشتري كل الحلول؟", "لا. تُشترى الحلول منفردة وتعمل كل منها بمفردها. لا يعتمد حل على آخر إلا إذا كان العمل نفسه يتطلب ذلك."),
            ("هل تبنون حلاً غير موجود في القائمة؟", "نعم. نبني حلولاً مخصصة عند الطلب. أخبرنا بالمشكلة التي تريد حلها ونقترح نطاق العمل والمدة وعرض السعر."),
            ("هل بيانات شركتي منفصلة عن بقية الشركات؟", "نعم. لكل شركة مساحة عمل معزولة، ولا يرى المستخدم إلا ما يسمح به دوره."),
            ("هل تعمل بالعربية؟", "نعم. تعمل المنصة كاملة بالعربية والإنجليزية، مع دعم الكتابة من اليمين إلى اليسار."),
        ],
        "cta_ready": "اطلب حلاً جاهزاً",
        "cta_custom": "اطلب حلاً مخصصاً",
        "cta_login": "تسجيل الدخول",
        "wa_ready": "مرحباً حسين، أريد حلاً جاهزاً من H.M One لشركتي.\nالاختيار: صفحة H.M One.\nالحلول التي تهمني:",
        "wa_custom": "مرحباً حسين، أريد بناء حل مخصص لشركتي.\nالاختيار: صفحة H.M One.\nالمشكلة التي أريد حلها:",
        "source": "صفحة H.M One",
        "home_h": ("H.M One:", "برمجيات لإدارة شركتك."),
        "home_lead": "الموارد البشرية والرواتب وإدارة المرافق والمشتريات والمخزون والمالية في منصة واحدة مترابطة. اختر الحلول التي تحتاجها، أو اطلب منا بناء حل مخصص.",
        "home_cta": "تعرّف على H.M One",
    },
}

# --------------------------------------------------------------------------- Work (portfolio)
# Fields we have delivered work in. The portfolio page shows a sample; each field opens a WhatsApp request.
WORK_FIELDS = [
    ("Real estate", "العقارات"),
    ("Retail", "التجزئة"),
    ("Healthcare", "الرعاية الصحية"),
    ("Beauty & perfume", "التجميل والعطور"),
    ("Food & beverage", "الأغذية والمشروبات"),
    ("Technology", "التقنية"),
    ("Events", "الفعاليات"),
    ("Sports", "الرياضة"),
    ("Mobile apps", "تطبيقات الجوال"),
    ("Gaming", "الألعاب"),
]

WORK = {
    "en": {
        "nav": "Portfolio",
        "title": "Our Portfolio | H.M Media",
        "description": "The H.M Media portfolio: a sample from 500+ projects in design, product visuals, video and motion graphics. Tell us your field and we send the work that fits.",
        "label": "Portfolio",
        "h1": ("Our", "Portfolio."),
        "intro": "500+ projects. This is a small sample.",
        "looking": "Looking for",
        "cta": "Request work in your field",
        "fields_label": "Fields we work in",
        "more_fields": "and more",
        "wa_all": "Hi Hussein, I'd like to see your portfolio.\nSelected from: Portfolio page.\nMy field:",
        "wa_field": "Hi Hussein, please send me your work in: {field}.\nSelected from: Portfolio page.",
        "wall_label": "Samples of our work",
        "design_alt": "H.M Media design work, sample {n}",
        "video_label": "Video sample {n}",
        "source": "Portfolio page",
    },
    "ar": {
        "nav": "أعمالنا",
        "title": "أعمالنا | H.M Media",
        "description": "أعمال H.M Media: عيّنة من أكثر من 500 مشروع في التصميم وصور المنتجات والفيديو والموشن جرافيك. أخبرنا بمجالك ونرسل لك الأعمال المناسبة.",
        "label": "أعمالنا",
        "h1": ("معرض", "أعمالنا."),
        "intro": "أكثر من 500 مشروع. وهذه عيّنة صغيرة.",
        "looking": "تبحث عن",
        "cta": "اطلب أعمالاً في مجالك",
        "fields_label": "مجالات نعمل فيها",
        "more_fields": "وغيرها",
        "wa_all": "مرحباً حسين، أريد الاطلاع على معرض أعمالكم.\nالاختيار: صفحة أعمالنا.\nمجالي:",
        "wa_field": "مرحباً حسين، أرجو إرسال أعمالكم في مجال: {field}.\nالاختيار: صفحة أعمالنا.",
        "wall_label": "نماذج من أعمالنا",
        "design_alt": "من أعمال التصميم لدى H.M Media، نموذج {n}",
        "video_label": "نموذج فيديو {n}",
        "source": "صفحة أعمالنا",
    },
}
