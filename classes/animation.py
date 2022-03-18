import abc


class Animation(abc.ABC):
    animation_name = None
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __eq__(self, other):
        return self.animation_name == other.animation_name

    def __ne__(self, other):
        return self.animation_name == other.animation_name

    def __str__(self):
        return f'{self.animation_name}: {self.name}'


class HimoutoUmaru(Animation):
    animation_name = '干物妹!うまるちゃん'
    
umaru = HimoutoUmaru('うまるちゃん', 17)

print(umaru)



