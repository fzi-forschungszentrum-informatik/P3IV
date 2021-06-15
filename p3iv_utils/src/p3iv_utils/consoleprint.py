#!/usr/bin/env python


class Print2Console(object):
    @staticmethod
    def get_format_options(style, bold):
        """Define the ANSI escape sequences for modifying the style of the output"""

        if style != None:
            options = {
                "bright": "1",
                "dim": "2",
                "underline": "4",
                "black": "30",
                "red": "31",
                "green": "32",
                "yellow": "33",
                "blue": "34",
                "magenta": "35",
                "cyan": "36",
                "white": "37",
            }

            code = options[style]

            if bold:
                code = "1;%s" % code
            return "\033[" + code + "m%s\033[0m"
        else:
            return ""

    @staticmethod
    def p(format_str, var, first_col_w=24, line_width=72, style=None, bold=False, decimals=2):
        """
        The variables to be printed ('var') must be added inside a list.
        First colum width is selected 24 characters long and
        total line width is limited to 72 characters.
        """

        # Initialize string
        string = ""

        # Instantiate 'Print2Console.get_format_options' as format_options
        format_options = Print2Console.get_format_options(style, bold)

        # Determine the number of items to be printed and white-spaces
        n_item = len(var)
        n_space = n_item - 1

        for i in range(n_item):
            if i == 0:
                if n_item == 1:
                    string += "%-" + str(line_width) + format_str[0]
                else:
                    string += "%-" + str(first_col_w) + format_str[0]
            else:
                # Define character (or sub-column) width for any element to be printed
                # 'n_item - 1' because the first element has already a length of 24
                col_w = (line_width - first_col_w - n_space) / (n_item - 1)

                if format_str[i] == "s":
                    string += " %" + str(col_w) + "s"
                elif format_str[i] == "i":
                    string += " %" + str(col_w) + "i"
                elif format_str[i] == "f":
                    string += " %" + str(col_w) + "." + str(decimals) + "f"

        # If format_options are defined, wrap the output
        if format_options != "":
            string = format_options % string

        # Print the format with its variables ('var')
        print(string % tuple(var))
