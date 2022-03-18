import abc


class Animation(abc.ABC):
    animation_name = None
    animation_type = None

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __eq__(self, other):
        return self.animation_name == other.animation_name

    def __ne__(self, other):
        return self.animation_name == other.animation_name

    def __str__(self):
        return f'######################################\n' \
               f'{self.animation_name}: {self.animation_type}\n' \
               f'######################################\n' \
               f'キャラクター名: {self.name}         \n' \
               f'######################################'


class HimoutoUmaru(Animation):
    animation_name = '干物妹!うまるちゃん'
    animation_type = 'コメディ'


umaru = HimoutoUmaru('うまるちゃん', 17)

print(umaru)



