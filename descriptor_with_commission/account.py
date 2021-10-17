## Из описания задания непонятно, должен ли Account поддерживать операции добавления денег на счет
## Кажется, как будто нет.
## Пыталась погуглить, можно ли с помощью дескрипторов сделать так, чтобы можно было писать "new_account.amount += 100",
## ничего внятного не нашла.

class Value:
    def __init__(self, label):
        self.label = label

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.label)
    
    def __set__(self, instance, value):
        assert(value >= 0), "cannot process negative amount"
        instance.__dict__[self.label] = value * (1 - instance.commission)

class Account:
    amount = Value('amount')
    
    def __init__(self, commission):
        self.commission = commission

new_account = Account(0.01)
new_account.amount = -100

print(new_account.amount)
90
