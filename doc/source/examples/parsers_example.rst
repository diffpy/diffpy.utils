.. _Parsers Example:

:tocdepth: -1

Parsers Example
###############

This example will demonstrate how diffpy.utils lets us easily process and serialize files.
Using the parsers module, we can load file data into simple and easy-to-work-with Python objects.

1) To begin, unzip :download:`parser_data<./example_data/parser_data.zip>` and take a look at ``data.txt``.
   Our goal will be to extract and serialize the data table as well as the parameters listed in the header of this file.

2) To get the data table, we will use the ``loadData`` function. The default behavior of this
   function is to find and extract a data table from a file.::

     from diffpy.utils.parsers.loaddata import loadData
     data_table = loadData('<PATH to data.txt>')

   While this will work with most datasets, on our ``data.txt`` file, we got a ``ValueError``. The reason for this is
   due to the comments ``$ Phase Transition Near This Temperature Range`` and ``--> Note Significant Jump in Rw <--``
   embedded within the dataset. To fix this, try using the ``comments`` parameter. ::

     data_table = loadData('<PATH to data.txt>', comments=['$', '-->'])

   This parameter tells ``loadData`` that any lines beginning with ``$`` and ``-->`` are just comments and
   more entries in our data table may follow.

   Here are a few other parameters to test out:

   * ``delimiter=','``: Look for a comma-separated data table. Useful for csv file types.
     However, since ``data.txt`` is whitespace separated, running ::

       loadData('<PATH to data.txt>', comments=['$', '-->'], delimiter=',')

     returns an empty list.
   * ``minrows=50``: Only look for data tables with at least 50 rows. Since our data table has much less than that many
     rows, running ::

       loadData('<PATH to data.txt>', comments=['$', '-->'], minrows=50)

     returns an empty list.
   * ``usecols=[0, 3]``: Only return the 0th and 3rd columns (zero-indexed) of the data table. For ``data.txt``, this
     corresponds to the temperature and rw columns. ::

       loadData('<PATH to data.txt>', comments=['$', '-->'], usecols=[0, 3])

3) Next, to get the header information, we can again use ``loadData``,
   but this time with the ``headers`` parameter enabled. ::

     hdata = loadData('<PATH to data.txt>', comments=['$', '-->'], headers=True)

4) Rather than working with separate ``data_table`` and ``hdata`` objects, it may be easier to combine them into a single
   dictionary. We can do so using the ``serialize_data`` function. ::

     from diffpy.utils.parsers.loaddata import serialize_data
     file_data = serialize_data('<PATH to data.txt', hdata, data_table)
     # File data is a dictionary with a single key
     # The key is the file name (in our case, 'data.txt')
     # The entry is a dictionary containing data from hdata and data_table
     data_dict = file_data['data.txt']

   This dictionary ``data_dict`` contains all entries in ``hdata`` and an additional entry named
   ``data table`` containing ``data_table``. ::

     here_is_the_data_table = data_dict['data table']

   There is also an option to name columns in the data table and save those columns as entries instead. ::

     data_table_column_names = ['temperature', 'scale', 'stretch', 'rw']  # names of the columns in data.txt
     file_data = serialize_data('<PATH to data.txt>', hdata, data_table, dt_colnames=data_table_column_names)
     data_dict = file_data['data.txt']

   Now we can extract specific data table columns from the dictionary. ::

     data_table_temperature_column = data_dict['temperature']
     data_table_rw_column = data_dict['rw']

5) When we are done working with the data, we can store it on disc for later use. This can also be done using the
   ``serialize_data`` function with an additional ``serial_file`` parameter.::

     parsed_file_data = serialize_data('<PATH to data.txt>', hdata, data_table, serial_file='<PATH to serialfile.json>')

   The returned value, ``parsed_file_data``, is the dictionary we just added to ``serialfile.json``.
   To extract the data from the serial file, we use ``deserialize_data``. ::

     from diffpy.utils.parsers.serialization import deserialize_data
     parsed_file_data = deserialize_data('<PATH to serialdata.json>')

6) Finally, ``serialize_data`` allows us to store data from multiple text file in a single serial file. For one last bit
   of practice, we will extract and add the data from ``moredata.txt`` into the same ``serialdata.json`` file.::

     data_table = loadData('<PATH to moredata.txt>')
     hdata = loadData('<PATH to moredata.txt>', headers=True)
     serialize_data('<PATH to moredata.txt>', hdata, data_table, serial_file='<PATH to serialdata.json>')

   The serial file ``serialfile.json`` should now contain two entries: ``data.txt`` and ``moredata.txt``.
   The data from each file can be accessed using ::

     serial_data = deserialize_data('<PATH to serialdata.json>')
     data_txt_data = serial_data['data.txt']  # Access data.txt data
     moredata_txt_data = serial_data['moredata.txt']  # Access moredata.txt data

For more information, check out the :ref:`documentation<Parsers Documentation>` of the ``parsers`` module.
