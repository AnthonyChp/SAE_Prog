"""
.. module:: exemple_ecriture_module
   :platform: Unix, windows
   :synopsis: exemple d'écriture d'un module pour autodoc par sphinx

.. moduleauthor:: Nom Prenom <prenom.nom@etu.univ-poitiers.fr>


"""

def fonction1(param1, param2):
    """ Cette fonction fait quelque chose.

    :param param1: premier paramètre.
    :type param1: str
    :param param2: deuxième paramètre.
    :type param2: bool
    :returns: description de la variable retournée.
    :rtype: int
    :raises: TypeError
    :example:
    
    .. code-block:: python

     entier = fonction1("toto", True)

    """
    return 0
