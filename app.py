print("""
# Brightness Reducer - HarshXor (Afrizal F.A) | R&D incrustwerush.org
""")

import time
import signal
import argparse
from Cocoa import NSApplication, NSWindow, NSBorderlessWindowMask, NSBackingStoreBuffered, NSColor, NSEvent
from AppKit import NSScreen


class DimOverlay:
    def __init__(self, alpha=0.3):
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        self.app = NSApplication.sharedApplication()
        self.alpha = alpha

        screen = NSScreen.mainScreen()
        frame = screen.frame()

        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            frame,
            NSBorderlessWindowMask,
            NSBackingStoreBuffered,
            False
        )
        self.window.setBackgroundColor_(
            NSColor.blackColor().colorWithAlphaComponent_(self.alpha)
        )
        self.window.setLevel_(9999)
        self.window.setIgnoresMouseEvents_(True)
        self.window.makeKeyAndOrderFront_(None)

        self.running = True

    def set_alpha(self, value):
        if value < 0:
            value = 0
        if value > 1:
            value = 1
        self.alpha = value
        self.window.setBackgroundColor_(
            NSColor.blackColor().colorWithAlphaComponent_(self.alpha)
        )

    def run(self):
        while self.running:
            event = self.app.nextEventMatchingMask_untilDate_inMode_dequeue_(
                (1 << 18),
                None,
                "kCFRunLoopDefaultMode",
                True
            )
            if event:
                self.app.sendEvent_(event)
                if event.type() == 10 and event.keyCode() == 53:  # ESC
                    self.running = False
            time.sleep(0.01)
        self.app.terminate_(None)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Screen dim overlay for macOS")
    parser.add_argument("--alpha", type=float, default=0.3,
                        help="Overlay darkness between 0.0 (no dim) and 1.0 (full black)")
    args = parser.parse_args()

    overlay = DimOverlay(alpha=args.alpha)
    overlay.run()
