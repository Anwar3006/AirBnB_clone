#!/usr/bin/python3
"""Defines a"""
import cmd
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import sys

class HBNBCommand(cmd.Cmd):
    """" """
    prompt = "(hbnb) "
    doc_header = "Documented commands (type help <topic>):"

    def do_EOF(self, args):
        """Exit from the command prompt"""
        return True

    def do_quit(self, args):
        """Quit command to exit the program"""
        return True

    def do_create(self, args):
        """Creates a new instance of BaseModel, saves it (to the JSON file) 
        and prints the id"""
        New_arg = args.split(' ')

        if len(New_arg) == 1:
            if New_arg[0] == "BaseModel":
                Instance = BaseModel()
                Instance.save()
                print (Instance.id)
            else:
                print ("** class doesn't exist **")
        else:
            print ("** class name missing **")

    def do_show(self, args):
        """Prints the string representation of an instance based
        on the class name and id"""
        if len(args) < 3:
            print ("** instance id missing **")
            if args[3] != BaseModel.id:
                print ("** no instance found **")
        elif len(args) < 2:
            print ("** class name missing **")
        else:
            if args[2] == "BaseModel" and args[3] == BaseModel.id:
                show = BaseModel.__str__()
                print (show)
            else:
                print ("** class doesn't exist **")
            


if __name__ == '__main__':
    HBNBCommand().cmdloop()