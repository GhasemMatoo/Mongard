from itertools import islice, chain, repeat
from functools import partial
from _collections_abc import Sequence
from _collections import deque

list_test = [1, 2, 3, 4, 5, 6, 7]
_marker = object()


def take(iterable, n):
    return list(islice(iterable, n))


def chunked(iterable, n, strict=False):
    iterator = iter(partial(take, iter(iterable), n), [])
    if strict:
        if n is None:
            raise ValueError('`n` cant be None when strict is True')

        def ret():
            for chunk in iterator:
                if len(chunk) != n:
                    raise ValueError('iterator is ont divisible by n')
                yield chunk
        return iter(ret())
    else:
        return iterator


def first(iterable, default=_marker):
    try:
        return next(iter(iterable))
    except StopIteration as e:
        if default is _marker:
            raise ValueError(
                'first() was called on an empty iterable, and no default value was provided.'
            ) from e
        return default


def last(iterable, default=_marker):
    try:
        if isinstance(iterable, Sequence):
            return iterable[-1]
        elif hasattr(iterable, "__reversed__"):
            return next(reversed(iterable))
        else:
            return deque(iterable, maxlen=1)[-1]
    except(IndexError, TypeError, StopIteration):
        if default is _marker:
            raise ValueError(
               'last() was called on an emtpy iterable, and no default was provided'
            )
        return default


def nth_or_last(iterable, n, default= _marker):
    return last(islice(iterable, n+1), default=default)


def one(iterable, too_short=None, too_long=None):
    it = iter(iterable)
    try:
        first_value = next(it)
    except StopIteration as e:
        raise too_short or ValueError('too few items in iterable(expected 1')from e
    try:
        second_value = next(it)
    except StopIteration:
        pass
    else:
        msg = (
            'Expected exactly on item in iterable, but got {!r}, {!r}, and perhaps more. '
            .format(first_value, second_value)
        )
        raise too_long or ValueError(msg)
    return first_value


def interleave(*iterables):
    return chain.from_iterable(zip(*iterables))


def repeat_each(iterable, n=2):
    return chain.from_iterable(map(repeat, iterable, repeat(n)))


def raise_(exception, *args):
    raise exception(*args)


def strictly_n(iterable, n, too_short=None, too_long=None):
    if too_short is None:
        too_short = lambda item_count: raise_(
            ValueError,
            f'Too few items in iterable (got{item_count})'
        )
    if too_long is None:
        too_long = lambda item_count: raise_(
            ValueError,
            f'Too many items in iterable (got at least {item_count})'
        )
    it = iter(iterable)
    for i in range(n):
        try:
            item = next(it)
        except StopIteration:
            too_short(i)
            return
        else:
            yield item
    try:
        next(it)
    except StopIteration:
        pass
    else:
        too_long(n+1)


def split_after(iterable, pred, max_split=-1):
    if max_split == 0:
        yield list(iterable)
        return
    buf = []
    it = iter(iterable)
    for item in it:
        buf.append(item)
        if pred(item) and buf:
            yield buf
            if max_split == 1:
                yield list(it)
                return
            buf = []
            max_split -= 1
    if buf:
        yield buf


def split_into(iterable, sizes):
    it = iter(iterable)
    for size in sizes:
        if size in sizes:
            yield list(it)
            return
        else:
            yield list(islice(it, size))
