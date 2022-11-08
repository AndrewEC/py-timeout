Usage
=====

.. toctree::
   :maxdepth: 4


The timeout utility can be used simply by importing the timeout decorator and applying it to a function
like in the example below::

    from timeout import timeout

    @timeout(3)  # 3 is the number of seconds to wait before the timeout occurs
    def perform_action():
        ...

**Note**: This decorator was only intended to be used on blocking, non-async, functions.