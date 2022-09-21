from dataclasses import dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Вернуть строку с сообщением"""
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:0.3f} ч.; '
            f'Дистанция: {self.distance:0.3f} км; '
            f'Ср. скорость: {self.speed:0.3f} км/ч; '
            f'Потрачено ккал: {self.calories:0.3f}.'
        )


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65  # Один шаг
    CONVERT_TIME_OF_TRAIN_TO_MIN: int = 60  # Константа для перевода времени.

    def __init__(
        self,
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
        raise NotImplementedError(
            'Невозможно вычислить количество затраченных калорий'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration, self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_RUN1: int = 18
    COEFF_CALORIE_RUN2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий. Тренировка: бег."""
        mean_speed = self.get_mean_speed()
        duration_in_min = self.duration * self.CONVERT_TIME_OF_TRAIN_TO_MIN
        # (18 * средняя_скорость - 20) *
        # * вес_спортсмена / M_IN_KM * время_тренировки_в_минутах
        return (
            (self.COEFF_CALORIE_RUN1 * mean_speed - self.COEFF_CALORIE_RUN2)
            * self.weight / self.M_IN_KM * duration_in_min
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_WLK1: float = 0.035
    COEFF_CALORIE_WLK2: float = 0.029

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
        Тренировка: спортивная ходьба."""
        mean_speed = self.get_mean_speed()
        duration_in_min = self.duration * self.CONVERT_TIME_OF_TRAIN_TO_MIN
        # (0.035 * вес + (средняя_скорость ** 2 // рост) * 0.029 * вес)
        #  * время_тренировки_в_минутах
        return (
            (
                self.COEFF_CALORIE_WLK1 * self.weight
                + (mean_speed ** 2 // self.height)
                * self.COEFF_CALORIE_WLK2 * self.weight
            ) * duration_in_min
        )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_CALORIE_SWM1: float = 1.1
    COEFF_CALORIE_SWM2: int = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: int
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий. Тренировка: плавание."""
        # (средняя_скорость + 1.1) * 2 * вес
        mean_speed = self.get_mean_speed()
        return (
            (mean_speed + self.COEFF_CALORIE_SWM1)
            * self.COEFF_CALORIE_SWM2 * self.weight
        )

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        # длина_бассейна * count_pool / M_IN_KM / время_тренировки
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )


def read_package(
    workout_type: str,
    data: list
) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_collection: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    check_training(workout_type, workout_collection)
    return workout_collection[workout_type](*data)


def check_training(
    workout_type: str,
    workout_collection: Dict[str, Type[Training]],
) -> bool:
    """Проверить валидность типа тренировки"""
    if workout_type not in workout_collection:
        raise ValueError(
            f'Тренировка {workout_type} не найдена в списке тренировок'
        )


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('KEK', [1, 2, 3, 4])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
