import unittest

def nonNone(positions = None):
    def decorator(function):
        def wrapper(*args):

            none_position_list = []

            if positions != None:
                for position in positions:
                    if args[position] is None:
                        none_position_list.append(position)

                if none_position_list:                                          
                    raise ValueError(f"Przekazałeś argument None na pozycji {none_position_list}")
            
            else:
                for position, arg in enumerate(args):
                    if arg is None:
                        none_position_list.append(position)

                if none_position_list:                                          
                    raise ValueError(f"Przekazałeś argument None na pozycji {none_position_list}")


            return function(*args)
        return wrapper
    return decorator

@nonNone()
def multiply(a, b):
    return a*b

@nonNone([0,1])
def add(a, b, c ):
    return a+b

class ATestCase(unittest.TestCase):

    def test1(self):
        self.assertRaises(ValueError, multiply(None,None))  #problem ze sprawdzeniem 
    def test2(self):
        self.assertEqual(2, multiply(1,2))  

    def test3(self):
        self.assertRaises(ValueError, add(1,None,1))  #problem ze sprawdzeniem 
    def test4(self):
        self.assertEqual(2, add(1,1,None)) 
   
unittest.main()

