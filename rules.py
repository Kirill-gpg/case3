import collections
import collections.abc
# Патч для совместимости experta с Python 3.10+
collections.Mapping = collections.abc.Mapping

from experta import KnowledgeEngine, Rule, NOT, P
from facts import Component, Result

# Допустимые пределы
VOLTAGE_MIN = 4.5
VOLTAGE_MAX = 5.5
TEMP_MIN = -40
TEMP_MAX = 85
RESISTANCE_MIN = 100
RESISTANCE_MAX = 10000

class ExpertSystem(KnowledgeEngine):
    @Rule(Component(voltage=P(lambda v: v < VOLTAGE_MIN)))
    def low_voltage(self):
        self.declare(Result(status='Брак', reason='Напряжение ниже минимального'))

    @Rule(Component(voltage=P(lambda v: v > VOLTAGE_MAX)))
    def high_voltage(self):
        self.declare(Result(status='Брак', reason='Напряжение выше максимального'))

    @Rule(Component(temperature=P(lambda t: t < TEMP_MIN)))
    def low_temp(self):
        self.declare(Result(status='Требуется доп проверка', reason='Температура ниже минимальной'))

    @Rule(Component(temperature=P(lambda t: t > TEMP_MAX)))
    def high_temp(self):
        self.declare(Result(status='Брак', reason='Температура выше максимальной'))

    @Rule(Component(resistance=P(lambda r: r < RESISTANCE_MIN)))
    def low_res(self):
        self.declare(Result(status='Брак', reason='Сопротивление ниже минимального'))

    @Rule(Component(resistance=P(lambda r: r > RESISTANCE_MAX)))
    def high_res(self):
        self.declare(Result(status='Брак', reason='Сопротивление выше максимального'))