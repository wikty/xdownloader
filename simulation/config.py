import os

# Ghost Driver is a pure JavaScript implementation of 
# the WebDriver Wire Protocol for PhantomJS.
# GhostDriver is designed to be integral part of PhantomJS itself.
GHOST_DRIVER_PATH = os.path.abspath(os.path.join('..', 'bin', 'phantomjs-2.1.1-windows', 'phantomjs.exe'))
# Proxy for using W3C WebDriver-compatible clients to interact 
# with Gecko-based browsers, such as firefox.
GECKO_DRIVER_PATH = os.path.abspath(os.path.join('..', 'bin', 'geckodriver-v0.18.0-win32', 'geckodriver.exe'))