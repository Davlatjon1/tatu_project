from data.config import LANGUAGE_RU, LANGUAGE_EN, LANGUAGE_UZ

STATUS_AWAITING_SHIPMENT = 'awaiting_shipment'
STATUS_REJECTED = 'rejected'
STATUS_ON_THE_WAY = 'on_the_way'
STATUS_ACCEPTED = 'accepted'
STATUS_NEW = 'new'

ORDER_STATUSES = {
    STATUS_AWAITING_SHIPMENT: {
        LANGUAGE_RU: "🕔🚕 Ожидает отгрузки",
        LANGUAGE_EN: "🕔🚕 Awaiting shipment",
        LANGUAGE_UZ: "🕔🚕 Етказиб беришни кутмоқда"
    },
    STATUS_REJECTED: {
        LANGUAGE_RU: "❌ Отклонено",
        LANGUAGE_EN: "❌ Rejected",
        LANGUAGE_UZ: "❌ Рад етилди"
    },
    STATUS_ON_THE_WAY: {
        LANGUAGE_RU: "🚕 В пути",
        LANGUAGE_EN: "🚕 On the way",
        LANGUAGE_UZ: "🚕 Юлда"
    },
    STATUS_ACCEPTED: {
        LANGUAGE_RU: "✅ Принят",
        LANGUAGE_EN: "✅ Accepted",
        LANGUAGE_UZ: "✅ Қабул қилинган"
    },
    STATUS_NEW: {
        LANGUAGE_RU: "🆕 Новый",
        LANGUAGE_EN: "🆕 New",
        LANGUAGE_UZ: "🆕 Янги"
    }
}

# ----------------------------------- TYPES OF PAYMENT ----------------
CASH = 'cash'
TERMINAL = 'terminal'

TYPES_OF_PAYMENT = {
    CASH: {
        LANGUAGE_RU: '💵 Наличные',
        LANGUAGE_EN: '💵 Cash',
        LANGUAGE_UZ: '💵 Нақт пул'
    },
    TERMINAL: {
        LANGUAGE_RU: '💳 Терминал',
        LANGUAGE_EN: '💳 Terminal',
        LANGUAGE_UZ: '💳 Терминал'
    },
}

# ---------------------------------- TYPES OF ACT SVERKI -------------
TEXT = 'text'
FILE_PDF = 'file_pdf'
TYPES_OF_ACT_SVERKI = {
    TEXT: {
        LANGUAGE_RU: 'Текст',
        LANGUAGE_EN: 'Text',
        LANGUAGE_UZ: 'Матн'
    },
    FILE_PDF: {
        LANGUAGE_RU: 'Файл (pdf)',
        LANGUAGE_EN: 'File (pdf)',
        LANGUAGE_UZ: 'Файл (pdf)'
    }
}