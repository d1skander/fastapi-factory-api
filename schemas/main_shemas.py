from pydantic import BaseModel

from enum import Enum


class BoilerStatus(str ,Enum):
    IN_QUEUE = "In_queue"
    ASSEMBLING = "Assembling"
    TESTING = "Testing"
    READY_FOR_SHIPMENT = "Ready_for_shipment"


class FactoryRank(str, Enum):
    # === РАБОЧИЕ СТРОКИ (РАЗРЯДЫ ПО ЕТКС) ===
    RANK_1_2 = "Rank_1_2"          # Рабочий 1-2 разряда (Ученик / Низшая квалификация)
    RANK_3_4 = "Rank_3_4"          # Рабочий 3-4 разряда (Основной персонал / Средняя квалификация)
    RANK_5_6 = "Rank_5_6"          # Рабочий 5-6 разряда (Высшая квалификация / Наладчики ЧПУ, бригадиры)

    # === ИНЖЕНЕРНО-ТЕХНИЧЕСКИЕ РАБОТНИКИ (ИТР) ===
    ENGINEER_NO_CAT = "Eng_no_cat" # Инженер без категории (Молодой специалист после вуза)
    ENGINEER_CAT_3 = "Eng_cat_3"   # Инженер III категории (Опыт от 1 до 3 лет)
    ENGINEER_CAT_2 = "Eng_cat_2"   # Инженер II категории (Самостоятельный специалист)
    ENGINEER_CAT_1 = "Eng_cat_1"   # Инженер I категории (Старший инженер / Ведущий группы)
    CHIEF_SPECIALIST = "Chief_spec"# Главный / Ведущий специалист (Главный технолог, Главный конструктор)

    # === РУКОВОДСТВО И УПРАВЛЕНИЕ ===
    FOREMAN = "Foreman"            # Мастер участка / Сменный мастер (Линейный руководитель)
    SHOP_CHIEF = "Shop_chief"      # Начальник цеха / Начальник отдела
    CHIEF_ENGINEER = "Chief_eng"   # Главный инженер (Технический директор завода)
    FACTORY_DIRECTOR = "Director"  # Генеральный директор завода


class Order(BaseModel):
    name: str
    status: BoilerStatus
    power: int