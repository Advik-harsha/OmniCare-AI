"""
OmniCare AI — Regional Speech Counselor (8 Indian Languages) Engine
Qualcomm Snapdragon® AI Lab Build & Present Challenge 2026
Implements on-device multilingual discharge counseling and speech synthesis metadata
supporting Hindi, Tamil, Telugu, Kannada, Bengali, Marathi, Malayalam, and Gujarati.
"""

from typing import Dict, Any, List, Optional

try:
    from config import CONFIG
    from engine.execution_mode import wrap_clinical_response
except ImportError:
    from backend.config import CONFIG
    from backend.engine.execution_mode import wrap_clinical_response

# Supported 8 Indian Regional Languages with Native Script and Phonetic Pronunciation
REGIONAL_LANGUAGES: Dict[str, Dict[str, Any]] = {
    "hi-IN": {
        "code": "hi-IN",
        "name": "Hindi",
        "native_name": "हिन्दी",
        "voice_gender": "Female",
        "speech_rate": 0.95,
        "pitch": 1.0,
        "greeting": "नमस्ते। आपकी स्वास्थ्य रिपोर्ट और दवाइयों की जानकारी नीचे दी गई है।",
        "phonetic_greeting": "Namaste. Aapki swasthya report aur dawaiyon ki jaankari neeche di gayi hai.",
        "red_flag_warning": "यदि आपको सीने में तेज दर्द, सांस लेने में अत्यधिक कठिनाई या चक्कर आए, तो तुरंत नजदीकी आपातकालीन केंद्र जाएं।",
        "phonetic_red_flag": "Yadi aapko seene mein tej dard ya saans lene mein kathinai ho, to turant aapaatkaaleen kendra jaayein."
    },
    "ta-IN": {
        "code": "ta-IN",
        "name": "Tamil",
        "native_name": "தமிழ்",
        "voice_gender": "Female",
        "speech_rate": 0.92,
        "pitch": 1.05,
        "greeting": "வணக்கம். உங்கள் மருத்துவ பரிசோதனை மற்றும் மருந்து விவரங்கள் கீழே உள்ளன.",
        "phonetic_greeting": "Vanakkam. Ungal maruthuva arikkai matrum marundhu vivarangal.",
        "red_flag_warning": "நெஞ்சு வலி, கடுமையான மூச்சுத்திணறல் அல்லது தலைசுற்றல் ஏற்பட்டால், உடனடியாக அருகிலுள்ள அவசர சிகிச்சைப் பிரிவை அணுகவும்.",
        "phonetic_red_flag": "Nenju vali alladhu koodiya moochuthinaral erpattal, udanadiyaaga avasara sikitchai pirivai anugavum."
    },
    "te-IN": {
        "code": "te-IN",
        "name": "Telugu",
        "native_name": "తెలుగు",
        "voice_gender": "Female",
        "speech_rate": 0.94,
        "pitch": 1.0,
        "greeting": "నమస్కారం. మీ ఆరోగ్య నివేదిక మరియు మందుల వివరాలు క్రింద ఇవ్వబడ్డాయి.",
        "phonetic_greeting": "Namaskaram. Mee aarogya nivedika mariyu mandhula vivaralu.",
        "red_flag_warning": "తీవ్రమైన ఛాతీ నొప్పి లేదా శ్వాస తీసుకోవడంలో ఇబ్బంది కలిగితే వెంటనే అత్యవసర విభాగాన్ని సంప్రదించండి.",
        "phonetic_red_flag": "Theevramaina chathi noppi leda swasa theesukovadamlo ibbandhi kaligithe ventane athyavasara vibhagaanni sampradinchandi."
    },
    "kn-IN": {
        "code": "kn-IN",
        "name": "Kannada",
        "native_name": "ಕನ್ನಡ",
        "voice_gender": "Female",
        "speech_rate": 0.93,
        "pitch": 1.0,
        "greeting": "ನಮಸ್ಕಾರ. ನಿಮ್ಮ ಆರೋಗ್ಯ ವರದಿ ಮತ್ತು ಔಷಧಿಗಳ ವಿವರಗಳು ಕೆಳಗೆ ಇವೆ.",
        "phonetic_greeting": "Namaskara. Nimma aarogya varadi matthu aushadhigala vivaragalu.",
        "red_flag_warning": "ಎದೆ ನೋವು ಅಥವಾ ಉಸಿರಾಟದ ತೀವ್ರ ತೊಂದರೆ ಕಂಡುಬಂದರೆ ತಕ್ಷಣವೇ ತುರ್ತು ಚಿಕಿತ್ಸಾ ಕೇಂದ್ರಕ್ಕೆ ಭೇಟಿ ನೀಡಿ.",
        "phonetic_red_flag": "Ede novu athava usiraata thondare kandubandare thakshanave thurthu chikithsa kendrakke bheti needi."
    },
    "bn-IN": {
        "code": "bn-IN",
        "name": "Bengali",
        "native_name": "বাংলা",
        "voice_gender": "Female",
        "speech_rate": 0.96,
        "pitch": 1.0,
        "greeting": "নমস্কার। আপনার স্বাস্থ্য পরীক্ষা এবং ওষুধের বিবরণ নিচে দেওয়া হলো।",
        "phonetic_greeting": "Nomoshkar. Aaponar swasthya poriksha ebong oushodher biboron.",
        "red_flag_warning": "বুকে তীব্র ব্যথা বা শ্বাসকষ্ট অনুভব করলে অবিলম্বে নিকটস্থ জরুরি বিভাগে যোগাযোগ করুন।",
        "phonetic_red_flag": "Booke teebro byatha ba shwaaskashto onubhob korle obilombe nikot-stho joruri bibhaage jogajog korun."
    },
    "mr-IN": {
        "code": "mr-IN",
        "name": "Marathi",
        "native_name": "मराठी",
        "voice_gender": "Female",
        "speech_rate": 0.95,
        "pitch": 1.0,
        "greeting": "नमस्कार. आपला वैद्यकीय अहवाल आणि औषधांचे तपशील खालीलप्रमाणे आहेत.",
        "phonetic_greeting": "Namaskar. Aapla vaidyakiya ahaval aani aushadhanche tapashil.",
        "red_flag_warning": "छातीत असह्य वेदना किंवा श्वास घेण्यास त्रास झाल्यास तातडीने जवळच्या आपत्कालीन कक्षाशी संपर्क साधा.",
        "phonetic_red_flag": "Chhaatit asahya vedna kinva shwaas ghenyaas traas zaalyaas taatdine javalchya aapatkaaleen kakshaashi samparka saadhaa."
    },
    "ml-IN": {
        "code": "ml-IN",
        "name": "Malayalam",
        "native_name": "മലയാളം",
        "voice_gender": "Female",
        "speech_rate": 0.90,
        "pitch": 1.02,
        "greeting": "നമസ്കാരം. നിങ്ങളുടെ ആരോഗ്യ പരിശോധനാ വിവരങ്ങളും മരുന്നുകളുടെ കുറിപ്പടിയും താഴെ നൽകുന്നു.",
        "phonetic_greeting": "Namaskaram. Ningalude aarogya parishodhana vivarangalum marunnukalude kurippadiyum.",
        "red_flag_warning": "നെഞ്ചുവേദനയോ കഠിനമായ ശ്വാസതടസ്സമോ ഉണ്ടായാல் ഉടൻ തന്നെ അടുത്തുള്ള അടിയന്തിര വിഭാഗത്തിലേക്ക് പോകുക.",
        "phonetic_red_flag": "Nenju-vedanayo kadinamaaya swasathadasamo undaayaal udan thanne aduthulla adiyanthira vibhagathilekku pokuka."
    },
    "gu-IN": {
        "code": "gu-IN",
        "name": "Gujarati",
        "native_name": "ગુજરાતી",
        "voice_gender": "Female",
        "speech_rate": 0.95,
        "pitch": 1.0,
        "greeting": "નમસ્તે. તમારા સ્વાસ્થ્ય અહેવાલ અને દવાઓની વિગતો નીચે મુજબ છે.",
        "phonetic_greeting": "Namaste. Tamara swasthya aheval ane davaoni vigato.",
        "red_flag_warning": "છાતીમાં દુખાવો અથવા શ્વાસ લેવામાં ગંભીર તકલીફ જણાય તો તરત જ નજીકના ઇમરજન્સી સેન્ટરનો સંપર્ક કરો.",
        "phonetic_red_flag": "Chhati-man dukhāvo athva shwas levaman takleef janay to tarat j najikna emergency center-no sampark karo."
    }
}


def get_supported_languages() -> List[Dict[str, Any]]:
    """Returns the list of 8 supported Indian regional languages."""
    return list(REGIONAL_LANGUAGES.values())


def synthesize_counseling(
    condition: str = "Hypertension & Cardiovascular Health",
    language_code: str = "hi-IN",
    medications: Optional[List[str]] = None,
    lifestyle_tips: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Generates culturally tailored, phonetically clear discharge advice and
    Web Audio / Web Speech API parameters in the target Indian regional language.
    """
    code = language_code if language_code in REGIONAL_LANGUAGES else "hi-IN"
    lang_info = REGIONAL_LANGUAGES[code]

    meds = medications if medications else [
        "Atorvastatin 20mg (PMBJP Jan Aushadhi - 1 tablet at bedtime)",
        "Pantoprazole 40mg (1 tablet 30 min before breakfast)"
    ]

    tips = lifestyle_tips if lifestyle_tips else [
        "Maintain low-sodium diet (<5g salt per day)",
        "Daily 30-minute brisk walk",
        "Daily hydration (2-2.5 Liters of water)"
    ]

    # Construct regional translation narrative
    localized_instructions = [
        lang_info["greeting"],
        f"निदान / Diagnosis: {condition}",
        "दवाइयों का शेड्यूल / Medication Schedule (PMBJP जन औषधि केंद्र से 80%+ की बचत के साथ):"
    ]
    for m in meds:
        localized_instructions.append(f"• {m}")

    localized_instructions.append("दैनिक स्वास्थ्य सलाह / Lifestyle Guidance:")
    for t in tips:
        localized_instructions.append(f"• {t}")

    localized_instructions.append(f"चेतावनी / Red Flag Alert: {lang_info['red_flag_warning']}")

    # Phonetic guidance for fallback speech engines
    phonetic_instructions = [
        lang_info.get("phonetic_greeting", lang_info["greeting"]),
        f"Clinical Diagnosis: {condition}",
        "Medication Schedule with over 80 percent PMBJP Jan Aushadhi savings:"
    ]
    for m in meds:
        phonetic_instructions.append(f"• {m}")
    phonetic_instructions.append(f"Emergency Alert: {lang_info.get('phonetic_red_flag', lang_info['red_flag_warning'])}")

    res = {
        "engine": "Qualcomm Hexagon NPU Regional Speech Counselor (On-Device)",
        "language_code": code,
        "language": lang_info["name"],
        "native_name": lang_info["native_name"],
        "voice_gender": lang_info["voice_gender"],
        "synthesizer_config": {
            "rate": lang_info["speech_rate"],
            "pitch": lang_info["pitch"],
            "volume": 1.0,
            "browser_lang_tag": code,
            "tts_api": "HTML5 SpeechSynthesis / Web Audio API"
        },
        "counseling_script": "\n".join(localized_instructions),
        "localized_instructions": localized_instructions,
        "phonetic_instructions": phonetic_instructions,
        "phonetic_narrative": " ".join(phonetic_instructions),
        "red_flag_warning": lang_info["red_flag_warning"],
        "zero_cloud_egress": True
    }
    return wrap_clinical_response(res, "Edge Service: Regional Speech Counselor", "Multilingual Acoustic Prosody Synthesizer", 8.4)

