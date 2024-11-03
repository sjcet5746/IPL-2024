import streamlit as st
from datetime import datetime

# Streamlit app
st.title("Text to Speech Converter")

# Sidebar
st.sidebar.header("Settings")
st.sidebar.subheader("Last seen")
st.sidebar.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  # Display current date and time

# Definition of quantum computing
quantum_computing_definition = (
    "Quantum computing is a type of computation that harnesses the unique properties of quantum mechanics. "
    "Unlike classical computers that use bits as the smallest unit of data, quantum computers use quantum bits, "
    "or qubits, which can exist in multiple states at once. This allows quantum computers to process complex "
    "calculations much faster than classical computers, making them suitable for tasks such as cryptography, "
    "optimization problems, and simulations of quantum systems."
)

# Language selection with example texts
languages = {
    "en": quantum_computing_definition,  # English
    "es": "La computación cuántica es un tipo de computación que aprovecha las propiedades únicas de la mecánica cuántica.",  # Spanish
    "zh": "量子计算是一种利用量子力学独特性质的计算方式。",  # Chinese
    "hi": "क्वांटम कंप्यूटिंग एक प्रकार की गणना है जो क्वांटम यांत्रिकी की अद्वितीय विशेषताओं का लाभ उठाती है।",  # Hindi
    "ar": "الحوسبة الكمومية هي نوع من الحوسبة التي تستفيد من الخصائص الفريدة لميكانيكا الكم.",  # Arabic
    "bn": "কোয়ান্টাম কম্পিউটিং হল একটি প্রকারের গণনা যা কোয়ান্টাম মেকানিক্সের অনন্য বৈশিষ্ট্যগুলিকে কাজে লাগায়।",  # Bengali
    "pt": "A computação quântica é um tipo de computação que aproveita as propriedades únicas da mecânica quântica.",  # Portuguese
    "ru": "Квантовые вычисления — это тип вычислений, который использует уникальные свойства квантовой механики.",  # Russian
    "ja": "量子コンピューティングは、量子力学の独自の特性を利用する計算の一種です。",  # Japanese
    "de": "Quantencomputing ist eine Art von Berechnung, die die einzigartigen Eigenschaften der Quantenmechanik nutzt.",  # German
    "fr": "L'informatique quantique est un type de calcul qui exploite les propriétés uniques de la mécanique quantique.",  # French
    "it": "Il calcolo quantistico è un tipo di calcolo che sfrutta le proprietà uniche della meccanica quantistica.",  # Italian
    "ko": "양자 컴퓨팅은 양자 역학의 고유한 특성을 활용하는 계산 유형입니다.",  # Korean
    "tr": "Kuantum hesaplama, kuantum mekaniğinin benzersiz özelliklerini kullanan bir hesaplama türüdür.",  # Turkish
    "vi": "Điện toán lượng tử là một loại hình tính toán khai thác những đặc tính độc đáo của cơ học lượng tử.",  # Vietnamese
    "pl": "Komputery kwantowe to rodzaj obliczeń, które wykorzystują unikalne właściwości mechaniki kwantowej.",  # Polish
    "uk": "Квантові обчислення — це тип обчислень, який використовує унікальні властивості квантової механіки.",  # Ukrainian
    "fa": "محاسبات کوانتومی نوعی محاسبه است که از ویژگی‌های منحصر به فرد مکانیک کوانتومی بهره می‌برد.",  # Persian
    "th": "การคำนวณควอนตัมเป็นประเภทของการคำนวณที่ใช้ประโยชน์จากคุณสมบัติที่ไม่เหมือนใครของกลศาสตร์ควอนตัม.",  # Thai
    "ml": "ക്വാണ്ടം കമ്പ്യൂട്ടിംഗ് ഒരു കമ്പ്യൂട്ടിംഗാണ്, ക്വാണ്ടം യാന്ത്രികതയുടെ പ്രത്യേകതകൾ പ്രയോജനപ്പെടുത്തുന്നു.",  # Malayalam
    "ta": "குவாண்டம் கணினி என்பது குவாண்டம் மெக்கானிக்சின் தனிப்பட்ட பண்புகளை பயன்படுத்தும் கணினி வகையாகும்.",  # Tamil
    "kn": "ಕ್ವಾಂಟಮ್ ಕಂಪ್ಯೂಟಿಂಗ್ ಎಂದರೆ ಕ್ವಾಂಟಮ್ ಮೆಕ್ಯಾನಿಕ್‌ಗಳ ವಿಶೇಷತೆಗಳನ್ನು ಬಳಸುವ ಪ್ರಕಾರದ ಕಂಪ್ಯೂಟಿಂಗ್.",  # Kannada
    "te": "క్వాంటం కంప్యూటింగ్ అనేది క్వాంటం యాంత్రిక శాస్త్రం యొక్క ప్రత్యేకతలను ఉపయోగించే ఒక శ్రేణి కంప్యూటింగ్."  # Telugu
}

# Top 10 Indian languages
indian_languages = {
    "hi": "हिन्दी (Hindi) - क्वांटम कंप्यूटिंग एक प्रकार की गणना है जो क्वांटम यांत्रिकी की अद्वितीय विशेषताओं का लाभ उठाती है。",
    "bn": "বাংলা (Bengali) - কোয়ান্টাম কম্পিউটিং হল একটি প্রকারের গণনা যা কোয়ান্টাম মেকানিক্সের অনন্য বৈশিষ্ট্যগুলিকে কাজে লাগায়।",
    "te": "తెలుగు (Telugu) - క్వాంటం కంప్యూటింగ్ అనేది క్వాంటం యాంత్రిక శాస్త్రం యొక్క ప్రత్యేకతలను ఉపయోగించే ఒక శ్రేణి కంప్యూటింగ్.",
    "ta": "தமிழ் (Tamil) - குவாண்டம் கணினி என்பது குவாண்டம் மெக்கானிக்சின் தனிப்பட்ட பண்புகளை பயன்படுத்தும் கணினி வகையாகும்.",
    "ml": "മലയാളം (Malayalam) - ക്വാണ്ടം കമ്പ്യൂട്ടിംഗ് ഒരു കമ്പ്യൂട്ടിംഗാണ്, ക്വാണ്ടം യാന്ത്രികതയുടെ പ്രത്യേകതകൾ പ്രയോജനപ്പെടുത്തുന്നു.",
    "kn": "ಕನ್ನಡ (Kannada) - ಕ್ವಾಂಟಮ್ ಕಂಪ್ಯೂಟಿಂಗ್ ಎಂದರೆ ಕ್ವಾಂಟ್ ಮೆಕ್ಯಾನಿಕ್‌ಗಳ ವಿಶೇಷತೆಗಳನ್ನು ಬಳಸುವ ಪ್ರಕಾರದ ಕಂಪ್ಯೂಟಿಂಗ್.",
    "mr": "मराठी (Marathi) - क्वांटम संगणक एक प्रकारचा संगणक आहे जो क्वांटम यांत्रिकीच्या अद्वितीय गुणधर्मांचा उपयोग करतो.",
    "gu": "ગુજરાતી (Gujarati) - ક્વાન્ટમ કમ્પ્યુટિંગ એ એવી ગણતરી છે જે ક્વાન્ટમ મિકેનિક્સની વિશિષ્ટતાઓનો ઉપયોગ કરે છે.",
    "or": "ଓଡ଼ିଆ (Odia) - କ୍ୱାଣ୍ଟମ୍ କମ୍ପ୍ୟୁଟିଂ ହେଉଛି ଏକ ପ୍ରକାରର କମ୍ପ୍ୟୁଟିଂ, ଯାହା କ୍ୱାଣ୍ଟମ୍ ମେକାନିକ୍ସର ଅନନ୍ୟ ଗୁଣଧର୍ମଗୁଡିକୁ ଲାଭ ଦେଇଥାଏ।",
    "pa": "ਪੰਜਾਬੀ (Punjabi) - ਕੁਆਂਟਮ ਕੰਪਿਊਟਿੰਗ ਇੱਕ ਕਿਸਮ ਦਾ ਕੰਪਿਊਟਿੰਗ ਹੈ ਜੋ ਕੁਆਂਟਮ ਮਕੈਨਿਕਸ ਦੇ ਵਿਲੱਖਣ ਗੁਣਾਂ ਦਾ ਲਾਭ ਲੈਂਦੀ ਹੈ।"
}

# Combine Indian languages with existing languages
languages.update(indian_languages)

# User input
selected_language = st.selectbox("Select the language:", list(languages.keys()))
example_text = languages[selected_language]
user_input = st.text_area("Enter the text you want to modify:", example_text)

# Footer
st.markdown("<footer style='text-align: center; padding: 10px;'><small>© 2024 SriKrishna Text to Speech Converter. All rights reserved.</small></footer>", unsafe_allow_html=True)
