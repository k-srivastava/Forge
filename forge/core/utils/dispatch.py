# TODO: All full type hints for the function.
"""
Custom function-overloading in Python using Python decorators with type-hints.
"""
import functools
import typing


def multidispatch(*types: typing.Type):
    """
    Decorator for class methods using type-hints enabling, function-overloading using dynamic dispatch.

    :param types: Types to be overloaded.
    :type types: tuple[typing.Type]
    """

    def register(function: typing.Callable):
        """
        Register the function under the decorator.

        :param function: Function to be registered.
        :type function: Callable

        # :return:

        :raises TypeError: An overloaded function with its types must be unique.
        """
        name = function.__name__
        overloaded_function = multidispatch.registry.get(name)

        if overloaded_function is None:
            @functools.wraps(function)
            def wrapper(self, *args):
                """
                Wrap the function to be overloaded and check if matches are found.

                # :param self:
                # :param args:
                #
                # :return:

                :raises TypeError: A match for the overloaded function must exist within the class.
                """
                types_ = tuple(arg.__class__ for arg in args)
                function_ = wrapper.type_map.get(types_)

                if function_ is None:
                    raise TypeError('No match for overloaded function found.')

                return function_(self, *args)

            wrapper.type_map = {}
            overloaded_function = multidispatch.registry[name] = wrapper

        if types in overloaded_function.type_map:
            raise TypeError('Duplicate registrations for overloaded functions are not allowed.')

        overloaded_function.type_map[types] = function
        return overloaded_function

    return register


multidispatch.registry = {}
