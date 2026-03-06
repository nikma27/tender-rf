export interface Tender {
  id: number
  title: string
  fzType: string
  price: string
  region: string
  deadline: string
}

export const mockTenders: Tender[] = [
  {
    id: 1,
    title: "Поставка оргтехники для государственных нужд",
    fzType: "44-ФЗ",
    price: "2 500 000 ₽",
    region: "Москва",
    deadline: "15.04.2025",
  },
  {
    id: 2,
    title: "Ремонт административного здания",
    fzType: "223-ФЗ",
    price: "15 000 000 ₽",
    region: "Санкт-Петербург",
    deadline: "20.04.2025",
  },
  {
    id: 3,
    title: "Закупка медицинского оборудования",
    fzType: "44-ФЗ",
    price: "8 750 000 ₽",
    region: "Московская область",
    deadline: "25.04.2025",
  },
  {
    id: 4,
    title: "Разработка программного обеспечения",
    fzType: "223-ФЗ",
    price: "12 300 000 ₽",
    region: "Новосибирск",
    deadline: "30.04.2025",
  },
  {
    id: 5,
    title: "Поставка канцелярских товаров",
    fzType: "44-ФЗ",
    price: "450 000 ₽",
    region: "Казань",
    deadline: "05.05.2025",
  },
  {
    id: 6,
    title: "Строительство спортивного комплекса",
    fzType: "44-ФЗ",
    price: "125 000 000 ₽",
    region: "Екатеринбург",
    deadline: "15.05.2025",
  },
  {
    id: 7,
    title: "Услуги по охране объектов",
    fzType: "223-ФЗ",
    price: "3 200 000 ₽",
    region: "Нижний Новгород",
    deadline: "22.05.2025",
  },
  {
    id: 8,
    title: "Поставка продуктов питания",
    fzType: "44-ФЗ",
    price: "1 850 000 ₽",
    region: "Краснодар",
    deadline: "28.05.2025",
  },
]
