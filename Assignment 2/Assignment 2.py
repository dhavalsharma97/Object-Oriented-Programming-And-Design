# Author: Dhaval Harish Sharma
# RED ID: 824654344
# Currently enrolled in the class
"""Assignment 2: Implementing a spreadsheet with 9 cells with a GUI. A cell can contain either a formula, a number or be empty. A formula can contain numbers, reference to cells and the operations. There is a view button which is used to change the view from value to equation and vice versa. Also, there is a undo button provided in the spreadsheet which is used to undo the last operation."""
# Version: 1.0

from abc import ABCMeta, abstractmethod
from math import *
from tkinter import *
import unittest


class Equation:
    __metaclass__ = ABCMeta

    @abstractmethod
    def interpret(self, postfix_stack):
        pass


class Addition(Equation):
    def __init__(self):
        self.__result = 0

    def interpret(self, postfix_stack):
        self.__result = postfix_stack.pop() + postfix_stack.pop()
        postfix_stack.append(self.__result)


class Subtraction(Equation):
    def __init__(self):
        self.__result = 0

    def interpret(self, postfix_stack):
        self.__result = (-postfix_stack.pop()) + postfix_stack.pop()
        postfix_stack.append(self.__result)


class Multiplication(Equation):
    def __init__(self):
        self.__result = 0

    def interpret(self, postfix_stack):
        self.__result = postfix_stack.pop() * postfix_stack.pop()
        postfix_stack.append(self.__result)


class Division(Equation):
    def __init__(self):
        self.__result = 0

    def interpret(self, postfix_stack):
        self.__result = (1 / postfix_stack.pop()) * postfix_stack.pop()
        postfix_stack.append(self.__result)


class Logarithm(Equation):
    def __init__(self):
        self.__result = 0

    def interpret(self, postfix_stack):
        self.__result = log(postfix_stack.pop(), 2)
        postfix_stack.append(self.__result)


class Sine(Equation):
    def __init__(self):
        self.__result = 0

    def interpret(self, postfix_stack):
        self.__result = sin(postfix_stack.pop())
        postfix_stack.append(self.__result)


class Number(Equation):
    def __init__(self, digit):
        self.__digit = digit

    def interpret(self, postfix_stack):
        postfix_stack.append(self.__digit)


class Parser:
    def __init__(self, postfix_expr):
        self.__parse_tree = []
        self.__operands = {'+': Addition(),
                           '-': Subtraction(),
                           '*': Multiplication(),
                           '/': Division(),
                           'lg': Logarithm(),
                           'sin': Sine()}

        # Making a syntax tree
        for token in postfix_expr.split():
            if token in self.__operands:
                self.__parse_tree.append(self.__operands[token])
            else:
                self.__parse_tree.append(Number(int(token)))

    def evaluate(self):
        postfix_stack = []

        for symbol in self.__parse_tree:
            symbol.interpret(postfix_stack)

        return postfix_stack.pop()


class Memento:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_state(self):
        pass


# Saving the state of a cell
class ConcreteMemento(Memento):
    def __init__(self, cell_formula):
        self.__cell_formula = cell_formula

    def get_state(self):
        return self.__cell_formula


# Mediator for backing and restoring the mementos
class CareTaker:
    def __init__(self):
        self.mementos = []

    def backup(self, cell_obj, cell_memento):
        # Storing cell object and mementos of the corresponding cells
        self.mementos.append([])
        self.mementos[len(self.mementos) - 1].append(cell_obj)
        self.mementos[len(self.mementos) - 1].append(cell_memento)

    def undo(self):
        try:
            cell_obj, memento = self.mementos.pop()
            cell_obj.restore_memento(memento)
        except IndexError:
            pass


# Resolving references from the given formula
class ResolveReferences:
    def __init__(self, cell_obj):
        self.cell_obj = cell_obj
        self.new_references = []

    def resolve_ref(self):
        resolved_formula = ""
        pointer = 0

        # Making the resolved formula
        while pointer < len(self.cell_obj.formula):
            # Finding the reference of another cell in the formula
            if self.cell_obj.formula[pointer] == '$':
                ref_name = self.cell_obj.formula[pointer] + self.cell_obj.formula[pointer + 1].upper()
                ref_value = str(self.cell_obj.cells[ref_name].value)
                if ref_value == "Error":
                    return "Error"
                resolved_formula = resolved_formula + ref_value
                pointer = pointer + 1

                # Adding the cell to the observers list of the encountered reference
                if self.cell_obj.cells[ref_name] not in self.new_references:
                    self.new_references.append(self.cell_obj.cells[ref_name])
                    self.cell_obj.cells[ref_name].add_observer(self.cell_obj)
            else:
                resolved_formula = resolved_formula + self.cell_obj.formula[pointer]
            pointer = pointer + 1

        self.resolve_subjects(self.new_references)
        self.cell_obj.subjects = self.new_references
        return resolved_formula

    # Removing the cell from the subject's observers list which are no longer needed
    def resolve_subjects(self, new_references):
        for subject_pointer in self.cell_obj.subjects:
            if subject_pointer not in new_references:
                subject_pointer.remove_observer(self.cell_obj)


class DependencyDetector:
    def __init__(self, cell_obj):
        self.cell_obj = cell_obj
        self.visited = {}

    def detect_dependency(self):
        for cell in self.cell_obj.cells.keys():
            self.visited[cell] = False
        current_subjects = [subject.name for subject in self.cell_obj.subjects]

        while len(current_subjects) != 0:
            top_element = current_subjects.pop()
            if not self.visited[top_element]:
                for subject in self.cell_obj.cells[top_element].subjects:
                    if not self.visited[subject.name]:
                        if subject.name == self.cell_obj.name:
                            return True
                        current_subjects.append(subject.name)
            self.visited[top_element] = True
        return False


class Subject:
    __metaclass__ = ABCMeta

    @abstractmethod
    def add_observer(self, observer):
        pass

    @abstractmethod
    def remove_observer(self, observer):
        pass

    @abstractmethod
    def notify(self):
        pass


class Observer:
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self):
        pass


class Cell(Subject, Observer):
    def __init__(self, frame, name, cells, caretaker_obj):
        self.frame = frame
        self.name = name
        self.cells = cells
        self.caretaker_obj = caretaker_obj
        self.formula = '0'
        self.value = 0
        self.subjects = []
        self.observers = []

        self.var = StringVar()
        entry = self.widget = Entry(self.frame, textvariable=self.var)
        entry.bind("<Return>", self.enter_pressed)
        self.var.set("0")

    def add_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer):
        try:
            self.observers.remove(observer)
        except ValueError:
            pass

    def notify(self):
        for observer in self.observers:
            observer.update()
            observer.notify()

    def update(self):
        res_ref_obj = ResolveReferences(self)
        resolved_formula = res_ref_obj.resolve_ref()

        # Breaking the notify loop if there is a circular dependency
        if self.formula == "Error":
            return

        dep_det_obj = DependencyDetector(self)
        if dep_det_obj.detect_dependency():
            self.formula = "Error"
            self.value = "Error"
            self.set_var()
            return

        if resolved_formula != "Error":
            parser_obj = Parser(resolved_formula)
            self.value = parser_obj.evaluate()
        else:
            self.value = "Error"

        self.set_var()

    def save_memento(self):
        return ConcreteMemento(self.formula)

    def restore_memento(self, memento):
        self.formula = memento.get_state()
        self.update()
        self.notify()

    def set_var(self):
        SpreadSheet.current_view.display(self)

    def enter_pressed(self, event):
        self.caretaker_obj.backup(self, self.save_memento())
        self.formula = self.var.get()

        if hasattr(event, 'keysym') and event.keysym == "Return":
            self.update()
            self.notify()


class State:
    __metaclass__ = ABCMeta

    @abstractmethod
    def swap_view(self):
        pass

    @abstractmethod
    def display(self, cells):
        pass


class Value(State):
    def swap_view(self):
        SpreadSheet.current_view.__class__ = Expression
        
    def display(self, cell):
        cell.var.set(cell.value)


class Expression(State):
    def swap_view(self):
        SpreadSheet.current_view.__class__ = Value

    def display(self, cell):
        cell.var.set(cell.formula)


class SpreadSheet:
    # Initializing the GUI with Expression View
    current_view = Expression()

    def __init__(self, root):
        self.frame = root
        self.cells = {}
        self.caretaker_obj = CareTaker()
        self.create_cells()

        self.view_button = Button(self.frame, text="Expression", command=self.view_pressed)
        self.view_button.grid(row=2, column=3)
        self.undo_button = Button(self.frame, text="Undo", command=self.undo_pressed)
        self.undo_button.grid(row=2, column=5)

    def create_cells(self):
        for column_no in range(9):
            cell_name = Label(self.frame, text="${}".format(chr(ord("A") + column_no)))
            cell_name.grid(row=0, column=column_no)
            cell_obj = Cell(self.frame, cell_name["text"], self.cells, self.caretaker_obj)
            self.cells[cell_name["text"]] = cell_obj
            cell_obj.widget.grid(row=1, column=column_no)

    def view_pressed(self):
        SpreadSheet.current_view.swap_view()
        for cell in self.cells.values():
            SpreadSheet.current_view.display(cell)
        self.update_button_text()

    def update_button_text(self):
        if self.view_button["text"] == "Expression":
            self.view_button["text"] = "Value"
        else:
            self.view_button["text"] = "Expression"

    def undo_pressed(self):
        self.caretaker_obj.undo()


# Unit Testing Begins
class TestSpreadSheet(unittest.TestCase):
    def test_view_pressed(self):
        test_frame = Tk()
        spreadsheet_obj = SpreadSheet(test_frame)
        spreadsheet_obj.cells["$A"].formula = "5"
        spreadsheet_obj.cells["$A"].update()
        spreadsheet_obj.cells["$B"].formula = "$A 1 +"
        spreadsheet_obj.cells["$B"].update()
        self.assertEqual(spreadsheet_obj.cells["$B"].var.get(), "$A 1 +")
        spreadsheet_obj.view_pressed()
        self.assertEqual(spreadsheet_obj.cells["$B"].var.get(), "6")


class TestCell(unittest.TestCase):
    def test_update(self):
        test_frame = Tk()
        spreadsheet_obj = SpreadSheet(test_frame)
        spreadsheet_obj.cells["$A"].formula = "5"
        spreadsheet_obj.cells["$A"].update()
        spreadsheet_obj.cells["$B"].formula = "$A 1 +"
        spreadsheet_obj.cells["$B"].update()
        self.assertEqual(spreadsheet_obj.cells["$B"].formula, "$A 1 +")
        self.assertEqual(spreadsheet_obj.cells["$B"].value, 6)
        self.assertEqual(spreadsheet_obj.cells["$A"].observers[0], spreadsheet_obj.cells["$B"])

        # Testing Circular Dependency
        spreadsheet_obj.cells["$A"].formula = "$B 2 *"
        spreadsheet_obj.cells["$A"].update()
        spreadsheet_obj.cells["$A"].notify()
        self.assertEqual(spreadsheet_obj.cells["$A"].value, "Error")
        self.assertEqual(spreadsheet_obj.cells["$B"].value, "Error")

    def test_notify(self):
        test_frame = Tk()
        spreadsheet_obj = SpreadSheet(test_frame)
        spreadsheet_obj.cells["$A"].formula = "5"
        spreadsheet_obj.cells["$A"].update()
        spreadsheet_obj.cells["$B"].formula = "$A 1 +"
        spreadsheet_obj.cells["$B"].update()
        spreadsheet_obj.cells["$A"].formula = "10"
        spreadsheet_obj.cells["$A"].update()
        spreadsheet_obj.cells["$A"].notify()
        self.assertEqual(spreadsheet_obj.cells["$B"].value, 11)


class TestCareTaker(unittest.TestCase):
    def test_backup(self):
        test_frame = Tk()
        spreadsheet_obj = SpreadSheet(test_frame)
        caretaker_obj = CareTaker()
        cell_a_obj = spreadsheet_obj.cells["$A"]
        cell_a_obj.formula = "5"
        cell_a_obj.update()
        caretaker_obj.backup(cell_a_obj, cell_a_obj.save_memento())
        self.assertEqual(caretaker_obj.mementos[0][0], cell_a_obj)
        self.assertEqual(caretaker_obj.mementos[0][1].get_state(), "5")

    def test_undo(self):
        test_frame = Tk()
        spreadsheet_obj = SpreadSheet(test_frame)
        caretaker_obj = CareTaker()
        cell_a_obj = spreadsheet_obj.cells["$A"]
        cell_b_obj = spreadsheet_obj.cells["$B"]
        caretaker_obj.backup(cell_a_obj, cell_a_obj.save_memento())
        cell_a_obj.formula = "5"
        cell_a_obj.update()
        caretaker_obj.backup(cell_b_obj, cell_b_obj.save_memento())
        cell_b_obj.formula = "$A 1 +"
        cell_b_obj.update()
        self.assertEqual(cell_b_obj.value, 6)
        caretaker_obj.undo()
        self.assertEqual(cell_b_obj.value, 0)
        self.assertEqual(cell_a_obj.value, 5)
        caretaker_obj.undo()
        self.assertEqual(cell_a_obj.value, 0)


class TestParser(unittest.TestCase):
    def test_evaluate(self):
        parser_obj1 = Parser("5 4 2 - *")
        self.assertEqual(parser_obj1.evaluate(), 10)
        parser_obj1 = Parser("1 lg 0 sin -")
        self.assertEqual(parser_obj1.evaluate(), 0)
# Unit Testing Ends


def main():
    root = Tk()
    SpreadSheet(root)
    root.mainloop()
    unittest.main()


if __name__ == "__main__":
    main()
