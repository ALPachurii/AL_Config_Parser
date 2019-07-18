AL Config Parser
================

Azur Lane configuration file parser library

==========
How to use
==========

create ConfigParser object and access game info using it.

example:

.. code:: python

   from ConfigParser import ConfigParser
   parser = ConfigParser(path)

   # creates a meta ship object
   parser.getMetaShip(metaId)

   # creates a buff object
   parser.getRootBuff(buffId)
