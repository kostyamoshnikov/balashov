/**
 * Николай Балашов — единый источник дизайн-токенов.
 * Используется генераторами документов (Documents/_sources/build_*.js).
 * Для сайта те же значения продублированы в :root каждой HTML-страницы
 * (см. Brand/design-tokens.css — эталонная копия для сверки/копипаста).
 */
module.exports = {
  color: {
    paper: "#EFE3C8",
    ink: "#211B18",
    inkSoft: "#3A302A",
    crimson: "#E8323D",
    crimsonDeep: "#A81C24",
    cobalt: "#2F55D4",
    cobaltDeep: "#182E82",
    ochre: "#F0932B",
    ochreDeep: "#B4650E",
    ochreLight: "#FBC873",
    emerald: "#12A488",
    emeraldDeep: "#0B6A57",
    foil: "#FFC94D",
    foilDeep: "#C9861A",
    // цвета, используемые в docx-генераторах (ближайшие web-safe эквиваленты)
    docx: {
      ink: "211B18",
      crimson: "C4272E",
      gold: "B4650E",
      grey: "5A4A3A",
      paper: "F4ECD8",
    },
  },
  font: {
    display: "Bricolage Grotesque",       // имя, крупные цифры
    editorialItalic: "Instrument Serif",  // интонация, подписи
    body: "Public Sans",                  // связный текст
    labelsData: "Space Mono",             // метки, даты, технические детали
    // ближайшие аналоги, доступные в Word без установки шрифтов
    docx: {
      display: "Georgia",
      body: "Calibri",
      mono: "Consolas",
    },
  },
  contact: {
    email: "booking@balashov-circus.ru",
  },
};
