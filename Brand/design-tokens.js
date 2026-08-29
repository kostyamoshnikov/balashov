/**
 * «Шоу Балашова» — дизайн-токены реального бренда (по логотипу vk.ru/show_balashov).
 * Используется генераторами документов (Documents/_sources/build_*.js).
 */
module.exports = {
  color: {
    // цвета, используемые в docx-генераторах (ближайшие web-safe эквиваленты
    // палитры настоящего логотипа: чёрный фон, огненно-красный, золото)
    docx: {
      ink: "1A0F08",     // почти чёрный фон логотипа
      crimson: "C81E1E", // огненно-красный шатра/ленты
      gold: "C9861A",    // золото букв (тёмный вариант, для текста на белом)
      grey: "5A4A3A",
      paper: "FFFFFF",   // страница документа — обычная белая (не пытаемся повторить чёрный фон логотипа в Word)
    },
  },
  font: {
    docx: {
      display: "Georgia",
      body: "Calibri",
      mono: "Consolas",
    },
  },
  contact: {
    email: "balashov.show.ru@gmail.com",
    phone: "+7 911 913-83-74",
    vk: "https://vk.ru/show_balashov",
  },
};
