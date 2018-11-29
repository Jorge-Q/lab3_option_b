# Jorge Quinonez
# Student ID:80610688
# Professor: Diego Aguirre


class avl_node: # Class for the avl-tree node
    def __init__(self, value):
        self.value = value
        self.left_child = None
        self.right_child = None
        self.parent = None
        self.height = 0

    def get_balance(self):
        left_height = -1
        if self.left_child is not None:
            left_height = self.left_child.height
        right_height = -1
        if self.right_child is not None:
            right_height = self.right_child.height
        return left_height - right_height

    def update_height(self):
        left_height = -1
        if self.left_child is not None:
            left_height = self.left_child.height
        right_height = -1
        if self.right_child is not None:
            right_height = self.right_child.height
        self.height = max(left_height, right_height) + 1

    def set_child(self, which_child, child):
        if which_child != "left" and which_child != "right":
            return False
        if which_child == "left":
            self.left_child = child
        else:
            self.right_child = child
        if child is not None:
            child.parent = self
        self.update_height()
        return True

    def replace_child(self, current_child, new_child):
        if self.left_child is current_child:
            return self.set_child("left", new_child)
        elif self.right_child is current_child:
            return self.set_child("right", new_child)
        return False


class avl_tree(object): # Class for the AVL tree
    def __init__(self):
        self.root = None

    def get_height(self, current):
        if current is None: return 0
        return current.height

    def insert(self, value):  # Insertion method for the avl tree
        node = avl_node(value)
        if self.root is None:  # If the tree is empty, new node is the root
            self.root = node
            self.root.parent = None
            return
        cur = self.root
        while cur is not None:  # Insertion as a standard binary search tree
            if node.value < cur.value:
                if cur.left_child is None:
                    cur.left_child = node
                    node.parent = cur
                    cur = None
                else:
                    cur = cur.left_child

            else:
                if cur.right_child is None:
                    cur.right_child = node
                    node.parent = cur
                    cur = None

                else:
                    cur = cur.right_child
        node = node.parent
        while node is not None:  # Rebalance from the new node's parent up
            self.rebalance(node)
            node = node.parent


    def rebalance(self, node): # Method to rebalance an avl tree
        node.update_height()
        if node.get_balance() == -2:
            if node.right_child.get_balance() == 1:
                #Double rotation case
                self.right_rotate(node.right_child)
            return self.left_rotate(node)
        elif node.get_balance() == 2:
            if node.left_child.get_balance() == -1:
                #Double rotation case
                self.left_rotate(node.left_child)
            return self.right_rotate(node)
        return node

    def right_rotate(self, node):  # Right rotation for the avl tree
        left_right_child = node.left_child.right_child
        if node.parent is not None:
            node.parent.replace_child(node, node.left_child)
        else:
            self.root = node.left_child
            self.root.parent = None

        node.left_child.set_child('right', node)
        node.set_child('left', left_right_child)

        return node.parent

    def left_rotate(self, node):  # Left rotation for the avl tree
        right_left_child = node.right_child.left_child
        if node.parent is not None:
            node.parent.replace_child(node, node.right_child)
        else:
            self.root = node.right_child
            self.root.parent = None

        node.right_child.set_child("left", node)
        node.set_child("right", right_left_child)

        return node.parent

    def search(self, value):  # Search method for the avl tree
        temp = self.root
        while temp is not None:
            if temp.value == value:
                return True
            elif temp.value < value:
                temp = temp.right_child
            else:
                temp = temp.left_child
        return False


class rbt_node(object): # Class node for red-black tree
    def __init__(self, key, parent, is_red=False, left=None, right=None):
        self.key = key
        self.left_child = left
        self.right_child = right
        self.parent = parent
        if is_red:
            self.color = "red"
        else:
            self.color = "black"

    def both_children_black(self): # Method that returns true if both children are black
        if self.left_child is not None and self.left_child.is_red():
            return False
        if self.right_child is not None and self.right_child.is_red():
            return False
        return True

    def count(self):
        count = 1
        if self.left_child is not None:
            count += self.left_child.count()
        if self.right_child is not None:
            count += self.right_child.count()
        return count

    def get_grandparent(self): # Method that returns the grandparent of given node
        if self.parent is None:
            return None
        return self.parent.parent

    def get_siblings(self):# Method that returns the node's sibling
        if self.parent is not None:
            if self is self.parent.left_child:
                return self.parent.right_child
            return self.parent.left_child
        return None

    def get_uncle(self):# Method that returns the node's uncle
        grandparent = self.get_grandparent()
        if grandparent is None:
            return None
        if grandparent.left_child is self.parent:
            return grandparent.right_child
        return grandparent.left_child

    def is_black(self): # Checks if node is black
        return self.color == "black"

    def is_red(self): # Checks if node is red
        return self.color == "red"

    def replace_child(self, current_child, new_child):
        if self.left_child is current_child:
            return self.set_child("left", new_child)
        elif self.right_child is current_child:
            return self.set_child("right", new_child)
        return False

    def set_child(self, which_child, child):
        if which_child is not "left" and which_child is not "right":
            return False
        if which_child == "left":
            self.left_child = child
        else:
            self.right_child = child
        if child is not None:
            child.parent = self
        return True


class rb_tree(object): # Class for the red-black-tree
    def __init__(self):
        self.root = None

    def insert(self, key):
        new_node = rbt_node(key, None, True, None, None)
        self.insert_node(new_node)

    def insert_node(self, new_node):
        if self.root is None:  # If the root is empty
            self.root = new_node
        else:
            temp = self.root
            while temp is not None:
                if new_node.key < temp.key:
                    if temp.left_child is None:
                        temp.set_child("left", new_node)
                        break
                    else:
                        temp = temp.left_child
                else:
                    if temp.right_child is None:
                        temp.set_child("right", new_node)
                        break
                    else:
                        temp = temp.right_child

        new_node.color = "red"  # Set to red
        self.insertion_balance(new_node)  # Balance with the new node

    def insertion_balance(self, new_node):
        if new_node.parent is None: #If the bode is tree's root, color black
            new_node.color = "black"
            return

        if new_node.parent.is_black(): #If parent is black then we return
            return

        parent = new_node.parent #Saving parent, grandparent, and uncle node
        grandparent = new_node.get_grandparent()
        uncle = new_node.get_uncle()

        if uncle is not None and uncle.is_red(): #If parent and uncle red, change to black, color grandparent red
            parent.color = uncle.color = "black"
            grandparent.color = "red"
            self.insertion_balance(grandparent)
            return

        if new_node is parent.right_child and parent is grandparent.left_child:
            self.left_rotate(parent)
            new_node = parent
            parent = new_node.parent

        elif new_node is parent.left_child and parent is grandparent.right_child:
            self.right_rotate(parent)
            new_node = parent
            parent = new_node.parent

        parent.color = "black"
        grandparent.color = "red"

        if new_node is parent.left_child:
            self.right_rotate(grandparent)
        else:
            self.left_rotate(grandparent)

    def right_rotate(self, selected_node):  # Method that performs a right rotation
        left_right_child = selected_node.left_child.right_child
        if selected_node.parent is not None:
            selected_node.parent.replace_child(selected_node, selected_node.left_child)
        else:
            self.root = selected_node.left_child
            self.root.parent = None
        selected_node.left_child.set_child("right", selected_node)
        selected_node.set_child("left", left_right_child)

    def left_rotate(self, selected_node):  # Method that performs a left rotation
        right_left_child = selected_node.right_child.left_child
        if selected_node.parent is not None:
            selected_node.parent.replace_child(selected_node, selected_node.right_child)
        else:
            self.root = selected_node.right_child
            self.root.parent = None
        selected_node.right_child.set_child("left", selected_node)
        selected_node.set_child("right", right_left_child)

    def search(self, key):
        temp = self.root
        while temp is not None:
            if temp.key == key:
                return True
            elif key < temp.key:
                temp = temp.left_child
            else:
                temp = temp.right_child
        return False


# Methods required by the lab


def print_anagrams(word, prefix=""): # Method given to us by lab
    if len(word) <= 1:
        str = prefix + word
        if english_words.search(str):
            print(prefix + word)
    else:
        for i in range(len(word)):
            cur = word[i:i + 1]
            before = word[0:i]  # Letters before cur
            after = word[i+1:]  # Letters after cur

            if cur not in before:
                print_anagrams(before + after, prefix + cur)


def count_anagrams(word, prefix=""):  # Method to count the number of anagrams a word contains
    if len(word) <= 1:
        str = prefix + word
        if english_words.search(str):
            return 1
        else:
            return 0
    else:
        count = 0
        for i in range(len(word)):
            cur = word[i: i + 1]
            before = word[0: i]
            after = word[i + 1:]
            if cur not in before:
                count += count_anagrams(before + after, prefix + cur)
        return count


def max_anagrams_from_file(file_name):  # Method to find the word with the most anagrams in a file
    file = open(file_name, "r")
    max_count = 0
    max_word = ""
    for line in file:  # For every line in the file
        count = count_anagrams(line[0:-1])
        print("The word ", line[0:-1], " has:", count, " anagrams")
        if count > max_count:
            max_count = count
            max_word = line[0:-1]
    print("The word with the most anagrams is ", max_word, " with ", max_count," anagrams")


def create_tree(type, filename):  # Creates a tree based on the user's answer
    global english_words
    file = open(filename)
    if type == '1':  # If the user wants an avl tree
        english_words = avl_tree()
        for line in file:
            english_words.insert(line[:-1].lower())
        print("The avl-tree has been created")
    elif type == '2':  # If the user wants an rb tree
        english_words = rb_tree()
        for line in file:
            english_words.insert(line[:-1].lower())
        print("The red-black-tree has been created")
    else:  # If the user entered an invalid number
        print("Invalid answer")
        return False
    return True


def main():
    try:
        action = input("Would you like to use an AVL tree or a Red-Black tree(Enter 1 for AVl, Enter 2 for Red-Black Tree)\n")
        file_name = input("Enter the name of the file you would like to use:\n")
        create_tree(action, file_name)
        print("*************************************")
        word = input("Please enter a word for which you would like to test the anagrams method:\n")
        print_anagrams(word.lower())
        print("The total number of anagrams for ", word, " is", count_anagrams(word.lower()))
        print("*************************************")
        print("We will now find the word in the file with the most anagrams")
        max_anagrams_from_file(file_name)
    except:
        print("An error has ocurred! The program will now close")



main()