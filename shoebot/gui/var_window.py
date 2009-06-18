#!/usr/bin/env python
import sys
import gtk

NUMBER = 1
TEXT = 2
BOOLEAN = 3
BUTTON = 4

if sys.platform != 'win32':
    ICON_FILE = '/usr/share/shoebot/icon.png'
else:
    import os.path
    ICON_FILE = os.path.join(sys.prefix, 'share', 'shoebot', 'icon.png')

class VarWindow:
    def __init__(self, parent, bot):
        self.parent = parent

        self.window = gtk.Window()
        self.window.set_destroy_with_parent(True)
        self.window.connect("destroy", self.do_quit)
        vbox = gtk.VBox(homogeneous=True, spacing=20)

        # set up sliders
        self.variables = []

        for item in bot.vars:
            self.variables.append(item)
            if item.type is NUMBER:
                self.add_number(vbox, item)
            elif item.type is TEXT:
                self.add_text(vbox, item)
            elif item.type is BOOLEAN:
                self.add_boolean(vbox, item)
            elif item.type is BUTTON:
                self.add_button(vbox, item)

        self.window.add(vbox)
        self.window.set_size_request(400,35*len(self.variables))
        self.window.show_all()
        ## gtk.main()

    def add_number(self, container, v):
        # create a slider for each var
        sliderbox = gtk.HBox(homogeneous=False, spacing=0)
        label = gtk.Label(v.name)
        sliderbox.pack_start(label, False, True, 20)

        adj = gtk.Adjustment(v.value, v.min, v.max, .1, 2, 1)
        adj.connect("value_changed", self.cb_set_var, v)
        hscale = gtk.HScale(adj)
        hscale.set_value_pos(gtk.POS_RIGHT)
        sliderbox.pack_start(hscale, True, True, 0)
        container.pack_start(sliderbox, True, True, 0)

    def add_text(self, container, v):
        textcontainer = gtk.HBox(homogeneous=False, spacing=0)
        label = gtk.Label(v.name)
        textcontainer.pack_start(label, False, True, 20)

        entry = gtk.Entry(max=0)
        entry.set_text(v.value)
        entry.connect("changed", self.cb_set_var, v)
        textcontainer.pack_start(entry, True, True, 0)
        container.pack_start(textcontainer, True, True, 0)

    def add_boolean(self, container, v):
        buttoncontainer = gtk.HBox(homogeneous=False, spacing=0)
        button = gtk.CheckButton(label=v.name)
        # we send the state of the button to the callback method
        button.connect("toggled", self.cb_set_var, v)

        buttoncontainer.pack_start(button, True, True, 0)
        container.pack_start(buttoncontainer, True, True, 0)


    def add_button(self, container, v):
        buttoncontainer = gtk.HBox(homogeneous=False, spacing=0)
        # in buttons, the varname is the function, so we use __name__
        button = gtk.Button(label=v.name.__name__)
        button.connect("clicked", self.parent.bot.namespace[v.name], None)
        buttoncontainer.pack_start(button, True, True, 0)
        container.pack_start(buttoncontainer, True, True, 0)


    def do_quit(self, widget):
        pass

    def cb_set_var(self, widget, v):
        ''' Called when a slider is adjusted. '''
        # set the appropriate bot var
        if v.type is NUMBER:
            self.parent.drawingarea.bot.namespace[v.name] = widget.value
        elif v.type is BOOLEAN:
            self.parent.drawingarea.bot.namespace[v.name] = widget.get_active()
        elif v.type is TEXT:
            self.parent.drawingarea.bot.namespace[v.name] = widget.get_text()
        # and redraw the canvas
        self.parent.drawingarea.redraw()


