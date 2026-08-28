"""Stage B: the single registered read of the sealed retro cohort.

This package holds the Stage B surface and nothing else: the B.0
preconditions (counts, timestamps, and hashes only), and — after Amendment
3 registers the single blindness exemption — the sealed reader and the
one-shot CLI behind the latch. Stage B sends no network request; every
input is already on disk.
"""
