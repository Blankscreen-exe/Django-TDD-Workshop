# Django-TDD-Workshop


### Resource
- [Harry Percival - Introduction to TDD with Django - PyCon 2018](https://www.youtube.com/watch?v=_rLPDxpXIFc&list=PLE-U1jn4wS02YkS4uHmGEbwUdaWTWG4Uv)
- [Obey The Testing Goat](https://www.obeythetestinggoat.com/)
- [Django tests with nose and coverage](https://medium.com/@Zaccc123/django-tests-with-nose-and-coverage-dff5d3633b4b)
- [Django testing docs](https://django-testing-docs.readthedocs.io/en/latest/coverage.html#coverage-reports)

### Notes

- change `collection` import in `venv/lib/python3.10/site-packages/nose/suite.py` to
```py
import collections
collections.Callable = collections.abc.Callable
```