#!/usr/bin/python3
"""Defines a Console Module that controls all databases"""


from datetime import datetime
import cmd
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import re
import shlex


class HBNBCommand(cmd.Cmd):
    """"Command Processor Class"""
    prompt = "(hbnb) "
    doc_header = "Documented commands (type help <topic>):"
    Classes = ['BaseModel', 'User', 'State', 'City',
               'Amenity', 'Place', 'Review']

    def do_EOF(self, line):
        """Exit from the command prompt"""
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_create(self, line):
        """Creates a new instance of BaseModel, saves it (to the JSON file)
        and prints the id"""
        command = self.parseline(line)[0]

        if command is None:
            print("** class name missing **")
        elif command not in self.Classes:
            print("** class doesn't exist **")
        else:
            new_inst = eval(command)()
            print(new_inst.id)
            new_inst.save()

    def do_show(self, line):
        """Prints the string representation of an instance based
        on the class name and id"""

        classname = self.parseline(line)[0]
        classid = self.parseline(line)[1]

        if classname is None:
            print("** class name missing **")
        elif classname not in self.Classes:
            print("** class doesn't exist **")
        elif classid == '':
            print("** instance id missing **")
        else:
            data = models.storage.all().get(classname + '.' + classid)
            if data is None:
                print("** no instance found **")
            print(data)

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id"""
        classname = self.parseline(line)[0]
        classid = self.parseline(line)[1]

        if classname is None:
            print("** class name missing **")
        elif classname not in self.Classes:
            print("** class doesn't exist **")
        elif classid == '':
            print("** instance id missing **")
        else:
            key = classname + '.' + classid
            data = models.storage.all().get(key)
            if data is None:
                print("** no instance found **")
            else:
                del models.storage.all()[key]
                models.storage.save()

    def do_all(self, line):
        """Prints all string representation of all instances
        based or not on the class name.
        """
        classname = self.parseline(line)[0]
        objs = models.storage.all()
        if classname is None:
            print([str(objs[obj]) for obj in objs])
        elif classname in self.Classes:
            keys = objs.keys()
            print([str(objs[key])
                   for key in keys if key.startswith(classname)])
        else:
            print("** class doesn't exist **")

    def do_update(self, line):
        """Updates an instance based on the class name and id
            by adding or updating attribute.
        """
        args = shlex.split(line)
        args_size = len(args)
        if args_size == 0:
            print('** class name missing **')
        elif args[0] not in self.Classes:
            print("** class doesn't exist **")
        elif args_size == 1:
            print('** instance id missing **')
        else:
            key = args[0] + '.' + args[1]
            inst_data = models.storage.all().get(key)
            if inst_data is None:
                print('** no instance found **')
            elif args_size == 2:
                print('** attribute name missing **')
            elif args_size == 3:
                print('** value missing **')
            else:
                args[3] = self.analyze_parameter_value(args[3])
                setattr(inst_data, args[2], args[3])
                setattr(inst_data, 'updated_at', datetime.now())
                models.storage.save()

    def analyze_parameter_value(self, value):
        """Checks a parameter value for an update
        Analyze if a parameter is a string that needs
        convert to a float number or an integer number.
        Args:
            value: The value to analyze
        """
        if value.isdigit():
            return int(value)
        elif value.replace('.', '', 1).isdigit():
            return float(value)

        return value

    def get_objects(self, instance=''):
        """Gets the elements created by the console
        This method takes care of obtaining the information
        of all the instances created in the file `objects.json`
        that is used as the storage engine.
        When an instance is sent as an argument, the function
        takes care of getting only the instances that match the argument.
        Args:
            instance (:obj:`str`, optional): The instance to finds into
                the objects.
        Returns:
            list: If the `instance` argument is not empty, it will search
            only for objects that match the instance. Otherwise, it will show
            all instances in the file where all objects are stored.
        """
        objects = models.storage.all()

        if instance:
            keys = objects.keys()
            return [str(val) for key, val in objects.items()
                    if key.startswith(instance)]

        return [str(val) for key, val in objects.items()]

    def default(self, line):
        """
        When the command prefix is not recognized, this method
        looks for whether the command entered has the syntax:
            "<class name>.<method name>" or not,
        and links it to the corresponding method in case the
        class exists and the method belongs to the class.
        """
        if '.' in line:
            splitted = re.split(r'\.|\(|\)', line)
            class_name = splitted[0]
            method_name = splitted[1]

            if class_name in self.Classes:
                if method_name == 'all':
                    print(self.get_objects(class_name))
                elif method_name == 'count':
                    print(len(self.get_objects(class_name)))
                elif method_name == 'show':
                    class_id = splitted[2][1:-1]
                    self.do_show(class_name + ' ' + class_id)
                elif method_name == 'destroy':
                    class_id = splitted[2][1:-1]
                    self.do_destroy(class_name + ' ' + class_id)

    def emptyline(self):
        """When an empty line is entered in response to the prompt,
            it won't repeat the last nonempty command entered."""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
