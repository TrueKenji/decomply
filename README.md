<h1>decomply</h1>
decomply (decomposeApply) is a short utility package, providing functionality to traverse nested dictionaries (or any enumerable object) and apply a custom function on their values.

Supports also lists, using their indexes as key. Additionally, custom handlers can be supplied to extend support to more types.

<h3>Example:</h3>
Consider a dictionary like this

~~~
input_data = {
    "First Layer": {
        "Second layer": 3,
        "Second layer 2nd element": 4
    },
    "First layer 2nd element": -1
}
~~~

Suppose you want to increment the numbers by 1. Then you can use

~~~
Decomply(
  apply=lambda _, item: item + 1
  ).decomply(input_data)
~~~

Output

~~~
{
  "First Layer": {
      "Second layer": 4,
      "Second layer 2nd element": 5
  },
  "First layer 2nd element": 0
}
~~~

decomply will traverse the dictionary, stopping at certain points. Then it will apply the desired function on the value at hand and "repeat" the process. In a sense, it decomposes the object into a partition and then applies a function on each part, hence the name decomposeApply, in short `decomply`

<h2>Install</h2>

`pip install decomply`

<h2>API</h2>

<h3>Decomply</h3>

The constructor's signature is 

~~~
def __init__(
    self,
    traverse: callable = lambda trace, item: True,
    apply: callable = lambda trace, item: item,
    delete: callable = lambda trace, item: str(trace[-1]).startswith("_"),
    handlers: set[EnumerableHandler] = None
):
~~~

Decomply accepts 4 parameters, each with a default value.
The first 3 parameters are callables, which all receive two parameters:
~~~
trace: a list of keys, reflecting the path to traverse to the current item
item: the current value
~~~

The callables are

~~~
apply: lambda: trace, item: item
~~~

`apply` is the function to be applied on the single items.  It defaults to returning the original item

~~~
traverse: lambda: trace, item: True
~~~

`traverse` allows to specify whether to keep traversing. If the function evaluates to `False`, traversal is stopped and `apply` is applied to the current item

~~~
delete: lambda: trace, item: str(trace[-1]).startswith("_")
~~~

`delete` allows to drop key/values entirely. Defaults to dropping those keys, which start with _, allowing a commenting-like functionality (especially useful when dealing with jsons).

The fourth parameter is a set of objects implementing the EnumerableHandler interface. Such a handler must be able to iterate through an associated object type and offer some more methods to handle.

<h2>decomply</h2>

To invoke, the decomply method is used. It's signature is

~~~
def decomply(self, item: Union[dict, list], trace: List[Union[str, int]] = None, initial_check: bool = True) -> dict:
~~~

It accepts 3 parameters:

~~~
item: Union[dict, list]
~~~

`item` is the object to decomply, either a nested dict or list. Both types can appear interchangeably within.

~~~
trace: List[Union[str, int]] = None
~~~

`trace` is a list of keys, which are used to traverse the item until a certain place. Typically this trace is initialized as an empty list

~~~
initial_check: bool = True
~~~

`initial_check` is a boolean indicating whether the passed item should already be tested against `self.traverse`.

<h3>Complete Example</h3>

Let's take the following input

~~~
input_data = {
    "First Layer": {
        "Second layer": 3,
        "_Second layer 2nd element": 4,
        "Second layer 3rd element": [
            42,
            69
        ]
    },
    "First layer 2nd element": {
        "fuu": {
            "fuu 1st entry": 6,
            "fuu 2nd entry": 10,
            "fuu 3rd entry": {
                "I will be dropped": 0
            }
        }
    }
}

Decomply(
    traverse = lambda _, item: not isinstance(item, list),
    apply = lambda _, item: item + [666] if isinstance(item, list) else item + 1,
    delete = lambda trace, _: len(trace) > 3
).decomply(input_data)
~~~

- traverse the dict as long as 
    - the next item is not a list
    - AND: the item is enumerable (<- this is a mandatory part of the traverse condition always attached within Decomply constructor) 
- When either condition fails, check out the item at hand. If it is
    - a list, extend it with the value 666
    - not a list, increment it by 1
- Delete all layers with a depth greater than 3

Output

~~~
{
    "First Layer": {
        "Second layer": 4,
        "_Second layer 2nd element": 5,
        "Second layer 3rd element": [
            42,
            69,
            666
        ]
    },
    "First layer 2nd element": {
        "fuu": {
            "fuu 1st entry": 7,
            "fuu 2nd entry": 11,
            "fuu 3rd entry": {}
        }
    }
}
~~~

I published a use case in my [jsgui](https://github.com/TrueKenji/jsgui) package, feel free to check it out for more complex examples.