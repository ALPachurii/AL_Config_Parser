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

============================
Style guide for contributors
============================

1) The paradigm should be mainly functional

2) Docstring should use sphinx style

3) Naming should use java style, that is, upper camel case for class and file names and lower camel case otherwise
