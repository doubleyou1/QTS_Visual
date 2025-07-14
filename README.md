# QTS_Visual

Visualisieren verschiedener crystal structurs



Dokumentation/ Idee:

Gitter Klasse erstellen

init sollte folgende Input haben:
Input:
    - Länge in x Richtung
    - Länge in y Richtung
    - Länge in z Richtung
    - Atom Abstand in x Richtung
    - Atom Abstand in y Richtung
    - Atom Abstand in z Richtung
    - Atom Basis: array mit vectoren
    - Simple Cubic, Face centred cubic, body centred cubic, hexagonal close packing, hexagonal cubic close packing
    - lattice basis vectors

Global Attribute:
    - countable_lattice: 3D array. Adressiert die Atome über abzählen. Also [2][1][3][0] wäre das 3 Atom in X, Richtung, 2 Atom in Y Richtung und 4 Atom in Z Richtung, 1 Atom in der Basis
        - eigentlich unnötig geworden
    - metric_lattice: 3D array. Adressiert die Atome über die metrische Position im Raum. z.B. Atomic Spacing in alle Richtungen ist 1 nm. (3, 2, 4) für das Beispiel zuvor. Wenn jetzt aber das zweite Atom aus der Basis gemeint ist [2][1][3][1] (Basis Vektoren sind (0,0,0) und (1/2, 1/2, 1/2)), dann (3.5, 2.5, 4.5)

