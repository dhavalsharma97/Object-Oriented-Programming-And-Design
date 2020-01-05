# Author: Dhaval Harish Sharma
# RED ID: 824654344
# Currently enrolled in the class
"""Assignment 3: Implement a binary search tree with addition. Use the null object pattern to add a null node to your tree to eliminate the need to check
for null references or pointers. Modify the binary tree to accept a visitor. Use the strategy pattern to provide an ordering that the tree uses to order
its elements."""
# Version: 1.0

from abc import ABCMeta, abstractmethod
import unittest


class Node:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_val(self):
        pass

    @abstractmethod
    def is_null(self):
        pass

    @abstractmethod
    def accept_tree_visitor(self, visitor_obj):
        pass


class BSTNode(Node):
    def __init__(self, key):
        self._val = key
        self.left = EmptyNode()
        self.right = EmptyNode()

    def get_val(self):
        return self._val

    def is_null(self):
        return False

    def accept_tree_visitor(self, visitor_obj):
        return visitor_obj.visit_bst_node(self)

    def insert_node(self, ordering_strategy_obj, key):
        if ordering_strategy_obj.insertion_order(self._val, key):
            self.right = self.right.insert_node(ordering_strategy_obj, key)
        else:
            self.left = self.left.insert_node(ordering_strategy_obj, key)

        return self

    def search_node(self, key):
        if self._val == key:
            return self
        elif self._val < key:
            return self.right.search_node(key)
        else:
            return self.left.search_node(key)


class EmptyNode(Node):
    def __init__(self):
        self._val = None
        self.left = None
        self.right = None

    def get_val(self):
        return self._val

    def is_null(self):
        return True

    def accept_tree_visitor(self, visitor_obj):
        return visitor_obj.visit_empty_node(self)

    def insert_node(self, ordering_strategy_obj, key):
        return BSTNode(key)

    def search_node(self, key):
        return None


class OrderingStrategy:
    __metaclass__ = ABCMeta

    @abstractmethod
    def insertion_order(self, node_val, key):
        pass


class AlphaOrdering(OrderingStrategy):
    def insertion_order(self, node_val, key):
        if node_val < key:
            return True
        else:
            return False


class ReverseAlphaOrdering(OrderingStrategy):
    def insertion_order(self, node_val, key):
        if node_val[::-1] < key[::-1]:
            return True
        else:
            return False


class TreeVisitor:
    __metaclass__ = ABCMeta

    @abstractmethod
    def visit_bst_node(self, node_obj):
        pass

    @abstractmethod
    def visit_empty_node(self, node_obj):
        pass


class TraversalVisitor(TreeVisitor):
    def visit_bst_node(self, node_obj):
        return "(" + node_obj.get_val() + node_obj.left.accept_tree_visitor(self) + node_obj.right.accept_tree_visitor(self) + ")"

    def visit_empty_node(self, node_obj):
        return "()"


class Tree:
    __metaclass__ = ABCMeta

    @abstractmethod
    def insert(self, key):
        pass

    @abstractmethod
    def search(self, key):
        pass

    @abstractmethod
    def accept_tree_visitor(self, tree_visitor_obj):
        pass


class BinarySearchTree(Tree):
    def __init__(self, root_key, ordering_strategy_obj):
        self.root = BSTNode(root_key)
        self.ordering_strategy_obj = ordering_strategy_obj

    def insert(self, key):
        # Searching to see if duplicate value exists in the tree
        if self.search(key):
            return -1

        self.root.insert_node(self.ordering_strategy_obj, key)

    def search(self, key):
        return self.root.search_node(key)

    def accept_tree_visitor(self, tree_visitor_obj):
        return self.root.accept_tree_visitor(tree_visitor_obj)


# Unit Testing Begins!
class TestBinarySearchTree(unittest.TestCase):
    def test_insert(self):
        ordering_strategy_obj = AlphaOrdering()
        bst_obj = BinarySearchTree("elite", ordering_strategy_obj)
        self.assertEqual(bst_obj.root.get_val(), "elite")
        self.assertEqual(isinstance(bst_obj.root.right, EmptyNode), True)

        bst_obj.insert("cat")
        bst_obj.insert("grapes")
        self.assertEqual(bst_obj.root.left.get_val(), "cat")
        self.assertEqual(bst_obj.root.right.get_val(), "grapes")
        self.assertEqual(isinstance(bst_obj.root.left.left, EmptyNode), True)

    def test_search(self):
        ordering_strategy_obj = AlphaOrdering()
        bst_obj = BinarySearchTree("elite", ordering_strategy_obj)
        bst_obj.insert("cat")
        bst_obj.insert("grapes")

        self.assertEqual(bst_obj.search("cat"), bst_obj.root.left)
        self.assertEqual(bst_obj.search("dog"), None)

    def test_accept_tree_visitor(self):
        # Alphabetical Ordering
        alpha_ordering_obj = AlphaOrdering()
        bst_obj_1 = BinarySearchTree("elite", alpha_ordering_obj)
        bst_obj_1.insert("cat")
        bst_obj_1.insert("grapes")
        bst_obj_1.insert("bottle")

        # Reverse Alphabetical Ordering
        reverse_alpha_ordering_obj = ReverseAlphaOrdering()
        bst_obj_2 = BinarySearchTree("elite", reverse_alpha_ordering_obj)
        bst_obj_2.insert("cat")
        bst_obj_2.insert("grapes")
        bst_obj_2.insert("bottle")

        tree_visitor_obj = TraversalVisitor()
        self.assertEqual(bst_obj_1.accept_tree_visitor(tree_visitor_obj), "(elite(cat(bottle()())())(grapes()()))")
        self.assertEqual(bst_obj_2.accept_tree_visitor(tree_visitor_obj), "(elite(bottle()())(cat(grapes()())()))")


class TestBSTNode(unittest.TestCase):
    def test_accept_tree_visitor(self):
        ordering_strategy_obj = AlphaOrdering()
        bst_obj = BinarySearchTree("elite", ordering_strategy_obj)
        bst_obj.insert("cat")
        bst_obj.insert("grapes")
        bst_obj.insert("bottle")

        tree_visitor_obj = TraversalVisitor()
        self.assertEqual(bst_obj.root.left.accept_tree_visitor(tree_visitor_obj), "(cat(bottle()())())")


class TestTraversalVisitor(unittest.TestCase):
    def test_visit_bst_node(self):
        ordering_strategy_obj = AlphaOrdering()
        bst_obj = BinarySearchTree("elite", ordering_strategy_obj)
        bst_obj.insert("cat")
        bst_obj.insert("grapes")

        tree_visitor_obj = TraversalVisitor()
        self.assertEqual(tree_visitor_obj.visit_bst_node(bst_obj.root), "(elite(cat()())(grapes()()))")
# Unit Testing Ends!


def main():
    ordering_strategy_obj = AlphaOrdering()
    bst_obj = BinarySearchTree("elite", ordering_strategy_obj)

    elements_arr = ["cat", "bottle", "dog", "grapes", "fish", "house"]
    for element in elements_arr:
        bst_obj.insert(element)

    traversal_visitor_obj = TraversalVisitor()
    print(bst_obj.accept_tree_visitor(traversal_visitor_obj))


if __name__ == '__main__':
    main()
