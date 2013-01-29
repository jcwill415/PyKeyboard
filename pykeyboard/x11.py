from Xlib.display import Display
from Xlib import X
from Xlib.ext.xtest import fake_input
from Xlib.XK import string_to_keysym

from base import PyKeyboardMeta

import time

special_X_keysyms = {
    ' ' : "space",
    '\t' : "Tab",
    '\n' : "Return",  # for some reason this needs to be cr, not lf
    '\r' : "Return",
    '\e' : "Escape",
    '!' : "exclam",
    '#' : "numbersign",
    '%' : "percent",
    '$' : "dollar",
    '&' : "ampersand",
    '"' : "quotedbl",
    '\'' : "apostrophe",
    '(' : "parenleft",
    ')' : "parenright",
    '*' : "asterisk",
    '=' : "equal",
    '+' : "plus",
    ',' : "comma",
    '-' : "minus",
    '.' : "period",
    '/' : "slash",
    ':' : "colon",
    ';' : "semicolon",
    '<' : "less",
    '>' : "greater",
    '?' : "question",
    '@' : "at",
    '[' : "bracketleft",
    ']' : "bracketright",
    '\\' : "backslash",
    '^' : "asciicircum",
    '_' : "underscore",
    '`' : "grave",
    '{' : "braceleft",
    '|' : "bar",
    '}' : "braceright",
    '~' : "asciitilde"
    }

class PyKeyboard(PyKeyboardMeta):
    """The PyKeyboard implementation for X11 systems (mostly linux)."""
    def __init__(self, display=None):
        PyKeyboardMeta.__init__(self)
        self.display = Display(display)
        self.display2 = Display(display)
        self.special_key_assignment()
    
    def press_key(self, character=''):
        """
        Press a given character key. Also works with character keycodes as
        integers, but not keysyms.
        """
        try:  # Detect uppercase or shifted character
            shifted = self.is_char_shifted(character)
        except AttributeError:  # Handle the case of integer keycode argument
            fake_input(self.display, X.KeyPress, character)
            self.display.sync()
        else:
            if shifted:
                fake_input(self.display, X.KeyPress, self.shift_key)
            char_val = self.lookup_character_value(character)
            fake_input(self.display, X.KeyPress, char_val)
            self.display.sync()

    def release_key(self, character=''):
        """
        Release a given character key. Also works with character keycodes as
        integers, but not keysyms.
        """
        try:  # Detect uppercase or shifted character
            shifted = self.is_char_shifted(character)
        except AttributeError:  # Handle the case of integer keycode argument
            fake_input(self.display, X.KeyRelease, character)
            self.display.sync()
        else:
            if shifted:
                fake_input(self.display, X.KeyRelease, self.shift_key)
            char_val = self.lookup_character_value(character)
            fake_input(self.display, X.KeyRelease, char_val)
            self.display.sync()

    def tap_key(self, character='', repeat=1):
        """
        Press and release a given character key n times. Also works with
        character keycodes as integers, but not keysyms.
        """
        for i in xrange(repeat):
            self.press_key(character)
            self.release_key(character)
    
    def type_string(self, char_string, char_interval=0):
        """A convenience method for typing longer strings of characters."""
        for i in char_string:
            time.sleep(char_interval)
            self.tap_key(i)
    
    def is_char_shifted(self, character):
        """Returns True if the key character is uppercase or shifted."""
        if character.isupper():
            return True
        if character in '<>?:"{}|~!@#$%^&*()_+':
            return True
        return False

    def special_key_assignment(self):
        """
        Determines the keycodes for common special keys on the keyboard. These
        are integer values and can be passed to the other key methods.
        Generally speaking, these are non-printable codes.
        """
        #This set of keys compiled using the X11 keysymdef.h file as reference
        #They comprise a relatively universal set of keys, though there may be
        #exceptions which may come up for other OSes and vendors. Countless
        #special cases exist which are not handled here, but may be extended.
        #TTY Function Keys
        self.backspace_key = self.lookup_character_value('BackSpace')
        self.tab_key = self.lookup_character_value('Tab')
        self.linefeed_key = self.lookup_character_value('Linefeed')
        self.clear_key = self.lookup_character_value('Clear')
        self.return_key = self.lookup_character_value('Return')
        self.enter_key = self.return_key  # Because many keyboards call it "Enter"
        self.pause_key = self.lookup_character_value('Pause')
        self.scroll_lock_key = self.lookup_character_value('Scroll_Lock')
        self.sys_req_key = self.lookup_character_value('Sys_Req')
        self.escape_key = self.lookup_character_value('Escape')
        self.delete_key = self.lookup_character_value('Delete')
        #Modifier Keys
        self.shift_l_key = self.lookup_character_value('Shift_L')
        self.shift_r_key = self.lookup_character_value('Shift_R')
        self.shift_key = self.shift_l_key  # Default Shift is left Shift
        self.alt_l_key = self.lookup_character_value('Alt_L')
        self.alt_r_key = self.lookup_character_value('Alt_R')
        self.alt_key = self.alt_l_key  # Default Alt is left Alt
        self.control_l_key = self.lookup_character_value('Control_L')
        self.control_r_key = self.lookup_character_value('Control_R')
        self.control_key = self.control_l_key  # Default Ctrl is left Ctrl
        self.caps_lock_key = self.lookup_character_value('Caps_Lock')
        self.shift_lock_key = self.lookup_character_value('Shift_Lock')
        self.meta_l_key = self.lookup_character_value('Meta_L')
        self.meta_r_key = self.lookup_character_value('Meta_R')
        self.super_l_key = self.lookup_character_value('Super_L')
        self.super_r_key = self.lookup_character_value('Super_R')
        self.hyper_l_key = self.lookup_character_value('Hyper_L')
        self.hyper_r_key = self.lookup_character_value('Hyper_R')
        #Cursor Control and Motion
        self.home_key = self.lookup_character_value('Home')
        self.up_key = self.lookup_character_value('Up')
        self.down_key = self.lookup_character_value('Down')
        self.left_key = self.lookup_character_value('Left')
        self.right_key = self.lookup_character_value('Right')
        self.end_key = self.lookup_character_value('End')
        self.begin_key = self.lookup_character_value('Begin')
        self.page_up_key = self.lookup_character_value('Page_Up')
        self.page_down_key = self.lookup_character_value('Page_Down')
        self.prior_key = self.lookup_character_value('Prior')
        self.next_key = self.lookup_character_value('Next')
        #Misc Functions
        self.select_key = self.lookup_character_value('Select')
        self.print_key = self.lookup_character_value('Print')
        self.execute_key = self.lookup_character_value('Execute') 
        self.insert_key = self.lookup_character_value('Insert')
        self.undo_key = self.lookup_character_value('Undo')
        self.redo_key = self.lookup_character_value('Redo')
        self.menu_key = self.lookup_character_value('Menu')
        self.find_key = self.lookup_character_value('Find')
        self.cancel_key = self.lookup_character_value('Cancel')
        self.help_key = self.lookup_character_value('Help')
        self.break_key = self.lookup_character_value('Break')
        self.mode_switch_key = self.lookup_character_value('Mode_switch')
        self.script_switch_key = self.lookup_character_value('script_switch')
        self.num_lock_key = self.lookup_character_value('Num_Lock')
        #Keypad Keys: Dictionary structure
        keypad = ['Space', 'Tab', 'Enter', 'F1', 'F2', 'F3', 'F4', 'Home',
                  'Left', 'Up', 'Right', 'Down', 'Prior', 'Page_Up', 'Next',
                  'Page_Down', 'End', 'Begin', 'Insert', 'Delete', 'Equal',
                  'Multiply', 'Add', 'Separator', 'Subtract', 'Decimal',
                  'Divide', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.keypad_keys = {k: self.lookup_character_value('KP_'+str(k)) for k in keypad}
        self.numpad_keys = self.keypad_keys
        #Function Keys/ Auxilliary Keys
        #FKeys
        self.function_keys = [None] + [self.lookup_character_value('F'+str(i)) for i in xrange(1,36)]
        #LKeys
        self.l_keys = [None] + [self.lookup_character_value('L'+str(i)) for i in xrange(1,11)]
        #RKeys
        self.r_keys = [None] + [self.lookup_character_value('R'+str(i)) for i in xrange(1,16)]

    def lookup_character_value(self, character):
        """
        Looks up the keysym for the character then returns the keycode mapping
        for that keysym.
        """
        ch_keysym = string_to_keysym(character)
        if ch_keysym == 0:
            ch_keysym = string_to_keysym(special_X_keysyms[character])
        return self.display.keysym_to_keycode(ch_keysym)
