#!/usr/bin/env python2
import pygtk
pygtk.require('2.0')
import gtk, appindicator, keybinder
import os, sys
import lib.singleton
import ConfigParser

class Ui(object):
    def delete_event(self, widget, event, data=None):
        return False

    def hello(self, widget, data=None):
        print "hun?"

    def settings(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title(self.name)
        #self.window.connect("delete_event", self.delete_event)
        self.window.set_border_width(10)
        label = gtk.Label("Graphical settings not implemented yet")
        #self.button.connect("clicked", self.hello, None)
        #self.button.connect_object("clicked", gtk.Widget.destroy, self.window)
        self.window.add(label)
        label.show()
        #self.button.show()
        self.window.show()


        #keystr = "o"
        #keybinder.bind(keystr, self.callback, "nohup gmrun >> /tmp/pyhk.log &")

class Indicator(object):
    def menuitem_response(self, w, buf):
        function = {
                'exit': sys.exit,
                'settings': self.settings,
                'reload': self.handleKeys
        }[buf]()
        pass

    def startIndicator(self):
        self.ind = appindicator.Indicator("example-simple-client",
                "apple-green",
                appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status (appindicator.STATUS_ACTIVE)
        self.ind.set_attention_icon("indicator-messages-new")

        menu = gtk.Menu()

        menu_items = gtk.MenuItem('Settings')
        menu_items.connect("activate", self.menuitem_response, "settings")
        menu.append(menu_items)
        menu_items.show()

        menu_items = gtk.MenuItem('Reload')
        menu_items.connect("activate", self.menuitem_response, "reload")
        menu.append(menu_items)
        menu_items.show()

        menu_items = gtk.MenuItem("Exit")
        menu_items.connect("activate", self.menuitem_response, "exit")
        menu.append(menu_items)
        menu_items.show()
        self.ind.set_menu(menu)

class Hk(Indicator, Ui):
    boundKeys = []
    name = 'Gbindme'
    nameLower = 'gbindme'

    def __init__(self):
        self.cfgDir = os.path.expanduser('~') \
                + '/.config//'
        if not os.path.exists(self.cfgDir):
            os.makedirs(self.cfgDir)

        self.hkCfg = self.cfgDir + 'keys.cfg'
        self.keyCfg = self.cfgDir + self.nameLower + '.cfg'

        if not os.path.isfile(self.hkCfg):
            open(self.hkCfg, 'a').close()
        if not os.path.isfile(self.keyCfg):
            open(self.keyCfg, 'a').close()

    
    def callback(self, user_data):
        os.system(user_data)

    def run(self):
        me = lib.singleton.SingleInstance()
        self.handleKeys()
        self.startIndicator()
        gtk.main()

    def handleKeys(self):
        if len(self.boundKeys)>0:
            for key in self.boundKeys:
                keybinder.unbind(key)
            self.boundKeys = []

        config = ConfigParser.ConfigParser()
        config.read(self.keyCfg)
        sections = config.sections()

        for s in sections:
            cmd = config.get(s, 'Exec')
            key = config.get(s, 'Key')
            try:
                keybinder.bind(key, self.callback, "nohup " + cmd)
                self.boundKeys.append(key)
            except:
                print "Error: can't bind ", key, "key"

Hk().run()
