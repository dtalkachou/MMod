# СЕТИ ПЕТРИ

## Сеть №1

![network_1](src/images/net1.jpg)

### Диаграммы маркировок

#### MATLAB

![diagr_1](src/images/diag1.jpg)

#### Найденная

![diagr_1_2](src/images/diag1_2.jpg)

### Классификация

### По динамическим ограничениям

1.	**1-ограниченная**, т.к. ни в одной позиции число маркеров не будет превышать единицу.
2.	**Безопасная**, т.к. она 1-ограничена.
3.	**1-консервативная**, т.к. в процессе функционирования общее число маркеров остается постоянным.
4.	**Не живая**, т.к. при выполнении перехода `t4`, переход `t3` не будет никогда возбужден.
5.	**Не устойчивая**, т.к. если сработает переход `t4`, то с перехода `t1` снимается возбуждение и наоборот.

### По статическим ограничениям

1.	**Сеть свободного выбора**, т.к. каждая дуга, выходящая из позиции, является либо единственным выходом из нее, либо единственным входом в переход.
2.	**Не является маркированным графом**, т.к. позиция `р4` имеет два выхода, а позиция `р5` не имеет выходов.
3.	**Не автоматная**, т.к. переход `t3` имеет два входа и два выхода
4.	**Не бесконфликтная**, т.к. позиция `р4` является входной для `t1` и `t4`, но не является для них выходной.

## Сеть №2

![network_2](src/images/net2.jpg)

### Диаграммы маркировок

#### MATLAB

![diagr_2](src/images/diag2.jpg)

#### Найденная

![diagr_2_2](src/images/diag2_2.jpg)

### Классификация

### По динамическим ограничениям

1.	**2-ограниченная**, т.к. ни в одной позиции число маркеров не будет превышать число два.
2.	**Не безопасная**, т.к. сеть 2-ограниченная.
3.	**Не консервативная**, т.к. в процессе функционирования общее число маркеров не остается постоянным.
4.	**Живая**, т.к. каждый переход является потенциально срабатывающим при любой маркировке.
5.	**Устойчивая**, т.к. срабатывание одного из возможных переходов не может снять возбуждение с других переходов.

### По статическим ограничениям

1.	**Сетью свободного выбора**, т.к. каждая дуга, выходящая из позиции, является либо единственным выходом из нее, либо единственным входом в переход.
2.	**Маркированный граф**, т.к. каждая позиция имеет в точности по одному входному и одному выходному переходу.
3.	**Не автоматная**, т.к. переход `t4` имеет более одного входа.
4.	**Бесконфликтная**, т.к. для каждой позиции существует не более одной исходящей дуги.
