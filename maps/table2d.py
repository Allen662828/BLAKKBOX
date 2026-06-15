class Table2DStructure:

    def matches(self, rows, cols):

        return (rows == 1 and cols > 1) or \
               (cols == 1 and rows > 1)
