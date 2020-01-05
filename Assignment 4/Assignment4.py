# Author: Dhaval Harish Sharma
# RED ID: 824654344
# Currently enrolled in the class
"""Assignment 4: Implement a flyweight pattern for characters. There is a character class that stores only the unicode
code point of the character. There is a single point of access to the same flyweight factory. The flyweight factory is
also used for fonts. The goal is to save space."""
# Version: 1.0

import sys
import unittest


class CharFactory:
    def __init__(self):
        self.characters = {}

    def __sizeof__(self):
        size = 0
        for key in self.characters:
            size += sys.getsizeof(key)
            size += sys.getsizeof(self.characters[key])
        return size

    # Reuse the character instead of building a new one
    def get_character(self, curr_char):
        if curr_char in self.characters:
            char = self.characters[curr_char]
        else:
            char = Character(curr_char)
            self.characters[curr_char] = char

        return char

    def get_character_array(self):
        return self.characters


class Character:
    def __init__(self, new_val):
        self.val = new_val

    def __sizeof__(self):
        size = 0
        size += sys.getsizeof(self.val)
        return size

    def set_char(self, new_val):
        self.val = new_val

    def get_char(self):
        return self.val


class StyledCharacter:
    def __init__(self, new_val, new_font):
        self.val = new_val
        self.font = new_font

    def __sizeof__(self):
        size = 0
        size += sys.getsizeof(self.val)
        size += sys.getsizeof(self.font)
        return size

    def set_char(self, new_val):
        self.val = new_val

    def get_char(self):
        return self.val


class Font:
    def __init__(self, new_name, new_size, new_style):
        self.name = new_name
        self.size = new_size
        self.style = new_style

    def __sizeof__(self):
        size = 0
        size += sys.getsizeof(self.name)
        size += sys.getsizeof(self.size)
        size += sys.getsizeof(self.style)
        return size

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name

    def get_size(self):
        return self.size

    def set_size(self, new_size):
        self.size = new_size

    def get_style(self):
        return self.style

    def set_style(self, new_style):
        self.style = new_style


class RunArray:
    def __init__(self):
        self.fonts = {}

    def __sizeof__(self):
        size = 0
        for key in self.fonts:
            size += sys.getsizeof(key)
            size += sys.getsizeof(self.fonts[key])
        return size

    def add(self, start, count, new_font):
        end = start + count
        self.delete(start, end)
        self.add_at_index(start, end, new_font)

    def append(self, count, new_font):
        start = 0
        for font in self.fonts:
            for indices in self.fonts[font]:
                if indices[1] > start:
                    start = indices[1]
        self.add_at_index(start, start + count, new_font)

    def add_at_index(self, start, end, font):
        if font not in self.fonts:
            self.fonts[font] = [[start, end]]
        else:
            self.fonts[font].append([start, end])

    def delete(self, start, end):
        for font in self.fonts:
            for indices in self.fonts[font]:
                if indices[0] <= start or indices[1] >= end:
                    if indices[1] < end:
                        count = start - indices[0]
                        if count > 0:
                            self.add_at_index(indices[0], start - 1, font)
                    elif indices[0] > start:
                        count = indices[1] - end
                        if count > 0:
                            self.add_at_index(end + 1, indices[1], font)
                    else:
                        count = start - indices[0]
                        if count > 0:
                            self.add_at_index(indices[0], start - 1, font)
                self.fonts[font].remove(indices)

    def get_font(self, index):
        for font in self.fonts:
            for indices in self.fonts[font]:
                if indices[0] <= index and indices[1] >= index:
                    return font
        return None


# Unit Testing Begins!
class TestFlyWeight(unittest.TestCase):
    def compare_size(self):
        input_str = "CS 635 Advanced Object-Oriented Design & Programming\n" + "Fall Semester, 2018\n" + "Doc 17 Mediator, Flyweight, Facade, Demeter, Active Object\n" + "Nov 19, 2019\n" + "Copyright ©, All rights reserved. 2019 SDSU & Roger Whitney, 5500 Campanile Drive, San" + "Diego, CA 92182-7700 USA. OpenContent (http://www.opencontent.org/opl.shtml) license defines the copyright on this document."

        # Storing strings with flyweight pattern
        runarray_obj = RunArray()
        runarray_obj.add(0, 144, Font("Comic Sans MS", 13, "bold"))
        runarray_obj.add(145, 355, Font("Aerial", 10, "italian"))
        runarray_obj.append(356, Font("Comic Sans MS", 12, ""))

        char_factory_obj = CharFactory()
        chars = []
        flyweight_size = 0
        for index in range(len(input_str)):
            chars.append(char_factory_obj.get_character(input_str[index]))
            flyweight_size += sys.getsizeof(chars[index])

        # Storing strings without flyweight pattern
        chars = []
        non_flyweight_size = 0
        for index in range(len(input_str)):
            char = Character(input_str[index])
            font = None

            if index < 145:
                font = Font("Comic Sans MS", 13, "bold")
            elif index < 356:
                font = Font("Aerial", 10, "italian")
            else:
                font = Font("Comic Sans MS", 12, "")
            chars.append(StyledCharacter(input_str[index], font))
            non_flyweight_size += sys.getsizeof(chars[index])

        self.assertLess(flyweight_size, non_flyweight_size)
# Unit Testing Ends!


def main():
    unittest.main()


if __name__ == "__main__":
    main()
