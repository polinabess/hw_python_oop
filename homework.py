
class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, duration: float,
                 distance: float, speed: float, calories: float) -> None:
        self.tratraining_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.tratraining_type}; '
                f'Длительность: {self.duration:0.3f} ч.; '
                f'Дистанция: {self.distance:0.3f} км; '
                f'Ср. скорость: {self.speed:0.3f} км/ч; '
                f'Потрачено ккал: {self.calories:0.3f}.')


class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    LEN_STEP = 0.65  # Один шаг

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration, self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий. Тренировка: бег."""
        mean_speed = self.get_mean_speed()
        duration_in_min = self.duration * 60
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        # (18 * средняя_скорость - 20) *
        # * вес_спортсмена / M_IN_KM * время_тренировки_в_минутах
        spent_calories: float = (
            (coeff_calorie_1 * mean_speed - coeff_calorie_2)
            * self.weight / self.M_IN_KM * duration_in_min)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
        Тренировка: спортивная ходьба."""
        mean_speed = self.get_mean_speed()
        duration_in_min = self.duration * 60
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        # (0.035 * вес + (средняя_скорость**2 // рост) * 0.029 * вес)
        #  * время_тренировки_в_минутах
        spent_calories: float = (
            (coeff_calorie_1 * self.weight
             + (mean_speed**2 // self.height)
             * coeff_calorie_2 * self.weight) * duration_in_min)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий. Тренировка: плавание."""
        # (средняя_скорость + 1.1) * 2 * вес
        mean_speed = self.get_mean_speed()
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        spent_calories: float = (
            (mean_speed + coeff_calorie_1) * coeff_calorie_2 * self.weight)
        return spent_calories

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        # длина_бассейна * count_pool / M_IN_KM / время_тренировки
        mean_speed: float = (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration)
        return mean_speed


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return workout_type_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
