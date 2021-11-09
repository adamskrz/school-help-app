from functools import wraps

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock


def yield_to_sleep(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        gen = func()
        def next_step(*_):
            try:
                t = next(gen)  # this executes 'func' before next yield and returns control to you
            except StopIteration:
                pass
            else:
                Clock.schedule_once(next_step, t)  # having control you can resume func execution after some time
        next_step()
    return wrapper


@yield_to_sleep  # use this decorator to cast 'yield' to non-blocking sleep
def test_function():
    for i in range(10):
        if (i % 2 == 0):
            yield 5  # use yield to "sleep"
            print('Called')
        else:
            print('Whatever')


class TestApp(App):
    def build(self):
        test_function()
        return BoxLayout()


if __name__ == '__main__':
    TestApp().run()